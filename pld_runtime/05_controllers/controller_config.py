#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pld_runtime.controllers.controller_config

Centralized configuration definition for PLD runtime controllers.

This file exists to:

- Provide a *single stable config model* for controller-level behavior
- Allow typed, documented parameters for runtime tuning
- Support environment-based overrides while preserving deterministic defaults
- Avoid scattered implicit config inside controllers/action_router/etc.

This is intentionally lightweight and declarative.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from ..enforcement.thresholds import EnforcementMode
from ..detection.runtime_signal_bridge import BridgeConfig
from .action_router import ActionRouterConfig


# ---------------------------------------------------------------------------
# Execution Mode / Personality
# ---------------------------------------------------------------------------

class ControllerPersonality(str, Enum):
    """
    Defines how the runtime controller should behave at a systemic level.

    Modes
    -----
    diagnostic:
        Verbose events, relaxed enforcement, runtime telemetry exposed.
        Best for development and debugging.

    operational:
        Production mode: balanced enforcement, limited noise, stable outputs.

    guarded:
        Strict enforcement: minimal drift tolerance.
        Designed for high-risk or compliance-bound systems.

    experimental:
        Allows incomplete enforcement or experimental logic without failing.
        Intended for R&D or testing new detectors/policies.

    Notes
    -----
    Personality does NOT directly modify logic — it maps into:

        - enforcement mode
        - router behavior
        - bridge sensitivity

    The caller may override these individually even if personality is set.
    """

    DIAGNOSTIC = "diagnostic"
    OPERATIONAL = "operational"
    GUARDED = "guarded"
    EXPERIMENTAL = "experimental"


# ---------------------------------------------------------------------------
# Controller Runtime Configuration Model
# ---------------------------------------------------------------------------

@dataclass
class RuntimeControllerConfig:
    """
    Full configuration for PldRuntimeController.

    This object is intended to be passed into the controller constructor
    and optionally persisted as part of a deployment manifest.

    Parameters
    ----------
    personality:
        High-level runtime posture preset (overridable).

    enforcement_mode:
        Specific enforcement posture (strict/balanced/observational).
        If None, defaults to the mode implied by personality.

    platform:
        System identifier for envelope metadata.

    environment:
        Runtime environment value (prod/staging/local/test).

    mode:
        Additional runtime metadata tag, set by operators.

    enable_schema_validation:
        If True, validation for events + envelopes is active.

    enable_sequence_checks:
        If True, event stream order is evaluated via sequence rules.

    auto_wrap_envelope:
        Controls whether envelope creation happens automatically.

    bridge:
        Configuration for RuntimeSignalBridge (thresholds, turn mapping).

    router:
        Configuration for ActionRouter (target behavior and escalation).
    """

    # high-level personality
    personality: ControllerPersonality = ControllerPersonality.OPERATIONAL

    # lower-level overrides
    enforcement_mode: Optional[EnforcementMode] = None

    # metadata fields applied to envelopes
    platform: str = "unknown"
    environment: str = "production"
    mode: str = "runtime"

    # operational toggles
    enable_schema_validation: bool = True
    enable_sequence_checks: bool = True
    auto_wrap_envelope: bool = True

    # nested config areas
    bridge: BridgeConfig = BridgeConfig()
    router: ActionRouterConfig = ActionRouterConfig()


# ---------------------------------------------------------------------------
# Personality → Effective Enforcement Mapping
# ---------------------------------------------------------------------------

def resolve_effective_enforcement_mode(config: RuntimeControllerConfig) -> EnforcementMode:
    """
    Compute the resolved enforcement mode based on:

        - explicit override (`config.enforcement_mode`)
        - global personality preset

    This keeps enforced behavior consistent and predictable.
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

    # Fallback (unlikely)
    return EnforcementMode.BALANCED


__all__ = [
    "ControllerPersonality",
    "RuntimeControllerConfig",
    "resolve_effective_enforcement_mode",
]
