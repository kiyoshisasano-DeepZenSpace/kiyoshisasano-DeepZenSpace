#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.structured_logger

Structured logging façade for PLD runtime.

This module provides a high-level interface to log:

    - Normalized turns
    - PLD events and envelopes
    - Controller outcomes
    - Route instructions (from ActionRouter)

It does NOT own any I/O backend.
Instead, it delegates to a simple "writer" callable, which can be:

    - file-based
    - console-based
    - database / queue producer
    - OpenTelemetry exporter (see exporters/)

The goal is to keep logging:

    - consistent (fixed record schema)
    - low-friction (simple function calls)
    - replayable (session+turn indexed)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Literal

from ..detection.runtime_signal_bridge import NormalizedTurn
from ..controllers.pld_controller import ControllerOutcome
from ..controllers.action_router import RouteInstruction


# ---------------------------------------------------------------------------
# Logging Modes
# ---------------------------------------------------------------------------

class LoggingMode(str, Enum):
    """
    Logging verbosity / purpose.

    - DEBUG:
        Maximum detail. Includes raw detector outputs, policies, routes.

    - COMPACT:
        Minimal fields needed for operational observability.

    - EVALUATION:
        Focused on signals needed for offline evaluation / datasets.

    - SILENT:
        No-op; all log_* calls are dropped.
    """

    DEBUG = "debug"
    COMPACT = "compact"
    EVALUATION = "evaluation"
    SILENT = "silent"


# ---------------------------------------------------------------------------
# Record Types
# ---------------------------------------------------------------------------

@dataclass
class BaseRecord:
    """
    Common fields for all PLD structured log records.

    Fields
    ------
    kind:
        Record type tag, e.g., "turn", "pld_event", "controller_outcome".

    ts:
        ISO 8601 timestamp, UTC (Z).

    session_id:
        Session identifier (if applicable).
    """

    kind: str
    ts: str
    session_id: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TurnRecord(BaseRecord):
    """
    Log entry for a NormalizedTurn.
    """

    turn_id: str
    role: str
    text: str
    runtime: Dict[str, Any]

    @classmethod
    def from_turn(cls, turn: NormalizedTurn) -> "TurnRecord":
        return cls(
            kind="turn",
            ts=_now_iso(),
            session_id=turn.session_id,
            turn_id=turn.turn_id,
            role=turn.role,
            text=turn.text,
            runtime=turn.runtime,
        )


@dataclass
class PldEventRecord(BaseRecord):
    """
    Log entry for a single PLD event (optionally with envelope).
    """

    event: Dict[str, Any]
    envelope: Optional[Dict[str, Any]] = None

    @classmethod
    def from_event(
        cls,
        *,
        session_id: str,
        event: Dict[str, Any],
        envelope: Optional[Dict[str, Any]] = None,
    ) -> "PldEventRecord":
        return cls(
            kind="pld_event",
            ts=event.get("timestamp") or _now_iso(),
            session_id=session_id,
            event=event,
            envelope=envelope,
        )


@dataclass
class ControllerOutcomeRecord(BaseRecord):
    """
    Log entry for a full ControllerOutcome (per turn).

    In DEBUG mode, this can be used directly.
    In COMPACT / EVALUATION mode, a reduced view may be emitted instead.
    """

    outcome: Dict[str, Any]

    @classmethod
    def from_outcome(cls, outcome: ControllerOutcome) -> "ControllerOutcomeRecord":
        return cls(
            kind="controller_outcome",
            ts=_now_iso(),
            session_id=outcome.session_id,
            outcome=outcome.to_dict(),
        )


@dataclass
class RouteInstructionRecord(BaseRecord):
    """
    Log entry for a RouteInstruction (policy-action mapping).
    """

    instruction: Dict[str, Any]

    @classmethod
    def from_instruction(
        cls,
        session_id: str,
        instr: RouteInstruction,
    ) -> "RouteInstructionRecord":
        return cls(
            kind="route_instruction",
            ts=_now_iso(),
            session_id=session_id,
            instruction=instr.to_dict(),
        )


# ---------------------------------------------------------------------------
# Writer Type
# ---------------------------------------------------------------------------

WriterFunc = Callable[[Dict[str, Any]], None]


# ---------------------------------------------------------------------------
# Structured Logger
# ---------------------------------------------------------------------------

