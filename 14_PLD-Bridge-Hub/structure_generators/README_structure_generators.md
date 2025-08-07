# 🧠 Structure Generators — PLD-based Interaction Bots

This directory contains prototype tools that generate or classify interaction structures according to **Phase Loop Dynamics (PLD)**.
Each generator models structural dynamics such as **Pause**, **Drift**, **Repair**, or **Reentry**, and maps these to UI decisions or dialogue system actions.

---

## 📦 Current Bot: `pause_classifier_bot.py`

This GPT-powered classifier tags user interaction logs with PLD-based **pause types**, such as:

```python
PAUSE_TYPES = [
    "⏸️ Cognitive",      # PLD Paper1: Latency-driven phase shift
    "⏸️ UI Friction",    # PLD Paper2: Forced drift by interface
    "⏸️ Disengagement",  # PLD Paper1: Unrepaired drift (see also: Recombination failure in Paper2)
    "⏸️ Repair",         # PLD Paper2: Cue-triggered realignment
    "⏸️ Latency Hold"    # PLD Paper1: Intentional pause
]
```

🔍 Classification is performed via `GPT-4`, using contextual reasoning and pause pattern analysis. 

#### Example Prompt Behavior
```text
Log > User hovered over the back button but paused for 3.2s
🧠 Classification: ⏸️ UI Friction
💬 Reason: Long hesitation near navigation element suggests structural hesitation.
```

✅ Works in both **command-line** and **function-based API** modes.  
☁️ Usable via **Colab / Spaces** for non-devs.

---

## 🔄 PLD Generator Matrix

|                | Pause | Drift | Repair | Reentry |
|----------------|-------|-------|--------|---------|
| **Classifier** | ✅    |       | ✅     |         |
| **Tracker**    |       | 🟡    |        |         |
| **Builder**    |       |       | 🟡     | 🟡      |

→ Tools and their conceptual coverage in PLD theory.

---

## 🧩 PLD Theory Links

- 📘 [`zenodo_paper_links.md`](../docs/zenodo_paper_links.md): Core theoretical definitions of Pause/Drift/Repair/Resonance
- 🗂️ [`notion_ui_templates`](../notion_ui_templates/README_notion_ui_templates.md): Related Notion template implementations

---

## 🛠 Planned Generators (Coming Soon)

| Generator Name         | Description                                               | Status    |
|------------------------|-----------------------------------------------------------|-----------|
| `reentry_detector.py`  | Detects reentrant patterns (user resuming intent later)   | 🟡 Draft   |
| `drift_tracker.py`     | Scores conversational or UI drift over interaction logs   | 🟡 Planned |
| `structure_builder.py` | Generates Notion or dialogue node structure via LLM       | 🟡 Planned |
| `repair_suggester.py`  | Provides soft correction prompts based on pause type      | 🟡 Planned |

These tools aim to support structure-aware design decisions across UX, HCI, and NLP.

---

## 📜 License

**Creative Commons BY-NC 4.0**
- Attribution required / No commercial use without permission
- Drift-aware extensions encouraged over raw optimization

---
