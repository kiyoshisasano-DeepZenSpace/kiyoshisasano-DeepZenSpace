# 03 — Hard Repair  
*Operator Primitive (Canonical Code Edition — 2025)*  

> **Purpose:** Restore stability when system state becomes structurally corrupted — beyond what Soft Repair (R1–R2) can safely resolve.  
> Hard Repair is a **controlled reset**, not a failure. It prevents error propagation and restores reliable execution.

---

## **1 — When Hard Repair Is Required**

Hard Repair should only occur when **continuing the current task risks compounding error**.

| Trigger Code | Condition | Example |
|--------------|-----------|---------|
| **D1_instruction (repeated)** | System repeatedly misinterprets original objective | Wrong task despite clarifications |
| **D2_context (critical)** | Memory contradiction or corrupted constraint state | User constraints overwritten |
| **D3_flow** | Agent trapped in procedural/tool loop | Retry loops, broken step order |
| **D5_information (persistent)** | Facts remain incorrect despite correction | Conflicting factual state |

Operational Target: **Hard Repair < 12–15% of total repair events**  
If higher → Soft Repair detection or drift classification requires review.

---

## **2 — PLD Taxonomy Alignment (Updated)**

Hard Repair corresponds to a **single canonical code**:

| Allowed Hard Repair Code | Meaning | Notes |
|--------------------------|---------|-------|
| **R5_hard_reset** | Reset corrupted state and re-establish shared reality | 🚨 replaces all legacy categories (Repair-Reset, Repair-Recontextualize, Repair-Restart, Repair-ContextDrop) |

> ⛔ Legacy labels are deprecated.  
> Hard Repair must use the single canonical code: **R5_hard_reset**.

---

## **3 — Canonical Hard Repair Sequence**

Hard Repair follows a **four-step protocol**:

```
(1) Acknowledge corruption
(2) Execute reset (local, thread, or full)
(3) Reconfirm goal + constraints
(4) Resume aligned workflow
```


Example user-facing output:

> “Thanks — earlier responses became inconsistent.  
> I’ll reset context to avoid confusion.  
> Can you confirm: we're booking a 4-star hotel under $150 in Cambridge?”

---

## **4 — Implementation Templates (Updated)**

### **A. LangChain — Reset Operator (Schema-Compatible)**

```python
def hard_repair(memory):
    memory.clear()  # level depends on severity

    return {
        "pld_signal": {
            "event_type": "repair_triggered",
            "pld": {
                "phase": "repair",
                "code": "R5_hard_reset",
                "confidence": 1.0
            }
        },
        "response": (
            "Resetting context to ensure correctness. "
            "Please restate any key details so we continue aligned."
        )
    }
```

---

### B. OpenAI Assistants API — Canonical Log Event
```json
{
  "event_type": "repair_triggered",
  "pld": {
    "phase": "repair",
    "code": "R5_hard_reset",
    "confidence": 1.0
  },
  "payload": {
    "trigger": "state_corruption",
    "previous_signals": ["D2_context", "D3_flow"]
  },
  "timestamp": "2025-01-14T12:22:55Z"
}
```

---

### C. Rasa Policy Rule (Updated Naming)
```yaml
rules:
  - rule: Trigger Hard Repair
    condition:
      - slot_was_set:
          - pld_drift_code: critical
    steps:
      - action: utter_hard_repair
      - action: clear_slots  # reset memory selectively
```

---

## 5 — Reset Levels (Revised)

| Level                                       | Name                                                     | Scope                                               | Typical Drift Source |
| ------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------- | -------------------- |
| **L1 — Local Reset**                        | Most recent step only                                    | Minor correction of current turn workflow           | D3_flow             |
| **L2 — Thread Reset (recommended default)** | Reset task memory but retain user identity & constraints | Misalignment in intent or context across turns      | D1_instruction / D2_context |
| **L3 — Full Context Reset**                 | All conversation memory cleared                          | Persistent factual contradiction or corrupted state | D5_information      |
| **L4 — Cold Start**                         | New session identity                                     | User explicitly requests or system forced recovery  | N/A (explicit user trigger) |


---

## 6 — Anti-Patterns

| Anti-Pattern                                  | Why It Fails                    |
| --------------------------------------------- | ------------------------------- |
| ❌ Silent resets                               | breaks user trust               |
| ❌ Using R5 when R1/R2 was sufficient          | instability + overcorrection    |
| ❌ Hard repair loops                           | indicates architectural fault   |
| ❌ Resetting due to uncertainty—not corruption | incorrect threshold calibration |

---

## 7 — Dependency: Required Reentry Phase

Hard Repair is not complete until the agent performs Reentry Control:
- restates confirmed goal
- confirms constraints
- declares next action

Example:
> “Great — thanks for confirming.
> Starting aligned workflow now.”

---

## 8 — Validation Checklist

| Condition                                      | Must Be True |
| ---------------------------------------------- | ------------ |
| Soft Repair attempted unless severity=critical | ✔            |
| Drift confidence ≥ threshold                   | ✔            |
| Reset scope intentional                        | ✔            |
| Schema-level event logged                      | ✔            |
| Reentry executed before resume                 | ✔            |

If any are missing → Hard Repair was premature.

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
