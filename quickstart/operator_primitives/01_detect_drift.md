# 01 — Detect Drift  
*Operator Primitive

> **Purpose:** Detect when an agent has deviated from the intended task state, user constraints, or previously established context — *before repair becomes expensive.*

---

## **1 — What This Primitive Solves**

LLM-based agents rarely fail because the answer is *incorrect* —  
they fail because they silently drift away from:

- user constraints (price, location, timing, preferences)  
- system state (tool results, validated memory, workflow)  
- reasoning thread (goal, steps, or commitments)

**Drift detection is the first safeguard**, preventing:

- cascading hallucination  
- tool retry loops  
- unnecessary resets  
- user frustration and distrust  

This primitive installs **early detection hooks**, allowing the system to initiate **Soft Repair proactively**, not reactively.

---

## **2 — PLD Taxonomy Alignment**

| Drift Type | Detectable via | Typical Trigger |
|-----------|----------------|----------------|
| **Drift-Information** | mismatch between belief state & tool output | DB/API returns evidence contradicting the agent |
| **Drift-Constraint** | user’s boundaries violated | agent proposes invalid option |
| **Drift-Intent** | divergence from original user goal | response shifts topic or objective |
| **Drift-Memory** | context loss or overwritten facts | forgotten key detail |
| **Drift-Procedural** | deviation from expected workflow | skipped check or reordered step |

---

## **3 — Detection Signals & Rules**

Drift detection uses both:

- **local signals** (current turn), and  
- **global signals** (conversation memory + tool state).

| Signal Category | Example Trigger | Operational Rule |
|----------------|-----------------|-----------------|
| **Semantic Contradiction** | “No hotels available” → “Here are 3 hotels” | Compare response vs verified memory |
| **Constraint Break** | user: ≤ $100 → agent: $240 option | Validate against stored constraints |
| **Plan Interruption** | agent restarts workflow without reason | Compare next action to plan graph |
| **Intent Loss** | response ignores request | Topic shift beyond embedding threshold |
| **Latency-Driven Hallucination Risk** | delay followed by filler or invention | Mark high-latency uncertainty |

**Base rule format:**

```
IF system_output conflicts with verified memory OR tool_state  
THEN mark drift (type = detected dimension)
```

---

## **4 — Implementation Examples**

### **A. LangChain (Pseudo-Real)**

```python
def detect_drift(turn, memory, constraints, last_tool_result):
    signals = []

    if last_tool_result and "no result" in last_tool_result and "found" in turn.lower():
        signals.append("Drift-Information")

    if constraints and any(value not in turn for value in constraints.values()):
        signals.append("Drift-Constraint")

    if memory and memory.get("goal") and memory["goal"].lower() not in turn.lower():
        signals.append("Drift-Intent")

    return signals or None
```

---

### **B. Autogen (Callback-Based)**

```python
class DriftMonitor:
    def after_agent_turn(self, response, state):
        if response.contradicts(state.tool_memory):
            return {"drift": "Drift-Information"}
        if response.breaks(state.constraints):
            return {"drift": "Drift-Constraint"}
        return None
```

---

### **C. OpenAI Assistants (Tools + Memory Signals)**

```python
event = {
  "turn_id": turn_id,
  "drift": "Drift-Information" if contradiction else None,
  "confidence": score
}
```

---

## **5 — Logging Format (PLD Schema Compatible)**

```json
{
  "turn_id": 7,
  "speaker": "system",
  "detected_drift": "Drift-Information",
  "evidence": "Previous tool said 'no hotels found', response suggests availability.",
  "confidence": 0.87
}
```

---

## **6 — Expected System Response Flow**

This primitive **does not fix** drift —  
it triggers downstream operators.

| Drift Detected | Next Step (Triggered Operator) |
|---------------|--------------------------------|
| Drift-Information | → Soft Repair (validate or offer updated options) |
| Drift-Constraint | → Soft Repair (clarify or relax constraint) |
| Drift-Intent | → Reentry control |
| Severe or repeated drift | → Hard Repair escalation |

---

## **7 — Anti-Patterns (Avoid These)**

🚫 Allowing drift to accumulate  
→ leads to runaway hallucination.

🚫 Treating all drift as equal  
→ minor mismatch ↑ ≠ full reset.

🚫 Detecting drift without logging  
→ destroys observability and debugging.

---

## **8 — Quick Sanity Test**

**Input:**

> “There are no 4-star hotels available.”  
(But previous API returned: 4 matches.)

**Expected Output:**

```
[ Drift-Information Detected ]
```

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY-NC 4.0**