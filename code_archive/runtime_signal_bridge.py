#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.detection.runtime_signal_bridge (v1.1 Canonical Edition)

Bridge between normalized runtime signals (turns, tool calls, latency info)
and PLD detection modules.

Responsibilities
----------------
- Accept a **normalized runtime turn** (platform-agnostic).
- Run:
    - DriftDetector
    - RepairDetector
    - PatternClassifier (optional)
- Emit:
    - a list of PLD *event* objects (compatible with pld_event.schema.json)
    - helper for wrapping events into runtime envelopes
      (compatible with runtime_event_envelope.json)

Non-goals
---------
- No policy decisions (handled by enforcement/response_policy.py)
- No temporal reasoning (handled by enforcement/sequence_rules.py)
- No schema enforcement (handled by enforcement/schema_validator.py)

Canonical Alignment
-------------------
- Event schema: quickstart/metrics/schemas/pld_event.schema.json
- Runtime schema: pld_runtime/01_schemas/pld_event.schema.json
- PLD codes:     pld_runtime/01_schemas/drift_repair_codes.json
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Literal

from .drift_detector import (
    DriftDetector,
    DriftDetectionConfig,
    DriftDetectionResult,
    drift_signal_to_pld_event,
)
from .repair_detector import (
    RepairDetector,
    RepairDetectionConfig,
    RepairDetectionResult,
    repair_signal_to_pld_event,
)
from .pattern_classifier import (
    PatternClassifier,
    PatternClassifierConfig,
    PatternClassificationResult,
)


Role = Literal["user", "assistant", "system"]


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class NormalizedTurn:
    """
    Platform-agnostic representation of a single runtime turn.

    Expected source: pld_runtime.ingestion.* adapters.

    Attributes
    ----------
    session_id:
        Conversation / agent session identifier.

    turn_id:
        Identifier for this turn within the session (string; platform-specific).

    role:
        "user", "assistant", or "system".

    text:
        Human-readable content (agent output, user input, or system message).

    runtime:
        Runtime information, e.g.:
            {
              "latency_ms": 123,
              "tool_used": "search_api",
              "expected_format": "json",
              "reset_flag": False,
              ...
            }
    """

    session_id: str
    turn_id: str
    role: Role
    text: str
    runtime: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BridgeConfig:
    """
    Configuration for RuntimeSignalBridge.

    Flags
    -----
    enable_drift:
        Run DriftDetector when True.

    enable_repair:
        Run RepairDetector when True.

    enable_pattern_classifier:
        Run PatternClassifier when True.

    drift:
        Configuration for DriftDetector.

    repair:
        Configuration for RepairDetector.

    pattern:
        Configuration for PatternClassifier.
    """

    enable_drift: bool = True
    enable_repair: bool = True
    enable_pattern_classifier: bool = True

    drift: DriftDetectionConfig = field(default_factory=DriftDetectionConfig)
    repair: RepairDetectionConfig = field(default_factory=RepairDetectionConfig)
    pattern: PatternClassifierConfig = field(default_factory=PatternClassifierConfig)


@dataclass
class BridgeResult:
    """
    Combined outcome for a single turn.

    - `events` are PLD events (not envelopes).
    - `drift`, `repair`, `pattern` expose raw detector outputs.
    """

    events: List[Dict[str, Any]] = field(default_factory=list)
    drift: Optional[DriftDetectionResult] = None
    repair: Optional[RepairDetectionResult] = None
    pattern: Optional[PatternClassificationResult] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "events": self.events,
            "drift": self.drift.strongest().__dict__ if self.drift and self.drift.signals else None,
            "repair": self.repair.strongest().__dict__ if self.repair and self.repair.signals else None,
            "pattern": self.pattern.to_dict() if self.pattern else None,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# ---------------------------------------------------------------------------
# Runtime → PLD bridge
# ---------------------------------------------------------------------------

