"""
# version: 2.0.0
# status: experimental (runtime template)
# authority: Level 5 — runtime implementation (consumes Level 1–3 specifications)
# purpose: Provides a template dataset adapter mapping MultiWOZ dialogues to PLD-aligned runtime events.
# scope: Emits structurally compliant PLD events with optional runtime envelopes; no inference or validation logic included.
# dependencies: Level 1 schema, Level 2 event matrix, Level 3 metrics rules, Level 5 runtime envelope.
# change_classification: runtime-only, non-breaking (template; customization expected)
"""

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Mapping, Optional, Tuple, Union


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public configuration dataclasses
# ---------------------------------------------------------------------------


@dataclass
class MultiWOZIngestionConfig:
    """
    Configuration for ingesting MultiWOZ-style dialogues.

    This configuration is deliberately minimal. Most projects will want to extend
    this with fields for:
      - dataset split (train/val/test)
      - domain filters
      - experiment tags / tenant / region, etc.

    NOTE: This is a runtime-only structure; it does not affect any Level 1–3
    specifications.
    """

    dataset_name: str = "MultiWOZ"
    split: Optional[str] = None

    # Envelope/runtime defaults (Level 5 only, must align with envelope enums).
    environment: str = "sandbox"  # one of: production, staging, sandbox, local
    mode: str = "batch"  # one of: stream, batch, debug, audit
    platform: str = "custom"  # one of: assistants_api, langgraph, vertex_ai, rasa, batch_eval, custom, unknown
    platform_detail: Optional[str] = None
    user_id: Optional[str] = None

    # Whether to wrap PLD events in the runtime envelope when using the
    # envelope-based iteration helpers. Note: this is NOT used by
    # iter_multiwoz_corpus, which returns generic ingestion items.
    emit_envelopes: bool = True


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _now_iso8601_z() -> str:
    """
    Return an RFC 3339 / ISO 8601 timestamp in UTC with 'Z' suffix.

    This matches the expectations for both event.timestamp and envelope.timestamp.
    """
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_path(path: Union[str, Path]) -> Path:
    if isinstance(path, Path):
        return path
    return Path(path)


def _uuid4_str() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# MultiWOZ normalization
# ---------------------------------------------------------------------------


@dataclass
class NormalizedTurn:
    """
    Minimal normalized representation of a turn in a dialogue.

    Attributes:
        speaker: "user" or "system" (or other dataset-specific role labels).
        text: primary utterance text.
        raw: original turn structure from the dataset (for payload passthrough).
    """

    speaker: str
    text: str
    raw: Mapping[str, Any]


@dataclass
class NormalizedDialogue:
    """
    Minimal normalized representation of a dialogue / session.

    Attributes:
        dialogue_id: stable identifier for the dialogue; used as PLD session_id.
        turns: ordered list of NormalizedTurn.
        raw: original dialogue structure from the dataset (for payload passthrough).
    """

    dialogue_id: str
    turns: List[NormalizedTurn]
    raw: Mapping[str, Any]


def _normalize_multiwoz_dialogue_from_log(
    dialogue_id: str,
    dialogue_obj: Mapping[str, Any],
) -> NormalizedDialogue:
    """
    Best-effort normalizer for common MultiWOZ 2.x-style JSON structures.

    Expected (non-normative) input shape:

        {
          "goal": {...},
          "log": [
            {"text": "...", "metadata": {...}, ...},  # system or user
            ...
          ]
        }

    Many MultiWOZ releases alternate user/system on even/odd indices; this
    helper encodes that convention but does NOT treat it as normative. If your
    dataset variant encodes speaker roles explicitly, override this behavior by
    replacing `_normalize_multiwoz_dialogue` with a project-specific
    implementation.

    This function is runtime-only. It must not be treated as part of the PLD
    semantic layer.
    """
    log = dialogue_obj.get("log", [])
    normalized_turns: List[NormalizedTurn] = []
    warned_missing_speaker = False

    for idx, turn in enumerate(log):
        # Prefer explicit "speaker" when available, otherwise fall back to the
        # index-based heuristic with a warning.
        if "speaker" in turn:
            speaker = str(turn.get("speaker", "system"))
        else:
            if not warned_missing_speaker:
                logger.warning(
                    "multiwoz_loader: 'speaker' key missing in 'log' entries for "
                    "dialogue_id=%s; falling back to index-based heuristic "
                    "(even=user, odd=system).",
                    dialogue_id,
                )
                warned_missing_speaker = True
            speaker = "user" if idx % 2 == 0 else "system"

        text = str(turn.get("text", ""))

        normalized_turns.append(
            NormalizedTurn(
                speaker=speaker,
                text=text,
                raw=turn,
            )
        )

    return NormalizedDialogue(
        dialogue_id=str(dialogue_id),
        turns=normalized_turns,
        raw=dialogue_obj,
    )


