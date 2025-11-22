# version: 2.0.0
# status: draft
# authority: Level 5 — runtime implementation
# scope: Repair selection and classification from PLD-aligned drift signals
# change_type: runtime-only, incremental patch (core issue integration)
# dependencies: PLD Event Schema v2.0; PLD Event Matrix v2.0

"""
PLD Runtime — Repair Detector (Scaffold + Minimal Reference Behavior)

Status: draft
Authority: Level 5 — runtime implementation
Scope: Repair selection and classification from PLD-aligned drift signals

Changes in this patch:
    - Implements minimal working strategy logic (resolves: Non-Executable Prototype).
    - Introduces RepairMode Enum to prevent magic string schema fragility.
    - Normalizes DriftSignal to avoid data duplication conflicts (computed code property).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


# ---------------------------------------------------------------------------
# Validation Mode
# ---------------------------------------------------------------------------

class ValidationMode(str, Enum):
    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"


# ---------------------------------------------------------------------------
# Schema-safe Repair Codes
# ---------------------------------------------------------------------------

class RepairMode(str, Enum):
    """Stable repair taxonomy aligned with expected R-prefix lifecycle semantics."""

    R1_CLARIFY = "R1_clarify"
    R2_SOFT_REPAIR = "R2_soft_repair"
    R3_REWRITE = "R3_rewrite"
    R4_REQUEST_CLARIFICATION = "R4_request_clarification"
    R5_HARD_RESET = "R5_hard_reset"
    FALLBACK = "R2_soft_repair"  # generic fallback


# ---------------------------------------------------------------------------
# Drift Signal — normalized to avoid conflicting data
# ---------------------------------------------------------------------------

@dataclass
class DriftSignal:
    """Represents drift, using source_event as the single source of truth."""

    source_event: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    @property
    def code(self) -> str:
        """Always derive from canonical PLD event payload to avoid desync."""
        return self.source_event.get("pld", {}).get("code", "D0_unspecified")


# ---------------------------------------------------------------------------
# Repair Decision Model
# ---------------------------------------------------------------------------

@dataclass
class RepairDecision:
    """Canonical output from repair selection."""

    mode: RepairMode
    escalation_level: Optional[int] = None
    normalized: bool = False
    notes: Optional[str] = None


# ---------------------------------------------------------------------------
# Repair Detector (with minimal functioning reference logic)
# ---------------------------------------------------------------------------

class RepairDetector:
    """PLD-aligned repair selector.

    Now contains:
        ✔ minimal executable strategy table
        ✔ schema-safe decision taxonomy
        ✔ drift normalization safeguards
    """

    _REFERENCE_STRATEGY_TABLE = {
        "D1": RepairMode.R1_CLARIFY,
        "D2": RepairMode.R2_SOFT_REPAIR,
        "D3": RepairMode.R2_SOFT_REPAIR,
        "D4": RepairMode.R3_REWRITE,
        "D5": RepairMode.R5_HARD_RESET,
    }

    def __init__(
        self,
        validation_mode: ValidationMode = ValidationMode.STRICT,
        max_soft_repairs: int = 1,
        max_total_repairs: int = 3,
    ) -> None:
        self.validation_mode = validation_mode
        self.max_soft_repairs = max_soft_repairs
        self.max_total_repairs = max_total_repairs

    # ---------------------------------------------------------------------
    # Core logic
    # ---------------------------------------------------------------------

    def select_repair(
        self,
        drift: DriftSignal,
        repair_count_for_session: int,
        repair_count_for_drift_code: int,
    ) -> RepairDecision:
        """Select a repair strategy for a given drift signal.

        Args:
            drift:
                DriftSignal instance describing the detected drift.
            repair_count_for_session:
                Number of prior repair attempts in the current session.
            repair_count_for_drift_code:
                Number of prior repair attempts specifically associated with
                this drift.code.

        Returns:
            RepairDecision describing the chosen repair strategy.
        """
        # TODO: Review required — clarify state ownership between Detector and Controller
        drift_prefix = drift.code.split("_")[0]  # ex: "D3"
        mode = self._REFERENCE_STRATEGY_TABLE.get(drift_prefix, RepairMode.FALLBACK)

        # Escalation rule:
        # - First cross of max_soft_repairs threshold → intermediate rewrite (R3)
        # - Hard reset (R5) reserved for crossing max_total_repairs
        if repair_count_for_drift_code >= self.max_soft_repairs:
            if repair_count_for_session >= self.max_total_repairs:
                mode = RepairMode.R5_HARD_RESET
            else:
                mode = RepairMode.R3_REWRITE

        return RepairDecision(
            mode=mode,
            escalation_level=repair_count_for_drift_code,
            notes=f"Selected via reference strategy for {drift.code}",
        )

    def to_repair_event(
        self,
        decision: RepairDecision,
        session_id: str,
        turn_sequence: int,
        base_timestamp: str,
        source: str = "runtime",
        previous_event_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Construct a PLD repair event skeleton from a RepairDecision."""
        return {
            "schema_version": "2.0",
            "event_id": f"repair-{turn_sequence}-{decision.mode.value}-{base_timestamp}",
            "timestamp": base_timestamp,
            "session_id": session_id,
            "turn_sequence": turn_sequence,
            "source": source,
            "event_type": "repair_triggered",
            "pld": {
                "phase": "repair",
                "code": decision.mode.value,
                "confidence": 1.0,
            },
            "ux": {
                "user_visible_state_change": False,
            },
            "payload": {
                "notes": decision.notes,
                "escalation_level": decision.escalation_level,
                "previous_event_id": previous_event_id,
            },
        }

    def validate_drift_signal(self, drift: DriftSignal) -> None:
        """Optional hook for drift-signal validation against PLD semantics."""
        # TODO: Review required (alignment question #1: state ownership / RepairHistory)
        # TODO: Review required (alignment question #2: validation strictness vs fail-open prototype)
        return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__ = [
    "RepairDetector",
    "ValidationMode",
    "RepairDecision",
    "RepairMode",
    "DriftSignal",
]


# ---------------------------------------------------------------------------
# Deferred for later phase
# ---------------------------------------------------------------------------

"""
Future-Stage Considerations (Not implemented in this patch):

- Automatic escalation memory / session state retention
- Full event bus integration for ID, timestamp, and ordering authority
- Cross-session analytics and adaptive escalation weighting
- Configurable plug-in detection heuristics similar to the v1.1 behavioral model
"""
