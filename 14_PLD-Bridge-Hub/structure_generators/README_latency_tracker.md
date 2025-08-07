# 🕒 Latency Tracker — Phase Drift Logger

This module tracks latency patterns in user interactions and logs potential **Phase Drift** events.  
It is part of the **Phase Loop Dynamics (PLD)** toolkit, focusing on passive observation rather than classification or repair.

---

## ⚙️ Functionality

- ⏸ Detects pauses exceeding a defined threshold (e.g., 800ms)
- 🧠 Records drift segments for later analysis
- 📊 Outputs structured CSV logs for review or modeling

> Drift is not an error — it's rhythm under construction.  
> — *Phase Loop Dynamics Paper 1*

---

## 🧬 PLD Concept Mapping

| Code Element     | PLD Theory Concept     |
|------------------|------------------------|
| `input_latency`  | Drift vector (⏸️)       |
| `pause_threshold`| Latency boundary for phase transition |
| `csv_logger()`   | Drift trace emission   |
| `user_input_loop()` | Field presence monitoring |

---

## 🗂 Output Log Format

A sample CSV row:

```csv
timestamp,input_text,latency_ms,is_drift
2025-08-07 12:34:56,"What does resonance mean again?",935,True
```

Each row represents a user's input and its associated pause time.  
If the latency exceeds the threshold, it is flagged as a **Drift event**.

---

## 🚀 Usage

```bash
export OPENAI_API_KEY="your-key"  # If GPT-based enhancements are later added
python latency_tracker.py
```

During execution, the system will:

1. Prompt for input
2. Measure the delay since the last submission
3. Log the entry if the pause exceeds the defined threshold

> This module is ideal for **low-friction UX drift monitoring**, or as part of a **multi-phase analysis pipeline**.

---

## 📚 Related Resources

- 📘 PLD Theory Overview: [`docs/zenodo_paper_links.md`](../docs/zenodo_paper_links.md)
- 📦 UX Pause Classifier: [`structure_generators/pause_classifier_bot.py`](./pause_classifier_bot.py)
- 🌀 Reentry Detector: [`structure_generators/reentry_detector.py`](./reentry_detector.py)
- 🧩 Notion UI Kit: [`notion_ui_templates/README_notion_ui_templates.md`](../notion_ui_templates/README_notion_ui_templates.md)

---

## 🛠️ Configuration

- `PAUSE_THRESHOLD_MS`: Default is `800` ms — can be adjusted in code or via environment variable.
- `CSV_LOG_PATH`: Default output is `drift_log.csv` in current directory.

---

## 🧪 Example

```python
# Sample interaction with drift
User: "Wait... what was the repair operator again?"  [~900ms pause]
→ Logged as DRIFT

# Short latency
User: "Nevermind."  [~150ms pause]
→ Not logged
```

---

## 🧠 Notes on Interpretation

This tracker does not **interpret** drift — it **observes**.  
Classification or repair triggering should be handled by adjacent tools (e.g., `pause_classifier_bot.py`).

---

## 🤝 Contributing

We welcome contributions that align with PLD principles.

> Please read [`CONTRIBUTING.md`](../CONTRIBUTING.md) before submitting changes.

Minimal guidelines:

- Link any change in detection logic to PLD theoretical sources.
- Add reasoning to `docs/design_rationale.md` if new thresholds or metrics are introduced.
- Prioritize **rhythm-aligned instrumentation** over performance optimization.

---

## 📜 License

**License**: Creative Commons BY-NC 4.0  
SPDX-License-Identifier: CC-BY-NC-4.0  
Copyright (c) 2023–2025  
