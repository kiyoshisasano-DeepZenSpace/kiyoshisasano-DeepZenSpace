# 02 — Soft Repair  
*Operator Primitive (Canonical Code Edition — 2025)*  

> **Purpose:** Restore alignment after detected drift **without resetting context**.  
> Soft Repair provides a reversible correction path that preserves task continuity, memory integrity, and user trust.

---

## **1 — Why Soft Repair Exists**

Most drift events are **recoverable** — not catastrophic.  
However, naive agent behavior often responds with:

- a full state reset  
- repetition  
- contradiction  
- or ignoring the drift  

Soft Repair introduces a **low-cost recovery layer** that maintains:

- shared context  
- conversational rhythm  
- verified memory  
- workflow continuity  

It should trigger **immediately after drift detection**, especially when drift confidence ≥ operational threshold (default: `0.55–0.78` depending on domain).

---

## **2 — PLD Canonical Repair Taxonomy Alignment (v2.1)**

> ⛔ 旧名称は廃止。すべて **Canonical Codes** に統一。

| Repair Type (Old Name) | Canonical Code | Use Case |
|------------------------|---------------|----------|
| Repair-Clarify | **R1_clarify** | Meaning unclear / missing confirmation |
| Repair-AddInfo / Repair-Correct | **R2_soft_repair** | Information mismatch / correction / evidence update |
| — (reserved) | R3_tool_repair *(optional)* | Tool reconciliation / retry mediated repair |
| Repair-OfferOptions | R4_negotiation | Constraint negotiation / alternatives |
| Repair-Reframe | R5_reframe | Intent drift recovery / goal correction |

> NOTE: For most systems, **R1 and R2 are required minimum viable operators.**

---

## **3 — When Soft Repair Should Trigger**

Soft Repair activates when **drift is detected and recoverable**, such as:

| Drift Code | Trigger Example | Repair Start |
|------------|----------------|--------------|
| **D1_instruction** | Answer does not match user request | → R1_clarify |
| **D2_context** | constraint violation / mismatched memory | → R2_soft_repair |
| **D4_tool** | agent contradicts tool output | → R2_soft_repair + tool_ref_check |
| **D5_information** | incorrect fact or outdated assumption | → R2_soft_repair |
| (Repeated drift) | pattern persists beyond threshold | → escalate → Hard Repair |

---

## **4 — Canonical Soft Repair Pattern**

The format is intentionally predictable:

```
(1) Acknowledge  
(2) Correct or Clarify  
(3) Confirm next step
```


Example:

> “Thanks — let me correct that.  
> You’re right: there *are* 4 available options.  
> Should I sort them by lowest cost or highest rating?”

---

## **5 — Implementation Examples (Updated)**

### **A. LangChain Function Pattern — Updated to Canonical Codes**

```python
def soft_repair(drift_code: str, memory: dict):
    if drift_code == "D5_information":
        return f"Thanks — updating based on verified information: {memory.get('latest_results')}"

    if drift_code == "D2_context":
        return f"Just confirming: your budget is {memory['constraints'].get('budget')} — still correct?"

    if drift_code == "D1_instruction":
        return "Quick check — are we continuing with the original goal?"

    return "Let me clarify briefly."
```

### B. Autogen Callback (Canonical Revision)
```python
class SoftRepair:
    def handle(self, drift_code, context):
        responses = {
            "D5_information": "Updating based on verified facts.",
            "D1_instruction": "Quick alignment check — continuing the same task?",
            "D2_context": "Adjusting based on stored constraints."
        }
        return responses.get(drift_code, "Let me clarify that.")
```

---

### C. OpenAI Assistants API Event (Schema-Compliant)
```python
{
  "event_type": "repair",
  "pld": {
    "phase": "repair",
    "code": "R1_clarify"
  },
  "applied_to": {
    "drift_code": "D2_context"
  },
  "prompt": "Confirming: your maximum budget was $100 — correct?",
  "timestamp": "2025-01-14T12:05:44Z"
}
```

---

## 6 — Logging Format (PLD Schema Compatible)
```python
{
  "event_type": "repair",
  "turn_id": 8,
  "pld": {
    "phase": "repair",
    "code": "R2_soft_repair"
  },
  "applied_to": {
    "drift_code": "D5_information"
  },
  "confidence": 0.92,
  "timestamp": "2025-01-14T12:05:44Z"
}
```

---

## 7 — Anti-Patterns

| Anti-Pattern                      | Effect                             |
| --------------------------------- | ---------------------------------- |
| ❌ Ignoring drift                  | leads to compounding contradiction |
| ❌ Over-apologizing                | perceived instability              |
| ❌ Repeating repair multiple times | creates UX fatigue                 |
| ❌ Resetting too early             | destroys workflow trust            |
| ❌ Adding new unverified claims    | introduces secondary drift         |

---

## 8 — Validation Checklist

| Requirement                                | Must be true |
| ------------------------------------------ | ------------ |
| acknowledgment present                     | ✔️           |
| correction evidence-grounded               | ✔️           |
| user direction confirmed                   | ✔️           |
| no new uncertainty introduced              | ✔️           |
| memory updates deferred until confirmation | ✔️           |

---

## 9 — Quick Test

### Input:
> User constraint: “No seafood.”
> Assistant recommends sushi.

### Expected Canonical Output:
```bash
[R2_soft_repair applied → drift source: D2_context]
```

> “Thanks — correcting that.
> You mentioned avoiding seafood, so I’ll remove sushi from the list.
> Should I filter for Italian or vegan options instead?”


Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
