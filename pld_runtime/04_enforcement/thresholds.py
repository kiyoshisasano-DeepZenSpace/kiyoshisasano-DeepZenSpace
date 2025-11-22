"""
pld_runtime/04_enforcement/thresholds.py

PLD Runtime Thresholds — Merged Edition

version: 2.0.4-rt-merge
status: runtime
referenced_authority_levels: [1, 2, 3, 5]
scope: Enforcement thresholds (drift detection, observability, timing windows, validation mode alignment)
change_type: merged-from-v1.1, runtime-only, non-breaking, patch-integration

PRIMARY BASIS:
    - v2.0.0-rt1 template (authoritative runtime structure)
MERGED CONTENT:
    - v1.1 timing-based enforcement semantics retained selectively where still applicable
      and not replaced by new confidence/escalation logic.

GOVERNANCE RULES:
    - No changes to Level 1 schema fields or enums.
    - No changes to Level 2 phase–prefix or event_type–phase mapping.
    - No changes to Level 3 metric definitions.
    - Additions are runtime-only, safe, and do not alter canonical interpretations.

# TODO: Review required (referenced_authority_levels usage — should ThresholdProfile
# carry an explicit authority level for runtime validation?)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Mapping, Any


# ---------------------------------------------------------------------------
# Validation Modes (authoritative from v2 runtime)
# ---------------------------------------------------------------------------

class ValidationMode(str, Enum):
    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"


# ---------------------------------------------------------------------------
# Runtime Environment (aligned with envelope)
# ---------------------------------------------------------------------------

class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    SANDBOX = "sandbox"
    LOCAL = "local"


# ---------------------------------------------------------------------------
# v2 Runtime Threshold Classes (updated for interface consistency)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DriftThresholds:
    min_confidence_to_emit: float
    min_confidence_for_escalation: float
    max_soft_repairs_per_cycle: int
    max_drift_cycles_before_failover: int


@dataclass(frozen=True)
class ObservabilityThresholds:
    latency_spike_ms: int
    consecutive_spike_window: int


@dataclass(frozen=True)
class RecoveryThresholds:
    """
    Thresholds for recovery and reentry behavior.

    # NOTE: Migration difference
    # These thresholds are aligned with VRL semantics but do not redefine how
    # the VRL metric is computed; they only configure runtime windows.
    """

    max_recovery_turns: int
    max_recovery_seconds: int

    # TODO: Review required (clarify whether recovery enforcement uses
    # OR vs AND between max_recovery_turns and max_recovery_seconds).


@dataclass(frozen=True)
class ValidationThresholds:
    allow_rejected_events_for_observability_metrics: bool
    log_normalization_attempts: bool
    include_should_violations_in_canonical_metrics: bool


# ---------------------------------------------------------------------------
# Optional Timing Thresholds
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TimingThresholds:
    """
    Retained from v1.1 to support timing-based evaluation workflows.

    These are optional at the behavioral level — enforcement logic SHOULD check
    `.enabled` to decide whether to use these limits.
    """

    enabled: bool = False
    drift_to_repair_ms: int = 30000
    repair_to_reentry_ms: int = 30000
    jitter_allowance_ms: int = 5000
    grace_window_end_ms: int = 10000

    # TODO: Review required (should a global configuration flag determine activation?)


# ---------------------------------------------------------------------------
# Unified Threshold Profile
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ThresholdProfile:
    environment: Environment
    validation_mode: ValidationMode

    drift: DriftThresholds
    observability: ObservabilityThresholds
    recovery: RecoveryThresholds
    validation: ValidationThresholds
    timing: TimingThresholds  # presence is guaranteed; optionality via `enabled` flag


# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

_DEFAULT_VALIDATION_THRESHOLDS: Mapping[ValidationMode, ValidationThresholds] = {
    ValidationMode.STRICT: ValidationThresholds(
        allow_rejected_events_for_observability_metrics=False,
        log_normalization_attempts=False,
        include_should_violations_in_canonical_metrics=False,
    ),
    ValidationMode.WARN: ValidationThresholds(
        allow_rejected_events_for_observability_metrics=True,
        log_normalization_attempts=True,
        include_should_violations_in_canonical_metrics=True,
    ),
    ValidationMode.NORMALIZE: ValidationThresholds(
        allow_rejected_events_for_observability_metrics=True,
        log_normalization_attempts=True,
        include_should_violations_in_canonical_metrics=True,
    ),
}


# ---------------------------------------------------------------------------
# Named Configuration Constants (keyword-based for safety)
# ---------------------------------------------------------------------------

# Base defaults
_BASE_DRIFT = DriftThresholds(
    min_confidence_to_emit=0.60,
    min_confidence_for_escalation=0.80,
    max_soft_repairs_per_cycle=2,
    max_drift_cycles_before_failover=3,
)
_BASE_OBSERVABILITY = ObservabilityThresholds(
    latency_spike_ms=3500,
    consecutive_spike_window=2,
)
_BASE_RECOVERY = RecoveryThresholds(
    max_recovery_turns=10,
    max_recovery_seconds=300,
)
_BASE_TIMING = TimingThresholds(enabled=False)

# Production overrides
_PRODUCTION_DRIFT = DriftThresholds(
    min_confidence_to_emit=0.70,
    min_confidence_for_escalation=0.90,
    max_soft_repairs_per_cycle=2,
    max_drift_cycles_before_failover=2,
)
_PRODUCTION_OBSERVABILITY = ObservabilityThresholds(
    latency_spike_ms=2500,
    consecutive_spike_window=2,
)
_PRODUCTION_RECOVERY = RecoveryThresholds(
    max_recovery_turns=8,
    max_recovery_seconds=240,
)
_PRODUCTION_TIMING = TimingThresholds(
    enabled=True,
    drift_to_repair_ms=15000,
    repair_to_reentry_ms=15000,
    jitter_allowance_ms=3000,
    grace_window_end_ms=5000,
)


# ---------------------------------------------------------------------------
# Profile Factory
# ---------------------------------------------------------------------------

def _make_profile(env: Environment, mode: ValidationMode) -> ThresholdProfile:
    """
    Construct a ThresholdProfile for a given environment and validation mode.

    # NOTE: Now driven by named constants instead of literals.
    """
    if env is Environment.PRODUCTION:
        drift = _PRODUCTION_DRIFT
        observability = _PRODUCTION_OBSERVABILITY
        recovery = _PRODUCTION_RECOVERY
        timing = _PRODUCTION_TIMING
    else:
        drift = _BASE_DRIFT
        observability = _BASE_OBSERVABILITY
        recovery = _BASE_RECOVERY
        timing = _BASE_TIMING

    return ThresholdProfile(
        environment=env,
        validation_mode=mode,
        drift=drift,
        observability=observability,
        recovery=recovery,
        validation=_DEFAULT_VALIDATION_THRESHOLDS[mode],
        timing=timing,
    )


# ---------------------------------------------------------------------------
# Explicit full Cartesian mapping of configurations
# ---------------------------------------------------------------------------

DEFAULT_PROFILES: Dict[tuple[Environment, ValidationMode], ThresholdProfile] = {
    (env, mode): _make_profile(env, mode)
    for env in Environment
    for mode in ValidationMode
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_threshold_profile(environment: str, validation_mode: str) -> ThresholdProfile:
    """
    Resolve a ThresholdProfile given runtime environment and validation mode.
    """

    try:
        env_enum = Environment(environment.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported environment: {environment!r}") from exc

    try:
        mode_enum = ValidationMode(validation_mode.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported validation_mode: {validation_mode!r}") from exc

    return DEFAULT_PROFILES[(env_enum, mode_enum)]


__all__ = [
    "Environment",
    "ValidationMode",
    "DriftThresholds",
    "ObservabilityThresholds",
    "RecoveryThresholds",
    "ValidationThresholds",
    "TimingThresholds",
    "ThresholdProfile",
    "DEFAULT_PROFILES",
    "get_threshold_profile",
]


# ---------------------------------------------------------------------------
# Deferred for later phase
# ---------------------------------------------------------------------------

# - Potential refactor: Replace _make_profile branching logic with configuration strategy map.
# - Potential dynamic loading from external configuration bundles.
# - Potential environment inheritance (e.g., PRE_PROD → PRODUCTION defaults).
# - Evaluate whether optional timing should support partial overrides rather than on/off state.
