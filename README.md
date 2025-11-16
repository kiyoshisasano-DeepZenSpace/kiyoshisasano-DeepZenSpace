# PLD: Phase Loop Dynamics  
*A Runtime Phase Model for Stable Multi-Turn LLM Systems*

---

## 🧠 Why PLD Exists — 10-Second Summary

Modern multi-turn LLM agents rarely fail because of knowledge gaps —  
they fail because alignment **drifts over time**.

PLD introduces a **runtime control loop** that:

- Detects drift early  
- Repairs behavior  
- Confirms alignment before continuing  

```
Detect → Repair → Reenter → Continue → Complete
```

---

### 📍 High-Level Runtime Model (Visual Summary)

> A compact view of the runtime loop, metrics integration, and conceptual role of PLD.

<img src="./README_model.svg" width="100%" />

---

## 🧩 What PLD *Is* — In 30 Seconds


PLD is:

- A **runtime phase model** for interaction stability  
- A structured method for **drift detection and repair**
- A **behavioral governance layer**, not a model prompt or product
- **Observable and measurable** — compatible with telemetry and evaluation
- Implementation-agnostic: works with tool agents, retrieval systems, planners, and chat models  

> PLD governs **how behavior evolves over turns**, not how a single output is generated.

---

## 🚀 Who Uses PLD

| Role | Value |
|------|-------|
| **LLM / Agent Engineers** | Reduced cascade errors, fewer resets |
| **Interaction & UX Designers** | Predictable repair and alignment signaling |
| **AgentOps & Evaluation Teams** | Observable behavioral diagnostics and metrics |

---

## 🧭 The PLD Runtime Loop

| Phase | Purpose | Signals |
|-------|---------|---------|
| **Drift** | Detect divergence from task or shared reality | tool errors, contradiction, missing context |
| **Repair** | Soft/hard correction | clarification, reset, constraint restatement |
| **Reentry** | Confirm restored alignment | checkpoint, summarization |
| **Continue** | Resume execution | next step |
| **Outcome** | End state | complete / partial / failed / abandoned |

> Framework-agnostic: supports LangGraph, Assistants API, AutoGen, Swarm, Rasa, or custom orchestrators.

---

## 📈 Runtime Model Diagram

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

Full reference: `/docs/model_diagram.md`

---

## 🆚 Before vs After PLD

| Without PLD | With PLD |
|-------------|----------|
| Silent brittle failures | Explicit repair and confirmation |
| Repeated invalid tool calls | Controlled retry + fallback |
| Lost context | Structured reentry checkpoints |
| Unpredictable user experience | Observable, governable behavior |

---

### 🏗 Optional: Architectural Perspective

📄 `/docs/architecture_layers.md`  
A higher-level view for teams mapping PLD into large orchestration stacks.

---

### 🏁 Quickstart — Run the Minimal Runtime

Before diving into the full documentation, you can **experience PLD behavior** in less than 10 seconds:

```bash
python quickstart/hello_pld_runtime.py
```

Try with custom input:
```bash
python quickstart/hello_pld_runtime.py "Can we switch topics and talk about cooking?"
```
Run all example scenarios:
```bash
python quickstart/hello_pld_runtime.py --examples
```

> PLD is best understood through interaction — not just by reading.
> This script demonstrates the core runtime loop:
> Drift → Repair → Reentry → Continue
> (in a minimal mock runtime environment)

For deeper usage patterns, continue with:  
➡️` quickstart/README_quickstart.md` 

---

## 📂 Repository Overview

```
/quickstart     — Learning path + implementation patterns (start here)
/pld_runtime    — Reference runtime (optional)
/docs           — Taxonomy, conceptual model, reference material
/analytics      — Benchmark datasets + case studies
/field          — Collaboration playbooks and adoption patterns
```

➡ Full structure: `/docs/repo_structure.md`

---

## 📏 Operational Metrics

Once PLD is active in a system, evaluation may include:

- Drift frequency
- Repair efficiency (soft vs hard)
- Reentry confirmation success
- Stability vs latency trade-offs
- Outcome completion distribution

Reference definitions:  
👉 `/docs/07_pld_operational_metrics_cookbook.md`

---

## 🧪 Practical Adoption Path

| Step | Folder | Purpose |
|------|--------|---------|
| **1** | `/quickstart/overview/` | Understand the runtime loop |
| **2** | `/quickstart/operator_primitives/` | Apply operator logic |
| **3** | `/quickstart/patterns/` | Modular behavior patterns |
| **4** | `/quickstart/patterns/04_integration_recipes/` | **Runnable reference examples** |
| **5** | `/quickstart/metrics/` | Log drift → repair → reentry → outcome |
| **6** | `/analytics/` | Compare results against evaluated traces |

