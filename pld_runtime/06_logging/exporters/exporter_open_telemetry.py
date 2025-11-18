# Version: 1.1
# Stability: experimental (API subject to change)
# Migration: no breaking changes expected, but OTel integration optional.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.exporters.exporter_open_telemetry

Optional OpenTelemetry exporter for PLD runtime traces.

This module maps PLD runtime semantics to standard telemetry concepts:

    - SessionTrace      → Trace
    - Turn              → Span
    - PLD Event         → Structured Log Record (attributes)
    - ControllerOutcome → Child span with policy metadata

Design goals
------------
- Safe when OpenTelemetry is not installed (clean no-op behavior).
- Simple, minimal mapping that can be extended by callers.
- Compatible with SessionTraceBuffer and related logging components.

Typical usage
-------------
    from pld_runtime.logging.session_trace_buffer import SessionTraceBuffer
    from pld_runtime.logging.exporters.exporter_open_telemetry import OpenTelemetryExporter

    buffer = SessionTraceBuffer()
    exporter = OpenTelemetryExporter(endpoint="http://otel-collector:4317")

    # After runtime has populated the buffer:
    exported_count = exporter.export_session(buffer, session_id="sess-123")
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Literal

from ..session_trace_buffer import (
    SessionTraceBuffer,
    TraceItem,
)

# Try loading OpenTelemetry. If missing, we degrade cleanly.
try:  # pragma: no cover - optional dependency
    from opentelemetry import trace, logs
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    from opentelemetry.sdk.logs import LoggerProvider
    from opentelemetry.sdk.logs.export import BatchLogRecordProcessor
    from opentelemetry.exporter.otlp.proto.grpc.log_exporter import OTLPLogExporter

    _OTEL_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    _OTEL_AVAILABLE = False


ExportMode = Literal["trace", "log", "hybrid"]


