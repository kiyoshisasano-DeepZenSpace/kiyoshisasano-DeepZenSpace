#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.exporters.exporter_jsonl

JSON Lines (JSONL) exporters for PLD runtime traces.

This module provides utilities to export:

- Full session traces from SessionTraceBuffer
- Only PLD events from traces (for evaluation datasets)
- Controller outcomes or route instructions if needed

Each exported line is a single JSON object suitable for:

- Offline analysis
- Metric pipelines
- Training / evaluation datasets
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from ..session_trace_buffer import (
    SessionTraceBuffer,
    SessionTrace,
    TraceItem,
)
from ..event_writer import (
    JsonlFileWriter,
    make_jsonl_file_writer,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _trace_item_to_flat_record(
    session_id: str,
    item: TraceItem,
) -> Dict[str, Any]:
    """
    Convert a TraceItem into a flattened record for JSONL export.

    Structure:

        {
          "session_id": "...",
          "kind": "turn" | "pld_event" | ...,
          "ts": "...",
          "seq": 0,
          "payload": {...}
        }

    The payload is preserved as-is to avoid losing information.
    """
    return {
        "session_id": session_id,
        "kind": item.kind,
        "ts": item.ts,
        "seq": item.seq,
        "payload": item.payload,
    }


def _ensure_writer(path: str | Path) -> JsonlFileWriter:
    return make_jsonl_file_writer(path, append=False, ensure_ascii=False, auto_flush=True)


# ---------------------------------------------------------------------------
# Export: Session-level
# ---------------------------------------------------------------------------

def export_session_trace(
    buffer: SessionTraceBuffer,
    session_id: str,
    path: str | Path,
) -> int:
    """
    Export a single session trace to a JSONL file.

    Each line is a flattened TraceItem record (see _trace_item_to_flat_record).
    Returns the number of lines written.
    """
    trace = buffer.get_trace(session_id)
    if trace is None:
        return 0

    writer = _ensure_writer(path)
    written = 0

    try:
        for item in trace.items:
            record = _trace_item_to_flat_record(session_id, item)
            writer(record)
            written += 1
    finally:
        writer.close()

    return written


def export_all_traces(
    buffer: SessionTraceBuffer,
    path: str | Path,
) -> int:
    """
    Export all session traces from the buffer to a single JSONL file.

    Records are written in no particular session order; they follow
    the internal SessionTrace ordering.

    Returns the number of lines written.
    """
    writer = _ensure_writer(path)
    written = 0

    try:
        for session_id, trace in buffer._traces.items():  # noqa: SLF001 (internal access by design)
            for item in trace.items:
                record = _trace_item_to_flat_record(session_id, item)
                writer(record)
                written += 1
    finally:
        writer.close()

    return written


# ---------------------------------------------------------------------------
# Export: PLD event–only (evaluation friendly)
# ---------------------------------------------------------------------------

def _iter_pld_events_from_trace(trace: SessionTrace) -> Iterable[Dict[str, Any]]:
    """
    Yield bare PLD events from a SessionTrace.

    For items with kind == "pld_event", payload is expected to be:

        { "event": {...}, "envelope": {...} | None }

    Other kinds are ignored.
    """
    for item in trace.items:
        if item.kind != "pld_event":
            continue
        payload = item.payload or {}
        event = payload.get("event")
        if isinstance(event, dict):
            yield event


def export_pld_events_for_session(
    buffer: SessionTraceBuffer,
    session_id: str,
    path: str | Path,
) -> int:
    """
    Export only PLD events for a given session to JSONL.

    Each line is the raw PLD event (pld_event.schema.json object).
    Returns the number of events written.
    """
    trace = buffer.get_trace(session_id)
    if trace is None:
        return 0

    writer = _ensure_writer(path)
    written = 0
    try:
        for event in _iter_pld_events_from_trace(trace):
            writer(event)
            written += 1
    finally:
        writer.close()
    return written


def export_pld_events_all_sessions(
    buffer: SessionTraceBuffer,
    path: str | Path,
) -> int:
    """
    Export all PLD events across all sessions to a single JSONL file.

    Each line is a raw PLD event.

    Returns the number of events written.
    """
    writer = _ensure_writer(path)
    written = 0
    try:
        for session_id, trace in buffer._traces.items():  # noqa: SLF001
            for event in _iter_pld_events_from_trace(trace):
                writer(event)
                written += 1
    finally:
        writer.close()
    return written


__all__ = [
    "export_session_trace",
    "export_all_traces",
    "export_pld_events_for_session",
    "export_pld_events_all_sessions",
]
