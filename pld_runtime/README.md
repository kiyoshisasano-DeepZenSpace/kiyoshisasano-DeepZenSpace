---
title: "PLD Runtime Package"
version: "2025.1"
status: stable
maintainer: "Kiyoshi Sasano"
tags:
  - runtime
  - pld
  - agent-governance
  - orchestration
license: "CC BY-NC 4.0"
---

# PLD Runtime Package  
Operational Engine for Phase Loop Dynamics

This module implements the **runtime execution layer** of Phase Loop Dynamics (PLD).

Where `docs/` defines the theory and taxonomy,  
the runtime answers a concrete question:

> **“Given real turns, signals, and system behavior — what should happen next?”**

The runtime converts:

- raw turns, traces, and conversations  
- detection signals (Drift → Repair → Reentry → Outcome)  
- policies and governance constraints  

into:

- actionable system decisions  
- structured traces for evaluation  
- stable stateful behavior across turns

---

## 1. Package Structure

Each top-level module reflects a PLD lifecycle stage.

```
01_schemas/      # Structural contract + validation formats
02_ingestion/    # Normalize turns → Unified runtime input
03_detection/    # Drift, repair, reentry signal detection
04_enforcement/  # Structural + temporal policy checks
05_controllers/  # State machine + runtime governance
06_logging/      # JSONL, trace emitters, telemetry exporters
07_failover/     # Safety nets, escalation, controlled resets
```

All directory numbers are **stable identifiers** and part of the public API.

---

## 2. Module Overview

Each section includes: purpose → responsibilities → example artifacts.

---

### 2.1 — `01_schemas/` (Contract Baseline)

**Purpose**  
Defines canonical data contracts for runtime processing.

**Artifacts**
- `pld_event.schema.json`
- `runtime_event_envelope.json`

**Responsibilities**
- Validate event structure
- Ensure compatibility across modules and external tools

> _Everything downstream assumes these schemas do not silently change._

---

### 2.2 — `02_ingestion/` (Normalization Layer)

**Purpose**  
Convert heterogeneous input into:

```
NormalizedTurn(session_id, turn_id, role, text, runtime)
```

**Artifacts**
- `normalization.py`
- `ingestion_config.py`
- dataset adapters (e.g., MultiWOZ-compatible)

**Responsibilities**
- Normalize roles (`user`, `assistant`, `system`, `tool`)
- Guarantee consistent sequencing before detection

---

### 2.3 — `03_detection/` (Signal Layer)

**Purpose**  
Transform normalized turns into PLD signals:

```
Drift → Repair → Reentry → Outcome
```

**Artifacts**
- `drift_detector.py`
- `repair_detector.py`
- `pattern_classifier.py`
- `runtime_signal_bridge.py`

**Responsibilities**
- Detection only (no enforcement decisions)

---

### 2.4 — `04_enforcement/` (Policy Validation Layer)

**Purpose**  
Evaluate signals against rules and determine enforcement stance.

**Artifacts**
- `schema_validator.py`
- `sequence_rules.py`
- `thresholds.py`
- `response_policy.py`

**Responsibilities**
- Structural validation
- Temporal ordering checks
- Policy scoring and recommended action derivation

---

### 2.5 — `05_controllers/` (Runtime Governance)

**Purpose**  
Maintain interaction state and apply enforcement decisions.

**Artifacts**
- `state_machine.py`
- `pld_controller.py`
- `action_router.py`
- `controller_config.py`

**Responsibilities**
- Track current PLD phase
- Produce `ControllerOutcome`
- Route decisions to logging, agent control, or escalation

---

### 2.6 — `06_logging/` (Telemetry & Trace Layer)

**Purpose**  
Provide replayable, structured, exportable records.

**Artifacts**
- `structured_logger.py`
- `session_trace_buffer.py`
- `event_writer.py`
- `exporter_jsonl.py`
- optional: `exporter_open_telemetry.py`

**Responsibilities**
- Persist turns, events, decisions, and state transitions
- Support streaming, debug, evaluation, and silent modes

---

### 2.7 — `07_failover/` (Safety Nets)

**Purpose**  
Stabilize runtime during detected breakdown states.

**Artifacts**
- `runtime_failover.py`
- `strategy_registry.py`
- `backoff_policies.py`
- `reconciliation.py`

**Responsibilities**
- Decide reset, backoff, escalation, or human override
- Produce `FailoverDecision` + recovery plan

---

## 3. High-Level Data Flow

```
raw input → ingestion → detection → enforcement → controller
            │                                     │
            └────────────── logging ──────────────┘
                          │
                       failover (if triggered)
```

---

## 4. Extension & Governance Rules

| Rule | Meaning |
|------|--------|
| Numeric module prefixes never change | Ensures stability across versions |
| New core modules must be ≥ `08_` | Runtime ordering semantics preserved |
| All runtime effects must be explicit | No silent resets or drift acknowledgments |
| All events must validate against schemas | No schema drift allowed |

---

## 5. Versioning & License

- Versioning: **Semantic + Runtime Migration Notes**
- License: **CC BY-NC 4.0**
- Maintainer: **Kiyoshi Sasano**

---

> **The runtime exists to ensure alignment persists — not just at model level, but across the lifespan of a conversation.**
