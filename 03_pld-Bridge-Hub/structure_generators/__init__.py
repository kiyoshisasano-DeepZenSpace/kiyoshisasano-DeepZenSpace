# 03_pld-Bridge-Hub/structure_generators/__init__.py
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — Structure Generators Package

Contains core modules for constructing, tracking, and classifying
Phase Loop Dynamics (PLD) event structures.

Modules:
    latency_tracker        → Event-level latency tracking and Δ𝒟 computation
    pause_classifier_bot   → Local/LLM-based pause classification
    reentry_detector       → Conversational reentry event extraction

Usage example:
    from structure_generators.latency_tracker import LatencyEvent
    from structure_generators.pause_classifier_bot import classify_pause
    from structure_generators.reentry_detector import detect_reentry
"""

from .latency_tracker import LatencyEvent, emit_pld_jsonl
from .pause_classifier_bot import classify_pause
from .reentry_detector import detect_reentry  # if defined in your file

__all__ = [
    "LatencyEvent",
    "emit_pld_jsonl",
    "classify_pause",
    "detect_reentry",
]
