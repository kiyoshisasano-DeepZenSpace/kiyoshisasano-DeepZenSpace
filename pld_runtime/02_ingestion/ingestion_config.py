"""
# version: 2.0
# status: draft (runtime)
# authority: Level 5 — runtime implementation (consumes Level 1–3 specifications)
# purpose: Defines ingestion configuration for envelope rules, transport mapping, and adapter settings.
# scope: Provides governance-aligned defaults, legacy adapter compatibility, and immutable ingestion configuration.
# dependencies: Level 1 schema; Level 2 event matrix; Level 3 metrics rules; Level 5 runtime event envelope.
# change_classification: editorial + runtime-only (functional extension; migration-aligned)
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import (
    Any,
    Dict,
    Iterable,
    Mapping,
    MutableMapping,
    Optional,
    Protocol,
    TypedDict,
)

import os


# ---------------------------------------------------------------------------
# Validation modes
# ---------------------------------------------------------------------------


class ValidationMode(str, Enum):
    """
    Runtime validation modes.

    These MUST remain aligned with the tri-modal validation regime defined
    for PLD events and metrics:

      - strict
      - warn
      - normalize

    See:
      - docs/schemas/metrics_schema.yaml
      - docs/metrics/PLD_metrics_spec.md
    """

    STRICT = "strict"
    WARN = "warn"
    NORMALIZE = "normalize"


DEFAULT_VALIDATION_MODE: ValidationMode = ValidationMode.STRICT
"""
Default ingestion validation mode.

This default MUST be compatible with the metrics layer default_mode "strict".
# NOTE: Migration difference
#   - Legacy ingestion configurations that did not enforce strict validation
#     will now, by default, operate under strict structural + semantic checks. :contentReference[oaicite:4]{index=4}
"""


# ---------------------------------------------------------------------------
# Schema and matrix references (governance-aligned)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SchemaReference:
    """
    Immutable reference to a canonical schema or semantic mapping file.

    This type is intentionally minimal and does NOT attempt to interpret
    schema content; it only captures where the authoritative artefact is
    located and how it should be treated by the runtime.
    """

    id: str
    """Logical identifier (e.g., 'pld_event.schema.json')."""

    path: str
    """
    Filesystem path to the canonical file.

    IMPORTANT:
    - This is a locator only. The runtime MUST treat the target file as
      read-only and MUST NOT rewrite or normalize it.
    """

    authority_level: int
    """
    Governance authority level (1–5).

    Lower numbers indicate higher precedence:
      1 → structural schema (hard invariant)
      2 → semantic matrix
      3 → operational metrics / standards
      5 → runtime-only implementation
    """

    description: str = ""


@dataclass(frozen=True)
class EnvelopeRuleReference:
    """
    Reference to the runtime envelope schema and associated invariants.

    The envelope is a Level 5 construct that wraps a PLD event, which
    remains the source of truth for lifecycle semantics.
    """

    schema: SchemaReference
    enforce_session_id_consistency: bool = True
    """
    When True, ingestion MUST enforce:

        envelope.session.session_id == event.session_id

    as required by the envelope's x-validation block. :contentReference[oaicite:5]{index=5}
    """


# ---------------------------------------------------------------------------
# Source kinds and adapter definitions (legacy ingestion capability)
# ---------------------------------------------------------------------------


class IngestionSourceKind(str, Enum):
    """
    High-level classification of ingestion sources.

    dataset:
        Static corpora such as MultiWOZ, internal logs, CSV/JSON exports.

    live_runtime:
        Online logs streamed from a running agent system.

    batch_export:
        Periodic exports from production systems (nightly dumps, job outputs).

    synthetic:
        Generated dialogs/sequences for experiments or testing.

    unknown:
        Fallback when source is not clearly identified.

    # NOTE: Migration difference
    #   - Semantics unchanged from the legacy v1.1 ingestion config.
    """

    DATASET = "dataset"
    LIVE_RUNTIME = "live_runtime"
    BATCH_EXPORT = "batch_export"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


class IngestionItem(TypedDict):
    """
    Minimal item type for adapter output.

    Adapters are expected to produce dialogs as sequences of IngestionItem
    objects, which must at least provide the minimum fields required for
    downstream validation and normalization.

    Required:
      - text: textual content of the turn
      - role: speaker role label
      - session_id: logical session identifier

    Additional keys MAY be present (e.g., runtime_* fields, metadata) but
    are not explicitly typed here and SHOULD be handled via looser runtime
    validation or extended TypedDicts when needed.
    """

    text: str
    role: str
    session_id: str


class DialogIterator(Protocol):
    """
    Protocol for adapter functions that yield dialogs as lists of
    IngestionItem objects.

    Implementations may read from files, APIs, or in-memory objects,
    but the interface remains simple:

        -> Iterable[list[IngestionItem]]

    # TODO: Review required (adapter lifecycle management / runtime module loading safety)
    #   - Define where dynamic loading and signature checks are enforced to
    #     ensure adapter functions conform to DialogIterator at runtime and to
    #     fail early when return types are incompatible (e.g., list[str] only).
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Iterable[list[IngestionItem]]:  # pragma: no cover - protocol
        ...