class OpenTelemetryExporter:
    """
    Export SessionTraceBuffer data into OpenTelemetry.

    Parameters
    ----------
    endpoint:
        OTLP-compatible endpoint (grpc/http). If None, the OTLP exporters will
        use their library defaults.

    mode:
        Controls which OpenTelemetry signal types are emitted:
            - "trace"   → only spans
            - "log"     → only log records
            - "hybrid"  → both spans and logs (default)

    enabled:
        If False, exporter becomes a no-op even if OpenTelemetry is available.

    Notes
    -----
    - If OpenTelemetry is NOT installed, this exporter degrades to a no-op.
    - This module does not mutate SessionTraceBuffer or PLD structures.
      It only reads traces and forwards them to the OTel SDK.
    """

    def __init__(
        self,
        *,
        endpoint: Optional[str] = None,
        mode: ExportMode = "hybrid",
        enabled: bool = True,
    ) -> None:
        self.mode: ExportMode = mode.lower() if isinstance(mode, str) else mode
        if self.mode not in ("trace", "log", "hybrid"):
            self.mode = "hybrid"

        # Public toggles
        self.enabled: bool = bool(enabled and _OTEL_AVAILABLE)

        # Underlying OTel handles (may remain None when disabled)
        self.tracer: Any = None
        self.logger: Any = None

        if not self.enabled:
            # Clean no-op mode: nothing else to configure
            return

        # ---- Tracing pipeline ----
        trace_provider = TracerProvider()
        span_exporter = OTLPSpanExporter(endpoint=endpoint)
        trace_provider.add_span_processor(BatchSpanProcessor(span_exporter))
        trace.set_tracer_provider(trace_provider)
        self.tracer = trace.get_tracer("pld_runtime")

        # ---- Logging pipeline ----
        log_provider = LoggerProvider()
        log_exporter = OTLPLogExporter(endpoint=endpoint)
        log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        logs.set_logger_provider(log_provider)
        self.logger = logs.get_logger("pld_runtime")

    # ------------------------------------------------------------------
    # Public export methods
    # ------------------------------------------------------------------

    def export_session(self, buffer: SessionTraceBuffer, session_id: str) -> int:
        """
        Export a single PLD runtime session into OpenTelemetry.

        Parameters
        ----------
        buffer:
            SessionTraceBuffer containing runtime traces.

        session_id:
            Identifier of the session to export.

        Returns
        -------
        int
            Number of trace items processed for this session (not necessarily
            equal to the number of spans/logs emitted, depending on mode).
        """
        if not self.enabled or self.tracer is None:
            return 0

        trace_obj = buffer.get_trace(session_id)
        if trace_obj is None:
            return 0

        exported = 0

        # Root span per session
        with self.tracer.start_as_current_span(f"session:{session_id}") as session_span:
            session_span.set_attribute("pld.session_id", session_id)
            session_span.set_attribute("pld.length", len(trace_obj.items))

            for item in trace_obj.items:
                exported += self._export_item(
                    item=item,
                    parent_span=session_span,
                    session_id=session_id,
                )

        return exported

    def export_all_sessions(self, buffer: SessionTraceBuffer) -> int:
        """
        Export all known sessions in the buffer into OpenTelemetry.

        Parameters
        ----------
        buffer:
            SessionTraceBuffer containing runtime traces.

        Returns
        -------
        int
            Total number of trace items processed across all sessions.
        """
        if not self.enabled or self.tracer is None:
            return 0

        total = 0
        # Direct access is intentional: exporter operates over all traces.
        for session_id in list(buffer._traces.keys()):  # noqa: SLF001
            total += self.export_session(buffer, session_id)
        return total

    # ------------------------------------------------------------------
    # Internal mapping
    # ------------------------------------------------------------------

    def _export_item(
        self,
        *,
        item: TraceItem,
        parent_span: Any,
        session_id: str,
    ) -> int:
        """
        Map a single TraceItem to OTel spans and/or logs.

        Returns 1 to indicate that the item was processed, regardless of
        whether any signals were emitted (respecting mode settings).
        """
        kind = item.kind

        # ---- Trace spans: turns and controller outcomes ----
        if self.mode in ("trace", "hybrid") and self.tracer is not None:
            if kind in {"turn", "controller_outcome"}:
                with self.tracer.start_as_current_span(
                    f"{kind}:{item.seq}",
                    parent=parent_span,
                ) as span:
                    span.set_attribute("pld.kind", kind)
                    span.set_attribute("pld.session_id", session_id)
                    span.set_attribute("pld.seq", item.seq)
                    span.set_attribute("pld.timestamp", item.ts)

                    # Flatten payload into attributes; complex structures are JSON-encoded.
                    for key, value in item.payload.items():
                        attr_key = f"payload.{key}"
                        if isinstance(value, (str, int, float, bool)) or value is None:
                            span.set_attribute(attr_key, value)
                        else:
                            span.set_attribute(attr_key, json.dumps(value))

        # ---- Log records: PLD events ----
        if self.mode in ("log", "hybrid") and self.logger is not None:
            if kind == "pld_event":
                attributes: Dict[str, Any] = {
                    "pld.kind": kind,
                    "pld.session_id": session_id,
                    "pld.seq": item.seq,
                    # Preserve full payload as JSON string to avoid losing structure.
                    "payload": json.dumps(item.payload),
                }

                record = self.logger.make_record(
                    severity_text="INFO",
                    body=f"PLD_EVENT:{session_id}:{item.seq}",
                    attributes=attributes,
                )

                # API compatibility: prefer `emit`, fall back to `log_record` if needed.
                if hasattr(self.logger, "emit"):
                    self.logger.emit(record)  # type: ignore[call-arg]
                elif hasattr(self.logger, "log_record"):  # pragma: no cover - API variant
                    self.logger.log_record(record)  # type: ignore[call-arg]

        return 1


__all__ = [
    "OpenTelemetryExporter",
    "ExportMode",
]
