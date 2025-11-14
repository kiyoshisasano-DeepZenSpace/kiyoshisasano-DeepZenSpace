# Version: 0.2.0
# Stability: experimental (API subject to change)
# Migration: no breaking changes expected, but OTel integration optional.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.logging.exporters.exporter_open_telemetry

Optional OpenTelemetry exporter for PLD runtime traces.

This module maps PLD runtime semantics to standard telemetry concepts:

    - SessionTrace   → Trace
    - Turn           → Span
    - PLD Event      → Structured Log Record (attributes)
    - ControllerOutcome → child span with policy metadata

This exporter is intentionally minimal and safe:

    - If OpenTelemetry is NOT installed → no-op mode
    - If enabled → exports using OTel tracing + logs API

Intended deployment targets:
    - Jaeger
    - Grafana Tempo
    - Honeycomb
    - DataDog APM
    - OTLP Collector (grpc/http)
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

from ..session_trace_buffer import (
    SessionTraceBuffer,
    SessionTrace,
    TraceItem,
)

# Try loading OpenTelemetry. If missing, we degrade cleanly.
try:
    from opentelemetry import trace, logs
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

    from opentelemetry.sdk.logs import LoggerProvider
    from opentelemetry.sdk.logs.export import BatchLogRecordProcessor
    from opentelemetry.exporter.otlp.proto.grpc.log_exporter import OTLPLogExporter

    _OTEL_AVAILABLE = True
except Exception:
    _OTEL_AVAILABLE = False


class OpenTelemetryExporter:
    """
    Export SessionTraceBuffer data into OpenTelemetry.

    Parameters
    ----------
    endpoint:
        OTLP-compatible endpoint (grpc/http). Required if OTel is available.

    mode:
        "trace"   → only spans
        "log"     → only logs
        "hybrid"  → both

    enabled:
        If False → no-op even if OTEL is available.
    """

    def __init__(
        self,
        *,
        endpoint: Optional[str] = None,
        mode: str = "hybrid",
        enabled: bool = True,
    ) -> None:

        self.mode = mode.lower()
        self.enabled = enabled and _OTEL_AVAILABLE

        if not self.enabled:
            self.tracer = None
            self.logger = None
            return

        # Configure tracing pipeline
        trace_provider = TracerProvider()
        trace_exporter = OTLPSpanExporter(endpoint=endpoint)
        trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
        trace.set_tracer_provider(trace_provider)
        self.tracer = trace.get_tracer("pld_runtime")

        # Configure logs pipeline
        log_provider = LoggerProvider()
        log_exporter = OTLPLogExporter(endpoint=endpoint)
        log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
        logs.set_logger_provider(log_provider)
        self.logger = logs.get_logger("pld_runtime")

    # ----------------------------------------------------------------------
    # Public export methods
    # ----------------------------------------------------------------------

    def export_session(self, buffer: SessionTraceBuffer, session_id: str) -> int:
        """
        Export a single PLD runtime session into OpenTelemetry.

        Returns number of exported entries.
        """
        if not self.enabled:
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
                exported += self._export_item(item, session_span, session_id)

        return exported

    # ----------------------------------------------------------------------
    # Internal mapping
    # ----------------------------------------------------------------------

    def _export_item(
        self,
        item: TraceItem,
        parent_span: Any,
        session_id: str,
    ) -> int:

        kind = item.kind

        # ---- case: trace span for turns, controller outcome ----
        if self.mode in ("trace", "hybrid") and kind in {"turn", "controller_outcome"}:
            with self.tracer.start_as_current_span(f"{kind}:{item.seq}", parent=parent_span) as span:
                span.set_attribute("pld.kind", kind)
                span.set_attribute("pld.seq", item.seq)
                span.set_attribute("pld.timestamp", item.ts)

                # flatten payload into attributes
                for key, value in item.payload.items():
                    span.set_attribute(f"payload.{key}", json.dumps(value))

        # ---- case: event logging ----
        if self.mode in ("log", "hybrid") and kind == "pld_event":
            record = self.logger.make_record(
                severity_text="INFO",
                body=f"PLD_EVENT:{session_id}:{item.seq}",
                attributes={
                    "pld.kind": kind,
                    "pld.session_id": session_id,
                    "pld.seq": item.seq,
                    "payload": json.dumps(item.payload),
                },
            )
            self.logger.emit(record)

        return 1


__all__ = [
    "OpenTelemetryExporter",
]
