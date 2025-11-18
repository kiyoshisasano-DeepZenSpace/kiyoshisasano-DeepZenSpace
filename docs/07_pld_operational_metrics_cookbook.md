<!-- License: CC BY 4.0 -->

# 📄 07 — PLD Operational Metrics Cookbook  
_For SRE, AgentOps, Data Engineering, and Product Owners_  

**Version:** 1.1 (Runtime Alignment Edition)  
**Maintainer:** Kiyoshi Sasano  
**Status:** ✔ Operational — Production Ready  

---

> **PLD metrics are operational signals — not product KPIs.**  
They help teams detect drift loops, evaluate repair strategy effectiveness, reduce user-visible instability, and prevent runaway retries.

Metrics should guide **rollout safety, debugging, release gating, and regression detection** — not leaderboard optimization.

---

## 📊 Operational Dashboard Reference

This cookbook defines the metrics used in the operational dashboard below.  
BI teams (Supabase, Grafana, Datadog, Kibana, Looker, Metabase) should reference this document when implementing dashboards.

<p align="center">
<img src="assets/dashboard_mockup.svg" width="100%" />
</p>

> This visualization is a **reference target** — teams may start with single queries and evolve toward the full dashboard.

---

## 🧭 How to Use This Dashboard

| Deployment Phase | Primary Metrics | Purpose |
|-----------------|----------------|---------|
| **Early rollout** | PRDR, VRL, FR | Detect regressions and unstable repair loops |
| **Mid rollout** | REI, MRBF | Compare repair strategies and measure cost/benefit |
| **Stabilized** | FR + periodic PRDR | Low-noise regression monitoring |

---

## 🧪 Interpretation Standard

All metrics in this cookbook follow a consistent semantic structure:

| Marker | Meaning |
|--------|---------|
| 🟢 Healthy | Expected, stable runtime behavior |
| ⚠ Elevated | Acceptable but requires observation |
| 🔴 Critical | Drift instability, persistent looping, or failure patterns |

> Metrics guide action — they are **not optimization targets**.

---

## 🔌 Schema Requirements

Metrics require PLD logging with the `v1.1` schema:

📄 **Schema:** `quickstart/metrics/schemas/pld_event.schema.json`  
📦 **Dataset Example:** `quickstart/metrics/datasets/pld_events_demo.jsonl`

### Event Mapping (v1.1)

| Logical Category | `event_type` | PLD Phase | Code Prefix |
|------------------|-------------|-----------|------------|
| Drift detection | `drift_detected` | `drift` | `D*` |
| Repair attempt | `repair_triggered` | `repair` | `R*` |
| Visible repair | `repair_visible` | `repair` | `R*` |
| Reentry success | `reentry_observed` | `reentry` | `RE*` |
| Failover | `failover_triggered` | `failover` | `OUT*` or `F*` |

---

## 📐 Metric 1 — Post-Repair Drift Recurrence (PRDR)

**Purpose:**  
Measure whether repairs permanently resolve drift or merely delay recurrence.

```
PRDR = repeated drift events (within N turns after repair)
        ÷ total repair events
```

**Recommended Window:** `N = 3–5 turns`

### Classification

| Rate | Meaning | Action |
|------|---------|--------|
| 🟢 0–10% | Durable repairs | No changes required |
| ⚠ 10–30% | Partial improvement | Adjust tone/threshold/tooling |
| 🔴 >30% | Fragile repair strategy | Investigate upstream (RAG, tools) |

### PostgreSQL Query

```sql
WITH repairs AS (
  SELECT session_id, turn_id AS repair_turn
  FROM pld_events
  WHERE event_type = 'repair_triggered'
),
drifts AS (
  SELECT r.session_id, COUNT(*) AS repeated_drift
  FROM repairs r
  JOIN pld_events e
    ON e.session_id = r.session_id
   AND e.turn_id BETWEEN r.repair_turn + 1 AND r.repair_turn + 5
   AND e.event_type = 'drift_detected'
  GROUP BY r.session_id
)
SELECT
  COALESCE(SUM(repeated_drift), 0)::float / NULLIF(COUNT(*), 0) AS prdr
FROM drifts;
```

---

## ⚙ Metric 2 — Repair Efficiency Index (REI)

**Purpose:** Evaluate whether repairs provide a net benefit relative to operational cost.

```
REI = (performance improvement %) ÷ operational cost per session
```

Cost may include: tokens, latency, hallucination risk, tool usage, or user experience penalties.

### Interpretation

