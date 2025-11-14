#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.detection.drift_detector

Detects potential PLD Drift signatures in runtime events or agent traces.

This module does NOT enforce or modify runtime behavior.
It emits *candidate drift events* which can then be:

    - validated by schema_validator
    - sequenced by sequence_rules
    - escalated via response_policy
    - logged for evaluation or offline analysis

Detection is probabilistic and rule-based at this stage
(no ML classifier yet).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Literal, Tuple


# ---------------------------------------------------------------------------
# Drift Categories (aligned with drift_repair_codes.json)
# ---------------------------------------------------------------------------

DriftType = Literal[
    "content_drift",
    "intent_mismatch",
    "hallucination",
    "format_violation",
    "tool_misuse",
    "latency_behavioral_drift",
    "unknown"
]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class DriftDetectionConfig:
    """
    Rule-based drift detection parameters.

    Sensitivity scale:
    - low: drift requires strong evidence
    - medium: balanced default
    - high: aggressive detection (useful for debugging)

    Latency drift threshold:
        If runtime latency > latency_ms_threshold, mark potential drift.
    """

    sensitivity: Literal["low", "medium", "high"] = "medium"
    latency_ms_threshold: int = 2500
    detect_format_drift: bool = True
    detect_tool_misuse: bool = True
    detect_intent_shift: bool = True
    detect_hallucination_keywords: bool = False  # future upgrade placeholder


# ---------------------------------------------------------------------------
# Result Model
# ---------------------------------------------------------------------------

@dataclass
class DriftSignal:
    """Intermediate signal before conversion into a full PLD event."""
    type: DriftType
    confidence: float
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftDetectionResult:
    """Return value of the detector."""
    has_drift: bool
    signals: List[DriftSignal]

    def strongest(self) -> Optional[DriftSignal]:
        return max(self.signals, key=lambda s: s.confidence) if self.signals else None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_text(text: Optional[str]) -> str:
    return (text or "").lower().strip()


# ---------------------------------------------------------------------------
# Detection Logic
# ---------------------------------------------------------------------------

class DriftDetector:
    """
    Rule-based drift detector.

    Input may include:
        - LLM responses
        - transcript turns
        - tool call results
        - runtime metadata (latency, model switch, missing context)
    """

    def __init__(self, config: Optional[DriftDetectionConfig] = None):
        self.config = config or DriftDetectionConfig()

    def detect(self, *, content: str, runtime: Dict[str, Any]) -> DriftDetectionResult:
        """
        Detect drift from a single conversational turn or agent execution.

        Parameters
        ----------
        content : str
            Raw agent response or tool result.

        runtime : dict
            Expected structure:
            {
                "latency_ms": int,
                "tool_used": Optional[str],
                "expected_format": Optional[str]
            }
        """
        signals: List[DriftSignal] = []

        normalized = _normalize_text(content)

        # ------------------ Format Drift ------------------
        if self.config.detect_format_drift:
            fmt = runtime.get("expected_format")
            if fmt and fmt not in normalized:
                signals.append(
                    DriftSignal(
                        type="format_violation",
                        confidence=0.55 if self.config.sensitivity == "low" else 0.75,
                        message=f"Content may not match expected format: '{fmt}'",
                        metadata={"expected": fmt}
                    )
                )

        # ------------------ Tool Misuse ------------------
        if self.config.detect_tool_misuse:
            if runtime.get("tool_used") and "error" in normalized:
                signals.append(
                    DriftSignal(
                        type="tool_misuse",
                        confidence=0.6 if self.config.sensitivity == "low" else 0.8,
                        message="Tool invocation appears inconsistent or failed.",
                        metadata={"tool": runtime.get("tool_used")}
                    )
                )

        # ------------------ Latency Drift ------------------
        latency = runtime.get("latency_ms", 0)
        if latency and latency > self.config.latency_ms_threshold:
            signals.append(
                DriftSignal(
                    type="latency_behavioral_drift",
                    confidence=0.5,
                    message=f"High latency detected ({latency} ms).",
                    metadata={"latency_ms": latency}
                )
            )

        # ------------------ Intent Mismatch ------------------
        if self.config.detect_intent_shift and "sorry" in normalized and "?" not in normalized:
            signals.append(
                DriftSignal(
                    type="intent_mismatch",
                    confidence=0.6,
                    message="Potential intent mismatch or reset phrase detected."
                )
            )

        return DriftDetectionResult(
            has_drift=bool(signals),
            signals=signals,
        )


# ---------------------------------------------------------------------------
# Conversion to PLD Event Format
# ---------------------------------------------------------------------------

def drift_signal_to_pld_event(
    signal: DriftSignal,
    *,
    session_id: str,
    turn_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convert a DriftSignal into a complete PLD event conforming to
    pld_event.schema.json.

    Caller is responsible for envelope wrapping.
    """

    return {
        "event_id": f"drift-{signal.type}-{_now_iso()}",
        "timestamp": _now_iso(),
        "session_id": session_id,
        "turn_id": turn_id,
        "source": "runtime_detector",
        "event_type": "drift_detected",

        "pld": {
            "phase": "drift",
            "code": signal.type,
            "confidence": signal.confidence,
        },

        "payload": {
            "message": signal.message,
            "metadata": signal.metadata,
        },

        "runtime": {
            "detector": "rule_based_v1"
        }
    }


__all__ = [
    "DriftDetector",
    "DriftDetectionConfig",
    "DriftSignal",
    "DriftDetectionResult",
    "drift_signal_to_pld_event",
]
