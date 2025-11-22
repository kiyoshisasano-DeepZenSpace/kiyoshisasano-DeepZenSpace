#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.controllers.controller_config (v1.1 Canonical Edition)

Centralized configuration model for PLD runtime controllers.

This file provides:

- A single authoritative configuration structure for runtime controllers  
- Typed, documented fields to support predictable runtime tuning  
- Environment-aware extension without implicit mutation or hidden defaults  
- A declarative, stable surface for deployment manifests and orchestrators  

This module is intentionally minimal and framework-agnostic.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..enforcement.thresholds import EnforcementMode
from ..detection.runtime_signal_bridge import BridgeConfig
from .action_router import ActionRouterConfig


# ---------------------------------------------------------------------------
# Controller Personality — Runtime Behavior Posture (High-Level)
# ---------------------------------------------------------------------------

class ControllerPersonality(str, Enum):
    """
    Describes the systemic execution posture of the runtime controller.

    The selected personality influences:

        - enforcement aggressiveness
        - allowed drift tolerance
        - verbosity and telemetry visibility
        - router escalation patterns

    Personality does NOT directly adjust logic. Instead, it configures:

        - `EnforcementMode`
        - `ActionRouterConfig`
        - `RuntimeSignalBridge` sensitivity

    Modes
    -----
    diagnostic:
        High verbosity, relaxed enforcement, transparent execution.
        Ideal for debugging and development.

    operational:
        Balanced and stable posture suitable for production deployment.

    guarded:
        Low tolerance for drift signals. Strong enforcement and escalation.
        Intended for compliance-critical or safety-sensitive environments.

    experimental:
        Allows partial or incomplete enforcement logic.
        Suitable for research pilots or A/B runtime evaluation.
    """

    DIAGNOSTIC = "diagnostic"
    OPERATIONAL = "operational"
    GUARDED = "guarded"
    EXPERIMENTAL = "experimental"


# ---------------------------------------------------------------------------
# Runtime Controller Configuration Model
# ---------------------------------------------------------------------------

@dataclass
class RuntimeControllerConfig:
    """
    Canonical configuration model for `PldRuntimeController`.

    This configuration should be constructed explicitly during deployment or
    passed through a manifest. It is intentionally stable and versioned.

    Parameters
    ----------
    personality:
        High-level posture preset affecting enforcement and routing behavior.

    enforcement_mode:
        Optional override for the effective enforcement setting.
        If unset, `resolve_effective_enforcement_mode()` derives a mode
        based on the selected personality.

    platform:
        Identifies the execution platform or agent environment.

    environment:
        Execution environment label (e.g., production/staging/local/test).

    mode:
        Optional modifier conveying runtime metadata or operator intent.

    enable_schema_validation:
        If True, PLD event envelopes and payloads are validated
        against canonical schemas.

    enable_sequence_checks:
        If True, enforces ordering guarantees and phase validity rules.

    auto_wrap_envelope:
        If True, the runtime automatically generates event envelopes.

    bridge:
        Configuration for the RuntimeSignalBridge, responsible for converting
        raw signals into phase transitions and telemetry events.

    router:
        Configuration for the ActionRouter, controlling repair strategy
        selection, escalation, and execution routing.
    """

    # high-level posture
    personality: ControllerPersonality = ControllerPersonality.OPERATIONAL

    # explicit override (optional)
    enforcement_mode: Optional[EnforcementMode] = None

    # metadata identifiers
    platform: str = "unknown"
    environment: str = "production"
    mode: str = "runtime"

    # operational toggles
    enable_schema_validation: bool = True
    enable_sequence_checks: bool = True
    auto_wrap_envelope: bool = True

    # nested system configuration
    bridge: BridgeConfig = BridgeConfig()
    router: ActionRouterConfig = ActionRouterConfig()


# ---------------------------------------------------------------------------
# Enforcement Resolution Logic
# ---------------------------------------------------------------------------

def resolve_effective_enforcement_mode(config: RuntimeControllerConfig) -> EnforcementMode:
    """
    Resolve the final enforcement mode applied to the runtime controller.

    Priority Rules
    --------------
    1. If `config.enforcement_mode` is explicitly set → return as-is.
    2. Otherwise derive the setting based on the configured personality.

    The result ensures consistent operational behavior and prevents implicit,
    uncontrolled policy drift.
    """

    if config.enforcement_mode is not None:
        return config.enforcement_mode

    match config.personality:
        case ControllerPersonality.DIAGNOSTIC:
            return EnforcementMode.OBSERVATIONAL
        case ControllerPersonality.OPERATIONAL:
            return EnforcementMode.BALANCED
        case ControllerPersonality.GUARDED:
            return EnforcementMode.STRICT
        case ControllerPersonality.EXPERIMENTAL:
            return EnforcementMode.OBSERVATIONAL

    # Defensive fallback (not expected under normal configuration)
    return EnforcementMode.BALANCED


__all__ = [
    "ControllerPersonality",
    "RuntimeControllerConfig",
    "resolve_effective_enforcement_mode",
]

