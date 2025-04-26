from fastapi import FastAPI, Body
from models import PhaseState, Feedback
from datetime import datetime
import os
import json
import csv

app = FastAPI()

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

latest_phase_state = None

@app.post("/phase_state")
async def receive_phase_state(phase_state: PhaseState = Body(...)):
    global latest_phase_state
    latest_phase_state = phase_state

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    filename = f"phase_{timestamp}.json"
    filepath = os.path.join(LOG_DIR, filename)

    data = phase_state.dict()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    csv_file = os.path.join(LOG_DIR, "phase_log.csv")
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if os.stat(csv_file).st_size == 0:
            writer.writerow(["timestamp", "current_phase", "drift_risk", "latency_rhythm"])
        writer.writerow([
            timestamp,
            phase_state.phase_state.current_phase,
            phase_state.phase_state.drift_risk,
            phase_state.phase_state.latency_rhythm
        ])

    return {"status": "ok"}

@app.get("/current_phase")
async def get_current_phase():
    if not latest_phase_state:
        return {"status": "no phase data received yet"}
    return {"current_phase_state": latest_phase_state}

@app.post("/feedback")
async def receive_feedback(feedback: Feedback = Body(...)):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    csv_file = os.path.join(LOG_DIR, "feedback_log.csv")
    with open(csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if os.stat(csv_file).st_size == 0:
            writer.writerow(["timestamp", "feedback_type", "details"])
        writer.writerow([
            timestamp,
            feedback.feedback_type,
            feedback.details
        ])

    return {"status": "feedback recorded"}

@app.get("/feedback_log")
async def get_feedback_log():
    feedbacks = []
    csv_file = os.path.join(LOG_DIR, "feedback_log.csv")
    if os.path.exists(csv_file):
        with open(csv_file, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                feedbacks.append(row)
    return {"feedback_log": list(reversed(feedbacks))}
