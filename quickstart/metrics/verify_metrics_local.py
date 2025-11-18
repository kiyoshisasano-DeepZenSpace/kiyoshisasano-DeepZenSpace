#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Kiyoshi Sasano

# quickstart/run_minimal_engine.py
#!/usr/bin/env python3
# quickstart/run_minimal_engine.py
#
# Purpose:
#   Minimal working example for running the *real* PLD runtime engine.
#   Unlike `hello_pld_runtime.py` (teaching mock), this script executes
#   the actual controller, ingestion pipeline, and policy evaluation flow.
#
# When to use:
#   - Use this file when you want to verify the runtime installation.
#   - Start with `hello_pld_runtime.py` if you're learning the concepts first.
#
# Requirements:
#   - The folder `pld_runtime/` must exist or be installed.
#   - This script expects minimal runtime defaults (no configuration needed).
#
# Note:
#   If you want multiple scenarios (e.g. rag_empty/tool_error/normal),
#   consider creating a separate script like `run_engine_scenarios.py`
#   to keep this file focused and minimal.

"""
from __future__ import annotations

import sys
import uuid
from typing import Optional


def main(argv: Optional[list[str]] = None) -> int:
    """
    Run a minimal end-to-end PLD runtime controller example.

    This script intentionally uses a single hard-coded turn that simulates
    a "RAG returned no results" scenario, just to exercise:

      - controller wiring
      - policy evaluation
      - basic outcome fields
    """
    if argv is None:
        argv = sys.argv[1:]

    try:
        # --- Import from the real runtime package ---------------------------
        from pld_runtime.controllers.pld_controller import PldRuntimeController
        from pld_runtime.controllers.controller_config import ControllerConfig
        from pld_runtime.ingestion.normalization import NormalizedTurn
    except ImportError as e:
        print("❌ PLD runtime not available.", file=sys.stderr)
        print(f"   Import error: {e}", file=sys.stderr)
        print("   Tip: Ensure `pld_runtime/` is installed or on PYTHONPATH.", file=sys.stderr)
        print("   If you're exploring PLD concepts, run: `hello_pld_runtime.py`.", file=sys.stderr)
        return 1

    try:
        # --- Initialize the PLD runtime controller --------------------------
        config = ControllerConfig()
        controller = PldRuntimeController(config=config)
        session_id = f"session_{uuid.uuid4().hex}"

        # --- Construct a simulated drift condition --------------------------
        # Example: A RAG subsystem returns no usable results.
        turn: NormalizedTurn = NormalizedTurn(
            session_id=session_id,
            turn_id="turn_1",
            role="system",
            text="RAG returned [no results]",
            runtime={"source": "rag_service", "confidence": 0.0},
        )

        # --- Run the controller on a single turn ----------------------------
        outcome = controller.process_turn(turn)

    except Exception as e:
        print("❌ Runtime failure while executing controller.", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        return 1

    # --- Display raw operational outcome -----------------------------------
    print("\n--- PLD Runtime Controller Outcome ---\n")
    print(f"Session ID:     {getattr(outcome, 'session_id', 'N/A')}")
    print(f"Phase:          {getattr(outcome, 'phase', 'N/A')}")
    print(f"Next Action:    {getattr(outcome, 'next_action', 'N/A')}")

    policy_eval = getattr(outcome, "policy_evaluation", None)
    if policy_eval and getattr(policy_eval, "decisions", None):
        print("\nPolicy Decisions:")
        for decision in policy_eval.decisions:
            code = getattr(decision, "code", "N/A")

            # `decision.action` is expected to be an Enum; use `.value` for display.
            action = getattr(decision, "action", None)
            if action is None:
                action_str = "N/A"
            else:
                action_str = getattr(action, "value", str(action))

            print(f"  - {code}: {action_str}")

    trace_id = getattr(outcome, "trace_id", None)
    if trace_id:
        print(f"\nTrace ID:       {trace_id}")

    reentry_status = getattr(outcome, "reentry_status", None)
    if reentry_status is not None:
        print(f"Reentry Status: {reentry_status}")

    # --- Reading Guide ------------------------------------------------------
    print("\nHow to interpret:")
    print("  Phase        → Current PLD stage (DRIFT / REPAIR / REENTRY / CONTINUE)")
    print("  Next Action  → What the runtime recommends doing next")
    print("  Decisions    → Which enforcement policies were triggered")
    print("  Trace ID     → Identifier for logging or replay")
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
