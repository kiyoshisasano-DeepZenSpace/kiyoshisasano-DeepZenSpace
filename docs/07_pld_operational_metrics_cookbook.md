# 07 — PLD Operational Metrics Cookbook  
_For SRE, AgentOps, and Product Owners_  
Version: **1.0 (Operational Edition)**  
Maintainer: **Kiyoshi Sasano**  
Status: **Reference Metrics (Operational Decision Support)**  

---

> _These metrics are optional operational extensions. They are not required to use PLD, but they help teams measure stability, compare repair strategies, and make informed release and tuning decisions._

## 1. Purpose — Why This Exists

Once PLD logging is active, most teams reach a stage where raw drift and repair counts are no longer enough to guide decisions.

Typical questions at this stage:

- “Are our repairs actually improving outcomes?”
- “Which repair strategies are worth the cost?”
- “Why does the agent feel stable technically but unreliable to users?”

This document provides **operational metrics** that can be calculated from existing logs to support **prioritization, monitoring, and tuning decisions**.

These metrics do **not modify the PLD framework** — they extend how teams interpret PLD signals in production.

---

## 2. Prerequisites

Before applying these metrics, verify:

| Requirement | Description |
|------------|-------------|
| PLD structured logs | Events conform to `pld_event.schema.json` |
| Turn-level context | Includes `session_id`, `turn_index`, event type and metadata |
| Analysis capability | SQL / Pandas / Snowflake / BigQuery / OpenSearch |
| Dashboarding | Examples: Grafana, Metabase, Looker, DataDog, Kibana (or your preferred tool) |

---

## 3. Operational Metrics

### Metric 1 — Post-Repair Drift Recurrence (PRDR)

**Purpose:** Identify whether repairs are durable or merely delaying the same drift.

**Formula:**

```
PRDR = (# of repeated drift events within N turns after a repair)
        / (total # of repairs)
```

Recommended `N`: **3–5 turns**

**Interpretation:**

| PRDR Value | Meaning | Suggested Action |
|-----------|---------|------------------|
| 0–10% | Repairs are holding | No action needed |
| 10–30% | Repairs partially effective | Review messaging or thresholds |
| >30% | Repairs fragile / repetitive | Consider: address upstream root causes (context, retrieval, tools) |

**Use Case:** Regression monitoring and repair strategy evaluation.

---

### Metric 2 — Repair Efficiency Index (REI)

**Purpose:** Compare repair strategies based on outcome improvement relative to cost.

**Formula:**

```
REI = (% improvement in task success) / (cost per session)
```

Where:

- *Task success* = improvement in completion rate or goal success (baseline vs. with repairs)
- *Cost* may include latency, tokens, or similar measurable impact

**Example Cost Function:**

⚠️ This is one possible approach — teams should adjust based on constraints.

```
cost = (token_cost * weight_token) + (latency_ms * weight_latency)
```

Your version may prioritize cost, performance, user timing expectations, or infrastructure limits.

**Interpretation:**

| REI Trend | Meaning | Action |
|-----------|---------|--------|
| Increasing | High-impact repairs | Candidate for rollout |
| Stable | Neutral tradeoff | Monitor |
| Declining | Low value or excessive cost | Simplify repair or reduce usage |

**Use Case:** A/B testing, release decision making, and cost/performance trade-off evaluation.

---

### Metric 3 — Visible Repair Load (VRL)

**Purpose:** Track the perceived stability of the agent from the user perspective.

**Formula:**

```
VRL = (# of user-visible repair messages) per 100 turns
```

Includes messages such as: *"Let me correct that,"* or *"Just to clarify..."*

**Interpretation:**

| VRL Range | User Perception | Suggested Action |
|-----------|----------------|------------------|
| 0–5 | Smooth interaction | Ideal |
| 5–20 | Noticeable but acceptable | Improve repair tone or precision |
| >20 | Perceived instability | Consider detector tuning or reducing unnecessary repairs |

**Use Case:** UX quality measurement and conversational design alignment.

---

### Metric 4 — Failover Rate (FR)

**Purpose:** Determine how frequently drift cannot be repaired and requires a controlled abort or fallback path.

**Formula:**

```
FR = (# sessions entering failover path) / (total sessions)
```

