---
title: "PLD Event Log — Demo Analysis Report"
version: 2025.1
status: reference
maintainer: "Kiyoshi Sasano"
source_dataset: "datasets/pld_events_demo.jsonl"
category: "metrics/reports"
tags:
  - PLD
  - metrics
  - analysis
  - drift
  - repair
  - reentry
---

# 📊 PLD Event Log — Demo Analysis Report (Sample Dataset)

This document demonstrates how to interpret logged PLD interaction events using the sample dataset located in:

```
datasets/pld_events_demo.jsonl
```

The goal is to illustrate **how drift, repair, reentry, and timing signatures** can be extracted and summarized from raw logs.

---

## 1. Dataset Overview

| Metric | Value |
|--------|-------|
| Total sessions | **10** |
| Total turns | **124** |
| Drift events | **27** |
| Repair events | **21** |
| Hard repairs | **4** |
| Reentry attempts | **18** |
| Average latency | **2.1s** |

This dataset represents a **controlled simulation**, intended for validating:

- schema integrity  
- ingestion pipelines  
- metric extraction logic  

before scaling to production or benchmark datasets (e.g., MultiWOZ-based evaluation).

---

## 2. Drift Distribution

| Drift Type | Count | Share |
|------------|-------|-------|
| Drift-Information | 13 | 48% |
| Drift-Procedure | 7 | 26% |
| Drift-Intent | 5 | 18% |
| Drift-Contradiction | 2 | 8% |

> **Interpretation:** Most drift stems from assumption errors and incorrect information rather than instruction misunderstanding.

This suggests the model **believes it is correct before context is stable** — a known risk pattern in PLD systems.

---

## 3. Repair Behavior

| Repair Type | Count | Success Rate |
|-------------|-------|--------------|
| SoftRepair-AddOptions | 9 | 78% |
| SoftRepair-Clarify | 5 | 60% |
| SoftRepair-ConstraintConfirm | 3 | **100%** |
| HardRepair-ResetSession | 4 | 50% |

📌 Key Insight:

> **Soft repair is highly effective when triggered early.**  
Delays increase the escalation path toward hard reset.

---

## 4. Reentry Outcome Analysis

| Result | Count |
|--------|-------|
| Successful Reentry | **12** |
| Partial Recovery | **4** |
| Failed Reentry | **2** |

Observed patterns:

- Silent correction → ❌ higher failure rate  
- Explicit acknowledgment → ✔ better alignment  
- Confirmation phrasing boosted success probability

Example of high-performing phrasing:

```
“Let me correct that — here are the available hotels under your selected budget.”
```

---

## 5. Latency Correlation

Latency strongly influenced drift and repair patterns:

- Drift clusters emerged when latency exceeded **3.2s**
- Hard repair likelihood doubled after latency spike + drift pairing
- Reentry success highest when response time post-repair was **< 1.5s**

⏱ Latency functions as a **secondary destabilizer** — even when logic is correct.

---

## 6. Summary of Findings

### ✔ System Strengths

- Drift was detected in most cases rather than ignored  
- Early-stage soft repair preserved conversational continuity  
- Reentry patterns successfully stabilized the task flow  

### ⚠ Weaknesses Observed

- Repair triggers lacked consistency across drift types  
- Some repairs occurred **multiple turns** after the drift signal  
- Latency spikes amplified perceived unreliability  

---

## 7. Engineering Recommendations

| Priority | Recommendation |
|----------|---------------|
| ⭐⭐⭐ Enable drift prediction **before tool execution** |
| ⭐⭐ Standardize thresholds for triggering soft repair |
| ⭐ Improve latency smoothing + pacing microcopy |

---

## 8. Next Steps

To operationalize scaling:

1. Deploy runtime logging to match schema  
2. Record at least **≥ 1,000 live conversations**  
3. Compute continuous metrics from logs  
4. Load `dashboards/reentry_success_dashboard.json`  
5. Compare system variants against baseline checkpoints  

---

## Attribution

Generated using the **PLD Quickstart Metrics Framework**.  
© 2025 — Kiyoshi Sasano / Contributors  
License: CC BY-NC 4.0