#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.ingestion.multiwoz_loader

Concept
-------
Adapter for loading MultiWOZ-style dialogs and converting them into
`NormalizedTurn` sequences suitable for PLD runtime.

This module is intentionally tolerant of slight format variants:

- Canonical MultiWOZ 2.x (top-level mapping: dialog_id → {goal, log})
- "Dialog list" style:
    [
      {
        "dialogue_id": "...",
        "turns": [
          {"speaker": "USER", "utterance": "..."},
          {"speaker": "SYSTEM", "utterance": "..."},
          ...
        ]
      },
      ...
    ]

The goal is not perfect coverage of every variant but a stable, usable
ingestion path for evaluation studies built on MultiWOZ-derived data.

Procedure
---------
1. Load JSON file(s) from a given path.
2. Detect whether the top-level structure is:
      - mapping: {dialog_id: dialog_obj}
      - list: [dialog_obj, ...]
3. For each dialog:
      - derive `session_id` from `dialogue_id` / dict key / filename
      - normalize turns into `NormalizedTurn` objects
      - map dataset speakers → canonical roles:
            USER/USR → user
            SYSTEM/SYS → assistant
4. Yield (session_id, [NormalizedTurn, ...]) pairs.

Implementation
--------------
All I/O is local file-based JSON.
No network calls.
No schema enforcement here (that happens later via PLD runtime).

Validation
----------
Callers are expected to:

- run small smoke tests on corpus subsets
- verify that the number of turns and basic alternation look correct
- optionally compare against original MultiWOZ scripts, if needed.

Next Step
---------
`metrics_studies/*` modules can consume `iter_multiwoz_corpus()` and feed
resulting `NormalizedTurn` streams into controllers and evaluation
pipelines.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union

from .normalization import make_turn, normalize_role
from ..detection.runtime_signal_bridge import NormalizedTurn, Role


PathLike = Union[str, Path]


# ---------------------------------------------------------------------------
# Speaker → Role mapping
# ---------------------------------------------------------------------------

_DEFAULT_SPEAKER_MAP: Dict[str, Role] = {
    "user": "user",
    "usr": "user",
    "customer": "user",
    "client": "user",
    "visitor": "user",

    "system": "assistant",
    "sys": "assistant",
    "agent": "assistant",
    "operator": "assistant",
    "bot": "assistant",
}


def _speaker_to_role(raw: str) -> Role:
    key = (raw or "").strip().lower()
    return _DEFAULT_SPEAKER_MAP.get(key, normalize_role(key))


# ---------------------------------------------------------------------------
# Core dialog normalization
# ---------------------------------------------------------------------------

def load_multiwoz_dialog(
    dialog: Mapping[str, Any],
    *,
    session_id: Optional[str] = None,
) -> List[NormalizedTurn]:
    """
    Convert a single MultiWOZ-style dialog dict into a list of NormalizedTurn.

    This function attempts to support two main shapes:

    1) Canonical MultiWOZ 2.x:

        {
          "goal": {...},
          "log": [
            {"text": "hello", "metadata": {...}},
            {"text": "hi, how can I help?", "metadata": {...}},
            ...
          ]
        }

       dialog_id is expected to be provided externally (e.g., map key).

    2) Dialog-list style:

        {
          "dialogue_id": "MUL1234",
          "turns": [
            {"speaker": "USER", "utterance": "hello"},
            {"speaker": "SYSTEM", "utterance": "hi, how can I help?"},
            ...
          ]
        }

    Parameters
    ----------
    dialog:
        Single dialog object.

    session_id:
        If given, used as session identifier. Otherwise, attempts:

            dialog["dialogue_id"] or dialog["dialog_id"]

        and falls back to "unknown".

    Returns
    -------
    List[NormalizedTurn]
    """
    sid = (
        session_id
        or str(dialog.get("dialogue_id") or dialog.get("dialog_id") or "unknown")
    )

    # Case 1: "turns" format
    if "turns" in dialog and isinstance(dialog["turns"], list):
        return _turns_style_to_normalized(sid, dialog["turns"])

    # Case 2: canonical MultiWOZ "log" format
    if "log" in dialog and isinstance(dialog["log"], list):
        return _log_style_to_normalized(sid, dialog["log"])

    # Fallback: try generic "utterances" or bail out as empty
    if "utterances" in dialog and isinstance(dialog["utterances"], list):
        return _turns_style_to_normalized(sid, dialog["utterances"])

    # Unknown layout; return empty list so caller can log/inspect separately.
    return []


