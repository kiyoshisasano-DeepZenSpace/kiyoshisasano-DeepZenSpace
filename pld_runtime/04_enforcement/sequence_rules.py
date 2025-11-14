#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.enforcement.sequence_rules

Temporal enforcement for Phase Loop Dynamics (PLD) event streams.

This module checks that event sequences respect core PLD runtime rules, e.g.:

    Drift ⇒ (within Δt) Repair ⇒ (within Δt) Reentry

It operates on already-logged PLD events or envelopes and assumes that
structural validation has been handled by schema_validator.

Key ideas:
- Drift, Repair, Reentry are inferred from the PLD phase field (preferred)
  and/or event_type as a fallback.
- Time is interpreted from RFC3339 / ISO8601 timestamps on each event.
- Violations are reported as structured objects, not exceptions.

This module does not modify events; it only inspects them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Literal, Optional, Sequence, Tuple


Role = Literal["drift", "repair", "reentry", "other", "unknown"]

EnvelopeMode = Literal["event", "envelope"]


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class SequenceRuleConfig:
    """
    Configuration for temporal PLD sequence checks.

    All thresholds are in milliseconds.

    Semantics:

    - max_drift_to_repair_ms:
        Upper bound Δt between a Drift and its corresponding Repair.
        If exceeded, a DRIFT_TIMEOUT violation is recorded.

    - max_repair_to_reentry_ms:
        Upper bound Δt between a Repair and its corresponding Reentry.
        If exceeded, a REPAIR_TIMEOUT violation is recorded.

    - require_repair_for_drift:
        If True, any drift that never receives a repair by the end of the
        sequence produces a DRIFT_WITHOUT_REPAIR violation.

    - require_reentry_after_repair:
        If True, any repair that never receives reentry by the end of the
        sequence produces a REPAIR_WITHOUT_REENTRY violation.

    - allow_reentry_without_repair:
        If False, any reentry not preceded by a repair produces a
        REENTRY_WITHOUT_PRECEDING_REPAIR violation.
    """

    max_drift_to_repair_ms: int = 30000
    max_repair_to_reentry_ms: int = 30000
    require_repair_for_drift: bool = True
    require_reentry_after_repair: bool = True
    allow_reentry_without_repair: bool = False


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class SequenceViolation:
    """
    A single violation of PLD temporal sequence rules.
    """

    code: str
    message: str
    index: int
    event_id: Optional[str] = None
    session_id: Optional[str] = None
    drift_code: Optional[str] = None
    repair_code: Optional[str] = None
    reentry_code: Optional[str] = None
    drift_to_repair_ms: Optional[float] = None
    repair_to_reentry_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "index": self.index,
            "event_id": self.event_id,
            "session_id": self.session_id,
            "drift_code": self.drift_code,
            "repair_code": self.repair_code,
            "reentry_code": self.reentry_code,
            "drift_to_repair_ms": self.drift_to_repair_ms,
            "repair_to_reentry_ms": self.repair_to_reentry_ms,
        }


@dataclass
class SequenceAnalysisResult:
    """
    Summary results for a single event sequence (e.g., one session / trace).
    """

    ok: bool
    violations: List[SequenceViolation] = field(default_factory=list)
    cycles_analyzed: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "cycles_analyzed": self.cycles_analyzed,
            "violations": [v.to_dict() for v in self.violations],
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_ts(ts: str) -> datetime:
    """
    Parse RFC3339 / ISO8601 timestamps, including 'Z'.

    This keeps behavior deterministic and avoids depending on external libs.
    """
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts).astimezone(timezone.utc)


