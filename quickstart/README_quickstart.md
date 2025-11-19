---
title: "PLD Applied Quickstart Kit"
version: "2025.2"
status: stable
maintainer: "Kiyoshi Sasano"
tags:
  - PLD
  - LLM Agents
  - Drift Control
  - Runtime Repair
  - Telemetry-Driven AI
---

# 🚀 PLD Applied Quickstart Kit  
**For LLM Agents, Orchestrators, and Conversational Systems (2025 Edition)**  

> PLD is best understood **through runtime experience — not theory alone.**

This kit provides everything needed to implement **Phase Loop Dynamics (PLD)** in a live AI agent:

- Drift detection and classification  
- Repair selection (soft → hard)
- Reentry confirmation and stabilization  
- Failover rules and bounded execution  
- Metrics, dashboards, and runtime governance  

PLD is not a prompting trick.  
It is a **runtime interaction control model** for applied AI systems.

---

## 🏁 Start Here — Run the Minimal Runtime

`hello_pld_runtime.py` is the simplest runnable demonstration of the full PLD loop.

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

💡 This establishes intuition for the runtime lifecycle:
```bash
Drift → Repair → Reentry → Continue
```

---

🔧 Next: Run the Real Engine

Once you understand the runtime feel, activate the full controller:

```bash
python run_minimal_engine.py
```

✔ Uses the real PLD policies
✔ Logs events using the canonical schema
✔ Produces a trace of decisions and alignment events

This is the first verification checkpoint that your environment is correctly wired.

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

> **The goal is not correctness — the goal is recoverable alignment**.

---

## 2 — How to Use This Folder

| Step  | Location               | What You Learn                                 |
| ----- | ---------------------- | ---------------------------------------------- |
| **1** | `overview/`            | High-level mental model                        |
| **2** | `hello_pld_runtime.py` | First hands-on runtime experience              |
| **3** | `operator_primitives/` | Drift → Repair → Reentry linguistic operators  |
| **4** | `patterns/`            | Best-practice runtime behavior and UX phrasing |
| **5** | `integration_recipes/` | LangGraph / Rasa / OpenAI Assistants wiring    |
| **6** | `metrics/`             | Telemetry, dashboards, and stability analysis  |

➡️ For framework bindings:
`quickstart/patterns/04_integration_recipes/`

---

## 3 — Core Runtime Lifecycle

PLD operates as a deterministic runtime loop:
```python
User Turn
   ↓
Drift Detected? ── No ──▶ Continue
         │
        Yes
         ↓
Select Repair → Apply → Reentry Check → Continue / Escalate / Failover
```
Each step produces structured telemetry aligned with:
```pgsql
quickstart/metrics/schemas/pld_event.schema.json
```

---

## 4 — Example Logged Event

```json
{
  "session_id": "MWZ-001",
  "turn_id": 4,
  "event_type": "drift_detected",
  "pld": {
    "phase": "drift",
    "code": "D2_context",
    "confidence": 0.92
  },
  "runtime": {
    "latency_ms": 3120,
    "source": "assistant"
  }
}
```

Compatible with:
- LangGraph state stores
- OpenAI Assistants streaming telemetry
- Tool traces + RAG observability systems
- OpenTelemetry spans

---

## 5 — What Gets Measured

| Metric                    | Meaning                               |
| ------------------------- | ------------------------------------- |
| Drift Frequency           | Stability baseline                    |
| Soft vs Hard Repair Ratio | Efficiency vs escalation pressure     |
| Reentry Success Rate      | Ability to stabilize after correction |
| Failover Trigger Rate     | Safety boundary activation            |
| Latency-Induced Drift     | UX-performance dependency             |
| Outcome Distribution      | Completion vs abandonment             |

These power:

- model comparisons
- policy tuning
- architecture iteration
- UX alignment studies
- Behavior is only real when measurable.

---

## 6 — Evaluation Dataset (Optional But Useful)

The dataset at:
```bash
analytics/multiwoz_2.4_n200/
```

allows you to:
- benchmark models
- test pattern changes
- measure policy improvements

This supports the cycle:
```perl
prototype → evaluate → tune → redeploy
```

---

## 🔁 The PLD Feedback Loop

Once everything is wired:
```pgsql
Runtime → Logging → Metrics → Dashboard → Adjust Policy → Update Patterns → Rerun
```
This enables **governable agent behavior**.

---

### License & Attribution

Creative Commons **BY-NC 4.0**  
Maintainer: **Kiyoshi Sasano**

---

> PLD is not static rules —  
> it is a sustained discipline for maintaining aligned shared reality with the user.

