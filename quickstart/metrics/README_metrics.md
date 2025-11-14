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

This is the **minimal operational implementation** — fast to integrate and aligned with the full benchmark workflow used in the MultiWOZ (N=200) evaluation.

---

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

From the repository root:

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
## 3. Core Metric Categories

| Metric Class | Meaning | Examples |
|--------------|---------|----------|
| Drift Metrics | Frequency and type of divergence | D1_information_drift, D3_intent_drift |
| Repair Metrics | Whether the system corrects locally or resets | Soft Repair Rate / Hard Repair Rate |
| Reentry Metrics | Whether the agent stabilizes after repair | Reentry Success Rate (RE1–RE3) |
| Timing Metrics | Latency effects on perceived reliability | Avg Latency, High-Latency Threshold Events |
| Outcome Metrics | Completion trajectory | Complete / Partial / Abandoned / Reset |

These metrics align directly with:

- `docs/`
- `quickstart/operator_primitives/`
- `quickstart/patterns/`
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

This workflow ensures consistency across agent versions, prompting strategies, and orchestration architectures.

---

## 5. Quick Interpretation Rules

| Signal | Meaning | Suggested Action |
|--------|---------|------------------|
| Drift ↑ + Soft Repair ↑ | System is interpretable but imprecise | Improve constraints, grounding, or tool conditioning |
| Drift ↑ + Hard Repair ↑ | Architecture or memory mismatch | Review UX pacing, context access, or tool spec |
| Reentry Success ↓ | Repair is not stabilizing | Adjust confirmation pattern or reentry checkpoint |
| Outcome Complete ↑ + Latency ↑ | Stable but slow | Tune streaming, caching, or pacing strategy |

Use these rules as a runtime debugging baseline, especially during early prototyping.

---

## 6. Metrics → Action Matrix (Runtime Decision Guide)

Once events are logged and visualized, use this matrix to determine next steps.  
It connects **observation → system response → improvement path.**

| Observed Pattern (Log) | Severity | Recommended Action | Notes |
|------------------------|----------|--------------------|-------|
| Low drift frequency + high repair success | Low | Continue normal execution | System is stable |
| Repeated soft repairs on same task | Medium | Improve prompts or constraints | Often signals weak grounding |
| Frequent hard repairs | High | Review memory, tools, or orchestration logic | Indicates structural issue |
| Reentry failure after repair | Critical | Trigger fallback strategy or session reset | Prevents infinite loops |
| High abandonment rate | Critical | Analyze UX timing + failure messaging | Often perception, not logic |

This matrix should become part of your AgentOps workflow and CI evaluation strategy.

---

## 7. When to Expand

Expand this module when:

- Evaluating > 200 real interactions  
- Comparing multiple model or runtime strategies  
- Testing production traffic  
- Tracking repair policies over time in continuous deployment  

If you are still validating system fit or integration strategy:

→ **This Quickstart module is sufficient.**

---

## 8. License

Creative Commons — **CC BY-NC 4.0**  
© 2025 — DeepZenSpace  
Maintainer: **Kiyoshi Sasano**

---

> **PLD Metrics is not generic analytics —  
it is behavioral instrumentation.  
It measures whether the agent remains aligned with the interaction contract.**