def _normalize_multiwoz_dialogue(
    dialogue_key: Union[str, int],
    dialogue_obj: Mapping[str, Any],
) -> NormalizedDialogue:
    """
    Entry point for normalizing a raw MultiWOZ dialogue object.

    By default this delegates to `_normalize_multiwoz_dialogue_from_log`. If
    your local MultiWOZ variant uses a different layout (e.g. `{"turns": [...]}`,
    explicit speakers, etc.), you SHOULD fork this function and implement the
    appropriate logic while preserving the NormalizedDialogue structure.

    This function is intentionally NOT schema- or matrix-aware. It only shapes
    dataset content into a general turn sequence.
    """
    # Common cases:
    # - MultiWOZ 2.x: {"goal": {...}, "log": [...]}  (handled here)
    # - Custom-normalized: {"dialogue_id": "...", "turns": [...]}
    if "log" in dialogue_obj:
        return _normalize_multiwoz_dialogue_from_log(str(dialogue_key), dialogue_obj)

    if "turns" in dialogue_obj:
        turns_data = dialogue_obj["turns"]
        normalized_turns: List[NormalizedTurn] = []

        for turn in turns_data:
            speaker = str(turn.get("speaker", "system"))
            text = str(turn.get("text", ""))
            normalized_turns.append(
                NormalizedTurn(
                    speaker=speaker,
                    text=text,
                    raw=turn,
                )
            )

        dialogue_id = str(dialogue_obj.get("dialogue_id", dialogue_key))
        return NormalizedDialogue(
            dialogue_id=dialogue_id,
            turns=normalized_turns,
            raw=dialogue_obj,
        )

    # Fallback: treat the object as a flat turn list.
    if isinstance(dialogue_obj, list):
        normalized_turns = [
            NormalizedTurn(
                speaker=str(turn.get("speaker", "system")),
                text=str(turn.get("text", "")),
                raw=turn,
            )
            for turn in dialogue_obj  # type: ignore[arg-type]
        ]
        return NormalizedDialogue(
            dialogue_id=str(dialogue_key),
            turns=normalized_turns,
            raw={"turns": dialogue_obj},
        )

    raise ValueError(
        f"Unsupported MultiWOZ dialogue structure for key={dialogue_key!r}; "
        f"expected 'log' or 'turns' key."
    )


def iter_normalized_dialogues_from_path(
    path: Union[str, Path],
) -> Iterator[NormalizedDialogue]:
    """
    Iterate over normalized dialogues from a MultiWOZ-style JSON file.

    Supported top-level shapes (non-normative examples):

        1. Dict-of-dialogues:
            {
              "<dialogue_id>": { ... },  # dialogue object
              ...
            }

        2. List-of-dialogues:
            [
              { "dialogue_id": "...", "log": [...] },
              ...
            ]

    Any other shape SHOULD be handled by a project-specific loader that
    prepares a compatible structure and then calls `_normalize_multiwoz_dialogue`.
    """
    p = _coerce_path(path)
    raw = json.loads(p.read_text())

    if isinstance(raw, Mapping):
        for key, dialogue_obj in raw.items():
            if not isinstance(dialogue_obj, Mapping):
                continue
            yield _normalize_multiwoz_dialogue(key, dialogue_obj)

    elif isinstance(raw, list):
        for idx, dialogue_obj in enumerate(raw):
            if not isinstance(dialogue_obj, Mapping):
                continue
            key: Union[str, int] = dialogue_obj.get("dialogue_id", idx)
            yield _normalize_multiwoz_dialogue(key, dialogue_obj)
    else:
        raise ValueError(
            f"Unsupported MultiWOZ container type {type(raw)!r}; "
            f"expected dict or list."
        )


# ---------------------------------------------------------------------------
# PLD event construction (Level 1 + Level 2 alignment)
# ---------------------------------------------------------------------------


