# 🧠 PLD Structure Generators — Overview

This directory contains **Phase Loop Dynamics (PLD)**-based modules that classify, track, and generate interaction structures such as **Pause**, **Drift**, **Repair**, and **Reentry**.

---

## 📂 Module Index

| Module / File                            | Purpose |
|------------------------------------------|---------|
| `pause_classifier_bot.py`                | GPT-based pause type classifier (⏸️ Cognitive, UI Friction, etc.) |
| `latency_tracker.py`                     | Detects latency events exceeding a threshold |
| `reentry_detector.py`                     | Detects when a user resumes a previously dropped intent |
| `README_latency_tracker.md`               | Detailed latency tracker documentation |
| `README_reentry_detector.md`              | Detailed reentry detector documentation |
| `README_structure_generators.md`          | PLD generator concepts and theory links |
| `GENERATOR_MODULES_OVERVIEW.md`           | Module descriptions and navigation |

---

## 🚀 How to Try

Run individual modules directly:

```bash
# Example: Classify a pause
python pause_classifier_bot.py --input "User hesitated for 3s before clicking"

# Example: Track latency
python latency_tracker.py
```
Some modules require API keys (e.g., OpenAI) — see each module's README.

---

## 🔄 Cross-Repo Synergy

- **Notion UI Templates** → [NOTION_TEMPLATES_OVERVIEW.md](../notion_ui_templates/NOTION_TEMPLATES_OVERVIEW.md)  
- **PLD Theory Papers** → [Zenodo Papers & Definitions](../docs/zenodo_paper_links.md)  
- **Bridge Hub Overview** → [PLD_OVERVIEW.md](../PLD_OVERVIEW.md)

---

## 📜 License

**CC BY-NC 4.0** — Attribution required, non-commercial use only.
