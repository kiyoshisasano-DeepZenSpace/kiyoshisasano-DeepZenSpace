#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Kiyoshi Sasano

"""
quickstart/metrics/verify_metrics_local.py

Purpose
-------
Minimal local verification script for the PLD metrics quickstart.

It does three things:

  1. Load the demo event log:
       quickstart/metrics/datasets/pld_events_demo.jsonl

  2. Optionally run a small DuckDB query (if duckdb is installed)
     to show that the JSONL can be treated as a SQL table.

  3. Compute the key operational metrics from the cookbook
     over this demo dataset:

        - FR   : Failover Rate
        - MRBF : Mean Repairs Before Failover
        - VRL  : Visible Repair Load (%)
        - PRDR : Post-Repair Drift Recurrence (%)

This is intended as a sanity check that:

  - the demo log is structurally sound,
  - the metric definitions are implementable, and
  - the numbers are plausible (not NaN / zero everywhere).

Usage
-----
    cd quickstart/metrics
    python verify_metrics_local.py

Optional (for the DuckDB snippet):

    pip install duckdb
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional DuckDB support (for a small SQL demo)
# ---------------------------------------------------------------------------

try:  # pragma: no cover - optional dependency
    import duckdb  # type: ignore[import]
except Exception:  # pragma: no cover - optional dependency
    duckdb = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Event:
    """
    Minimal view over a PLD event row for metric computation.

    We only use the fields needed for the cookbook metrics:
      - session_id
      - turn_id
      - event_type
      - pld.phase / pld.code
    """

    session_id: str
    turn_id: int
    event_type: str
    pld_phase: str
    pld_code: str

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> "Event":
        session_id = str(raw.get("session_id", ""))
        event_type = str(raw.get("event_type", "") or "")
        pld = raw.get("pld") or {}
        pld_phase = str(pld.get("phase", "none"))
        pld_code = str(pld.get("code", "NONE"))

        turn_raw = raw.get("turn_id", 0)
        try:
            turn_id = int(turn_raw)
        except Exception:
            # Fallback: arbitrary but stable ordering if turn_id is not numeric
            turn_id = 0

        return cls(
            session_id=session_id,
            turn_id=turn_id,
            event_type=event_type,
            pld_phase=pld_phase,
            pld_code=pld_code,
        )


# ---------------------------------------------------------------------------
# IO helpers
# ---------------------------------------------------------------------------

def load_demo_events(path: Path) -> List[Event]:
    if not path.exists():
        raise FileNotFoundError(f"Demo dataset not found: {path}")

    events: List[Event] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            raw = json.loads(line)
            events.append(Event.from_raw(raw))
    return events


def duckdb_preview(path: Path) -> None:
    """
    Small SQL-based preview using DuckDB, if available.

    This is intentionally minimal and not required for metric computation.
    """
    if duckdb is None:
        print("🐤 DuckDB not installed — skipping SQL preview.\n")
        return

    print("🐤 DuckDB preview (reading JSONL as a table):")
    con = duckdb.connect()
    try:
        con.execute(
            "CREATE OR REPLACE VIEW pld_events AS "
            "SELECT * FROM read_json_auto(?, ignore_errors := true)",
            [str(path)],
        )
        rows = con.execute(
            "SELECT COUNT(*) AS events, "
            "       COUNT(DISTINCT session_id) AS sessions "
            "FROM pld_events"
        ).fetchall()
        events, sessions = rows[0]
        print(f"  Events   : {events}")
        print(f"  Sessions : {sessions}\n")
    finally:
        con.close()


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------

@dataclass
class MetricsSummary:
    total_events: int
    total_sessions: int
    failover_rate: float      # FR (0–1)
    mean_repairs_before_failover: float  # MRBF
    visible_repair_load: float           # VRL (%) 0–100
    prdr: float                          # Post-Repair Drift Recurrence (%) 0–100


def compute_metrics(events: List[Event], *, prdr_window: int = 3) -> MetricsSummary:
    if not events:
        return MetricsSummary(
            total_events=0,
            total_sessions=0,
            failover_rate=0.0,
            mean_repairs_before_failover=0.0,
            visible_repair_load=0.0,
            prdr=0.0,
        )

    # Group by session and sort by turn_id
    sessions: Dict[str, List[Event]] = {}
    for ev in events:
        sessions.setdefault(ev.session_id, []).append(ev)

    for evs in sessions.values():
        evs.sort(key=lambda e: e.turn_id)

    total_events = len(events)
    total_sessions = len(sessions)

    # ---- FR & MRBF ---------------------------------------------------------
    failover_sessions: List[str] = []
    repairs_before_failover: List[int] = []

    for sid, evs in sessions.items():
        failover_index: Optional[int] = None
        for idx, ev in enumerate(evs):
            if ev.event_type == "failover_triggered":
                failover_index = idx
                break

        if failover_index is None:
            continue

        failover_sessions.append(sid)

        # Count repair_triggered before failover
        repair_count = sum(
            1
            for ev in evs[:failover_index]
            if ev.event_type == "repair_triggered"
        )
        repairs_before_failover.append(repair_count)

    failover_rate = (
        len(failover_sessions) / total_sessions if total_sessions > 0 else 0.0
    )
    mean_repairs_before_failover = (
        (sum(repairs_before_failover) / len(repairs_before_failover))
        if repairs_before_failover
        else 0.0
    )

    # ---- VRL (Visible Repair Load) ----------------------------------------
    # We treat event_type == 'repair_visible' (and 'clarification_prompt' if present)
    # as visible repairs.
    visible_events = sum(
        1
        for ev in events
        if ev.event_type in {"repair_visible", "clarification_prompt"}
    )
    visible_repair_load = (
        (visible_events * 100.0 / total_events) if total_events > 0 else 0.0
    )

    # ---- PRDR (Post-Repair Drift Recurrence) ------------------------------
    # For each repair_triggered, check whether a drift_detected occurs
    # within the next `prdr_window` turns in the same session.
    total_repairs = 0
    repairs_with_recurrence = 0

    for sid, evs in sessions.items():
        # Pre-extract drift turn_ids for quick lookup
        drift_turns = {ev.turn_id for ev in evs if ev.event_type == "drift_detected"}

        for ev in evs:
            if ev.event_type != "repair_triggered":
                continue
            total_repairs += 1

            start_turn = ev.turn_id + 1
            end_turn = ev.turn_id + prdr_window
            recurrence = any(
                t in drift_turns for t in range(start_turn, end_turn + 1)
            )
            if recurrence:
                repairs_with_recurrence += 1

    prdr = (
        (repairs_with_recurrence * 100.0 / total_repairs)
        if total_repairs > 0
        else 0.0
    )

    return MetricsSummary(
        total_events=total_events,
        total_sessions=total_sessions,
        failover_rate=failover_rate,
        mean_repairs_before_failover=mean_repairs_before_failover,
        visible_repair_load=visible_repair_load,
        prdr=prdr,
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    base_dir = Path(__file__).resolve().parent
    data_path = base_dir / "datasets" / "pld_events_demo.jsonl"

    print(f"📂 Loading demo dataset: {data_path}")
    try:
        events = load_demo_events(data_path)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 1

    print(f"✅ Loaded {len(events)} events\n")

    # Optional DuckDB preview
    duckdb_preview(data_path)

    # Compute cookbook-aligned metrics
    summary = compute_metrics(events)

    print("=== PLD Metrics — Demo Summary ===")
    print(f"Total sessions              : {summary.total_sessions}")
    print(f"Total events                : {summary.total_events}")
    print()
    print(f"FR   (Failover Rate)        : {summary.failover_rate * 100:.2f}%")
    print(f"MRBF (Mean Repairs/Failover): {summary.mean_repairs_before_failover:.2f}")
    print(f"VRL  (Visible Repair Load)  : {summary.visible_repair_load:.2f}%")
    print(f"PRDR (Post-Repair Drift Rec): {summary.prdr:.2f}%")
    print()
    print("Interpretation (see docs/07_pld_operational_metrics_cookbook.md):")
    print("  • FR   → how often sessions end in failover.")
    print("  • MRBF → how many repairs happen before we give up.")
    print("  • VRL  → how frequently users see explicit repairs.")
    print("  • PRDR → whether repairs actually prevent future drift.\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
