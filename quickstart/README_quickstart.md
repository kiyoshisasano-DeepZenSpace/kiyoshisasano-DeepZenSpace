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

This kit contains everything needed to implement **Phase Loop Dynamics (PLD)** in real AI systems — including drift detection, repair workflows, reentry control, and runtime evaluation.

PLD is not theory.  
It is a **runtime interaction control model** built for applied AI systems.

---

## 1 — Why PLD Exists

LLMs fail not because they lack knowledge —  
but because they fail to **maintain coherent task state across turns.**

| Failure Mode | Result |
|--------------|--------|
| Loss of grounding | User distrust |
| Incorrect propagation of prior context | Cascading errors |
| Tool/API mismatch without acknowledgement | Workflow stalls |
| Full resets | Lost session state & user patience |

PLD formalizes the lifecycle to prevent collapse:

> **Drift → Repair → Reentry → Resonance → Outcome**

---

## 2 — How to Use This Folder

Follow the structure in this order:

| Step | Folder | Purpose |
|------|--------|---------|
| **1** | `overview/` | Learn the model quickly |
| **2** | `operator_primitives/` | Use drift, repair, latency, reentry operators |
| **3** | `patterns/` | Drop-in templates for LLM, UX, and orchestration |
| **4** | `metrics/` | Logging schemas and evaluation dashboards |
| **5** | `_meta/` | Versioning, change logs, migration notes |

This mirrors **real engineering adoption** from conceptual understanding → implementation → measurement.

---

## 3 — Minimal Working Example

```python
from pld import detect_drift, soft_repair, classify_event

turn = "I don't have any hotels at that price."

drift = detect_drift(turn)
repair = soft_repair(drift)

event = classify_event(turn, drift, repair)
print(event)
```

Example output:

```json
{
  "event_type": "soft_repair",
  "drift": "information",
  "strategy": "option_expansion"
}
```

---

## 4 — Runtime Logging Schema (Aligned with `metrics/schemas/`)

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
- Autogen / Multi-agent orchestration  
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
| Latency Drift Penalty | Impact of delays on stability |

These metrics support both **behavioral evaluation and engineering validation.**

---

## 6 — Relationship to Evaluation Dataset

A separate dataset exists in:

```
analytics/multiwoz_2.4_n200/
```

- This quickstart focuses on **implementation**
- The dataset focuses on **measurement and validation**

Together they support prototype → production → benchmark alignment.

---

## 7 — Linked Core References

| File | Use |
|------|-----|
| `docs/02_pld_event_schema.md` | Core taxonomy + event definitions |
| `quickstart/operator_primitives/` | Drift → Repair → Reentry logic |
| `quickstart/metrics/` | Logging, dashboards, evaluation |
| `analytics/multiwoz_2.4_n200/` | Applied benchmark + scoring |

---

## License & Attribution

```
Creative Commons BY-NC 4.0
Maintainer: Kiyoshi Sasano
```

> PLD is not static rules —  
> **it is a runtime discipline for maintaining shared reality with the user.**

---
