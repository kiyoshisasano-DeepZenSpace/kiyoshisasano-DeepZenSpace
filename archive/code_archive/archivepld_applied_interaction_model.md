# PLD Applied Interaction Model  
### (GitHub Public Edition — Fully Taxonomy-Aligned — 2025)

This document provides the **canonical system-level interaction model** for PLD  
(Phase Loop Dynamics) as used in:

- LLM agents with tool execution  
- Task-oriented dialogue (TOD) systems  
- Multi-agent orchestration (planner → executor → critic → monitor loops)  
- Latency-aware UX frameworks  

It is aligned with the official PLD taxonomy and annotation prompt:

| Component | Reference |
|----------|-----------|
| Taxonomy | `docs/drift_repair_taxonomy.md` |
| Labeling Standard | `docs/labeling_prompt.md` |
| Evaluation Example | `metrics/multiwoz_2.4_n200/` |

No HCI terminology is included.  
This is the **developer-facing implementation reference.**

---

## 1. Purpose

PLD defines a structured way to **detect, classify, and stabilize** interaction loops.

It answers four engineering questions:

1. **What drift occurred?** (D1–D5)
2. **What repair response is appropriate?** (R1–R4)
3. **Did the workflow return to the intended path?** (RE1–RE3)
4. **Is the system stabilizing or degrading over time?** (Resonance Stage)

PLD does **not prescribe behavior** — it provides a **framework for analysis, automation, and recovery logic.**

---

## 2. Core Loop

```
[Input / Event]
        ↓
  Drift Detected (D1–D5)
        ↓
  Repair Attempt (R1–R4)
        ↓
  Reentry (RE1–RE3)
        ↓
  Resonance (Stable Flow)
        ↓
  Outcome (complete / incomplete)
```

This loop applies across:

- conversational agents  
- inference-time pipelines  
- tool execution stacks  
- orchestration frameworks  
- timing/latency controllers  

---

## 3. Drift Types (D1–D5)

| Code | Name | Trigger Examples |
|------|------|------------------|
| **D1 — Information Drift** | DB/API contradictions, hallucinated attributes, “no result” then later results |
| **D2 — Context Drift** | lost constraint, overwritten slot, mixing unrelated states |
| **D3 — Intent Drift** | switching domain, irrelevant reasoning, unrequested plan changes |
| **D4 — Procedural Drift** | failed sequencing, looping planner, ignored tool outputs, multi-agent role confusion |
| **D5 — Pacing / Latency Drift** | long silence, broken streaming, unacknowledged delay |

> **D1 and D4 are the highest-risk categories for cascading workflow corruption.**

---

## 4. Repair Operations (R1–R4)

| Code | Repair Type | Meaning |
|------|-------------|---------|
| **R1 — Local Repair (Soft Repair)** | clarifying question, corrected tool call, offering options |
| **R2 — Structural Repair** | restoring state, syncing tool output, correcting workflow role alignment |
| **R3 — UX Repair** | pacing correction, confidence calibration, progressive waiting feedback |
| **R4 — Hard Repair (Restart / Reset)** | full context reset when state is unrecoverable |

> R4 should be **rare** and used only after failed R1–R3 attempts.

---

## 5. Reentry Types (RE1–RE3)

| Code | Type | Meaning |
|------|------|---------|
| **RE1 — Intent Reentry** | Return to the original task objective |
| **RE2 — Constraint Reentry** | Previously declared constraints are restored and honored |
| **RE3 — Workflow Reentry** | The system realigns with the intended execution sequence |

---

## 6. Resonance (Stable Interaction Regime)

Resonance indicates the loop is stabilized after drift-repair cycles.

A system is considered resonant if:

- latency stabilizes  
- no contradictory tool outputs appear  
- workflow avoids looping/planning recursion  
- repair frequency decreases over time  

Tracking resonance provides a measure of **interaction maturity**.

---

## 7. Architecture Mapping

### **A. LLM Agent Runtime Loop**

```
observe → predict → tool-call → evaluate → drift? → repair → update state → continue
```

PLD connects at three checkpoints:

- drift detector  
- repair type selector  
- reentry validation  

---

### **B. Task-Oriented Dialogue Systems**

Maps cleanly to:

```
NLU → DST → Policy → NLG → Execution
```

PLD stabilizes:

- slot constraint consistency  
- DB mismatch handling  
- fallback prioritization strategies  

---

### **C. Multi-Agent Orchestration (Planner/Executor/Critic)**

```
planner → executor → critic → (monitor optional) → planner
```

PLD prevents:

- role drift  
- execution loops  
- contradictory beliefs between agents  

---

### **D. Latency & UX-Control Systems**

Used for:

- streaming stability
- buffering behavior
- trust-preserving pacing patterns

---

## 8. Minimal Integration API (Example)

A full PLD-aware event stream may emit:

```json
{
  "event": "pld_drift",
  "type": "D1_information_drift",
  "timestamp": "2025-02-01T12:30:44Z",
  "metadata": {
    "tool": "db.search",
    "system_claim": "no hotels available",
    "later_contradiction": "3 results found"
  }
}
```

Followed by repair and reentry messages:

```json
{
  "event": "pld_repair",
  "type": "R2_structural_repair",
  "metadata": {
    "action": "restore constraints"
  }
}
```

---

## 9. Metrics Alignment

The PLD model supports:

- Drift Rate  
- Soft Repair vs Hard Repair Ratio  
- Reentry Success Rate  
- Resonance Stability Score  
- Outcome Completion Rate  

These metrics are used in:

```
metrics/multiwoz_2.4_n200/
```

---

## 10. Repository Placement

```
docs/pld_applied_interaction_model.md
```

---

## 11. Version

PLD Applied-AI Unified Edition  
2025-02  
Maintainer: DeepZenSpace
