---
title: "PLD Applied Quickstart Kit"
version: "2025 Edition"
status: stable
maintainer: "Kiyoshi Sasano"
tags:
  - PLD
  - LLM Agents
  - Repair Systems
  - Drift Detection
  - Applied AI
---

# 🚀 PLD Applied Quickstart Kit  
**For LLM Agents, Orchestrators, and Conversational Systems (2025 Edition)**  

> PLD is easiest to understand when experienced, not read.

This kit provides practical materials for implementing **Phase Loop Dynamics (PLD)** in real AI systems — including drift detection, repair workflows, reentry logic, and runtime evaluation.

PLD is not just a conceptual framework —  
it is a **runtime interaction control model** for applied AI.

--- After title and introduction ---

 PLD is not just a conceptual framework —
 it is a runtime interaction control model for applied AI.

### 🏁 Start Here — Run the Minimal Runtime

> `hello_pld_runtime.py` is intentionally located inside `quickstart/` —  
> it is a learning-oriented runtime demonstration, not part of the PLD engine source.

You can run the minimal working example immediately:

```bash
python hello_pld_runtime.py
```

Try custom input:

```bash
python hello_pld_runtime.py "Can we switch topics and talk about cooking?"
```

Run all example scenarios:

```bash
python hello_pld_runtime.py --examples
```

➡️ This is the fastest path to understanding what PLD *feels like* in runtime.


---

## 1 — Why PLD Exists

LLMs rarely fail because they lack knowledge —  
they fail because they lose **task alignment across turns.**

| Failure Mode | Result |
|--------------|--------|
| Loss of grounding | User distrust |
| Incorrect propagation of prior context | Cascading errors |
| Tool/API mismatch without acknowledgement | Workflow stalls |
| Full resets | Lost session state & user confidence |

PLD formalizes the lifecycle to prevent collapse:

> **Drift → Repair → Reentry → Resonance → Outcome**

---

## 2 — How to Use This Folder

The structure supports multiple entry points based on your goals.  
One suggested learning path is:

| Step | Folder | Focus |
|------|--------|--------|
| **1** | `overview/` | High-level mental model |
| **2** | `hello_pld_runtime.py` | First runnable runtime experience |
| **3** | `operator_primitives/` | Drift, repair, and reentry operators |
| **4** | `04_integration_recipes/` | Examples showing how PLD can be applied to real agent components |
| **5** | `metrics/` | Logging schemas + evaluation dashboards |
| **6** | `_meta/` | Versioning, migration, design notes |

> 📌 If you'd like to see PLD applied in runnable examples, explore:  
> `quickstart/patterns/04_integration_recipes/README_recipes.md`

---

> After completing Tier 1 (operators + core loop), you may optionally continue with:
> `quickstart/patterns/04_integration_recipes/failover_recipe.md`
>
> This enables **bounded retry + controlled termination**, preventing infinite repair loops and introducing measurable abort semantics.

---

## ⭐ Start Here — Run the Minimal Example

Before reading, **run the runtime loop once.**
This creates the first “behavioral intuition” for PLD:

```
python hello_pld_runtime.py
```

Expected output:

```
🚨 Drift Detected
🔧 Repair Applied
✅ Reentry Confirmed

Outcome: continue_after_repair
```

> This script demonstrates the core runtime lifecycle:
> **Drift → Repair → Reentry → Continue**

After running it, continue with the sections below.

---

## 3 — Conceptual Logic (For Reference)

This example is intentionally minimal — it illustrates the PLD lifecycle,
not a production implementation.

👉 For a runnable implementation, use:  
`hello_pld_runtime.py`

---

## 4 — Runtime Logging Schema (Aligned with metrics/schemas/)
```json
{
  "session_id": "MWZ-001",
  "turn_id": 4,
  "speaker": "system",
  "event_type": "drift_detected",
  "metadata": { "category": "information" },
  "latency_ms": 3120
}
```

Compatible with:
- LangGraph / LangChain memory stores

- OpenAI Assistants + Tools API event streams

- Autogen / multi-agent orchestrators

- OpenTelemetry / Mixpanel / PostHog / Elastic

---

## 5 — What to Measure

| Metric | Meaning |
|--------|---------|
| Drift Frequency | Baseline stability indicator |
| Soft Repair Ratio | Early correction effectiveness |
| Hard Repair Escalation Rate | Cost of failed soft repair |
| Reentry Confirmation Success | Continuity + alignment |
| Outcome Completion | End-to-end task success |
| Latency Drift Penalty | Stability impact of delays |

These support both **behavioral evaluation** and **engineering validation**.

---

## 6 — Relationship to Evaluation Dataset

A separate dataset exists in:

`analytics/multiwoz_2.4_n200/`

- This quickstart focuses on **implementation**
- The dataset supports **measurement and benchmarking**

Using both enables:

**prototype → evaluation → iteration**

---

## 7 — Linked Core References

| File | Purpose |
|------|---------|
| `docs/02_pld_event_schema.md` | PLD taxonomy + event definitions |
| `quickstart/operator_primitives/` | Drift → Repair → Reentry logic |
| `quickstart/patterns/04_integration_recipes/` | Runnable agent examples |
| `quickstart/metrics/` | Logging → dashboards → evaluation |
| `analytics/multiwoz_2.4_n200/` | Applied benchmark dataset |

---

### License & Attribution

Creative Commons **BY-NC 4.0**  
Maintainer: **Kiyoshi Sasano**

---

> PLD is not static rules —  
> it is a runtime discipline for maintaining shared reality with the user.

