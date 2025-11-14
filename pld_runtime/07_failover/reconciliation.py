#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.failover.reconciliation

Concept
-------
Reconciliation = "how we come back" after a failover event.

Where `runtime_failover` answers:

    "Which failover strategy should we apply now?"

this module answers:

    "Once that strategy has been applied, how and when do we allow the
     system to *reenter* normal operation?"

In PLD terms this is tightly linked to:

    Drift → Repair → Reentry → Outcome

Reconciliation focuses on the **Reentry** side after a failover.

Procedure
---------
Given:
    - current PLDState
    - FailoverDecision (which strategy was chosen)
    - optional StrategySpec (semantics / hints)

we derive a ReconciliationPlan that tells the host system:

    - what kind of reentry is intended
    - whether to reset internal PLD state
    - whether isolation should be lifted
    - whether previous degradation should be relaxed

Implementation
--------------
This module is pure logic:

- no I/O
- no logging
- no timers or sleeps

Host systems are expected to interpret ReconciliationPlan and
apply the actual changes (model switch, reset, session unlock, etc.).

Validation
----------
Unit tests should verify:

- SAFE_RESET_SESSION → fresh session reentry
- HUMAN_HANDOFF → guarded reentry until human release
- ISOLATE_AND_AUDIT → no automatic reentry
- SOFT_DEGRADE / FALLBACK_TOOL_ONLY → soft reentry once conditions improve

Next Step
---------
If more complex policies are needed (time-based, metric-based),
host systems can wrap this module and add their own gating logic.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from enum import Enum
from typing import Any, Dict, Optional

from .runtime_failover import FailoverDecision, FailoverStrategy
from .strategy_registry import StrategySpec, get_strategy_spec
from ..controllers.state_machine import PLDState


# ---------------------------------------------------------------------------
# Reentry / reconciliation model
# ---------------------------------------------------------------------------

class ReentryMode(str, Enum):
    """
    Coarse-grained mode of returning to normal operation.

    - NONE:
        No reentry permitted yet. Session remains in failover/isolation.

    - SOFT_REENTRY:
        Gradual return: keep some mitigations (e.g., degraded capabilities)
        while monitoring for stability.

    - GUARDED_REENTRY:
        Reentry allowed but tightly monitored. Typically after human handoff.

    - FRESH_SESSION:
        Reentry is only allowed via a new session/context. Old state is abandoned.
    """

    NONE = "none"
    SOFT_REENTRY = "soft_reentry"
    GUARDED_REENTRY = "guarded_reentry"
    FRESH_SESSION = "fresh_session"


@dataclass
class ReconciliationPlan:
    """
    Recommended reconciliation behavior after a FailoverDecision.

    Fields
    ------
    reentry_mode:
        How the system is allowed to reenter normal operation.

    reset_pld_state:
        If True, PLDState (phase, cycles, active drift/repair) should be
        reset to initial, usually combined with FRESH_SESSION.

    keep_session_history:
        If True, session traces/logs should be kept available for audit,
        even if a new session is used for user interaction.

    relax_degradation:
        If True, previously applied soft degradation (SOFT_DEGRADE or
        FALLBACK_TOOL_ONLY) may be gradually relaxed.

    allow_isolation_release:
        If True, ISOLATE_AND_AUDIT strategies may be lifted once external
        criteria are met (e.g., human review completed).

    notes:
        Human-readable explanation of the plan.

    metadata:
        Free-form hints for host runtimes, e.g.:
            {
              "min_stable_turns": 3,
              "require_human_ack": True,
            }
    """

    reentry_mode: ReentryMode
    reset_pld_state: bool
    keep_session_history: bool
    relax_degradation: bool
    allow_isolation_release: bool
    notes: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["reentry_mode"] = self.reentry_mode.value
        return d


# ---------------------------------------------------------------------------
# Core reconciliation logic
# ---------------------------------------------------------------------------

def plan_reconciliation(
    *,
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec] = None,
) -> ReconciliationPlan:
    """
    Compute a ReconciliationPlan for a given PLDState and FailoverDecision.

    If StrategySpec is not provided, it is looked up from the registry.
    """
    if spec is None:
        spec = get_strategy_spec(decision.strategy)

    strategy = decision.strategy

    if strategy is FailoverStrategy.NONE:
        return _plan_for_none(state, decision, spec)

    if strategy is FailoverStrategy.SOFT_DEGRADE:
        return _plan_for_soft_degrade(state, decision, spec)

    if strategy is FailoverStrategy.SAFE_RESET_SESSION:
        return _plan_for_safe_reset(state, decision, spec)

    if strategy is FailoverStrategy.SWITCH_MODEL_SHADOW:
        return _plan_for_switch_model(state, decision, spec)

    if strategy is FailoverStrategy.FALLBACK_TOOL_ONLY:
        return _plan_for_fallback_tool(state, decision, spec)

    if strategy is FailoverStrategy.HUMAN_HANDOFF:
        return _plan_for_human_handoff(state, decision, spec)

    if strategy is FailoverStrategy.ISOLATE_AND_AUDIT:
        return _plan_for_isolate_and_audit(state, decision, spec)

    # Fallback: conservative, no automatic reentry
    return ReconciliationPlan(
        reentry_mode=ReentryMode.NONE,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,
        allow_isolation_release=False,
        notes=f"Unknown strategy {strategy.value}; reconciliation disabled.",
        metadata={"phase": state.phase, "cycles_completed": state.cycles_completed},
    )