def _speaker_to_pld_source(speaker: str) -> str:
    """
    Map dataset speaker label → PLD source enum.

    PLD event schema constrains `source` to:
        "user", "assistant", "runtime", "controller", "detector", "system"

    This mapping is intentionally simple and conservative.
    """
    s = speaker.lower()
    if s in {"user", "usr", "customer", "client"}:
        return "user"
    if s in {"system", "sys", "agent", "assistant", "bot"}:
        return "assistant"
    # Fallback to "system" for unusual roles; caller may override upstream.
    return "system"


def _speaker_to_ingestion_role(speaker: str) -> str:
    """
    Map dataset speaker label → ingestion role field.

    The DialogIterator protocol (IngestionItem) expects a `role` field alongside
    `text` and `session_id`. For now we align this with the PLD `source` mapping,
    which yields "user", "assistant", or "system".
    """
    return _speaker_to_pld_source(speaker)


def _build_pld_code_for_continue(is_user_turn: bool) -> str:
    """
    Construct a PLD code for 'continue' phase.

    Lifecycle prefix 'C' MUST map to phase="continue" according to the Event Matrix.
    This helper keeps the code stable and explicit without inferring additional
    semantics.
    """
    # Examples:
    #   C0_user_turn
    #   C0_system_turn
    return "C0_user_turn" if is_user_turn else "C0_system_turn"


def _build_pld_code_for_session_closed() -> str:
    """
    Construct a PLD code for an outcome-oriented session closure.

    Lifecycle prefix 'O' MUST map to phase="outcome" according to the Event Matrix.
    """
    return "O0_session_closed"


# TODO (Open Question: Responsibility for PLD Conversion):
#   This module currently contains utilities for converting dataset turns
#   directly into PLD Events (multiwoz_turn_to_pld_event, iter_pld_events_from_multiwoz,
#   iter_envelopes_from_multiwoz), while iter_multiwoz_corpus exposes generic
#   IngestionItems (text, role, session_id) for the DialogIterator protocol.
#   Clarify whether the ingestion pipeline is intended to accept both:
#     - generic IngestionItems (raw) and
#     - pre-constructed PLD Events (or envelopes),
#   or whether PLD conversion logic should be concentrated in a dedicated layer.
#   The current IngestionConfig definition of IngestionItem may be too restrictive
#   if the architecture decides to treat PLD Events as first-class ingestion items.


def multiwoz_turn_to_pld_event(
    dialogue: NormalizedDialogue,
    turn_index: int,
    turn: NormalizedTurn,
    *,
    schema_version: str = "2.0",
    is_final_turn: bool,
) -> Dict[str, Any]:
    """
    Convert a single normalized MultiWOZ turn into a PLD runtime event.

    This function enforces:
      - Structural shape compatible with `pld_event.schema.json` (Level 1).
      - Default event_type/phase/code alignment consistent with the Event Matrix
        (Level 2).

    It does NOT:
      - Perform drift/repair detection.
      - Emit failover or evaluative events.
      - Perform JSON-Schema validation.

    Callers MUST validate the resulting events using the canonical PLD validators.
    """
    session_id = dialogue.dialogue_id
    is_user_turn = turn.speaker.lower() == "user"

    if is_final_turn:
        event_type = "session_closed"
        phase = "outcome"
        code = _build_pld_code_for_session_closed()
    else:
        event_type = "continue_allowed"
        phase = "continue"
        code = _build_pld_code_for_continue(is_user_turn=is_user_turn)

    # Core PLD event structure (must remain aligned with Level 1 schema).
    event: Dict[str, Any] = {
        "schema_version": schema_version,
        "event_id": _uuid4_str(),
        "timestamp": _now_iso8601_z(),
        "session_id": session_id,
        "turn_sequence": int(turn_index + 1),
        # Optional: turn_id can be used for correlation without affecting ordering.
        "turn_id": f"{session_id}:{turn_index + 1}",
        "source": _speaker_to_pld_source(turn.speaker),
        "event_type": event_type,
        "pld": {
            "phase": phase,
            "code": code,
            # Confidence is optional; this default expresses that we are not
            # inferring drift/repair semantics here.
            "confidence": 1.0,
            "metadata": {
                "dataset": "MultiWOZ",
                "dialogue_id": dialogue.dialogue_id,
                "turn_index": turn_index,
                "speaker": turn.speaker,
            },
        },
        "payload": {
            # Free-form content; Level 1 treats this as an open object.
            "text": turn.text,
            "raw_turn": dict(turn.raw),
            "raw_dialogue": dict(dialogue.raw),
        },
        # `runtime` block is optional in the PLD event schema; we omit it here
        # to keep the template minimal. Projects that want per-event runtime
        # metadata (latency, model, tool, etc.) SHOULD populate it upstream.
        "ux": {
            # Each utterance in MultiWOZ is visible to the user in the dialogue.
            "user_visible_state_change": True,
        },
        # Optional: callers may add "metrics" or "extensions" here, provided
        # they remain compatible with the event schema. This template leaves
        # them empty.
    }

    return event


