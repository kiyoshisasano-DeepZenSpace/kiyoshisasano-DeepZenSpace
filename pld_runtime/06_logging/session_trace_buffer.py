#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.session_trace_buffer

In-memory buffer for PLD runtime traces, grouped by session_id.

This module provides:

- A normalized structure for storing:
    - Normalized turns
    - PLD events (and optional envelopes)
    - Controller outcomes
    - Route instructions
- Simple APIs for:
    - appending new items during runtime
    - snapshotting a session trace for export
    - clearing / trimming traces

It does NOT:

- write to disk
- send data to external systems
- perform schema validation or policy decisions

Those responsibilities live in:

- enforcement/* for validation / sequence rules / policy
- logging/structured_logger.py for actual I/O
- exporters/* for persistent storage or external telemetry
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Literal

from ..detection.runtime_signal_bridge import NormalizedTurn
from ..controllers.pld_controller import ControllerOutcome
from ..controllers.action_router import RouteInstruction


TraceItemKind = Literal[
    "turn",
    "pld_event",
    "controller_outcome",
    "route_instruction",
]


# ---------------------------------------------------------------------------
# Trace item models
# ---------------------------------------------------------------------------

@dataclass
class TraceItem:
    """
    Single element in a session trace.

    Fields
    ------
    kind:
        "turn", "pld_event", "controller_outcome", or "route_instruction".

    ts:
        ISO 8601 timestamp (UTC, Z).

    seq:
        Monotonic sequence number within the session trace.

    payload:
        Kind-specific content; always a plain dict.
    """

    kind: TraceItemKind
    ts: str
    seq: int
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SessionTrace:
    """
    In-memory trace for a single session.

    Items are stored in order of insertion; seq is strictly increasing.
    """

    session_id: str
    items: List[TraceItem] = field(default_factory=list)
    _next_seq: int = 0

    def append(self, item: TraceItem) -> None:
        self.items.append(item)
        self._next_seq = max(self._next_seq, item.seq + 1)

    def next_seq(self) -> int:
        return self._next_seq

    def snapshot(self) -> Dict[str, Any]:
        """
        Return a serializable snapshot of the entire session trace.
        """
        return {
            "session_id": self.session_id,
            "length": len(self.items),
            "items": [i.to_dict() for i in self.items],
        }


# ---------------------------------------------------------------------------
# Buffer configuration
# ---------------------------------------------------------------------------

class TraceRetentionPolicy(str, Enum):
    """
    Retention behavior for the buffer.

    - UNBOUNDED:
        Keep all traces in memory until explicitly cleared.

    - PER_SESSION_LIMIT:
        Keep up to `max_items_per_session` items per session; oldest are dropped.

    - GLOBAL_LIMIT:
        Keep up to `max_total_items` items globally; oldest (across sessions)
        are dropped when exceeded.
    """

    UNBOUNDED = "unbounded"
    PER_SESSION_LIMIT = "per_session_limit"
    GLOBAL_LIMIT = "global_limit"


@dataclass
class SessionTraceBufferConfig:
    """
    Configuration for SessionTraceBuffer.

    Parameters
    ----------
    retention_policy:
        See TraceRetentionPolicy.

    max_items_per_session:
        Used when retention_policy == PER_SESSION_LIMIT.

    max_total_items:
        Used when retention_policy == GLOBAL_LIMIT.
    """

    retention_policy: TraceRetentionPolicy = TraceRetentionPolicy.UNBOUNDED
    max_items_per_session: int = 500
    max_total_items: int = 5000


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Buffer
# ---------------------------------------------------------------------------

class SessionTraceBuffer:
    """
    In-memory storage for PLD session traces.

    Typical usage
    -------------
        buffer = SessionTraceBuffer()

        # when a normalized turn is received:
        buffer.add_turn(turn)

        # when controller outcome is produced:
        buffer.add_controller_outcome(outcome)

        # when route instructions are created:
        buffer.add_route_instructions(session_id, instructions)

        # to export a session trace:
        trace = buffer.get_trace("session-123")
        snapshot = trace.snapshot() if trace else None
    """

    def __init__(self, config: Optional[SessionTraceBufferConfig] = None) -> None:
        self.config = config or SessionTraceBufferConfig()
        self._traces: Dict[str, SessionTrace] = {}
        self._global_items: List[tuple[str, int]] = []  # (session_id, seq)

    # ---- public append API ----

    def add_turn(self, turn: NormalizedTurn) -> None:
        trace = self._get_or_create_trace(turn.session_id)
        seq = trace.next_seq()
        item = TraceItem(
            kind="turn",
            ts=_now_iso(),
            seq=seq,
            payload=turn.to_dict(),
        )
        trace.append(item)
        self._register_global(turn.session_id, seq)
        self._enforce_retention()

    def add_pld_event(
        self,
        *,
        session_id: str,
        event: Dict[str, Any],
        envelope: Optional[Dict[str, Any]] = None,
    ) -> None:
        trace = self._get_or_create_trace(session_id)
        seq = trace.next_seq()
        payload = {
            "event": event,
            "envelope": envelope,
        }
        item = TraceItem(
            kind="pld_event",
            ts=event.get("timestamp") or _now_iso(),
            seq=seq,
            payload=payload,
        )
        trace.append(item)
        self._register_global(session_id, seq)
        self._enforce_retention()

    def add_controller_outcome(self, outcome: ControllerOutcome) -> None:
        trace = self._get_or_create_trace(outcome.session_id)
        seq = trace.next_seq()
        item = TraceItem(
            kind="controller_outcome",
            ts=_now_iso(),
            seq=seq,
            payload=outcome.to_dict(),
        )
        trace.append(item)
        self._register_global(outcome.session_id, seq)
        self._enforce_retention()

    def add_route_instructions(
        self,
        *,
        session_id: str,
        instructions: List[RouteInstruction],
    ) -> None:
        if not instructions:
            return
        trace = self._get_or_create_trace(session_id)
        for instr in instructions:
            seq = trace.next_seq()
            item = TraceItem(
                kind="route_instruction",
                ts=_now_iso(),
                seq=seq,
                payload=instr.to_dict(),
            )
            trace.append(item)
            self._register_global(session_id, seq)
        self._enforce_retention()

    # ---- access API ----

    def get_trace(self, session_id: str) -> Optional[SessionTrace]:
        """
        Get the SessionTrace for a session, or None if unknown.
        """
        return self._traces.get(session_id)

    def snapshot(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Return a serializable snapshot for a session, or None.
        """
        trace = self.get_trace(session_id)
        return trace.snapshot() if trace else None

    def clear_session(self, session_id: str) -> None:
        """
        Drop all trace data for a given session.
        """
        if session_id not in self._traces:
            return
        del self._traces[session_id]
        # Filter global index entries
        self._global_items = [
            (sid, seq) for (sid, seq) in self._global_items if sid != session_id
        ]

    def clear_all(self) -> None:
        """
        Remove all traces from memory.
        """
        self._traces.clear()
        self._global_items.clear()

    # ---- internal helpers ----

    def _get_or_create_trace(self, session_id: str) -> SessionTrace:
        trace = self._traces.get(session_id)
        if trace is None:
            trace = SessionTrace(session_id=session_id)
            self._traces[session_id] = trace
        return trace

    def _register_global(self, session_id: str, seq: int) -> None:
        self._global_items.append((session_id, seq))

    def _enforce_retention(self) -> None:
        policy = self.config.retention_policy

        if policy is TraceRetentionPolicy.UNBOUNDED:
            return

        if policy is TraceRetentionPolicy.PER_SESSION_LIMIT:
            self._enforce_per_session_limit()
        elif policy is TraceRetentionPolicy.GLOBAL_LIMIT:
            self._enforce_global_limit()

    def _enforce_per_session_limit(self) -> None:
        limit = max(1, self.config.max_items_per_session)
        for session_id, trace in list(self._traces.items()):
            if len(trace.items) <= limit:
                continue
            # Drop oldest items until within limit
            excess = len(trace.items) - limit
            removed = trace.items[:excess]
            trace.items = trace.items[excess:]
            # Update global index
            removed_seqs = {i.seq for i in removed}
            self._global_items = [
                (sid, seq)
                for (sid, seq) in self._global_items
                if not (sid == session_id and seq in removed_seqs)
            ]

    def _enforce_global_limit(self) -> None:
        limit = max(1, self.config.max_total_items)
        total_items = sum(len(t.items) for t in self._traces.values())
        if total_items <= limit:
            return

        # Compute how many items to drop
        to_drop = total_items - limit
        dropped = 0

        # Sort global index by (append order) → _global_items is already append-ordered.
        # We iterate from oldest to newest.
        for session_id, seq in list(self._global_items):
            if dropped >= to_drop:
                break

            trace = self._traces.get(session_id)
            if trace is None:
                continue

            # Find and remove item with this seq in the session trace.
            for idx, item in enumerate(trace.items):
                if item.seq == seq:
                    del trace.items[idx]
                    dropped += 1
                    break

            # Remove from global index
            self._global_items = [
                (sid, s) for (sid, s) in self._global_items if not (sid == session_id and s == seq)
            ]

            if not trace.items:
                # Optionally drop empty trace
                del self._traces[session_id]


__all__ = [
    "TraceItemKind",
    "TraceItem",
    "SessionTrace",
    "TraceRetentionPolicy",
    "SessionTraceBufferConfig",
    "SessionTraceBuffer",
]
