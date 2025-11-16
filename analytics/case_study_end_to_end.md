---
title: "End-to-End Case Study: PLD Runtime in a SaaS Support Agent"
version: "1.0"
status: "Canonical Case Study"
maintainer: "Kiyoshi Sasano"
updated: "2025-01-18"
visibility: "Public"
scope: "Research → Implementation → Operation"
---

# End-to-End Case Study  
### *Stabilizing a SaaS Support Agent Using PLD Runtime Loop*

---

## 1 — Purpose of This Case Study

This document demonstrates how Phase Loop Dynamics (PLD) improves **runtime behavioral stability** in a real-world multi-turn agent scenario.

PLD here is evaluated across three lenses:

| Perspective | Question |
|------------|----------|
| **Research** | Does the runtime loop reduce drift frequency and escalation? |
| **Engineering** | Can PLD be implemented without rewriting the architecture? |
| **Operations** | Does PLD generate observable signals that support monitoring and regression control? |

Success criteria:

> **With PLD, the system should not “avoid failure” — it should *recover* in a controlled and observable manner.**

---

## 2 — Scenario: SaaS Support Chat Assistant

A customer is interacting with a support bot to:

- search documentation (RAG),
- create support tickets (tool call),
- continue the session over multiple turns (memory).

The agent must maintain alignment while:

| Component | Drift Risk | PLD Label |
|-----------|------------|-----------|
| Retrieval | Irrelevant or empty results | `D5_information` |
| Tools | Invalid parameter or missing schema field | `D4_tool` |
| Memory | Incorrect plan, pricing tier, or status recall | `D2_context` |

This scenario surfaces the *three core failure modes PLD was designed to govern*.

---

## 3 — Baseline Behavior (No PLD)

### 3.1 Architecture
```
User → LLM →
↳ Mock RAG (KB lookup)
↳ Mock Tool (Create Ticket)
↳ Ephemeral Memory
→ Response
```

### 3.2 Example Interaction

| Turn | Agent Behavior | Problem |
|------|---------------|---------|
| 1 | “There is no record of that feature.” | RAG irrelevant result → hallucination amplification |
| 2 | Attempts creating support ticket without required field `"priority"` | Invalid tool request |
| 3 | Suggests enterprise-only features to a free-tier user | Memory misalignment |

### 3.3 Initial Metrics Snapshot

| Metric | Value | Interpretation |
|--------|------|----------------|
| **PRDR: 0.78** | ~78% of recovery attempts fail or escalate | System cannot self-correct |
| **VRL: 0.04** | Almost no visible repair | Repairs are silent or nonexistent |
| **REI: 0.00** | No successful reentry confirmations | Flow collapses instead of stabilizing |

Baseline takeaway:

> **The system behaves correctly only when nothing goes wrong.**

---

## 4 — Incremental PLD Adoption

PLD does not require redesign — it wraps existing behaviors.

### Phase Additions

| Step | Change | Runtime Effect |
|------|--------|----------------|
| 1 | Add `Drift → Detect` node | Signals `D*` drift classification |
| 2 | Add soft/hard repair strategies | Routed based on drift type |
| 3 | Add `Reentry → Confirmation` | Stabilizes state before continuing |
| 4 | Log `R*`, `RE*`, `OUT*` events | Enables monitoring and analytics |

### Example: Repaired interaction trace
```
D5 → R2 Soft Repair → RE1 Confirm → Continue
D4 → R3 Hard Repair → RE1 Confirm → Continue
D2 → R1 Clarify Memory → RE2 Checkpoint → Continue
```

The system now behaves **with control**, not reaction.

---

## 5 — Final Integrated Runtime

### Architecture with PLD Enabled

```mermaid
flowchart TD
    User --> Drift["Detect Drift (D*)"]
    Drift -->|detected| Repair[Soft/Hard Repair (R*)]
    Drift -->|none| Task[Task Execution]
    Repair --> Reentry[Reentry Confirmation (RE*)]
    Reentry --> Task
    Task --> Outcome[(Outcome + Telemetry OUT*)]
```
### Example Execution Log (Condensed)

```json
[
  {"event":"D5_information","turn":1},
  {"event":"R2_soft_repair","strategy":"option_expansion"},
  {"event":"RE1_alignment_check"},
  {"event":"continue"},
  {"event":"D4_tool"},
  {"event":"R3_schema_fix"},
  {"event":"RE1_alignment_check"},
  {"event":"continue"}
]
```
Now the agent not only behaves —
it explains, tracks, and regulates its behavior.

---

## 6 — Observability and Metrics Impact

After applying PLD, metrics change measurably.

| Metric | Before | After | Meaning |
|--------|--------|-------|---------|
| PRDR | **0.78 → 0.21** | Repairs now succeed vs. escalating |
| VRL | **0.04 → 0.63** | Most repairs are now visible to users |
| REI | **0.00 → 0.84** | Flow returns to aligned state reliably |

Interpretation:

> The system still fails — but no longer collapses.  
> **Failure becomes governable and recoverable.**

---

## 7 — Operational Interpretation

From an engineering lens:

- The loop creates **controlled retry pathways**
- System behavior becomes **inspectable and repeatable**
- Failures become **policy choices, not accidents**

From a product lens:

- Repair transparency builds trust
- Drift no longer compounds into abandonment
- Stability survives long-horizon interaction

From a reliability/SRE lens:

- Logs map directly to dashboards
- Regression detection becomes automated
- Drift patterns become measurable risk, not mystery

---

## 8 — Lessons Learned

| Insight | Consequence |
|---------|-------------|
| Retrieval, tooling, and memory failures are *structurally different.* | They require distinct repair strategies. |
| Repair is not a model output — it is a **runtime policy.** | UX and strategy must be designed intentionally. |
| Stability emerges not from correctness — | but from **the ability to return to alignment.** |

---

## Final Summary

This case study demonstrates that:

> **PLD increases agent stability not by preventing error,  
> but by restoring alignment after it occurs — predictably, observably, and repeatedly.**

Systems implementing PLD move from:

❌ *Unpredictable conversational collapse*  
to  
✅ *Controlled, measurable runtime alignment.*

---

Maintainer: **Kiyoshi Sasano**
