# 03 — PLD Event Schema (Applied-AI)

This document defines the **canonical data structure** for logging Phase Loop Dynamics (PLD) events in LLM agents, tool-using workflows, and multi-turn evaluation pipelines.

The schema is used when:
- generating PLD traces during runtime
- annotating turn-level Drift/Repair/Reentry events
- running PLD metrics and dashboards
- exporting datasets (e.g., MultiWOZ evaluations)

---

## 1. Data Model Overview

Each **PLD event** corresponds to one drift/repair cycle evaluation on a single turn or tool interaction.

```
Interaction → (Drift) → (Repair) → (Reentry) → Outcome check
```

Each logged event must contain:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | string (UUID) | Yes | Unique per event |
| `dialog_id` | string | Yes | Trace grouping identifier |
| `turn_index` | integer | Yes | Incrementing; aligns with log sequence |
| `drift` | enum D0–D5 | Yes | D0=none, D1–D5 per taxonomy |
| `repair` | enum R0–R4 | Yes | R0=none, R1–R4 |
| `reentry` | enum RE0–RE3 | Yes | RE0=none, RE1–RE3 |
| `outcome_complete` | boolean | Yes | Whether task state is satisfied |
| `confidence` | float 0.0–1.0 | Optional | Human/LLM confidence in annotation |
| `rationale` | text | Optional | LLM/human justification |
| `metadata` | object | Optional | Tool, timestamps, agent info |

**Values MUST match the reference taxonomy**  
(`02_pld_drift_repair_reference.md`).

---

## 2. Code Value Standards

| Category | None | Valid Codes |
|---------|------|-------------|
| Drift | `D0_none` | `D1_latency`, `D2_context`, `D3_memory`, `D4_procedural`, `D5_information` |
| Repair | `R0_none` | `R1_local`, `R2_structural`, `R3_ux`, `R4_hard_reset` |
| Reentry | `RE0_none` | `RE1_intent`, `RE2_constraint`, `RE3_workflow` |

⚠ **Coding must be single-source-of-truth** and never free-text.

---

## 3. Canonical JSON Example

```jsonc
{
  "event_id": "f07a359d-7765-490c-bf1b-3ec1b47d6aa1",
  "dialog_id": "MW24-057",
  "turn_index": 12,
  "drift": "D5_information",
  "repair": "R2_structural",
  "reentry": "RE3_workflow",
  "outcome_complete": false,
  "confidence": 0.89,
  "rationale": "DB returned 'no matches', later contradiction occurred. Structural fix triggered workflow recovery.",
  "metadata": {
    "tool_name": "db.search",
    "latency_ms": 1840,
    "timestamp": "2025-01-15T10:42:30Z"
  }
}
```

---

## 4. File Format Rules

| Rule | Details |
|------|---------|
| Line format | JSON Lines (`.jsonl`) for runtime logs |
| Ordering | Sorted by `dialog_id`, then `turn_index` |
| Export compatibility | Must pass the JSON Schema (below) |

Recommended filename convention:

```
pld_events_{source}_{YYYYMMDD}.jsonl
```

Example:
```
pld_events_demo_20250218.jsonl
```

---

## 5. Official JSON Schema Location

Runtime validators should import directly from:

```
quickstart/metrics/schemas/pld_event.schema.json
```

Do **not** duplicate schema values.  
Schema must remain a **live contract** between:

- drift detector
- repair controller
- evaluation dashboards
- datasets

---

## 6. Compatibility Checklist

| Component | Integration requirement |
|----------|------------------------|
| Labeling prompt | Field names and enums must match exactly |
| Metrics | Metrics use these enum categories |
| Casebooks | Event IDs must be linkable |
| UX latency trackers | use `metadata.latency_ms` |

If you extend `metadata`, annotate reasoning in PR.

---

## 7. Versioning Rules

Increment Major version only if:

- any enum code changes  
- mandatory field changes  

Otherwise → Minor version bump.

---

## 8. Placement

```
docs/
  ├── 03_pld_event_schema.md  ← (this file)
  └── 02_pld_drift_repair_reference.md  ← value source
```

---

Maintainer: Kiyoshi Sasano