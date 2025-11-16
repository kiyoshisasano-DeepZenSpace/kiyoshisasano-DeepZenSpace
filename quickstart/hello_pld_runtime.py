"""
hello_pld_runtime.py
--------------------
Minimal runnable demonstration of Phase Loop Dynamics (PLD).
Supports:
- default example
- custom input (`python hello_pld_runtime.py "your text"`)
- scenario mode (`python hello_pld_runtime.py --examples`)
"""

import sys
from dataclasses import dataclass


# -------------------------------------------------------------------------
# Result model
# -------------------------------------------------------------------------
@dataclass
class PLDResult:
    drift: bool
    repaired: bool
    reentered: bool
    outcome: str


# -------------------------------------------------------------------------
# Mock PLD runtime (teaching-grade, not production)
# -------------------------------------------------------------------------
class MockPldRuntime:
    """
    A simplified runtime model illustrating the drift → repair → reentry → continue logic.
    This version uses naive heuristics — the goal is feel, not correctness.
    """

    def detect_drift(self, text: str) -> bool:
        """Return True if user appears off-task based on simple keyword rules."""
        drift_keywords = ["recipe", "cooking", "off-topic", "unrelated"]
        return any(k in text.lower() for k in drift_keywords)

    def apply_repair(self) -> bool:
        """Simulate repairing the detected drift."""
        return True

    def confirm_reentry(self) -> bool:
        """Simulate verifying alignment after repair."""
        return True

    def run(self, user_input: str) -> PLDResult:
        """Execute the runtime lifecycle."""
        if not user_input.strip():
            return PLDResult(False, False, False, "empty_input")

        drift = self.detect_drift(user_input)

        if not drift:
            return PLDResult(False, False, False, "continue")

        repaired = self.apply_repair()
        reentered = self.confirm_reentry()

        return PLDResult(
            drift=True,
            repaired=repaired,
            reentered=reentered,
            outcome="continue_after_repair"
        )


# -------------------------------------------------------------------------
# CLI Output formatting
# -------------------------------------------------------------------------
def render_output(result: PLDResult):
    """Print formatted runtime state."""
    print("\n--- PLD Runtime Result ---\n")

    if result.outcome == "empty_input":
        print("⚠️ No content provided.\n")
        return

    if not result.drift:
        print("🟢 No drift detected — continuing as normal.\n")
        return

    print("🚨 Drift Detected")
    print("🔧 Repair Applied" if result.repaired else "⚠️ Repair Failed")
    print("✅ Reentry Confirmed\n" if result.reentered else "❌ Reentry Failed\n")

    print(f"Outcome: {result.outcome}\n")


# -------------------------------------------------------------------------
# Example Scenarios
# -------------------------------------------------------------------------
def run_examples():
    runtime = MockPldRuntime()

    scenarios = [
        ("No drift", "I understand. Continuing the task now."),
        ("Explicit drift", "Let me talk about a cooking recipe instead."),
        ("Implicit drift", "Okay wait — what if we discuss something unrelated?")
    ]

    for name, text in scenarios:
        print("\n" + "=" * 60)
        print(f"Scenario: {name}")
        print("=" * 60)
        print(f"Input: {text}")
        result = runtime.run(text)
        render_output(result)


# -------------------------------------------------------------------------
# CLI Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    runtime = MockPldRuntime()

    if "--examples" in sys.argv:
        run_examples()
        sys.exit(0)

    if len(sys.argv) > 1:
        user_input = " ".join(arg for arg in sys.argv[1:] if arg != "--examples")
    else:
        user_input = "Okay, understood — but let me talk about an irrelevant recipe now."

    result = runtime.run(user_input)
    render_output(result)
