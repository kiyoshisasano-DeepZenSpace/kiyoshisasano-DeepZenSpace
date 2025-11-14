#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.controllers.state_machine

Online PLD state machine for a single conversational session or trace.

This module:

- Maintains the current PLD phase:
    none → drift → repair → reentry → outcome
- Tracks active drift/repair segments
- Applies simple, local transition rules when new PLD events arrive
- Returns structured results that controllers can use to decide actions

It does NOT:

- Inspect raw text or runtime metadata
- Perform temporal checks (see enforcement.sequence_rules)
- Call tools or models (see controllers/pld_controller and action router)
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional, Tuple


Phase = Literal["none", "drift", "repair", "reentry", "outcome"]


# ---------------------------------------------------------------------------
# Datatypes
# ---------------------------------------------------------------------------

@dataclass
class PLDState:
    """
    Online PLD state for a single session / trace.

    Fields
    ------
    phase:
        Current coarse-grained PLD phase.

    active_drift_code:
        Code for the currently active drift (e.g., "D1_information_drift"),
        or None if no drift is currently open.

    active_repair_code:
        Code for the currently active repair (e.g., "R2_structural_repair"),
        or None if no repair is currently underway.

    cycles_completed:
        Number of full Drift → Repair → Reentry cycles completed so far.

    last_event_id:
        Most recent PLD event_id seen (if any).

    last_timestamp:
        Timestamp (ISO 8601, Z) of the most recent event, if known.
    """

    phase: Phase = "none"
    active_drift_code: Optional[str] = None
    active_repair_code: Optional[str] = None
    cycles_completed: int = 0
    last_event_id: Optional[str] = None
    last_timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TransitionResult:
    """
    Result of applying a new PLD event to a PLDState.

    Fields
    ------
    from_phase:
        Phase before the event.

    to_phase:
        Phase after the event.

    valid:
        True if the transition is allowed by the state machine,
        False if it violates the local phase ordering.

    reason:
        Short description of how/why the transition happened.

    state:
        Updated PLDState after applying the event.
    """

    from_phase: Phase
    to_phase: Phase
    valid: bool
    reason: str
    state: PLDState

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["state"] = self.state.to_dict()
        return d


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _extract_phase_and_code(event: Dict[str, Any]) -> Tuple[Phase, Optional[str]]:
    """
    Extract (phase, code) from a PLD event object that conforms
    to pld_event.schema.json.

    Falls back to "none" if the fields are missing or invalid.
    """
    pld = event.get("pld") or {}
    phase_raw = str(pld.get("phase", "none")).lower()

    if phase_raw not in {"drift", "repair", "reentry", "outcome", "none"}:
        phase: Phase = "none"
    else:
        phase = phase_raw  # type: ignore[assignment]

    code = pld.get("code")
    if code is not None:
        code = str(code)

    return phase, code


def _extract_timestamp(event: Dict[str, Any]) -> str:
    ts = event.get("timestamp")
    if isinstance(ts, str) and ts:
        return ts
    return _now_iso()


def _is_drift(code: Optional[str], phase: Phase) -> bool:
    if phase == "drift":
        return True
    if code is None:
        return False
    return code.startswith("D")


def _is_repair(code: Optional[str], phase: Phase) -> bool:
    if phase == "repair":
        return True
    if code is None:
        return False
    return code.startswith("R")


def _is_reentry(code: Optional[str], phase: Phase) -> bool:
    if phase == "reentry":
        return True
    if code is None:
        return False
    return code.startswith("RE")


# ---------------------------------------------------------------------------
# Core state machine
# ---------------------------------------------------------------------------

def step(state: PLDState, event: Dict[str, Any]) -> TransitionResult:
    """
    Apply a single PLD event to the current PLDState.

    Parameters
    ----------
    state:
        Existing PLDState for this session / trace.

    event:
        A dict representing a PLD event (pld_event.schema.json).

    Returns
    -------
    TransitionResult
        Contains updated state, validity flag, and transition metadata.

    Notes
    -----
    This state machine is intentionally simple:

        none → drift → repair → reentry → outcome

    With permissive handling of:
        - repeated drift (overwrites active drift)
        - repairs without prior drift (remain in "repair" phase)
        - reentry without repair (treated as phase move, but flagged invalid)
    """
    from_phase: Phase = state.phase
    phase, code = _extract_phase_and_code(event)
    timestamp = _extract_timestamp(event)
    event_id = str(event.get("event_id", "")) or None

    new_state = PLDState(
        phase=state.phase,
        active_drift_code=state.active_drift_code,
        active_repair_code=state.active_repair_code,
        cycles_completed=state.cycles_completed,
        last_event_id=event_id or state.last_event_id,
        last_timestamp=timestamp or state.last_timestamp,
    )

    reason = ""
    valid = True

    # No phase information → no state change.
    if phase == "none":
        reason = "No PLD phase on event; state unchanged."
        return TransitionResult(
            from_phase=from_phase,
            to_phase=new_state.phase,
            valid=True,
            reason=reason,
            state=new_state,
        )

    # Drift-like event
    if _is_drift(code, phase):
        new_state.phase = "drift"
        new_state.active_drift_code = code
        new_state.active_repair_code = None
        reason = "Drift detected; entering drift phase."

        # If we already had an active drift, this overwrites it.
        if state.active_drift_code is not None:
            reason = "New drift overwrote previous active drift."
        return TransitionResult(
            from_phase=from_phase,
            to_phase=new_state.phase,
            valid=True,
            reason=reason,
            state=new_state,
        )

    # Repair-like event
    if _is_repair(code, phase):
        new_state.phase = "repair"
        new_state.active_repair_code = code

        if state.active_drift_code is None:
            reason = "Repair observed without active drift."
            # Conceptually a weaker/invalid sequence, but we still move the phase.
            valid = False
        else:
            reason = "Repair observed for active drift."

        return TransitionResult(
            from_phase=from_phase,
            to_phase=new_state.phase,
            valid=valid,
            reason=reason,
            state=new_state,
        )

    # Reentry-like event
    if _is_reentry(code, phase):
        new_state.phase = "reentry"

        if state.active_repair_code is None:
            reason = "Reentry observed without active repair."
            valid = False
        else:
            reason = "Reentry observed after repair."
            # Completed cycle: drift → repair → reentry
            new_state.cycles_completed += 1
            # Reset active drift/repair after a successful cycle
            new_state.active_drift_code = None
            new_state.active_repair_code = None

        return TransitionResult(
            from_phase=from_phase,
            to_phase=new_state.phase,
            valid=valid,
            reason=reason,
            state=new_state,
        )

    # Outcome and other phases:
    if phase == "outcome":
        new_state.phase = "outcome"
        reason = "Outcome event observed; marking latest known phase as outcome."
        # Outcome does not reset cycles or active drift/repair on its own.
        return TransitionResult(
            from_phase=from_phase,
            to_phase=new_state.phase,
            valid=True,
            reason=reason,
            state=new_state,
        )

    # Fallback: unknown phase value.
    reason = "Unknown or unsupported PLD phase; state unchanged."
    return TransitionResult(
        from_phase=from_phase,
        to_phase=new_state.phase,
        valid=False,
        reason=reason,
        state=new_state,
    )


# ---------------------------------------------------------------------------
# Convenience API
# ---------------------------------------------------------------------------

def initial_state() -> PLDState:
    """
    Return a fresh PLDState with no active drift or repair.
    """
    return PLDState()


__all__ = [
    "Phase",
    "PLDState",
    "TransitionResult",
    "step",
    "initial_state",
]
