# LangGraph Integration Example — PLD Applied Framework  
*(2025 Edition | Implementation Scaffold)*

This document demonstrates how to integrate **Phase Loop Dynamics (PLD)** into a LangGraph-based LLM agent.

The goal is not domain content — but a **generalized operational blueprint** supporting:

- Drift detection  
- Soft / Hard Repair routing  
- Reentry checkpoints  
- Structured PLD event logging  
- Stability during multi-turn reasoning  

---

## 1. Architecture Overview

PLD introduces operational checkpoints into the reasoning graph.

```
User Input
   ↓
[ DRIFT DETECTION NODE ]
     ↳ drift detected → [ SOFT REPAIR ] → [ REENTRY ]
     ↳ no drift → continue
   ↓
[ TASK EXECUTION / TOOLING ]
   ↓
[ OUTCOME + TELEMETRY ]
```

Each node is modular and replaceable.

---

## 2. Requirements

```bash
pip install langchain langgraph openai
```

Optional (recommended):

```bash
pip install pydantic pandas opentelemetry-api
```

---

## 3. Shared Utilities

```python
# pld_utils.py — shared utilities for LangGraph + PLD

from enum import Enum
from typing import Optional, Dict

class DriftType(str, Enum):
    NONE = "none"
    INFORMATION = "drift_information"
    AMBIGUOUS = "drift_ambiguous"
    REPEATED = "drift_repeated"

def detect_drift(turn: str, last_turn: Optional[str] = None) -> DriftType:
    """Lightweight drift classifier (placeholder — replace with model rule stack later)."""

    if not turn:
        return DriftType.NONE

    if last_turn and turn.strip().lower() == last_turn.strip().lower():
        return DriftType.REPEATED

    if "sorry" in turn.lower() or "no results" in turn.lower():
        return DriftType.INFORMATION

    if "?" in turn and len(turn.split()) <= 2:
        return DriftType.AMBIGUOUS

    return DriftType.NONE

def build_pld_event(event_type: str, metadata: Dict):
    """Standardized PLD event log shape."""
    return {
        "event_type": event_type,
        "metadata": metadata,
    }
```

---

## 4. LangGraph Nodes

### 🧩 4.1 — Drift Detection Node

```python
from langgraph.graph import StateGraph, END
from pld_utils import detect_drift, DriftType, build_pld_event

def drift_detection_node(state):
    user_input = state["input"]
    last_output = state.get("last_output", None)

    drift = detect_drift(user_input, last_output)

    state["repair_state"] = drift
    state.setdefault("pld_events", []).append(
        build_pld_event("drift_detected", {"drift": drift})
    )

    return state
```

---

### 🧩 4.2 — Soft Repair Node

```python
SOFT_REPAIR_TEXT = {
    DriftType.AMBIGUOUS: "Just to clarify — what outcome are you aiming for?",
    DriftType.REPEATED: "It looks like we may be repeating — should we adjust constraints?",
    DriftType.INFORMATION: "It seems the previous information may not apply — here are alternative options."
}

def soft_repair_node(state):
    drift = state["repair_state"]

    state["output"] = SOFT_REPAIR_TEXT.get(
        drift, "Let’s reset the context slightly — what should we focus on?"
    )

    state["pld_events"].append(
        build_pld_event("soft_repair", {"strategy": drift})
    )

    return state
```

---

### 🧩 4.3 — Reentry Confirmation Node

```python
def reentry_node(state):
    state["pld_events"].append(
        build_pld_event("reentry_check", {"previous_state": state["repair_state"]})
    )
    state["repair_state"] = DriftType.NONE
    return state
```

---

### 🧩 4.4 — Main Task Node (replace with toolchain)

```python
def main_task_node(state):
    query = state["input"]
    response = f"Executing task with query: {query}"

    state["output"] = response

    state["pld_events"].append(
        build_pld_event("task_execution", {"query": query})
    )

    return state
```

---

## 5. Routing Logic

```python
workflow = StateGraph()

workflow.add_node("detect_drift", drift_detection_node)
workflow.add_node("soft_repair", soft_repair_node)
workflow.add_node("reentry", reentry_node)
workflow.add_node("task", main_task_node)

workflow.add_edge("detect_drift", "soft_repair", condition=lambda s: s["repair_state"] != DriftType.NONE)
workflow.add_edge("detect_drift", "task", condition=lambda s: s["repair_state"] == DriftType.NONE)

workflow.add_edge("soft_repair", "reentry")
workflow.add_edge("reentry", "task")

workflow.set_entry_point("detect_drift")
workflow.set_finish_point("task")

graph = workflow.compile()
```

---

## 6. Running the Agent

```python
state = {"input": "No hotels match that price."}
result = graph.invoke(state)

print(result["output"])
print(result["pld_events"])
```

---

## 7. Extensions & Roadmap

| Feature | Path |
|--------|------|
| Replace rule-based drift classifier | LLM-based + rule hybrid detector |
| Persist telemetry | SQLite, Mixpanel, OpenTelemetry |
| Domain tuning | Configurable repair/goal policies |
| Multi-agent orchestration | Use Reentry → Turn-Hand-off Pattern |

---

## License

**Creative Commons BY-NC 4.0**  
© 2025 — DeepZenSpace / Contributors

---

### Summary

This integration establishes:

✔ A reusable **Drift → Repair → Reentry** control loop  
✔ A modular LangGraph pipeline  
✔ PLD event telemetry for debugging, evaluation, and stability tracking  
✔ A future-proof scaffold for real tool-using agents  

---
