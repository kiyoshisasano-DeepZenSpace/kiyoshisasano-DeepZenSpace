# latency_tracker.py
# Tracks latency between UI events or user inputs, mapping delays to PLD pause types

import time
import csv
import os
from typing import List, Dict

# 📘 PLD Theory Mapping:
# - Latency beyond threshold = ⏸️ Pause event
# - PLD Paper 1: Drift as phase delay
# - PLD Paper 2: UI-friction-induced delay (Fitts' Law deviation)

# ✅ Configuration
PAUSE_THRESHOLD_MS = 800  # Based on PLD Paper1 Fig.3 & interaction latency norms
CSV_LOG_PATH = "pause_log.csv"

# ⏸️ Pause Event Structure
def create_pause_event(start: float, end: float) -> Dict:
    duration_ms = (end - start) * 1000
    label = "⏸️ Pause" if duration_ms > PAUSE_THRESHOLD_MS else "✅ Smooth"
    return {
        "start_time": start,
        "end_time": end,
        "duration_ms": round(duration_ms, 2),
        "pause_type": label
    }

# 🚀 Logger
def log_event_to_csv(event: Dict, path: str = CSV_LOG_PATH):
    if not path.endswith(".csv"):
        raise ValueError("Log path must be a .csv file")
    file_exists = os.path.isfile(path)
    with open(path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=event.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(event)

# 🧪 Example Usage
if __name__ == "__main__":
    print("🔴 Recording start time...")
    start = time.time()
    input("⏸️ Press Enter after pausing...")
    end = time.time()

    event = create_pause_event(start, end)
    print("🧠 Detected Pause Event:", event)
    log_event_to_csv(event)