class AdapterSpec(TypedDict, total=False):
    """
    Lightweight description of an ingestion adapter.

    Fields
    ------
    module:
        Python module path as string, e.g. "pld_runtime.ingestion.multiwoz_loader".

    function:
        Function name within the module, e.g. "iter_multiwoz_corpus".

    kwargs:
        Default keyword arguments to be passed when the adapter is invoked.

    # NOTE: Migration difference
    #   - The structure is identical to the legacy AdapterSpec, but it is now
    #     used in combination with governance-aware IngestionConfig.
    """

    module: str
    function: str
    kwargs: Dict[str, Any]


# ---------------------------------------------------------------------------
# Ingestion configuration model
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class IngestionValidationPolicy:
    """
    Aggregated ingestion-time validation policy.

    This policy is runtime-only and MUST NOT contradict Level 1–3 rules.
    It may narrow behavior (e.g., reject more events) but MUST NOT accept
    events that violate MUST-level constraints in the event schema or
    event matrix. :contentReference[oaicite:6]{index=6}

    # TODO: Review required (validation responsibility ownership)
    #   - Clarify which component enforces this policy in practice
    #     (e.g., ingestion orchestrator vs. individual adapters).
    """

    mode: ValidationMode = DEFAULT_VALIDATION_MODE

    validate_schema: bool = True
    """
    When True, every ingested PLD event MUST pass JSON Schema validation
    against the Level 1 event schema before any semantic checks.
    """

    validate_semantics: bool = True
    """
    When True, every ingested PLD event MUST be checked against the
    Level 2 event matrix (phase ↔ prefix and event_type ↔ phase rules).
    """

    validate_envelope: bool = True
    """
    When True, the runtime envelope MUST be validated (if present),
    including envelope-level structural checks plus any x-validation
    invariants such as session_id consistency.
    """

    drop_metrics_on_violation: bool = True
    """
    When True, events that fail MUST-level constraints MUST NOT
    contribute to metrics, consistent with strict / warn modes
    in the metrics schema. :contentReference[oaicite:7]{index=7}
    """


