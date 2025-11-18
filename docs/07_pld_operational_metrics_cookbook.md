<!-- License: CC BY 4.0 -->

📄 **07 — PLD Operational Metrics Cookbook**  
_For SRE, AgentOps, and Product Owners_  
Version: **1.1 (Operational Edition)**  
Maintainer: **Kiyoshi Sasano**  
Status: **Operational Reference — Used for Release, Monitoring, and Tuning**

---

> **These metrics are operational signals — not permanent KPIs.**  
They support release gating, anomaly detection, failure pattern tracking, and repair strategy evaluation — not scorekeeping.  
Metrics should be used during rollout, tuning, and regression analysis, then reduced once stability is proven.

---

### 📊 Operational Dashboard Preview

The dashboard below represents the **end-state visualization** of the metrics defined in this cookbook.  
It provides an at-a-glance understanding of whether a system is stable, drifting, cost-efficient, or entering failure-prone behavior.

<p align="center">
<img src="assets/dashboard_mockup.svg" width="100%" />
</p>

> This dashboard is a **reference implementation target**, not a requirement during early rollout.  
> It exists to provide a visual north star for teams integrating monitoring into Supabase, Grafana, Looker, Metabase, or similar platforms.

---

### How to Use This Dashboard

| Phase of rollout | Primary metrics | Purpose |
|-----------------|----------------|---------|
| **Early rollout** | PRDR, VRL, FR | Detect regressions, fragile repairs, and unstable drift loops |
| **Mid rollout** | REI, MRBF | Compare strategies, cost/benefit tradeoffs, and intervention timing |
| **Post stabilization** | FR + periodic PRDR scans | Low-noise monitoring for regressions or release effects |

---

### Interpretation Guidance

All metrics in the dashboard follow a standard operational classification:

| Marker | Meaning |
|--------|---------|
| 🟢 **Healthy Range** | Behavior stable, predictable, and cost-aligned |
| ⚠️ **Elevated / Watch** | Acceptable but may require tuning |
| 🔴 **Critical** | Indicates systemic drift, looping repairs, or user-visible instability |

Metrics are **signals** — not evaluation scores. They should guide intervention, not optimization targets.

---

### Why This Dashboard Matters

These metrics shift PLD from _logging_ to _governance_ by answering questions such as:

- _“Do repairs prevent future drift, or only delay it?”_
- _“Are visible repairs creating UX friction?”_
- _“Is the system giving up too early — or trying too long?”_
- _“Does the cost of repair justify the benefit?”_

Once operationalized, the dashboard becomes a **runtime alignment contract**:

> **Stable system behavior across turns — not just per response.**

---

### Export Targets

| Export Format | Status | Notes |
|---------------|--------|-------|
| Supabase dashboard | **Recommended baseline** | Matches mock layout |
| Grafana JSON | Planned | Requires schema mapping |
| Looker model | Optional | For enterprise analytics teams |
| CSV / notebook workflow | Built-in via queries | Useful for offline experimentation |

---

## **1. Metrics Purpose & Motivation**

Once PLD logging is active, teams quickly reach a point where raw drift/repair counts don’t answer operational questions such as:

- _“Are repairs actually improving outcomes?”_  
- _“Which repair strategies are worth the cost?”_  
- _“Why does the system appear technically stable yet feel unstable to users?”_

This cookbook provides **operationally meaningful metrics** derived from PLD runtime logs to support **monitoring, decision-making, and optimization.**

---

## **2. Prerequisites**

| Requirement | Description |
|------------|-------------|
| PLD structured logs | Conforms to `pld_event.schema.json` |
| Turn context | Includes session, turn index, event_type metadata |
| Query capability | SQL engine (Postgres, DuckDB, Snowflake, BigQuery, OpenSearch SQL mode) |
| Reporting | Grafana, Looker, Metabase, DataDog, Kibana, or equivalent |

---

## **3. Metrics**

---

### **Metric 1 — Post-Repair Drift Recurrence (PRDR)**  
**Purpose:** Measure whether repairs are **durable** or merely **delay drift recurrence**.

```
PRDR = (# of repeated drift events within N turns after a repair)
        / (total # of repairs)
```

Recommended window: **N = 3–5 turns**

#### Interpretation

| Value | Meaning | Action |
|-------|---------|--------|
| 0–10% | Repairs holding | No action |
| 10–30% | Repairs partially effective | Review repair tone/selection thresholds |
| >30% | Repairs fragile | Investigate upstream: RAG, tools, context injection |

#### Example Query (Generic SQL)

