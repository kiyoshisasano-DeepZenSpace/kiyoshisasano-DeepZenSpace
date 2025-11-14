# 02 — Soft Repair  
*Operator Primitive (Applied-AI Edition)*  

> **Purpose:** Restore alignment after detected drift **without resetting context**.  
> Soft Repair recovers stability through clarification, constraint negotiation, or corrective restatement — while keeping the current task thread intact.

---

## **1 — Why Soft Repair Exists**

Most drift events are **recoverable**, not catastrophic.  
However, many systems respond with:

- full state reset  
- contradiction  
- or ignoring the drift  

Soft Repair provides a **low-cost recovery layer** that preserves:

- user trust  
- conversational rhythm  
- memory integrity  
- task continuity  

Soft Repair should be applied **immediately after drift detection**, not delayed.

---

## **2 — PLD Taxonomy Alignment**

| Repair Type | Typical Scenario | Notes |
|------------|------------------|-------|
| **Repair-AddInfo** | Missing detail or ambiguity | Default + safest |
| **Repair-Clarify** | Constraint mismatch or unclear request | Used when uncertainty > confidence |
| **Repair-Correct** | Agent contradicted a verified source | Must acknowledge discrepancy |
| **Repair-OfferOptions** | Constraint conflict from tools | Booking/recommender flows |
| **Repair-Reframe** | Restoring original goal when intent drifted | Prevents derailment |

Soft Repair should **not overwrite long-term memory until confirmed**.

---

## **3 — When Soft Repair Should Trigger**

Soft Repair activates when any of the following occur:

| Condition | Example Trigger |
|----------|----------------|
| ⚠️ Response contradicts tool output | “No hotels” → later “3 hotels found” |
| ⚠️ Overconfident hallucination | claims without evidence |
| ⚠️ Constraint violation | budget violated, date mismatch |
| ⚠️ Intent drift | assistant changes subject |
| ⚠️ Workflow deviation | skipped confirmation step |

---

## **4 — Canonical Soft Repair Pattern**

Soft Repair follows a **three-part structure**:

```
(1) Acknowledge  
(2) Correct or Clarify  
(3) Confirm next step
```

Example:

> “Thanks — let me correct that.  
> You’re right: there *are* available 4-star options.  
> Would you prefer the lowest price or best rating?”

---

## **5 — Implementation Examples**

### **A. LangChain Function Pattern**

```python
def soft_repair(event, memory):
    if event["drift"] == "Drift-Information":
        return f"Thanks — let me correct that. Updated results show: {memory.get('latest_results')}"
    
    if event["drift"] == "Drift-Constraint":
        return f"To confirm, your budget is {memory['constraints'].get('budget')} — is that correct?"

    if event["drift"] == "Drift-Intent":
        return "Just confirming — we're still working on the original goal, correct?"

    return "Let me clarify that briefly."
```

---

### **B. Autogen Callback Template**

```python
class SoftRepair:
    def handle(self, drift_type, context):
        return {
            "Drift-Information": "Updating based on corrected information.",
            "Drift-Intent": "Just to confirm — are we still pursuing the same objective?"
        }.get(drift_type, "Let me clarify that.")
```

---

### **C. OpenAI Assistants API (Metadata Event)**

```json
{
  "action": "soft_repair",
  "strategy": "Repair-Clarify",
  "reason": "constraint_conflict",
  "prompt": "Thanks — confirming: your max budget is still $100?"
}
```

---

## **6 — Logging Format (PLD Schema Compatible)**

```json
{
  "turn_id": 8,
  "event_type": "soft_repair",
  "repair_strategy": "Repair-Clarify",
  "drift_type": "Drift-Constraint",
  "confidence": 0.92
}
```

---

## **7 — Anti-Patterns (Avoid These)**

| Anti-Pattern | Why It Breaks the System |
|--------------|--------------------------|
| ❌ Ignoring drift | Creates cascading contradictions |
| ❌ Excess apologizing | Signals instability / uncertainty |
| ❌ Over-repairing | Feels robotic / unpredictable |
| ❌ Premature reset | Breaks workflow and memory |
| ❌ Introducing new uncertainty during repair | Turns repair into new drift |

---

## **8 — Validation Checklist**

| Check | Expected |
|-------|----------|
| Mistake acknowledged? | ✔️ |
| Correction grounded in evidence? | ✔️ |
| User path forward proposed? | ✔️ |
| Intent or constraints re-confirmed? | ✔️ |
| No new hallucination introduced? | ✔️ |

If any item fails → retry Soft Repair or escalate to Hard Repair.

---

## **9 — Quick Sanity Test**

**Input:**
> User constraint: “No seafood.”  
> Assistant recommends sushi.

**Expected Soft Repair Output:**

> “Thanks — correcting that.  
> You mentioned avoiding seafood, so I'll remove sushi from the list.  
> Would you prefer Italian or vegan options instead?”

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY-NC 4.0**