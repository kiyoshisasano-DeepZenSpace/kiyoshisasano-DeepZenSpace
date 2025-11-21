```
📄 docs/metrics/PLD_metrics_spec.md
Status: Working Draft (Candidate)
Version: 2.0.0
Audience: Engineers and researchers implementing PLD-compatible runtimes
```

---

# 1. Scope and Purpose

This document defines the **normative specification** for canonical PLD operational metrics derived from runtime event streams.

All metrics defined here are:

* **Implementation-agnostic**
* **Deterministic**
* **Derivable exclusively from PLD-valid events**
* **Aligned with PLD structural (Level 1) and semantic (Level 2) validity requirements**

This specification MUST be used when implementing metric computation and validation in PLD-compatible systems.

---

# 2. Governance and Enforcement Hierarchy

Metric computation MUST respect the following precedence order:

| Priority | Source Layer                                                  | Enforcement              |
| -------- | ------------------------------------------------------------- | ------------------------ |
| **1**    | PLD Event Schema (`pld_event.schema.json`)                    | Structural: MUST         |
| **2**    | PLD Event Matrix (`event_matrix.yaml` + supporting semantics) | Semantic: MUST           |
| **3**    | This specification                                            | Metric definitions: MUST |
| **4**    | Examples, tooling, dashboards, operational interpretation     | Informative: MAY         |

If a conflict arises, higher-priority layers MUST prevail.

---

# 3. General Requirements

## 3.1 Metric Determinism

All metrics MUST be computed solely from events that are valid under:

* The PLD event schema
* The event matrix constraints

Metrics MUST NOT depend on:

* User text or transcripts
* Model embeddings
* System-specific interpretation thresholds
* External signals not encoded in PLD event structures

## 3.2 Required Metadata Format

Every metric definition MUST include the following fields:

```
---
metric: <NAME>
version: <SEMVER>
status: <canonical|experimental|deprecated>
validation_modes: [strict|warn|normalize]
output_unit: <percent|seconds|ratio|count>
output_range: <closed or open numeric range>
schema_dependency: pld_event.schema.json
semantic_dependency: event_matrix.yaml + event_matrix.md
maturity: <C0|C1|C2|C3>
evidence: <E0|E1|E2|E3>
---
```

This metadata block MUST accompany every canonical metric entry.

## 3.3 Event Ordering

Metric calculations MUST use `turn_sequence` as the authoritative ordering signal.

If event timestamps exist but conflict with ordering derived from turn sequencing, **turn ordering prevails.**

---

# 4. Canonical Metrics (v2 Baseline)

The following metrics are the canonical baseline metrics for PLD-aligned evaluation. Additional experimental or domain-specific metrics MAY be introduced but MUST NOT redefine or conflict with metrics defined here.

---

## 4.1 PRDR — Post-Repair Drift Recurrence

### 4.1.1 Definition

A session is considered recurrent if:

* It contains at least one `repair_triggered` event, and
* It later emits a drift event (`drift_detected` or `drift_escalated`), where
* The drift occurs **after** the most recent repair.

### 4.1.2 Formal Expression

```math
PRDR =
\frac{
|\{ s \in S \mid \exists\;repair(s) \;\land\; drift\_after\_repair(s) \}|}{|\{ s \in S \mid \exists\;repair(s) \}|}
\times 100
```

Where:

* ( S ) = set of distinct session identifiers
* Ordering MUST be determined using `turn_sequence`.

---

## 4.2 VRL — Recovery Latency (Cycle-Based)

### 4.2.1 Cycle Definition

A recovery cycle is defined as:

```
drift → (zero or more repair events) → recovery
```

A recovery event MUST be one of:

| event_type         | required phase |
| ------------------ | -------------- |
| `reentry_observed` | `reentry`      |
| `continue_allowed` | `continue`     |

If no recovery event occurs within an implementation-defined cutoff (default: 10 turns), the cycle result MUST be recorded as `"NaN"`.

### 4.2.2 Formal Expression

```math
VRL =
\text{mean}(
timestamp(recovery\_event_i)
-
timestamp(first\_drift\_event_i)
)
```

Each implementation MUST compute at minimum:

* mean
* median
* p95 percentile

Aggregation MUST be performed per recovery cycle, not per event.

---

## 4.3 FR — Failover Recurrence Index

### 4.3.1 Definition

This metric measures the proportion of failover events relative to lifecycle events.

Only events whose lifecycle phase is one of:

```
drift, repair, reentry, continue, outcome, failover
```

MAY contribute to the denominator.

### 4.3.2 Formal Expression

```math
FR =
\frac{
\#(failover\_triggered)
}{
\#(lifecycle\_events)
}
```

Where:

* `failover_triggered` MUST be counted only when its phase is `failover`.
* `lifecycle_events` MUST include only events with valid lifecycle phases as defined by the PLD event matrix.

---

# 5. Validation Requirements

Metric computation MUST respect runtime validation mode rules:

| Mode      | Behavior                                                                                      |
| --------- | --------------------------------------------------------------------------------------------- |
| strict    | MUST reject events violating MUST-level rules; rejected events MUST NOT contribute to metrics |
| warn      | MUST reject MUST-level violations; SHOULD allow SHOULD-level violations                       |
| normalize | MUST attempt normalization using event matrix; normalized events MAY contribute if valid      |

Normalization MUST NOT modify original persisted logs.

---

# 6. Versioning and Evolution

All metrics in this document are versioned. Changes to formulas, scope, or meaning MUST increment metric version identifiers, even if the global specification version remains constant.

No metric name MAY be reused for a different definition.

---

## End of Specification

Source basis: `07_pld_operational_metrics_cookbook.txt`
