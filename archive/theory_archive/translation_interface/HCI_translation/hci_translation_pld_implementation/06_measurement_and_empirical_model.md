# Measurement and Empirical Model — PLD → HCI Implementation  
**Folder:** `06_translation_interface/HCI_translation/hci_translation_pld_implementation/`  
**Version:** 1.0 • Last updated: 2025-10-13  
**License:** CC BY-NC 4.0  
**Maintainer:** Phase Loop Dynamics Research Group

---

## 1. Purpose

This document defines the **measurement framework** and **empirical modeling pipeline** for Phase Loop Dynamics (PLD) within HCI systems.  
It bridges **behavioral telemetry** (e.g., drift, repair, reentry, latency hold) with **statistical models** used to evaluate rhythmic coordination and adaptive performance.

---

## 2. Measurement Objectives

1. **Quantify rhythm and recovery** across drift–repair–reentry cycles.  
2. **Evaluate timing adaptation** (L₃) via latency, hesitation, and interrupt data.  
3. **Estimate coherence** between system tempo and user response tempo.  
4. **Predict stability and engagement** via empirical PLD coefficients.  
5. **Provide reproducible metrics** compatible with HCI experimental design (A/B tests, within-subject comparisons).

---

## 3. Core Metrics (from Schema)

| Metric | Description | Formula / Source |
|--------|--------------|------------------|
| `drift_to_repair_ratio` | How often drift leads to repair | drift_detected.count / repair_triggered.count |
| `reentry_success_rate` | User recovery effectiveness | reentry_success.count / reentry_attempts |
| `avg_latency_hold` | Mean intentional delay | latency_hold.sum(duration_ms) / latency_hold.count |
| `latency_interrupt_rate` | User cancellations of pacing | latency_hold.count(user_cancelled=true) / latency_hold.count |
| `time_to_repair` | Average lag (drift → repair) | mean(Δt) between drift_detected and repair_triggered |
| `repair_loop_depth` | Max consecutive repairs per context | max(repair_triggered per context_id) |
| `ρ_resonance` | Synchrony between user and system | Pearson or circular correlation of tempo time-series |

---

## 4. Empirical Model Overview

We model user–system dynamics as a **temporal feedback process**, where drift and repair are coupled via **phase delay** and **alignment gain**.

Let:  
- `D(t)` = drift occurrence rate  
- `R(t)` = repair rate  
- `τ` = latency control (ms)  
- `ρ` = coherence coefficient (−1 ≤ ρ ≤ 1)

### 4.1 Linearized feedback model
```math
R(t) = α * D(t−τ) + β * Δρ(t)
```
where:
- `α` = sensitivity to drift frequency  
- `β` = resonance correction gain  
- `Δρ(t)` = change in local tempo coherence

### 4.2 Exponential decay recovery
Recovery likelihood decays with unresolved drift duration:

```math
P(reentry | drift) = 1 − e^{−λ * Δt}
```
`λ` estimated empirically from inter-event intervals (`Δt` between drift and reentry).

### 4.3 Temporal alignment coefficient
Quantifies stability of response timing relative to pacing latency.

```math
ρ_tempo = corr(τ_system, τ_user)
```

---

## 5. Experimental Pipeline (Implementation Steps)

| Step | Description | Output |
|------|--------------|--------|
| 1 | Collect event logs (`pld_events.jsonl`) | raw data |
| 2 | Validate via `pld_event.schema.json` | validation report |
| 3 | Aggregate per session (group by `session_id`) | drift/repair counts |
| 4 | Compute derived metrics (Python/R) | analytics table |
| 5 | Fit empirical models (e.g., OLS, mixed-effects) | parameters α, β, λ, ρ |
| 6 | Visualize trends (dashboard/plotly/matplotlib) | time-series charts |
| 7 | Export summary for research archive | CSV or parquet |

---

## 6. Data Processing Specification (Python Example)

