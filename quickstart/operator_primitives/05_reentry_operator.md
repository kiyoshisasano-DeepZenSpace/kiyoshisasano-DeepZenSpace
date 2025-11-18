# 05 — Reentry Operator  
*Operator Primitive (Applied-AI Edition v1.1 — Canonical Code Compliant)*  

> **Purpose:** Restore stable execution after drift and repair by confirming alignment, shared understanding, and next action.  
> Reentry is the checkpoint between **repair → resumed flow**, ensuring confidence and continuity.

---

## 1 — Why Reentry Exists

Repair resolves the issue — but **does not confirm shared alignment**.

Without Reentry:

- the user may not know if the system is corrected  
- assumptions may diverge  
- drift recurrence risk increases  
- task confidence remains unstable  

Reentry ensures:

✔ repair acknowledged  
✔ memory and intent aligned  
✔ next step confirmed  
✔ interaction rhythm restored  

---

## 2 — When Reentry Is Required

| Event Type | Required? | Reason |
|------------|-----------|--------|
| Soft Repair (**R1_soft_repair / R2**) | **Yes (minimal)** | Light alignment check |
| Hard Repair (**R5_hard_reset**) | **Mandatory** | Reset requires explicit anchor |
| Latency disruption + repair | **Yes** | Timing breaks confidence |
| Silent correction or inconsistency fix | **Yes** | Prevent hidden divergence |
| No repair detected | No | Continue normal flow |

---

## 3 — Reentry Forms

| Form | Description | Use Case |
|------|-------------|----------|
| **RE1_minimal_check** | Lightweight verification | After minor drift or R1 clarification |
| **RE2_state_refresh** | Brief structured summary | After confusion or multiple drift events |
| **RE3_auto** | Automatic system-led reentry | When correction required no user input |
| **RE4_memory_restore** | Reconfirm recovered memory | Memory or context rebuild after reset |
| **RE5_commit_gate** | User must choose before branching | Irreversible or branching actions |

---

### Canonical Examples

#### **RE1_minimal_check**

> “Just confirming — we’re still searching for a 4-star hotel under £150, correct?”

---

#### **RE2_state_refresh**

> “Quick recap:  
> • City: Cambridge  
> • Budget: £120/night  
> • Room type: Double  
>  
> Should I continue?”

---

#### **RE3_auto** (system-driven confidence restoration)

> “Alignment confirmed — continuing.”

---

#### **RE4_memory_restore**

> “Context reset complete.  
> Confirm: hotel search, 4-star limit, budget £150?”

---

#### **RE5_commit_gate**

> “Before I continue: do you prefer free cancellation or lowest price?”

---

## 4 — Implementation Templates

### Python (Canonical Logic)

```python
def reentry(state, code):
    if code == "R5_hard_reset":
        return f"Context restored. Confirm: {state}"
    return f"To confirm — we're continuing with: {state}?"
```

---

### LangGraph Transition

```yaml
after_repair:
  on_enter: reentry_operator
  next: proceed
```

---

### OpenAI Assistants API — Schema-Aligned Logging

```json
{
  "event_type": "reentry_triggered",
  "pld": {
    "phase": "reentry",
    "code": "RE3_auto",
    "confidence": 0.97
  },
  "payload": {
    "previous_phase": "repair",
    "requires_confirmation": true
  }
}
```

---

## 5 — Anti-Patterns

| Anti-Pattern                  | Result                             |
| ----------------------------- | ---------------------------------- |
| ❌ repair without reentry      | user uncertainty continues         |
| ❌ generic confirmation        | feels robotic and unclear          |
| ❌ requesting full restatement | unnecessary effort → disengagement |
| ❌ repeating confirmation loop | perceived incompetence             |

---

Reentry must be precise, minimal, confident.

---

## 6 — Timing Requirements

Reentry must occur immediately after repair and before:
> assumptions
> tool calls
> branching
> irreversible steps

It functions as a checkpoint, not conversation padding.

---

## 7 — Validation Checklist

| Check                                | Required |
| ------------------------------------ | -------- |
| User understands repair completed    | ✔        |
| Task state explicitly confirmed      | ✔        |
| No additional uncertainty introduced | ✔        |
| Interaction pacing restored          | ✔        |
| Tone confident (not apologetic)      | ✔        |

---

## Summary

Reentry converts repair from a local fix into restored task stability.
> “Alignment confirmed — continuing.”

---

Maintainer: Kiyoshi Sasano
Edition: PLD Applied 2025 v1.1
License: CC-BY 4.0
