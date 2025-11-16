"""
hello_pld_runtime.py
--------------------

Minimal runnable demonstration of Phase Loop Dynamics (PLD).

This script shows the core runtime semantics:

    - Drift detection
    - Repair intervention
    - Reentry confirmation
    - Outcome evaluation

It is NOT a full PLD implementation — this is the smallest possible
interactive example meant to demonstrate runtime behavior and logging.

Run:
    python hello_pld_runtime.py

Expected Output Example:

    ------------------------------------------------------------
    🚨 Drift Detected
    🔧 Repair Applied
    ✅ Reentry Confirmed

    Outcome: continue_after_repair
    ------------------------------------------------------------

"""

from dataclasses import dataclass


# -------------------------------------------------------------------------
# Minimal PLD component (mock runtime)
# -------------------------------------------------------------------------

@dataclass
class PLDResult:
    drift_detected: bool
    repair_applied: bool
    reentry_confirmed: bool
    outcome: str


class MockPldRuntime:
    """
    A lightweight mock runtime representing PLD semantics without requiring
    the full implementation. This exists only to demonstrate:

        input → drift detection → repair → reentry → outcome
    """

    def detect_drift(self, text: str) -> bool:
        """
        Simplified heuristic rule:
        Consider the input 'drifted' if it contains common off-topic signals.
        """
        return any(keyword in text.lower() for keyword in ["irrelevant", "off-topic"])

    def apply_repair(self) -> bool:
        """Simulated repair always succeeds."""
        return True

    def confirm_reentry(self) -> bool:
        """Simulated confirmation."""
        return True

    def run(self, user_input: str) -> PLDResult:
        drift = self.detect_drift(user_input)

        if not drift:
            return PLDResult(False, False, False, "continue")

        repair = self.apply_repair()
        confirmed = self.confirm_reentry()

        return PLDResult(
            drift_detected=drift,
            repair_applied=repair,
            reentry_confirmed=confirmed,
            outcome="continue_after_repair" if confirmed else "repeat_repair"
        )


# -------------------------------------------------------------------------
# Human-friendly rendering layer
# -------------------------------------------------------------------------

def render_output(result: PLDResult):
    print("\n" + "-" * 60)

    if result.drift_detected:
        print("🚨 Drift Detected")
    else:
        print("👌 No Drift Detected")

    if result.repair_applied:
        print("🔧 Repair Applied")

    if result.reentry_confirmed:
        print("✅ Reentry Confirmed")

    print(f"\nOutcome: {result.outcome}")
    print("-" * 60 + "\n")


# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------

if __name__ == "__main__":
    runtime = MockPldRuntime()

    # Default example input (replace later with CLI or integration hooks)
    test_input = "Okay, understood — but let me talk about an irrelevant recipe now."

    print("User Input:")
    print(test_input)

    result = runtime.run(test_input)
    render_output(result)
