#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.detection.pattern_classifier (v1.1 Canonical Edition)

Lightweight PLD phase/code classifier for individual turns or segments.

Responsibilities:
- Classify a text segment into:
    - phase:  drift / repair / reentry / outcome / none
    - code:   concrete PLD code from 01_schemas/drift_repair_codes.json
    - confidence: 0.0–1.0
- Provide both:
    - heuristic (no-LLM) mode
    - LLM-assisted mode (when OpenAI API is available)

NON-goals:
- Full dataset labeling (that pipeline should follow docs/04_pld_labeling_prompt_llm.md)
- Temporal reasoning across multiple turns (use enforcement/sequence_rules.py)

Intended usage:
- Online detection of candidate PLD events for runtime logging
- Quick classification in tools / dashboards
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Optional, Literal, List, Tuple


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Phase = Literal["drift", "repair", "reentry", "outcome", "none"]

ClassificationSource = Literal["heuristic", "llm", "llm_fallback_heuristic", "none"]


@dataclass
class PatternClassifierConfig:
    """
    Configuration for PLD pattern classifier.

    Parameters
    ----------
    use_llm:
        If True, attempt LLM-based classification first, with heuristic fallback.

    model:
        OpenAI model name for LLM classification.

    min_confidence:
        Minimum confidence below which the classifier will degrade to a
        `phase = "none"` result with `code = "D0_none"`.
    """

    use_llm: bool = False
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    min_confidence: float = 0.35


@dataclass
class PatternClassificationResult:
    """
    Lightweight classification outcome.
    """

    phase: Phase
    code: str
    confidence: float
    source: ClassificationSource
    rationale: str = ""
    raw_llm: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # raw_llm may contain non-serializable objects; keep it simple
        if self.raw_llm is not None:
            d["raw_llm"] = self.raw_llm
        return d


# ---------------------------------------------------------------------------
# Drift/Repair/Reentry code registry loader
# ---------------------------------------------------------------------------

_HERE = Path(__file__).resolve().parent
_SCHEMAS_DIR = _HERE.parent / "01_schemas"
_CODES_FILE = _SCHEMAS_DIR / "drift_repair_codes.json"

_DRIFT_CODES: List[str] = []
_REPAIR_CODES: List[str] = []
_REENTRY_CODES: List[str] = []


def _load_code_registry() -> None:
    """
    Load drift/repair/reentry codes from 01_schemas/drift_repair_codes.json
    if available; otherwise keep in-memory defaults.
    """
    global _DRIFT_CODES, _REPAIR_CODES, _REENTRY_CODES

    if _DRIFT_CODES or _REPAIR_CODES or _REENTRY_CODES:
        return

    if not _CODES_FILE.exists():
        # Minimal safe defaults in case schemas are missing
        _DRIFT_CODES = ["D0_none"]
        _REPAIR_CODES = ["R0_none"]
        _REENTRY_CODES = ["RE0_none"]
        return

    try:
        data = json.loads(_CODES_FILE.read_text(encoding="utf-8"))
        allowed = data.get("allowed_values", {})
        _DRIFT_CODES = list(map(str, allowed.get("drift", ["D0_none"])))
        _REPAIR_CODES = list(map(str, allowed.get("repair", ["R0_none"])))
        _REENTRY_CODES = list(map(str, allowed.get("reentry", ["RE0_none"])))
    except Exception:
        _DRIFT_CODES = ["D0_none"]
        _REPAIR_CODES = ["R0_none"]
        _REENTRY_CODES = ["RE0_none"]


# ---------------------------------------------------------------------------
# Heuristic layer
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    return text.strip().lower()


def _fallback_code(preferred: str, pool: List[str], default: str) -> str:
    """
    Choose a canonical code, preferring `preferred` if present in `pool`.
    """
    if preferred in pool:
        return preferred
    if pool:
        return pool[0]
    return default


