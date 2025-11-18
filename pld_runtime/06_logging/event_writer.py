#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.event_writer (v1.1 Canonical Edition)

Thin abstraction layer for writing structured PLD records to sinks.

This module focuses on *how to emit a dict record*:

    record: Dict[str, Any]  →  sink (file / stdout / custom handler)

It is intentionally minimal:

- no knowledge of PLD internals or phases
- no schema validation (see enforcement.schema_validator)
- no retry / backoff
- no queueing

Higher layers (StructuredLogger, controllers, exporters/*) handle:

- adherence to pld_event.schema.json / runtime_event_envelope.json
- PLD phase/code semantics (Drift → Repair → Reentry → Outcome)
- batching, buffering, and transport

This layer only implements concrete "writers".
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Protocol


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------

class EventWriter(Protocol):
    """
    Generic protocol for event writers.

    Any callable matching this Protocol can be used as a writer:

        def writer(record: Dict[str, Any]) -> None:
            ...

    Typical records are either:

        - PLD events (pld_event.schema.json)
        - Runtime envelopes (runtime_event_envelope.json)

    StructuredLogger and controllers accept this interface.
    """

    def __call__(self, record: Dict[str, Any]) -> None:  # pragma: no cover - protocol
        ...


# ---------------------------------------------------------------------------
# In-memory writer (useful for tests)
# ---------------------------------------------------------------------------

@dataclass
class MemoryWriter:
    """
    Store records in memory. Intended for tests and small demos.

    Attributes
    ----------
    records:
        List of emitted records (dicts). Can be inspected by callers.
    """

    records: list[Dict[str, Any]]

    def __init__(self) -> None:
        self.records = []

    def __call__(self, record: Dict[str, Any]) -> None:
        self.records.append(record)

    def clear(self) -> None:
        self.records.clear()


# ---------------------------------------------------------------------------
# JSONL file writer
# ---------------------------------------------------------------------------

@dataclass
class JsonlFileWriter:
    """
    JSON Lines writer: one JSON object per line.

    Parameters
    ----------
    path:
        Target file path.

    append:
        If True (default), append to the file.
        If False, truncate file on first use.

    ensure_ascii:
        Passed through to json.dumps.

    auto_flush:
        If True, flush stream after each write.
    """

    path: Path
    append: bool = True
    ensure_ascii: bool = False
    auto_flush: bool = True

    _file: Optional[Any] = None
    _opened_mode: Optional[str] = None

    def __post_init__(self) -> None:
        self.path = Path(self.path)

    def __call__(self, record: Dict[str, Any]) -> None:
        if self._file is None:
            mode = "a" if self.append else "w"
            self._file = self.path.open(mode, encoding="utf-8")
            self._opened_mode = mode
        line = json.dumps(record, ensure_ascii=self.ensure_ascii)
        self._file.write(line + "\n")
        if self.auto_flush:
            self._file.flush()

    def close(self) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None
            self._opened_mode = None


def make_jsonl_file_writer(
    path: str | Path,
    *,
    append: bool = True,
    ensure_ascii: bool = False,
    auto_flush: bool = True,
) -> JsonlFileWriter:
    """
    Convenience constructor for a JsonlFileWriter.
    """
    return JsonlFileWriter(
        path=Path(path),
        append=append,
        ensure_ascii=ensure_ascii,
        auto_flush=auto_flush,
    )


# ---------------------------------------------------------------------------
# Stream / stdout writer
# ---------------------------------------------------------------------------

@dataclass
class StreamWriter:
    """
    Write JSON lines to a text stream (e.g., stdout, stderr).

    Parameters
    ----------
    stream:
        File-like object with a .write(str) method.
        Default: sys.stdout

    Notes
    -----
    This is commonly used in:

        - local debugging (PLD events to console)
        - container logs (stdout/stderr collectors)
        - simple evaluation scripts
    """

    stream: Any = sys.stdout
    ensure_ascii: bool = False
    auto_flush: bool = True

    def __call__(self, record: Dict[str, Any]) -> None:
        line = json.dumps(record, ensure_ascii=self.ensure_ascii)
        self.stream.write(line + "\n")
        if self.auto_flush and hasattr(self.stream, "flush"):
            self.stream.flush()


def make_stdout_writer(
    *,
    ensure_ascii: bool = False,
    auto_flush: bool = True,
) -> StreamWriter:
    """
    Convenience constructor for a StreamWriter bound to stdout.
    """
    return StreamWriter(stream=sys.stdout, ensure_ascii=ensure_ascii, auto_flush=auto_flush)


def make_stderr_writer(
    *,
    ensure_ascii: bool = False,
    auto_flush: bool = True,
) -> StreamWriter:
    """
    Convenience constructor for a StreamWriter bound to stderr.
    """
    return StreamWriter(stream=sys.stderr, ensure_ascii=ensure_ascii, auto_flush=auto_flush)


# ---------------------------------------------------------------------------
# Adapter for custom callables
# ---------------------------------------------------------------------------

def wrap_callable(func: Callable[[Dict[str, Any]], None]) -> EventWriter:
    """
    Wrap an arbitrary callable as an EventWriter.

    This exists mainly to make typings explicit; at runtime it is a no-op.

    Example
    -------
    >>> def send_to_bus(record: Dict[str, Any]) -> None:
    ...     publish("pld-events", record)
    ...
    >>> writer = wrap_callable(send_to_bus)
    >>> writer({"event_id": "...", "pld": {...}})
    """
    def _wrapped(record: Dict[str, Any]) -> None:
        func(record)
    return _wrapped  # type: ignore[return-value]


__all__ = [
    "EventWriter",
    "MemoryWriter",
    "JsonlFileWriter",
    "make_jsonl_file_writer",
    "StreamWriter",
    "make_stdout_writer",
    "make_stderr_writer",
    "wrap_callable",
]
