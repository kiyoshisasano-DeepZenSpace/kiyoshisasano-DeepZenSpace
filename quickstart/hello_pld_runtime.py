# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Kiyoshi Sasano
"""
hello_pld_runtime.py
--------------------
Minimal runnable demonstration of Phase Loop Dynamics (PLD).

This script provides a simple, interactive example illustrating the core
runtime sequence:

    Drift → Repair → Reentry → Continue → Outcome

It is intentionally minimal and not meant to represent a full implementation.
Its purpose is to provide "first contact" intuition of PLD runtime behavior.

Usage:

    # Default example
    python hello_pld_runtime.py

    # Custom example
    python hello_pld_runtime.py "Can we switch topics and talk about cooking?"

    # Run multiple preset cases
    python hello_pld_runtime.py --examples
"""

from dataclasses import dataclass
from typing import Optional
import sys


# -------------------------------------------------------------------------
# Core Data Model
# -------------------------------------------------------------------------
@dataclass
class PLDResult:
    drift_detected: bool
    repair_applied: bool
    reentry_confirmed: bool
    outcome: str  # e.g., "continue_after_repair", "continue_no_repair", "empty_input"


# -------------------------------------------------------------------------
# Minimal Runtime Logic (Mock Implementation)
# -------------------------------------------------------------------------
class MockPldRuntime:
    """
    Minimal demonstration runtime.

    Drift detection here uses a simple keyword check.
    A real implementation would leverage:
        - Embeddings / semantic similarity
        - LLM-based classification
        - Tool validation and session context alignment
    """

    def detect_drift(self, text: str) -> bool:
        """
        Return True if user appears off-task based on simple keyword rules.

        Args:
            text: Input text from user

        Returns:
            Boolean indicating whether drift is detected.
        """
        drift_keywords = [
            "recipe",
            "cooking",
            "off-topic",
            "unrelated",
            "switch",  # added for phrases like "switch topics"
        ]

        return any(k in text.lower() for k in drift_keywords)

    def run(self, user_input: str) -> PLDResult:
        """
        Process a single user turn and return a minimal PLDResult object.
        """

        if not user_input or not user_input.strip():
            return PLDResult(False, False, False, "empty_input")

        drift = self.detect_drift(user_input)

        # In a real implementation, this event would be logged here.
        # Example pseudo-log:
        #
        # log_pld_event({
        #     "event_type": "drift_detected" if drift else "no_drift",
        #     "source_text": user_input,
        #     "timestamp": datetime.now()
        # })

        if not drift:
            return PLDResult(False, False, True, "continue_no_repair")

        return PLDResult(True, True, True, "continue_after_repair")


# -------------------------------------------------------------------------
# Output Renderer
# -------------------------------------------------------------------------
def render_output(result: PLDResult) -> None:
    """Print user-friendly interpretation of PLD result."""

    if result.outcome == "empty_input":
        print("⚠️ Empty input — nothing to process.\n")
        return

    if result.drift_detected:
        print("🚨 Drift Detected")
        print("🔧 Repair Applied")
        print("🛂 Reentry Confirmed")
    else:
        print("✅ No drift — task continuity preserved")

    print(f"\nOutcome: {result.outcome}\n")


# -------------------------------------------------------------------------
# Example Scenarios
# -------------------------------------------------------------------------
def run_examples():
    runtime = MockPldRuntime()

    scenarios = [
        ("Aligned continuation", "I understand the task. Let me continue scheduling the booking."),
        ("Direct drift", "That's irrelevant to what we're discussing."),
        ("Topic switching", "Can we switch topics and talk about cooking?"),
        ("Off-topic trivia", "Did you know penguins have knees?"),
    ]

    for name, text in scenarios:
        print(f"\n{'=' * 60}")
        print(f"Scenario: {name}")
        print(f"{'=' * 60}")
        print(f"Input: {text}\n")
        result = runtime.run(text)
        render_output(result)


# -------------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    runtime = MockPldRuntime()

    # Scenario mode
    if "--examples" in sys.argv:
        run_examples()
        sys.exit(0)

    # Custom input mode
    if len(sys.argv) > 1:
        test_input = " ".join(arg for arg in sys.argv[1:] if arg != "--examples")
    else:
        test_input = "Okay, understood — but let me talk about an irrelevant recipe now."

    print("\nUser Input:")
    print(test_input)
    print("\n--- Runtime Result ---\n")

    result = runtime.run(test_input)
    render_output(result)

