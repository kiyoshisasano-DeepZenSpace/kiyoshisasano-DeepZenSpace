#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.failover.runtime_failover

Concept
-------
Translate PLD runtime signals into a *failover decision* that a host
system can implement.

Inputs:
    - PolicyEvaluation (response_policy)
    - PLDState (controllers.state_machine)
    - optional SequenceAnalysisResult (enforcement.sequence_rules)
    - optional RouteInstruction list (controllers.action_router)

Output:
    - FailoverDecision:
        - strategy         (e.g., "none", "safe_reset_session", "human_handoff")
        - severity         ("info" / "warning" / "error" / "critical")
        - hard_reset       (bool)
        - preferred_route_target (optional RouteTarget)
        - metadata         (hints for backoff, model switch, etc.)

This module is *pure decision logic*:
    - no logging
    - no network calls
    - no side-effects
Concrete behavior is implemented by:
    - controllers.action_router (RouteInstruction → runtime actions)
    - failover.strategy_registry, failover.backoff_policies
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, List, Optional

from ..enforcement.response_policy import (
    PolicyEvaluation,
    PolicyAction,
    Severity,
)
from ..enforcement.sequence_rules import SequenceAnalysisResult
from ..controllers.state_machine import PLDState
from ..controllers.action_router import RouteInstruction, RouteTarget


# ---------------------------------------------------------------------------
# Failover Strategy / Severity
# ---------------------------------------------------------------------------


class FailoverStrategy(str, Enum):
    """
    High-level, implementation-agnostic failover strategies.

    These are *labels*, not concrete behaviors. A host system or a
    strategy registry is expected to map these to specific actions.

    - NONE:
        No failover required.

    - SOFT_DEGRADE:
        Reduce capability surface (e.g., fewer tools, shorter answers)
        without resetting session or escalating.

    - SAFE_RESET_SESSION:
        Reset session state / memory while keeping the same agent stack.

    - SWITCH_MODEL_SHADOW:
        Route traffic to a more conservative or shadow model.

    - FALLBACK_TOOL_ONLY:
        Avoid free-form LLM; rely on tool-based answers where possible.

    - HUMAN_HANDOFF:
        Escalate to human operator or human-in-the-loop.

    - ISOLATE_AND_AUDIT:
        Stop interaction and send session for offline review.
    """

    NONE = "none"
    SOFT_DEGRADE = "soft_degrade"
    SAFE_RESET_SESSION = "safe_reset_session"
    SWITCH_MODEL_SHADOW = "switch_model_shadow"
    FALLBACK_TOOL_ONLY = "fallback_tool_only"
    HUMAN_HANDOFF = "human_handoff"
    ISOLATE_AND_AUDIT = "isolate_and_audit"


@dataclass
class FailoverDecision:
    """
    Final failover decision for a given session at a given time.
    """

    strategy: FailoverStrategy
    severity: Severity
    hard_reset: bool
    preferred_route_target: Optional[RouteTarget]
    triggered_by_codes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["strategy"] = self.strategy.value
        d["severity"] = self.severity.value
        d["preferred_route_target"] = (
            self.preferred_route_target.value if self.preferred_route_target else None
        )
        return d


@dataclass
class FailoverContext:
    """
    Aggregated context for deciding failover.
    """

    session_id: str
    policy: PolicyEvaluation
    state: PLDState
    sequence_result: Optional[SequenceAnalysisResult] = None
    routes: List[RouteInstruction] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers: severity aggregation & trigger collection
# ---------------------------------------------------------------------------

_SEVERITY_ORDER: Dict[Severity, int] = {
    Severity.INFO: 0,
    Severity.WARNING: 1,
    Severity.ERROR: 2,
    Severity.CRITICAL: 3,
}


def _max_severity(*severities: Severity) -> Severity:
    if not severities:
        return Severity.INFO
    return max(severities, key=lambda s: _SEVERITY_ORDER.get(s, 0))


def _collect_trigger_codes(ctx: FailoverContext) -> List[str]:
    """
    Collect codes that contributed to this failover decision.

    Includes:
        - PolicyDecision codes
        - SequenceViolation codes (if any)
    """
    codes: List[str] = [d.code for d in ctx.policy.decisions]
    if ctx.sequence_result is not None:
        codes.extend(v.code for v in ctx.sequence_result.violations)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_codes: List[str] = []
    for c in codes:
        if c in seen:
            continue
        seen.add(c)
        unique_codes.append(c)
    return unique_codes


def _has_sequence_violation(
    ctx: FailoverContext,
    code: str,
) -> bool:
    if ctx.sequence_result is None:
        return False
    return any(v.code == code for v in ctx.sequence_result.violations)


