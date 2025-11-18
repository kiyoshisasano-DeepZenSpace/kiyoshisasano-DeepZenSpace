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
# Internal helpers
# ---------------------------------------------------------------------------


def _strategy_hints(spec: Optional[StrategySpec]) -> Dict[str, Any]:
    """
    Safely extract a hints dict from StrategySpec.

    This keeps reconciliation robust even if the registry returns None
    or a spec without .hints.
    """
    if spec is None:
        return {}
    hints = getattr(spec, "hints", None)
    if hints is None:
        return {}
    if not isinstance(hints, dict):
        return {}
    return hints


def _triggered_by(decision: FailoverDecision) -> Any:
    """
    Safely extract a list (or other payload) describing which codes
    triggered this failover decision.
    """
    return getattr(decision, "triggered_by_codes", None)


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
    Missing specs degrade gracefully (assumed empty hints).
    """
    if spec is None:
        spec = get_strategy_spec(decision.strategy)

    strategy = decision.strategy

    if strategy == FailoverStrategy.NONE:
        return _plan_for_none(state, decision, spec)

    if strategy == FailoverStrategy.SOFT_DEGRADE:
        return _plan_for_soft_degrade(state, decision, spec)

    if strategy == FailoverStrategy.SAFE_RESET_SESSION:
        return _plan_for_safe_reset(state, decision, spec)

    if strategy == FailoverStrategy.SWITCH_MODEL_SHADOW:
        return _plan_for_switch_model(state, decision, spec)

    if strategy == FailoverStrategy.FALLBACK_TOOL_ONLY:
        return _plan_for_fallback_tool(state, decision, spec)

    if strategy == FailoverStrategy.HUMAN_HANDOFF:
        return _plan_for_human_handoff(state, decision, spec)

    if strategy == FailoverStrategy.ISOLATE_AND_AUDIT:
        return _plan_for_isolate_and_audit(state, decision, spec)

    # Fallback: conservative, no automatic reentry
    return ReconciliationPlan(
        reentry_mode=ReentryMode.NONE,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,
        allow_isolation_release=False,
        notes=f"Unknown strategy {getattr(strategy, 'value', strategy)}; "
        "reconciliation disabled.",
        metadata={
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": _triggered_by(decision),
        },
    )


# ---------------------------------------------------------------------------
# Strategy-specific planning helpers
# ---------------------------------------------------------------------------


def _plan_for_none(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    hints = _strategy_hints(spec)
    return ReconciliationPlan(
        reentry_mode=(
            ReentryMode.SOFT_REENTRY
            if state.phase in {"repair", "reentry"}
            else ReentryMode.GUARDED_REENTRY
        ),
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes="No failover strategy applied; allow normal reentry with mild monitoring.",
        metadata={
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": _triggered_by(decision),
            "hints": hints,
        },
    )


def _plan_for_soft_degrade(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    SOFT_DEGRADE → allow gradual return if system stabilizes.

    Heuristic:
        - keep PLDState
        - require a small number of stable turns before relaxing
    """
    hints = _strategy_hints(spec)
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
            "backoff_profile": hints.get("backoff_profile"),
            "triggered_by": _triggered_by(decision),
        },
    )


def _plan_for_safe_reset(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    SAFE_RESET_SESSION → require a fresh conversational context,
    but keep history for audit / debugging.
    """
    hints = _strategy_hints(spec)
    return ReconciliationPlan(
        reentry_mode=ReentryMode.FRESH_SESSION,
        reset_pld_state=True,
        keep_session_history=True,
        relax_degradation=True,
        allow_isolation_release=True,
        notes=(
            "Session should be restarted with fresh PLD state; "
            "previous history retained for audit."
        ),
        metadata={
            "require_user_ack": hints.get("require_user_ack", True),
            "allow_resume_with_new_session": hints.get(
                "allow_resume_with_new_session", True
            ),
            "triggered_by": _triggered_by(decision),
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
        },
    )


def _plan_for_switch_model(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    SWITCH_MODEL_SHADOW → reentry continues in a guarded mode
    under a more conservative model.

    PLDState is preserved, but we may require more stable cycles before
    relaxing back to the original model.
    """
    hints = _strategy_hints(spec)
    min_stable_turns = max(3, 5 - state.cycles_completed)

    return ReconciliationPlan(
        reentry_mode=ReentryMode.GUARDED_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,  # stay conservative for a while
        allow_isolation_release=True,
        notes=(
            "Operating under shadow model; stay in guarded reentry "
            "until enough stable turns are observed."
        ),
        metadata={
            "prefer_shadow_model": hints.get("prefer_shadow_model", True),
            "shadow_model_tier": hints.get("shadow_model_tier", "conservative"),
            "min_stable_turns": min_stable_turns,
            "cycles_completed": state.cycles_completed,
            "phase": state.phase,
            "triggered_by": _triggered_by(decision),
        },
    )


def _plan_for_fallback_tool(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    FALLBACK_TOOL_ONLY → tool-first operation with soft reentry.

    Reentry plan:
        - keep PLDState
        - require tool-success-based stability before re-enabling full generation
    """
    hints = _strategy_hints(spec)
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
            "tool_first_policy": hints.get("tool_first_policy", True),
            "disable_freeform_generation": hints.get(
                "disable_freeform_generation", True
            ),
            "min_tool_success_turns": 2,
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": _triggered_by(decision),
        },
    )


def _plan_for_human_handoff(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    HUMAN_HANDOFF → reentry depends on human operator.

    By default we require explicit human release before returning
    to autonomous operation.
    """
    hints = _strategy_hints(spec)
    return ReconciliationPlan(
        reentry_mode=ReentryMode.GUARDED_REENTRY,
        reset_pld_state=False,
        keep_session_history=True,
        relax_degradation=False,
        allow_isolation_release=True,
        notes="Human handoff in effect; reentry requires human release/approval.",
        metadata={
            "require_human_release": True,
            "expose_session_trace": hints.get("expose_session_trace", True),
            "notify_human_channel": hints.get("notify_human_channel", True),
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": _triggered_by(decision),
        },
    )


def _plan_for_isolate_and_audit(
    state: PLDState,
    decision: FailoverDecision,
    spec: Optional[StrategySpec],
) -> ReconciliationPlan:
    """
    ISOLATE_AND_AUDIT → no automatic reentry.

    The system should remain in isolation until an external audit or
    manual override is performed.
    """
    hints = _strategy_hints(spec)
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
            "lock_session": hints.get("lock_session", True),
            "require_manual_release": hints.get("require_manual_release", True),
            "mark_for_audit": hints.get("mark_for_audit", True),
            "phase": state.phase,
            "cycles_completed": state.cycles_completed,
            "triggered_by": _triggered_by(decision),
        },
    )


__all__ = [
    "ReentryMode",
    "ReconciliationPlan",
    "plan_reconciliation",
]
