---
title: "PLD Event Schema — Runtime Event Specification"
version: "v1.1 (2025 Edition)"
status: stable
target: implementation + evaluation + observability
---

# PLD Event Schema  
*A unified logging format for detecting, repairing, and validating alignment across turns in multi-turn LLM agents.*

---

## 1. Purpose

The PLD Event Schema defines the **runtime logging format** used to capture behavioral signals across the interaction loop:

> **Drift → Repair → Reentry → Continue → Outcome**

This schema serves three goals:

| Goal | Used By | Purpose |
|------|---------|---------|
| **Runtime control** | Orchestrators, state machines | Trigger repairs, failover, or continuation decisions |
| **Evaluation & Metrics** | Analytics pipelines | Compute PRDR, VRL, MRBF, REI, Failover rate |
| **Trace Transparency** | Researchers, UX teams | Understand why the agent changed state and how it recovered |

The schema is implementation-agnostic and compatible with:

- LangGraph / ReAct / Tool-based agents  
- OpenAI Assistants API events  
- Rasa / AutoGen / Swarm  
- Custom orchestrators and multi-model controllers  
- OpenTelemetry, PostHog, Elastic, Mixpanel

---

## 2. Core Structure

Each runtime turn emits **at least one event**.

A valid PLD event contains:

```jsonc
{
  "event_id": "uuid",
  "session_id": "MWZ-001",
  "turn_id": 4,
  "timestamp": "2025-01-17T14:22:11.130Z",

  "speaker": "system", // "user" | "assistant" | "tool" | "system"

  "event_type": "drift_detected", 
  "pld": {
    "phase": "drift",
    "code": "D4_tool" // canonical drift / repair / reentry codes
  },

  "content": {
    "input": "search hotels in london",
    "output": null,
    "tool": "searchHotels",
    "error": "missing_required_field: check_in_date"
  },

  "metrics": {
    "latency_ms": 3120,
    "confidence": 0.41
  },

  "meta": {
    "model": "gpt-5.1",
    "env": "dev",
    "trace_id": "trace-ab12"
  }
}
```

---

## 3. Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | string (UUID) | Unique event identifier |
| `session_id` | string | Conversation or agent session |
| `turn_id` | integer | Sequential identifier of the turn |
| `timestamp` | ISO-8601 | Recorded at event creation |
| `event_type` | enum | Defines the event category (see below) |
| `pld.phase` | enum | One of: `drift`, `repair`, `reentry`, `continue`, `outcome`, `neutral` |
| `pld.code` | string | Canonical event code (e.g., `D5_information`, `R2_soft_repair`) |

> `pld.code` is the semantic anchor — all evaluation, repair policy, and analytics operate over this field.

---

## 4. Event Type Specification

Event types categorize events at the system-level.  
They map to PLD phases as shown:

| event_type | phase | description |
|-----------|-------|-------------|
| `user_turn` | neutral | Raw user input |
| `assistant_response` | neutral | Standard response (no detected drift) |
| `tool_call` | continue | Valid tool operation |
| `drift_detected` | drift | Divergence or failure state |
| `repair_attempted` | repair | System applies correction (soft or hard) |
| `reentry_checkpoint` | reentry | Alignment confirmation (summary/check-back) |
| `continue_after_repair` | continue | Phase recovery success |
| `failover_triggered` | outcome | Controlled fallback path activated |
| `session_ended` | outcome | Conversation or task complete |

---

## 5. PLD Code System

PLD codes provide canonical classification across implementations.

### Drift Codes (`D*`)

| Code | Meaning |
|------|---------|
| `D1_contradiction` | conflicting facts |
| `D2_memory_loss` | lost context / missing constraints |
| `D3_instruction_divergence` | task or persona drift |
| `D4_tool` | invalid or repeated tool call |
| `D5_information` | hallucination, unsupported statement |
| `D6_context_mismatch` | retrieval mismatch or irrelevant reasoning |

### Repair Codes (`R*`)

| Code | Meaning |
|------|---------|
| `R1_soft_repair` | lightweight clarification / redirect |
| `R2_hard_repair` | reset constraints or reframing |
| `R3_partial_reset` | preserves state selectively |
| `R4_full_reset` | restart with acknowledgment |

### Reentry Codes (`X*`)

| Code | Meaning |
|------|---------|
| `X1_checkpoint_summary` | summarize context before continuing |
| `X2_confirmation_request` | ask user to confirm state |
| `X3_continuity_verified` | successful validation — resume |

### Outcome Codes (`O*`)

| Code | Meaning |
|------|---------|
| `O1_success` | task completed |
| `O2_partial` | incomplete but acceptable |
| `O3_failure` | unrecoverable failure |
| `O4_abandoned` | user terminated |

---

## 6. Example Log Sequence

A typical 5-turn alignment event:

```jsonl
{ "event_type": "drift_detected", "pld": { "phase": "drift", "code": "D4_tool" } }
{ "event_type": "repair_attempted", "pld": { "phase": "repair", "code": "R2_hard_repair" } }
{ "event_type": "reentry_checkpoint", "pld": { "phase": "reentry", "code": "X1_checkpoint_summary" } }
{ "event_type": "continue_after_repair", "pld": { "phase": "continue", "code": "X3_continuity_verified" } }
{ "event_type": "assistant_response", "pld": { "phase": "continue", "code": null } }
```

---

## 7. Validation and Versioning

- Schema source: `quickstart/metrics/schemas/pld_event.schema.json`
- Minor revisions use: `v1.1.x`  
- Breaking changes → `v2.0`

All downstream datasets MUST declare schema version:

```json
{ "schema_version": "pld.v1.1" }
```

---

## 8. Summary

> The PLD Event Schema enables **runtime governance, observability, and measurable alignment**.

It is the backbone connecting:

- runtime controllers  
- metrics and dashboards  
- evaluation datasets  
- agent UX tuning  
- failover and autonomy governance  

When the schema is implemented, drift becomes:

> **detectable → correctable → confirmable → measurable.**

---

Maintainer: **Kiyoshi Sasano**  
License: **CC-BY-4.0**  
Schema status: **stable / production-ready**
