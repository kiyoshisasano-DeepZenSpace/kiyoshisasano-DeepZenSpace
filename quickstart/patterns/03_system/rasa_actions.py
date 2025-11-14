# patterns/03_system/rasa_actions.py
# PLD Applied-AI Edition
#
# Soft Repair / Drift Detection / Reentry Guard actions for Rasa
# --------------------------------------------------------------
# Depends on:
#   - slots: user_goal, constraint_price, constraint_category, repair_state
#   - responses: see rasa_soft_repair.yml
#
# Maintainer: Kiyoshi Sasano

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, FollowupAction


# -------------------------------------------------------------------
# Helper: simple drift classifier (placeholder, customize as needed)
# -------------------------------------------------------------------


def classify_drift(tracker: Tracker) -> Text:
    """Very lightweight drift classifier.

    This is intentionally simple and rule-based so teams
    can replace it with their own model-based or heuristic logic.

    Returns:
        "drift_information" | "drift_repeated" | "drift_ambiguous" | "none"
    """
    latest_intent = tracker.get_intent_of_latest_message(skip_fallback_intent=False)
    last_bot_utter = tracker.get_last_event_for("bot", action_name=None)

    # Fallback / confusion → ambiguous drift
    if latest_intent == "fallback":
        return "drift_ambiguous"

    # Repeated same user message → repeated drift
    last_user_events = [
        e
        for e in tracker.events
        if e.get("event") == "user" and e.get("text") is not None
    ]
    if len(last_user_events) >= 2:
        last_text = last_user_events[-1]["text"]
        prev_text = last_user_events[-2]["text"]
        if last_text.strip().lower() == prev_text.strip().lower():
            return "drift_repeated"

    # Simple placeholder: if last bot message apologized or looked uncertain → information drift
    if last_bot_utter:
        text = (last_bot_utter.get("text") or "").lower()
        if "sorry" in text or "couldn't find" in text or "no results" in text:
            return "drift_information"

    return "none"


# -------------------------------------------------------------------
# Action: Detect Drift
# -------------------------------------------------------------------


class ActionDetectDrift(Action):
    """Detects potential drift and annotates it via the `repair_state` slot."""

    def name(self) -> Text:
        return "action_detect_drift"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        drift_label = classify_drift(tracker)

        # Default: no drift
        if drift_label == "none":
            return []

        # Store drift classification in slot
        events: List[EventType] = [SlotSet("repair_state", drift_label)]

        # Optionally log to console (for debugging)
        print(f"[PLD] Drift detected: {drift_label}")

        return events


# -------------------------------------------------------------------
# Action: Apply Soft Repair (fallback handler)
# -------------------------------------------------------------------


class ActionApplySoftRepair(Action):
    """Central Soft Repair handler.

    This is configured as `core_fallback_action_name` in rasa_soft_repair.yml,
    so it is invoked when Rasa is unsure how to respond.
    """

    def name(self) -> Text:
        return "action_apply_soft_repair"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        repair_state = tracker.get_slot("repair_state")

        events: List[EventType] = []

        # If no drift is marked yet, treat as generic ambiguity
        if not repair_state or repair_state == "none":
            events.append(SlotSet("repair_state", "drift_ambiguous"))
            repair_state = "drift_ambiguous"

        # Route based on drift type
        if repair_state == "drift_information":
            # Likely DB/API mismatch or incorrect assumption
            dispatcher.utter_message(response="utter_soft_repair_add_options")

        elif repair_state == "drift_repeated":
            # Multiple failed attempts → step towards relaxing constraints
            dispatcher.utter_message(response="utter_soft_repair_relax_constraints")

        elif repair_state == "drift_ambiguous":
            # Unclear intent or low NLU confidence
            dispatcher.utter_message(response="utter_soft_repair_clarify")

        else:
            # Fallback behavior if unexpected state
            dispatcher.utter_message(response="utter_soft_repair_clarify")

        print(f"[PLD] Soft repair applied for state: {repair_state}")

        return events


# -------------------------------------------------------------------
# Action: Reentry Guard
# -------------------------------------------------------------------


class ActionReentryGuard(Action):
    """Ensures that after a repair, we safely reenter the main task.

    Typically used after the user `affirm`s or clarifies constraints.
    It can:
      - clear or downgrade `repair_state`
      - log that reentry has occurred
    """

    def name(self) -> Text:
        return "action_reentry_guard"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        current_state = tracker.get_slot("repair_state")

        print(f"[PLD] Reentry guard invoked. Previous repair_state={current_state}")

        # Once reentry is confirmed, we clear the repair state
        events: List[EventType] = [SlotSet("repair_state", None)]

        # Optional: could emit a structured log event for PLD metrics
        # Example (pseudo):
        # log_pld_event(
        #     event_type="reentry",
        #     session_id=tracker.sender_id,
        #     metadata={"previous_repair_state": current_state},
        # )

        return events