| Trend | Meaning | Action |
|-------|---------|--------|
| ↑ Increasing | Efficient strategy | Candidate for broader rollout |
| → Flat | Neutral | Monitor only |
| ↓ Declining | Cost > benefit | Simplify or disable strategy |

### Query Template (PostgreSQL Example)

Requires a baseline value (A/B, staged rollout, or historical window).

```sql
SELECT
  ((AVG(success_variant) - AVG(success_baseline)) / AVG(success_baseline))
    AS improvement_ratio,
  AVG(cost_score) AS avg_cost,
  ((AVG(success_variant) - AVG(success_baseline)) / AVG(success_baseline))
    / AVG(cost_score) AS rei
FROM experiment_sessions;
```

---

## 👁 Metric 3 — Visible Repair Load (VRL)

**Purpose:** Measure user-visible instability.

```
VRL = (# visible repair messages per 100 turns)
```

### Included Signals:

| event_type | Count? | Example |
|------------|--------|---------|
| `repair_visible` | ✔ | "Let me fix that…" |
| `clarification_prompt` | ✔ | "Before I continue…" |
| `repair_triggered` only | ✖ | Internal-only repair |

### Query

```sql
SELECT
  (COUNT(*) FILTER (WHERE event_type IN ('repair_visible', 'clarification_prompt')) * 100.0)
    / COUNT(*) AS vrl
FROM pld_events;
```

### Classification

| Score | UX Interpretation | Action |
|-------|------------------|--------|
| 🟢 0–5 | Feels smooth | Ideal |
| ⚠ 5–20 | Noticeable | Adjust tone or trigger sensitivity |
| 🔴 >20 | Unstable UX | Reduce repair visibility |

---

## 🛑 Metric 4 — Failover Rate (FR)

**Purpose:** Detect when the agent abandons tasks due to unresolvable drift.

```
FR = # failover sessions ÷ total sessions
```

### Query

```sql
SELECT
  COUNT(DISTINCT session_id) FILTER (WHERE event_type = 'failover_triggered')::float
  / COUNT(DISTINCT session_id) AS failover_rate
FROM pld_events;
```

### Thresholds

| Value | Meaning | Action |
|-------|---------|--------|
| 🟢 0–5% | Expected | Normal variance |
| ⚠ 5–15% | Elevated | Inspect failure patterns |
| 🔴 >15% | Systemic | Investigate drift detectors and repair design |

---

## 🔁 Metric 5 — Mean Repairs Before Failover (MRBF)

**Purpose:** Measure persistence before system abandonment.

```
MRBF = total repairs before failover ÷ number of failover sessions
```

### Query

```sql
WITH failovers AS (
  SELECT session_id
  FROM pld_events
  WHERE event_type = 'failover_triggered'
)
SELECT
  AVG(
    (SELECT COUNT(*) FROM pld_events e
     WHERE e.session_id = f.session_id
       AND e.event_type = 'repair_triggered')
  ) AS mrbf
FROM failovers f;
```

### Interpretation

| Value | Meaning | Action |
|-------|---------|--------|
| 🟢 0–1 | Premature fail | Loosen thresholds |
| 🟡 2–3 | Healthy retry window | Recommended |
| 🔴 ≥4 | Repair loop | Escalate strength or fail earlier |

---

## 🧪 Quickstart: Run Metrics on Demo Dataset

1. Load demo data:

```sql
CREATE TABLE pld_events_raw (data jsonb);

\copy pld_events_raw (data)
FROM 'quickstart/metrics/datasets/pld_events_demo.jsonl';
```

2. Normalize into a queryable view:

```sql
CREATE VIEW pld_events AS
SELECT
  data->>'event_id' AS event_id,
  data->>'session_id' AS session_id,
  (data->>'turn_id')::int AS turn_id,
  data->>'event_type' AS event_type,
  data->'pld'->>'phase' AS phase,
  data->'pld'->>'code' AS code,
  (data->'runtime'->>'latency_ms')::numeric AS latency_ms,
  data
FROM pld_events_raw;
```

3. Run metric queries (PRDR, VRL, FR, MRBF).
4. Import `quickstart/metrics/dashboards/reentry_success_dashboard.json` into your BI tool.

---

## Summary

| Metric | Category | Purpose |
|--------|----------|---------|
| **PRDR** | Stability | Detect fragile repair behavior |
| **REI** | ROI | Evaluate cost vs benefit |
| **VRL** | UX | Track visible instability |
| **FR** | Failure tolerance | Detect unresolved drift |
| **MRBF** | Persistence | Identify looping repair patterns |

---

> **When metrics flatten and remain healthy for 4–6 weeks, monitoring shifts from continuous to periodic validation.**

---

**End of Document**
