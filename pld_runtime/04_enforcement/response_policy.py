"""
# version: 2.0.0
# status: runtime
# authority: Level 5 — runtime implementation
# purpose: Enforces PLD event validation and ingestion response policy.
# scope: Maps validation mode and violation set to enforcement decisions without modifying Level 1–3 assets.
# dependencies: Read-only Level 1–3 PLD event, event matrix, and metrics specifications.
# change_classification: runtime-only, non-breaking extension (assumes v2.0 event/matrix/metrics contracts)
"""

from __future__ import annotations

import enum
import logging
import os
from dataclasses import dataclass
from typing import Any, Callable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Validation Modes (Level 3-aligned)
# ---------------------------------------------------------------------------

class ValidationMode(str, enum.Enum):
    """
    PLD validation modes.
    """

    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"

    @classmethod
    def from_env(cls, value: Optional[str]) -> "ValidationMode":
        if not value:
            return cls.STRICT
        normalized = value.strip().lower()
        for mode in cls:
            if mode.value == normalized:
                return mode
        logger.warning(
            "Unknown PLD validation mode '%s'; falling back to 'strict'.",
            value,
        )
        return cls.STRICT


DEFAULT_VALIDATION_MODE: ValidationMode = ValidationMode.from_env(
    os.getenv("PLD_VALIDATION_MODE", "strict")
)


# ---------------------------------------------------------------------------
# Violation classification (runtime-only abstraction)
# ---------------------------------------------------------------------------

class ViolationKind(str, enum.Enum):
    """
    Runtime-only violation categorization.
    """

    SCHEMA = "schema"
    SEMANTIC_MUST = "semantic_must"
    SEMANTIC_SHOULD = "semantic_should"
    NORMALIZATION_ERROR = "normalization_error"
    RUNTIME_ERROR = "runtime_error"


@dataclass(frozen=True)
class Violation:
    kind: ViolationKind
    message: str
    code: Optional[str] = None
    details: Optional[Mapping[str, Any]] = None


# ---------------------------------------------------------------------------
# Policy decisions
# ---------------------------------------------------------------------------

class Decision(str, enum.Enum):
    ACCEPT = "accept"
    ACCEPT_WITH_WARNINGS = "accept_with_warnings"
    NORMALIZE_AND_ACCEPT = "normalize_and_accept"
    REJECT = "reject"


@dataclass
class PolicyResult:
    decision: Decision
    normalized_event: Optional[Mapping[str, Any]]
    violations: Sequence[Violation]
    warnings: Sequence[str]


Normalizer = Callable[
    [Mapping[str, Any], Sequence[Violation]],
    Tuple[Optional[Mapping[str, Any]], Sequence[Violation]],
]


