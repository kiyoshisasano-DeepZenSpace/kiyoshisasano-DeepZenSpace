#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.enforcement.thresholds (v1.1 Canonical Edition)

Central time and policy thresholds for PLD runtime enforcement.

Purpose
-------
- Unify configurable timing and behavioral tolerances for PLD traces.
- Provide a stable contract for evaluation, runtime enforcement,
  and post-hoc analysis.
- Support multiple strictness presets (production, research, debug).

This module does NOT perform validation or sequencing itself.
It only exposes configuration values in a controlled format.

Canonical Alignment
-------------------
- Phases:  drift → repair → reentry → outcome → none
- Metrics: thresholds are typically consumed by:
    - sequence_rules.SequenceRuleConfig
    - response_policy.evaluate_policy
    - controller-level enforcement logic
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any


# ---------------------------------------------------------------------------
# Enforcement Modes (policy behavior)
# ---------------------------------------------------------------------------

class EnforcementMode(str, Enum):
    """
    High-level enforcement posture.

    STRICT
        Hard failures when sequence or timing rules are violated.
        Used in production models where consistency is critical.

    BALANCED
        Violations do NOT stop execution, but trigger repair hints or logging.
        Recommended default for applied PLD operations.

    OBSERVATIONAL
        No enforcement, only monitoring/evaluation.
        Useful for research traces and drift baselining.
    """

    STRICT = "strict"
    BALANCED = "balanced"
    OBSERVATIONAL = "observational"


# ---------------------------------------------------------------------------
# Threshold Configuration Schema
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Thresholds:
    """
    Time thresholds in milliseconds.

    Naming conventions
    ------------------
    drift_to_repair_ms
        Allowed latency between a drift and the required repair.

    repair_to_reentry_ms
        Allowed latency between a repair and reentry confirmation.

    jitter_allowance_ms
        Additional slack for noisy runtime conditions (e.g., network jitter).
        Typically used by higher-level analysis, not by sequence_rules directly.

    grace_window_end_ms
        Delay allowed before labeling unhandled sequences as timeout cases.
        Can be used by batch evaluators to determine when a trace is "complete".
    """

    drift_to_repair_ms: int = 30000
    repair_to_reentry_ms: int = 30000

    # Optional tolerances for noisy runtime conditions.
    jitter_allowance_ms: int = 5000

    # Delay allowed before labeling unhandled sequences as timeout cases.
    grace_window_end_ms: int = 10000

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Predefined Profiles
# ---------------------------------------------------------------------------

THRESHOLDS_PROFILES: Dict[EnforcementMode, Thresholds] = {
    EnforcementMode.STRICT: Thresholds(
        drift_to_repair_ms=10000,
        repair_to_reentry_ms=10000,
        jitter_allowance_ms=2000,
        grace_window_end_ms=3000,
    ),
    EnforcementMode.BALANCED: Thresholds(
        drift_to_repair_ms=30000,
        repair_to_reentry_ms=30000,
        jitter_allowance_ms=5000,
        grace_window_end_ms=10000,
    ),
    EnforcementMode.OBSERVATIONAL: Thresholds(
        drift_to_repair_ms=60000,
        repair_to_reentry_ms=60000,
        jitter_allowance_ms=10000,
        grace_window_end_ms=30000,
    ),
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_thresholds(mode: EnforcementMode | str = EnforcementMode.BALANCED) -> Thresholds:
    """
    Retrieve threshold configuration for a given enforcement mode.

    Falls back to BALANCED if the input is not recognized.
    """
    if isinstance(mode, str):
        try:
            mode = EnforcementMode(mode.lower())  # type: ignore[arg-type]
        except Exception:
            mode = EnforcementMode.BALANCED
    return THRESHOLDS_PROFILES[mode]


__all__ = [
    "EnforcementMode",
    "Thresholds",
    "get_thresholds",
    "THRESHOLDS_PROFILES",
]
