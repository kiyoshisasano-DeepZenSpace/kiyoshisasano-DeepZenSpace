# 03 — Hard Repair  
*Operator Primitive (Applied-AI Edition)*  

> **Purpose:** Restore stability when conversational or system state has become structurally corrupted — beyond what Soft Repair can safely resolve.  
> Hard Repair is a **controlled reset**, not a failure. It protects task integrity.

---

## **1 — When Hard Repair Is Required**

Hard Repair should only be triggered if **continuing would propagate error**.

| Trigger Condition | Example |
|------------------|---------|
| **Cascaded contradictions** | multiple self-conflicting system responses |
| **Lost task frame** | assistant no longer knows the user's objective |
| **State corruption** | incorrect memory committed as factual |
| **Irreconcilable constraint conflict** | user requirements cannot be aligned |
| **Failure loop recurrence** | repeated failed tool calls leading to hallucination |

Recommended target: **<15% of repair events**.  
If higher → drift detection or Soft Repair is failing upstream.

---

## **2 — PLD Taxonomy Alignment**

Hard Repair corresponds to:

- **Repair-Reset**
- **Repair-Recontextualize**
- **Repair-Restart**
- **Repair-ContextDrop**

Hard Repair should **generally ask for confirmation**, unless the system is already nonsensical.

---

## **3 — Canonical Hard Repair Sequence**

Hard Repair follows a **four-step protocol**:

```
(1) Acknowledge failure  
(2) Reset context (scope depends on severity)  
(3) Reconfirm goal and constraints  
(4) Restart aligned execution path
```

Example:

> “Thanks — it looks like some earlier details became inconsistent.  
> I’ll reset context to avoid confusion.  
> Can you confirm the goal: booking a 4-star hotel under $150 in Cambridge?”

---

## **4 — Implementation Templates**

### **A. LangChain (Reset Operator Function)**

```python
def hard_repair(memory):
    memory.clear()  # selective or full reset depending on level
    return {
        "response": (
            "Resetting the conversation context to ensure accuracy. "
            "Please restate the key details so we continue correctly."
        ),
        "reset": True
    }
```

---

### **B. OpenAI Assistants API — Event Record**

```json
{
  "event_type": "hard_repair",
  "trigger": "state_corruption",
  "action": "context_reset",
  "requires_user_confirmation": true
}
```

---

### **C. Rasa Policy Rule**

```yaml
rules:
  - rule: Trigger Hard Repair
    condition:
      - slot_was_set:
          - drift_level: critical
    steps:
      - action: utter_hard_repair
      - action: clear_slots
```

---

## **5 — Reset Scope Levels**

| Level | Name | Scope | Use Case |
|-------|------|--------|----------|
| **Level 1 — Local Reset** | Last step only | Mild procedural drift |
| **Level 2 — Thread Reset** | Task segment history | Multi-step inconsistency |
| **Level 3 — Full Reset** | Entire memory (except identity/permissions) | Severe corruption |
| **Level 4 — Cold Start** | New session behavior | Only upon explicit user request |

Default recommendation: **Level 2** unless evidence suggests escalation.

---

## **6 — Anti-Patterns to Avoid**

| Anti-Pattern | Why It Fails |
|--------------|-------------|
| ❌ Silent reset | breaks trust |
| ❌ Reset instead of Soft Repair | overcorrection and instability |
| ❌ Reset without acknowledgment | user confusion |
| ❌ Reset loops | system architecture flaw |
| ❌ Reset due to uncertainty rather than corruption | miscalibrated drift detection |

---

## **7 — Hard Repair + Reentry Dependency**

Hard Repair is **not complete** until the system passes through **Reentry Control**:

- task goal confirmed
- constraints re-validated
- next step stated explicitly
- user confirms return to aligned flow

Example:

> “Great — thanks for confirming.  
> Starting fresh: I'm now checking available hotels under $150.”

---

## **8 — Validation Checklist**

| Check | Required? |
|-------|-----------|
| Drift severity was critical (not mild) | ✔️ |
| Soft Repair attempted first | ✔️ |
| Reset level chosen intentionally | ✔️ |
| User informed before reset | ✔️ |
| Restart plan clearly stated | ✔️ |

If any are **missing → Hard Repair is premature**.

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
