---
title: "PLD Metrics Module — Quickstart Edition"
version: 2025.1
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

This folder provides the **measurement layer** of the PLD Applied Interaction Framework.  
Its purpose is to help developers **log, evaluate, and visualize** how well an agent detects drift, performs repairs, reenters alignment, and maintains conversational stability.

This is the **minimal operational implementation** — fast to integrate and aligned with the evaluation workflow used in the MultiWOZ (N=200) baseline.

---

### 🚀 Quick Validation — Run Metrics Locally

If you want to run the PLD metrics against the bundled demo dataset:

```bash
cd quickstart/metrics
pip install duckdb
python verify_metrics_local.py
```
This script demonstrates how PLD runtime events turn into measurable
stability metrics.

## 1. What This Module Enables

Once integrated, you can:

- Log system events using a **standard PLD JSON schema**
- Track Drift / Soft Repair / Hard Repair / Reentry / Outcome
- Generate stability dashboards and longitudinal comparisons
- Compare system versions and prompting strategies
- Integrate metrics into:

  - LangChain / LangGraph  
  - OpenAI Assistants API  
  - Rasa / Dialogue Managers  
  - Custom orchestration pipelines  

This module is designed for **runtime observability**, not offline annotation.

---

## 2. Module Structure

```txt
quickstart/metrics/
│
├── README_metrics.md                 ← You are here
│
├── schemas/                          ← Canonical data definitions
│   ├── pld_event.schema.json         ← PLD event-level schema
│   └── metrics_schema.yaml           ← Field dictionary + definitions
│
├── datasets/                         ← Example data
│   └── pld_events_demo.jsonl         ← Sample PLD log file
│
├── guides/                           ← Implementation guidance
│   └── drift_event_logging.md        ← How to instrument runtime logging
│
├── reports/                          ← Example evaluation outputs
│   └── pld_events_demo_report.md     ← Summary analysis of the demo dataset
│
└── dashboards/                       ← Visualization presets
    └── reentry_success_dashboard.json ← Metrics dashboard template
```

---

## 3. Core Metric Categories

| Metric Class | Meaning | Examples |
|--------------|---------|----------|
| Drift Metrics | Frequency and type of divergence | D1_information_drift, D3_intent_drift |
| Repair Metrics | Local correction vs systemic reset | Soft Repair Rate / Hard Repair Rate |
| Reentry Metrics | Stability after repair | Reentry Success Rate (RE1–RE3) |
| Timing Metrics | Latency effects and UX perception | Avg Latency, High-Latency Flags |
| Outcome Metrics | Completion trajectory | Complete / Partial / Abandoned / Reset |

These metrics align directly with:

- `docs/`
- `docs/07_pld_operational_metrics_cookbook.md` (PRDR, REI, VRL definitions)
- `quickstart/operator_primitives/`
- `quickstart/patterns/04_integration_recipes/`
- `metrics_studies/multiwoz_2.4_n200/`

---

## 4. Adoption Workflow

| Phase | Action | Reference |
|-------|--------|-----------|
| Step 1 | Instrument logging | `schemas/pld_event.schema.json` |
| Step 2 | Validate schema compliance | `schemas/metrics_schema.yaml` |
| Step 3 | Produce sample log | `datasets/pld_events_demo.jsonl` |
| Step 4 | Run evaluation | `reports/pld_events_demo_report.md` |
| Step 5 | Visualize stability | `dashboards/reentry_success_dashboard.json` |

This workflow enables consistent comparison across model versions, prompting strategies, and orchestration architectures.

---

## 5. Quick Interpretation Rules

> Use these as a **runtime debugging compass** during early prototyping.

| Signal | Meaning | Suggested Action |
|--------|---------|------------------|
| Drift ↑ + Soft Repair ↑ | System is interpretable but imprecise | Improve constraint clarity or grounding signals |
| Drift ↑ + Hard Repair ↑ | Architecture or memory mismatch | Review orchestration, tool routing, or context windows |
| Reentry Success ↓ | Repair did not stabilize | Adjust checkpoint phrasing or confirmation policy |
| Outcome Complete ↑ + Latency ↑ | Stable but slow | Optimize streaming, caching, or UX pacing |

> For an end-to-end applied example showing metrics in practice:  
> **`/analytics/case_study_end_to_end.md`**

---

## 6. Metrics → Action Matrix (Runtime Decision Guide)

Once events are logged and visualized, use this matrix to determine next steps.  
It connects **observed patterns → system response → improvement pathway.**

| Observed Pattern (Log) | Severity | Suggested Action | Notes |
|------------------------|----------|------------------|-------|
| Low drift frequency + high repair success | Low | Continue execution | System is functioning as expected |
| Repeated soft repairs on same flow | Medium | Improve constraints or grounding | Often indicates partial context ambiguity |
| Frequent hard repairs | High | Review memory, tools, and runtime architecture | Strong signal of structural mismatch |
| Reentry failure after repair | Critical | Trigger fallback strategy or session reset | Prevents repeated stall loops |
| High abandonment rate | Critical | Analyze UX pacing and communication | Often a perception failure, not a logic defect |

---

## 7. When to Expand

Expand this module when:

- Evaluating **>200 interactions**
- Comparing **multiple model or runtime variants**
- Running **production experiments**
- Tracking **repair policies over time in CI/CD**

If you are still validating early integration:

→ **This Quickstart edition is sufficient.**

---

## 8. License

Creative Commons — **CC BY 4.0**  
© 2025 — DeepZenSpace  
Maintainer: **Kiyoshi Sasano**

---

> **PLD Metrics is not general analytics —  
it is behavioral instrumentation.  
It measures whether an agent maintains alignment with the interaction contract.**



