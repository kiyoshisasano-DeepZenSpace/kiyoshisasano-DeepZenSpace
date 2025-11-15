# PLD: Phase Loop Dynamics  
### *A Runtime Phase Model for Stable Multi-Turn LLM Systems*

---

## 🧠 Why PLD Exists — 10 Seconds

Modern multi-turn LLM systems rarely fail due to capability —  
they fail because alignment **drifts over time**.

PLD introduces a runtime loop that:

- Detects drift early  
- Repairs and confirms alignment  

…so systems remain stable across turns.

```
Detect → Repair → Reenter → Continue → Complete
```

---

## 🧩 What PLD *Is* — 30-Second Understanding

PLD is:

- 🧠 A **runtime phase model** for continuous multi-turn alignment  
- 🔍 A methodology for drift detection and structured repair  
- 📊 An **observable behavioral framework** (not a single implementation)  
- 🧩 A set of **integration patterns** — compatible with existing orchestrators  
- ⚙️ Model-agnostic, applicable to RAG agents, tool-based systems, and workflows  

> PLD defines ***how alignment is maintained over time*** —  
not how a single response is generated.  
> PLD is adopted as a **runtime governance pattern**, not installed as a package.

---

## 🚀 Who Should Use PLD

| Role | What PLD Improves |
|---|---|
| **LLM / Agent Engineers** | Tool stability, reduced cascading errors |
| **Conversation & UX Designers** | Predictable repair and confidence signaling |
| **QA, Evaluation, AgentOps** | Observable, repeatable behavior diagnostics |

---

## 🧭 The PLD Runtime Loop

| Phase | Purpose | Signals |
|---|---|---|
| **Drift** | Detect divergence from task or shared state | contradiction, invalid tool, memory loss |
| **Repair** | Soft/hard correction | clarification, reset, constraint restatement |
| **Reentry** | Confirm restored alignment | checkpointing, summarization |
| **Continue** | Resume execution | next step |
| **Outcome** | Completed / partial / failed / abandoned | terminal state |

> Works with LangGraph, Assistants API, Swarm, AutoGen, Rasa, or custom orchestration loops.

---

### 📈 Model Diagram

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

📁 Full: `/docs/model_diagram.md`

---

## 🆚 Before / After

| Without PLD | With PLD |
|---|---|
| Repeated invalid tools | Drift → repair → confirmed retry |
| Lost context | Anchored via reentry checkpoints |
| Silent failure | Controlled outcome or fallback |
| Unpredictable UX | Observable corrective behavior |

PLD is **not cosmetic** — it governs how behavior evolves.

---

## 📂 Repository Overview

```
/quickstart     — Conceptual model + integration patterns (start here)
/pld_runtime    — Reference implementation (not required for adoption)
/docs           — Runtime phase model + behavioral taxonomy
/analytics      — Benchmark datasets + evaluation traces
/field          — Adoption methodology + collaboration governance
```

➡ Full layout: `/docs/repo_structure.md`

---

## 🧪 Getting Started

| Step | Folder | Purpose |
|---|---|---|
| 1 | `/quickstart/overview/` | Understand the runtime phases |
| 2 | `/quickstart/operator_primitives/` | Apply drift/repair/reentry primitives |
| 3 | `/quickstart/patterns/` | Integration with agent frameworks |
| 4 | `/quickstart/metrics/` | Log drift → repair → reentry → outcome |
| 5 | `/analytics/` | Compare results against validated traces |

---

### ▶ Conceptual Demonstration

> **This is a conceptual illustration of phase transitions — not an implementation.**

```python
# PLD Phase Model (Conceptual)

current_phase = detect_drift(conversation_state)

if current_phase == Phase.DRIFT:
    conversation_state = apply_repair(conversation_state)
    current_phase = Phase.REPAIR

if current_phase == Phase.REPAIR:
    if confirm_alignment(conversation_state):
        current_phase = Phase.CONTINUE
    else:
        current_phase = Phase.DRIFT  # Restart the phase loop

# Actual implementation depends on your orchestrator and tool stack.
```

---

## 📊 Evidence & Benchmarking

Validated with:

- MultiWOZ 2.4 (200 labeled dialogs)
- Tool-enabled agents  
- Memory-integrated systems  
- Prototype production deployments  

Observed changes:

- ↓ Drift frequency  
- ↓ Abandonment  
- ↑ Successful reentry  
- ↓ Invalid tool sequences  

📁 Details: `/analytics/`

---

## 🔌 Integrations

Supports:

- LangGraph  
- Assistants API  
- Swarm  
- AutoGen / CrewAI  
- Rasa  
- ReAct-style routing  
- Custom frameworks  

No lock-in — **only the loop matters.**

---

## 🤝 Contribution

Preferred contributions:

- Runtime adapters  
- PLD-formatted datasets  
- Metrics dashboards  
- Alternative repair heuristics  

📄 Roles and governance: `field/ROLE_ALIGNMENT.md`

Before modifying behavior:

```
quickstart/_meta/MIGRATION.md
quickstart/_meta/CHANGELOG.md
```

---

## 📜 License

```
CC BY-NC 4.0 — internal use, research, experimentation allowed.
Commercial deployment requires permission.
```

---

Maintainer: **Kiyoshi Sasano**

> **PLD is behavioral infrastructure —  
it governs alignment persistence across interaction, not initialization.**
