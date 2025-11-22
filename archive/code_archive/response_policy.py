#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.enforcement.response_policy (v1.1 Canonical Edition)

Map validation / sequence analysis results to runtime-friendly
policy decisions.

This module does NOT execute repairs or mutate state.
It only decides *what should happen* given:

- schema validation results
- temporal sequence analysis (drift → repair → reentry → outcome)
- enforcement mode / thresholds

Controllers or runtime hosts are expected to consume these decisions
and implement concrete behavior (e.g., tool calls, resets, logging).

Canonical Alignment
-------------------
- Phases:  drift → repair → reentry → outcome → none
- Codes:   D*/R*/RE* taxonomy (see pld_runtime/01_schemas/drift_repair_codes.json)
- Events:  Compatible with pld_event.schema.json
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional

from .schema_validator import ValidationResult
from .sequence_rules import (
    SequenceAnalysisResult,
    SequenceViolation,
)
from .thresholds import (
    EnforcementMode,
    Thresholds,
    get_thresholds,
)


# ---------------------------------------------------------------------------
# Decision model
# ---------------------------------------------------------------------------

class PolicyAction(str, Enum):
    """
    High-level action categories that controllers can implement.

    These are **abstract runtime intents** that can be mapped onto
    concrete repair behaviors using canonical PLD codes:

        - R1_clarify
        - R2_soft_repair
        - R3_rewrite
        - R4_request_clarification
        - R5_hard_reset

    Actions
    -------
    LOG_ONLY:
        Record the event / violation, but do not alter runtime behavior.

    SOFT_REPAIR:
        Suggest or trigger soft / local repair behavior
        (typically R1_clarify or R2_soft_repair, possibly R3_rewrite).

    STRUCTURAL_REPAIR:
        Suggest or trigger structural repair, including more invasive
        interventions that may map to R2_soft_repair or R5_hard_reset.

    ESCALATE:
        Escalate to human / supervisor / secondary pipeline.
        Often paired with R4_request_clarification at the UX level.

    ABORT_SESSION:
        Request session termination or hard reset
        (usually R5_hard_reset at the PLD level).

    NOOP:
        No action; everything is within tolerances.
    """

    LOG_ONLY = "log_only"
    SOFT_REPAIR = "soft_repair"
    STRUCTURAL_REPAIR = "structural_repair"
    ESCALATE = "escalate"
    ABORT_SESSION = "abort_session"
    NOOP = "noop"


class Severity(str, Enum):
    """
    Severity of a policy decision.

    - INFO:
        Purely informational. No direct risk to the interaction.

    - WARNING:
        May degrade interaction quality but not considered critical.

    - ERROR:
        Clear violation of expected behavior, requires attention or
        non-trivial repair.

    - CRITICAL:
        Severe breakdown (e.g., repeated drift without repair,
        schema corruption). Likely requires abort / hard reset.
    """

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class PolicyDecision:
    """
    A single policy decision derived from validation / sequence analysis.

    Fields
    ------
    action:
        High-level PolicyAction recommended by enforcement.

    severity:
        Severity classification for this decision.

    code:
        Short decision code or violation key, e.g. "DRIFT_TIMEOUT",
        "SCHEMA_INVALID_EVENT", "NO_VIOLATION".

    message:
        Human-readable explanation suitable for logs or dashboards.

    details:
        Optional contextual metadata (indexes, timings, validator info, etc).
    """

    action: PolicyAction
    severity: Severity
    code: str
    message: str

    # Optional contextual metadata
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Enum to str for JSON-friendliness
        d["action"] = self.action.value
        d["severity"] = self.severity.value
        return d


@dataclass
class PolicyEvaluation:
    """
    Aggregated response policy evaluation for a session / trace.

    Controllers can use this as the "what should we do next?" object.

    Fields
    ------
    ok:
        True if all decisions are NOOP or LOG_ONLY. False otherwise.

    mode:
        Effective EnforcementMode used for this evaluation.

    thresholds:
        Thresholds object derived from mode (e.g., max drift count,
        timeouts, severity escalation rules).

    decisions:
        List of PolicyDecision entries (may be a single NOOP).
    """

    ok: bool
    mode: EnforcementMode
    thresholds: Thresholds
    decisions: List[PolicyDecision] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ok": self.ok,
            "mode": self.mode.value,
            "thresholds": self.thresholds.to_dict(),
            "decisions": [d.to_dict() for d in self.decisions],
        }


