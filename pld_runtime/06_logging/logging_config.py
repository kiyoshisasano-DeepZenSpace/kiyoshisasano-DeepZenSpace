#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.logging_config

Configuration model and factory utilities for logging components.

This module defines how logging behavior is configured across runtime:

- global logging mode
- trace buffering strategy
- writer backend selection (stdout, jsonl, memory, custom)
- integration with StructuredLogger and SessionTraceBuffer

It does NOT:
- perform logging itself
- mutate runtime state automatically
- auto-detect environment (caller decides)

Intended usage pattern:

    from pld_runtime.logging.logging_config import (
        LoggingConfig,
        configure_logging,
    )

    cfg = LoggingConfig(
        mode="debug",
        writer="stdout",
        trace_retention="per_session",
        max_items_per_session=300,
    )

    logging_ctx = configure_logging(cfg)

    # then in runtime:
    logger = logging_ctx.logger
    buffer = logging_ctx.trace_buffer

This keeps logging pluggable yet standardized across environments.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, Literal, Optional

from .structured_logger import (
    StructuredLogger,
    LoggingMode,
)
from .event_writer import (
    make_stdout_writer,
    make_jsonl_file_writer,
    MemoryWriter,
    wrap_callable,
)
from .session_trace_buffer import (
    SessionTraceBuffer,
    SessionTraceBufferConfig,
    TraceRetentionPolicy,
)


# ---------------------------------------------------------------------------
# Allowed configuration values
# ---------------------------------------------------------------------------

WriterSelection = Literal[
    "stdout",
    "jsonl",
    "memory",
    "none",
    "custom_callable",
]


RetentionSelection = Literal[
    "unbounded",
    "per_session",
    "global_limit",
]


# ---------------------------------------------------------------------------
# Config Model
# ---------------------------------------------------------------------------

@dataclass
class LoggingConfig:
    """
    Declarative logging configuration for PLD runtime.

    Fields
    ------
    mode:
        LoggingMode enum value or string ("debug", "compact", "evaluation", "silent").

    writer:
        How logs should be emitted:
            - "stdout" → console output
            - "jsonl" → file-based JSONL records
            - "memory" → in-memory capture (test-friendly)
            - "none" → null output (silent)
            - "custom_callable" → user-supplied function

    writer_path:
        File path for jsonl mode (required if writer == "jsonl").

    trace_retention:
        Strategy for session_trace_buffer.

    max_items_per_session:
        Used when trace_retention == "per_session".

    max_total_items:
        Used when trace_retention == "global_limit".

    custom_writer:
        Optional callable to use when writer == "custom_callable".
    """

    mode: str | LoggingMode = "compact"
    writer: WriterSelection = "stdout"
    writer_path: Optional[str] = None

    trace_retention: RetentionSelection = "unbounded"
    max_items_per_session: int = 300
    max_total_items: int = 5000

    custom_writer: Optional[Any] = None  # must accept dict → None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Logger + Buffer Assembly
# ---------------------------------------------------------------------------

@dataclass
class LoggingContext:
    """
    Result of configure_logging(...).

    Contains instantiated components ready for runtime use:

        - logger
        - trace_buffer
    """

    logger: StructuredLogger
    trace_buffer: SessionTraceBuffer
    config: LoggingConfig

    def to_dict(self) -> Dict[str, Any]:
        return {
            "logger": repr(self.logger),
            "trace_buffer": f"<SessionTraceBuffer sessions={len(self.trace_buffer._traces)}>",
            "config": self.config.to_dict(),
        }


# ---------------------------------------------------------------------------
# Config Processing Helpers
# ---------------------------------------------------------------------------

def _resolve_mode(mode: str | LoggingMode) -> LoggingMode:
    if isinstance(mode, LoggingMode):
        return mode
    try:
        return LoggingMode(mode.lower())
    except Exception:
        return LoggingMode.COMPACT


def _resolve_writer(cfg: LoggingConfig):
    """Return an EventWriter based on config."""
    match cfg.writer:
        case "stdout":
            return make_stdout_writer()

        case "jsonl":
            if not cfg.writer_path:
                raise ValueError("logging_config: writer=jsonl requires writer_path.")
            return make_jsonl_file_writer(cfg.writer_path)

        case "memory":
            return MemoryWriter()

        case "none":
            return lambda rec: None

        case "custom_callable":
            if not callable(cfg.custom_writer):
                raise ValueError("logging_config: custom_writer must be a callable.")
            return wrap_callable(cfg.custom_writer)

        case _:
            raise ValueError(f"Unknown writer type: {cfg.writer}")


def _resolve_trace_buffer(cfg: LoggingConfig) -> SessionTraceBuffer:
    """Return configured SessionTraceBuffer instance."""

    retention_map = {
        "unbounded": TraceRetentionPolicy.UNBOUNDED,
        "per_session": TraceRetentionPolicy.PER_SESSION_LIMIT,
        "global_limit": TraceRetentionPolicy.GLOBAL_LIMIT,
    }

    policy = retention_map.get(cfg.trace_retention, TraceRetentionPolicy.UNBOUNDED)

    buffer_config = SessionTraceBufferConfig(
        retention_policy=policy,
        max_items_per_session=cfg.max_items_per_session,
        max_total_items=cfg.max_total_items,
    )

    return SessionTraceBuffer(config=buffer_config)


# ---------------------------------------------------------------------------
# Public Factory: configure_logging()
# ---------------------------------------------------------------------------

def configure_logging(cfg: LoggingConfig) -> LoggingContext:
    """
    Create a fully configured LoggingContext from LoggingConfig.

    - resolves logging mode
    - creates writer backend
    - instantiates structured logger
    - allocates session trace buffer

    Returns
    -------
    LoggingContext
    """

    mode = _resolve_mode(cfg.mode)
    writer = _resolve_writer(cfg)
    trace_buffer = _resolve_trace_buffer(cfg)

    logger = StructuredLogger(writer=writer, mode=mode)

    return LoggingContext(
        logger=logger,
        trace_buffer=trace_buffer,
        config=cg,
    )


__all__ = [
    "LoggingConfig",
    "LoggingContext",
    "configure_logging",
]
