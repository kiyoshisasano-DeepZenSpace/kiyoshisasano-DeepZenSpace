---
title: "Canonical LangGraph Pattern — PLD Runtime Loop"
version: "1.1"
status: "Reference Scaffold"
maintainer: "Kiyoshi Sasano"
updated: "2025-01-15"
visibility: "Public"
scope: "System Pattern (Baseline)"
---

## Framework Context

⚠️ **This example uses LangGraph for demonstration purposes.**

PLD is framework-agnostic — the same runtime loop can be implemented in:

- Assistants API
- AutoGen / CrewAI
- Rasa
- Custom orchestration loops

LangGraph is simply **one possible implementation path**, not a requirement.


# Canonical LangGraph Example — PLD Runtime Loop  
*(Standardized Scaffold — aligned to Integration Recipes)*

This file represents the **canonical baseline pattern** for implementing  
**Phase Loop Dynamics (PLD)** using LangGraph.

It now reflects the full runtime model:

> **Drift → Repair → Reentry → Continue → Outcome**

This version replaces the earlier lightweight scaffold.

---

## 1. Purpose

This file exists to provide a:

- **Stable starting point**
- **Framework-consistent runtime loop**
- **Telemetry-ready execution pattern**
- **Compatible anchor for:**
  - `rag_repair_recipe.md`
  - `tool_agent_recipe.md`
  - `memory_alignment_recipe.md`
  - `reentry_orchestration_recipe.md`

This scaffold is intentionally **minimal**, yet **PLD-complete**.

---

## 2. Requirements

```bash
pip install langchain langgraph openai
```
Optional (recommended):
```bash
pip install pydantic opentelemetry-api pandas
```

---

## 3. Shared PLD Utilities (Runtime Vocabulary)
```python
from enum import Enum
from typing import Optional, Dict


class DriftCode(str, Enum):
    """Canonical PLD drift codes (Tier 1 alignment)."""
    NONE = "D0_none"
    INFORMATION = "D5_information"
    TOOL = "D4_tool"
    CONTEXT = "D2_context"


class ReentryCode(str, Enum):
    AUTO = "RE3_auto"
    FAILED = "RE2_failed"


def detect_drift(turn: str) -> DriftCode:
    """Stub rule — Integration Recipes replace this."""
    if "error" in turn.lower():
        return DriftCode.TOOL
    if "no results" in turn.lower():
        return DriftCode.INFORMATION
    if "wait what" in turn.lower():
        return DriftCode.CONTEXT
    return DriftCode.NONE


def log_event(event_type: str, pld_code: str, payload: Dict = None):
    """PLD-structured event aligned to pld_event.schema.json."""
    return {
        "event_type": event_type,
        "pld": {
            "phase": event_type.split("_")[0] if "_" in event_type else "none",
            "code": pld_code,
            "confidence": 0.95
        },
        "payload": payload or {}
    }
```

---

## 4. LangGraph Nodes (Aligned with Integration Recipes)
# 🧩 4.1 — Drift Detection Node
```python
def detect_drift_node(state):
    user_input = state["input"]
    drift_code = detect_drift(user_input)

    state["drift"] = drift_code
    state.setdefault("pld_events", []).append(
        log_event("drift_detected", drift_code, {"input": user_input})
    )

    return state
```
---

# 🧩 4.2 — Soft Repair Node (Visible Repair — default)
> Behavior matches RAG / Tool / Memory recipes, not custom phrasing.
```python
SOFT_REPAIR_MAP = {
    DriftCode.INFORMATION: "Let me adjust the search strategy based on that.",
    DriftCode.TOOL: "It looks like the tool call may have failed — retrying.",
    DriftCode.CONTEXT: "Let's re-anchor the shared context before we continue."
}

def soft_repair_node(state):
    repair_code = f"R1_soft_repair:{state['drift']}"
    state["output"] = SOFT_REPAIR_MAP.get(state["drift"], "Repairing alignment...")

    state["pld_events"].append(
        log_event("repair_triggered", repair_code, {"strategy": "soft"})
    )

    return state
```

---

# 🧩 4.3 — Reentry Check Node
```python
def reentry_node(state):
    # standard rule: assume success (visible repair) unless drift recurs
    state["pld_events"].append(
        log_event("reentry_observed", ReentryCode.AUTO, {"after": state["drift"]})
    )
    state["drift"] = DriftCode.NONE
    return state
```

---

# 🧩 4.4 — Core Task Node (Replace per domain)
```python
def task_node(state):
    query = state["input"]
    state["output"] = f"[TASK EXECUTION] → {query}"

    state["pld_events"].append(
        log_event("outcome_event", "OUT1_in_progress", {"query": query})
    )
    return state
```

---

## 5. Routing Logic — Full PLD Loop
```python
from langgraph.graph import StateGraph

workflow = StateGraph()

workflow.add_node("detect", detect_drift_node)
workflow.add_node("repair", soft_repair_node)
workflow.add_node("reentry", reentry_node)
workflow.add_node("task", task_node)

workflow.add_edge("detect", "repair", condition=lambda s: s["drift"] != DriftCode.NONE)
workflow.add_edge("detect", "task",   condition=lambda s: s["drift"] == DriftCode.NONE)

workflow.add_edge("repair", "reentry")
workflow.add_edge("reentry", "task")

workflow.set_entry_point("detect")
graph = workflow.compile()
```

---

## 6.Running the System
```python
result = graph.invoke({"input": "No results found error."})
print(result["output"])
print(result["pld_events"])
```
---

### 7. Alignment Notes

| Behavior | Source |
|----------|--------|
| Drift Signals | `docs/06_pld_concept_reference_map.md` |
| Repair Semantics | Integration Recipes (Tier 1) |
| Reentry Routing | `reentry_orchestration_recipe.md` (Tier 2) |
| Logging Format | `pld_runtime/schema/pld_event.schema.json` |

---

#### Final Principle

> This file is the default implementation pattern for **LangGraph + PLD**.  
> All other recipes extend — not replace — this scaffold.

Maintainer: **Kiyoshi Sasano**  
License: **CC-BY-4.0**