def _heuristic_phase_and_code(text: str) -> Tuple[Phase, str, float, str]:
    """
    Very light heuristic classifier:
    - Prefers interpretability over complexity.
    - Returns (phase, code, confidence, rationale).
    """
    _load_code_registry()

    t = _normalize(text)
    if not t:
        return "none", "D0_none", 0.0, "Empty text."

    # -------------------- DRIFT-ish signals --------------------

    # User flags incorrect or off-target information → D5_information
    if any(k in t for k in ["that's not correct", "inaccurate", "wrong", "incorrect", "not what i asked"]):
        code = _fallback_code("D5_information", _DRIFT_CODES, "D0_none")
        return "drift", code, 0.7, "User explicitly flags incorrect or off-target information."

    # Topic / intent mismatch → D1_instruction
    if any(k in t for k in ["off topic", "not relevant", "different topic"]):
        code = _fallback_code("D1_instruction", _DRIFT_CODES, "D0_none")
        return "drift", code, 0.65, "User flags topic or intent mismatch."

    # Lost or inconsistent context → D2_context
    if any(k in t for k in ["we already said", "as i mentioned", "you forgot", "you lost the context"]):
        code = _fallback_code("D2_context", _DRIFT_CODES, "D0_none")
        return "drift", code, 0.65, "User indicates lost or inconsistent context."

    # -------------------- REPAIR-ish signals --------------------

    # Clarification / small correction → R1_clarify
    if any(k in t for k in ["let me correct", "to clarify", "small correction", "i'll fix that"]):
        code = _fallback_code("R1_clarify", _REPAIR_CODES, "R0_none")
        return "repair", code, 0.7, "Explicit local clarification or correction phrasing."

    # Hard reset / context discard → R5_hard_reset
    if any(k in t for k in ["reset this", "start over", "clear the context", "from scratch"]):
        code = _fallback_code("R5_hard_reset", _REPAIR_CODES, "R0_none")
        return "repair", code, 0.75, "Hard reset or context discard phrasing."

    # Structural / state-level repair → R2_soft_repair (soft structural repair)
    if any(k in t for k in ["refreshing", "resync", "re-sync", "reloading data", "rebuilding the plan"]):
        code = _fallback_code("R2_soft_repair", _REPAIR_CODES, "R0_none")
        return "repair", code, 0.7, "Structural or state-level repair phrasing."

    # UX-oriented apology / retry → R3_rewrite
    if any(k in t for k in ["sorry about that", "apologize", "let me try again", "try again"]):
        code = _fallback_code("R3_rewrite", _REPAIR_CODES, "R0_none")
        return "repair", code, 0.6, "UX-oriented apology or retry phrasing."

    # -------------------- REENTRY-ish signals --------------------

    # Resume or continue task → RE3_auto
    if any(k in t for k in ["back to the main task", "continue where we left", "resume", "as we were saying"]):
        code = _fallback_code("RE3_auto", _REENTRY_CODES, "RE0_none")
        return "reentry", code, 0.65, "Explicit resume or continue phrasing."

    # Restore previous constraints → RE4_memory_restore
    if "use the previous constraints" in t or "same conditions as before" in t:
        code = _fallback_code("RE4_memory_restore", _REENTRY_CODES, "RE0_none")
        return "reentry", code, 0.6, "Mentions restoring earlier constraints or state."

    # Workflow-oriented continuation → RE3_auto
    if "continue the workflow" in t or "pick up the flow" in t:
        code = _fallback_code("RE3_auto", _REENTRY_CODES, "RE0_none")
        return "reentry", code, 0.6, "Workflow reentry phrasing."

    # -------------------- Otherwise: no strong signal --------------------

    return "none", "D0_none", 0.0, "No strong PLD pattern identified."


def classify_heuristic(text: str, *, min_confidence: float = 0.0) -> PatternClassificationResult:
    """
    Pure heuristic classification (no LLM).
    """
    phase, code, conf, rationale = _heuristic_phase_and_code(text)
    if conf < min_confidence:
        phase, code, conf, rationale = "none", "D0_none", 0.0, "Confidence below configured minimum."

    return PatternClassificationResult(
        phase=phase,
        code=code,
        confidence=conf,
        source="heuristic" if conf > 0.0 else "none",
        rationale=rationale,
        raw_llm=None,
    )


# ---------------------------------------------------------------------------
# LLM layer (optional)
# ---------------------------------------------------------------------------

