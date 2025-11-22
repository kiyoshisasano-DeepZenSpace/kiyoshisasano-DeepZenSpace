#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# version: 2.0.0
# status: draft (runtime template, experimental)
# authority: Level 5 — runtime implementation (consumes Levels 1–3)
# purpose: Normalizes PLD events according to semantic rules and validation modes.
# scope: Applies Level 2 semantic alignment post-schema validation; retains legacy role/turn normalization for compatibility.
# dependencies: Level 1 schema; Level 2 event matrix; Level 3 operational validation mode rules.
# change_classification: runtime-only, non-breaking (example/template modernization)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Literal, Union

# ---------------------------------------------------------------------------
# Shared neutral types (Core Technical Issue: inverted dependency resolved)
# ---------------------------------------------------------------------------
from ..types import NormalizedTurn, Role  # NOTE: Migration target for shared runtime models


# ---------------------------------------------------------------------------
# Semantic normalization constants
# ---------------------------------------------------------------------------

VALID_PHASES: tuple[str, ...] = (
    "drift",
    "repair",
    "reentry",
    "continue",
    "outcome",
    "failover",
    "none",
)

PREFIX_TO_PHASE: Dict[str, str] = {
    "D": "drift",
    "R": "repair",
    "RE": "reentry",
    "C": "continue",
    "O": "outcome",
    "F": "failover",
}

MUST_PHASE_MAP: Dict[str, str] = {
    "drift_detected": "drift",
    "drift_escalated": "drift",
    "repair_triggered": "repair",
    "repair_escalated": "repair",
    "reentry_observed": "reentry",
    "continue_allowed": "continue",
    "continue_blocked": "continue",
    "failover_triggered": "failover",
}

SHOULD_PHASE_MAP: Dict[str, str] = {
    "evaluation_pass": "outcome",
    "evaluation_fail": "outcome",
    "session_closed": "outcome",
    "info": "none",
}

MAY_EVENTS: set[str] = {
    "latency_spike",
    "pause_detected",
    "fallback_executed",
    "handoff",
}


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def extract_prefix(code: str) -> Optional[str]:
    """Extract lifecycle/non-lifecycle prefix from pld.code."""
    if not code:
        return None
    head = code.split("_", 1)[0]
    i = len(head)
    while i > 0 and head[i - 1].isdigit():
        i -= 1
    return (head[:i] or head) or None


# ---------------------------------------------------------------------------
# Issue and normalization result dataclasses
# ---------------------------------------------------------------------------

@dataclass
class NormalizationIssue:
    code: str
    message: str
    severity: Literal["info", "warning", "error"]
    path: str
    fixed: bool = False


@dataclass
class NormalizationResult:
    event: Dict[str, Any]
    issues: List[NormalizationIssue]
    accepted: bool

    @property
    def has_errors(self) -> bool:
        return any(i.severity == "error" and not i.fixed for i in self.issues)


# ---------------------------------------------------------------------------
# Core semantic normalizer
# ---------------------------------------------------------------------------

def normalize_event(
    event: Dict[str, Any],
    mode: Literal["strict", "warn", "normalize"] = "normalize",
) -> NormalizationResult:
    """
    Normalize PLD event semantics based on Level 2 and Level 3 rules.

    # NOTE: Migration difference from older ingestion normalization logic.
    """
    if mode not in ("strict", "warn", "normalize"):
        raise ValueError(f"Unsupported validation mode: {mode!r}")

    normalized = dict(event)
    issues: List[NormalizationIssue] = []

    pld = normalized.get("pld") or {}
    event_type = normalized.get("event_type")
    phase = pld.get("phase")
    code = pld.get("code")

    if event_type is None or phase is None or code is None:
        issues.append(
            NormalizationIssue(
                code="SEMANTIC_MISSING_FIELDS",
                message="event_type, pld.phase, and pld.code required.",
                severity="error",
                path=".",
            )
        )
        return NormalizationResult(normalized, issues, False)

    must_phase = MUST_PHASE_MAP.get(event_type)
    if must_phase and phase != must_phase:
        issue = NormalizationIssue(
            code="SEMANTIC_PHASE_MISMATCH_MUST",
            message=f"event_type={event_type!r} requires phase={must_phase!r}, found={phase!r}",
            severity="error",
            path="pld.phase",
        )
        if mode == "normalize":
            pld = dict(pld)
            pld["phase"] = must_phase
            normalized["pld"] = pld
            issue.fixed = True
            issue.severity = "warning"
            phase = must_phase
        issues.append(issue)

    should_phase = SHOULD_PHASE_MAP.get(event_type)
    if should_phase and phase != should_phase:
        issues.append(
            NormalizationIssue(
                code="SEMANTIC_PHASE_MISMATCH_SHOULD",
                message=f"event_type={event_type!r} expected phase={should_phase!r}, found={phase!r}",
                severity="warning",
                path="pld.phase",
            )
        )

    prefix = extract_prefix(code)
    if prefix in PREFIX_TO_PHASE and phase != PREFIX_TO_PHASE[prefix]:
        issue = NormalizationIssue(
            code="SEMANTIC_PREFIX_PHASE_MISMATCH",
            message=f"prefix={prefix!r} implies {PREFIX_TO_PHASE[prefix]!r}, found={phase!r}",
            severity="error",
            path="pld.phase",
        )
        if mode == "normalize":
            if not must_phase or must_phase == PREFIX_TO_PHASE[prefix]:
                pld = dict(pld)
                pld["phase"] = PREFIX_TO_PHASE[prefix]
                normalized["pld"] = pld
                issue.fixed = True
                issue.severity = "warning"
        issues.append(issue)

    accepted = not any(i.severity == "error" and not i.fixed for i in issues)
    return NormalizationResult(normalized, issues, accepted)


