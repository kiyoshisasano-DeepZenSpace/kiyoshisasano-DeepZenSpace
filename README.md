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

> PLD is not cosmetic — it governs **how behavior evolves**.

---

### 🏗 Optional: Architecture View  

If you prefer a **layered systems perspective** before exploring the runtime loop or implementation paths, see:

📄 `/docs/architecture_layers.md` — *How PLD maps signals → analysis → decisions → execution as a behavioral control system.*

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

### Operational Metrics (Optional)

Once PLD is running in production, you may want to evaluate the impact of drift detection and repair strategies over time.  
For teams at that stage, see the companion document:

👉 `docs/07_pld_operational_metrics_cookbook.md` — _Metrics for evaluating stability, cost trade-offs, and user experience impact._

---

## 🧪 Getting Started

| Step | Folder | Purpose |
|---|---|---|
| **1** | `/quickstart/overview/` | Understand the runtime phases |
| **2** | `/quickstart/operator_primitives/` | Apply drift/repair/reentry primitives |
| **3** | `/quickstart/patterns/` | Examples of how PLD can be applied (not required) |
| **4** | `/quickstart/metrics/` | Log drift → repair → reentry → outcome |
| **5** | `/analytics/` | Compare results against validated traces |

---

### 🧩 Next: Runnable Integration Recipes

Once you understand the PLD runtime loop and operator primitives,  
a practical next step is exploring reference implementation examples:

📁 `quickstart/patterns/04_integration_recipes/`

These recipes are designed to be:

| Property | Meaning |
|----------|---------|
| 🧪 **Runnable** | Can be executed locally with no external infrastructure |
| 🔍 **Observable** | Emits structured PLD signals (`D*`, `R*`, `RE*`, `OUT*`) |
| 📈 **Measurable** | Compatible with `07_pld_operational_metrics_cookbook.md` |
| 🧱 **Modular** | Works with RAG, tooling, memory, or any orchestration stack |

#### Available Reference Recipes

| Layer | File | Purpose |
|-------|------|---------|
| Component | `rag_repair_recipe.md` | Detect and repair retrieval failures (D5) |
| Component | `tool_agent_recipe.md` | Recover from invalid/failed tool execution (D4) |
| Component | `memory_alignment_recipe.md` | Detect and correct state/persona drift (D2) |
| System (Capstone) | `reentry_orchestration_recipe.md` | Central routing after repair → continue / fallback / complete |

> 📌 These examples demonstrate how PLD concepts apply to working agent systems.  
> If patterns are the **parts**, recipes show **one way to assemble them into behavior** — not the only way.

---

### ▶ Conceptual Demonstration

> This is a conceptual illustration of phase transitions — **not an implementation.**

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
```

> Actual implementation depends on your orchestrator and tool stack.

---

## 📊 Evidence & Benchmarking

Validated with:

- MultiWOZ 2.4 (200 labeled dialogs)  
- Tool-enabled agents  
- Memory-integrated systems  
- Prototype production deployments  

Observed improvements:

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

> No lock-in — only the **loop** matters.

---

## 🤝 Contribution & Collaboration

Contributions welcome, especially:

- Runtime adapters  
- PLD-formatted datasets  
- Metrics dashboards  
- Repair heuristics  

For shared PoCs or joint evaluation → see `/field/` for:

- Role alignment  
- Shared terminology  
- Collaboration structure  

Before modifying quickstart behavior:

```
quickstart/_meta/MIGRATION.md
quickstart/_meta/CHANGELOG.md
```

---

## 📍 When PLD Makes Sense

Best when:

✔ Multi-turn interactions retain shared state  
✔ Tools, retrieval, memory or reasoning loops exist  
✔ Recovery matters more than one-shot answers  

Less useful when:

⚠ Single-turn Q&A  
⚠ Fully scripted flows  
⚠ Failure recovery irrelevant  

---

## 📍 What PLD Provides

- Shared behavioral vocabulary  
- Runtime phase loop  
- Observability structure  

PLD does **not** provide:

- ❌ One fixed implementation  
- ❌ A universal prompt  
- ❌ A package to install  

---

## 📜 License

```
CC BY-NC 4.0 — internal use, research, experimentation allowed.
Commercial deployment requires permission.
Maintainer: Kiyoshi Sasano
```

---

> **PLD is behavioral infrastructure —  
it governs alignment persistence across interaction —  
not just correctness at initialization.**