def _sequence_flags(ctx: FailoverContext) -> Dict[str, bool]:
    """
    Convenience flags summarizing key sequence violations.
    """
    return {
        "drift_without_repair": _has_sequence_violation(ctx, "DRIFT_WITHOUT_REPAIR"),
        "drift_timeout": _has_sequence_violation(ctx, "DRIFT_TIMEOUT"),
        "repair_timeout": _has_sequence_violation(ctx, "REPAIR_TIMEOUT"),
        "reentry_without_repair": _has_sequence_violation(
            ctx, "REENTRY_WITHOUT_PRECEDING_REPAIR"
        ),
    }


# ---------------------------------------------------------------------------
# Core decision logic
# ---------------------------------------------------------------------------


def decide_failover(ctx: FailoverContext) -> FailoverDecision:
    """
    Compute a FailoverDecision from FailoverContext.

    High-level mapping:

        if policy.ok:
            → strategy NONE
        else if CRITICAL:
            → ISOLATE_AND_AUDIT or HUMAN_HANDOFF (depending on cycles)
        else if ERROR:
            → SAFE_RESET_SESSION or SWITCH_MODEL_SHADOW / FALLBACK_TOOL_ONLY
        else if WARNING:
            → SOFT_DEGRADE or FALLBACK_TOOL_ONLY

    PLDState and optional sequence_result are used to refine decisions.
    """
    policy = ctx.policy
    severity = _max_severity(*(d.severity for d in policy.decisions))
    triggered_codes = _collect_trigger_codes(ctx)

    # Default: no failover when policy.ok
    if policy.ok:
        return FailoverDecision(
            strategy=FailoverStrategy.NONE,
            severity=severity,
            hard_reset=False,
            preferred_route_target=None,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": "policy_ok",
                "sequence_ok": ctx.sequence_result.ok if ctx.sequence_result else None,
            },
        )

    # Determine base strategy by severity
    if severity == Severity.CRITICAL:
        return _decide_for_critical(ctx, severity, triggered_codes)
    if severity == Severity.ERROR:
        return _decide_for_error(ctx, severity, triggered_codes)
    if severity == Severity.WARNING:
        return _decide_for_warning(ctx, severity, triggered_codes)

    # INFO corner case
    return _decide_for_info(ctx, severity, triggered_codes)


# ---------------------------------------------------------------------------
# Strategy selection helpers by severity level
# ---------------------------------------------------------------------------


def _decide_for_critical(
    ctx: FailoverContext,
    severity: Severity,
    triggered_codes: List[str],
) -> FailoverDecision:
    """
    CRITICAL severity → strong failover.

    Preference order:
        1. If policy contains explicit ABORT_SESSION / ESCALATE:
             → ISOLATE_AND_AUDIT or HUMAN_HANDOFF
        2. Otherwise:
             → SAFE_RESET_SESSION with SESSION_CONTROL as preferred route.
    """
    has_abort = any(d.action == PolicyAction.ABORT_SESSION for d in ctx.policy.decisions)
    has_escalate = any(d.action == PolicyAction.ESCALATE for d in ctx.policy.decisions)
    state = ctx.state

    seq_flags = _sequence_flags(ctx)

    if has_abort or has_escalate:
        # If we already have repeated cycles or strong sequence violations,
        # prefer full isolation over a simple handoff.
        if state.cycles_completed >= 2 or seq_flags["drift_without_repair"]:
            strategy = FailoverStrategy.ISOLATE_AND_AUDIT
            route = RouteTarget.SESSION_CONTROL
            reason = "critical_with_repeated_cycles_or_unrepaired_drift"
        else:
            strategy = FailoverStrategy.HUMAN_HANDOFF
            route = RouteTarget.HUMAN_ESCALATION
            reason = "critical_policy_abort_or_escalate"

        return FailoverDecision(
            strategy=strategy,
            severity=severity,
            hard_reset=True,
            preferred_route_target=route,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": reason,
                "cycles_completed": state.cycles_completed,
                "phase": state.phase,
                "sequence_flags": seq_flags,
            },
        )

    # Fallback: safe reset when critical but no explicit abort/escalate
    return FailoverDecision(
        strategy=FailoverStrategy.SAFE_RESET_SESSION,
        severity=severity,
        hard_reset=True,
        preferred_route_target=RouteTarget.SESSION_CONTROL,
        triggered_by_codes=triggered_codes,
        metadata={
            "reason": "critical_without_explicit_abort",
            "cycles_completed": state.cycles_completed,
            "phase": state.phase,
            "sequence_flags": seq_flags,
        },
    )


