---
title: "State Transition Examples — PLD LLM Patterns"
version: 2025.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "patterns/llm"
tags:
  - PLD
  - drift repair cycle
  - applied AI
  - state machine
  - runtime alignment
---

# State Transition Examples  
_Concrete patterns demonstrating drift → repair → reentry stabilization_

This reference provides **canonical examples** of how an LLM should behave across the core PLD loop:

```
Normal → Drift → Detection → Repair (Soft/Hard) → Reentry → Continue → Complete
```

These examples are aligned with:

- `pld_event.schema.json`  
- `tool_response_rules.md`  
- `drift_response_patterns.md`  

Each scenario includes:

- 🧩 **State Summary**  
- 🧠 **Expected Model Behavior**  
- 💬 **Example Turn Transcript**  
- 📈 **Logged Event Snapshot**  

---

## 📍 Example 1 — Information Drift → Soft Repair → Reentry

### 🧩 Transition Map

```
NORMAL → DRIFT_DETECTED → SOFT_REPAIR → REENTRY_OBSERVED → CONTINUE
```

### 🧠 Behavior Intent

- Detect misunderstanding early  
- Ask for clarification **once**
- Resume task once intent is confirmed  

### 💬 Transcript

```
User: "Book a flight to Paris next Thursday."
Assistant: "Paris has many museums. Would you like a recommendation?"
```

➡ drift detected (topic deviation)

**Soft Repair Response:**

```
To make sure I understand correctly:

✈ Do you want me to book a flight,
or were you asking about travel tips?

Please choose:

1) Book a flight
2) Just information
```

**Reentry after user confirms:**

```
Got it — booking a flight.

Next question: morning or afternoon departure?
```

### 📈 Log Snapshot (compressed)

```json
{
  "event_type": "drift_detected",
  "pld": { "code": "D5_information", "phase": "drift" }
}
{
  "event_type": "repair_triggered",
  "pld": { "code": "R1_clarify", "phase": "repair" }
}
{
  "event_type": "reentry_observed",
  "pld": { "code": "RE1_intent", "phase": "reentry" }
}
```

---

## 🔧 Example 2 — Tool Failure → Retry → Visible Repair → Failover Avoided

### 🧩 Transition Map

```
NORMAL → TOOL_ERROR → RETRY → VISIBLE_REPAIR → REENTRY → CONTINUE
```

### 💬 Transcript

```
Assistant: "Searching hotel availability…"
→ TOOL_REQUEST(hotels.search)

Tool: ❌ timeout
```

**Retry (silent):**

```
→ TOOL_RETRY
```

Tool fails again.

**Visible Repair Response:**

```
The booking system didn't return results yet.
Before I retry — want to narrow it down?

1) Budget-friendly options  
2) 4-star and above  
3) Flexible dates  
```

→ User selects option.

**Reentry:**

```
Thanks — retrying with updated filters.
```

---

## 🚨 Example 3 — Escalating Loop → Hard Repair → Failover

### 🧩 Transition Map

```
NORMAL → DRIFT_LOOPS → MULTIPLE_SOFT_REPAIRS → HARD_REPAIR → FAILOVER_TRIGGERED
```

### Behavior Rule:

> If ≥3 repair attempts fail to stabilize alignment AND user intent remains ambiguous → **failover**.

### 💬 Transcript

```
User: "Help me set up a tax report."
Assistant: "What region?"
User: "US."
Assistant: "Which year?"
User: "Current."
Assistant: "Okay— generating document..."
→ Tool returns error: invalid schema
Assistant retry… fails…
Assistant: "Please confirm: personal or business tax?"
User: "Same as I said."
```

➡ drift persists → escalate

**Hard Repair Response:**

```
It looks like we’re stuck.

I’ll restart with a clearer structure.
```

➡ If still unstable:

```
I cannot complete this flow confidently — handing off for review.
```

---

## 🎯 Example 4 — Latency-Induced Drift → Pacing → Recovery

### 🧩 Transition Map

```
NORMAL → LATENCY_SPIKE → PACING_REPAIR → CONTINUE
```

### 💬 Transcript

```
User: "Summarize this document."
(5 seconds silence)
Assistant pacing:
"Still working — almost done."
```

→ Finish normally.

No clarification or escalation needed.

---

## 🎓 Example 5 — Successful Workflow Completion

### 🧩 Transition Map

```
CONTINUE → COMPLETE
```

Example:

```
Your reservation is confirmed 🎉
Would you like a receipt emailed?
```

→ Log event_type: `outcome`, `pld.phase: complete`

---

## Final Reference Checklist

```
☑ Every transition has a detectable reason
☑ Repair type matches severity (soft → hard → failover)
☑ Reentry always includes explicit stabilization phrase
☑ Normal continuation never hides repair history
☑ Logs emitted at every transition boundary
```

---

### Maintainer  
**Kiyoshi Sasano — Applied Runtime Interaction Design**

---

> “A stable agent isn’t one that avoids drift —  
> it’s one that **detects, repairs, and continues smoothly.**”
