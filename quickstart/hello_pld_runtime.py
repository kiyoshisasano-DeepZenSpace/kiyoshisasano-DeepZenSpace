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

Usage:
    # Default example
    python hello_pld_runtime.py
    
    # Custom input
    python hello_pld_runtime.py "Your custom message here"
    
    # Run all example scenarios
    python hello_pld_runtime.py --examples

Expected Output Example:
    ------------------------------------------------------------
    🚨 Drift Detected
    🔧 Repair Applied
    ✅ Reentry Confirmed
    
    Outcome: continue_after_repair
    ------------------------------------------------------------
"""

import sys
from dataclasses import dataclass

# -------------------------------------------------------------------------
# Minimal PLD component (mock runtime)
# -------------------------------------------------------------------------

@dataclass
class PLDResult:
    """Result container for PLD runtime execution."""
    drift_detected: bool
    repair_applied: bool
    reentry_confirmed: bool
    outcome: str


class MockPldRuntime:
    """
    A lightweight mock runtime representing PLD semantics without requiring
    the full implementation. This exists only to demonstrate:
        input → drift detection → repair → reentry → outcome
    
    In production, this would use:
    - LLM-based drift classification
    - Context-aware repair strategies
    - Structured reentry validation
    """
    
    def detect_drift(self, text: str) -> bool:
        """
        Simplified heuristic rule:
        Consider the input 'drifted' if it contains common off-topic signals.
        
        In production, this would use:
        - LLM-based classification
        - Context comparison against task state
        - Tool/API validation
        
        Args:
            text: User input to check for drift
        
        Returns:
            True if drift detected, False otherwise
        """
        drift_keywords = [
            "irrelevant", "off-topic", "switch topics", 
            "change subject", "talk about", "different topic"
        ]
        return any(keyword in text.lower() for keyword in drift_keywords)
    
    def apply_repair(self) -> bool:
        """
        Simulated repair always succeeds.
        
        In production:
        - Soft repair: clarification, constraint restatement
        - Hard repair: context reset, escalation
        """
        return True
    
    def confirm_reentry(self) -> bool:
        """
        Simulated reentry confirmation.
        
        In production:
        - Verify alignment restoration
        - Confirm task continuation readiness
        - Validate context consistency
        """
        return True
    
    def run(self, user_input: str) -> PLDResult:
        """
        Execute the PLD runtime loop on given input.
        
        Args:
            user_input: Text to process
        
        Returns:
            PLDResult with phase outcomes
        """
        # Handle empty input
        if not user_input or not user_input.strip():
            return PLDResult(False, False, False, "empty_input")
        
        # Phase 1: Drift detection
        drift = self.detect_drift(user_input)
        
        if not drift:
            # No drift → continue normally
            return PLDResult(False, False, False, "continue")
        
        # Phase 2: Repair
        repair = self.apply_repair()
        
        # Phase 3: Reentry confirmation
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
    """Display PLD result in human-readable format."""
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
# Example scenarios
# -------------------------------------------------------------------------

def run_examples():
    """Run multiple example scenarios to demonstrate drift vs no-drift."""
    runtime = MockPldRuntime()
    
    scenarios = [
        (
            "No drift - aligned continuation",
            "I understand the booking requirements. Let me proceed with the reservation."
        ),
        (
            "Drift detected - topic switch",
            "Can we switch topics and talk about cooking instead?"
        ),
        (
            "Drift detected - off-topic",
            "That's irrelevant to what we're discussing right now."
        ),
        (
            "Drift detected - subject change",
            "Let me talk about a completely different topic for a moment."
        ),
        (
            "No drift - clarification request",
            "Could you clarify the time preference for the meeting?"
        ),
    ]
    
    for i, (name, input_text) in enumerate(scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Scenario {i}/{len(scenarios)}: {name}")
        print(f"{'='*60}")
        print(f"Input: {input_text}")
        
        result = runtime.run(input_text)
        render_output(result)


# -------------------------------------------------------------------------
# Entry point
# -------------------------------------------------------------------------

if __name__ == "__main__":
    runtime = MockPldRuntime()
    
    # Check for --examples flag
    if "--examples" in sys.argv:
        print("\n🎯 Running all example scenarios...\n")
        run_examples()
        sys.exit(0)
    
    # Check for custom input via command line
    if len(sys.argv) > 1:
        # Join all arguments (excluding script name)
        test_input = " ".join(sys.argv[1:])
    else:
        # Default example
        test_input = "Okay, understood — but let me talk about an irrelevant recipe now."
    
    print("User Input:")
    print(test_input)
    
    result = runtime.run(test_input)
    render_output(result)