class ResponsePolicy:
    """
    Enforcement policy for PLD event ingestion.
    """

    def __init__(
        self,
        mode: ValidationMode = DEFAULT_VALIDATION_MODE,
        normalizer: Optional[Normalizer] = None,
    ) -> None:
        self.mode = mode
        self._normalizer = normalizer

    def apply(
        self,
        event: Mapping[str, Any],
        violations: Sequence[Violation],
    ) -> PolicyResult:

        schema_violations = [v for v in violations if v.kind is ViolationKind.SCHEMA]
        if schema_violations:
            return self._reject_with(
                "Schema violation detected; rejecting event in all modes.",
                violations,
            )

        if self.mode is ValidationMode.STRICT:
            return self._apply_strict(event, violations)
        if self.mode is ValidationMode.WARN:
            return self._apply_warn(event, violations)
        if self.mode is ValidationMode.NORMALIZE:
            return self._apply_normalize(event, violations)

        fallback_violation = Violation(
            kind=ViolationKind.RUNTIME_ERROR,
            message=f"Unknown validation mode: {self.mode!r}",
        )
        return self._reject_with("Runtime configuration error.", violations + [fallback_violation])

    def _apply_strict(
        self,
        event: Mapping[str, Any],
        violations: Sequence[Violation],
    ) -> PolicyResult:

        must_violations = _filter_violations(violations, ViolationKind.SEMANTIC_MUST)
        if must_violations:
            return self._reject_with(
                "MUST-level semantic violation in strict mode.",
                violations,
            )

        should_violations = _filter_violations(violations, ViolationKind.SEMANTIC_SHOULD)
        warnings: List[str] = []
        if should_violations:
            warnings.append(
                "Event accepted in strict mode but contains SHOULD-level semantic violations."
            )

        return PolicyResult(
            decision=Decision.ACCEPT,
            normalized_event=None,
            violations=violations,
            warnings=warnings,
        )

    def _apply_warn(
        self,
        event: Mapping[str, Any],
        violations: Sequence[Violation],
    ) -> PolicyResult:

        must_violations = _filter_violations(violations, ViolationKind.SEMANTIC_MUST)
        if must_violations:
            return self._reject_with(
                "MUST-level semantic violation in warn mode.",
                violations,
            )

        should_violations = _filter_violations(violations, ViolationKind.SEMANTIC_SHOULD)
        warnings: List[str] = []
        if should_violations:
            warnings.append(
                "Event accepted with SHOULD-level semantic violations (warn mode)."
            )

        return PolicyResult(
            decision=Decision.ACCEPT_WITH_WARNINGS if warnings else Decision.ACCEPT,
            normalized_event=None,
            violations=violations,
            warnings=warnings,
        )

    def _apply_normalize(
        self,
        event: Mapping[str, Any],
        violations: Sequence[Violation],
    ) -> PolicyResult:

        must_violations = _filter_violations(violations, ViolationKind.SEMANTIC_MUST)

        if not must_violations:
            should = _filter_violations(violations, ViolationKind.SEMANTIC_SHOULD)
            warnings = ["Event accepted with SHOULD-level violations."] if should else []
            return PolicyResult(
                decision=Decision.ACCEPT_WITH_WARNINGS if warnings else Decision.ACCEPT,
                normalized_event=None,
                violations=violations,
                warnings=warnings,
            )

        if not self._normalizer:
            v = Violation(
                kind=ViolationKind.NORMALIZATION_ERROR,
                message="normalize mode configured but no normalizer provided; cannot normalize MUST violations.",
            )
            return self._reject_with("Normalization required but unavailable.", violations + [v])

        try:
            normalized_event, updated_violations = self._normalizer(event, violations)
        except Exception as exc:
            logger.exception("Error during normalization: %s", exc)
            v = Violation(
                kind=ViolationKind.RUNTIME_ERROR,
                message="Exception raised during normalization.",
                details={"exception": repr(exc)},
            )
            return self._reject_with("Normalization failed with runtime error.", violations + [v])

        if normalized_event is None:
            v = Violation(
                kind=ViolationKind.NORMALIZATION_ERROR,
                message="Normalizer unable to safely correct event.",
            )
            return self._reject_with("Normalization failed.", updated_violations + [v])

        # -------------------------------
        # CORE FIX #1 — verify MUST violations removed
        # -------------------------------
        remaining_must = _filter_violations(updated_violations, ViolationKind.SEMANTIC_MUST)
        if remaining_must:
            return self._reject_with(
                "Normalization incomplete — MUST violations remain.",
                updated_violations,
            )

        # -------------------------------
        # CORE FIX #2 — minimal schema revalidation safeguard
        # -------------------------------
        if not _schema_sanity_check(normalized_event):
            v = Violation(
                kind=ViolationKind.SCHEMA,
                message="Normalized event failed post-normalization schema safety check.",
            )
            return self._reject_with(
                "Schema violation after normalization.",
                updated_violations + [v],
            )

        warnings: List[str] = ["Event successfully normalized and accepted."]
        if _filter_violations(updated_violations, ViolationKind.SEMANTIC_SHOULD):
            warnings.append("Residual SHOULD-level semantic violations remain.")

        return PolicyResult(
            decision=Decision.NORMALIZE_AND_ACCEPT,
            normalized_event=normalized_event,
            violations=updated_violations,
            warnings=warnings,
        )

    def _reject_with(
        self,
        reason: str,
        violations: Sequence[Violation],
    ) -> PolicyResult:

        warnings = [reason]
        logger.debug("PLD event rejected: %s; violations=%r", reason, violations)
        return PolicyResult(
            decision=Decision.REJECT,
            normalized_event=None,
            violations=violations,
            warnings=warnings,
        )


def _filter_violations(
    violations: Sequence[Violation],
    kind: ViolationKind,
) -> List[Violation]:
    return [v for v in violations if v.kind is kind]


def _schema_sanity_check(event: Mapping[str, Any]) -> bool:
    """
    Minimal safety check — NOT a replacement for schema validation.

    Checks presence of required structural keys from Level 1 schema.

    This prevents downstream runtime crashes when normalization introduces
    malformed objects.

    This is intentionally lightweight and MUST NOT infer structure or modify content.
    """
    required_fields = {
        "schema_version",
        "event_id",
        "timestamp",
        "session_id",
        "turn_sequence",
        "source",
        "event_type",
        "pld",
        "payload",
        "ux",
    }
    return required_fields.issubset(event.keys())


def example_normalizer(
    event: Mapping[str, Any],
    violations: Sequence[Violation],
) -> Tuple[Optional[Mapping[str, Any]], Sequence[Violation]]:
    """
    Non-normative example normalizer — placeholder only.

    TODO: Must explicitly define whether returned violation list is:
          (a) full updated violation state or
          (b) unresolved delta only.
    """
    return dict(event), list(violations)


# ---------------------------------------------------------------------------
# Deferred for later phase
# ---------------------------------------------------------------------------
"""
- Possible split of ViolationKind.RUNTIME_ERROR into sub-categories.
- Evaluate whether config defaults must derive from metrics_schema.yaml
  instead of environment-based configuration.
- Define canonical Normalizer violation return format contract.
"""
