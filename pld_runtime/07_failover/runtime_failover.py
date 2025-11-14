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
        - strategy_id       (e.g., "none", "safe_reset", "human_handoff")
        - severity          ("info" / "warning" / "error" / "critical")
        - hard_reset        (bool)
        - preferred_route   (optional RouteTarget)
        - metadata          (hints for backoff, model switch, etc.)

Procedure
---------
1. Inspect PolicyEvaluation:
      - if ok=True → no failover (strategy "none")
      - otherwise, find the highest-severity decisions.
2. Combine with PLDState:
      - repeated drift cycles without successful reentry
      - frequent repairs / resets
3. Optionally look at SequenceAnalysisResult:
      - missing repair / missing reentry patterns
      - repeated DRIFT_WITHOUT_REPAIR_BEFORE_NEXT_DRIFT
4. Map this context into a FailoverDecision:
      - no-op / soft-degrade / safe-reset / human-handoff, etc.

Implementation
--------------
This module is *pure decision logic*:
    - no logging
    - no network calls
    - no side-effects
Concrete behavior is implemented by:
    - controllers.action_router (RouteInstruction → runtime actions)
    - future failover.strategy_registry, failover.backoff_policies

Validation
---------
Unit tests should assert:
    - stable mapping from (policy, state) → strategy_id
    - monotonicity w.r.t. severity escalation
    - no hard_reset when severity is only INFO/WARNING

Next Step
---------
A separate `strategy_registry.py` can define named strategies and
associate them with concrete runtime recipes (tool calls, model changes).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from ..enforcement.response_policy import (
    PolicyEvaluation,
    PolicyDecision,
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

    Fields
    ------
    strategy:
        Chosen FailoverStrategy, or NONE.

    severity:
        Highest observed severity (from PolicyEvaluation or derived).

    hard_reset:
        True if the strategy implies losing conversational state
        (session reset, context discard).

    preferred_route_target:
        Optional RouteTarget that is most appropriate for the strategy,
        e.g., SESSION_CONTROL or HUMAN_ESCALATION.

    triggered_by_codes:
        Policy decision codes or sequence violation codes that led
        to this failover.

    metadata:
        Free-form hints (e.g., suggested backoff, new model name, etc.).
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

    Fields
    ------
    session_id:
        Session identifier.

    policy:
        PolicyEvaluation for the latest turn.

    state:
        Current PLDState (phase, cycles, active drift/repair).

    sequence_result:
        Optional SequenceAnalysisResult for the session.

    routes:
        Optional list of RouteInstruction produced for the latest turn.
    """

    session_id: str
    policy: PolicyEvaluation
    state: PLDState
    sequence_result: Optional[SequenceAnalysisResult] = None
    routes: List[RouteInstruction] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers: severity aggregation
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


def _collect_trigger_codes(policy: PolicyEvaluation) -> List[str]:
    return [d.code for d in policy.decisions]


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
            → ISOLATE_AND_AUDIT or HUMAN_HANDOFF (depending on codes)
        else if ERROR:
            → SAFE_RESET_SESSION or SWITCH_MODEL_SHADOW
        else if WARNING:
            → SOFT_DEGRADE or FALLBACK_TOOL_ONLY

    PLDState is used to refine decisions, for example:

        - Many cycles_completed with recurring drift
          → stronger strategy (e.g., switch model, human handoff)

        - Active drift with no repair yet
          → prefer soft degrade over hard reset
    """
    policy = ctx.policy
    severity = _max_severity(*(d.severity for d in policy.decisions))
    triggered_codes = _collect_trigger_codes(policy)

    # Default: no failover
    if policy.ok:
        return FailoverDecision(
            strategy=FailoverStrategy.NONE,
            severity=severity,
            hard_reset=False,
            preferred_route_target=None,
            triggered_by_codes=triggered_codes,
            metadata={"reason": "policy_ok"},
        )

    # Determine base strategy by severity
    if severity == Severity.CRITICAL:
        decision = _decide_for_critical(ctx, severity, triggered_codes)
    elif severity == Severity.ERROR:
        decision = _decide_for_error(ctx, severity, triggered_codes)
    elif severity == Severity.WARNING:
        decision = _decide_for_warning(ctx, severity, triggered_codes)
    else:
        decision = _decide_for_info(ctx, severity, triggered_codes)

    return decision


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
             → SAFE_RESET_SESSION with HUMAN_HANDOFF as preferred route.
    """
    has_abort = any(d.action == PolicyAction.ABORT_SESSION for d in ctx.policy.decisions)
    has_escalate = any(d.action == PolicyAction.ESCALATE for d in ctx.policy.decisions)

    if has_abort or has_escalate:
        # Choose between isolation vs handoff based on drift cycles
        if ctx.state.cycles_completed >= 2:
            strategy = FailoverStrategy.ISOLATE_AND_AUDIT
            route = RouteTarget.SESSION_CONTROL
            reason = "critical_with_repeated_cycles"
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
                "cycles_completed": ctx.state.cycles_completed,
                "phase": ctx.state.phase,
            },
        )

    # Fallback: safe reset + handoff
    return FailoverDecision(
        strategy=FailoverStrategy.SAFE_RESET_SESSION,
        severity=severity,
        hard_reset=True,
        preferred_route_target=RouteTarget.SESSION_CONTROL,
        triggered_by_codes=triggered_codes,
        metadata={
            "reason": "critical_without_explicit_abort",
            "cycles_completed": ctx.state.cycles_completed,
            "phase": ctx.state.phase,
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
        - Otherwise:
            → SAFE_RESET_SESSION
    """
    state = ctx.state
    active_drift = state.active_drift_code is not None
    active_repair = state.active_repair_code is not None

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
