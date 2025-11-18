#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.detection.drift_detector (v1.1)

Detects potential PLD Drift signatures using the v1.1 canonical taxonomy.

This module is aligned with:
- quickstart/metrics/schemas/pld_event.schema.json
- pld_runtime/01_schemas/pld_event.schema.json
- Integration Recipes v1.1 (Drift → Repair → Reentry → Outcome)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List, Literal


# ---------------------------------------------------------------------------
# Canonical Drift Codes (v1.1 Taxonomy)
# ---------------------------------------------------------------------------

DriftCode = Literal[
    "D5_information",
    "D1_instruction",
    "D4_tool",
    "D2_context",
    "D3_flow",
    "D0_none",
]


@dataclass
class DriftSignal:
    """
    Represents a single detected drift signal using the canonical PLD taxonomy.

    Attributes:
        type: Canonical PLD drift code (e.g., D5_information, D2_context).
        confidence: Detection confidence in the range [0.0, 1.0].
        message: Human-readable explanation of the drift.
        metadata: Optional structured details for downstream analysis.
    """
    type: DriftCode
    confidence: float
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DriftDetectionConfig:
    """
    Configuration for drift detection heuristics.

    Attributes:
        sensitivity: Coarse-grained sensitivity knob for future use
                    (e.g., 'high' → lower thresholds).
        latency_ms_threshold: Threshold in milliseconds used for latency-based
                              flow drift detection.
    """
    sensitivity: Literal["low", "medium", "high"] = "medium"
    latency_ms_threshold: int = 2500


class DriftDetector:
    """
    Rule-based drift detector producing canonical PLD drift signals.

    The detector only produces drift signals (D* codes). It does not
    perform repair or reentry decisions; those are handled by the runtime
    controller and Integration Recipes.
    """

    def __init__(self, config: Optional[DriftDetectionConfig] = None) -> None:
        self.config = config or DriftDetectionConfig()

    def detect(self, *, content: str, runtime: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect potential drift signatures based on response content and runtime context.

        Args:
            content: The candidate model response text.
            runtime: Runtime context, such as:
                     - expected_format: Required substring or marker.
                     - tool_used: Name of tool invoked in this turn.
                     - latency_ms: Measured latency for the turn.
                     - user_goal: Optional canonical representation of user intent.

        Returns:
            A dictionary with:
                - has_drift: bool, whether any drift signal was detected.
                - signals: List[DriftSignal], all detected signals.
        """
        signals: List[DriftSignal] = []
        normalized = (content or "").lower().strip()

        # ------------------ D2_context (Format / Constraint) ------------------
        expected_format = runtime.get("expected_format")
        if expected_format and expected_format.lower() not in normalized:
            signals.append(
                DriftSignal(
                    type="D2_context",
                    confidence=0.75,
                    message=f"Content is missing the expected format marker: '{expected_format}'.",
                )
            )

        # ------------------ D4_tool (Execution Failure) ------------------
        tool_used = runtime.get("tool_used")
        if tool_used and "error" in normalized:
            signals.append(
                DriftSignal(
                    type="D4_tool",
                    confidence=0.8,
                    message="Tool invocation appears to have failed or returned an error state.",
                    metadata={"tool": tool_used},
                )
            )

        # ------------------ D3_flow (Latency-Based Flow Drift) ------------------
        latency = runtime.get("latency_ms", 0)
        if isinstance(latency, (int, float)) and latency > self.config.latency_ms_threshold:
            signals.append(
                DriftSignal(
                    type="D3_flow",
                    confidence=0.5,
                    message=f"High latency detected ({latency} ms) relative to configured threshold.",
                    metadata={"latency_ms": latency},
                )
            )

        # ------------------ D1_instruction (Intent Drift) ------------------
        user_goal = runtime.get("user_goal")
        if user_goal and isinstance(user_goal, str):
            # Very lightweight heuristic: if user_goal keywords are mostly absent
            # we treat this as potential instruction drift.
            goal_tokens = {t for t in user_goal.lower().split() if len(t) > 3}
            missing_tokens = [t for t in goal_tokens if t not in normalized]

            if goal_tokens and len(missing_tokens) == len(goal_tokens):
                signals.append(
                    DriftSignal(
                        type="D1_instruction",
                        confidence=0.7,
                        message="Candidate response appears misaligned with the stated user goal.",
                        metadata={
                            "user_goal": user_goal,
                            "missing_tokens": missing_tokens,
                        },
                    )
                )

        # ------------------ D5_information (Retrieval / Knowledge Failure) ------------------
        # Simple heuristic example for information drift.
        if "no results" in normalized or "i don't know" in normalized:
            signals.append(
                DriftSignal(
                    type="D5_information",
                    confidence=0.6,
                    message="Potential information retrieval failure or ungrounded response.",
                )
            )

        # If no specific drift was detected, record explicit D0_none if needed downstream.
        if not signals:
            signals.append(
                DriftSignal(
                    type="D0_none",
                    confidence=1.0,
                    message="No drift detected based on current heuristics.",
                )
            )

        return {
            "has_drift": any(s.type != "D0_none" for s in signals),
            "signals": signals,
        }


def drift_signal_to_pld_event(signal: DriftSignal, session_id: str) -> Dict[str, Any]:
    """
    Convert a DriftSignal into a canonical PLD event structure.

    The resulting event is compatible with:
      - quickstart/metrics/schemas/pld_event.schema.json
      - pld_runtime/01_schemas/pld_event.schema.json
    """
    now = datetime.now(timezone.utc)

    return {
        "event_id": f"evt_{now.timestamp()}",
        "session_id": session_id,
        "timestamp": now.isoformat(),
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
    }
