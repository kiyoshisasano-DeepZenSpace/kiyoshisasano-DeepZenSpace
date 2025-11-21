# PLD Runtime Event Envelope — Operational Notes (Working Draft — v2.0) (v2.0 — Operational Edition)

This document supplements the schema file located at:

* `pld_runtime/01_schemas/runtime_event_envelope.schema.json`
* Referenced PLD schema: `docs/schemas/pld_event.schema.json`

This document is intended as the **operational companion to the schema**, providing:

* Interpretation guidance
* Required implementation behaviors
* Deployment considerations
* Validation and storage strategies
* Correct usage patterns and anti-patterns

This is the canonical reference for engineers implementing runtime ingestion, logging, validation, observability, analytics pipelines, or schema governance around the PLD Runtime Envelope.

---

## 1. Purpose of the Envelope

The Envelope represents the **transport and observability layer** for PLD runtime activity.
It exists to:

* Carry exactly **one PLD event** (the semantic unit)
* Add runtime context required for routing, indexing, observability, and operational debugging
* Provide metadata used by distributed systems (platform, trace, environment, execution mode)

> The Envelope **does not redefine or override the meaning of the PLD event**.
> PLD semantics (phase, code, transition logic, lifecycle meaning) are defined **only** in `pld_event.schema.json`.

---

## 2. Required Validation Responsibilities

The Envelope schema enforces **structural correctness only**.
Runtime validators **must enforce additional rules**.

### 2.1 Mandatory Runtime Rules

| Runtime Rule                                                              | Enforcement                    | Status   |
| ------------------------------------------------------------------------- | ------------------------------ | -------- |
| `session.session_id == event.session_id`                                  | MUST validate during ingestion | Required |
| Nested `event` MUST validate against PLD schema (`pld_event.schema.json`) | MUST enforce                   | Required |
| Unknown fields must **not pollute canonical schema**                      | MUST isolate into metadata     | Required |

### 2.2 About `x-validation`

The schema may include `x-validation`, but JSON Schema engines do **not execute these rules**.

They function as **"runtime enforcement contracts"**, and **MUST be implemented in code**.

Example enforcement points:

* ingestion middleware
* schema validator service
* message bus interceptors
* CI validation test harness

**Wrong assumption:**

> "Since it's declared in the schema, validation will automatically occur."

Correct behavior:

> "Schema expresses the rule. The runtime enforces it."

---

## 3. Timestamp Semantics

Two timestamps exist intentionally and represent different concepts.

| Field                | Meaning                                 | Constraints                                             |
| -------------------- | --------------------------------------- | ------------------------------------------------------- |
| `envelope.timestamp` | Time the envelope was generated/emitted | Operational timestamp — may differ from event timestamp |
| `event.timestamp`    | Time the semantic PLD event occurred    | Used for analytics, lifecycle evaluation, sequencing    |

Runtime systems MUST NOT assume these values are equal.

---

## 4. Ordering Rules — Critical Clarification

PLD systems operate with **two optional ordering indicators**:

| Field                 | Role                                         | Allowed Use                                                                |
| --------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| `event.turn_sequence` | **Authoritative ordering of runtime events** | ✔ MUST be used for lifecycle analysis, reconstruction, sequence validation |
| `trace.turn_index`    | Debugging convenience index                  | ❌ MUST NOT be used for ordering, inference, or PLD lifecycle computation   |

```
🔴 Wrong: using trace.turn_index for state evaluation
🟢 Correct: use event.turn_sequence
```

This rule prevents misinterpretation during retries, backfills, partial replays, or distributed tracing edge cases.

---

## 5. `$ref` Resolution Strategy — Deployment Guidance

Envelope schemas reference the PLD event schema. Implementations must support **two resolution modes**:

| Mode                     | Typical Environment                                       | Behavior                                   |
| ------------------------ | --------------------------------------------------------- | ------------------------------------------ |
| Local Resolution Mode    | Development / monorepo                                    | Use existing relative `$ref`               |
| Registry Resolution Mode | CI/CD, schema registry, microservices, Docker, serverless | Resolve using `$id` or URI, not filesystem |