@dataclass(frozen=True)
class IngestionConfig:
    """
    Top-level ingestion configuration for the PLD runtime.

    This configuration is meant to be instantiated once at process
    startup and passed into ingestion / validation components.

    It also subsumes the legacy v1.1 "single ingestion pipeline"
    configuration by including source/adapter-related fields:

      - name
      - source_kind
      - adapter
      - session_id_field
      - role_field
      - text_field
      - runtime_prefix
      - extra_metadata

    # NOTE: Functional behavior change
    #   - IngestionConfig is now immutable (frozen=True).
    #   - Governance references are required for construction.
    """

    # Governance references (required, no defaults)
    pld_event_schema: SchemaReference
    event_matrix: SchemaReference
    metrics_schema: SchemaReference
    envelope_rules: EnvelopeRuleReference

    # Validation policy
    validation: IngestionValidationPolicy = field(
        default_factory=IngestionValidationPolicy
    )

    # Optional free-form configuration for environment-specific overrides.
    extra: Mapping[str, Any] = field(default_factory=dict)

    # Legacy ingestion fields (dataset / adapter configuration).
    name: str = "default"
    source_kind: IngestionSourceKind = IngestionSourceKind.UNKNOWN
    adapter: Optional[AdapterSpec] = None
    session_id_field: str = "dialog_id"
    role_field: str = "role"
    text_field: str = "text"
    runtime_prefix: str = "runtime_"
    extra_metadata: Mapping[str, Any] = field(default_factory=dict)

    def with_overrides(
        self,
        *,
        validation_mode: Optional[ValidationMode] = None,
        extra: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
        source_kind: Optional[IngestionSourceKind] = None,
        adapter: Optional[AdapterSpec] = None,
        session_id_field: Optional[str] = None,
        role_field: Optional[str] = None,
        text_field: Optional[str] = None,
        runtime_prefix: Optional[str] = None,
        extra_metadata: Optional[Mapping[str, Any]] = None,
    ) -> "IngestionConfig":
        """
        Return a new config instance with optional overrides.

        This helper is runtime-only and MUST NOT mutate the original
        configuration instance.

        # NOTE: Migration difference
        #   - Extends the original governance-only with_overrides() to also
        #     support legacy ingestion fields.
        """
        new_validation = (
            self.validation
            if validation_mode is None
            else IngestionValidationPolicy(
                mode=validation_mode,
                validate_schema=self.validation.validate_schema,
                validate_semantics=self.validation.validate_semantics,
                validate_envelope=self.validation.validate_envelope,
                drop_metrics_on_violation=self.validation.drop_metrics_on_violation,
            )
        )

        merged_extra: MutableMapping[str, Any] = dict(self.extra)
        if extra:
            merged_extra.update(extra)

        merged_extra_metadata: MutableMapping[str, Any] = dict(self.extra_metadata)
        if extra_metadata:
            merged_extra_metadata.update(extra_metadata)

        return IngestionConfig(
            pld_event_schema=self.pld_event_schema,
            event_matrix=self.event_matrix,
            metrics_schema=self.metrics_schema,
            envelope_rules=self.envelope_rules,
            validation=new_validation,
            extra=merged_extra,
            name=name if name is not None else self.name,
            source_kind=source_kind if source_kind is not None else self.source_kind,
            adapter=adapter if adapter is not None else self.adapter,
            session_id_field=(
                session_id_field
                if session_id_field is not None
                else self.session_id_field
            ),
            role_field=role_field if role_field is not None else self.role_field,
            text_field=text_field if text_field is not None else self.text_field,
            runtime_prefix=(
                runtime_prefix if runtime_prefix is not None else self.runtime_prefix
            ),
            extra_metadata=merged_extra_metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this configuration as a plain dictionary with a stable shape.

        # NOTE: Migration difference
        #   - This method generalizes the legacy to_dict() to include governance
        #     references and validation policy. Callers that only care about
        #     source-level fields SHOULD filter the result accordingly.
        """
        data = asdict(self)
        data["source_kind"] = self.source_kind.value
        data["validation_mode"] = self.validation.mode.value
        return data


# ---------------------------------------------------------------------------
# Path resolution helper
# ---------------------------------------------------------------------------


def _resolve_schema_path(relative: str) -> str:
    """
    Resolve a repository-relative schema path into an absolute filesystem path.

    Resolution strategy:
      1. If PLD_RUNTIME_ROOT is set, resolve relative to that directory.
      2. Otherwise, resolve relative to the repository root inferred from
         this file's location (two levels above pld_runtime/02_ingestion).

    # NOTE: Migration difference
    #   - Replaces hard-coded relative paths in load_default_ingestion_config()
    #     with a context-robust resolution strategy that tolerates non-root
    #     working directories.
    #
    # TODO: Review required (PLD_RUNTIME_ROOT semantics)
    #   - Clarify whether PLD_RUNTIME_ROOT is expected to point at a source
    #     checkout root or an installed package root, and how this interacts
    #     with packaging of docs/schemas in production environments.
    """
    root_env = os.getenv("PLD_RUNTIME_ROOT")
    if root_env:
        return str(Path(root_env) / relative)

    repo_root = Path(__file__).resolve().parents[2]
    return str(repo_root / relative)


# ---------------------------------------------------------------------------
# Default configuration factory
# ---------------------------------------------------------------------------


def load_default_ingestion_config() -> IngestionConfig:
    """
    Construct the default ingestion configuration.

    This function wires together Level 1–3 artefacts plus the Level 5
    runtime envelope schema. Paths are repository-relative and may be
    adapted by higher-level bootstrapping code (e.g. configuration or
    environment-specific resolvers).

    This function MUST NOT perform I/O; it only returns declarative
    configuration objects.
    """

    # Level 1 — Structural schema for PLD events (hard invariant). :contentReference[oaicite:8]{index=8}
    pld_event_schema = SchemaReference(
        id="pld_event.schema.json",
        path=_resolve_schema_path("docs/schemas/pld_event.schema.json"),
        authority_level=1,
        description="Hard invariant JSON Schema for PLD runtime events.",
    )

    # Level 2 — Event matrix (semantic rules). :contentReference[oaicite:9]{index=9}
    event_matrix = SchemaReference(
        id="event_matrix.yaml",
        path=_resolve_schema_path("docs/schemas/event_matrix.yaml"),
        authority_level=2,
        description="Normative mapping between event_type, phase, and prefixes.",
    )

    # Level 3 — Metrics schema (operational metrics layer). :contentReference[oaicite:10]{index=10}
    metrics_schema = SchemaReference(
        id="metrics_schema.yaml",
        path=_resolve_schema_path("docs/schemas/metrics_schema.yaml"),
        authority_level=3,
        description="Canonical metrics schema for PLD Runtime v2.0.",
    )

    # Level 5 — Runtime event envelope schema (transport wrapper). :contentReference[oaicite:11]{index=11}
    envelope_schema = SchemaReference(
        id="runtime_event_envelope.schema.json",
        path=_resolve_schema_path("pld_runtime/01_schemas/runtime_event_envelope.json"),
        authority_level=5,
        description="Runtime-only transport envelope for PLD events.",
    )

    envelope_rules = EnvelopeRuleReference(
        schema=envelope_schema,
        enforce_session_id_consistency=True,
    )

    validation = IngestionValidationPolicy(
        mode=DEFAULT_VALIDATION_MODE,
        validate_schema=True,
        validate_semantics=True,
        validate_envelope=True,
        drop_metrics_on_violation=True,
    )

    return IngestionConfig(
        pld_event_schema=pld_event_schema,
        event_matrix=event_matrix,
        metrics_schema=metrics_schema,
        envelope_rules=envelope_rules,
        validation=validation,
        extra={},
    )


# ---------------------------------------------------------------------------
# Convenience presets (merged from legacy ingestion_config)
# ---------------------------------------------------------------------------


def make_multiwoz_config(
    *,
    name: str = "multiwoz_2.x",
    corpus_path: Optional[str] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> IngestionConfig:
    """
    Create a preset IngestionConfig for MultiWOZ-style corpora.

    This assumes the presence of:

        pld_runtime.ingestion.multiwoz_loader.iter_multiwoz_corpus

    # NOTE: Migration difference
    #   - The returned config now includes governance references and validation
    #     policy from load_default_ingestion_config().
    """
    base = load_default_ingestion_config()

    adapter: AdapterSpec = {
        "module": "pld_runtime.ingestion.multiwoz_loader",
        "function": "iter_multiwoz_corpus",
    }
    if corpus_path is not None:
        adapter["kwargs"] = {"path": corpus_path}

    meta: Dict[str, Any] = dict(extra_metadata or {})
    meta.setdefault("family", "multiwoz")

    return base.with_overrides(
        name=name,
        source_kind=IngestionSourceKind.DATASET,
        adapter=adapter,
        session_id_field="dialogue_id",
        role_field="role",
        text_field="text",
        runtime_prefix="runtime_",
        extra_metadata=meta,
    )


def make_synthetic_config(
    *,
    name: str = "synthetic",
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> IngestionConfig:
    """
    Create a preset config for synthetic dialog generators.

    The actual generator must still be wired by the caller.

    # NOTE: Migration difference
    #   - The returned config now uses governance-aligned defaults from
    #     load_default_ingestion_config().
    """
    base = load_default_ingestion_config()

    meta: Dict[str, Any] = dict(extra_metadata or {})
    meta.setdefault("family", "synthetic")

    return base.with_overrides(
        name=name,
        source_kind=IngestionSourceKind.SYNTHETIC,
        extra_metadata=meta,
    )


# Deferred for later phase
#   - Packaging of non-Python artifacts (schemas, docs) into production
#     distributions (e.g., wheels), potentially via importlib.resources or
#     an equivalent resource-loader pattern to decouple schema access from
#     the source checkout layout.


__all__ = [
    "ValidationMode",
    "SchemaReference",
    "EnvelopeRuleReference",
    "IngestionValidationPolicy",
    "IngestionSourceKind",
    "IngestionItem",
    "DialogIterator",
    "AdapterSpec",
    "IngestionConfig",
    "load_default_ingestion_config",
    "make_multiwoz_config",
    "make_synthetic_config",
]