# ---------------------------------------------------------------------------
# Strategy-specific planning helpers
# ---------------------------------------------------------------------------

def _plan_for_none(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    return ReconciliationPlan(
        reentry_mode=ReentryMode.SOFT_REENTRY
        if state.phase in {"repair", "reentry"}
        else ReentryMode.GUARDED_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes="No failover strategy applied; allow normal reentry with mild monitoring.",
        metadata={
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": decision.triggered_by_codes,
        },
    )


def _plan_for_soft_degrade(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    SOFT_DEGRADE → allow gradual return if system stabilizes.

    Heuristic:
        - keep PLDState
        - require a small number of stable turns before relaxing
    """
    min_stable_turns = max(2, 3 - state.cycles_completed)

    return ReconciliationPlan(
        reentry_mode=ReentryMode.SOFT_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes="Soft degradation in effect; allow gradual relaxation after stability.",
        metadata={
            "min_stable_turns": min_stable_turns,
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "backoff_profile": spec.hints.get("backoff_profile"),
        },
    )


def _plan_for_safe_reset(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    SAFE_RESET_SESSION → require a fresh conversational context,
    but keep history for audit / debugging.
    """
    return ReconciliationPlan(
        reentry_mode=ReentryMode.FRESH_SESSION,
        reset_pld_state=True,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes="Session should be restarted with fresh PLD state; "
              "previous history retained for audit.",
        metadata={
            "require_user_ack": spec.hints.get("require_user_ack", True),
            "allow_resume_with_new_session": spec.hints.get(
                "allow_resume_with_new_session", True
            ),
            "triggered_by": decision.triggered_by_codes,
        },
    )


def _plan_for_switch_model(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    SWITCH_MODEL_SHADOW → reentry continues in a guarded mode
    under a more conservative model.

    PLDState is preserved, but we may require more stable cycles before
    relaxing back to the original model.
    """
    min_stable_turns = max(3, 5 - state.cycles_completed)

    return ReconciliationPlan(
        reentry_mode=ReentryMode.GUARDED_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,  # stay conservative for a while
        allow_isolation_release=True,
        notes="Operating under shadow model; stay in guarded reentry "
              "until enough stable turns are observed.",
        metadata={
            "prefer_shadow_model": spec.hints.get("prefer_shadow_model", True),
            "shadow_model_tier": spec.hints.get("shadow_model_tier", "conservative"),
            "min_stable_turns": min_stable_turns,
            "cycles_completed": state.cycles_completed,
        },
    )


def _plan_for_fallback_tool(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    FALLBACK_TOOL_ONLY → tool-first operation with soft reentry.

    Reentry plan:
        - keep PLDState
        - require tool-success-based stability before re-enabling full generation
    """
    return ReconciliationPlan(
        reentry_mode=ReentryMode.SOFT_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes=(
            "Tool-only fallback active; allow re-enabling free-form generation "
            "after tools have produced stable results."
        ),
        metadata={
            "tool_first_policy": spec.hints.get("tool_first_policy", True),
            "disable_freeform_generation": spec.hints.get(
                "disable_freeform_generation", True
            ),
            "min_tool_success_turns": 2,
            "phase": state.phase,
        },
    )


def _plan_for_human_handoff(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    HUMAN_HANDOFF → reentry depends on human operator.

    By default we require explicit human release before returning
    to autonomous operation.
    """
    return ReconciliationPlan(
        reentry_mode=ReentryMode.GUARDED_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,
        allow_isolation_release=True,
        notes="Human handoff in effect; reentry requires human release/approval.",
        metadata={
            "require_human_release": True,
            "expose_session_trace": spec.hints.get("expose_session_trace", True),
            "notify_human_channel": spec.hints.get("notify_human_channel", True),
            "phase": state.phase,
        },
    )


def _plan_for_isolate_and_audit(
    state: PLDState,
    decision: FailoverDecision,
    spec: StrategySpec,
) -> ReconciliationPlan:
    """
    ISOLATE_AND_AUDIT → no automatic reentry.

    The system should remain in isolation until an external audit or
    manual override is performed.
    """
    return ReconciliationPlan(
        reentry_mode=ReentryMode.NONE,
        reset_pld_state=False,  # decision to reset is up to auditors
        keep_session_history=True,
        relax_degradation=False,
        allow_isolation_release=False,
        notes=(
            "Session isolated for audit; no automatic reentry allowed. "
            "Manual review and explicit release are required."
        ),
        metadata={
            "lock_session": spec.hints.get("lock_session", True),
            "require_manual_release": spec.hints.get("require_manual_release", True),
            "mark_for_audit": spec.hints.get("mark_for_audit", True),
            "triggered_by": decision.triggered_by_codes,
        },
    )


__all__ = [
    "ReentryMode",
    "ReconciliationPlan",
    "plan_reconciliation",
]