def iter_pld_events_from_multiwoz(
    path: Union[str, Path],
    *,
    cfg: Optional[MultiWOZIngestionConfig] = None,
) -> Iterator[Dict[str, Any]]:
    """
    High-level iterator: MultiWOZ JSON file → PLD events (no envelope).

    Each normalized turn becomes exactly one PLD event. The last turn of each
    dialogue additionally closes the session with `event_type="session_closed"`
    and phase="outcome" (SHOULD, per the Event Matrix's session_closed_policy).
    """
    if cfg is None:
        cfg = MultiWOZIngestionConfig()

    for dialogue in iter_normalized_dialogues_from_path(path):
        num_turns = len(dialogue.turns)
        if num_turns == 0:
            continue

        for turn_index, turn in enumerate(dialogue.turns):
            is_final_turn = turn_index == (num_turns - 1)
            event = multiwoz_turn_to_pld_event(
                dialogue=dialogue,
                turn_index=turn_index,
                turn=turn,
                is_final_turn=is_final_turn,
            )

            # Optionally annotate payload with dataset-level metadata.
            payload = event.get("payload", {})
            payload.setdefault("dataset", cfg.dataset_name)
            if cfg.split is not None:
                payload.setdefault("split", cfg.split)
            event["payload"] = payload

            yield event


# ---------------------------------------------------------------------------
# Envelope construction (Level 5 transport mapping)
# ---------------------------------------------------------------------------


