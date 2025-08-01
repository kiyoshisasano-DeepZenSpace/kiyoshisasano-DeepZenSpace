from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction

class ActionCheckRepairAttempts(Action):
    def name(self) -> str:
        return "action_check_repair_attempts"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        attempts = tracker.get_slot("repair_attempts") or 0
        if attempts >= 2:
            return [FollowupAction("utter_fallback_repair")]
        else:
            return [
                SlotSet("repair_attempts", attempts + 1),
                FollowupAction("utter_soft_repair")
            ]

class ActionStoreReentryFlag(Action):
    def name(self) -> str:
        return "action_store_reentry_flag"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [SlotSet("resumed_from_repair", True)]
