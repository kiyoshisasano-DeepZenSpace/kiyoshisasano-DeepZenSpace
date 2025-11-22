#!/usr/bin/env python3
# version: 2.0.0
# status: draft
# authority_scope: Level 5 — runtime implementation
# purpose: Turn-level drift detection for PLD-aligned runtimes, producing PLD-compatible drift codes.
# change_classification: runtime-only, behavioral merge from v1.1 to v2 scaffold + issue resolution
# dependencies: Level 1 PLD event schema, Level 2 event matrix, Level 3 metrics specification

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, List
import re


# -----------------------------------------------------------------------------
# Rule configuration (addresses "magic numbers" core issue)
# -----------------------------------------------------------------------------
DRIFT_RULE_CONFIG = {
    "D4_tool_error": {
        "confidence": 0.95,
        "priority": 3,
    },
    "D5_latency_spike": {
        "confidence": 0.7,
        "priority": 1,
    },
    "D2_context": {
        "confidence": 0.75,
        "priority": 1,
    },
    "D1_instruction": {
        "confidence": 0.7,
        "priority": 2,
    },
    "D5_information": {
        "confidence": 0.6,
        "priority": 0,
    },
    "D3_repeated_plan": {
        "confidence": 0.8,
        "priority": 2,
    },
}


# -----------------------------------------------------------------------------
# Core Signal Object
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class DriftSignal:
    code: str
    confidence: float
    reason: Optional[str] = None
    details: Mapping[str, Any] | None = None
    # Higher priority wins when confidences are equal.
    priority: int = 0


# -----------------------------------------------------------------------------
# Input Contract Definition (formalizes turn_state interface)
# -----------------------------------------------------------------------------
class TurnStateProtocol(Mapping[str, Any]):
    """
    This protocol defines required and optional fields used by the detector.

    Required semantics:
    - latency_ms: numeric runtime performance metric
    - content: candidate model output text

    Optional semantics:
    - expected_format
    - user_goal
    - history (list of past turn dicts; structure MAY vary)
    - tool_used
    - tool_error (boolean)
    """