# ---------------------------------------------------------------------------
# Legacy (deprecated) NormalizedTurn helpers
# ---------------------------------------------------------------------------

_CANONICAL_ROLES = {
    "user": "user",
    "human": "user",
    "customer": "user",
    "client": "user",
    "assistant": "assistant",
    "ai": "assistant",
    "bot": "assistant",
    "agent": "assistant",
    "system": "system",
    "orchestrator": "system",
    "router": "system",
}

# TODO: Clarify role normalization fidelity:
#       orchestrator/router currently collapsed into 'system'.
#       Assess impact on PLD analysis and debugging of control-plane issues.
def normalize_role(raw_role: str) -> Role:
    key = (raw_role or "").strip().lower()
    return _CANONICAL_ROLES.get(key, "user")  # type: ignore[return-value]


def make_turn(
    *,
    session_id: str,
    turn_id: str,
    role: Union[str, Role],
    text: str,
    runtime: Optional[Dict[str, Any]] = None,
) -> NormalizedTurn:
    canonical_role = normalize_role(role) if isinstance(role, str) else role
    return NormalizedTurn(
        session_id=str(session_id),
        turn_id=str(turn_id),
        role=canonical_role,
        text=str(text or ""),
        runtime=dict(runtime or {}),
    )


def from_chat_message(
    *,
    session_id: str,
    msg_id: str,
    role: Union[str, Role],
    content: str,
    latency_ms: Optional[int] = None,
    source: Optional[str] = None,
    expected_format: Optional[str] = None,
    extra_runtime: Optional[Dict[str, Any]] = None,
) -> NormalizedTurn:
    runtime: Dict[str, Any] = {}
    if latency_ms is not None:
        runtime["latency_ms"] = int(latency_ms)
    if source is not None:
        runtime["source"] = str(source)
    if expected_format is not None:
        runtime["expected_format"] = str(expected_format)
    if extra_runtime:
        runtime.update(extra_runtime)

    return make_turn(
        session_id=session_id,
        turn_id=msg_id,
        role=role,
        text=content,
        runtime=runtime,
    )


def from_tool_call(
    *,
    session_id: str,
    call_id: str,
    tool_name: str,
    request_repr: str,
    response_repr: str,
    latency_ms: Optional[int] = None,
    role: Union[str, Role] = "assistant",
    success: Optional[bool] = None,
    extra_runtime: Optional[Dict[str, Any]] = None,
) -> NormalizedTurn:
    text = "\n".join([
        f"[TOOL_CALL] name={tool_name}",
        f"[REQUEST] {request_repr}",
        f"[RESPONSE] {response_repr}",
    ])

    runtime: Dict[str, Any] = {
        "tool_used": tool_name,
        "latency_ms": latency_ms,
        "tool_success": success,
    }
    runtime = {k: v for k, v in runtime.items() if v is not None}
    if extra_runtime:
        runtime.update(extra_runtime)

    return make_turn(
        session_id=session_id,
        turn_id=call_id,
        role=role,
        text=text,
        runtime=runtime,
    )


def from_system_event(
    *,
    session_id: str,
    event_id: str,
    description: str,
    reason: Optional[str] = None,
    reset_flag: bool = False,
    extra_runtime: Optional[Dict[str, Any]] = None,
) -> NormalizedTurn:
    text = f"[SYSTEM] {description}"
    if reason:
        text += f" (reason: {reason})"

    runtime: Dict[str, Any] = {"reset_flag": bool(reset_flag)}
    if extra_runtime:
        runtime.update(extra_runtime)

    return make_turn(
        session_id=session_id,
        turn_id=event_id,
        role="system",
        text=text,
        runtime=runtime,
    )


def from_dialog_turn_dict(
    *,
    dialog: Dict[str, Any],
    turn: Dict[str, Any],
    session_key: str = "dialog_id",
    turn_key: str = "turn_id",
    role_key: str = "role",
    text_key: str = "text",
    runtime_prefix: str = "runtime_",
) -> NormalizedTurn:
    session_id = str(dialog.get(session_key, "unknown"))
    turn_id = str(turn.get(turn_key, "0"))
    role = str(turn.get(role_key, "user"))
    text = str(turn.get(text_key, ""))

    runtime: Dict[str, Any] = {
        k[len(runtime_prefix):]: v
        for k, v in turn.items()
        if k.startswith(runtime_prefix)
    }

    return make_turn(
        session_id=session_id,
        turn_id=turn_id,
        role=role,
        text=text,
        runtime=runtime,
    )


# ---------------------------------------------------------------------------
# Public exports
# ---------------------------------------------------------------------------

__all__ = [
    "NormalizationIssue",
    "NormalizationResult",
    "normalize_event",
    "normalize_role",
    "make_turn",
    "from_chat_message",
    "from_tool_call",
    "from_system_event",
    "from_dialog_turn_dict",
]


# ---------------------------------------------------------------------------
# Deferred for later phase
# ---------------------------------------------------------------------------
"""
Future-Stage Considerations:

- Whether pld.code prefix should overwrite SHOULD-based phase mismatches
  in normalize mode when the MUST map is also absent.
- Whether normalization should rewrite or generate codes when invalid.
- Role mapping fidelity question: system/orchestrator/router distinctions.
- Architecture refactor separating presentation roles from PLD-event semantics.
"""

