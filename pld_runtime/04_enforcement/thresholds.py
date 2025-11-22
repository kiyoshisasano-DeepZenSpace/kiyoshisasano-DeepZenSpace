# version: 2.0.0
# status: runtime
# authority_level_scope: Level 5 — runtime implementation
# purpose: Threshold policy definitions and evaluation helpers for PLD runtime metrics and runtime profiles.
# change_classification: runtime-only, non-breaking, prototype technical review patch
# dependencies: Level 1 PLD event schema v2.x, Level 2 event matrix v2.x, Level 3 runtime metrics schema v2.x

"""
Threshold policy module for PLD-aligned runtimes.

This module provides data structures and entry points for defining and
evaluating metric-based enforcement thresholds (warn/alert/failover, etc.).
It is intentionally implementation-specific and MUST NOT override Level 1–3
specifications. All semantics derived from metrics MUST use PLD-valid events.

# NOTE: Migration difference
# Environment/validation-mode threshold profiles from v2.0.4-rt-merge are
# retained as a compatibility layer. Metric-level threshold evaluation
# (MetricThreshold + evaluate_thresholds) is the primary interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple


# ---------------------------------------------------------------------------
# Core enums
# ---------------------------------------------------------------------------


class ValidationMode(str, Enum):
    """Mirror of runtime validation modes used for PLD event/metric handling."""

    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"


class ThresholdOperator(str, Enum):
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    EQ = "=="
    NE = "!="


class ThresholdSeverity(str, Enum):
    INFO = "info"
    WARN = "warn"
    CRITICAL = "critical"


class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    SANDBOX = "sandbox"
    LOCAL = "local"


# ---------------------------------------------------------------------------
# Metric-level configuration structures (primary)
# ---------------------------------------------------------------------------


# NOTE: Core Technical Issue Addressed — semantic ambiguity:
# Until a formal vocabulary is governed, string interpretation responsibility
# is explicitly delegated to the consumer (runtime or policy engine).
AGGREGATION_SCOPE_NOTE = (
    "Interpretation of `aggregation_scope` and `window` is implementation-defined; "
    "runtime-level consumers MUST supply normalization or validation if required."
)


@dataclass(frozen=True)
class MetricThreshold:
    metric: str
    operator: ThresholdOperator
    value: float
    severity: ThresholdSeverity

    # Optional configuration-layer hints
    aggregation_scope: Optional[str] = None
    window: Optional[str] = None
    validation_mode: Optional[ValidationMode] = None
    description: Optional[str] = None

    # NOTE: Migration difference
    _semantics_notice: str = AGGREGATION_SCOPE_NOTE


@dataclass(frozen=True)
class ThresholdBreach:
    metric: str
    threshold: MetricThreshold
    observed_value: float
    message: str


# ---------------------------------------------------------------------------
# Legacy-style runtime profile thresholds (compatibility layer)
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
    max_recovery_turns: int
    max_recovery_seconds: int


@dataclass(frozen=True)
class ValidationThresholds:
    allow_rejected_events_for_observability_metrics: bool
    log_normalization_attempts: bool
    include_should_violations_in_canonical_metrics: bool


@dataclass(frozen=True)
class TimingThresholds:
    enabled: bool = False
    drift_to_repair_ms: int = 30000
    repair_to_reentry_ms: int = 30000
    jitter_allowance_ms: int = 5000
    grace_window_end_ms: int = 10000


@dataclass(frozen=True)
class ThresholdProfile:
    environment: Environment
    validation_mode: ValidationMode

    drift: DriftThresholds
    observability: ObservabilityThresholds
    recovery: RecoveryThresholds
    validation: ValidationThresholds
    timing: TimingThresholds


# ---------------------------------------------------------------------------
# Evaluation helpers (metric-level)
# ---------------------------------------------------------------------------

_EPSILON = 1e-9  # NOTE: Core Technical Issue Fixed — float comparison stability


def _compare(operator: ThresholdOperator, lhs: float, rhs: float) -> bool:
    """Pure comparator helper (audit safe, no implicit type coercion)."""

    # NOTE: Migration difference — EQ and NE now use tolerance-based comparisons.
    if operator == ThresholdOperator.EQ:
        return abs(lhs - rhs) < _EPSILON
    if operator == ThresholdOperator.NE:
        return abs(lhs - rhs) >= _EPSILON

    if operator == ThresholdOperator.GT:
        return lhs > rhs
    if operator == ThresholdOperator.GTE:
        return lhs >= rhs
    if operator == ThresholdOperator.LT:
        return lhs < rhs
    if operator == ThresholdOperator.LTE:
        return lhs <= rhs

    raise ValueError(f"Unsupported operator: {operator!r}")


def evaluate_thresholds(
    metrics: Mapping[str, float],
    thresholds: Iterable[MetricThreshold],
    *,
    active_mode: Optional[ValidationMode] = None,
) -> Sequence[ThresholdBreach]:
    """Evaluate MetricThreshold entries against provided metric values.

    WARNING: This function only evaluates generic MetricThresholds.
    It does NOT enforce legacy ThresholdProfile limits (Drift/Recovery).
    Consumers MUST apply any profile-based checks separately.
    """
    breaches: list[ThresholdBreach] = []

    for threshold in thresholds:
        if threshold.validation_mode and active_mode and threshold.validation_mode is not active_mode:
            continue

        value = metrics.get(threshold.metric)
        if value is None:
            # NOTE: Core Technical Issue Fixed — missing metrics in STRICT mode
            if active_mode is ValidationMode.STRICT:
                message_parts: list[str] = [
                    f"metric={threshold.metric}",
                    "observed=missing",
                    "reason=missing_metric_in_strict_mode",
                    f"severity={threshold.severity.value}",
                ]
                breaches.append(
                    ThresholdBreach(
                        metric=threshold.metric,
                        threshold=threshold,
                        observed_value=float("nan"),
                        message="; ".join(message_parts),
                    )
                )
            continue

        if _compare(threshold.operator, value, threshold.value):
            message_parts: list[str] = [
                f"metric={threshold.metric}",
                f"observed={value}",
                f"operator={threshold.operator.value}",
                f"threshold={threshold.value}",
                f"severity={threshold.severity.value}",
            ]
            if threshold.aggregation_scope:
                message_parts.append(f"scope={threshold.aggregation_scope}")
            if threshold.window:
                message_parts.append(f"window={threshold.window}")
            if threshold.description:
                message_parts.append(f"desc={threshold.description}")

            breaches.append(
                ThresholdBreach(
                    metric=threshold.metric,
                    threshold=threshold,
                    observed_value=value,
                    message="; ".join(message_parts),
                )
            )

    return breaches


# ---------------------------------------------------------------------------
# Default threshold sets
# ---------------------------------------------------------------------------


def get_default_thresholds() -> Tuple[MetricThreshold, ...]:
    return ()


def build_threshold_index(
    thresholds: Iterable[MetricThreshold],
) -> Dict[str, Tuple[MetricThreshold, ...]]:
    index: Dict[str, list[MetricThreshold]] = {}
    for t in thresholds:
        index.setdefault(t.metric, []).append(t)
    return {metric: tuple(ts) for metric, ts in index.items()}


# ---------------------------------------------------------------------------
# Legacy profile system (retained for compatibility)
# ---------------------------------------------------------------------------


_DEFAULT_VALIDATION_THRESHOLDS: Mapping[ValidationMode, ValidationThresholds] = {
    ValidationMode.STRICT: ValidationThresholds(False, False, False),
    ValidationMode.WARN: ValidationThresholds(True, True, True),
    ValidationMode.NORMALIZE: ValidationThresholds(True, True, True),
}

_BASE_DRIFT = DriftThresholds(0.60, 0.80, 2, 3)
_BASE_OBSERVABILITY = ObservabilityThresholds(3500, 2)
_BASE_RECOVERY = RecoveryThresholds(10, 300)
_BASE_TIMING = TimingThresholds(enabled=False)

_PRODUCTION_DRIFT = DriftThresholds(0.70, 0.90, 2, 2)
_PRODUCTION_OBSERVABILITY = ObservabilityThresholds(2500, 2)
_PRODUCTION_RECOVERY = RecoveryThresholds(8, 240)
_PRODUCTION_TIMING = TimingThresholds(True, 15000, 15000, 3000, 5000)


def _make_profile(env: Environment, mode: ValidationMode) -> ThresholdProfile:
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


DEFAULT_PROFILES: Dict[Tuple[Environment, ValidationMode], ThresholdProfile] = {
    (env, mode): _make_profile(env, mode)
    for env in Environment
    for mode in ValidationMode
}


def get_threshold_profile(environment: str, validation_mode: str) -> ThresholdProfile:
    try:
        env_enum = Environment(environment.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported environment: {environment!r}") from exc

    try:
        mode_enum = ValidationMode(validation_mode.lower())
    except ValueError as exc:
        raise ValueError(f"Unsupported validation_mode: {validation_mode!r}") from exc

    return DEFAULT_PROFILES[(env_enum, mode_enum)]


# ---------------------------------------------------------------------------
# Extension Point
# ---------------------------------------------------------------------------


class ThresholdSource:
    def load(self) -> Tuple[MetricThreshold, ...]:  # pragma: no cover
        raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO (based on Open Questions)
# ---------------------------------------------------------------------------

# TODO: Clarify whether `metric` in MetricThreshold must map to Level 3 metric IDs.
# TODO: Define precedence rules between MetricThreshold vs ThresholdProfile when both apply.
# TODO: Determine expected behavior for TimingThresholds.enabled when disabled (ignore vs nullify).
# TODO: Clarify injection and lifecycle model for concrete ThresholdSource implementations.
# TODO: Decide whether ValidationMode.STRICT should subsume WARN thresholds or remain mutually exclusive.


# ---------------------------------------------------------------------------
# Deferred for later phase
# ---------------------------------------------------------------------------

# - Consider enumeration or schema constraints for aggregation_scope/window.
# - Consider replacement of dual threshold models with unified enforcement stack.
# - Consider external configuration loading integration and governance hooks.

