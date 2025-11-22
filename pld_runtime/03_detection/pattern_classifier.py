# PLD Runtime Pattern Classifier
# version: 2.0.0
# status: experimental merge candidate
# authority: Level 5 — runtime implementation
# scope: Per-turn drift pattern classification for PLD-aligned runtimes
# purpose: Unified runtime classifier supporting structured signals and optional heuristic/LLM fallback
# change_classification: runtime-only merge
# dependencies: PLD event schema v2.x, PLD event matrix v2.x

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Sequence, Literal


# -----------------------------------------------------------------------------
# Canonical Drift Codes
# -----------------------------------------------------------------------------

class DriftCode(str, Enum):
    # Core Issue 1 Fix: add missing canonical codes for LLM classification usefulness
    D0_NONE = "D0_none"
    D1_INSTRUCTION = "D1_instruction"       # Newly added
    D2_CONTEXT = "D2_context"               # Newly added
    D3_REPEATED_PLAN = "D3_repeated_plan"
    D4_TOOL_ERROR = "D4_tool_error"
    D5_LATENCY_SPIKE = "D5_latency_spike"
    D9_UNSPECIFIED = "D9_unspecified"


# -----------------------------------------------------------------------------
# Runtime Context Models
# -----------------------------------------------------------------------------

@dataclass(frozen=True)
class TurnContext:
    session_id: str
    turn_sequence: int
    source: str
    model_name: Optional[str] = None
    tools_called: Sequence[str] = ()


@dataclass(frozen=True)
class TurnSignals:
    tool_error: bool = False
    latency_ms: Optional[float] = None
    repeated_plan_detected: bool = False
    external_drift_code: Optional[str] = None
    extra: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DriftClassification:
    code: DriftCode
    confidence: float
    reason: str
    auxiliary: Mapping[str, Any] = field(default_factory=dict)


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

ClassificationSource = Literal["heuristic", "signal", "llm", "llm_fallback_heuristic", "none"]


@dataclass
class PatternClassifierConfig:
    latency_spike_threshold_ms: float = 3500.0
    min_confidence_default: float = 1.0
    tool_error_confidence: float = 0.95
    repeated_plan_confidence: float = 0.80
    latency_spike_confidence: float = 0.70
    allow_external_override: bool = True

    # legacy behavior
    use_llm: bool = False
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    min_confidence: float = 0.35


# -----------------------------------------------------------------------------
# Optional legacy heuristic fallback
# -----------------------------------------------------------------------------

def _normalize(text: str) -> str:
    return text.strip().lower()


def _heuristic_classify_text(text: str, *, min_confidence_target: float) -> Optional[DriftClassification]:
    t = _normalize(text)
    
    # TODO (Open Question 1): Clarify semantics of empty-text classification
    if not t:
        return DriftClassification(
            code=DriftCode.D0_NONE,
            confidence=0.0,
            reason="Empty text heuristic.",
        )

    if any(k in t for k in ["wrong", "inaccurate", "not what i asked"]):
        return DriftClassification(
            DriftCode.D1_INSTRUCTION,
            0.7,
            "Heuristic: user flagged intent mismatch.",
        )

    if any(k in t for k in ["you forgot", "lost context", "we already said"]):
        return DriftClassification(
            DriftCode.D2_CONTEXT,
            0.65,
            "Heuristic: user indicates context inconsistency.",
        )

    if any(k in t for k in ["resume", "continue where we left"]):
        return DriftClassification(
            DriftCode.D0_NONE,
            0.6,
            "Heuristic continuation phrasing detected.",
        )

    return None


# -----------------------------------------------------------------------------
# LLM fallback module
# -----------------------------------------------------------------------------

def _classify_with_llm(text: str, config: PatternClassifierConfig) -> Optional[DriftClassification]:
    # TODO (Open Question 2): Consider prompt enhancement with brief code definitions
    try:
        from openai import OpenAI  # type: ignore
        client = OpenAI()
    except Exception:
        return None

    allowed = [c.value for c in DriftCode]

    prompt = (
        "Classify conversational drift using PLD codes.\n"
        "Return JSON with keys: { code, confidence, reason }\n\n"
        f"Allowed codes: {allowed}"
    )

    try:
        resp = client.chat.completions.create(
            model=config.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=config.temperature,
        )
        parsed = json.loads(resp.choices[0].message.content or "{}")

        code_raw = str(parsed.get("code", DriftCode.D9_UNSPECIFIED.value))
        code_enum = DriftCode(code_raw) if code_raw in allowed else DriftCode.D9_UNSPECIFIED

        confidence = float(parsed.get("confidence", 0.0))
        if confidence < config.min_confidence:
            return None

        reason = parsed.get("reason", "LLM classification")
        return DriftClassification(code_enum, confidence, reason)

    except Exception:
        return None


# -----------------------------------------------------------------------------
# Final Unified Classifier
# -----------------------------------------------------------------------------

class PatternClassifier:
    """
    Primary drift detector.

    NOTE: Core Issue 2 acknowledgment:
    This classifier intentionally surfaces ONLY the dominant detected condition.
    It does NOT emit an array of signals.
    """

    def __init__(self, config: Optional[PatternClassifierConfig] = None) -> None:
        self._config = config or PatternClassifierConfig()

    def classify(
        self,
        context: TurnContext,
        signals: TurnSignals,
        text: Optional[str] = None,
    ) -> DriftClassification:

        # External override (respects dynamic controlled override)
        external = self._classify_external(signals)
        if external:
            return external

        # Priority evaluation
        if signals.tool_error:
            return DriftClassification(
                DriftCode.D4_TOOL_ERROR,
                self._config.tool_error_confidence,
                "Tool error detected.",
            )

        if signals.repeated_plan_detected:
            return DriftClassification(
                DriftCode.D3_REPEATED_PLAN,
                self._config.repeated_plan_confidence,
                "Repeated plan detected.",
            )

        if signals.latency_ms and signals.latency_ms > self._config.latency_spike_threshold_ms:
            return DriftClassification(
                DriftCode.D5_LATENCY_SPIKE,
                self._config.latency_spike_confidence,
                "Latency spike detected.",
            )

        # Fallback heuristics before LLM
        if text and not self._config.use_llm:
            h = _heuristic_classify_text(text, min_confidence_target=self._config.min_confidence)
            if h:
                return h

        if text and self._config.use_llm:
            llm = _classify_with_llm(text, self._config)
            if llm:
                return llm

        return DriftClassification(
            DriftCode.D0_NONE,
            self._config.min_confidence_default,
            "No drift detected.",
        )

    def _classify_external(self, signals: TurnSignals) -> Optional[DriftClassification]:
        raw = signals.external_drift_code
        if not raw or not self._config.allow_external_override or not raw.startswith("D"):
            return None

        for c in DriftCode:
            if c.value == raw:
                return DriftClassification(
                    c,
                    self._config.min_confidence_default,
                    "External override provided (trusted).",
                )

        return DriftClassification(
            DriftCode.D9_UNSPECIFIED,
            self._config.min_confidence_default,
            "External override provided (unrecognized, normalized).",
            auxiliary={"external_code": raw},
        )


__all__ = [
    "PatternClassifier",
    "PatternClassifierConfig",
    "DriftClassification",
    "TurnContext",
    "TurnSignals",
    "DriftCode",
]


# -----------------------------------------------------------------------------
# Deferred for later phase
# -----------------------------------------------------------------------------
# - Multi-signal reporting and aggregation strategy
# - LLM prompt enrichment with human-readable semantic definitions
# - Confidence semantics standardization across empty-text vs valid-text cases
