"""
# version: 2.0
# status: runtime
# authority: Level 5 — runtime implementation (consumes Level 1–3 specifications)
# purpose: Validates PLD runtime event envelopes against schema, matrix, and transport rules.
# scope: Applies envelope rules, transport mapping checks, and Level 1–3 schema/matrix constraints without modification.
# dependencies: Level 1 PLD event schema; Level 2 event matrix; Level 3 metrics/operational rules; Level 5 runtime event envelope.
# change_classification: runtime-only, non-breaking (validator-layer behavior only)
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

# External dependencies:
# - jsonschema (Draft 7)
# - PyYAML (for event_matrix_schema.yaml.txt), if you choose to load from disk.
#
# This template is written so that you MAY inject pre-parsed schema/matrix objects
# instead of doing any I/O here, which is generally preferred for production runtimes.

try:
    from jsonschema import Draft7Validator, ValidationError
except Exception:  # pragma: no cover - optional dependency wiring
    Draft7Validator = None  # type: ignore[assignment]
    ValidationError = Exception  # type: ignore[assignment]


Json = Mapping[str, Any]
MutableJson = MutableMapping[str, Any]
JsonPath = Tuple[Union[str, int], ...]


class ValidationMode(str, Enum):
    """
    Validation mode MUST be one of: strict | warn | normalize.

    Semantics align with Level 2 / Level 3 validation_modes:

      - strict:
          must_violations: reject
          should_violations: ignore
      - warn:
          must_violations: reject
          should_violations: warn
      - normalize:
          must_violations: normalize (when unambiguous) else reject
          should_violations: warn_or_accept

    This enum is intentionally minimal; do NOT add modes without governance.
    """

    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"


class IssueSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class IssueDomain(str, Enum):
    SCHEMA = "schema"
    SEMANTIC = "semantic"
    ENVELOPE = "envelope"


@dataclass
class ValidationIssue:
    """
    Structured representation of a single validation issue.

    - code: stable machine-consumable identifier
    - message: human-readable explanation
    - path: JSON path into the validated object (JSON Pointer–like)
    - severity: error|warning|info
    - domain: schema|semantic|envelope
    - rule: optional reference to a Level 1/2/3 rule identifier
    """

    code: str
    message: str
    path: JsonPath
    severity: IssueSeverity
    domain: IssueDomain
    rule: Optional[str] = None

    def is_error(self) -> bool:
        return self.severity == IssueSeverity.ERROR


@dataclass
class EventValidationResult:
    """
    Result of validating a single PLD event (without the outer envelope).

    - event: possibly normalized event (always present)
    - mode: validation mode used
    - issues: list of issues encountered
    - normalized: True if any in-place correction was applied (normalize mode)
    - valid: True if no ERROR-severity issues remain
    """

    event: MutableJson
    mode: ValidationMode
    issues: List[ValidationIssue]
    normalized: bool

    @property
    def valid(self) -> bool:
        return not any(i.is_error() for i in self.issues)


@dataclass
class EnvelopeValidationResult:
    """
    Result of validating the runtime transport envelope plus nested event.

    - envelope: possibly normalized envelope
    - event_result: validation result for the nested event
    - issues: envelope-specific issues; event issues are in event_result
    - valid: True if envelope and event are both valid
    """

    envelope: MutableJson
    event_result: EventValidationResult
    issues: List[ValidationIssue]

    @property
    def valid(self) -> bool:
        if not self.event_result.valid:
            return False
        return not any(i.is_error() for i in self.issues)


@dataclass
class PLDSpecContext:
    """
    Aggregated view of the PLD specification, supplied at runtime.

    Prefer injecting fully-parsed JSON/YAML objects rather than doing I/O in this module.

    Fields:
      - event_schema: Level 1 JSON Schema for PLD events
      - event_matrix: Level 2 machine-readable event matrix
      - envelope_schema: Level 5 JSON Schema for the runtime envelope (optional)
    """

    event_schema: Json
    event_matrix: Json
    envelope_schema: Optional[Json] = None


class PLDValidator:
    """
    PLD-aware validator that:

      1. Applies Level 1 JSON Schema validation to events.
      2. Applies Level 2 Event Matrix semantics (prefix/phase, event_type/phase).
      3. Applies Level 5 envelope validation and session_id consistency.
      4. Implements mode-dependent behavior (strict, warn, normalize) without
         rewriting or inferring new schema/matrix structure.

    This class MUST NOT mutate the supplied schema/matrix context.
    """

    def __init__(self, spec: PLDSpecContext) -> None:
        if Draft7Validator is None:
            raise RuntimeError(
                "jsonschema.Draft7Validator is not available. "
                "Install `jsonschema` or inject a compatible validator."
            )

        self._spec = spec
        self._event_validator = Draft7Validator(spec.event_schema)
        self._envelope_validator = (
            Draft7Validator(spec.envelope_schema) if spec.envelope_schema is not None else None
        )

        # Precompute semantic maps from the event matrix.
        em = spec.event_matrix

        # TODO: Review required (uncertain alignment)
        # Event Matrix structure contract:
        # - Current implementation assumes spec.event_matrix is a flat mapping
        #   with keys like "valid_phases", "prefix_to_phase", "must_phase_map",
        #   "should_phase_map", "may_events", "validation_modes".
        # - Consider validating the structure of event_matrix or introducing a
        #   TypedDict / schema for the matrix itself to avoid runtime crashes
        #   if the upstream YAML structure changes.

        # Valid phases (Level 2) – used for sanity checks.
        self._valid_phases = set(em.get("valid_phases", []))

        # Lifecycle prefix → phase constraints (Level 2, prefix_to_phase).
        self._prefix_to_phase: Dict[str, str] = dict(em.get("prefix_to_phase", {}))

        # phase="none" policy (Level 2).
        self._none_phase_policy = em.get("none_phase_policy", {}) or {}

        # MUST mappings: event_type → phase
        self._must_phase_map: Dict[str, str] = dict(em.get("must_phase_map", {}))

        # SHOULD mappings: event_type → phase
        self._should_phase_map: Dict[str, str] = dict(em.get("should_phase_map", {}))

        # MAY-level event list (semantics are permissive; no direct constraint).
        self._may_events: Sequence[str] = tuple(em.get("may_events", []) or [])

        # Validation mode semantics from matrix/metrics. We do not re-encode them
        # exhaustively here; instead we implement a minimal, conservative behavior
        # aligned with the narrative specs.
        self._validation_modes_config: Json = em.get("validation_modes", {})

    # -------------------------------------------------------------------------
    # Public API
    # -------------------------------------------------------------------------

    def validate_event(
        self,
        event: Mapping[str, Any],
        mode: ValidationMode = ValidationMode.STRICT,
    ) -> EventValidationResult:
        """
        Validate a single PLD event against:

          - Level 1 JSON Schema (hard invariant).
          - Level 2 Event Matrix semantics (prefix/phase & event_type/phase).

        In NORMALIZE mode, limited, conservative normalization is allowed where:

          - The correct phase can be uniquely inferred from event_type (MUST map).
          - The correct phase can be uniquely inferred from lifecycle prefix.
          - No conflict exists between those two sources of truth.

        This function never mutates the input mapping; it operates on a deep copy.
        """
        working_event: MutableJson = copy.deepcopy(event)
        issues: List[ValidationIssue] = []

        # 1. Structural schema validation (Level 1).
        issues.extend(self._run_schema_validation(working_event))

        # If schema invalid, we do not trust structure enough to normalize; exit early.
        if any(i.is_error() for i in issues):
            return EventValidationResult(
                event=working_event,
                mode=mode,
                issues=issues,
                normalized=False,
            )

        # 2. Semantic validation & optional normalization (Level 2).
        normalized = self._run_semantic_validation(working_event, mode, issues)

        return EventValidationResult(
            event=working_event,
            mode=mode,
            issues=issues,
            normalized=normalized,
        )

    def validate_envelope(
        self,
        envelope: Mapping[str, Any],
        mode: ValidationMode = ValidationMode.STRICT,
        validate_nested_event: bool = True,
    ) -> EnvelopeValidationResult:
        """
        Validate a runtime envelope plus its nested PLD event.

        Behavior:

          1. Optionally validate `envelope` against the Level 5 envelope schema.
          2. Validate the nested `event` using validate_event().
          3. Enforce the session_id consistency rule:

               envelope.session.session_id == event.session_id

             as described by x-validation/session_id_consistency in
             runtime_event_envelope.json.

        The input envelope is deep-copied; neither the original envelope nor the
        original nested event is mutated by this function.
        """
        working_env: MutableJson = copy.deepcopy(envelope)
        issues: List[ValidationIssue] = []

        # 1. Envelope structural validation (Level 5).
        issues.extend(self._run_envelope_schema_validation(working_env))

        # 2. Nested event extraction.
        raw_event = working_env.get("event", {})
        if not isinstance(raw_event, Mapping):
            issues.append(
                ValidationIssue(
                    code="ENVELOPE_EVENT_TYPE",
                    message="envelope.event MUST be an object.",
                    path=("event",),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.ENVELOPE,
                    rule="runtime_envelope.event_object",
                )
            )
            # If event is not an object, there is nothing sensible to validate further.
            dummy_result = EventValidationResult(
                event={},
                mode=mode,
                issues=[],
                normalized=False,
            )
            return EnvelopeValidationResult(
                envelope=working_env,
                event_result=dummy_result,
                issues=issues,
            )

        # 3. Nested event validation.
        if validate_nested_event:
            event_result = self.validate_event(raw_event, mode=mode)
            # Replace possibly-normalized event back into envelope.
            working_env["event"] = event_result.event
        else:
            # No validation; wrap raw event.
            event_result = EventValidationResult(
                event=copy.deepcopy(raw_event),
                mode=mode,
                issues=[],
                normalized=False,
            )

        # 4. session_id consistency rule (x-validation in runtime_event_envelope.json).
        self._check_session_consistency(
            working_env,
            event_result.event,
            issues,
        )

        return EnvelopeValidationResult(
            envelope=working_env,
            event_result=event_result,
            issues=issues,
        )

    # -------------------------------------------------------------------------
    # Internal helpers: Level 1 — schema validation
    # -------------------------------------------------------------------------

    def _run_schema_validation(self, event: MutableJson) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []

        for error in self._event_validator.iter_errors(event):
            path = tuple(error.path)  # type: ignore[arg-type]
            issues.append(
                ValidationIssue(
                    code="SCHEMA_ERROR",
                    message=str(error.message),
                    path=path,
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.SCHEMA,
                    rule="pld_event.schema",
                )
            )

        return issues

    # -------------------------------------------------------------------------
    # Internal helpers: Level 5 — envelope schema validation
    # -------------------------------------------------------------------------

    def _run_envelope_schema_validation(self, envelope: MutableJson) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []

        if self._envelope_validator is None:
            # Envelope schema is optional for some deployments.
            return issues

        for error in self._envelope_validator.iter_errors(envelope):
            path = tuple(error.path)  # type: ignore[arg-type]
            issues.append(
                ValidationIssue(
                    code="ENVELOPE_SCHEMA_ERROR",
                    message=str(error.message),
                    path=path,
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.ENVELOPE,
                    rule="runtime_event_envelope.schema",
                )
            )

        return issues

    # -------------------------------------------------------------------------
    # Internal helpers: Level 2 — semantic validation & normalization
    # -------------------------------------------------------------------------

    def _run_semantic_validation(
        self,
        event: MutableJson,
        mode: ValidationMode,
        issues: List[ValidationIssue],
    ) -> bool:
        """
        Apply semantic rules from the Event Matrix:

          - Prefix ↔ phase consistency.
          - event_type ↔ phase mappings (MUST / SHOULD).

        May perform limited normalization in NORMALIZE mode. Returns True if any
        normalization was applied.
        """
        normalized = False

        event_type = str(event.get("event_type", ""))
        pld_obj = event.get("pld", {})
        if not isinstance(pld_obj, Mapping):
            # This should already be caught by schema, but we guard defensively.
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_PLD_TYPE",
                    message="pld MUST be an object.",
                    path=("pld",),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.SEMANTIC,
                    rule="event_matrix.pld_object",
                )
            )
            return normalized

        phase = str(pld_obj.get("phase", ""))
        code = str(pld_obj.get("code", ""))

        # 1. Prefix ↔ phase rule (hard rule, Level 2).
        prefix = self._extract_prefix(code)
        normalized |= self._check_and_maybe_normalize_prefix_phase(
            event,
            mode,
            prefix,
            phase,
            issues,
        )
        # Refresh phase after prefix-driven normalization.
        phase = str(event.get("pld", {}).get("phase", phase))

        # 2. event_type → phase MUST mapping.
        normalized |= self._check_and_maybe_normalize_must_phase(
            event,
            mode,
            event_type,
            phase,
            prefix,
            issues,
        )
        # Refresh phase again in case MUST-level normalization was applied.
        phase = str(event.get("pld", {}).get("phase", phase))

        # 3. event_type → phase SHOULD mapping.
        self._check_should_phase(
            event_type,
            phase,
            issues,
            mode,
        )

        # NOTE: MAY events are intentionally not constrained here.
        # They are allowed in any phase as per the matrix.

        return normalized

    def _extract_prefix(self, code: str) -> Optional[str]:
        """
        Extract lifecycle or non-lifecycle prefix from pld.code.

        The canonical rule from the semantic docs is:

          Prefix = <characters before first "_"> minus trailing digits.

        Example:
          "D4_tool_error" → "D"

        We apply this rule, then check if the resulting prefix matches any known
        lifecycle prefix in prefix_to_phase. Non-lifecycle prefixes are returned
        as-is (for phase="none" policy checks).
        """
        if not code:
            return None

        head = code.split("_", 1)[0]
        # Strip trailing digits
        i = len(head)
        while i > 0 and head[i - 1].isdigit():
            i -= 1
        prefix = head[:i] or head

        return prefix or None

    def _check_and_maybe_normalize_prefix_phase(
        self,
        event: MutableJson,
        mode: ValidationMode,
        prefix: Optional[str],
        phase: str,
        issues: List[ValidationIssue],
    ) -> bool:
        """
        Enforce lifecycle prefix/phase consistency and phase="none" policy.

        Rules:

          - If prefix ∈ prefix_to_phase:
                phase MUST match prefix_to_phase[prefix].
          - If phase == "none":
                lifecycle prefixes (D/R/RE/C/O/F) MUST NOT be used.

        In NORMALIZE mode, we may correct phase when prefix uniquely determines it.
        """
        normalized = False
        if not prefix:
            return normalized

        # Lifecycle prefix handling
        if prefix in self._prefix_to_phase:
            expected_phase = self._prefix_to_phase[prefix]
            if phase != expected_phase:
                message = (
                    f"Lifecycle prefix '{prefix}' requires phase='{expected_phase}', "
                    f"found phase='{phase}'."
                )
                if mode == ValidationMode.NORMALIZE and phase in self._valid_phases:
                    # Safe normalization: correct phase to the prefix-driven phase.
                    self._set_pld_phase(event, expected_phase)
                    issues.append(
                        ValidationIssue(
                            code="SEMANTIC_PREFIX_PHASE_NORMALIZED",
                            message=message + " Normalized phase to match prefix.",
                            path=("pld", "phase"),
                            severity=IssueSeverity.WARNING,
                            domain=IssueDomain.SEMANTIC,
                            rule="event_matrix.prefix_to_phase",
                        )
                    )
                    normalized = True
                else:
                    issues.append(
                        ValidationIssue(
                            code="SEMANTIC_PREFIX_PHASE_MISMATCH",
                            message=message,
                            path=("pld", "phase"),
                            severity=IssueSeverity.ERROR,
                            domain=IssueDomain.SEMANTIC,
                            rule="event_matrix.prefix_to_phase",
                        )
                    )
        else:
            # Non-lifecycle prefix under phase != "none" is allowed by the schema,
            # but we must respect the phase="none" policy.
            if phase == "none":
                # Non-lifecycle prefix with phase="none" is valid.
                return normalized

            # For phase != "none" and non-lifecycle prefix, the matrix does not
            # impose a hard prohibition. We record an informational issue only.
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_NON_LIFECYCLE_PREFIX_WITH_PHASE",
                    message=(
                        f"Non-lifecycle prefix '{prefix}' used with phase='{phase}'. "
                        "This is structurally allowed but SHOULD be reviewed for "
                        "semantic consistency."
                    ),
                    path=("pld", "code"),
                    severity=IssueSeverity.INFO,
                    domain=IssueDomain.SEMANTIC,
                    rule="event_matrix.none_phase_policy",
                )
            )

        # phase="none" MUST NOT use lifecycle prefixes, per none_phase_policy.
        allow_lifecycle = bool(self._none_phase_policy.get("allow_lifecycle_prefixes", False))
        if phase == "none" and prefix in self._prefix_to_phase and not allow_lifecycle:
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_NONE_PHASE_LIFECYCLE_PREFIX",
                    message=(
                        f"phase='none' MUST NOT use lifecycle prefix '{prefix}'. "
                        "Use non-lifecycle prefixes (e.g., INFO_*, META_*, SYS_*)."
                    ),
                    path=("pld", "code"),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.SEMANTIC,
                    rule="event_matrix.none_phase_policy",
                )
            )

        return normalized

    def _check_and_maybe_normalize_must_phase(
        self,
        event: MutableJson,
        mode: ValidationMode,
        event_type: str,
        phase: str,
        prefix: Optional[str],
        issues: List[ValidationIssue],
    ) -> bool:
        """
        Enforce MUST-level event_type → phase mapping.

        In NORMALIZE mode, we may correct phase when:

          - event_type has a MUST map in must_phase_map, AND
          - the target phase is unambiguous, AND
          - it does not conflict with lifecycle prefix requirements.
        """
        normalized = False

        if not event_type:
            return normalized

        if event_type not in self._must_phase_map:
            return normalized

        expected_phase = self._must_phase_map[event_type]
        if phase == expected_phase:
            return normalized

        # Check potential conflict with lifecycle prefix.
        if prefix in self._prefix_to_phase:
            prefix_phase = self._prefix_to_phase[prefix]
            if prefix_phase != expected_phase:
                # Irreconcilable conflict between event_type and prefix.
                issues.append(
                    ValidationIssue(
                        code="SEMANTIC_EVENTTYPE_PREFIX_PHASE_CONFLICT",
                        message=(
                            f"event_type '{event_type}' requires phase='{expected_phase}', "
                            f"but lifecycle prefix '{prefix}' requires phase='{prefix_phase}'."
                        ),
                        path=("pld", "phase"),
                        severity=IssueSeverity.ERROR,
                        domain=IssueDomain.SEMANTIC,
                        rule="event_matrix.must_phase_map + prefix_to_phase",
                    )
                )
                return normalized

        message = (
            f"event_type '{event_type}' MUST use phase='{expected_phase}', "
            f"found phase='{phase}'."
        )

        if mode == ValidationMode.NORMALIZE:
            # Safe normalization: adjust phase to the MUST-mapped phase.
            self._set_pld_phase(event, expected_phase)
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_EVENTTYPE_PHASE_NORMALIZED",
                    message=message + " Normalized phase to match event_type.",
                    path=("pld", "phase"),
                    severity=IssueSeverity.WARNING,
                    domain=IssueDomain.SEMANTIC,
                    rule="event_matrix.must_phase_map",
                )
            )
            normalized = True
        else:
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_EVENTTYPE_PHASE_MISMATCH",
                    message=message,
                    path=("pld", "phase"),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.SEMANTIC,
                    rule="event_matrix.must_phase_map",
                )
            )

        return normalized

    def _check_should_phase(
        self,
        event_type: str,
        phase: str,
        issues: List[ValidationIssue],
        mode: ValidationMode,
    ) -> None:
        """
        Enforce SHOULD-level event_type → phase mappings.

        Behavior:

          - strict:
                SHOULD violations are ignored (no issue).
          - warn / normalize:
                SHOULD violations emit WARNING-level issues, but do not invalidate
                the event.

        No automatic normalization is performed here; that is left to higher-
        level logic if desired.
        """
        if event_type not in self._should_phase_map:
            return

        expected_phase = self._should_phase_map[event_type]
        if phase == expected_phase:
            return

        if mode == ValidationMode.STRICT:
            # As per Level 2/3, we ignore SHOULD violations in strict mode.
            return

        issues.append(
            ValidationIssue(
                code="SEMANTIC_EVENTTYPE_PHASE_SHOULD",
                message=(
                    f"event_type '{event_type}' SHOULD use phase='{expected_phase}', "
                    f"found phase='{phase}'."
                ),
                path=("pld", "phase"),
                severity=IssueSeverity.WARNING,
                domain=IssueDomain.SEMANTIC,
                rule="event_matrix.should_phase_map",
            )
        )

    def _set_pld_phase(self, event: MutableJson, phase: str) -> None:
        pld = event.setdefault("pld", {})
        if isinstance(pld, MutableMapping):
            pld["phase"] = phase

    # -------------------------------------------------------------------------
    # Internal helpers: Level 5 — session_id consistency
    # -------------------------------------------------------------------------

    def _check_session_consistency(
        self,
        envelope: MutableJson,
        event: MutableJson,
        issues: List[ValidationIssue],
    ) -> None:
        """
        Enforce:

          envelope.session.session_id == event.session_id

        as specified by x-validation/session_id_consistency in
        runtime_event_envelope.json.
        """
        session = envelope.get("session", {})
        if not isinstance(session, Mapping):
            # Non-object session is a schema concern; we treat here as envelope error.
            issues.append(
                ValidationIssue(
                    code="ENVELOPE_SESSION_TYPE",
                    message="envelope.session MUST be an object.",
                    path=("session",),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.ENVELOPE,
                    rule="runtime_envelope.session_object",
                )
            )
            return

        env_session_id = session.get("session_id")
        evt_session_id = event.get("session_id")

        if env_session_id is None or evt_session_id is None:
            # Missing fields should already be caught by schema, but we do not
            # duplicate that logic here.
            return

        if env_session_id != evt_session_id:
            issues.append(
                ValidationIssue(
                    code="ENVELOPE_SESSION_ID_MISMATCH",
                    message=(
                        "Envelope session.session_id MUST equal event.session_id "
                        f"(found '{env_session_id}' vs '{evt_session_id}')."
                    ),
                    path=("session", "session_id"),
                    severity=IssueSeverity.ERROR,
                    domain=IssueDomain.ENVELOPE,
                    rule="runtime_envelope.x-validation.session_id_consistency",
                )
            )


# -------------------------------------------------------------------------
# JSONL validation helper (merged from v1.1 behavior)
# -------------------------------------------------------------------------


def _issue_path_to_string(path: JsonPath) -> str:
    if not path:
        return "<root>"
    return ".".join(str(p) for p in path)


def validate_jsonl_file(
    path: Union[str, Path],
    validator: PLDValidator,
    *,
    envelope_mode: bool = False,
    mode: ValidationMode = ValidationMode.STRICT,
    error_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """
    Validate a JSONL file containing either bare PLD events or full runtime envelopes.

    Returns a summary dict:

    {
      "ok": bool,
      "total": int,
      "valid": int,
      "invalid": int,
      "errors": [ {line, path, message, code, severity, domain, rule}, ... ],
      "used_fallback": bool
    }

    If error_callback is provided, each error record will be passed to the callback
    instead of being accumulated in the returned "errors" list. This avoids unbounded
    memory growth when validating large corpora.

    # NOTE: Migration difference
    # - v1.1 used schema-only validation with optional fallback schemas.
    # - This version uses PLDValidator, which enforces both Level 1 (schema) and
    #   Level 2 (semantic matrix) rules and does NOT support fallback schemas.
    # - "used_fallback" is always False and preserved only for downstream compatibility.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))

    total = 0
    valid_count = 0
    invalid_count = 0
    errors: List[Dict[str, Any]] = []

    def _emit_error(record: Dict[str, Any]) -> None:
        if error_callback is not None:
            error_callback(record)
        else:
            errors.append(record)

    with p.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            total += 1
            try:
                obj = json.loads(line)
            except Exception as e:
                invalid_count += 1
                _emit_error(
                    {
                        "line": idx,
                        "path": "<parse>",
                        "message": f"Invalid JSON: {e}",
                        "code": "PARSE_ERROR",
                        "severity": IssueSeverity.ERROR.value,
                        "domain": IssueDomain.SCHEMA.value,
                        "rule": None,
                    }
                )
                continue

            if envelope_mode:
                result = validator.validate_envelope(obj, mode=mode)
                is_valid = result.valid
                issue_sources = list(result.issues) + list(result.event_result.issues)
            else:
                result = validator.validate_event(obj, mode=mode)
                is_valid = result.valid
                issue_sources = list(result.issues)

            if is_valid:
                valid_count += 1
            else:
                invalid_count += 1
                for issue in issue_sources:
                    if not issue.is_error():
                        continue
                    _emit_error(
                        {
                            "line": idx,
                            "path": _issue_path_to_string(issue.path),
                            "message": issue.message,
                            "code": issue.code,
                            "severity": issue.severity.value,
                            "domain": issue.domain.value,
                            "rule": issue.rule,
                        }
                    )

    return {
        "ok": invalid_count == 0,
        "total": total,
        "valid": valid_count,
        "invalid": invalid_count,
        "errors": errors,
        # NOTE: Migration difference
        # kept for structural compatibility with v1.1 summary payloads;
        # fallback schemas are no longer used in this implementation.
        "used_fallback": False,
    }


# Deferred for later phase
# - No additional Future-Stage Considerations have been integrated from the
#   current technical review. This block is reserved for future items once
#   they are formally recorded and prioritized.


