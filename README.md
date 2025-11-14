# PLD: Phase Loop Dynamics  
### *A Practical Runtime Framework for Stable Multi-Turn LLM Systems*

## 🧠 Why PLD Exists — 10 Seconds

Modern multi-turn LLM systems don’t fail because they lack capability —  
they fail because alignment **drifts over time**.

PLD provides a runtime loop that:

- Detects drift early  
- Repairs and confirms alignment  
- Keeps agents stable across turns  

```powershell
Detect → Repair → Reenter → Continue → Complete
```


PLD helps AI systems stay aligned across multi-turn interactions — even when tools, memory, or intent shift.

Modern LLM systems rarely fail because they lack capability.  
They fail because the interaction **drifts**.

> **PLD detects drift early, repairs it, confirms alignment, and keeps the system synchronized with the user.**

```
Detect Drift → Repair → Reenter Context → Continue → Complete
```

---

## 🧩 What PLD *Is* — 30-Second Understanding

PLD is:

- 🧠 A runtime model for multi-turn LLM alignment  
- 🔍 A method for early detection of conversational drift  
- 🧩 A framework integrating detection, repair, re-entry, and outcome tracking  
- ⚙️ Model-agnostic and compatible with RAG, agents, and tool orchestrators  

If you're building multi-turn systems with reasoning, memory, or tools — **PLD applies.**

---

## 🚀 Who Should Use PLD

| Role | What PLD Improves |
|---|---|
| **LLM / Agent Engineers** | Tool invocation stability, reduced hallucination cascades |
| **Conversation & UX Designers** | Predictable recovery, confidence signaling, latency-aware behavior |
| **Evaluation / QA / AgentOps** | Structured behavioral metrics and repeatable test harnesses |

---

## 🧭 The PLD Runtime Loop

| Phase | Purpose | Example Signals |
|---|---|---|
| **Drift** | System diverges from goal or shared state | contradiction, wrong tool, mis-memory, task confusion |
| **Repair** | Apply soft or hard corrective action | correction, clarification, constraint restatement, reset |
| **Reentry** | Confirm alignment before proceeding | confirmation question, summary, checkpoint |
| **Continue** | Resume task execution | next step or subtask |
| **Outcome** | Success, partial, failure, or abandonment | measurable terminal state |

> PLD is framework-agnostic — works with proprietary LLMs, OSS models, scripted agents, or tool orchestrators.

---

### 📈 PLD Runtime Loop Diagram

```mermaid
flowchart LR
    Start([Turn])
    Drift{Drift?}
    Repair["Repair\n(soft/hard)"]
    Reentry["Reentry\n(confirm)"]
    Continue[Continue]
    Outcome[(Outcome)]

    Start --> Drift
    Drift -->|No| Continue
    Drift -->|Yes| Repair --> Reentry -->|Aligned| Continue --> Outcome --> Start
    Reentry -->|Not aligned| Drift

```
📌 Full diagram (zoomable):  
➡ `/docs/model_diagram.md`


---

## 🆚 Before / After — What Changes With PLD?

| Scenario | Without PLD | With PLD |
|---|---|---|
| Tool call drift | Model repeats incorrect calls | System detects drift → clarifies → retries |
| Context loss | Prior constraints forgotten | Repair + reentry keep context anchored |
| Silent failure | Interaction collapses | Runtime triggers recovery or graceful exit |
| User trust | Unpredictable responses | Visible correction + confirmation → confidence |

PLD isn’t cosmetic — **it changes how the system behaves over time.**

---

## 📂 Repository Overview

```txt
📦 Repository Structure (High-Level)

- /quickstart — Start here (hands-on intro)
- /pld_runtime — Production-ready runtime framework
- /docs — Model rationale + diagrams
- /analytics — Benchmark results
- /field — Adoption guides & onboarding

➡ Full structure: /docs/repo_structure.md
```

---

## 🧪 Getting Started (Fast Path)

This repository includes everything from conceptual overview to full integration examples.  
If you prefer starting hands-on, the fastest entry point is below:

| Step | Folder | Purpose |
|---|---|---|
| **1** | `/quickstart/overview/` | Learn the PLD runtime model |
| **2** | `/quickstart/operator_primitives/` | Use drift, repair, and reentry operators |
| **3** | `/quickstart/patterns/` | Apply drop-in templates for agents and UX |
| **4** | `/quickstart/metrics/` | Log drift → repair → reentry → outcome |
| **5** | `/analytics/` | Benchmark behavioral improvements |

---

### ▶ Minimal Runnable Example

If you'd like to **see the PLD loop in action immediately**, a standalone executable demo is provided:

```bash
python quickstart/examples/minimal_pld_demo.py
```

This script illustrates:

- Drift detection  
- A soft repair action  
- A reentry confirmation step  
- JSON event logging aligned to the PLD schema  

It runs without any external model or configuration (a stub LLM is included).  
Use it if you want a concrete reference point before exploring the rest of the quickstart.


---

## 📌 Where PLD Is Useful — Practical Use Cases

| Domain / System Type | Where PLD Helps | Failure Without PLD |
|----------------------|-----------------|----------------------|
| **Customer Support Assistants** | Prevents looped clarifications and drifting tone | Escalation loops, inconsistent answers |
| **Tool-Using Agents (ReAct / LangGraph / Swarm)** | Stops recursive mis-invocations and invalid tool calls | Compounding errors, runaway retries |
| **RAG Assistants** | Maintains grounding across retrieval cycles and memory refresh | Evidence drift, hallucinated citations |
| **Workflow / Automation Agents** | Supports predictable repair and restart checkpoints | Partial execution, silent resets |
| **AgentOps / Evaluation Pipelines** | Standardizes behavior comparison across models and versions | No reproducibility, subjective evaluation |

> If your system uses **memory, retrieval, multi-step reasoning, or external tools**, PLD improves runtime stability.

---

## 📊 Evidence & Benchmarking

Validated with:

- MultiWOZ 2.4 dataset — **200 labeled conversations**
- Tool-using autonomous agents  
- Memory-enabled orchestration systems  
- Prototype production systems  

Observed outcomes:

- ↓ Drift Events  
- ↓ Abandonment / collapse  
- ↑ Successful Re-entry confirmation  
- ↓ Invalid / repeated tool calls  

📁 Results available in: `analytics/`

---

## 🔌 Integrations

Compatible with:

- LangGraph  
- AutoGen / CrewAI  
- Assistants API  
- Swarm  
- ReAct  
- Rasa actions  
- Custom orchestration stacks  

No lock-in — **only the loop matters.**

---

## 🤝 Contribution

We welcome contributions focused on **practical adoption**, including:

- Runtime adapters (LangGraph, Swarm, Assistants API, Rasa, ReAct, etc.)  
- Additional PLD-labeled datasets  
- Metrics extensions and dashboards  
- Alternative repair strategies or timing heuristics  

Before modifying quickstart behavior, check:

```
quickstart/_meta/MIGRATION.md  
quickstart/_meta/CHANGELOG.md  
```

---

## 📜 License

```
CC BY-NC 4.0 — free for internal development, research, and experimentation.
Commercial deployment requires permission.
```

---

Maintainer: **Kiyoshi Sasano**

> **PLD is behavioral infrastructure —  
not just evaluation.  
It keeps systems aligned continuously, not just at initialization.**
