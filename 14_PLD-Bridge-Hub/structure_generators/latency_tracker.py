# latency_tracker.py
# Tracks latency patterns in user interaction — for PLD Pause detection

import time
from typing import List, Dict, Optional
import csv

# 📘 Related Theory:
# - PLD Paper 1: Drift as latency-based deviation
# - PLD Paper 2: Delay segment as precursor to repair/reentry

# Optional config
LATENCY_THRESHOLD = 1.5  # seconds (minimum pause to count as significant)
CSV_LOG_PATH = "latency_log.csv"

class LatencyEvent:
    def __init__(self, start_time: float):
        self.start = start_time
        self.end: Optional[float] = None
        self.duration: Optional[float] = None

    def stop(self):
        self.end = time.time()
        self.duration = round(self.end - self.start, 3)

    def to_dict(self) -> Dict:
        return {
            "start": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.start)),
            "end": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.end)) if self.end else "",
            "duration_sec": self.duration if self.duration else ""
        }

class LatencyTracker:
    def __init__(self):
        self.events: List[LatencyEvent] = []
        self.current_event: Optional[LatencyEvent] = None

    def mark_pause_start(self):
        self.current_event = LatencyEvent(time.time())

    def mark_pause_end(self):
        if not self.current_event:
            return
        self.current_event.stop()
        if self.current_event.duration and self.current_event.duration >= LATENCY_THRESHOLD:
            self.events.append(self.current_event)
            print(f"⏸️ Significant pause recorded: {self.current_event.duration} sec")
        else:
            print(f"⏱️ Pause too short: {self.current_event.duration} sec — ignored")
        self.current_event = None

    def export_csv(self, path=CSV_LOG_PATH):
        with open(path, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["start", "end", "duration_sec"])
            writer.writeheader()
            for event in self.events:
                writer.writerow(event.to_dict())
        print(f"✅ Latency log exported to {path}")

if __name__ == "__main__":
    tracker = LatencyTracker()
    print("🌀 Latency Tracker started. Press Enter to simulate pause start/end.")

    while True:
        cmd = input("▶️ Press Enter to toggle (or type 'q' to quit): ")
        if cmd.strip().lower() == 'q':
            break
        if not tracker.current_event:
            tracker.mark_pause_start()
        else:
            tracker.mark_pause_end()

    tracker.export_csv()
