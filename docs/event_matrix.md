---
title: "PLD Event Matrix Specification"
version: "2.0"
status: "Final"
authority: "Hard Invariant (Semantic Layer)"
applies_to: "quickstart/metrics/schemas/pld_event.schema.json"
paired_machine_source: "docs/event_matrix.yaml"
---

# PLD Event Matrix — Normative Rules

## 0. Purpose

This document defines the **semantic validation layer** for PLD runtime events.

The JSON Schema ensures **structural validity**, while this matrix ensures **semantic correctness and operational consistency**.

> A PLD event MUST satisfy both layers to be considered valid.

---

## 1. Phase ↔ Code Prefix Constraint (MUST)

### Required Mapping

| Prefix | Required Phase |
|--------|---------------|
| `D`    | drift |
| `R`    | repair |
| `RE`   | reentry |
| `C`    | continue |
| `O`    | outcome |
| `F`    | failover |

---

### Hard Rule

```sql
extract_prefix(pld.code) MUST correspond to pld.phase.
```

#### Equivalent executable form:

```python
assert PREFIX_MAP[extract_prefix(code)] == phase
```

#### Prefix Extraction Rules

```sql
Prefix = <characters before first "_"> minus trailing digits.
Example: "D4_tool_error" → "D"
```

---

#### Special Case: `phase="none"` (Normative)

Events whose `pld.phase` is `"none"`:

- **MUST NOT** use lifecycle prefixes (`D/R/RE/C/O/F`)
- **SHOULD** use free-form semantic label codes (e.g., `INFO_debug`)

Example:

| code         | phase | valid?             |
| ------------ | ----- | ------------------ |
| `INFO_debug` | none  | ✔                  |
| `SYS_init`   | none  | ✔                  |
| `D4_error`   | none  | ❌ prefix violation |

---

## 2. Event Type → Phase Alignment

### 2.1 Constraint Levels

| Level  | Meaning                  | Enforcement         |
| ------ | ------------------------ | ------------------- |
| MUST   | Required mapping         | Reject on violation |
| SHOULD | Expected/default mapping | Warn on violation   |
| MAY    | Context-controlled       | Always allowed      |

---

### 2.2 Canonical Matrix

| event_type         | allowed phase | constraint |
| ------------------ | ------------- | ---------- |
| drift_detected     | drift         | MUST       |
| drift_escalated    | drift         | MUST       |
| repair_triggered   | repair        | MUST       |
| repair_escalated   | repair        | MUST       |
| reentry_observed   | reentry       | MUST       |
| continue_allowed   | continue      | MUST       |
| continue_blocked   | continue      | MUST       |
| failover_triggered | failover      | MUST       |

---

### 2.3 Evaluative Events (SHOULD)

| event_type      | recommended phase        | constraint |
| --------------- | ------------------------ | ---------- |
| evaluation_pass | outcome                  | SHOULD     |
| evaluation_fail | outcome                  | SHOULD     |
| session_closed  | outcome (default) / none | SHOULD     |
| info            | none                     | SHOULD     |

---

### 2.4 Context-Dependent Events (MAY)

| event_type        | allowed phases | constraint                            | notes                 |
| ----------------- | -------------- | ------------------------------------- | --------------------- |
| latency_spike     | any            | MAY                                   | observability         |
| pause_detected    | any            | MAY                                   | idle                  |
| handoff           | any            | MAY                                   | system/human transfer |
| fallback_executed | any            | MAY (recommended: repair or failover) | operational override  |

---

## 3. Phase Inference Guidance (Reference Code)

```python
VALID_PHASES = ["drift", "repair", "reentry", "continue", "outcome", "failover", "none"]

def infer_phase(event_type: str, context: dict) -> str:
    current = context.get("current_phase")
    if current not in VALID_PHASES:
        current = None

    if event_type == "fallback_executed":
        if current in ["repair", "failover"]:
            return current
        return "failover"

    if event_type in ["latency_spike", "pause_detected", "handoff"]:
        return current or "none"

    return "none"
```

---

## 4. Machine Mapping Source of Truth

This document is paired with:
```bash
docs/event_matrix.yaml
```
→ That file is the normative mapping used by CI, validators, and SDKs.

---

## 5. Validation Modes

| Mode          | MUST Violations | SHOULD Violations | Intended Use                             |
| ------------- | --------------- | ----------------- | ---------------------------------------- |
| **strict**    | Reject ❌        | Ignore            | Production ingestion                     |
| **warn**      | Reject ❌        | Warn ⚠            | Staging / Model tuning                   |
| **normalize** | Auto-repair     | Warn ⚠ or accept  | Autonomous agents / runtime self-healing |

---

## 6. Validity Condition (Formal)

### Natural Language:
> An event is considered PLD-valid **only if both its schema and its semantic mapping are valid**.

### Logical Form:

```scss
PLD_valid(event) ⇔ schema_valid(event) ∧ matrix_valid(event)
```

### Machine Expression:

```python
is_valid = schema_valid(event) and matrix_valid(event)
```

---

End of Specification
