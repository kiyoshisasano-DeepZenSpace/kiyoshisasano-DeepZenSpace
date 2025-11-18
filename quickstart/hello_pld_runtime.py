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

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple
import sys


# -------------------------------------------------------------------------
# Core Data Model
# -------------------------------------------------------------------------


@dataclass
class PLDResult:
    """
    Minimal PLD runtime outcome for a single user turn.

    Fields
    ------
    drift_detected:
        True if the runtime judged the input as "off-task" or drifting.

    repair_applied:
        True if some form of repair is (conceptually) applied.
        In this mock implementation, this is a simple boolean flag.

    reentry_confirmed:
        True if the system considers itself "back on track"
        after repair (or if no repair was needed).

    outcome:
        High-level label for what happened, e.g.:
            - "continue_after_repair"
            - "continue_no_repair"
            - "empty_input"
    """

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

        This is intentionally naïve: the goal is just to make the
        example scenarios in this file line up with the runtime behavior.
        """
        drift_keywords = [
            "recipe",
            "cooking",
            "off-topic",
            "unrelated",
            "irrelevant",
            "switch",
            "penguin",
            "topic",
        ]
        lowered = text.lower()
        return any(keyword in lowered for keyword in drift_keywords)

    def run(self, user_input: str) -> PLDResult:
        """
        Process a single user turn and return a minimal PLDResult.

        This is a *single-turn* toy example; there is no session memory,
        no state machine, and no actual repair behavior.
        """
        if not user_input or not user_input.strip():
            return PLDResult(
                drift_detected=False,
                repair_applied=False,
                reentry_confirmed=False,
                outcome="empty_input",
            )

        drift = self.detect_drift(user_input)

        if not drift:
            return PLDResult(
                drift_detected=False,
                repair_applied=False,
                reentry_confirmed=True,
                outcome="continue_no_repair",
            )

        return PLDResult(
            drift_detected=True,
            repair_applied=True,
            reentry_confirmed=True,
            outcome="continue_after_repair",
        )


# -------------------------------------------------------------------------
# Output Renderer
# -------------------------------------------------------------------------


def render_output(result: PLDResult) -> None:
    """Print human-readable interpretation of the PLD result."""

    if result.outcome == "empty_input":
        print("⚠️ Empty input — nothing to process.\n")
        return

    if result.drift_detected:
        print("🚨 Drift Detected")
        print("🔧 Repair Applied")
        print("🛂 Reentry Confirmed")
    else:
        print("✅ No drift — task continuity preserved")

    print(f"\nOutcome: {result.outcome}")

    # Debug visibility for learning purposes
    print(f"🧪 Debug: {result}\n")


# -------------------------------------------------------------------------
# Example Scenarios
# -------------------------------------------------------------------------


def run_examples() -> None:
    """Run a small set of canned scenarios to illustrate behavior."""
    runtime = MockPldRuntime()

    scenarios: List[Tuple[str, str]] = [
        (
            "Aligned continuation",
            "I understand the task. Let me continue scheduling the booking.",
        ),
        (
            "Direct drift",
            "That's irrelevant to what we're discussing.",
        ),
        (
            "Topic switching",
            "Can we switch topics and talk about cooking?",
        ),
        (
            "Off-topic trivia",
            "This is random penguin trivia for no reason.",
        ),
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


def main(argv: Optional[list[str]] = None) -> int:
    """
    CLI entrypoint.

    - `--examples`  → run built-in scenarios
    - otherwise     → treat remaining args as a single user input string
    """
    if argv is None:
        argv = sys.argv[1:]

    runtime = MockPldRuntime()

    if "--examples" in argv:
        run_examples()
        return 0

    # Join all args except the flag as the input text.
    user_args = [arg for arg in argv if arg != "--examples"]

    if user_args:
        test_input = " ".join(user_args)
    else:
        test_input = "Okay — understood, but let me talk about an unrelated recipe now."

    print("\nUser Input:")
    print(test_input)
    print("\n--- Runtime Result ---\n")

    result = runtime.run(test_input)
    render_output(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

