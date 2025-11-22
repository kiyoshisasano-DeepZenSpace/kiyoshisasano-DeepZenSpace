# version: 2.0.0
# status: experimental
# authority: Level 5 — runtime implementation
# scope: Bridge runtime-level detection signals into PLD-compliant events and optional envelopes.
# change_type: runtime-only
# dependencies: PLD Level 1–3 specifications, version 2.0

"""
runtime_signal_bridge

Mode: runtime_template

This module provides a minimal, opinionated template for mapping runtime
signals into PLD-compliant events (and optionally into a runtime envelope).

Scope and constraints:
- Structural and semantic validity of PLD events are governed exclusively
  by the Level 1 schema and Level 2 event matrix.
- This module MUST NOT alter or reinterpret Level 1–3 semantics.
- All mappings provided here are runtime-only defaults and MAY be customized
  per deployment, provided PLD validity is preserved.
"""

from __future__ import annotations

import dataclasses
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Mapping, MutableMapping, Optional

# ------------------------------
# Types and simple data carriers
# ------------------------------


PLD_SOURCE = Literal[
    "user", "assistant", "runtime", "controller", "detector", "system"
]

ValidationMode = Literal["strict", "warn", "normalize"]

_DRIFT_CODE_PASSTHROUGH = re.compile(
    r"^D[0-9]+_[a-z0-9]+(?:_[a-z0-9]+)*$"
)


@dataclass(frozen=True)
class RuntimeSignal:
    """
    Generic runtime signal emitted by detection code.

    This structure is intentionally minimal and non-normative. It is a
    convenience carrier for bridging into PLD events. Callers MAY define
    their own richer types and adapt in a thin wrapper.

    Fields:
        kind: Stable identifier for the detection outcome. This SHOULD
              map to a PLD lifecycle prefix (e.g., 'D4_tool_error'),
              but that is a runtime convention, not a schema requirement.
        severity: Free-form severity label for local triage (e.g., 'low',
                  'medium', 'high', 'critical'). Not part of PLD schema.
        details: Arbitrary key/value data used when deriving payload and
                 pld.metadata.
    """

    kind: str
    severity: str = "unknown"
    details: Mapping[str, Any] = dataclasses.field(default_factory=dict)


@dataclass(frozen=True)
class BridgeConfig:
    """
    Configuration for the runtime signal bridge.

    Fields:
        default_source: PLD `source` value used when constructing events.
        validation_mode: Declared PLD validation mode. This is advisory
                         only; the actual validator is external.
        default_user_visible: Default for `ux.user_visible_state_change`
                             when a caller does not specify a value.
    """

    default_source: PLD_SOURCE = "detector"
    validation_mode: ValidationMode = "strict"
    default_user_visible: bool = True


# ------------------------------
# Core bridge implementation
# ------------------------------


