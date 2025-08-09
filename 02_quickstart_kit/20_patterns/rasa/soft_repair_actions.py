from typing import Any, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from datetime import datetime
from pathlib import Path
import json

LOGS = Path(__file__).resolve().parent.parent / "logs"
LOGS.mkdir(exist_ok=True)
LOG_FILE = LOGS / "pld_events.jsonl"

def log_event(event_type: str, tracker: Tracker, metadata: Dict[str, Any] = None):
    payload = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "session_id": tracker.sender_id,
        "metadata": metadata or {}
    }
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")

class ActionCheckRepairAttempts(Action):
    def name(self) -> str:
        return "action_check_repair_attempts"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Read current attempts and simulate a latency hold to match PLD L3
        attempts = tracker.get_slot("repair_attempts") or 0
        latency_ms = 900

        # Log drift (L2) and latency hold (L3) consistently with the schema
        last_intent = tracker.latest_message.get("intent", {})
        log_event("drift_detected", tracker, {"attempt": attempts + 1, "last_intent": last_intent})
        log_event("latency_hold", tracker, {
            "duration_ms": float(latency_ms),
            "reason": "soft_repair_probe"
        })

        if attempts >= 2:
            log_event("repair_failed", tracker, {"attempt": attempts})
            return [FollowupAction("utter_fallback_repair")]
        else:
            log_event("repair_triggered", tracker, {"attempt": attempts + 1})
            return [
                SlotSet("repair_attempts", attempts + 1),
                FollowupAction("utter_soft_repair")
            ]

class ActionStoreReentryFlag(Action):
    def name(self) -> str:
        return "action_store_reentry_flag"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        prior_context_id = tracker.get_slot("prior_context_id") or "unknown"
        log_event("reentry_success", tracker, {"prior_context_id": prior_context_id})
        return [SlotSet("resumed_from_repair", True)]