**Interpretation:**

| FR Range | Meaning | Action |
|----------|---------|--------|
| 0–5% | Expected | Normal in systems with unpredictable components (tools, retrieval, APIs) |
| 5–15% | Elevated | Review repair strategy, timeout conditions, or upstream dependency reliability |
| >15% | Problematic | Indicates systemic failure or insufficient repair paths |

---

### Metric 5 — Mean Repairs Before Failover (MRBF)

**Purpose:** Measure **how long the system persisted before giving up**.

**Formula:**

```
MRBF = Sum(repair_attempts_before_failover) / # failover sessions
```

**Interpretation:**

| Value | Meaning | Question to ask |
|-------|---------|----------------|
| 0–1 | Rapid failure | Should fail early? Is the detector too strict? |
| 2–3 | Reasonable persistence | ✔ Healthy bounded retry behavior |
| ≥4 | Excessive looping | Soft repairs ineffective → consider stronger repair or new routing logic |

> These metrics are only relevant when a system includes a **failover policy or abort semantics**, such as in `failover_recipe.md`.

---

## 4. Recommended Reporting View

```
- PRDR → Line chart (trend monitor)
- REI → Comparison bars (per repair strategy)
- VRL → Heatmap (repair types × frequency)
```

⚠️ These are examples — choose formats suitable for your reporting style and tooling.

---

## 5. Summary

These metrics turn PLD logs into **actionable operational insight**:

| Metric | Category | Role | Primary Value |
|--------|----------|------|---------------|
| PRDR | Stability | Required | Detect fragile or repeated drift patterns |
| REI | Cost vs. value | Required | Quantify repair strategy ROI |
| VRL | User experience perception | Optional | Align repairs with UX and trust outcomes |

---

**Next Step:**  
Add PRDR and REI into release evaluation, and track VRL where UX matters.

This document may evolve based on field results and implementation feedback.

---

## 📎 Appendix A — Reference Starting Points (Operational Setup)

This appendix provides **example baselines** for teams incorporating PLD metrics into production workflows.

These values are intentionally non-prescriptive — they exist to remove ambiguity during early adoption. Teams should adjust based on domain constraints, user expectations, and tolerance for recovery behavior.

---

### 1. Operational Maturity Levels

| Level | State | Suggested Metrics | Primary Focus |
|-------|-------|------------------|---------------|
| **Level 1 — Logging Only** | PLD events are consistently recorded | None | Establish dashboards and data quality baseline |
| **Level 2 — Monitoring** | Drift and repair patterns observable over time | Example: PRDR | Identify recurring failure modes |
| **Level 3 — Optimization** | Repair strategies evaluated for impact and cost | Example: PRDR + REI | A/B strategy refinement and release decisions |
| **Level 4 — Experience Management** | UX-perceived stability monitored | Example: PRDR + REI + VRL | Balance correctness, efficiency, and trust perception |

> Recommendation: Transition between levels only after metrics remain stable for **2–4 weeks**.  
> ⚠️ These levels are **guidance**, not requirements — teams may define their own maturity path.

---

### 2. Example Alert Thresholds

⚠️ These are **reference values**, not universal standards.  
Use them as starting points, then calibrate against real-world usage and operational risk.

| Metric | Example Threshold | Alert Type | Notes |
|--------|------------------|------------|-------|
| PRDR > 0.30 (rolling 50 sessions) | Warning | Suggests partially effective repairs or recurring drift |
| PRDR > 0.45 (rolling 50 sessions) | Critical | Indicates systemic failure or persistent misalignment |
| REI < baseline − 15% | Regression Gate | Used in release approvals, rollback criteria, or A/B selections |
| VRL > 18 per 100 turns | UX Review | May indicate perceptible instability despite functional correctness |

> Thresholds should evolve alongside product maturity, scale, and user expectations.

---

### 3. When to Reduce Monitoring

PLD metrics are operational signals, not permanent KPIs.

Monitoring cadence may be reduced when:

- Metrics stay within expected ranges for **4–6 consecutive weeks**, and  
- No regression is observed across releases or environment changes.

At that point, teams may shift from continuous monitoring to periodic audits (e.g., weekly reviews, release checkpoints), reducing operational overhead while retaining observability.

---