def _turns_style_to_normalized(
    session_id: str,
    turns: List[Mapping[str, Any]],
) -> List[NormalizedTurn]:
    """
    Map list-style turns (with speaker+utterance/text) to NormalizedTurn.
    """
    result: List[NormalizedTurn] = []

    for idx, t in enumerate(turns):
        speaker_raw = str(t.get("speaker") or t.get("role") or "user")
        utterance = str(t.get("utterance") or t.get("text") or "")
        role = _speaker_to_role(speaker_raw)

        turn_id = str(t.get("turn_id") or idx)

        runtime: Dict[str, Any] = {}
        # Preserve any extra keys into runtime_ namespace as a conservative choice.
        for k, v in t.items():
            if k in {"speaker", "role", "utterance", "text", "turn_id"}:
                continue
            runtime[f"src_{k}"] = v

        turn = make_turn(
            session_id=session_id,
            turn_id=turn_id,
            role=role,
            text=utterance,
            runtime=runtime,
        )
        result.append(turn)

    return result


def _log_style_to_normalized(
    session_id: str,
    log: List[Mapping[str, Any]],
) -> List[NormalizedTurn]:
    """
    Map canonical MultiWOZ "log" style to NormalizedTurn.

    MultiWOZ logs are typically alternating USER/SYSTEM turns, but
    speaker labels may not be explicit; we infer based on index:

        index 0, 2, 4, ... → user
        index 1, 3, 5, ... → assistant

    If 'speaker' or 'role' is present, that mapping is preferred.
    """
    result: List[NormalizedTurn] = []

    for idx, t in enumerate(log):
        # Prefer explicit speaker/role
        if "speaker" in t or "role" in t:
            speaker_raw = str(t.get("speaker") or t.get("role") or "user")
            role = _speaker_to_role(speaker_raw)
        else:
            # Fallback: alternate user/assistant by index
            role = "user" if idx % 2 == 0 else "assistant"

        text = str(t.get("text") or "")
        turn_id = str(t.get("turn_id") or idx)

        runtime: Dict[str, Any] = {}
        # Common MultiWOZ keys: "metadata", "span_info", ...
        for k in ("metadata", "span_info", "dialog_act"):
            if k in t:
                runtime[f"src_{k}"] = t[k]

        turn = make_turn(
            session_id=session_id,
            turn_id=turn_id,
            role=role,
            text=text,
            runtime=runtime,
        )
        result.append(turn)

    return result


# ---------------------------------------------------------------------------
# Corpus-level helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def iter_multiwoz_file(path: PathLike) -> Iterator[Tuple[str, List[NormalizedTurn]]]:
    """
    Iterate over dialogs contained in a single MultiWOZ-style JSON file.

    The file may contain either:

    1) Mapping: { dialog_id: dialog_obj, ... }
    2) List: [ dialog_obj, ... ]

    Yields
    ------
    (session_id, [NormalizedTurn, ...])
    """
    p = Path(path)
    data = _load_json(p)

    # Mapping: {dialog_id: dialog_obj}
    if isinstance(data, dict):
        for dialog_id, dialog_obj in data.items():
            if not isinstance(dialog_obj, Mapping):
                continue
            turns = load_multiwoz_dialog(dialog_obj, session_id=str(dialog_id))
            yield str(dialog_id), turns
        return

    # List: [dialog_obj, ...]
    if isinstance(data, list):
        for dialog_obj in data:
            if not isinstance(dialog_obj, Mapping):
                continue
            session_id = str(
                dialog_obj.get("dialogue_id")
                or dialog_obj.get("dialog_id")
                or p.stem
            )
            turns = load_multiwoz_dialog(dialog_obj, session_id=session_id)
            yield session_id, turns
        return

    # Unknown structure: yield nothing
    return


def iter_multiwoz_corpus(path: PathLike) -> Iterator[Tuple[str, List[NormalizedTurn]]]:
    """
    Iterate over all dialogs from a MultiWOZ-style corpus path.

    If `path` is:

    - a file: delegates to iter_multiwoz_file.
    - a directory: recursively searches for *.json and yields dialogs
      from each file.

    Yield order is not guaranteed but is deterministic for a given
    filesystem layout.
    """
    p = Path(path)
    if p.is_file():
        yield from iter_multiwoz_file(p)
        return

    if p.is_dir():
        for json_file in sorted(p.rglob("*.json")):
            yield from iter_multiwoz_file(json_file)
        return

    # Neither file nor directory: nothing to yield
    return


__all__ = [
    "load_multiwoz_dialog",
    "iter_multiwoz_file",
    "iter_multiwoz_corpus",
]
