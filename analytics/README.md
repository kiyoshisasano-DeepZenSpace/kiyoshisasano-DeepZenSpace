# 📊 PLD Analytics & Evaluation Index

This folder contains the **evaluation resources and applied evidence layer** used to validate Phase Loop Dynamics (PLD) in real-world systems.

Where:

- `/docs/` defines the concepts and taxonomy  
- `/quickstart/metrics/` enables runtime instrumentation  
→ **`/analytics/` evaluates whether the system behaves as expected.**  

---

## 1 — Folder Purpose

Use this folder when you are:

- validating runtime behavior against external dialogs
- comparing system revisions or orchestration strategies
- performing field evaluation before production rollout
- benchmarking drift / repair / reentry patterns at scale

This is the **analysis layer**, not a deployment or training resource.

---
## 2 — Contents

This folder now contains two resource types:

- **Applied evaluation artifacts** (datasets, case studies)
- **Analytical frameworks** (interpretation layer for canonical metrics)

### 🔹 Analytical Frameworks (New)

These documents extend the formal metric definitions in  
`/docs/metrics/PLD_metrics_spec.md` by providing:

- interpretation guidance
- observed usage patterns
- analysis strategies
- failure signatures
- research questions

| File | Focus |
|------|-------|
| `PRDR_framework.md` | Recurrence patterns after repair and stability inference |
| `VRL_framework.md` | Temporal recovery behavior and responsiveness |
| `continue_repair_ratio.md` | High-level alignment stability indicator |
| `failure_mode_clustering.md` | Structural patterns of drift causes and remedies |
| `session_closure_typology.md` | How interactions terminate and what closure implies |

These documents are **informative** (not normative) and intended for:

- researchers
- model evaluators
- system designers
- runtime governance engineers

They SHOULD be used **after** metrics are computed, not before.

---

## 3 — Recommended Entry Points

| Goal | Start Here | Next |
|------|-----------|------|
| Benchmark system behavior | `multiwoz_2.4_n200/README.md` | Compare results to runtime logs |
| Understand PLD in a real applied system | `case_study_end_to_end.md` | Map insights to runtime design |
| Build dashboards or operational metrics | `/quickstart/metrics/` | `/docs/07_pld_operational_metrics_cookbook.md` |

---

## 4 — Relationships to Other Modules

```
/quickstart/metrics/                  → Logging and runtime instrumentation
/analytics/                           → Analysis, comparison, evidence and scoring
/docs/07_pld_operational_metrics_... → Metric definitions (PRDR, REI, VRL)
/quickstart/patterns/04_integration_recipes/ → Runnable runtime reference examples
```

This ensures full continuity from:

> **logging → evaluation → interpretation → system improvement**

---

## 5 — When to Use This Folder

Use `analytics/` when:

- you have logs from a working prototype  
- metrics are being emitted or captured  
- drift, repair, and reentry patterns are visible and measurable  

Once data exists, this folder helps answer:

> **“Is the system stable — and where should we improve next?”**

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025 — Analytics Layer**

