# README — PLD Applied Pattern Library  
*(Quickstart Edition for Agent Developers)*

This folder provides ready-to-use implementation patterns for integrating  
**PLD behaviors — Drift → Repair → Reentry → Resonance → Outcome**  
into LLM agents, tool-using systems, TOD frameworks, and conversational UX.

Unlike theory or taxonomy, this folder is **practical**.  
Every pattern answers one question:

> **How do I make my system behave correctly when interaction state changes?**

---

## 🔧 What This Folder Provides

| Layer | Purpose | Who Uses It |
|-------|---------|-------------|
| **LLM Patterns** | Detect drift, apply soft repair, confirm reentry | Prompt engineers, agent developers |
| **UX Patterns** | Maintain pacing, timing, and user trust | Designers, PMs, conversation UX |
| **System Patterns** | Execute recovery logic + telemetry in frameworks | LangChain/LangGraph, Rasa, custom runtimes |

Patterns are modular and stackable — adopt one or integrate all as a **behavior policy layer**.

---

## 📁 Folder Structure

```
patterns/
│
├── 01_llm/                       ← Prompt + agent behavior patterns
│   ├── drift_detection_prompts.md
│   ├── soft_repair_templates.md
│   └── reentry_confirmation_patterns.md
│
├── 02_ux/                        ← Timing + interaction design patterns
│   ├── figma_latency_hold.md
│   ├── failure_states_design.md
│   └── timing_patterns_catalog.md
│
├── 03_system/                    ← Executable patterns for frameworks
│   ├── rasa_soft_repair.yml
│   ├── rasa_actions.py
│   ├── langgraph_example.md
│   └── logging_examples.md
│
└── 04_integration_recipes/       ← (Next stage — runnable agents)
    └── README_recipes.md
```

> 📌 If patterns feel like **behavioral building blocks**,  
> recipes are where they become **runnable agents with PLD runtime logic.**

---

## 🧩 Pattern Design Principles

All patterns follow five core PLD rules:

| Rule | Meaning | Example |
|------|---------|---------|
| **Minimal Intrusion** | Repair without breaking flow | Soft repair before reset |
| **State Awareness** | Never assume memory is correct | Confirm constraints after repair |
| **Predictable Rhythm** | Timing prevents perceived failure | Latency hold → progressive update |
| **Explicit Recovery** | Users must know when repair happened | Reentry checkpoint phrasing |
| **Operational Logging** | All behavior emits telemetry | `pld_event.schema.json` compatible |

---

## 🚦 When to Use Which Pattern

| Situation | Recommended Pattern | Folder |
|----------|----------------------|--------|
| Output contradicts prior state | Soft Repair + Reentry | `01_llm/` |
| User hesitates or pause is long | Latency + UX Timing Pattern | `02_ux/` |
| Pipeline/tool/system failure | Hard Repair + Logging Pattern | `03_system/` |
| Multi-turn reasoning drift risk | Periodic State Confirmation | `01_llm/` |

---

## 📈 Telemetry Compatibility

All patterns align with:

- `metrics_schema.yaml`  
- `pld_event.schema.json`  
- MultiWOZ Applied Interaction baselines  
  (`multiwoz_2.4_n200/`)

Meaning:  
**Implementing a pattern automatically generates measurable stability signals.**

---

## 🧪 Incremental Adoption Guide

| Phase | Action |
|-------|--------|
| **Step 1** | Add soft repair templates |
| **Step 2** | Add drift detection + confirmation checkpoints |
| **Step 3** | Add UX latency + pacing behaviors |
| **Step 4** | Enable telemetry mapping |
| **Step 5** | Activate reentry policies |
| **Step 6** | **Move to Integration Recipes to build a working PLD agent → `/04_integration_recipes/`** |

> Patterns teach stability.  
> Recipes apply stability to a **full agent runtime.**

---

## 🔚 Summary

This folder is **not documentation — it’s a toolkit.**

Use these patterns to:

✔ stabilize agent behavior  
✔ prevent cascading drift  
✔ ensure transparent recovery  
✔ preserve shared context  
✔ increase task completion + user trust  

Patterns are designed to be copied, automated, integrated, and extended into internal libraries.

> When ready, continue to:  
> 👉 `quickstart/patterns/04_integration_recipes/README_recipes.md`  
> to turn these patterns into a **functioning PLD-enabled agent.**

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY-NC-4.0**
