#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Latency Tracker
Tracks latency between a "start" and "stop" user action, maps delays to Pause vs Smooth,
and optionally emits PLD-compatible events (JSONL) for the metrics pipeline.

Usage (interactive):
  python latency_tracker.py
  # Press Enter once to start, Enter again to stop.

Optional flags:
  --threshold-ms 800            # pause threshold (ms), default 800
  --csv pause_log.csv           # CSV log path (human-readable)
  --jsonl events_latency.jsonl  # JSONL path (PLD schema-ready 'latency_hold' events)
  --session-id sess_local_001   # session id for JSONL
  --reason soft_repair_probe    # metadata.reason for JSONL
  --context latency_tracker     # metadata.context for JSONL
"""

from __future__ import annotations
import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

DEFAULT_THRESHOLD_MS = 800
DEFAULT_CSV = "pause_log.csv"

@dataclass
class PauseEvent:
    start_time_unix: float
    end_time_unix: float
    start_time_iso: str
    end_time_iso: str
    duration_ms: float
    pause_label: str  # "⏸️ Pause" or "✅ Smooth"

def _iso_utc(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def create_pause_event(start_unix: float, end_unix: float, threshold_ms: int) -> PauseEvent:
    duration_ms = (end_unix - start_unix) * 1000.0
    label = "⏸️ Pause" if duration_ms > float(threshold_ms) else "✅ Smooth"
    return PauseEvent(
        start_time_unix=round(start_unix, 6),
        end_time_unix=round(end_unix, 6),
        start_time_iso=_iso_utc(start_unix),
        end_time_iso=_iso_utc(end_unix),
        duration_ms=round(duration_ms, 2),
        pause_label=label,
    )

def log_event_to_csv(event: PauseEvent, path: Path) -> None:
    if path.suffix.lower() != ".csv":
        raise ValueError("CSV path must end with .csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    row = asdict(event)
    file_exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def emit_pld_jsonl(event: PauseEvent, path: Path, session_id: str, reason: str, context: str) -> None:
    """
    Emit a PLD metrics-compatible event. Schema alignment:
      event_type: "latency_hold"
      timestamp: ISO8601 (now)
      session_id: provided
      metadata.duration_ms: required (number)
      metadata.reason/context/user_cancelled: examples
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    obj = {
        "event_type": "latency_hold",
        "timestamp": _iso_utc(time.time()),
        "session_id": session_id,
        "metadata": {
            "duration_ms": event.duration_ms,
            "reason": reason,
            "context": context,
            "user_cancelled": False
        }
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="PLD Latency Tracker")
    p.add_argument("--threshold-ms", type=int, default=DEFAULT_THRESHOLD_MS, help="Pause threshold in milliseconds")
    p.add_argument("--csv", type=str, default=DEFAULT_CSV, help="CSV path for human-readable logging")
    p.add_argument("--jsonl", type=str, default="", help="Optional JSONL path to emit PLD 'latency_hold' events")
    p.add_argument("--session-id", type=str, default="sess_local_001", help="Session id for JSONL")
    p.add_argument("--reason", type=str, default="manual_latency_test", help="metadata.reason for JSONL")
    p.add_argument("--context", type=str, default="latency_tracker", help="metadata.context for JSONL")
    return p.parse_args()

def interactive_once(threshold_ms: int) -> PauseEvent:
    print("🔴 Ready. Press Enter to START timing…", flush=True)
    input()
    start = time.monotonic()
    print("⏸️ Timing… Press Enter to STOP.", flush=True)
    input()
    end = time.monotonic()
    # Convert monotonic to wall-clock by anchoring now for ISO stamps
    # We still store unix epoch using time.time() at start/end moments for readability
    wall_start = time.time() - (end - start)
    wall_end = time.time()
    return create_pause_event(wall_start, wall_end, threshold_ms)

def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv).resolve()
    jsonl_path: Optional[Path] = Path(args.jsonl).resolve() if args.jsonl else None

    try:
        event = interactive_once(args.threshold_ms)
        print(f"🧠 Detected: {event.pause_label}  |  duration_ms={event.duration_ms}")
        print(f"   start={event.start_time_iso}  end={event.end_time_iso}")

        log_event_to_csv(event, csv_path)
        print(f"[ok] CSV appended → {csv_path}")

        if jsonl_path:
            emit_pld_jsonl(event, jsonl_path, args.session_id, args.reason, args.context)
            print(f"[ok] JSONL appended → {jsonl_path}")

        print("\nNext:")
        print(" - Use bootstrap_demo.py for a full demo pipeline (gen+validate+report).")
        print(" - Or validate this JSONL with scripts/validate_events.sh (if emitted).")
        return 0
    except KeyboardInterrupt:
        print("\n[cancelled] Aborted by user.")
        return 130
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
