#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.controllers.pld_controller

High-level runtime controller that connects:

    ingestion/NormalizedTurn
        → detection/RuntimeSignalBridge
        → enforcement (schema + sequence + policy)
        → controllers/state_machine (online PLD state)

Responsibilities
----------------
- Maintain per-session PLD state (phase, active drift/repair, cycles).
- Run detection on each normalized turn.
- Optionally validate events and envelopes against schemas.
- Optionally run sequence rules across the session.
- Produce a policy evaluation (what SHOULD happen next).
- Expose all of the above as a structured outcome per turn.

Non-goals
---------
- It does NOT:
    - call tools or LLMs to execute repairs
    - mutate external system state
    - write logs to disk / DB

Those behaviors should be implemented by the host application or
by a separate action router.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional, Tuple

from ..detection.runtime_signal_bridge import (
    RuntimeSignalBridge,
    BridgeConfig,
    NormalizedTurn,
    BridgeResult,
    wrap_event_in_envelope,
)
from ..enforcement.schema_validator import (
    ValidationResult,
    validate_event,
    validate_envelope,
)
from ..enforcement.sequence_rules import (
    SequenceAnalysisResult,
    analyze_sequence,
)
from ..enforcement.response_policy import (
    PolicyEvaluation,
    evaluate_policy,
)
from ..enforcement.thresholds import (
    EnforcementMode,
)
from .state_machine import (
    PLDState,
    TransitionResult,
    initial_state,
    step as state_step,
)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class ControllerConfig:
    """
    Configuration for PldRuntimeController.

    Attributes
    ----------
    enforcement_mode:
        Overall enforcement posture: strict / balanced / observational.

    enable_schema_validation:
        If True, validate events and envelopes against JSON Schemas.

    enable_sequence_checks:
        If True, run sequence_rules.analyze_sequence over the session history.

    auto_wrap_envelope:
        If True, each event is wrapped in a runtime envelope.

    platform:
        Platform identifier written into envelopes.

    environment:
        Runtime environment written into envelopes.

    mode:
        Runtime mode written into envelopes.
    """

    enforcement_mode: EnforcementMode = EnforcementMode.BALANCED
    enable_schema_validation: bool = True
    enable_sequence_checks: bool = True
    auto_wrap_envelope: bool = True

    platform: str = "unknown"
    environment: str = "sandbox"
    mode: str = "debug"


# ---------------------------------------------------------------------------
# Outcome Model
# ---------------------------------------------------------------------------

@dataclass
class ControllerEventRecord:
    """
    Per-event record produced while processing a single turn.
    """

    event: Dict[str, Any]
    envelope: Optional[Dict[str, Any]]
    event_validation: Optional[ValidationResult]
    envelope_validation: Optional[ValidationResult]
    state_transition: Optional[TransitionResult]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event": self.event,
            "envelope": self.envelope,
            "event_validation": self.event_validation.to_dict() if self.event_validation else None,
            "envelope_validation": self.envelope_validation.to_dict() if self.envelope_validation else None,
            "state_transition": self.state_transition.to_dict() if self.state_transition else None,
        }


@dataclass
class ControllerOutcome:
    """
    Aggregated outcome for processing a single NormalizedTurn.
    """

    session_id: str
    turn: Dict[str, Any]
    bridge: Dict[str, Any]

    state_after: Dict[str, Any]
    events: List[ControllerEventRecord]

    sequence_result: Optional[SequenceAnalysisResult]
    policy_evaluation: PolicyEvaluation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "turn": self.turn,
            "bridge": self.bridge,
            "state_after": self.state_after,
            "events": [e.to_dict() for e in self.events],
            "sequence_result": self.sequence_result.to_dict() if self.sequence_result else None,
            "policy_evaluation": self.policy_evaluation.to_dict(),
        }


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------

