#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.detection.repair_detector (v1.1 Canonical Edition)

Detects PLD Repair behavior in runtime traces.

This module:
- inspects conversational turns / agent actions
- emits *candidate repair signals*
- converts them to PLD events compatible with pld_event.schema.json

It does NOT:
- apply the repair
- reset state
- enforce any policy

Responsibility:
    detection only → enforcement/response_policy.py decides what to do.

Canonical Alignment:
- Repair codes follow the v1.1 taxonomy:

    R1_clarify
    R2_soft_repair
    R3_rewrite
    R4_request_clarification
    R5_hard_reset
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Literal, Optional


# ---------------------------------------------------------------------------
# Repair Categories (aligned with R1–R5 canonical codes)
# ---------------------------------------------------------------------------

RepairType = Literal[
    "R1_clarify",
    "R2_soft_repair",
    "R3_rewrite",
    "R4_request_clarification",
    "R5_hard_reset",
    "unknown",
]


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class RepairDetectionConfig:
    """
    Heuristic repair detection parameters.

    sensitivity:
        - low: conservative, only strong evidence is treated as repair
        - medium: balanced default
        - high: aggressive, more actions flagged as repair

    signals:
        - detect_ux_repair:
            pacing / apology / retry language (maps to R3_rewrite by default).
        - detect_local_repair:
            explicit corrections or clarifications without full reset
            (maps to R1_clarify / R2_soft_repair).
        - detect_structural_repair:
            mentions of memory, state alignment, re-sync, recomputing, etc.
            (maps to R2_soft_repair).
        - detect_hard_reset:
            "let's start over", session reset, context discard
            (maps to R5_hard_reset).
    """

    sensitivity: Literal["low", "medium", "high"] = "medium"
    detect_ux_repair: bool = True
    detect_local_repair: bool = True
    detect_structural_repair: bool = True
    detect_hard_reset: bool = True


# ---------------------------------------------------------------------------
# Result Model
# ---------------------------------------------------------------------------

@dataclass
class RepairSignal:
    """Intermediate repair signal prior to PLD event conversion."""
    type: RepairType
    confidence: float
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RepairDetectionResult:
    """Detection output for a single turn / action."""
    has_repair: bool
    signals: List[RepairSignal]

    def strongest(self) -> Optional[RepairSignal]:
        return max(self.signals, key=lambda s: s.confidence) if self.signals else None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _norm(text: Optional[str]) -> str:
    return (text or "").lower().strip()


def _confidence(base: float, sensitivity: str) -> float:
    if sensitivity == "low":
        return max(0.0, min(1.0, base - 0.1))
    if sensitivity == "high":
        return max(0.0, min(1.0, base + 0.1))
    return max(0.0, min(1.0, base))


# ---------------------------------------------------------------------------
# Detection Logic
# ---------------------------------------------------------------------------