---

### 🧩 Runnable Integration Recipes

```
quickstart/patterns/04_integration_recipes/
```

These reference examples are:

| Property | Meaning |
|----------|---------|
| 🧪 Runnable | Executable locally (no infra required) |
| 🔍 Observable | Emits structured PLD signals |
| 📈 Measurable | Compatible with metrics cookbook |
| 🧱 Modular | Works with memory, tools, or RAG systems |

---

### ▶ Minimal Conceptual Example

This illustrates the phase loop logic — not a runnable implementation.

```python
# Conceptual pseudo-implementation

phase = detect_drift(turn)

if phase is DRIFT:
    turn = repair(turn)
    phase = REPAIR

if phase is REPAIR:
    if confirm_alignment(turn):
        phase = CONTINUE
    else:
        phase = DRIFT
```

> Actual implementation depends on the orchestration environment.

---

## 📊 Evidence Layer

Validated through:

- MultiWOZ 2.4 (200 annotated dialogs)
- Real tool-enabled agents
- Applied SaaS support case studies
- Field PoCs

See: `/analytics/`

---

## 🔌 Integrations

Compatible with:

- LangGraph
- Assistants API
- Swarm
- Rasa
- ReAct-style planners
- Custom orchestration pipelines

No required framework — only the **loop semantics**.

---

## 🤝 Contribution & Collaboration

Contributions are welcome, especially:

- Runtime bridges and adapters  
- Evaluation datasets and traces  
- Operational repair heuristics  
- Metrics dashboards  

For shared PoCs or partnership work → see `/field/`.

Before altering terminology or behavior semantics:

```
quickstart/_meta/MIGRATION.md
quickstart/_meta/CHANGELOG.md
```

---

## 📍 When PLD Applies

Best suited when:

✔ Multi-turn workflows  
✔ Tools, retrieval, memory, or planning  
✔ Recovery matters more than one-shot accuracy  

Less relevant when:

⚠ Single-turn answers  
⚠ Fully deterministic scripted flows  

---

## 📜 License

This repository is licensed under a **hybrid (dual-license)** model to maximize both community adoption and intellectual property protection.

### 1. For Code Components (Apache 2.0)

All **code** components are licensed under the permissive **Apache License 2.0**.
This applies to:
* The entire `/pld_runtime/` engine (all `.py`, `.json` files)
* All runnable scripts in `/quickstart/` (e.g., `hello_pld_runtime.py`)
* All schemas (`.json`, `.yaml`) and configuration files

This allows developers and companies to freely **use, experiment with, and integrate** the PLD runtime code into their own systems (commercial or otherwise) with minimal legal friction.

* **Full License Text:** **[LICENSE-APACHE-2.0.txt](LICENSE-APACHE-2.0.txt)**

### 2. For Documentation & Methodology (CC BY-SA 4.0)

All **documentation and conceptual assets** (the "Methodology" or "IP") are licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.
This applies to:
* All `.md` files (including this `README.md`, `SUMMARY.md`, `/docs/`, `/analytics/`, `/field/`, and `/quickstart/patterns/04_integration_recipes/`)
* All `.svg` files (`README_model.svg`, `SUMMARY.svg`)
* The PLD methodology itself (e.g., the `PRDR`, `REI`, `VRL` metric definitions in `07_cookbook`)
* The `analytics/` datasets and case studies

This license allows you to **share and adapt** this knowledge, *even commercially*, as long as you:
1.  **Give appropriate attribution (BY)** to Kiyoshi Sasano.
2.  **Share your adaptations under the same (SA) license.**

* **Full License Text:** **[LICENSE-CC-BY-SA-4.0.txt](LICENSE-CC-BY-SA-4.0.txt)**

### Summary

| Asset Type | Path(s) | License | Why? |
| :--- | :--- | :--- | :--- |
| **Code (Engine)** | `/pld_runtime/`, `*.py`, `*.json` | **Apache 2.0** | **Maximize Adoption** (Frictionless use) |
| **IP (Methodology)** | `/docs/`, `/analytics/`, `*.md`, `*.svg` | **CC BY-SA 4.0** | **Protect Credit** (Prevents IP theft) |

---
Maintainer: **Kiyoshi Sasano**

Copyright © 2025 Kiyoshi Sasano. All rights reserved where applicable.

For commercial licensing, enterprise support, or OEM integration,
contact: <deepzenspace[at]gmail.com>.

---

> **PLD is behavioral infrastructure —  
it ensures alignment persists *across interaction*,  
not just at initialization.**
