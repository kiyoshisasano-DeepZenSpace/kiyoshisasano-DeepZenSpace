---
title: "PLD Metrics Module — Quickstart Edition"
version: 2025.1.1
maintainer: "Kiyoshi Sasano"
status: stable
tags:
  - PLD
  - evaluation
  - drift metrics
  - applied UX
  - behavioral logging
---

# 📊 PLD Metrics Module — Quickstart Edition

This module provides the **measurement layer** of the PLD Applied Interaction Framework.  
It enables developers to **log, aggregate, and visualize** behavioral signals that reflect an agent’s runtime stability and ability to recover from misalignment.

This edition is intended as the **minimal operational implementation** — consistent with the evaluation workflow used in the MultiWOZ-style benchmark baseline (N≈200 sessions).

---

### 🚀 Quick Validation — Run Metrics Locally

To verify schema integrity and metric computation against the bundled demo log:

```bash
cd quickstart/metrics
pip install duckdb
python verify_metrics_local.py
```

This validates end-to-end flow:

```metalab
Raw PLD events → Aggregated metrics → Dashboard tiles
```

---

## 1. What This Module Enables

After integration, you can:

- Log runtime behaviors using a standard PLD JSON schema
- Track Drift → Repair → Reentry → Outcome sequences
- Measure timing effects (latency and pacing sensitivity)
- Generate stability dashboards and longitudinal comparisons
- Compare runtime configurations, model versions, and prompting strategies

  - LangChain / LangGraph / Agents API
  - Rasa / Orchestrated tool-use runtimes
  - Custom controller architectures   

> This module is optimized for **runtime observability**, not offline annotation.

---

## 2. Module Structure

```txt
quickstart/metrics/
│
├── README_metrics.md                 ← You are here
│
├── schemas/                          ← Canonical data definitions
│   ├── pld_event.schema.json         ← Event-level logging schema
│   └── metrics_schema.yaml           ← Aggregated session-level metrics schema
│
├── datasets/
│   └── pld_events_demo.jsonl         ← Sample event log (for validation)
│
├── guides/
│   └── drift_event_logging.md        ← Logging implementation guide
│
├── reports/
│   └── pld_events_demo_report.md     ← Example analysis output
│
└── dashboards/
    └── reentry_success_dashboard.json ← Operational visualization configuration
```

---

## 3. Core Metric Categories

| Class           | Purpose                                 | Example Signals                     |
| --------------- | --------------------------------------- | ----------------------------------- |
| Drift Metrics   | Detect and categorize divergence        | D2_context, D3_intent, D4_tool      |
| Repair Metrics  | Understand local vs systemic correction | Soft vs Hard Repair Count           |
| Reentry Metrics | Measure post-repair stability           | Reentry Success Rate (RE1–RE3)      |
| Timing Metrics  | UX pacing + latency sensitivity         | P95 latency, pacing-repair triggers |
| Outcome Metrics | Completion and trajectory               | Complete / Reset / Abandoned        |
| Derived KPIs    | Operational decision signals            | PRDR / VRL / FR / MRBF / REI        |

These metrics align directly with:

- `docs/07_pld_operational_metrics_cookbook.md`
- Dashboard tiles in `dashboards/reentry_success_dashboard.json`
- Session-level schema in `schemas/metrics_schema.yaml`

---

## 4. Adoption Workflow

| Phase  | Action                        | Reference                                   |
| ------ | ----------------------------- | ------------------------------------------- |
| Step 1 | Instrument runtime logging    | `schemas/pld_event.schema.json`             |
| Step 2 | Validate logged data          | `guides/drift_event_logging.md`             |
| Step 3 | Aggregate per-session metrics | `schemas/metrics_schema.yaml`               |
| Step 4 | Run analysis locally          | `reports/pld_events_demo_report.md`         |
| Step 5 | Visualize stability at scale  | `dashboards/reentry_success_dashboard.json` |


This workflow supports CI, model comparison, regression tracking and rollout validation.

---

## 5. Quick Interpretation Rules

> Use these during development and debugging:

| Observed Pattern           | Meaning                           | What to Adjust                            |
| -------------------------- | --------------------------------- | ----------------------------------------- |
| Drift ↑ + Repair Success ↑ | Interpretation OK, grounding weak | Improve constraints or RAG                |
| Drift ↑ + Hard Repair ↑    | Systemic misalignment             | Review orchestration or memory            |
| Reentry Success ↓          | Repair didn't resolve state       | Improve repair phrasing or reentry policy |
| Stable but slow responses  | User-perceived fragility          | Reduce latency or pacing                  | |

> These patterns guide runtime tuning and release gating.

---

## 7. When to Expand

Expand instrumentation when:

- Evaluating **>200 interactions**
- Running A/B or rollout experiments
- Tracking multiple repair policies or model variants
- Using dashboards as part of CI or release blocking

If you are still validating early integration:

→ **This Quickstart edition is sufficient.**

---

## 7. License

Creative Commons — **CC BY 4.0**  
© 2025 — DeepZenSpace  
Maintainer: **Kiyoshi Sasano**

---

> **PLD Metrics measure whether the agent maintains the interaction contract across turns —
not how smart the model is, but how stable the system behaves.**