def _decide_for_error(
    ctx: FailoverContext,
    severity: Severity,
    triggered_codes: List[str],
) -> FailoverDecision:
    """
    ERROR severity → robust but reversible strategies.

    Heuristic mapping:

        - Many cycles_completed and still error:
            → SWITCH_MODEL_SHADOW
        - Active drift with no repair:
            → FALLBACK_TOOL_ONLY
        - Strong sequence violations (DRIFT_WITHOUT_REPAIR, timeouts):
            → SAFE_RESET_SESSION
        - Otherwise:
            → SAFE_RESET_SESSION (default)
    """
    state = ctx.state
    active_drift = state.active_drift_code is not None
    active_repair = state.active_repair_code is not None
    seq_flags = _sequence_flags(ctx)

    # Strong evidence of structural issues in the sequence
    if seq_flags["drift_without_repair"] or seq_flags["drift_timeout"]:
        return FailoverDecision(
            strategy=FailoverStrategy.SAFE_RESET_SESSION,
            severity=severity,
            hard_reset=True,
            preferred_route_target=RouteTarget.SESSION_CONTROL,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": "error_with_drift_sequence_violation",
                "phase": state.phase,
                "sequence_flags": seq_flags,
            },
        )

    if state.cycles_completed >= 2:
        # Too many loops, consider shadow model
        return FailoverDecision(
            strategy=FailoverStrategy.SWITCH_MODEL_SHADOW,
            severity=severity,
            hard_reset=False,
            preferred_route_target=RouteTarget.AGENT_CONTROL,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": "error_with_repeated_cycles",
                "cycles_completed": state.cycles_completed,
                "phase": state.phase,
                "sequence_flags": seq_flags,
            },
        )

    if active_drift and not active_repair:
        # Drift unresolved; lower capability and rely on tools
        return FailoverDecision(
            strategy=FailoverStrategy.FALLBACK_TOOL_ONLY,
            severity=severity,
            hard_reset=False,
            preferred_route_target=RouteTarget.AGENT_CONTROL,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": "error_with_unresolved_drift",
                "active_drift_code": state.active_drift_code,
                "sequence_flags": seq_flags,
            },
        )

    # Default: reset session but stay on same model
    return FailoverDecision(
        strategy=FailoverStrategy.SAFE_RESET_SESSION,
        severity=severity,
        hard_reset=True,
        preferred_route_target=RouteTarget.SESSION_CONTROL,
        triggered_by_codes=triggered_codes,
        metadata={
            "reason": "error_default_safe_reset",
            "phase": state.phase,
            "sequence_flags": seq_flags,
        },
    )


def _decide_for_warning(
    ctx: FailoverContext,
    severity: Severity,
    triggered_codes: List[str],
) -> FailoverDecision:
    """
    WARNING severity → softer mitigations.

    Mapping:

        - If still in DRIFT phase:
            → SOFT_DEGRADE (shorter replies, fewer tools)
        - If in REPAIR/REENTRY:
            → FALLBACK_TOOL_ONLY (trust tools more than LLM)
        - Otherwise:
            → SOFT_DEGRADE (no reset)
    """
    state = ctx.state

    if state.phase == "drift":
        strategy = FailoverStrategy.SOFT_DEGRADE
        reason = "warning_in_drift_phase"
    elif state.phase in {"repair", "reentry"}:
        strategy = FailoverStrategy.FALLBACK_TOOL_ONLY
        reason = "warning_in_repair_or_reentry"
    else:
        strategy = FailoverStrategy.SOFT_DEGRADE
        reason = "warning_default_soft_degrade"

    return FailoverDecision(
        strategy=strategy,
        severity=severity,
        hard_reset=False,
        preferred_route_target=RouteTarget.AGENT_HINT,
        triggered_by_codes=triggered_codes,
        metadata={
            "reason": reason,
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
        },
    )


def _decide_for_info(
    ctx: FailoverContext,
    severity: Severity,
    triggered_codes: List[str],
) -> FailoverDecision:
    """
    INFO severity but policy.ok=False is a corner case:

    - Typically indicates LOG_ONLY or NOOP with annotations.
    - We choose SOFT_DEGRADE only when cycles are high; otherwise no failover.
    """
    state = ctx.state

    if state.cycles_completed >= 3:
        return FailoverDecision(
            strategy=FailoverStrategy.SOFT_DEGRADE,
            severity=severity,
            hard_reset=False,
            preferred_route_target=RouteTarget.METRICS_ONLY,
            triggered_by_codes=triggered_codes,
            metadata={
                "reason": "info_with_many_cycles",
                "cycles_completed": state.cycles_completed,
            },
        )

    return FailoverDecision(
        strategy=FailoverStrategy.NONE,
        severity=severity,
        hard_reset=False,
        preferred_route_target=None,
        triggered_by_codes=triggered_codes,
        metadata={"reason": "info_level_no_failover"},
    )


__all__ = [
    "FailoverStrategy",
    "FailoverDecision",
    "FailoverContext",
    "decide_failover",
]