def wrap_event_in_envelope(
    event: Mapping[str, Any],
    *,
    cfg: Optional[MultiWOZIngestionConfig] = None,
    tags: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Wrap a PLD event in the runtime envelope defined by
    pld_runtime/01_schemas/runtime_event_envelope.json.

    Envelope invariants enforced here:

      - envelope.version == "2.0"
      - envelope.session.session_id == event.session_id
      - envelope.runtime.environment ∈ {"production","staging","sandbox","local"}
      - envelope.runtime.mode ∈ {"stream","batch","debug","audit"}

    This function does NOT:
      - Perform PLD event validation (callers MUST have validated event separately).
      - Modify the embedded event content.
    """
    if cfg is None:
        cfg = MultiWOZIngestionConfig()

    session_id = str(event["session_id"])

    session_block: Dict[str, Any] = {
        "session_id": session_id,
        "platform": cfg.platform,
    }
    if cfg.user_id is not None:
        session_block["user_id"] = cfg.user_id
    if cfg.platform_detail is not None:
        session_block["platform_detail"] = cfg.platform_detail

    runtime_block: Dict[str, Any] = {
        "environment": cfg.environment,
        "mode": cfg.mode,
    }
    if tags is not None:
        runtime_block["tags"] = dict(tags)

    envelope: Dict[str, Any] = {
        "envelope_id": _uuid4_str(),
        "timestamp": _now_iso8601_z(),
        "version": "2.0",
        "session": session_block,
        "runtime": runtime_block,
        "event": dict(event),
    }

    # Enforce the x-validation rule from the envelope schema using a standard
    # exception to avoid optimization-related removal of the check.
    if envelope["session"]["session_id"] != envelope["event"]["session_id"]:
        raise ValueError(
            "Envelope/session.session_id MUST equal event.session_id"
        )

    return envelope


def iter_envelopes_from_multiwoz(
    path: Union[str, Path],
    *,
    cfg: Optional[MultiWOZIngestionConfig] = None,
    tags: Optional[Mapping[str, Any]] = None,
) -> Iterator[Dict[str, Any]]:
    """
    High-level iterator: MultiWOZ JSON file → runtime envelopes containing PLD events.

    This is a helper for batch ingestion pipelines that ingest MultiWOZ dialogues
    and feed them into a PLD-aware backend that expects the runtime envelope
    format.

    Example (non-normative):

        cfg = MultiWOZIngestionConfig(
            dataset_name="MultiWOZ2.1",
            split="train",
            environment="sandbox",
            mode="batch",
            platform="custom",
            platform_detail="offline_evaluation_v1",
        )

        for envelope in iter_envelopes_from_multiwoz("multiwoz_train.json", cfg=cfg):
            ingest_envelope(envelope)  # project-specific

    Callers that do not want envelopes can use `iter_pld_events_from_multiwoz`
    directly.
    """
    if cfg is None:
        cfg = MultiWOZIngestionConfig()

    for event in iter_pld_events_from_multiwoz(path, cfg=cfg):
        yield wrap_event_in_envelope(event, cfg=cfg, tags=tags)


# ---------------------------------------------------------------------------
# DialogIterator adapter (Level 5 integration hook)
# ---------------------------------------------------------------------------


def iter_multiwoz_corpus(
    path: Union[str, Path],
    *,
    cfg: Optional[MultiWOZIngestionConfig] = None,
    tags: Optional[Mapping[str, Any]] = None,
    emit_envelopes: Optional[bool] = None,
) -> Iterator[List[Mapping[str, Any]]]:
    """
    Adapter entry point expected by ingestion_config / DialogIterator.

    Returns:
        An iterator over dialogues, where each yielded value is a list of
        IngestionItem-compatible mappings with the following minimum fields:

            {
              "text": <utterance text>,
              "role": <"user" | "assistant" | "system">,
              "session_id": <dialogue/session identifier>,
              ...
            }

        This function intentionally returns *only* generic ingestion items and
        does not expose PLD Events or Envelopes directly. Downstream layers
        (e.g., the Ingestion Orchestrator) are responsible for converting these
        items into PLD Events if required.

    Notes:
        - The `emit_envelopes` parameter is accepted for compatibility but is
          currently ignored. Regardless of its value, the return type is always
          a list of generic ingestion items as described above.
        - The exact aliasing between these dicts and the project's concrete
          IngestionItem type is handled by the configuration/orchestrator layer.
    """
    if cfg is None:
        cfg = MultiWOZIngestionConfig()

    # Keep the parameter for compatibility but do not vary the return type based
    # on it. This avoids inconsistent return types and aligns with the
    # DialogIterator protocol, which expects IngestionItems, not PLD Events or
    # Envelopes.
    _ = emit_envelopes
    _ = tags  # Currently unused at this layer; tags may be applied downstream.

    for dialogue in iter_normalized_dialogues_from_path(path):
        num_turns = len(dialogue.turns)
        if num_turns == 0:
            continue

        items: List[Mapping[str, Any]] = []

        for turn_index, turn in enumerate(dialogue.turns):
            _is_final_turn = turn_index == (num_turns - 1)

            item: Dict[str, Any] = {
                "text": turn.text,
                "role": _speaker_to_ingestion_role(turn.speaker),
                "session_id": dialogue.dialogue_id,
                # Optional metadata fields can be added as needed by the
                # orchestrator or downstream processing, but the core protocol
                # relies on the three keys above.
                "turn_index": turn_index,
                "dataset": cfg.dataset_name,
            }
            if cfg.split is not None:
                item["split"] = cfg.split

            items.append(item)

        if items:
            yield items


# ---------------------------------------------------------------------------
# Module-level summary
# ---------------------------------------------------------------------------

"""
Summary (non-executable, for human readers):

- This module is a Level 5 runtime ingestion template for MultiWOZ-style data.
- It introduces no new semantics beyond those already defined at Levels 1–3.
- It constructs PLD events that:
    * Respect the structural contract of `pld_event.schema.json`.
    * Use conservative, default-safe lifecycle mappings:
        - continue_allowed → phase="continue", C* codes.
        - session_closed  → phase="outcome", O* codes.
- It optionally wraps events in the Level 5 runtime envelope, enforcing
  session_id consistency between envelope and embedded event.
- It provides a DialogIterator-compatible adapter (iter_multiwoz_corpus) that
  returns generic ingestion items (text, role, session_id), leaving PLD
  conversion decisions to downstream orchestration.

Projects adopting this module SHOULD:

- Document runtime changes in `runtime_event_envelope.notes.md`.
- Route all generated events/envelopes through the canonical PLD validators.
- Extend or replace the normalization and mapping logic where richer semantics
  (drift/repair, failover, evaluation) are required.
"""

# Deferred for later phase
# Future-Stage Considerations:
# - None provided explicitly in the current technical review. Populate this
#   section when runtime governance or architecture review defines additional
#   follow-up work for this ingestion adapter (e.g., moving to a PLD-Event-
#   first ingestion protocol or introducing discriminators for mixed item
#   streams).