# ---------------------------------------------------------------------------
# Helpers: mapping violations → decisions
# ---------------------------------------------------------------------------

# Simple mapping from violation code to severity / suggested action.
# Sequence-related violations are expected to be emitted by sequence_rules.py
# using canonical phases (drift/repair/reentry/outcome).
_VIOLATION_POLICY_MAP: Dict[str, Dict[str, Any]] = {
    # Sequence rules
    "DRIFT_TIMEOUT": {
        "severity": Severity.WARNING,
        "action": PolicyAction.SOFT_REPAIR,
    },
    "REPAIR_TIMEOUT": {
        "severity": Severity.WARNING,
        "action": PolicyAction.SOFT_REPAIR,
    },
    "DRIFT_WITHOUT_REPAIR": {
        "severity": Severity.ERROR,
        "action": PolicyAction.STRUCTURAL_REPAIR,
    },
    "DRIFT_WITHOUT_REPAIR_BEFORE_NEXT_DRIFT": {
        "severity": Severity.ERROR,
        "action": PolicyAction.STRUCTURAL_REPAIR,
    },
    "REPAIR_WITHOUT_REENTRY": {
        "severity": Severity.WARNING,
        "action": PolicyAction.SOFT_REPAIR,
    },
    "REPAIR_WITHOUT_PRECEDING_DRIFT": {
        "severity": Severity.INFO,
        "action": PolicyAction.LOG_ONLY,
    },
    "REENTRY_WITHOUT_PRECEDING_REPAIR": {
        "severity": Severity.WARNING,
        "action": PolicyAction.LOG_ONLY,
    },

    # Schema / structural
    "SCHEMA_INVALID_EVENT": {
        "severity": Severity.ERROR,
        "action": PolicyAction.ESCALATE,
    },
    "SCHEMA_INVALID_ENVELOPE": {
        "severity": Severity.ERROR,
        "action": PolicyAction.ESCALATE,
    },
    "SCHEMA_PARSE_ERROR": {
        "severity": Severity.ERROR,
        "action": PolicyAction.ESCALATE,
    },
}