```python
import pandas as pd

events = pd.read_json("pld_events.jsonl", lines=True)
events["timestamp"] = pd.to_datetime(events["timestamp"])

# Compute drift → repair latency
drifts = events[events.event_type == "drift_detected"]
repairs = events[events.event_type == "repair_triggered"]

merged = pd.merge_asof(repairs.sort_values("timestamp"),
                       drifts.sort_values("timestamp"),
                       by="session_id", direction="backward", tolerance=pd.Timedelta("5m"),
                       suffixes=("_repair", "_drift"))

merged["time_to_repair"] = (merged["timestamp_repair"] - merged["timestamp_drift"]).dt.total_seconds()
avg_latency = merged["time_to_repair"].mean()
print("Average time to repair:", round(avg_latency, 2), "s")
```

---

## 7. Regression Model Example (Empirical Fit)

```python
import statsmodels.api as sm

X = merged[["confidence_score_drift", "time_to_repair"]]
X = sm.add_constant(X)
y = merged["goal_completed"].astype(int)

model = sm.Logit(y, X).fit()
print(model.summary())
```

This model estimates how **confidence score** and **repair timing** predict successful reentry or task completion.

---

## 8. PLD–Resonance Empirical Fit

Compute temporal coherence between user and system rhythms:

```python
import numpy as np

def coherence(series_sys, series_user):
    return np.corrcoef(series_sys, series_user)[0, 1]

ρ = coherence(tau_system, tau_user)
print("Tempo coherence (ρ):", round(ρ, 3))
```

> ρ ≥ 0.7 → stable alignment (resonance).  
> ρ < 0.3 → desynchronization (requires timing recalibration).

---

## 9. Dashboard & Visualization

**Recommended Views:**  
- *Line chart*: Reentry rate over time  
- *Bar chart*: Avg. latency vs. success rate  
- *Heatmap*: Drift occurrences by UI state  
- *Scatter*: Drift confidence vs. repair time  
- *Circular plot*: Resonance ρ over time (phase wheel)

All dashboards derive from the validated event stream and support **UTC normalization** and **live refresh (≤60s)**.

---

## 10. Experimental Design Templates

### 10.1 Within-subject (timing adaptation)
- Condition A: τ = 900 ms  
- Condition B: τ = 1200 ms  
- Measure: task success rate, ρ_tempo, subjective rhythm rating (Likert).

### 10.2 Between-group (repair strategy)
- Group 1: soft clarification only  
- Group 2: repair + reentry suggestion  
- Compare: reentry_success_rate, drift_to_repair_ratio, avg_latency_hold.

### 10.3 A/B test integration
```sql
SELECT variant, AVG(goal_completed::int) AS success_rate
FROM experiment_results
GROUP BY variant;
```

---

## 11. Model Evaluation Criteria

| Metric | Target | Interpretation |
|---------|---------|----------------|
| R² or pseudo-R² | ≥ 0.6 | Good model fit |
| p < 0.05 | Significant operator effect |
| AIC/BIC | minimized | Optimal parameterization |
| RMSE < 0.2 | Stable prediction |
| ρ_tempo ≥ 0.7 | Rhythmic resonance achieved |

---

## 12. Reporting Standards (HCI Publication Alignment)

When publishing empirical PLD–HCI results, report:

1. **Event statistics** (counts, ratios, timing distributions).  
2. **Model parameters** (α, β, λ, ρ) with confidence intervals.  
3. **Experimental configuration** (τ values, operator tiers, UI design).  
4. **Error handling** (dropped sessions, schema violations).  
5. **Interpretability notes** — e.g., whether resonance was observed as increased engagement or decreased hesitation.

---

## 13. Export Formats

| Type | Format | Notes |
|------|---------|------|
| Raw Logs | `.jsonl` | per-event records |
| Aggregated Metrics | `.csv`, `.xlsx` | for dashboard imports |
| Model Outputs | `.pkl`, `.rds` | parameter persistence |
| Reports | `.md`, `.pdf` | publishable summaries |

---

## 14. Compliance Checklist

- [ ] Logs validated against `pld_event.schema.json`.  
- [ ] Metrics computed for all major operators (L₂–L₅).  
- [ ] Latency intervals normalized (ms → s).  
- [ ] Coherence ρ computed for ≥ 30 interactions per session.  
- [ ] A/B or within-subject test conducted.  
- [ ] Report includes statistical summary + dashboard snapshot.

---

> “Measurement closes the rhythm; modeling explains it.”  
> — *Phase Loop Dynamics, 2025*