class RuntimeSignalBridge:
    """
    Bridge runtime signals into PLD events and optional envelopes.

    Responsibilities (runtime-only, Level 5 scope):

    - Map RuntimeSignal instances to PLD lifecycle events using
      Level 2 MUST mappings for event_type ↔ phase.
    - Construct structurally valid PLD events (Level 1) but defer
      final validation to external validators.
    - Optionally wrap events in a runtime envelope structure that is
      compatible with the runtime event envelope schema.

    This implementation is designed as a template. Callers MAY:
    - Replace or extend mapping logic.
    - Attach project-specific payload/runtime/ux shaping.
    - Integrate external validators or CI checks.
    """

    def __init__(self, config: Optional[BridgeConfig] = None) -> None:
        self._config = config or BridgeConfig()

    # ---------
    # Utilities
    # ---------

    @staticmethod
    def _now_iso() -> str:
        """Return current UTC time as an ISO 8601 string with full precision."""
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _new_uuid() -> str:
        """Generate a UUIDv4 string for event_id / envelope_id."""
        return str(uuid.uuid4())

    def _base_event(
        self,
        *,
        session_id: str,
        turn_sequence: int,
        source: Optional[PLD_SOURCE] = None,
    ) -> Dict[str, Any]:
        """
        Construct the PLD event base fields required by the schema.

        This helper does not set:
        - event_type
        - pld
        - payload
        - ux
        which MUST be populated by callers or higher-level helpers.
        """
        if turn_sequence < 1:
            raise ValueError("turn_sequence MUST be >= 1 to satisfy PLD schema.")

        # TODO: Clarify whether `source` should represent the reporter (e.g., detector)
        #       or the originating actor (e.g., assistant) when drift is detected
        #       from assistant-generated behavior.

        event: Dict[str, Any] = {
            "schema_version": "2.0",
            "event_id": self._new_uuid(),
            "timestamp": self._now_iso(),
            "session_id": session_id,
            "turn_sequence": int(turn_sequence),
            "source": (source or self._config.default_source),
        }
        return event

    # ---------------------------
    # Signal → PLD event mappings
    # ---------------------------

    def build_drift_event(
        self,
        *,
        signal: RuntimeSignal,
        session_id: str,
        turn_sequence: int,
        ux_user_visible_state_change: Optional[bool] = None,
        payload: Optional[MutableMapping[str, Any]] = None,
        runtime: Optional[MutableMapping[str, Any]] = None,
        metrics: Optional[MutableMapping[str, Any]] = None,
        extensions: Optional[MutableMapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Map a RuntimeSignal into a PLD `drift_detected` event.

        Semantic constraints enforced here:

        - event_type = "drift_detected"
        - pld.phase = "drift"
        - pld.code MUST begin with the 'D' lifecycle prefix
        - Code pattern MUST match the schema pattern.

        This helper does **not** perform full schema or matrix validation.
        Those checks MUST be performed by an external validator in the
        ingestion pipeline.

        TODO: Clarify the intended separation between event-level `runtime`
              (e.g., Python version, library versions, local tool metadata)
              and envelope-level `runtime` (e.g., environment, mode). If they
              conceptually overlap, additional guidance may be required to
              avoid duplication and ambiguity in downstream queries.
        """

        # Derive PLD code from signal.kind. If the caller already uses a
        # lifecycle-compatible prefix (e.g., D4_tool_error) that matches the
        # expected drift pattern, we reuse it; otherwise we provide a neutral
        # default that preserves the 'D' prefix.
        code = self._derive_drift_code(signal)

        pld_obj: Dict[str, Any] = {
            "phase": "drift",
            "code": code,
            "metadata": {
                "severity": signal.severity,
                "runtime_signal_kind": signal.kind,
                "runtime_signal_details": dict(signal.details),
            },
        }

        event = self._base_event(
            session_id=session_id,
            turn_sequence=turn_sequence,
        )
        event["event_type"] = "drift_detected"
        event["pld"] = pld_obj
        event["payload"] = dict(payload or {})
        if runtime is not None:
            event["runtime"] = dict(runtime)
        if metrics is not None:
            event["metrics"] = dict(metrics)
        if extensions is not None:
            event["extensions"] = dict(extensions)

        event["ux"] = {
            "user_visible_state_change": (
                self._config.default_user_visible
                if ux_user_visible_state_change is None
                else bool(ux_user_visible_state_change)
            )
        }

        return event

    def _derive_drift_code(self, signal: RuntimeSignal) -> str:
        """
        Derive a PLD drift code from a RuntimeSignal.

        Rules:
        - If signal.kind matches a lifecycle-compatible drift pattern
          (e.g., D4_tool_error), it is used as-is.
        - Otherwise, the code falls back to 'D0_<normalized_descriptor>' with
          a best-effort descriptor derived from signal.kind, but the prefix
          remains 'D' to preserve lifecycle semantics.

        The caller is responsible for ensuring that any deployment-
        specific codes remain consistent with the event matrix and
        validation strategy.
        """
        kind = signal.kind.strip()

        # Use a strict pass-through rule to avoid accidental misclassification
        # of arbitrary strings that merely start with 'D' (e.g., "DiskSpaceLow").
        if _DRIFT_CODE_PASSTHROUGH.match(kind):
            return kind

        # Neutral, prefix-consistent fallback.
        # Descriptor is lowercased and normalized into snake_case.
        descriptor = kind.lower().replace(" ", "_") or "unspecified"
        return f"D0_{descriptor}"

    # ------------------------------------------
    # Optional envelope construction (Level 5)
    # ------------------------------------------

    def wrap_in_envelope(
        self,
        *,
        event: Mapping[str, Any],
        session_id: str,
        environment: Literal["production", "staging", "sandbox", "local"],
        mode: Literal["stream", "batch", "debug", "audit"] = "stream",
        session_user_id: Optional[str] = None,
        session_platform: Optional[str] = None,
        session_platform_detail: Optional[str] = None,
        trace: Optional[Mapping[str, Any]] = None,
        tags: Optional[Mapping[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Wrap a PLD event in a runtime envelope structure.

        Structural goals:

        - Provide `envelope_id`, `timestamp`, `version`, `session`, `runtime`,
          and `event` fields compatible with the runtime envelope schema.
        - Enforce the Level 5 rule that envelope.session.session_id MUST
          equal event.session_id. A mismatch results in a ValueError.

        This helper does not attempt to validate the event itself; that remains
        the responsibility of upstream or downstream validators.
        """
        event_session_id = event.get("session_id")
        if event_session_id is None:
            raise ValueError("event.session_id is required to build an envelope.")

        if event_session_id != session_id:
            raise ValueError(
                "Envelope session_id MUST equal event.session_id. "
                f"Got session_id={session_id!r}, event.session_id={event_session_id!r}"
            )

        envelope_session: Dict[str, Any] = {
            "session_id": session_id,
        }
        if session_user_id is not None:
            envelope_session["user_id"] = session_user_id
        if session_platform is not None:
            envelope_session["platform"] = session_platform
        if session_platform_detail is not None:
            envelope_session["platform_detail"] = session_platform_detail

        envelope_runtime: Dict[str, Any] = {
            "environment": environment,
            "mode": mode,
        }
        if tags is not None:
            envelope_runtime["tags"] = dict(tags)

        envelope: Dict[str, Any] = {
            "envelope_id": self._new_uuid(),
            "timestamp": self._now_iso(),
            "version": "2.0",
            "session": envelope_session,
            "runtime": envelope_runtime,
            "event": dict(event),
        }

        if trace is not None:
            envelope["trace"] = dict(trace)

        return envelope


# ---------------------------
# Convenience factory methods
# ---------------------------


def default_bridge() -> RuntimeSignalBridge:
    """
    Construct a RuntimeSignalBridge with default configuration.

    This helper exists to keep call sites concise:

        bridge = default_bridge()
        drift_event = bridge.build_drift_event(...)

    The default configuration declares:
    - source='detector'
    - validation_mode='strict'
    - default_user_visible=True

    Callers MAY construct BridgeConfig explicitly when different behavior
    is required.
    """
    return RuntimeSignalBridge()


# Deferred for later phase
#
# - Clarify the semantic boundary between event-level `runtime` and
#   envelope-level `runtime` to avoid duplicated or ambiguous metadata.
# - Define a governance rule for how `source` should be chosen when a
#   drift condition is detected by one component (e.g., detector) but
#   originates from another (e.g., assistant or external system).
