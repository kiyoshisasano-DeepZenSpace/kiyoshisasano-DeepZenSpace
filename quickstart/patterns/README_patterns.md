# README — PLD Applied Pattern Library  
*(Quickstart Edition for Agent Developers)*

This folder provides ready-to-use implementation patterns for integrating  
**PLD behaviors — Drift → Repair → Reentry → Resonance → Outcome**  
into LLM agents, tool-using systems, TOD frameworks, and conversational UX.

Unlike theory or taxonomy, this folder is **practical**.  
Each pattern focuses on a single applied question:

> **How can a system respond effectively when interaction state shifts or drifts?**

---

## 🔧 What This Folder Provides

| Layer | Purpose | Who Uses It |
|-------|---------|-------------|
| **LLM Patterns** | Detect drift, apply soft repair, confirm reentry | Prompt engineers, agent developers |
| **UX Patterns** | Maintain pacing, timing, and user trust | Designers, PMs, conversation UX |
| **System Patterns** | Execute recovery logic + telemetry in frameworks | LangChain/LangGraph, Rasa, custom runtimes |

Patterns are modular and stackable — they can be adopted individually or combined as a **behavior policy layer**.

---

## 📁 Folder Structure

```
patterns/
│
├── 01_llm/ ← Prompt + agent behavior patterns
│ ├── drift_detection_prompts.md
│ ├── soft_repair_templates.md
│ └── reentry_confirmation_patterns.md
│
├── 02_ux/ ← Timing + interaction design patterns
│ ├── figma_latency_hold.md
│ ├── failure_states_design.md
│ └── timing_patterns_catalog.md
│
├── 03_system/ ← Executable patterns for frameworks
│ ├── rasa_soft_repair.yml
│ ├── rasa_actions.py
│ ├── langgraph_example.md
│ └── logging_examples.md
│
└── 04_integration_recipes/ ← (Optional next step: runnable examples)
└── README_recipes.md
```


> 📌 If patterns are the **behavior building blocks**,  
> recipes provide **examples of how they may be assembled into a working runtime.**

---

## 🧩 Pattern Design Principles

All patterns follow five core PLD principles:

| Rule | Meaning | Example |
|------|---------|---------|
| **Minimal Intrusion** | Repair without breaking flow | Soft repair before reset |
| **State Awareness** | Never assume memory is correct | Confirm constraints after repair |
| **Predictable Rhythm** | Timing reduces perceived failure | Latency hold → progressive update |
| **Explicit Recovery** | Recovery should be acknowledgeable | Reentry checkpoint phrasing |
| **Operational Logging** | Everything emits telemetry | `pld_event.schema.json` compatible |

---

## 🚦 When to Use Which Pattern

| Situation | Recommended Pattern | Folder |
|----------|----------------------|--------|
| Output contradicts prior state | Soft Repair + Reentry | `01_llm/` |
| User hesitates or pauses long | Latency + UX Timing Pattern | `02_ux/` |
| Tool or API execution fails | Hard Repair + Logging Pattern | `03_system/` |
| Multi-turn alignment risk | Periodic State Confirmation | `01_llm/` |

---

## 📈 Telemetry Compatibility

All patterns align with:

- `metrics_schema.yaml`  
- `pld_event.schema.json`  
- MultiWOZ Applied Interaction baselines (`multiwoz_2.4_n200/`)

Meaning:  
**Using a pattern automatically produces measurable stability signals.**

---

## 🧪 Optional Adoption Path

The following order is one common way to adopt patterns incrementally:

| Phase | Action |
|-------|--------|
| **Step 1** | Add soft repair templates |
| **Step 2** | Add drift detection + reentry checkpoints |
| **Step 3** | Add UX latency + pacing behaviors |
| **Step 4** | Enable telemetry mapping |
| **Step 5** | Add reentry policies |
| **Step 6 (Optional)** | Explore integration recipes to build a full PLD-enabled runtime |

> Patterns support stability.  
> Recipes show how stability can be applied to a working agent.

---

## 🔚 Summary

This folder is **not abstract documentation — it’s a toolkit.**

Use these patterns to:

✔ stabilize behavior across turns  
✔ prevent cascading drift  
✔ ensure recoverable state alignment  
✔ maintain transparency and user trust  
✔ increase task continuity and completion rates  

Patterns are designed to be copied, adapted, versioned, and integrated into internal libraries.

> When ready, you *may* continue to:  
> 👉 `quickstart/patterns/04_integration_recipes/README_recipes.md`  
> to explore how patterns can operate as part of a runnable PLD agent.

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY-4.0**

> Licensing Notice

All implementation `.py` files in this directory are provided under the **Apache License 2.0**
to allow reuse in production systems.

All documentation, patterns, recipes, and prompt design materials (`.md`, `.yml`, `.yaml`)
are licensed under **CC BY 4.0** as part of the PLD methodology.

This ensures:
- Free and open reuse of implementation code
- Attribution-preserving propagation of the conceptual framework



