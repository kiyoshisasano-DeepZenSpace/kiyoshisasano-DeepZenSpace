#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.ingestion.normalization

Normalization utilities for converting heterogeneous runtime inputs into
`NormalizedTurn` objects.

Concept
-------
Different platforms (chat UIs, APIs, orchestration frameworks, datasets)
have their own message / event formats. PLD Runtime expects a single
neutral shape:

    NormalizedTurn(session_id, turn_id, role, text, runtime)

This module centralizes that mapping logic.

Procedure
---------
1. Map raw roles (e.g., "assistant", "ai", "bot") to canonical roles:
       "user" | "assistant" | "system"
2. Extract or synthesize:
       - session_id
       - turn_id
       - text content
3. Build a `runtime` dict with optional metadata, e.g.:
       latency_ms, tool_used, expected_format, reset_flag, source

Implementation
--------------
The functions here perform *pure data normalization*:
- no I/O
- no validation
- no policy or PLD logic

Validation
----------
These functions are designed to be stable across platforms.
Callers should add their own unit tests for each log/source format
they integrate.

Next Step
---------
Ingestion adapters (e.g., openai_assistants_adapter.py, multiwoz_loader.py)
should use this module as the authoritative way to construct NormalizedTurn.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Literal, Union

from ..detection.runtime_signal_bridge import NormalizedTurn, Role


# ---------------------------------------------------------------------------
# Role normalization
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


def normalize_role(raw_role: str) -> Role:
    """
    Map various raw role strings into canonical Role:

        "user" | "assistant" | "system"

    Unrecognized roles default to "user", which is safer than
    mislabeling as assistant/system.
    """
    key = (raw_role or "").strip().lower()
    mapped = _CANONICAL_ROLES.get(key, "user")
    return mapped  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Generic constructors
# ---------------------------------------------------------------------------

def make_turn(
    *,
    session_id: str,
    turn_id: str,
    role: Union[str, Role],
    text: str,
    runtime: Optional[Dict[str, Any]] = None,
) -> NormalizedTurn:
    """
    Construct a NormalizedTurn from already-resolved fields.

    This is the lowest-level helper; most callers should use one of the
    higher-level factory functions below.
    """
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
    """
    Normalize a simple chat message (typical chat API or UI log)
    into a NormalizedTurn.

    Parameters
    ----------
    session_id:
        Conversation/session identifier.

    msg_id:
        Message identifier, used as turn_id.

    role:
        Free-form role string or Role literal.

    content:
        Text content of the message.

    latency_ms:
        Optional latency in ms for generating this message.

    source:
        Optional source label (e.g., "web_ui", "assistants_api").

    expected_format:
        Optional content format hint ("json", "markdown", etc).

    extra_runtime:
        Optional dict merged into runtime metadata.
    """
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
    """
    Normalize a tool call into a NormalizedTurn.

    Typical usage:
        - treat tool outputs as assistant-side turns for drift detection
        - include request/response in `text` for downstream detectors

    The resulting `text` embeds a lightweight textual summary of
    request and response to keep detectors context-aware without
    committing to a strict schema.
    """
    text_parts = [
        f"[TOOL_CALL] name={tool_name}",
        f"[REQUEST] {request_repr}",
        f"[RESPONSE] {response_repr}",
    ]
    text = "\n".join(text_parts)

    runtime: Dict[str, Any] = {
        "tool_used": tool_name,
        "latency_ms": latency_ms,
        "tool_success": success,
    }
    # remove None values to keep runtime compact
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
    """
    Normalize a system-level event (e.g., reset, handoff, routing decision)
    into a NormalizedTurn with role="system".

    This is primarily useful for:

        - marking context resets
        - annotating significant routing changes
        - signaling guardrail / moderation interventions
    """
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


# ---------------------------------------------------------------------------
# Dataset-like generic normalization
# ---------------------------------------------------------------------------

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
    """
    Generic helper to normalize dataset-style dialog+turn dicts.

    Assumes a structure like:

        dialog = {
          "dialog_id": "...",
          ...
        }
        turn = {
          "turn_id": "utt-3",
          "role": "user",
          "text": "hello",
          "runtime_latency_ms": 123,
          "runtime_source": "simulator",
          ...
        }

    All keys of `turn` whose name starts with `runtime_prefix`
    are added to the runtime dict with the prefix stripped.

    This is intentionally generic to support MultiWOZ-like
    datasets and custom corpora.
    """
    session_id = str(dialog.get(session_key, "unknown"))
    turn_id = str(turn.get(turn_key, "0"))
    role = str(turn.get(role_key, "user"))
    text = str(turn.get(text_key, ""))

    runtime: Dict[str, Any] = {}
    for k, v in turn.items():
        if not k.startswith(runtime_prefix):
            continue
        runtime_key = k[len(runtime_prefix) :]
        runtime[runtime_key] = v

    return make_turn(
        session_id=session_id,
        turn_id=turn_id,
        role=role,
        text=text,
        runtime=runtime,
    )


__all__ = [
    "normalize_role",
    "make_turn",
    "from_chat_message",
    "from_tool_call",
    "from_system_event",
    "from_dialog_turn_dict",
]