class StructuredLogger:
    """
    Thin façade over a generic writer to produce structured PLD records.

    Parameters
    ----------
    writer:
        A callable that receives a dict record. It may write to file,
        stdout, an HTTP endpoint, a message queue, etc.

    mode:
        Controls verbosity / content.

    session_scoping:
        If True, logger enforces presence of session_id on relevant records.

    Example
    -------
        import sys, json

        def stdout_writer(rec: dict) -> None:
            print(json.dumps(rec, ensure_ascii=False), file=sys.stdout)

        logger = StructuredLogger(writer=stdout_writer, mode=LoggingMode.DEBUG)

        # in runtime
        logger.log_turn(turn)
        logger.log_controller_outcome(outcome)
    """

    def __init__(
        self,
        writer: WriterFunc,
        mode: LoggingMode | str = LoggingMode.COMPACT,
        session_scoping: bool = True,
    ) -> None:
        if isinstance(mode, str):
            try:
                mode = LoggingMode(mode.lower())  # type: ignore[arg-type]
            except Exception:
                mode = LoggingMode.COMPACT
        self.writer = writer
        self.mode = mode
        self.session_scoping = session_scoping

    # ---- Public logging API ----

    def log_turn(self, turn: NormalizedTurn) -> None:
        """
        Log a normalized turn.

        - In SILENT mode: no-op.
        - Otherwise: emit a TurnRecord.
        """
        if self.mode is LoggingMode.SILENT:
            return
        rec = TurnRecord.from_turn(turn)
        self._emit(rec.to_dict())

    def log_pld_event(
        self,
        *,
        session_id: str,
        event: Dict[str, Any],
        envelope: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log a single PLD event (and optional envelope).

        - In SILENT mode: no-op.
        - In COMPACT mode: event only.
        - In DEBUG/EVALUATION: event + envelope if present.
        """
        if self.mode is LoggingMode.SILENT:
            return

        rec = PldEventRecord.from_event(
            session_id=session_id,
            event=event,
            envelope=envelope if self._include_envelope() else None,
        )
        self._emit(rec.to_dict())

    def log_controller_outcome(self, outcome: ControllerOutcome) -> None:
        """
        Log a full ControllerOutcome.

        - DEBUG: all fields.
        - EVALUATION: everything (offline analysis uses these).
        - COMPACT: skip this; rely on event-level logging.
        - SILENT: no-op.
        """
        if self.mode in (LoggingMode.SILENT, LoggingMode.COMPACT):
            return

        rec = ControllerOutcomeRecord.from_outcome(outcome)
        self._emit(rec.to_dict())

    def log_route_instructions(
        self,
        session_id: str,
        instructions: List[RouteInstruction],
    ) -> None:
        """
        Log RouteInstruction list produced by ActionRouter.

        - DEBUG: always log.
        - COMPACT/EVALUATION: log only non-trivial actions (non-NOOP).
        - SILENT: no-op.
        """
        if self.mode is LoggingMode.SILENT:
            return

        for instr in instructions:
            # basic filtering: in COMPACT/EVALUATION, drop metrics-only logs
            if self.mode in (LoggingMode.COMPACT, LoggingMode.EVALUATION):
                if instr.target.value == "metrics_only":
                    continue

            rec = RouteInstructionRecord.from_instruction(session_id, instr)
            self._emit(rec.to_dict())

    # ---- Internal helpers ----

    def _emit(self, record: Dict[str, Any]) -> None:
        """
        Emit a record to writer, optionally enforcing session scoping.
        """
        if self.session_scoping:
            kind = record.get("kind")
            # For turn/event/controller/route, session_id SHOULD be present.
            if kind in {"turn", "pld_event", "controller_outcome", "route_instruction"}:
                if not record.get("session_id"):
                    # Attach explicit marker rather than failing hard.
                    record.setdefault("_warning", "missing_session_id")

        self.writer(record)

    def _include_envelope(self) -> bool:
        """
        Decide whether to include envelope with PLD event logs
        based on logging mode.
        """
        return self.mode in (LoggingMode.DEBUG, LoggingMode.EVALUATION)


# ---------------------------------------------------------------------------
# Convenience: simple console logger
# ---------------------------------------------------------------------------

def make_console_logger(
    *,
    mode: LoggingMode | str = LoggingMode.COMPACT,
    stream: Any = None,
) -> StructuredLogger:
    """
    Create a StructuredLogger that writes JSON lines to a text stream
    (default: sys.stdout).

    This is primarily for quick experiments and local debugging.
    """
    import json
    import sys

    if stream is None:
        stream = sys.stdout

    def _writer(rec: Dict[str, Any]) -> None:
        print(json.dumps(rec, ensure_ascii=False), file=stream)

    return StructuredLogger(writer=_writer, mode=mode)


__all__ = [
    "LoggingMode",
    "BaseRecord",
    "TurnRecord",
    "PldEventRecord",
    "ControllerOutcomeRecord",
    "RouteInstructionRecord",
    "WriterFunc",
    "StructuredLogger",
    "make_console_logger",
]
