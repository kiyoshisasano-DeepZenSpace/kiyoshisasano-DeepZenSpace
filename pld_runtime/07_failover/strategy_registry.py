#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.failover.strategy_registry

Concept
-------
Canonical registry of *named failover strategies* for PLD Runtime.

This module does NOT perform any actions by itself.
Instead, it provides:

    FailoverStrategy  →  StrategySpec (what this is supposed to do)

Host systems (or higher-level orchestration) can then interpret these
specs and map them to:

    - concrete tool calls
    - model switches
    - session resets
    - human escalation workflows

Relationship to other modules
-----------------------------
- runtime_failover.decide_failover(...) chooses a FailoverStrategy.
- strategy_registry stores metadata and intent for each strategy.
- backoff_policies (future) may refer to StrategySpec.hints["backoff_profile"].

This keeps the *semantics* of each strategy centralized and documented.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

from .runtime_failover import FailoverStrategy
from ..controllers.action_router import RouteTarget


# ---------------------------------------------------------------------------
# Strategy specification model
# ---------------------------------------------------------------------------

@dataclass
class StrategySpec:
    """
    Descriptive specification for a failover strategy.

    Fields
    ------
    id:
        FailoverStrategy enum value.

    label:
        Short human-readable label.

    description:
        Longer explanation of the intent and typical behavior.

    default_route_target:
        Suggested RouteTarget to use when applying this strategy.

    hard_reset:
        Whether this strategy *typically* implies losing conversation
        state (session reset, context discard). This should agree with
        FailoverDecision.hard_reset in most cases.

    hints:
        Free-form structured hints for host runtimes, such as:

            {
              "prefer_shadow_model": True,
              "backoff_profile": "exponential_medium",
              "limit_tools": ["search", "db_lookup"],
              "max_retries": 2,
            }

        These hints are not enforced here—they are advisory.
    """

    id: FailoverStrategy
    label: str
    description: str
    default_route_target: Optional[RouteTarget]
    hard_reset: bool
    hints: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["id"] = self.id.value
        d["default_route_target"] = (
            self.default_route_target.value if self.default_route_target else None
        )
        return d


# ---------------------------------------------------------------------------
# Canonical registry
# ---------------------------------------------------------------------------

# NOTE:
# These specs are intentionally conservative and generic.
# Host systems can extend/override them in their own registries.

_STRATEGY_REGISTRY: Dict[FailoverStrategy, StrategySpec] = {
    FailoverStrategy.NONE: StrategySpec(
        id=FailoverStrategy.NONE,
        label="No failover",
        description="No special mitigation; proceed with normal behavior.",
        default_route_target=None,
        hard_reset=False,
        hints={"backoff_profile": "none"},
    ),

    FailoverStrategy.SOFT_DEGRADE: StrategySpec(
        id=FailoverStrategy.SOFT_DEGRADE,
        label="Soft degrade",
        description=(
            "Reduce capability surface without resetting the session. "
            "Examples: shorter answers, fewer tools, more guardrails."
        ),
        default_route_target=RouteTarget.AGENT_HINT,
        hard_reset=False,
        hints={
            "backoff_profile": "light",
            "limit_max_tokens": True,
            "limit_tools": True,
            "increase_safety_checks": True,
        },
    ),

    FailoverStrategy.SAFE_RESET_SESSION: StrategySpec(
        id=FailoverStrategy.SAFE_RESET_SESSION,
        label="Safe session reset",
        description=(
            "Politely reset the session or context while keeping the same "
            "model/tool stack. Intended for local corruption or unrecoverable "
            "context drift."
        ),
        default_route_target=RouteTarget.SESSION_CONTROL,
        hard_reset=True,
        hints={
            "backoff_profile": "medium",
            "require_user_ack": True,
            "allow_resume_with_new_session": True,
        },
    ),

    FailoverStrategy.SWITCH_MODEL_SHADOW: StrategySpec(
        id=FailoverStrategy.SWITCH_MODEL_SHADOW,
        label="Switch to shadow model",
        description=(
            "Switch to a more conservative or shadow model for subsequent "
            "turns, while preserving session where possible."
        ),
        default_route_target=RouteTarget.AGENT_CONTROL,
        hard_reset=False,
        hints={
            "prefer_shadow_model": True,
            "shadow_model_tier": "conservative",
            "backoff_profile": "medium",
        },
    ),

    FailoverStrategy.FALLBACK_TOOL_ONLY: StrategySpec(
        id=FailoverStrategy.FALLBACK_TOOL_ONLY,
        label="Tool-only fallback",
        description=(
            "Favor tool-based answers over free-form generation. "
            "Used when hallucination risk is high but tools are reliable."
        ),
        default_route_target=RouteTarget.AGENT_CONTROL,
        hard_reset=False,
        hints={
            "disable_freeform_generation": True,
            "tool_first_policy": True,
            "backoff_profile": "light",
        },
    ),

    FailoverStrategy.HUMAN_HANDOFF: StrategySpec(
        id=FailoverStrategy.HUMAN_HANDOFF,
        label="Human handoff",
        description=(
            "Escalate to a human operator or support channel. "
            "Agent should stop making strong claims and instead assist the "
            "handoff process."
        ),
        default_route_target=RouteTarget.HUMAN_ESCALATION,
        hard_reset=False,
        hints={
            "notify_human_channel": True,
            "expose_session_trace": True,
            "backoff_profile": "none",
        },
    ),

    FailoverStrategy.ISOLATE_AND_AUDIT: StrategySpec(
        id=FailoverStrategy.ISOLATE_AND_AUDIT,
        label="Isolate & audit",
        description=(
            "Stop interaction and mark the session for offline review. "
            "Designed for severe or suspicious behavior where continued "
            "interaction could be harmful."
        ),
        default_route_target=RouteTarget.SESSION_CONTROL,
        hard_reset=True,
        hints={
            "lock_session": True,
            "require_manual_release": True,
            "backoff_profile": "heavy",
            "mark_for_audit": True,
        },
    ),
}


# ---------------------------------------------------------------------------
# Public accessors
# ---------------------------------------------------------------------------

def get_strategy_spec(strategy: FailoverStrategy) -> StrategySpec:
    """
    Retrieve StrategySpec for a given FailoverStrategy.

    If the strategy is unknown (should not happen with current enum),
    a generic placeholder spec is returned.
    """
    spec = _STRATEGY_REGISTRY.get(strategy)
    if spec is not None:
        return spec

    # Fallback: generic placeholder
    return StrategySpec(
        id=strategy,
        label=f"Unknown strategy: {strategy.value}",
        description="No registered strategy spec; behavior is undefined.",
        default_route_target=None,
        hard_reset=False,
        hints={},
    )


def list_strategies() -> List[StrategySpec]:
    """
    Return all registered StrategySpec objects as a list.
    """
    return list(_STRATEGY_REGISTRY.values())


__all__ = [
    "StrategySpec",
    "get_strategy_spec",
    "list_strategies",
]
