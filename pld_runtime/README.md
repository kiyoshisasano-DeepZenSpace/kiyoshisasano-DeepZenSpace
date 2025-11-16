---
license: "Apache License 2.0"
spdx: "Apache-2.0"
copyright:
  holder: "Kiyoshi Sasano"
  year: 2025
terms:
  - "Use of this software is permitted under the Apache License, Version 2.0."
  - "You may obtain a copy of the license at: http://www.apache.org/licenses/LICENSE-2.0"
  - "Distributed on an 'AS IS' basis WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND."
---



# PLD Runtime Package  
Operational Engine for Phase Loop Dynamics

⚠️ **This is a reference implementation.**

PLD can be adopted without using this package.  
Many teams embed PLD behaviors into their own orchestrators  
(e.g., LangGraph, Assistants API, AutoGen, Rasa, or custom runtime layers).

This package demonstrates **one possible approach** to governing runtime behavior with PLD.

---

Where `docs/` defines the **concepts and taxonomy**,  
the runtime answers the operational question:

> **“Given real turns, signals, and system behavior — what should happen next?”**

The runtime combines:

- raw turns and interaction traces  
- detection signals (`Drift → Repair → Reentry → Outcome`)  
- control policies and governance rules  

into:

- actionable routing decisions  
- stable multi-turn behavior  
- structured traces suitable for evaluation and monitoring

---

## 1 — Package Structure

Each top-level module reflects a PLD lifecycle stage:

```
01_schemas/      # Structural contracts + validation formats
02_ingestion/    # Normalize turns → unified runtime input
03_detection/    # Detect drift/repair/reentry patterns
04_enforcement/  # Apply rules + determine enforcement stance
05_controllers/  # Phase state machine + runtime governance
06_logging/      # Structured traces, export, replay
07_failover/     # Safety nets, escalation, controlled resets
```

Directory numbers act as **stable ordering semantics**.

---

## 2 — Module Overview

Each folder includes: purpose → responsibilities → key artifacts.

---

### 2.1 — `01_schemas/` (Contract Layer)

Defines the canonical runtime contracts.

Artifacts:

- `pld_event.schema.json`
- `runtime_event_envelope.json`

Responsibilities:

- Validate structure and compatibility
- Maintain alignment across modules and external tooling

---

### 2.2 — `02_ingestion/` (Normalization Layer)

Convert heterogeneous input into a consistent runtime structure.

Artifacts:

- `normalization.py`
- `ingestion_config.py`
- dataset adapters (MultiWOZ-compatible)

Example output:

```
NormalizedTurn(session_id, turn_id, role, text, runtime)
```

---

### 2.3 — `03_detection/` (Signal Layer)

Generate PLD signals from normalized turns.

Artifacts:

- `drift_detector.py`
- `repair_detector.py`
- `pattern_classifier.py`
- `runtime_signal_bridge.py`

> Detection produces **signals only** — no enforcement actions yet.

---

### 2.4 — `04_enforcement/` (Policy Layer)

Evaluate detected signals and determine stance.

Artifacts:

- `schema_validator.py`
- `sequence_rules.py`
- `thresholds.py`
- `response_policy.py`

Responsibilities:

- Structural/temporal validation  
- Policy scoring  
- Action recommendation

---

### 2.5 — `05_controllers/` (Runtime Governance)

Coordinate state transitions and operational control.

Artifacts:

- `state_machine.py`
- `pld_controller.py`
- `action_router.py`
- `controller_config.py`

Responsibilities:

- Maintain the currently active PLD phase  
- Produce and route `ControllerOutcome` events  
- Drive downstream behavior (logging, retry, reentry, escalation)

---

### 2.6 — `06_logging/` (Telemetry Layer)

Emit structured traces suitable for evaluation and replay.

Artifacts:

- `structured_logger.py`
- `session_trace_buffer.py`
- `event_writer.py`
- `exporter_jsonl.py`
- optional: OpenTelemetry exporter

Logging supports both streaming and retrospective analysis.

---

### 2.7 — `07_failover/` (Stability & Safety Nets)

Provide recovery when standard repair and reentry fail.

Artifacts:

- `runtime_failover.py`
- `strategy_registry.py`
- `backoff_policies.py`
- `reconciliation.py`

Produces `FailoverDecision` (reset, escalate, fallback, or defer).

---

## 3 — High-Level Data Flow

This flow reflects the reference implementation structure.  
Your version may vary depending on framework and requirements.

```
raw input → ingestion → detection → enforcement → controller
            │                                     │
            └────────────── logging ──────────────┘
                          │
                       failover (if triggered)
```

---

## 4 — Extension & Governance Guidelines

| Rule | Meaning |
|------|--------|
| Numeric prefixes should not change | Preserves ordering across versions |
| New modules should be ≥ `08_` | Keeps lifecycle semantics stable |
| Runtime effects should be explicit | Avoids silent resets or hidden correction |
| Events should validate against schemas | Maintains consistency and evaluation readiness |

---

## 5 — Versioning & License

- Versioning: **semantic with migration notes**
- License: **Apache License, Version 2.0**
- Maintainer: **Kiyoshi Sasano**

---

> The runtime ensures alignment persists across the full interaction —  
> not only within the model, but across the agent’s lifecycle.




