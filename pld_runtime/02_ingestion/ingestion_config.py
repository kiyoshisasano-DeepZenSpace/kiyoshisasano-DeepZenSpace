#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.ingestion.ingestion_config (v1.1 Canonical Edition)

Concept
-------
Central configuration model for ingestion pipelines.

This module defines:

- how raw sources (logs, datasets, APIs) are described
- how they should be normalized into NormalizedTurn
- which adapters should be used for each source kind

It does NOT perform any I/O or parsing by itself.
Concrete ingestion logic lives in:

    - normalization.py
    - multiwoz_loader.py
    - source_*_*.py (adapters)

Procedure
---------
1. Choose an IngestionSourceKind (dataset, live_runtime, batch_export, etc.).
2. Optionally specify which adapter module/function to use.
3. Configure role/session mapping policies.
4. Pass IngestionConfig into ingestion orchestration code.

Implementation
--------------
This file only contains dataclasses, enums, and protocols describing
configuration. It is intentionally framework-agnostic and side-effect free.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, Optional, TypedDict, Protocol, Iterable

from ..detection.runtime_signal_bridge import NormalizedTurn


# ---------------------------------------------------------------------------
# Source kinds
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
    """

    DATASET = "dataset"
    LIVE_RUNTIME = "live_runtime"
    BATCH_EXPORT = "batch_export"
    SYNTHETIC = "synthetic"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Adapter protocol
# ---------------------------------------------------------------------------

class DialogIterator(Protocol):
    """
    Protocol for adapter functions that yield dialogs as lists of NormalizedTurn.

    Implementations may read from files, APIs, or in-memory objects,
    but the interface remains simple:

        -> Iterable[list[NormalizedTurn]]
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Iterable[list[NormalizedTurn]]:  # pragma: no cover - protocol
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
    """

    module: str
    function: str
    kwargs: Dict[str, Any]


# ---------------------------------------------------------------------------
# IngestionConfig model
# ---------------------------------------------------------------------------

@dataclass
class IngestionConfig:
    """
    Configuration for a single ingestion pipeline.

    Fields
    ------
    name:
        Human-readable identifier (used in logs / reports).

    source_kind:
        High-level source classification.

    adapter:
        Optional adapter specification describing how to obtain dialogs.

    session_id_field:
        Default key to use when deriving session IDs from dataset-like objects.

    role_field:
        Default key for roles in dataset-like objects.

    text_field:
        Default key for text content in dataset-like objects.

    runtime_prefix:
        Prefix for inferring runtime_* fields in dataset-like dicts.

    extra_metadata:
        Arbitrary metadata attached to this config.
        Useful for tracking dataset version, split, tags, etc.
    """

    name: str = "default"
    source_kind: IngestionSourceKind = IngestionSourceKind.UNKNOWN

    adapter: Optional[AdapterSpec] = None

    session_id_field: str = "dialog_id"
    role_field: str = "role"
    text_field: str = "text"
    runtime_prefix: str = "runtime_"

    extra_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this configuration as a plain dictionary with a stable shape.
        Enum values are represented by their underlying string values.
        """
        data = asdict(self)
        data["source_kind"] = self.source_kind.value
        return data


# ---------------------------------------------------------------------------
# Convenience presets
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
    """
    adapter: AdapterSpec = {
        "module": "pld_runtime.ingestion.multiwoz_loader",
        "function": "iter_multiwoz_corpus",
    }
    if corpus_path is not None:
        adapter["kwargs"] = {"path": corpus_path}

    meta = dict(extra_metadata or {})
    meta.setdefault("family", "multiwoz")

    return IngestionConfig(
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
    """
    meta = dict(extra_metadata or {})
    meta.setdefault("family", "synthetic")
    return IngestionConfig(
        name=name,
        source_kind=IngestionSourceKind.SYNTHETIC,
        extra_metadata=meta,
    )


__all__ = [
    "IngestionSourceKind",
    "DialogIterator",
    "AdapterSpec",
    "IngestionConfig",
    "make_multiwoz_config",
    "make_synthetic_config",
]
