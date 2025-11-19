---
title: "PLD Patterns — Runtime Behavior Guide"
version: 2025.1
maintainer: "Kiyoshi Sasano"
status: stable
category: behavioral_patterns
tags:
  - PLD
  - conversational agents
  - repair patterns
  - reentry patterns
  - applied AI design
---

# 🧩 PLD Patterns — Runtime Behavior Guide

This directory provides the **practical application layer** of the Phase Loop Dynamics (PLD) framework.

Where the metrics and schema define **what is measured**,  
patterns define **how an agent should behave** under drift, repair, and reentry conditions.

> The purpose of this module is to make agent behavior **predictable, recoverable, and aligned** — not just performant per-turn.

---

## 📌 Pattern Layer Structure

```txt
quickstart/patterns/
│
├── 01_llm/                  ← Model-side consistency & corrective behavior
├── 02_ux/                   ← Repair phrasing, pacing, visible alignment cues
├── 03_system/               ← Runtime orchestration, thresholds, failover logic
└── 04_integration_recipes/  ← Language/framework-specific examples (final stage)
```

Patterns are layered intentionally:

| Layer                   | Role                                                                  | When to Apply              |
| ----------------------- | --------------------------------------------------------------------- | -------------------------- |
| **LLM patterns**        | Ensure grounded generation and stable reasoning loops                 | Before user-facing testing |
| **UX patterns**         | Communicate corrections transparently and minimize friction           | During prototype runs      |
| **System patterns**     | Provide guardrails, retry logic, failover, and context management     | Pre-production             |
| **Integration recipes** | Bind patterns into frameworks (LangGraph, Assistants API, Rasa, etc.) | Production rollout         |

---

## 🔄 How Patterns Map to the PLD Loop

PLD patterns drive behavior during the **runtime lifecycle**:
```java
        ▼ Drift Detected (D1–D5)
    ┌───────────────────────────────┐
    │          REPAIR (R1–R4)       │
    └───────────────────────────────┘
                   ▼
         Reentry Observed (RE1–RE3)
                   ▼
             Continue / Outcome
```

Each phase corresponds to a pattern family:

| PLD Phase                 | Pattern Folder    |
| ------------------------- | ----------------- |
| Drift Detection + Control | 01_llm            |
| Soft / Hard Repair        | 01_llm + 02_ux    |
| Reentry Stabilization     | 02_ux + 03_system |
| Failover & Completion     | 03_system         |

---

## 📏 Standards Alignment

This patterns library works together with:
| Element              | File                                          |
| -------------------- | --------------------------------------------- |
| Event Schema         | `schemas/pld_event.schema.json`               |
| Derived Metrics      | `schemas/metrics_schema.yaml`                 |
| Dashboard            | `dashboards/reentry_success_dashboard.json`   |
| Operational Cookbook | `docs/07_pld_operational_metrics_cookbook.md` |

Patterns are not standalone — they are meant to be **observable and tuneable** using the metrics pipeline.

---

## 🎯 What These Patterns Solve

Without structured runtime behavior, agents exhibit:

- Silent corrections
- Repeated drift loops
- Invisible failure states
- Inconsistent recovery logic
- UX instability at scale

  With patterns applied:

  | Capability    | Behavior                                              |
| ------------- | ----------------------------------------------------- |
| Detectable    | Drift signals can be logged and measured              |
| Corrective    | Repairs respond proportionally to failure type        |
| Recoverable   | Reentry stabilizes and avoids looping behaviors       |
| Communicative | User-facing phrasing is predictable and bounded       |
| Governable    | Metrics → Policy → Runtime modification feedback loop |

---

## 🧪 How to Use These Patterns

| Stage         | What to do                                              | Reference                 |
| ------------- | ------------------------------------------------------- | ------------------------- |
| Prototype     | Apply LLM patterns first                                | `01_llm/`                 |
| Alpha testing | Add visible repair UX and timing controls               | `02_ux/`                  |
| Stabilization | Add system enforcement (policies, thresholds, failover) | `03_system/`              |
| Deployment    | Bind everything into a runtime framework                | `04_integration_recipes/` |

---

## 📝 Example: Minimal Pattern Binding

```text
User turn → Drift check → (If drift) → LLM Pattern → UX Repair → Reentry Pattern → Logging → Continue
```
In production:
```text
Event (raw) → Schema → Metrics → Dashboard → Tune Policy → Updated Patterns → Rerun
```

This creates a c**losed-loop governance model**.

---

## 📚 Next Steps

Proceed to:
> **01_llm/** — Model-side behavior anchoring and stable response strategies.
This folder contains:
- Repair-aware prompting
- Clarification templates for D1–D5 failure modes
- Reentry reinforcement phrasing
- Latency-aligned pacing templates

---

## Maintaining Alignment Over Time

Patterns should evolve when:
- Drift categories change
- Repair effectiveness drops
- VRL increases beyond acceptable range
- Failover rate (FR) exceeds baseline thresholds

Metrics → inform → patterns.

Patterns → guide → behavior.

Behavior → produces → measurable stability.

---

## License

Creative Commons — **CC BY 4.0**
© 2025 — DeepZenSpace / Contributors

> **Patterns turn PLD from a theory into a repeatable behavior system**.
