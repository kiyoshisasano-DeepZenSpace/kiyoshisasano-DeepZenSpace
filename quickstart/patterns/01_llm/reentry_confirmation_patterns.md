# Reentry Confirmation Patterns  
*Stability Re-Anchoring After Repair (PLD Applied v1.1)*

Reentry marks the transition from **repair mode → aligned execution mode**.  
Repair alone does **not** guarantee recovery — reentry ensures the system and user share the same task frame before continuing.

It acts as a **checkpoint**, not filler dialog.

---

## 1. Core Reentry Confirmation Template (Default)

Use after Soft Repair or R5_hard_reset unless alignment is obvious.



```
Great — correction applied.

Before continuing, here's the active task state:

Goal: <goal>
Constraints: <constraints>
Next step: <planned action>

Should I proceed? (Yes / Adjust)
```


Why it works:  
✔ restores alignment  
✔ eliminates ambiguity  
✔ prevents silent drift recurrence  

---

## 2. Lightweight Reentry (Minimal)

Use when drift was small and continuity is safe.


```
Update applied — continuing with:
<next action>

If anything needs adjusting, just tell me.
```


Tone: **confident, not apologetic.**

---

## 3. Ambiguity Collapse Pattern

Use after clarification dialogues.

```
Thanks — based on your confirmation, continuing with:

→ <selected option>

Next: <next step>
```


Helpful for **D1_instruction or D2_context** resolution.

---

## 4. Scope-Switch Reentry

Use when repair involved task reframing, not correction.

```
Understood — switching to the updated task:

New goal: <goal>
Relevant constraints: <constraints_if_any>

Choose one:

1. Restart using the new goal only
2. Continue using previous information

```


Prevents *context bleed*.

---

## 5. Tool/Source-of-Truth Correction Reentry

Use when a tool or verified fact changed the system state.

```
Correction applied — based on the latest verified data.

Updated result:
<corrected output>

Should I continue with <next action>?
```

Useful for **D5_information** repairs.

---

## 6. Latency-Aware Reentry (Voice/UI Systems)

Use when delay > pacing threshold (risk of D3_flow drift).

```
Thanks for waiting — I’m aligned again.

Continuing with:

<summary>

Ready to move forward?
```

Pairs with streaming cues.

---

## 7. Partial Recovery Pattern

Use when memory is partially restored.

```
Most of the previous issue is resolved — one item needs confirmation:

Missing detail:
<parameter>

Which option should we apply?
```


Avoid pretending recovery is complete when it isn't.

---

## 8. Autonomous Reentry (High Confidence Mode)

Use only when:

- confidence ≥ threshold,  
- no constraint modification,
- no branching required.

```
Adjustment complete — continuing.

→ <next step or action>
```


Should be rare and rule-driven.

---

## 9. Anti-Patterns

| Pattern | Result |
|--------|--------|
| ❌ Silent repair | Creates hidden state mismatch |
| ❌ Requesting full restatement | Increases cognitive load |
| ❌ Reconfirming unnecessarily | Signals uncertainty |
| ❌ Proceeding after ambiguity remains | High risk of repeated drift |

Reentry must feel **controlled, minimal, confident**.

---

## 10. Telemetry Event (Schema-Compatible)

Use this event **after reentry action is generated**.

```json
{
  "event_type": "reentry_observed",
  "pld": {
    "phase": "reentry",
    "code": "RE3_auto" 
  },
  "payload": {
    "confirmation_required": true,
    "confidence": 0.87
  }
}

```

Alternative code examples:

- `"RE4_memory_restore"` → used after context reconstruction
- `"RE2_clarify_gate"` → used when user confirmation determines next branch
  
---

### Summary

Reentry ensures:

- ✔ Alignment is explicit  
- ✔ the user and agent share the same mental model  
- ✔ execution resumes without ambiguity  
- ✔ drift → repair → reentry → continuation becomes a stable cycle

Without Reentry, repair is not recovery — it is only interruption.

---

Maintainer: **Kiyoshi Sasano**  

Edition: **PLD Applied 2025**
