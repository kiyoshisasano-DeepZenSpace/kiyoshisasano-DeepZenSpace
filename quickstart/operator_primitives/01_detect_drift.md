# 01 — Detect Drift  
*Operator Primitive*

> **Purpose:** Detect when an agent deviates from the intended task state, meaning, constraints, or previously established shared reality — before repair becomes expensive.

---

## **1 — Why Drift Detection Exists**

Failure in multi-turn systems rarely occurs because the model is *wrong* —  
failure happens because the agent silently drifts away from:

- verified facts  
- user constraints  
- established memory  
- task intent or plan  

Early drift detection prevents:

- cascading hallucination  
- repeated invalid tool calls  
- unnecessary resets  
- user distrust and UX collapse  

Drift detection enables proactive **R1 (Clarify)** or **R2 (Soft Repair)** instead of late-stage damage control.

---

## **2 — PLD Canonical Taxonomy Alignment (v2.1)**

| Drift Category (Old Name) | Canonical Code | Type | Trigger Example |
|---------------------------|---------------|------|----------------|
| Drift-Intent | **D1_instruction** | Instruction Drift | System output no longer answers user goal |
| Drift-Constraint / Drift-Memory | **D2_context** | Context Drift | Constraint or remembered fact violated |
| — | D3_reasoning *(reserved)* | Reasoning Drift | (Used in planners/tool-enabled systems) |
| Drift-Tool | **D4_tool** | Tool State Drift | Output contradicts tool result |
| Drift-Information | **D5_information** | Information Drift | Evidence contradicts previous verified state |

> ❗ Previous long-form labels remain valid for analysis,  
> but **canonical codes MUST be logged in new implementations.**

---

## **3 — Detection Signals**

Drift detection draws from:

- local turn semantics  
- global conversation memory  
- tool state  
- constraint store  
- explicit checkpoints  

| Signal Type | Example | Rule |
|-------------|---------|------|
| Semantic contradiction | `"no results"` vs `"found options"` | compare vs verified tool memory |
| Constraint violation | user: `< $100` → agent: `$400` | constraint store enforcement |
| Intent loss | agent answers a different question | compare vs stored user goal |
| Tool disagreement | tool failure but agent infers success | outcome mismatch |
| State regression | reset without reason | break in plan or checkpoint |

---

## **4 — Implementation Examples (Updated with Canonical Codes)**

### A. **LangChain (pseudo-real)**

```python
def detect_drift(turn: str, memory: dict, constraints: dict, last_tool_result: str):
    drift_codes = []

    if last_tool_result and "no result" in last_tool_result and "found" in turn.lower():
        drift_codes.append("D5_information")

    if constraints and any(str(v).lower() not in turn.lower() for v in constraints.values()):
        drift_codes.append("D2_context")

    if memory.get("goal") and memory["goal"].lower() not in turn.lower():
        drift_codes.append("D1_instruction")

    return drift_codes or None
```

---

### B. Autogen (callback)
```python
class DriftMonitor:
    def after_agent_turn(self, response, state):
        if response.contradicts(state.tool_memory):
            return {"code": "D4_tool"}
        if response.breaks(state.constraints):
            return {"code": "D2_context"}
        return None
```

---

### C. OpenAI Assistants (Tools + Memory)
```python
drift_code = "D5_information" if contradiction else None

event = {
  "event_type": "drift_detected",
  "pld": {
    "phase": "drift",
    "code": drift_code
  },
  "confidence": score
}
```
---

### 5 — Logging Format (Schema Compliant)

{
  "event_type": "drift_detected",
  "turn_id": 7,
  "pld": {
    "phase": "drift",
    "code": "D5_information"
  },
  "evidence": {
    "reason": "Tool said 'no hotels found', response claimed availability.",
    "source": "tool_output"
  },
  "confidence": 0.87,
  "timestamp": "2025-01-14T12:03:22Z"
}

---

### 6 — Expected System Response

| Detected Code     | Repair Path                                  |
| ----------------- | -------------------------------------------- |
| D1_instruction    | → **R1_clarify**                             |
| D2_context        | → **R2_soft_repair**                         |
| D4_tool           | → **R2_soft_repair** + tool retry policy     |
| D5_information    | → confirm source of truth or escalate        |
| Severe / repeated | → Hard Repair (reset checkpoint or failover) |

---

### 7 — Anti-Patterns

🚫 Treating all drift as equivalent
🚫 Logging drift without recording type or canonical code
🚫 Detecting drift but skipping repair confirmation (Reentry)

---

### 8 — Quick Test
#### Input:
> "There are no 4-star hotels available."
> (But previous tool output returned: 4 matches.)

#### Expected Detection Result:
```csharp
[D5_information detected]
```

---

Maintainer: Kiyoshi Sasano
Edition: PLD Canonical Codes 2025
License: CC-BY-4.0

---