class PldRuntimeController:
    """
    High-level orchestrator for PLD runtime operations.

    Lifecycle (per turn)
    --------------------
        1. Take a NormalizedTurn.
        2. Run RuntimeSignalBridge → get PLD events.
        3. (Optional) validate events / envelopes.
        4. Update PLD state machine with each event.
        5. (Optional) run sequence rules over session history.
        6. Run response policy → PolicyEvaluation.
        7. Return ControllerOutcome.

    This class keeps in-memory session state and event history;
    persistence is left to the caller.
    """

    def __init__(
        self,
        bridge_config: Optional[BridgeConfig] = None,
        controller_config: Optional[ControllerConfig] = None,
    ) -> None:
        self.bridge = RuntimeSignalBridge(bridge_config)
        self.config = controller_config or ControllerConfig()

        # PLD state per session_id
        self._state_by_session: Dict[str, PLDState] = {}
        # Event history per session_id (bare PLD events, not envelopes)
        self._events_by_session: Dict[str, List[Dict[str, Any]]] = {}

    # ---------- public API ----------

    def process_turn(
        self,
        turn: NormalizedTurn,
        *,
        turn_index: Optional[int] = None,
        user_id: Optional[str] = None,
    ) -> ControllerOutcome:
        """
        Process a single normalized turn and return a ControllerOutcome.

        Parameters
        ----------
        turn:
            NormalizedTurn from ingestion layer.

        turn_index:
            Optional position within the session trace.

        user_id:
            Optional user identifier used in envelopes.

        Notes
        -----
        - Multiple PLD events may be produced from a single turn.
        - sequence_result is computed at the session level (all events so far).
        - policy_evaluation considers:
            - latest sequence_result (if enabled)
            - latest validation results (if available)
        """
        session_id = turn.session_id
        state_before = self._get_state(session_id)

        bridge_result = self.bridge.process_turn(turn)
        records: List[ControllerEventRecord] = []

        # Ensure history containers
        history = self._events_by_session.setdefault(session_id, [])

        current_state = state_before
        last_event_validation: Optional[ValidationResult] = None
        last_envelope_validation: Optional[ValidationResult] = None

        for event in bridge_result.events:
            envelope: Optional[Dict[str, Any]] = None
            event_val: Optional[ValidationResult] = None
            envelope_val: Optional[ValidationResult] = None

            if self.config.auto_wrap_envelope:
                envelope = wrap_event_in_envelope(
                    event,
                    session_id=session_id,
                    user_id=user_id,
                    platform=self.config.platform,
                    environment=self.config.environment,
                    mode=self.config.mode,
                    trace_id=None,
                    turn_index=turn_index,
                )

            if self.config.enable_schema_validation:
                event_val = validate_event(event)
                last_event_validation = event_val

                if envelope is not None:
                    envelope_val = validate_envelope(envelope)
                    last_envelope_validation = envelope_val

            # Update local state machine
            transition = state_step(current_state, event)
            current_state = transition.state

            # Append to session history (for sequence rules)
            history.append(event)

            records.append(
                ControllerEventRecord(
                    event=event,
                    envelope=envelope,
                    event_validation=event_val,
                    envelope_validation=envelope_val,
                    state_transition=transition,
                )
            )

        # Store updated state
        self._state_by_session[session_id] = current_state

        # Sequence analysis over entire session history
        seq_result: Optional[SequenceAnalysisResult] = None
        if self.config.enable_sequence_checks and history:
            seq_result = analyze_sequence(history, mode="event")

        # Evaluate policy (what should happen next)
        policy = evaluate_policy(
            mode=self.config.enforcement_mode,
            sequence_result=seq_result,
            event_validation=last_event_validation,
            envelope_validation=last_envelope_validation,
        )

        return ControllerOutcome(
            session_id=session_id,
            turn=turn.to_dict(),
            bridge=bridge_result.to_dict(),
            state_after=current_state.to_dict(),
            events=records,
            sequence_result=seq_result,
            policy_evaluation=policy,
        )

    # ---------- internal helpers ----------

    def _get_state(self, session_id: str) -> PLDState:
        """
        Return existing PLDState for the session, or initialize one.
        """
        if session_id not in self._state_by_session:
            self._state_by_session[session_id] = initial_state()
        return self._state_by_session[session_id]

    def get_state_snapshot(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Read-only snapshot of current PLD state for a session.
        """
        state = self._state_by_session.get(session_id)
        return state.to_dict() if state else None

    def get_session_events(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Return a shallow copy of the PLD event history for a session.
        """
        return list(self._events_by_session.get(session_id, []))


__all__ = [
    "ControllerConfig",
    "ControllerEventRecord",
    "ControllerOutcome",
    "PldRuntimeController",
]
