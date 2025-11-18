# 05 — Reentry Operator  
*Operator Primitive (Applied-AI Edition)*  

> **Purpose:** Resume stable task execution after Drift + Repair by confirming alignment, shared understanding, and the intended next step — without forcing a restart.  
> Reentry marks the transition from “I repaired the issue” → “We are continuing confidently.”

---

## **1 — Why Reentry Exists**

Repair alone does **not** guarantee stability.

Without Reentry:

- Users may not know whether the system fixed the issue  
- Task intent may remain ambiguous  
- Drift risk increases sharply  

Reentry confirms:

✔ repair completed  
✔ context restored  
✔ user intent preserved  
✔ rhythm and trust re-established  

It is a **structural checkpoint**, not conversational filler.

---

## **2 — When Reentry Is Required**

| Event Type | Reentry Needed? | Notes |
|------------|-----------------|-------|
| Soft Repair | **Yes (light)** | Minimal alignment check |
| Hard Repair | **Mandatory** | Reset requires re-anchoring |
| Latency + Repair | **Yes** | Pacing disruption requires rebuild |
| Silent Correction | **Yes** | Prevents hidden state confusion |
| No Repair | No | Continue normal flow |

---

## **3 — Reentry Forms**

| Form | Purpose | When to Use |
|------|---------|------------|
| **Minimal Confirmation** | Lightweight state check | After Soft Repair |
| **State Refresh** | Summarize context | After confusion or hesitation |
| **Explicit Recommitment** | Formal restart | After Hard Repair |
| **Expectation Gate** | Confirmation before commitment | Before irreversible steps |

---

### **A. Minimal Confirmation**

> “Thanks — we’re still searching for a 4-star hotel under £150, correct?”

Used when repair was small and memory is intact.

---

### **B. State Refresh**

> “Quick recap:  
> • City: Cambridge  
> • Budget: £120/night  
> • Room type: Double  
>  
> Should I continue searching?”

Used after confusion, drift stack, or long gap.

---

### **C. Explicit Recommitment (Post-Reset)**

> “I’ve reset the conversation to avoid incorrect assumptions.  
> Can you confirm whether breakfast should be included?”

Used after Hard Repair or thread reset.

---

### **D. Expectation Gate**

> “Before I continue — do you prefer free cancellation or the lowest price?”

Used when the **next turn requires commitment or branching**.

---

## **4 — Implementation Templates**

### Python — Utility Function

```python
def reentry(previous_state, drift_type, repair_type):
    if repair_type == "hard":
        return f"I've reset context to ensure accuracy. Confirm: {previous_state}"
    return f"To confirm, we're still working on: {previous_state}?"
```

---

### LangGraph Transition Example

```yaml
state_after_repair:
  on_enter: reentry_operator
  next: continue_task
```

---

### OpenAI Assistants API Logging Schema

```json
{
  "event_type": "reentry",
  "strategy": "state_refresh",
  "drift_type": "Drift-Information",
  "repair_type": "soft"
}
```

---

## **5 — Anti-Patterns**

| Anti-Pattern | Result |
|-------------|--------|
| ❌ Repair without Reentry | User uncertainty persists |
| ❌ Reentry without context reference | Feels generic / robotic |
| ❌ Requesting full restatement | Creates unnecessary user effort |
| ❌ Multiple sequential confirmations | Signals incompetence |

Reentry should feel **precise, confident, minimal**.

---

## **6 — Timing Requirements**

Reentry must occur **immediately after Repair** and before:

- new assumptions  
- new tool calls  
- branching decisions  
- irreversible actions  

It acts as the **bridge** between Repair → resumed flow.

---

## **7 — Validation Checklist**

| Condition | Required |
|-----------|----------|
| User understands system is now aligned | ✔ |
| Task state explicitly confirmed | ✔ |
| No repeated clarification loop | ✔ |
| Rhythm returned to normal pacing | ✔ |
| Tone is confident (not apologetic) | ✔ |

---

## Summary

Reentry transforms repair from a **localized fix** into **full task recovery**.  
It signals:  

> “Context restored — continuing.”

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