# -----------------------------------------------------------------------------
# Detector Implementation
# -----------------------------------------------------------------------------
class DriftDetector:
    """
    PLD-aligned drift detector.

    The detector evaluates multiple drift heuristics per turn, aggregates
    candidate signals, then returns a single selected DriftSignal.
    """

    def __init__(
        self,
        *,
        latency_threshold_ms: int = 3500,
        max_repeated_plan_turns: int = 3,
        min_confidence_threshold: float = 0.6,
    ) -> None:
        """
        Parameters
        ----------
        latency_threshold_ms:
            Threshold for classifying latency spikes as drift.
        max_repeated_plan_turns:
            Window size for repeated-plan detection.
        min_confidence_threshold:
            Minimum confidence required for a signal to override the implicit
            "no drift" state. Addresses unbounded sensitivity / noise.
        """
        self.latency_threshold_ms = latency_threshold_ms
        self.max_repeated_plan_turns = max_repeated_plan_turns
        self.min_confidence_threshold = min_confidence_threshold

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------
    def detect(self, turn_state: TurnStateProtocol) -> DriftSignal:
        """
        Detect drift for a single agent turn.

        All detection rules execute and signals are collected. Highest confidence
        (then priority) determines primary signal. If the best signal falls
        below min_confidence_threshold, the detector returns D0_none.
        """

        signals: List[DriftSignal] = []

        raw_content = turn_state.get("content") or ""
        content = str(raw_content)
        normalized_content = content.lower().strip()

        # Tool Error Check
        if self._has_tool_error(turn_state, normalized_content):
            cfg = DRIFT_RULE_CONFIG["D4_tool_error"]
            signals.append(
                DriftSignal(
                    code="D4_tool_error",
                    confidence=cfg["confidence"],
                    reason="tool_error_flag",
                    details={
                        "tool_error": True,
                        "tool_used": turn_state.get("tool_used"),
                    },
                    priority=cfg["priority"],
                )
            )

        # Latency-Based Drift
        if self._has_latency_spike(turn_state):
            cfg = DRIFT_RULE_CONFIG["D5_latency_spike"]
            latency_ms = float(turn_state.get("latency_ms", 0.0))
            signals.append(
                DriftSignal(
                    code="D5_latency_spike",
                    confidence=cfg["confidence"],
                    reason="latency_above_threshold",
                    details={
                        "latency_ms": latency_ms,
                        "threshold_ms": self.latency_threshold_ms,
                    },
                    priority=cfg["priority"],
                )
            )

        # Context Drift
        if self._has_context_drift(turn_state, normalized_content):
            cfg = DRIFT_RULE_CONFIG["D2_context"]
            signals.append(
                DriftSignal(
                    code="D2_context",
                    confidence=cfg["confidence"],
                    reason="expected_format_missing",
                    details={
                        "expected_format": turn_state.get("expected_format"),
                    },
                    priority=cfg["priority"],
                )
            )

        # Instruction Drift
        if self._has_instruction_drift(turn_state, normalized_content):
            cfg = DRIFT_RULE_CONFIG["D1_instruction"]
            user_goal = turn_state.get("user_goal")
            tokens = self._goal_tokens(user_goal)
            missing = [t for t in tokens if t not in normalized_content]
            signals.append(
                DriftSignal(
                    code="D1_instruction",
                    confidence=cfg["confidence"],
                    reason="user_goal_tokens_partial_or_missing",
                    details={
                        "user_goal": user_goal,
                        "missing_tokens": missing,
                    },
                    priority=cfg["priority"],
                )
            )

        # Information Drift
        if self._has_information_drift(normalized_content):
            cfg = DRIFT_RULE_CONFIG["D5_information"]
            signals.append(
                DriftSignal(
                    code="D5_information",
                    confidence=cfg["confidence"],
                    reason="information_or_retrieval_failure",
                    details={},
                    priority=cfg["priority"],
                )
            )

        # Repeated Plan Drift
        if self._has_repeated_plan(turn_state):
            cfg = DRIFT_RULE_CONFIG["D3_repeated_plan"]
            signals.append(
                DriftSignal(
                    code="D3_repeated_plan",
                    confidence=cfg["confidence"],
                    reason="repeated_plan_detected",
                    details={
                        "max_repeated_plan_turns": self.max_repeated_plan_turns,
                    },
                    priority=cfg["priority"],
                )
            )

        # No drift detected
        if not signals:
            return DriftSignal(code="D0_none", confidence=1.0, priority=0)

        # Selection Strategy:
        # - Highest confidence wins
        # - On confidence tie, higher priority wins.
        best = max(signals, key=lambda s: (s.confidence, s.priority))

        # Enforce minimum confidence threshold; otherwise treat as no drift.
        if best.confidence < self.min_confidence_threshold:
            return DriftSignal(code="D0_none", confidence=1.0, priority=0)

        return best

    # -------------------------------------------------------------------------
    # Internal Heuristics
    # -------------------------------------------------------------------------
    def _has_tool_error(self, turn_state: Mapping[str, Any], normalized_content: str) -> bool:
        if turn_state.get("tool_error"):
            return True
        tool_used = turn_state.get("tool_used")
        if tool_used and "error" in normalized_content:
            return True
        return False

    def _has_latency_spike(self, turn_state: Mapping[str, Any]) -> bool:
        raw_latency = turn_state.get("latency_ms")
        if raw_latency is None:
            return False
        try:
            latency_ms = float(raw_latency)
        except (TypeError, ValueError):
            return False
        return latency_ms > float(self.latency_threshold_ms)

    def _has_context_drift(self, turn_state: Mapping[str, Any], normalized_content: str) -> bool:
        expected_format = turn_state.get("expected_format")
        if not expected_format or not isinstance(expected_format, str):
            return False
        return expected_format.lower() not in normalized_content

    def _has_instruction_drift(self, turn_state: Mapping[str, Any], normalized_content: str) -> bool:
        """
        Instruction / intent drift heuristic.

        Uses majority-missing rule:
        - Drift when more than 50% of goal tokens are absent from the response.
        """
        user_goal = turn_state.get("user_goal")
        if not isinstance(user_goal, str):
            return False

        goal_tokens = self._goal_tokens(user_goal)
        if not goal_tokens:
            return False

        missing = [t for t in goal_tokens if t not in normalized_content]
        missing_ratio = len(missing) / float(len(goal_tokens))

        return missing_ratio > 0.5

    @staticmethod
    def _goal_tokens(user_goal: str) -> set[str]:
        """
        Extract alphanumeric goal tokens, including numeric values.
        """
        return set(re.findall(r"\w+", user_goal.lower()))

    @staticmethod
    def _has_information_drift(normalized_content: str) -> bool:
        return (
            "no results" in normalized_content
            or "i don't know" in normalized_content
            or "unknown" in normalized_content
        )

    def _has_repeated_plan(self, turn_state: Mapping[str, Any]) -> bool:
        history = turn_state.get("history")
        if not isinstance(history, list) or len(history) < self.max_repeated_plan_turns:
            return False

        extracted = [self._extract_plan_text(entry) for entry in history[-self.max_repeated_plan_turns :]]
        extracted = [p for p in extracted if p]

        if len(extracted) < self.max_repeated_plan_turns:
            return False

        first = extracted[0]
        return all(p == first for p in extracted[1:])

    @staticmethod
    def _extract_plan_text(entry: Any) -> Optional[str]:
        """
        Normalize text before comparison to avoid brittle punctuation/whitespace
        differences when detecting repeated plans.
        """
        if not isinstance(entry, Mapping):
            return None

        plan = entry.get("plan") or entry.get("content")
        if not isinstance(plan, str):
            return None

        text = plan.strip()
        if not text:
            return None

        normalized = re.sub(r"\W+", " ", text).strip().lower()
        return normalized or None


# -----------------------------------------------------------------------------
# TODO ITEMS (from Open Questions)
# -----------------------------------------------------------------------------
# TODO: Clarify whether Level 2 Event Matrix supports multiple simultaneous drift signals.
# TODO: Define handling rule for missing metadata (treat as warning vs. clean pass).
# TODO: Confirm canonical latency unit: milliseconds vs. seconds.
# TODO: Define confidence thresholding strategy for overriding D0_none with low-confidence drift signals (runtime policy vs. detector default).
# TODO: Determine how strictly TurnStateProtocol will be enforced at runtime (e.g., adapters vs. direct dict access).
# TODO: Define operational "threshold of concern" for agent intervention based on confidence and priority.
# TODO: Clarify semantics of D0_none (fallback vs. positive assertion of health) and whether explicit "healthy" heuristics are required.
# TODO: Clarify semantic meaning of confidence values for deterministic checks (e.g., latency-based drift vs. probabilistic heuristics).


# -----------------------------------------------------------------------------
# Deferred for later phase
# -----------------------------------------------------------------------------
# - Rule-weighted classification strategies
# - Model-driven drift inference
# - Overlapping drift category handling policies
# - Confidence calibration based on historical tuning

