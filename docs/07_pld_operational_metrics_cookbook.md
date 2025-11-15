# 07 — PLD Operational Metrics Cookbook  
_For SRE, AgentOps, and Product Owners_  
Version: **1.0 (Operational Edition)**  
Maintainer: **Kiyoshi Sasano**  
Status: **Reference Metrics (Operational Decision Support)**  

---

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