class RuntimeSignalBridge:
    """
    Orchestrates detection modules for a single normalized turn.

    Typical usage
    -------------
        bridge = RuntimeSignalBridge()
        turn = NormalizedTurn(
            session_id="sess-123",
            turn_id="t-10",
            role="assistant",
            text="Sorry, let me correct that...",
            runtime={"latency_ms": 1800}
        )
        result = bridge.process_turn(turn)
        # result.events → list of PLD events
    """

    def __init__(self, config: Optional[BridgeConfig] = None):
        self.config = config or BridgeConfig()
        self._drift_detector = DriftDetector(self.config.drift)
        self._repair_detector = RepairDetector(self.config.repair)
        self._pattern_classifier = PatternClassifier(self.config.pattern)

    # ---- core entrypoint ----

    def process_turn(self, turn: NormalizedTurn) -> BridgeResult:
        """
        Run all enabled detectors on a given turn and return
        a BridgeResult containing PLD events and detector outputs.
        """
        events: List[Dict[str, Any]] = []
        drift_res: Optional[DriftDetectionResult] = None
        repair_res: Optional[RepairDetectionResult] = None
        pattern_res: Optional[PatternClassificationResult] = None

        # ---- Drift detection ----
        if self.config.enable_drift and turn.role == "assistant":
            drift_res = self._drift_detector.detect(
                content=turn.text,
                runtime={
                    "latency_ms": turn.runtime.get("latency_ms"),
                    "tool_used": turn.runtime.get("tool_used"),
                    "expected_format": turn.runtime.get("expected_format"),
                },
            )
            if drift_res.has_drift:
                strongest = drift_res.strongest()
                if strongest:
                    # Drift events are emitted with canonical D* codes.
                    events.append(
                        drift_signal_to_pld_event(
                            strongest,
                            session_id=turn.session_id,
                        )
                    )

        # ---- Repair detection ----
        if self.config.enable_repair and turn.role in ("assistant", "system"):
            repair_res = self._repair_detector.detect(
                content=turn.text,
                runtime={
                    "latency_ms": turn.runtime.get("latency_ms"),
                    "previous_phase": turn.runtime.get("previous_phase"),
                    "tool_used": turn.runtime.get("tool_used"),
                    "reset_flag": turn.runtime.get("reset_flag", False),
                    "previously_failed": turn.runtime.get("previously_failed", False),
                },
            )
            if repair_res.has_repair:
                strongest = repair_res.strongest()
                if strongest:
                    events.append(
                        repair_signal_to_pld_event(
                            strongest,
                            session_id=turn.session_id,
                            turn_id=None,  # turn index may be populated by caller if needed
                        )
                    )

        # ---- Pattern classifier (optional) ----
        if self.config.enable_pattern_classifier:
            pattern_res = self._pattern_classifier.classify_turn(
                text=turn.text,
                role=turn.role,
            )
            # Only emit an extra event if classifier is confident enough and
            # the phase is non-trivial.
            if (
                pattern_res.phase != "none"
                and pattern_res.confidence >= self.config.pattern.min_confidence
            ):
                events.append(
                    _pattern_to_pld_event(
                        pattern_res,
                        session_id=turn.session_id,
                        turn_id=turn.turn_id,
                        role=turn.role,
                    )
                )

        return BridgeResult(
            events=events,
            drift=drift_res,
            repair=repair_res,
            pattern=pattern_res,
        )


# ---------------------------------------------------------------------------
# PatternClassificationResult → PLD event
# ---------------------------------------------------------------------------

def _pattern_to_pld_event(
    cls: PatternClassificationResult,
    *,
    session_id: str,
    turn_id: str,
    role: Role,
) -> Dict[str, Any]:
    """
    Convert a pattern classification into a PLD event.

    This is intentionally generic: the specific drift/repair/reentry codes
    are passed through directly from the classifier, and must conform to
    the canonical v1.1 PLD taxonomy.
    """
    if cls.phase in {"drift", "repair", "reentry", "outcome"}:
        phase = cls.phase
    else:
        phase = "none"

    if phase == "drift":
        event_type = "drift_detected"
    elif phase == "repair":
        event_type = "repair_triggered"
    elif phase == "reentry":
        event_type = "reentry_observed"
    elif phase == "outcome":
        event_type = "outcome_classified"
    else:
        # Fallback to a generic, schema-valid event type.
        event_type = "latency_signal"

    return {
        "event_id": f"pattern-{phase}-{_now_iso()}",
        "timestamp": _now_iso(),
        "session_id": session_id,
        "turn_id": turn_id,
        "source": "detector",
        "event_type": event_type,
        "pld": {
            "phase": phase,
            "code": cls.code,
            "confidence": cls.confidence,
        },
        "payload": {
            "role": role,
            "rationale": cls.rationale,
            "classification_source": cls.source,
        },
        "runtime": {
            "detector": "pattern_classifier_v1_1",
        },
    }


# ---------------------------------------------------------------------------
# Envelope helper
# ---------------------------------------------------------------------------

def wrap_event_in_envelope(
    event: Dict[str, Any],
    *,
    session_id: str,
    user_id: Optional[str] = None,
    platform: str = "unknown",
    environment: str = "sandbox",
    mode: str = "debug",
    trace_id: Optional[str] = None,
    turn_index: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Wrap a PLD event into a runtime envelope compatible with
    runtime_event_envelope.json.

    Parameters
    ----------
    event:
        PLD event object (pld_event.schema.json).

    session_id:
        Session identifier (outer envelope may differ from inner session_id,
        but typically they should match).

    user_id:
        Optional user identifier.

    platform:
        Platform string, one of:
        ["assistants_api", "langgraph", "vertex_ai", "rasa", "open_webchat",
         "batch_eval", "unknown"].

    environment:
        "production", "staging", "sandbox", or "local".

    mode:
        "stream", "batch", "debug", or "audit".

    trace_id:
        Trace identifier, default: derived from session_id if not provided.

    turn_index:
        Integer position within the trace, if known.

    Returns
    -------
    dict
        Envelope object ready for schema validation and logging.
    """
    now = _now_iso()
    env_id = f"env-{event.get('event_id', 'unknown')}-{now}"
    trace_id = trace_id or f"trace-{session_id}"

    if turn_index is None:
        turn_index_val: int = 0
    else:
        turn_index_val = int(turn_index)

    return {
        "envelope_id": env_id,
        "timestamp": now,
        "session": {
            "session_id": session_id,
            "user_id": user_id,
            "platform": platform,
        },
        "trace": {
            "trace_id": trace_id,
            "turn_index": turn_index_val,
        },
        "runtime": {
            "environment": environment,
            "mode": mode,
        },
        "event": event,
    }


__all__ = [
    "NormalizedTurn",
    "BridgeConfig",
    "BridgeResult",
    "RuntimeSignalBridge",
    "wrap_event_in_envelope",
]