def _extract_inner_event(
    obj: Dict[str, Any],
    mode: EnvelopeMode,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Return (event, envelope_like) for a given object.

    - In "event" mode, event == obj and envelope_like == {}.
    - In "envelope" mode, event == obj["event"] and envelope_like == obj.
    """
    if mode == "event":
        return obj, {}
    if "event" not in obj or not isinstance(obj["event"], dict):
        # Treat malformed envelope as a bare event to avoid hard failure.
        return obj, obj
    return obj["event"], obj


def _classify_role(event: Dict[str, Any]) -> Role:
    """
    Infer the PLD role of an event using:

    1. event["pld"]["phase"] if present and recognized
    2. fallback heuristics on event["event_type"]
    """
    pld = event.get("pld") or {}
    phase = str(pld.get("phase", "")).lower()
    if phase in {"drift", "repair", "reentry"}:
        return phase  # type: ignore[return-value]
    if phase == "outcome":
        return "other"
    if phase == "none":
        return "other"

    et = str(event.get("event_type", "")).lower()
    if "drift" in et:
        return "drift"
    if "repair" in et:
        return "repair"
    if "reentry" in et:
        return "reentry"

    return "unknown"


def _event_timestamp(event: Dict[str, Any]) -> Optional[datetime]:
    ts = event.get("timestamp")
    if not isinstance(ts, str):
        return None
    try:
        return _parse_ts(ts)
    except Exception:
        return None


def _event_codes(event: Dict[str, Any]) -> Tuple[Optional[str], Optional[str]]:
    """
    Return (phase, code) from the event if available.

    phase is typically one of "drift", "repair", "reentry", "outcome", "none".
    code is a concrete PLD code like "D1_information_drift".
    """
    pld = event.get("pld") or {}
    phase = pld.get("phase")
    code = pld.get("code")
    return (phase, code)


def _ms_between(a: datetime, b: datetime) -> float:
    return (b - a).total_seconds() * 1000.0


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_sequence(
    events: Sequence[Dict[str, Any]],
    *,
    config: Optional[SequenceRuleConfig] = None,
    mode: EnvelopeMode = "event",
) -> SequenceAnalysisResult:
    """
    Analyze a sequence of PLD events or envelopes for temporal rule violations.

    Parameters
    ----------
    events:
        An ordered list of events (or envelopes if mode="envelope").
        The order should reflect the true temporal order of emission.

    config:
        SequenceRuleConfig with timeouts and strictness flags.
        If None, defaults are used.

    mode:
        - "event": each element is a PLD event (pld_event.schema.json).
        - "envelope": each element is a runtime envelope object with an
          "event" field containing the PLD event.

    Returns
    -------
    SequenceAnalysisResult
        Includes a flag indicating whether the sequence passes all checks,
        plus a list of violations (if any).
    """
    cfg = config or SequenceRuleConfig()
    violations: List[SequenceViolation] = []

    active_drift_index: Optional[int] = None
    active_drift_ts: Optional[datetime] = None
    active_drift_code: Optional[str] = None

    active_repair_index: Optional[int] = None
    active_repair_ts: Optional[datetime] = None
    active_repair_code: Optional[str] = None

    active_reentry_code: Optional[str] = None

    cycles = 0

    for idx, raw_obj in enumerate(events):
        event, env = _extract_inner_event(raw_obj, mode)
        role = _classify_role(event)
        ts = _event_timestamp(event)
        phase, code = _event_codes(event)

        event_id = event.get("event_id") or env.get("envelope_id")
        session_id = event.get("session_id") or (env.get("session") or {}).get("session_id")

        # Skip events without timestamp to avoid breaking sequence metrics.
        if ts is None:
            continue

        if role == "drift":
            # If there is a previous unresolved drift, we can optionally log that.
            if active_drift_index is not None and cfg.require_repair_for_drift:
                violations.append(
                    SequenceViolation(
                        code="DRIFT_WITHOUT_REPAIR_BEFORE_NEXT_DRIFT",
                        message="New drift occurred before previous drift was repaired.",
                        index=idx,
                        event_id=event_id,
                        session_id=session_id,
                        drift_code=active_drift_code,
                    )
                )
            active_drift_index = idx
            active_drift_ts = ts
            active_drift_code = code
            active_repair_index = None
            active_repair_ts = None
            active_repair_code = None
            active_reentry_code = None

        elif role == "repair":
            if active_drift_ts is None:
                # Repair without preceding drift
                if cfg.require_repair_for_drift:
                    violations.append(
                        SequenceViolation(
                            code="REPAIR_WITHOUT_PRECEDING_DRIFT",
                            message="Repair occurred without a preceding drift.",
                            index=idx,
                            event_id=event_id,
                            session_id=session_id,
                            repair_code=code,
                        )
                    )
            else:
                # Drift → Repair timing
                dt_ms = _ms_between(active_drift_ts, ts)
                if dt_ms > cfg.max_drift_to_repair_ms:
                    violations.append(
                        SequenceViolation(
                            code="DRIFT_TIMEOUT",
                            message=(
                                f"Repair occurred after {dt_ms:.1f} ms (> "
                                f"{cfg.max_drift_to_repair_ms} ms) from drift."
                            ),
                            index=idx,
                            event_id=event_id,
                            session_id=session_id,
                            drift_code=active_drift_code,
                            repair_code=code,
                            drift_to_repair_ms=dt_ms,
                        )
                    )
                active_repair_index = idx
                active_repair_ts = ts
                active_repair_code = code

        elif role == "reentry":
            if active_repair_ts is None:
                if not cfg.allow_reentry_without_repair:
                    violations.append(
                        SequenceViolation(
                            code="REENTRY_WITHOUT_PRECEDING_REPAIR",
                            message="Reentry occurred without a preceding repair.",
                            index=idx,
                            event_id=event_id,
                            session_id=session_id,
                            reentry_code=code,
                        )
                    )
            else:
                dt_ms = _ms_between(active_repair_ts, ts)
                if dt_ms > cfg.max_repair_to_reentry_ms:
                    violations.append(
                        SequenceViolation(
                            code="REPAIR_TIMEOUT",
                            message=(
                                f"Reentry occurred after {dt_ms:.1f} ms (> "
                                f"{cfg.max_repair_to_reentry_ms} ms) from repair."
                            ),
                            index=idx,
                            event_id=event_id,
                            session_id=session_id,
                            drift_code=active_drift_code,
                            repair_code=active_repair_code,
                            reentry_code=code,
                            repair_to_reentry_ms=dt_ms,
                        )
                    )
                active_reentry_code = code
                # A full drift→repair→reentry cycle has completed.
                cycles += 1
                active_drift_index = None
                active_drift_ts = None
                active_drift_code = None
                active_repair_index = None
                active_repair_ts = None
                active_repair_code = None
                active_reentry_code = None

        else:
            # other / unknown role: ignored for temporal cycle rules.
            pass

    # End-of-sequence checks
    if active_drift_index is not None and cfg.require_repair_for_drift:
        violations.append(
            SequenceViolation(
                code="DRIFT_WITHOUT_REPAIR",
                message="Sequence ended with an unrepaired drift.",
                index=active_drift_index,
                drift_code=active_drift_code,
            )
        )

    if active_repair_index is not None and cfg.require_reentry_after_repair:
        violations.append(
            SequenceViolation(
                code="REPAIR_WITHOUT_REENTRY",
                message="Sequence ended with a repair that never reached reentry.",
                index=active_repair_index,
                drift_code=active_drift_code,
                repair_code=active_repair_code,
            )
        )

    ok = len(violations) == 0
    return SequenceAnalysisResult(ok=ok, violations=violations, cycles_analyzed=cycles)


__all__ = [
    "SequenceRuleConfig",
    "SequenceViolation",
    "SequenceAnalysisResult",
    "analyze_sequence",
]
