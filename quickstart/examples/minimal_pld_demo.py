# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2025 Kiyoshi Sasano
"""
minimal_pld_demo.py

Minimal, vendor-agnostic example of the PLD runtime loop:

    Detect Drift → Repair → Reenter Context → Continue → Outcome

- No external LLM client required (uses a fake stub by default)
- Safe to run as-is: `python minimal_pld_demo.py`
- You can later replace `fake_llm_reply()` with a real LLM call.

This script is intentionally simple:
it shows how a single turn can produce a PLD event log.
"""

import json
import uuid
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# 1. Fake LLM stub (replace with your own client if desired)
# ---------------------------------------------------------------------------

def fake_llm_reply(user_message: str) -> str:
    """
    Very small stub that intentionally "drifts":
    User asks for a flight, but the system talks about hotels.
    """
    return (
        "Here are some hotel options in Berlin. "
        "You can choose from several great areas to stay."
    )


# ---------------------------------------------------------------------------
# 2. Drift detection / classification (toy heuristic)
# ---------------------------------------------------------------------------

def detect_drift(user_message: str, system_reply: str) -> dict:
    """
    Extremely simple heuristic:
    - If user mentions 'flight' but reply talks about 'hotel', treat as intent drift.
    - Otherwise: assume no drift for this demo.

    In a real system, this would call a classifier or PLD operator.
    """
    user_wants_flight = "flight" in user_message.lower()
    reply_mentions_hotel = "hotel" in system_reply.lower()

    if user_wants_flight and reply_mentions_hotel:
        return {
            "present": True,
            "type": "D3_intent_drift",
            "reason": "User asked for a flight, system responded with hotels.",
        }

    return {
        "present": False,
        "type": None,
        "reason": None,
    }


# ---------------------------------------------------------------------------
# 3. Soft Repair + Reentry (scripted for this minimal example)
# ---------------------------------------------------------------------------

def build_soft_repair_reply(user_message: str) -> str:
    """
    In PLD terms: a Soft Repair should be visible, minimal, and stabilizing.
    """
    return (
        "I answered with hotel options, but you asked about a flight. "
        "Let me correct that and focus on booking your flight to Berlin."
    )


def build_reentry_prompt(user_message: str) -> str:
    """
    Reentry = restore shared alignment before continuing.
    """
    return (
        "To confirm: you want to book a flight to Berlin next Tuesday, "
        "and you'd like economy class. Is that correct?"
    )


# ---------------------------------------------------------------------------
# 4. PLD Event construction (aligned with the PLD event schema)
# ---------------------------------------------------------------------------

def build_pld_event(
    session_id: str,
    turn_index: int,
    user_message: str,
    system_reply: str,
    drift_info: dict,
) -> dict:
    """
    Build a single PLD event object for this turn.

    This is a simplified, schema-aligned example:
    - drift
    - repair
    - reentry
    - outcome
    - metadata
    """
    drift_present = drift_info["present"]

    if drift_present:
        repair_block = {
            "present": True,
            "mode": "soft",          # "soft" or "hard"
            "code": "R1_clarify",    # example repair code
        }
        reentry_block = {
            "present": True,
            "code": "RE1_confirm",
            "success": True,
        }
        outcome_status = "complete"
    else:
        repair_block = {
            "present": False,
            "mode": None,
            "code": None,
        }
        reentry_block = {
            "present": False,
            "code": None,
            "success": None,
        }
        outcome_status = "complete"

    event = {
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "turn_index": turn_index,
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "user_message": user_message,
        "system_reply": system_reply,

        "drift": {
            "present": drift_present,
            "type": drift_info["type"],
            "reason": drift_info["reason"],
        },
        "repair": repair_block,
        "reentry": reentry_block,
        "outcome": {
            "status": outcome_status,    # e.g. "complete", "partial", "failed"
        },

        "metadata": {
            "demo": True,
            "source": "minimal_pld_demo",
            "notes": "Toy example to show Phase Loop Dynamics logging.",
        },
    }

    return event


# ---------------------------------------------------------------------------
# 5. Main demo routine
# ---------------------------------------------------------------------------

def run_demo() -> None:
    """
    Run a single-turn scenario:

    1. User asks for a flight to Berlin.
    2. Fake LLM responds with hotel suggestions (intent drift).
    3. We detect drift.
    4. We script a soft repair and reentry.
    5. We emit a PLD event log to stdout in JSON.
    """
    session_id = str(uuid.uuid4())
    turn_index = 0

    user_message = "Book a flight to Berlin next Tuesday in economy class."
    system_reply = fake_llm_reply(user_message)

    # 1) Detect drift
    drift_info = detect_drift(user_message, system_reply)

    # 2) Show what happened at the conversational level
    print("\n=== Conversation Trace (Demo) ===")
    print(f"User   : {user_message}")
    print(f"System : {system_reply}")

    if drift_info["present"]:
        soft_repair_reply = build_soft_repair_reply(user_message)
        reentry_prompt = build_reentry_prompt(user_message)

        print("\n[PLD] Drift detected:", drift_info["reason"])
        print("[PLD] Soft Repair   :", soft_repair_reply)
        print("[PLD] Reentry Check :", reentry_prompt)
    else:
        print("\n[PLD] No drift detected in this demo turn.")

    # 3) Build PLD event object
    event = build_pld_event(
        session_id=session_id,
        turn_index=turn_index,
        user_message=user_message,
        system_reply=system_reply,
        drift_info=drift_info,
    )

    # 4) Emit as JSON (this is what metrics / analytics will consume)
    print("\n=== PLD Event JSON (Demo) ===")
    print(json.dumps(event, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_demo()

