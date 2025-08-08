# 🧠 Structural Generators for Phase Loop Dynamics

This folder contains code modules that automatically generate structural patterns based on the **Phase Loop Dynamics (PLD)** framework.  
These include **pause-drift classification bots**, **loop structure builders**, and **coherence-based feedback routines**.

---

## 🧩 Module Overview

| Module / Folder             | Description |
|-----------------------------|-------------|
| `pause_classifier/`         | Lightweight LLM interface to detect user pauses and classify them by type |
| `loop_generator/`           | Builds loop structures from classified phases using PLD algebra |
| `pld_interface/`            | Shared utilities for coherence field computation, vector metrics, etc. |
| `GENERATOR_MODULES_OVERVIEW.md` | This file. Describes the overall logic and navigation of the structure generator stack |

---

## 🚀 Try the Bots (Coming Soon)

- 🧪 **Colab prototype** for structure classification  
- 🤖 **HF Spaces demo** for interactive chat with structural reflection  
- ⌨️ Local execution via `main.py` with configuration presets

```bash
python main.py --mode=pause_classify --input="I was trying to submit but the button disappeared"
```
## 🔄 Cross-Repo Synergy

This module set is designed to work in coordination with:

- 🧰 **Notion UI Templates**  
  → [UX Pause Rhythm Tracker Starter Kit](../notion_ui_templates/NOTION_TEMPLATES_OVERVIEW.md)

- 📘 **Theoretical Foundations**  
  → [Zenodo Papers & Definitions](../docs/zenodo_paper_links.md)

- 🌐 **Bridge Hub Overview**  
  → [PLD_OVERVIEW.md](../PLD_OVERVIEW.md)

These links provide the theoretical context, deployment examples, and interface guidelines for integrating structural generators into UX workflows or research pipelines.
