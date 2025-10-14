#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Latency Tracker

Tracks latency events across conversation sessions
and emits schema-compliant JSONL entries for later aggregation.
"""

import json, time, uuid
from pathlib import Path
from datetime import datetime, timezone

def _iso_utc(ts=None):
    """Return ISO8601 UTC string with 'Z'."""
    if ts is None:
        ts = time.time()
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

class LatencyEvent:
    """Represents a latency-hold or related timing segment."""
    def __init__(self, session_id: str, reason: str, duration_ms: float, context=None):
        self.session_id = session_id
        self.reason = reason
        self.duration_ms = duration_ms
        self.context = context or {}
        self.start_time = time.time()
        self.end_time = None
        self.event_id = str(uuid.uuid4())

    def end(self):
        self.end_time = time.time()

    @property
    def end_time_iso(self):
        return _iso_utc(self.end_time or time.time())

    def to_jsonl(self):
        """Return schema-compliant JSONL line."""
        return json.dumps({
            "event_type": "latency_hold",
            "timestamp": self.end_time_iso,
            "session_id": self.session_id,
            "metadata": {
                "duration_ms": self.duration_ms,
                "reason": self.reason,
                "context": self.context,
                "event_id": self.event_id
            }
        }, ensure_ascii=False)

def emit_pld_jsonl(event: LatencyEvent, out_path: Path):
    """Emit a JSONL line to the specified file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a", encoding="utf-8") as f:
        f.write(event.to_jsonl() + "\n")
    return out_path

if __name__ == "__main__":
    # demo run
    OUT = Path("demo_quick/latency_demo.jsonl")
    ev = LatencyEvent("sess_demo_001", reason="soft_repair_probe", duration_ms=800.0, context={"phase": "checkout"})
    time.sleep(0.1)
    ev.end()
    emit_pld_jsonl(ev, OUT)
    print(f"[ok] Wrote latency event to {OUT}")