Example production pattern:

```
$ref: "https://schemas.pld.dev/schema/pld_event/2.0.json"
```

Runtime validators MUST configure a resolver/resolution strategy and **not assume directory layout**.

---

## 6. Handling Unknown / Extended Fields

Fields under `session`, `runtime`, and `trace` allow extension for forward compatibility.
Unknown fields MUST be treated according to this policy:

| Category                    | Action                                                          |
| --------------------------- | --------------------------------------------------------------- |
| Canonical defined fields    | Extract and store in fixed columns                              |
| Unknown or extension fields | Store in a metadata bucket (e.g., `meta_json`, `envelope_meta`) |

This avoids schema pollution (example failure: storing typos like `seession_id`).

---

## 7. Validation Strategy Models (Performance + Reliability)

Different environments require different validation strictness.
Implementations SHOULD choose one of the following models:

| Model                  | Behavior                                                             | Use Case                                          |
| ---------------------- | -------------------------------------------------------------------- | ------------------------------------------------- |
| **Strict Mode**        | Every message fully validated                                        | Regulated, financial, clinical, high risk domains |
| **Sampling Mode**      | Validate a fixed % (e.g., 1–10%)                                     | Large-scale or high-throughput systems            |
| **Fail-Open With DLQ** | Invalid messages do not block processing; they are queued for review | Reliability-first streaming or real-time systems  |

Dead Letter Queue (DLQ) MUST retain enough metadata for replay and root-cause analysis.

---

## 8. Examples

### 8.1 Valid Minimal Envelope

```json
{
  "envelope_id": "645d1c3e-4bf4-4d32-92fd-7d3a4a0f1a11",
  "timestamp": "2025-01-01T12:00:00Z",
  "version": "2.0",
  "session": { "session_id": "sess_001" },
  "runtime": { "environment": "production", "mode": "stream" },
  "event": {
    "schema_version": "2.0",
    "event_id": "c1309a4f-1805-4c50-8a14-9a14b8a0b9e9",
    "timestamp": "2025-01-01T11:59:59Z",
    "session_id": "sess_001",
    "turn_sequence": 1,
    "event_type": "continue_allowed",
    "source": "runtime",
    "pld": { "phase": "continue", "code": "C0_normal" }
  }
}
```

### 8.2 Invalid (Session ID mismatch)

Rejected at ingestion.

### 8.3 Invalid (Semantic mismatch: phase vs event_type)

Fails PLD semantic validation.

---

## 9. CI/CD Enforcement Requirements

CI/CD pipelines SHOULD enforce:

* Schema validation
* Example compliance tests (valid must pass / invalid must fail)
* Schema-breaking change detection
* Confirmation prompts for required version bumps

---

## 10. Glossary (Operational Definitions)

| Term                | Definition                                                   |
| ------------------- | ------------------------------------------------------------ |
| Envelope            | Transport/observability wrapper carrying one PLD event       |
| PLD Event           | Semantically meaningful lifecycle event governed by PLD spec |
| Transport Timestamp | Envelope creation time                                       |
| Event Timestamp     | Time the semantic event occurred                             |
| Trace Metadata      | Debugging and observability context only — not semantic      |
| Extension Fields    | Unknown or future fields preserved for forward compatibility |

---

## Feedback and Contribution

This specification is part of an exploratory research effort and may evolve based on real-world testing and feedback.
If you are implementing the PLD Runtime Envelope or adapting it for production, your feedback is especially valuable.

Feedback is welcome via:

* **GitHub Issues**
* **GitHub Discussions**

Future revisions will incorporate lessons learned from early adopters.

---

## Summary

* The Envelope defines transportation and runtime context — not the semantics of the PLD event.
* The PLD event provides the lifecycle meaning and MUST be interpreted using the PLD event schema.
* Validation behavior depends on deployment requirements and may use strict, sampling, or fail-open validation.
* Forward compatibility and schema evolution are expected and supported.

> Goal: Incrementally move toward interoperability while remaining flexible during experimentation.

---

**End of Working Draft — v2.0**