```sql
WITH repairs AS (
  SELECT session_id, turn_index AS repair_turn
  FROM pld_events
  WHERE event_type = 'repair'
),
drift_after AS (
  SELECT r.session_id, COUNT(*) AS repeated_drifts
  FROM repairs r
  JOIN pld_events e ON e.session_id = r.session_id
   AND e.turn_index BETWEEN r.repair_turn + 1 AND r.repair_turn + 5
   AND e.event_type = 'drift'
  GROUP BY r.session_id
)
SELECT SUM(repeated_drifts)::float / COUNT(*) AS PRDR
FROM drift_after;
```

---

## Metric 2 — Repair Efficiency Index (REI)
Purpose: Measure cost-benefit tradeoff of repair strategies.
```matlab
% improvement = (success_with_repairs - success_baseline) / success_baseline

REI = % improvement / cost_per_session
```
📌 Baseline must come from A/B test, rollout comparison, or historical stable window.  

Example cost model:  
```ini
cost = (tokens * w_tokens) + (latency_ms * w_latency) + (tool_calls * w_tool)
```

#### Interpretation
| Trend | Meaning | Action |
|-------|---------|--------|
| ↑ Increasing | Efficient repairs | Candidate for rollout |
| → Flat | Neutral | Monitor |
| ↓ Declining | High cost for low gain | Simplify or disable |

Example Query
```sql
SELECT
  ((AVG(success_variant) - AVG(success_baseline)) / AVG(success_baseline)) 
    AS improvement_ratio,
  AVG(cost_per_session) AS avg_cost,
  ((AVG(success_variant) - AVG(success_baseline)) / AVG(success_baseline))
    / AVG(cost_per_session) AS REI
FROM experiment_sessions;
```

---

## Metric 3 — Visible Repair Load (VRL)
Purpose: Quantify perceived stability from user experience.
```ini
VRL = (# visible repair messages per 100 turns)
```
#### Count if:
| event_type             | Count? | Example                                |
| ---------------------- | ------ | -------------------------------------- |
| `repair_visible`       | ✔      | “Let me correct that.”                 |
| `clarification_prompt` | ✔      | “Before I continue, can you confirm…?” |
| `repair_silent`        | ✖      | Internal repair only                   |

Query 
```sql
SELECT
 (COUNT(*) FILTER (WHERE event_type IN ('repair_visible','clarification_prompt')) * 100.0)
   / COUNT(*) AS VRL
FROM pld_events;
```

Interpretation
| Score | UX Perception             | Action                                                 |
| ----- | ------------------------- | ------------------------------------------------------ |
| 0–5   | Feels smooth              | Ideal                                                  |
| 5–20  | Noticeable but acceptable | Adjust tone / routing                                  |
| >20   | Feels unstable            | Reduce visible repairs or adjust detection sensitivity |

---

## Metric 4 — Failover Rate (FR)
Purpose: Detect when the agent abandons a task because repairs cannot resolve drift.
```ini
FR = (# failover sessions) / (total sessions)
```
#### Interpretation
| Value | Meaning  | Action                                       |
| ----- | -------- | -------------------------------------------- |
| 0–5%  | Expected | Normal variance                              |
| 5–15% | Elevated | Inspect failure signatures                   |
| >15%  | Systemic | Investigate detectors, upstream dependencies |

#### Implementation Note:
Failover requires explicit logging (example):
```python
log_event({
  "event_type": "failover",
  "session_id": session,
  "repair_attempts": repair_count
})
```

---

## Metric 5 — Mean Repairs Before Failover (MRBF)
Purpose: Measure persistence before giving up.
```ini
MRBF = SUM(repair_attempts_before_failover) / # failover sessions
```

Example dataset:
| session_id | repair_attempts | failover |
| ---------- | --------------- | -------- |
| s1         | 1               | ✔        |
| s2         | 3               | ✔        |
| s3         | 0               | ✖        |
→ `MRBF = (1 + 3) / 2 = 2.0`

#### Interpretation
| Value | Meaning               | Action                                   |
| ----- | --------------------- | ---------------------------------------- |
| 0–1   | Premature fail        | Relax repair trigger?                    |
| 2–3   | Healthy bounded retry | ✔ Recommended                            |
| ≥4    | Looping               | Escalate repair strength or fail earlier |

---

## **4. Summary**
| Metric | Category    | Purpose                                   |
| ------ | ----------- | ----------------------------------------- |
| PRDR   | Stability   | Detect fragile repairs                    |
| REI    | ROI         | Compare repair strategies                 |
| VRL    | UX          | Measure perceived stability               |
| FR     | Risk        | Failover frequency                        |
| MRBF   | Persistence | How long the agent tries before giving up |

---

## 5. **When to Reduce Monitoring**
Reduce dashboard frequency when:
- Metrics remain stable for 4–6 weeks, and
- No regressions occur across releases or configuration changes.
At that stage, metrics shift from active monitoring → periodic health checks.

---

> These metrics turn PLD logging into repeatable, operational decision-making.
> They are tools for governance — not targets for optimization.