def _has_openai() -> bool:
    """Check if OpenAI client is available and minimally usable."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return False
    try:
        from openai import OpenAI  # type: ignore
        _ = OpenAI(api_key=api_key)
        return True
    except Exception:
        return False


def _classify_with_llm(text: str, config: PatternClassifierConfig) -> Optional[PatternClassificationResult]:
    """
    Attempt LLM-based classification. Returns None on any failure.
    """
    if not _has_openai():
        return None

    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "").strip())
    except Exception:
        return None

    _load_code_registry()

    codes_description = {
        "drift": _DRIFT_CODES,
        "repair": _REPAIR_CODES,
        "reentry": _REENTRY_CODES,
    }

    prompt = (
        "You are a PLD (Phase Loop Dynamics) classifier.\n"
        "Given a single turn from a conversation (user or assistant), "
        "label it with:\n"
        "  - phase: one of [drift, repair, reentry, outcome, none]\n"
        "  - code: one PLD code from the allowed sets, or 'D0_none' if no drift/repair/reentry applies\n"
        "  - confidence: float 0.0–1.0\n"
        "  - rationale: short natural language explanation.\n\n"
        "Allowed codes (drift/repair/reentry):\n"
        f"{json.dumps(codes_description, ensure_ascii=False, indent=2)}\n\n"
        "Return ONLY JSON with keys: phase, code, confidence, rationale.\n"
    )

    try:
        resp = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": "You classify conversational turns into PLD phases and canonical v1.1 PLD codes."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": f"TEXT = {json.dumps(text, ensure_ascii=False)}"},
            ],
            temperature=config.temperature,
        )
        content = resp.choices[0].message.content or ""
    except Exception:
        return None

    content = content.strip()
    if not content.startswith("{"):
        return None

    try:
        data = json.loads(content)
    except Exception:
        return None

    phase = str(data.get("phase", "none")).lower()
    if phase not in {"drift", "repair", "reentry", "outcome", "none"}:
        phase = "none"

    code = str(data.get("code", "D0_none") or "D0_none")
    try:
        conf = float(data.get("confidence", 0.0))
    except (TypeError, ValueError):
        conf = 0.0
    rationale = str(data.get("rationale", "")).strip()

    if conf < config.min_confidence:
        phase, code, conf = "none", "D0_none", 0.0

    return PatternClassificationResult(
        phase=phase,  # type: ignore[arg-type]
        code=code,
        confidence=conf,
        source="llm" if conf > 0.0 else "none",
        rationale=rationale,
        raw_llm={"response": data},
    )


# ---------------------------------------------------------------------------
# Public classifier API
# ---------------------------------------------------------------------------

class PatternClassifier:
    """
    Unified PLD pattern classifier.

    Typical usage:

        classifier = PatternClassifier(PatternClassifierConfig(use_llm=True))
        result = classifier.classify_turn(text="...", role="assistant")
    """

    def __init__(self, config: Optional[PatternClassifierConfig] = None):
        self.config = config or PatternClassifierConfig()

    def classify_turn(
        self,
        *,
        text: str,
        role: Literal["user", "assistant", "system"] = "user",
    ) -> PatternClassificationResult:
        """
        Classify a single turn.

        Role is included for future heuristics (currently not heavily used).
        """
        base = classify_heuristic(text, min_confidence=0.0)

        if not self.config.use_llm:
            # Heuristic only, apply threshold at the end.
            if base.confidence < self.config.min_confidence:
                base.phase = "none"
                base.code = "D0_none"
                base.confidence = 0.0
                base.source = "none"
                base.rationale = "Heuristic confidence below configured minimum."
            return base

        # Try LLM first; fallback to heuristic if needed.
        llm_res = _classify_with_llm(text, self.config)
        if llm_res is None or llm_res.confidence < self.config.min_confidence:
            # Fallback to heuristic
            base.source = "llm_fallback_heuristic" if base.confidence > 0.0 else "none"
            if base.confidence < self.config.min_confidence:
                base.phase = "none"
                base.code = "D0_none"
                base.confidence = 0.0
                base.rationale = "Both LLM and heuristic were below minimum confidence."
            return base

        return llm_res


__all__ = [
    "PatternClassifierConfig",
    "PatternClassificationResult",
    "PatternClassifier",
    "classify_heuristic",
]
