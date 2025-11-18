#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.controllers.action_router (v1.1 Canonical Edition)

Translate policy decisions into abstract route instructions that a host
application can implement.

This module performs the mapping:

    PolicyEvaluation
        → List[RouteInstruction]

It does NOT:

- call tools or LLMs
- terminate sessions
- send notifications
- write logs or metrics

All concrete side effects MUST be implemented by the caller, based on the
RouteInstruction objects returned here.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List

from ..enforcement.response_policy import (
    PolicyEvaluation,
    PolicyDecision,
    PolicyAction,
    Severity,
)


# ---------------------------------------------------------------------------
# Route targets
# ---------------------------------------------------------------------------

class RouteTarget(str, Enum):
    """
    Abstract destinations for policy-driven actions.

    Semantics
    ---------
    LOG:
        Send to logging / telemetry sink only. No behavior change.

    AGENT_HINT:
        Provide a soft hint to the agent (e.g., adjust prompt, add guidance).
        This is typically aligned with soft repair strategies (R1/R2).

    AGENT_CONTROL:
        Trigger a stronger agent-side intervention
        (e.g., structured repair step, hard-reset flow).

    HUMAN_ESCALATION:
        Notify or hand off to a human operator / support channel.

    SESSION_CONTROL:
        Request session termination, reset, or hard recovery.

    METRICS_ONLY:
        Record for evaluation / dashboards only; no live feedback.
        Commonly used for PRDR / REI / VRL instrumentation.
    """

    LOG = "log"
    AGENT_HINT = "agent_hint"
    AGENT_CONTROL = "agent_control"
    HUMAN_ESCALATION = "human_escalation"
    SESSION_CONTROL = "session_control"
    METRICS_ONLY = "metrics_only"


# ---------------------------------------------------------------------------
# Route instruction
# ---------------------------------------------------------------------------

@dataclass
class RouteInstruction:
    """
    One abstract instruction derived from a single PolicyDecision.

    The host runtime is responsible for mapping each instruction
    to concrete behavior (e.g., logging, repair calls, escalations).
    """

    session_id: str
    action: PolicyAction
    severity: Severity
    target: RouteTarget
    code: str
    message: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this instruction as a plain dict, converting enums into
        their underlying string representations.
        """
        d = asdict(self)
        d["action"] = self.action.value
        d["severity"] = self.severity.value
        d["target"] = self.target.value
        return d


# ---------------------------------------------------------------------------
# Router configuration
# ---------------------------------------------------------------------------

@dataclass
class ActionRouterConfig:
    """
    Configuration for ActionRouter behavior.

    Attributes
    ----------
    emit_noop_metrics:
        If True, even NOOP decisions produce a METRICS_ONLY instruction
        so that silent policies are still observable.

    escalate_on_critical:
        If True, any CRITICAL severity also generates HUMAN_ESCALATION
        for decisions that already affect the session.

    agent_control_for_structural:
        If True, STRUCTURAL_REPAIR decisions are routed to AGENT_CONTROL.
        If False, they are treated as SESSION_CONTROL for higher severity.
    """

    emit_noop_metrics: bool = True
    escalate_on_critical: bool = True
    agent_control_for_structural: bool = True


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

class ActionRouter:
    """
    Map PolicyEvaluation → list of RouteInstruction.

    Typical usage
    -------------
        router = ActionRouter()
        routes = router.route(session_id="sess-123", policy_evaluation=pe)

        for r in routes:
            if r.target is RouteTarget.LOG:
                # send to logging system
            elif r.target is RouteTarget.AGENT_HINT:
                # adjust prompt or inject hint
            elif r.target is RouteTarget.AGENT_CONTROL:
                # trigger structured repair or control flow
            ...

    The router is intentionally deterministic and side-effect free.
    """

    def __init__(self, config: ActionRouterConfig | None = None) -> None:
        self.config = config or ActionRouterConfig()

    # ---- public API ----

    def route(
        self,
        *,
        session_id: str,
        policy_evaluation: PolicyEvaluation,
    ) -> List[RouteInstruction]:
        """
        Convert a PolicyEvaluation into a list of RouteInstruction objects.

        Parameters
        ----------
        session_id:
            Identifier for the current conversational session.

        policy_evaluation:
            Result from response_policy evaluation, containing
            policy decisions and metadata.

        Returns
        -------
        List[RouteInstruction]
            Route instructions that a host application can interpret and
            execute according to its environment.
        """
        instructions: List[RouteInstruction] = []

        for decision in policy_evaluation.decisions:
            # NOOP: optionally emit metrics-only route
            if decision.action == PolicyAction.NOOP:
                if self.config.emit_noop_metrics:
                    instructions.append(
                        self._build_instruction(
                            session_id=session_id,
                            decision=decision,
                            target=RouteTarget.METRICS_ONLY,
                        )
                    )
                continue

            # LOG_ONLY
            if decision.action == PolicyAction.LOG_ONLY:
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.LOG,
                    )
                )
                continue

            # SOFT_REPAIR → agent hint + log
            if decision.action == PolicyAction.SOFT_REPAIR:
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.AGENT_HINT,
                    )
                )
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.LOG,
                    )
                )
                continue

            # STRUCTURAL_REPAIR → agent_control or session_control + log
            if decision.action == PolicyAction.STRUCTURAL_REPAIR:
                main_target = (
                    RouteTarget.AGENT_CONTROL
                    if self.config.agent_control_for_structural
                    else RouteTarget.SESSION_CONTROL
                )
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=main_target,
                    )
                )
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.LOG,
                    )
                )
                continue

            # ESCALATE → human escalation + log
            if decision.action == PolicyAction.ESCALATE:
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.HUMAN_ESCALATION,
                    )
                )
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.LOG,
                    )
                )
                continue

            # ABORT_SESSION → session control + log (+ escalation if CRITICAL)
            if decision.action == PolicyAction.ABORT_SESSION:
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.SESSION_CONTROL,
                    )
                )
                instructions.append(
                    self._build_instruction(
                        session_id=session_id,
                        decision=decision,
                        target=RouteTarget.LOG,
                    )
                )
                if (
                    self.config.escalate_on_critical
                    and decision.severity == Severity.CRITICAL
                ):
                    instructions.append(
                        self._build_instruction(
                            session_id=session_id,
                            decision=decision,
                            target=RouteTarget.HUMAN_ESCALATION,
                        )
                    )
                continue

        return instructions

    # ---- internals ----

    def _build_instruction(
        self,
        *,
        session_id: str,
        decision: PolicyDecision,
        target: RouteTarget,
    ) -> RouteInstruction:
        """
        Build a RouteInstruction from a PolicyDecision and a target.

        The original decision details are carried forward into metadata,
        preserving policy context for logging and downstream systems.
        """
        metadata = dict(decision.details)
        metadata.setdefault("policy_code", decision.code)
        metadata.setdefault("policy_message", decision.message)

        return RouteInstruction(
            session_id=session_id,
            action=decision.action,
            severity=decision.severity,
            target=target,
            code=decision.code,
            message=decision.message,
            metadata=metadata,
        )


__all__ = [
    "RouteTarget",
    "RouteInstruction",
    "ActionRouterConfig",
    "ActionRouter",
]