class RepairDetector:
    """
    Heuristic-based repair detector.

    Input:
        content:
            Agent/system message or tool result that might embody a repair.

        runtime:
            Free-form dict, recommended keys:
              - latency_ms
              - previously_failed (bool)
              - previous_phase ("drift", "repair", "reentry", "none")
              - tool_used
              - reset_flag (bool)  # if runtime knows it reset context

    Output:
        RepairDetectionResult with one or more RepairSignal objects
        classified into canonical repair types (R1–R5).
    """

    def __init__(self, config: Optional[RepairDetectionConfig] = None):
        self.config = config or RepairDetectionConfig()

    def detect(self, *, content: str, runtime: Dict[str, Any]) -> RepairDetectionResult:
        txt = _norm(content)
        signals: List[RepairSignal] = []

        # ---------- UX Repair (R3_rewrite-like) ----------
        # UX-facing language that smooths pacing or acknowledges issues.
        if self.config.detect_ux_repair:
            if any(
                k in txt
                for k in ["still checking", "one moment", "hold on", "processing", "investigating"]
            ):
                signals.append(
                    RepairSignal(
                        type="R3_rewrite",
                        confidence=_confidence(0.6, self.config.sensitivity),
                        message="Pacing / reassurance language suggests UX-oriented repair.",
                        metadata={"kind": "pacing_ack"},
                    )
                )
            if "sorry" in txt or "apologize" in txt:
                signals.append(
                    RepairSignal(
                        type="R3_rewrite",
                        confidence=_confidence(0.55, self.config.sensitivity),
                        message="Apologetic phrasing suggests UX repair / rewrite of prior behavior.",
                        metadata={"kind": "apology"},
                    )
                )

        # ---------- Local Repair (R1_clarify / R2_soft_repair-like) ----------
        if self.config.detect_local_repair:
            # Explicit clarification
            if any(k in txt for k in ["let me correct", "to clarify", "what i meant", "small correction"]):
                signals.append(
                    RepairSignal(
                        type="R1_clarify",
                        confidence=_confidence(0.7, self.config.sensitivity),
                        message="Explicit local clarification or correction.",
                        metadata={"kind": "local_correction"},
                    )
                )
            # Local retry / soft adjustment
            if "retry" in txt or "try again" in txt:
                signals.append(
                    RepairSignal(
                        type="R2_soft_repair",
                        confidence=_confidence(0.6, self.config.sensitivity),
                        message="Retry wording suggests local soft repair.",
                        metadata={"kind": "retry"},
                    )
                )

        # ---------- Structural Repair (R2_soft_repair-like) ----------
        if self.config.detect_structural_repair:
            if any(
                k in txt
                for k in ["resync", "re-sync", "synchronize", "refreshing context", "reloading data"]
            ):
                signals.append(
                    RepairSignal(
                        type="R2_soft_repair",
                        confidence=_confidence(0.75, self.config.sensitivity),
                        message="Mentions of synchronization / context refresh indicate structural soft repair.",
                        metadata={"kind": "state_sync"},
                    )
                )
            if "updating memory" in txt or "rebuilding the plan" in txt:
                signals.append(
                    RepairSignal(
                        type="R2_soft_repair",
                        confidence=_confidence(0.7, self.config.sensitivity),
                        message="Explicit state or plan rebuild indicates structural soft repair.",
                        metadata={"kind": "plan_rebuild"},
                    )
                )

        # ---------- Hard Reset (R5_hard_reset-like) ----------
        if self.config.detect_hard_reset:
            hard_reset_phrases = [
                "let's start over",
                "starting over",
                "reset this conversation",
                "clear the context",
                "i will restart",
            ]
            if any(p in txt for p in hard_reset_phrases) or runtime.get("reset_flag"):
                signals.append(
                    RepairSignal(
                        type="R5_hard_reset",
                        confidence=_confidence(0.8, self.config.sensitivity),
                        message="Hard reset / restart wording detected.",
                        metadata={"reset_flag": bool(runtime.get("reset_flag"))},
                    )
                )

        return RepairDetectionResult(
            has_repair=bool(signals),
            signals=signals,
        )


# ---------------------------------------------------------------------------
# Conversion to PLD Event Format
# ---------------------------------------------------------------------------

def repair_signal_to_pld_event(
    signal: RepairSignal,
    *,
    session_id: str,
    turn_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Convert a RepairSignal into a PLD event object compatible with
    pld_event.schema.json.

    Mapping (RepairType → PLD code):

        R1_clarify             → R1_clarify
        R2_soft_repair         → R2_soft_repair
        R3_rewrite             → R3_rewrite
        R4_request_clarification → R4_request_clarification
        R5_hard_reset          → R5_hard_reset
        unknown                → R2_soft_repair (generic soft repair fallback)
    """
    if signal.type in {
        "R1_clarify",
        "R2_soft_repair",
        "R3_rewrite",
        "R4_request_clarification",
        "R5_hard_reset",
    }:
        pld_code = signal.type
    else:
        # For unknown repairs, degrade to a generic soft repair code.
        pld_code = "R2_soft_repair"

    return {
        "event_id": f"repair-{signal.type}-{_now_iso()}",
        "timestamp": _now_iso(),
        "session_id": session_id,
        "turn_id": turn_id,
        "source": "runtime_detector",
        "event_type": "repair_triggered",
        "pld": {
            "phase": "repair",
            "code": pld_code,
            "confidence": signal.confidence,
        },
        "payload": {
            "message": signal.message,
            "metadata": signal.metadata,
        },
        "runtime": {
            "detector": "repair_rule_based_v1_1",
        },
    }


__all__ = [
    "RepairDetector",
    "RepairDetectionConfig",
    "RepairSignal",
    "RepairDetectionResult",
    "repair_signal_to_pld_event",
]