def _severity_for_mode(base: Severity, mode: EnforcementMode) -> Severity:
    """
    Adjust severity depending on enforcement mode.

    - STRICT:
        Keep or bump to more serious (no downscaling).

    - BALANCED:
        Keep as-is.

    - OBSERVATIONAL:
        Downgrade one level (except CRITICAL, which stays CRITICAL).
    """
    if mode == EnforcementMode.BALANCED:
        return base

    if mode == EnforcementMode.STRICT:
        # Already conservative; no downscaling.
        return base

    # OBSERVATIONAL: downgrade
    if mode == EnforcementMode.OBSERVATIONAL:
        if base == Severity.CRITICAL:
            return Severity.CRITICAL
        if base == Severity.ERROR:
            return Severity.WARNING
        if base == Severity.WARNING:
            return Severity.INFO
        return Severity.INFO

    # Fallback
    return base


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def evaluate_policy(
    *,
    mode: EnforcementMode | str = EnforcementMode.BALANCED,
    sequence_result: Optional[SequenceAnalysisResult] = None,
    event_validation: Optional[ValidationResult] = None,
    envelope_validation: Optional[ValidationResult] = None,
) -> PolicyEvaluation:
    """
    Combine schema validation and sequence-rule analysis into a
    single policy evaluation.

    Typical usage
    -------------
        seq = analyze_sequence(events_for_session, config=..., mode="envelope")
        event_val = validate_event(event)           # optional per-event
        env_val = validate_envelope(envelope_obj)   # optional

        pe = evaluate_policy(
            mode="balanced",
            sequence_result=seq,
            event_validation=event_val,
            envelope_validation=env_val,
        )

    Controllers can then:
        - inspect pe.ok
        - iterate over pe.decisions
        - map PolicyAction → concrete behavior (via ActionRouter, etc.)
    """
    # Normalize mode when passed as string
    if isinstance(mode, str):
        try:
            mode = EnforcementMode(mode.lower())  # type: ignore[arg-type]
        except Exception:
            mode = EnforcementMode.BALANCED

    thresholds = get_thresholds(mode)
    decisions: List[PolicyDecision] = []

    # ---- Schema validation: event ----
    if event_validation is not None and not event_validation.ok:
        for err in event_validation.errors:
            msg = f"Event schema violation at {err.path}: {err.message}"
            decisions.append(
                PolicyDecision(
                    action=_VIOLATION_POLICY_MAP["SCHEMA_INVALID_EVENT"]["action"],
                    severity=_severity_for_mode(
                        _VIOLATION_POLICY_MAP["SCHEMA_INVALID_EVENT"]["severity"],
                        mode,
                    ),
                    code="SCHEMA_INVALID_EVENT",
                    message=msg,
                    details={
                        "validator": err.validator,
                        "validator_value": err.validator_value,
                        "path": err.path,
                    },
                )
            )

    # ---- Schema validation: envelope ----
    if envelope_validation is not None and not envelope_validation.ok:
        for err in envelope_validation.errors:
            msg = f"Envelope schema violation at {err.path}: {err.message}"
            decisions.append(
                PolicyDecision(
                    action=_VIOLATION_POLICY_MAP["SCHEMA_INVALID_ENVELOPE"]["action"],
                    severity=_severity_for_mode(
                        _VIOLATION_POLICY_MAP["SCHEMA_INVALID_ENVELOPE"]["severity"],
                        mode,
                    ),
                    code="SCHEMA_INVALID_ENVELOPE",
                    message=msg,
                    details={
                        "validator": err.validator,
                        "validator_value": err.validator_value,
                        "path": err.path,
                    },
                )
            )

    # ---- Sequence violations ----
    if sequence_result is not None:
        for v in sequence_result.violations:
            base_policy = _VIOLATION_POLICY_MAP.get(
                v.code,
                {
                    "severity": Severity.WARNING,
                    "action": PolicyAction.LOG_ONLY,
                },
            )
            decisions.append(
                PolicyDecision(
                    action=base_policy["action"],
                    severity=_severity_for_mode(base_policy["severity"], mode),
                    code=v.code,
                    message=v.message,
                    details=_violation_details(v),
                )
            )

    # If there are no decisions, add a NOOP to make intent explicit
    if not decisions:
        decisions.append(
            PolicyDecision(
                action=PolicyAction.NOOP,
                severity=Severity.INFO,
                code="NO_VIOLATION",
                message="No schema or sequence violations detected.",
                details={},
            )
        )

    ok = all(d.action in {PolicyAction.NOOP, PolicyAction.LOG_ONLY} for d in decisions)

    return PolicyEvaluation(
        ok=ok,
        mode=mode,
        thresholds=thresholds,
        decisions=decisions,
    )


def _violation_details(v: SequenceViolation) -> Dict[str, Any]:
    """
    Convert a SequenceViolation into a compact metadata dict for decisions.

    The fields are designed to be directly loggable and to support
    downstream metrics such as:

        - PRDR (Post-Repair Drift Recurrence)
        - REI  (Repair Efficiency Index)
        - VRL  (Visible Repair Load)
    """
    return {
        "index": v.index,
        "event_id": v.event_id,
        "session_id": v.session_id,
        "drift_code": v.drift_code,
        "repair_code": v.repair_code,
        "reentry_code": v.reentry_code,
        "drift_to_repair_ms": v.drift_to_repair_ms,
        "repair_to_reentry_ms": v.repair_to_reentry_ms,
    }


__all__ = [
    "PolicyAction",
    "Severity",
    "PolicyDecision",
    "PolicyEvaluation",
    "evaluate_policy",
]
