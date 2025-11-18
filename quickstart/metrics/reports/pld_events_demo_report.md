---
title: "PLD Runtime Metrics — Demo Analysis Report"
version: 2025.1.1
status: reference
maintainer: "Kiyoshi Sasano"
source_dataset: "datasets/pld_events_demo.jsonl"
category: "metrics/reports"
tags:
  - PLD
  - runtime telemetry
  - drift
  - repair
  - failover
  - metrics
---

# 📊 PLD Runtime Metrics — Demo Analysis Report  
_Sample Dataset Evaluation (Schema-Aligned)_

This report demonstrates how to interpret PLD-structured runtime logs using the demo dataset:

```
datasets/pld_events_demo.jsonl
```

The purpose is to illustrate:

- Drift frequency and patterns  
- Repair behavior effectiveness  
- Reentry success signals  
- Failover risk signatures  
- Operational metrics from the PLD cookbook (PRDR, VRL, FR, MRBF)

---

## 1. Dataset Summary

| Metric | Value |
|--------|-------|
| Total sessions | **4** |
| Total logged events | **22** |
| Drift events (`event_type = drift_detected`) | **3** |
| Repair attempts (`event_type = repair_triggered`) | **10** |
| Reentry observations | **1** |
| Failovers | **1** |

> Note: This dataset is intentionally small and designed for schema validation—not benchmarking.

---

## 2. Operational Metrics (Cookbook-Aligned)

| Metric | Result | Status |
|--------|--------|--------|
| **PRDR — Post-Repair Drift Recurrence** | **50%** | ⚠ Elevated |
| **VRL — Visible Repair Load** | **12%** | ⚠ Noticeable |
| **FR — Failover Rate** | **25%** | 🔴 Critical |
| **MRBF — Mean Repairs Before Failover** | **7.0** | ⚠ High Persistence |
| **REI — Repair Efficiency Index** | _Not computable_ | (Requires baseline) |

📌 Interpretation:

> Repairs occur — but do not reliably prevent repeated drift, and escalation continues until failover.

---

## 3. Drift Pattern Analysis

| Code | Count | Notes |
|------|-------|-------|
| `D4_tool` | 2 | Tool execution failure recurring |
| `D5_information` | 1 | Interpretation mismatch |

**Observation:**  
Most drift originates from **tool execution failures**, not user intent ambiguity.

---

## 4. Repair Pipeline Behavior

| Repair Code | Instances | Type | Escalation Outcome |
|-------------|-----------|------|--------------------|
| `R2_soft_repair` | 9 | Automated retry-based soft repair | Did not prevent eventual failover |
| `R1_clarify` | 1 | Visible clarification | Followed by successful reentry |

Key Finding:

> Visible clarifying repairs (`repair_visible`) correlate with successful reentry, while repeated silent soft repair loops correlate with failover.

---

## 5. Reentry Stability

| Session | Event | Result |
|---------|-------|--------|
| `SESS-OK-01` | `reentry_observed (RE3_auto)` | ✔ Stable continuation |

Takeaway:

> Reentry success appears strongly influenced by **repair transparency + low latency.**

---

## 6. Failover Signals

Failover occurred in session: **`SESS-FAIL-01`**  
Characteristics:

- 7 consecutive soft repairs  
- No reentry attempt  
- Failover code: `OUT3_abandoned`

**Pattern matches:** _repair loop → no stabilization → abandonment_

---

## 7. Recommendations

| Priority | Action |
|----------|--------|
| ⭐⭐⭐ Introduce escalation threshold to prevent 7+ repair loops |
| ⭐⭐ Increase visibility of soft repairs to improve VRL → reentry success |
| ⭐ Evaluate tool failure detection timing |

---

## 8. Next Steps

To operationalize:

1. Connect logging to live runtime  
2. Accumulate ≥ **500–1000 real sessions**  
3. Feed into:  
   ```
   dashboards/reentry_success_dashboard.json
   ```  
4. Compare variants with PRDR + FR as gating metrics.

---

Report generated using the **PLD Metrics Quickstart Framework (v2025.1.1)**.  
License: **CC BY 4.0**

