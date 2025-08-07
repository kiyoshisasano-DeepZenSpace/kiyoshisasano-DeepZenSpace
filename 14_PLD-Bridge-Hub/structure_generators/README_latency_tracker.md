# ⏸️ Latency Tracker

Detects input latency events and classifies them based on Pause/Drift thresholds from Phase Loop Dynamics (PLD).

---

## ⚙️ Functionality

This script tracks time gaps between user interactions (e.g., UI events, button presses) and identifies when a **pause** occurs, based on a millisecond threshold.

| Feature         | Description                                  |
|----------------|----------------------------------------------|
| ⏱ Time Capture | Measures time between events (`start → end`) |
| 📊 Pause Label | Labels as `"⏸️ Pause"` if duration exceeds threshold |
| 📝 CSV Logging | Records all events into a local `.csv` file  |

---

## 🧠 PLD Theory Mapping

| Code Element     | PLD Concept                        | Source         |
|------------------|------------------------------------|----------------|
| `PAUSE_THRESHOLD_MS` | Cognitive latency / UI friction     | Paper 1 Fig.3 / Paper 2 |
| `pause_type`     | `⏸️ Pause` vs `✅ Smooth` classification | Drift boundary |
| CSV logging      | Loop trace of temporal irregularity | Field recovery |

---

## 🛠️ Configuration

| Variable             | Description                                     | Default |
|----------------------|-------------------------------------------------|---------|
| `PAUSE_THRESHOLD_MS` | Millisecond threshold for labeling a pause      | `800`   |
| `CSV_LOG_PATH`       | Output path for logging pause events (`.csv`)   | `"pause_log.csv"` |

> Threshold of 800ms based on:
> - PLD Paper 1 Fig.3 (Cognitive Drift Onset)
> - Modified Fitts’ Law for interface latency friction

---

## 🚀 Quick Example

```python
from latency_tracker import create_pause_event, log_event_to_csv
import time

print("🔴 Start interaction")
start = time.time()
input("⏸️ Press Enter when ready...")
end = time.time()

event = create_pause_event(start, end)
print("🧠 Detected Pause Event:", event)
log_event_to_csv(event)
```
---

## 🧠 Notes on Interpretation

**Extended Sensing Possibilities (Future)**:

| Input Modality    | Mapped Pause Type   | Rationale                        |
|-------------------|---------------------|----------------------------------|
| Eye tracking      | `⏸️ Cognitive`       | Blink/stare delay detection      |
| Scroll hesitation | `⏸️ UI Friction`     | Interaction breakdown            |
| Cursor wobble     | `⏸️ Latency Hold`    | Anticipatory pausing behavior    |

---

## 🤝 Contributing

**PLD-Theory Consistency Checklist**:
- [ ] Document which paper section your code corresponds to
- [ ] Add a comment link to `docs/zenodo_paper_links.md`  
- [ ] Ensure delay logic aligns with drift/repair models in Paper 1 & 2

---

## 📚 Related Resources

- 🧠 [PLD Theory Papers](../docs/zenodo_paper_links.md)
- 🧩 [UX Pattern Tracker](../notion_ui_templates/README_notion_ui_templates.md)
- 🤖 [Structure Generators Index](../structure_generators/README_structure_generators.md)
