# PLD for Agent Engineers (Applied-AI Entry Doc)

> **Audience:** Developers building LLM agents with tool-calling, memory systems, error-recovery, autonomy loops, or orchestration (LangGraph / Swarm / Autogen / Rasa / custom runtime).

> **Goal:** Understand PLD concepts _fast_ and apply them to real agents, without theory overhead.

---

## 1. Why PLD Exists — The Actual Engineering Pain

If you've built an agent beyond a single prompt, you've seen one or more of these:

| Symptom | What it Means |
|---------|--------------|
| 🔁 Tool calls repeating | The workflow state is unstable or misinterpreted |
| 🤔 Agent contradicts tool output | Belief state and environment state diverged |
| 💬 "Let’s start over." | Context collapse and forced reset |
| 🕑 Long pause → weird answer | Latency drift breaks pacing assumptions |
| 😵 Conversation drifts off topic | Goal or constraint misalignment |

These patterns appear **across frameworks and architectures**, meaning they are not implementation bugs — they are **interaction failure modes**.

**PLD gives a shared system to detect, label, and stabilize them.**

---

## 2. The Core Runtime Loop

Every interactive agent can be modeled as:

```
Action (User or System)
        ↓
    Drift (D1–D5)
        ↓
    Repair Attempt (R1–R4)
        ↓
    Reentry (RE1–RE3)
        ↓
    Resonance (Stable Loop)
```

PLD is **not a behavior template** — it is a **diagnostic & stabilization framework**.

---

## 3. The Three Classes (Working Definitions)

| Class | Meaning | Examples |
|-------|---------|----------|
| **Drift** | The agent deviates from expected memory, workflow, meaning, or timing | hallucinated DB states, missed constraints, tool mismatch |
| **Repair** | Any attempt to fix or recover from drift | ask for constraint, retry tool, modify arguments |
| **Reentry** | Returning to the intended workflow | "Continuing the booking. You wanted a 4-star under £100, right?" |

Full definitions live in:  
➡ `/docs/02_pld_drift_repair_reference.md`

---

## 4. Resonance — The Target Operating Mode

Once drift → repair → reentry stabilizes, we reach:

```
Stable Latency
+ Stable Constraints
+ Correct Tool Beliefs
+ No Looping
= Resonance
```

Resonance means:

- fewer repairs over time  
- consistent task progress  
- predictable dialogue pacing  
- tool usage aligned with context  

Resonance is **observable**, not theoretical.

See metrics in:  
➡ `/quickstart/metrics/`

---

## 5. How to Apply PLD in Real Systems (5-Step Integration)

| Step | What You Do | Where |
|------|-------------|-------|
| **1. Log events** | Use unified JSON schema | `/quickstart/metrics/schemas/pld_event.schema.json` |
| **2. Label** | Auto-label logs using LLM | `/docs/04_pld_labeling_prompt_llm.md` |
| **3. Validate** | Check codes against taxonomy | `/docs/02_pld_drift_repair_reference.md` |
| **4. Measure** | Run dashboards/reports | `/quickstart/metrics/` |
| **5. Stabilize** | Add operator primitives | `/quickstart/operator_primitives/` |

After 20–50 labeled sessions, failure modes become visible and fixable.

---

## 6. Minimal Runtime Example

```python
event = detect_pld(turn)

if event.drift:
    repair_op = select_repair(event)
    apply_operator(repair_op)

log_event(event)
```

Patterns and operators live in:

```
quickstart/operator_primitives/
bridge_hub/demo_pld_trace/
```

---

## 7. Navigation Map (Where to Read Next)

| Need | Go |
|------|----|
| Understand the allowed codes | `/docs/02_pld_drift_repair_reference.md` |
| Label logs with LLM | `/docs/04_pld_labeling_prompt_llm.md` |
| See real-world annotated examples | `/metrics/multiwoz_2.4_n200/` |
| Implement stabilization in runtime | `/quickstart/operator_primitives/` |
| Measure drift/repair outcomes | `/quickstart/metrics/` |

---

## 8. Version / Placement

This file is the **official entry point** into PLD Applied-AI.

```
docs/01_pld_for_agent_engineers.md
```

**Version:** Applied-AI Edition — 2025-02  
**Maintainer:** Kiyoshi Sasano