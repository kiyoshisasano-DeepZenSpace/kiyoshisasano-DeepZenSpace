<!-- License: CC BY 4.0 -->

# 01 — PLD for Agent Engineers  
*How to make multi-turn agents stable, observable, and governable.*

Version: **1.1 (Applied Runtime Edition)**  
Audience: **LLM / Agent engineers, infra & platform teams**  
Companion docs:  
- `02_pld_drift_repair_reference.md` — taxonomies & phase definitions  
- `03_pld_event_schema.md` — logging contract  
- `07_pld_operational_metrics_cookbook.md` — PRDR / VRL / FR / MRBF

---

## 0. What This Document Is (and Isn’t)

This file answers a very specific question:

> **“I already know how to build agents.  
> What does PLD actually change in how I implement and operate them?”**

It focuses on:

- How PLD **fits into an existing agent stack**
- What you **must implement** to be “PLD-aligned”
- Which signals to log and how to use them
- How to **debug and tune** using metrics (not vibes)

It is **not**:

- A general LLM primer
- A replacement for your framework (LangGraph, Assistants API, Rasa, etc.)
- A theoretical paper

Think of it as the **“agent engineer’s bridge”** between your current stack and the rest of this repo.

---

## 1. Mental Model in One Page

### 1.1 Why PLD Exists

Most multi-turn agents fail in ways that look like this:

- Works on the happy path, **falls apart** when users deviate
- **Repeats tool calls** or loops on the same plan
- “Fixes” an error, then **drifts again 3 turns later**
- Breaks when you **swap models** or change tool behavior
- Feels “fine in dev” and “fragile in prod”

These are **not** random bugs. They are symptoms of missing runtime governance.

PLD names and structures that governance as a **phase loop**:

```text
Drift → Repair → Reentry → Continue → Outcome
```

Every turn is evaluated in terms of:
1. **Drift** – did we deviate from the task / shared reality?
2. **Repair** – if yes, what corrective action did we take (soft vs hard)?
3. **Reentry** – did that correction actually stabilize behavior?
4. **Continue** – can we safely proceed with the task?
5. **Outcome** – how did this episode end?

---

### 1.2 What Changes for You as an Engineer
You still:
- build tools / RAG / memory / planners
- design prompts and routing
- integrate with your framework of choice

  PLD **adds**:
1.A shared vocabulary for failures and corrections (D1–D5, R1–R4, RE1–RE3, OUT codes)
2.A minimal logging schema (`03_pld_event_schema.md`) that all agents should emit
3.A set of patterns and recipes for how agents should react when drift is detected
4.Operational metrics (PRDR, VRL, FR, MRBF) that tell you if changes made things better or worse

You don’t adopt a new framework; you adopt a **discipline + schema + patterns**.

---

## 2. Where PLD Sits in a Typical Agent Stack
A simplified stack:
```text
User → Orchestrator / Graph → LLM + Tools + Memory → Outputs
                  ↑
           PLD Runtime Loop
(Drift detection / Repair / Reentry / Outcome logging)
```
PLD fits as a sidecar control layer inside your orchestration, not as a replacement.

### 2.1 Conceptual Placement
- Before sending output to the user
– You check for drift and decide if repair is needed.

- After a repair
– You log whether the next turns re-stabilize or drift again.

- At session end
– You log the outcome and how many repairs/failovers occurred.

This can be a dedicated node/step (LangGraph), middleware (Assistants), or decorators around your handlers.

---

## 3. The Three Things You Must Implement

To be “PLD-aligned” in code, you really need three building blocks:
1.Drift detection
2.Repair policy (soft vs hard, when to escalate)
3.Reentry confirmation + logging

### 3.1 Drift Detection
You need a function with this shape:

```python
from enum import Enum
from typing import TypedDict, Optional


class DriftCode(str, Enum):
    D0_NONE = "D0_none"
    D1_INFO = "D1_information"
    D2_CONTEXT = "D2_context"
    D3_INTENT = "D3_intent"
    D4_TOOL = "D4_tool"
    D5_LATENCY = "D5_latency"


class DriftSignal(TypedDict, total=False):
    code: DriftCode
    confidence: float
    reason: str


def detect_drift(turn_state) -> DriftSignal:
    """
    turn_state: whatever your orchestrator uses:
      - { user_message, tool_outputs, previous_summary, latency_ms, ... }
    returns: structured drift signal
    """
    # Example: simple rule + placeholder for LLM-based evaluator
    if turn_state.get("tool_error"):
        return {"code": DriftCode.D4_TOOL, "confidence": 0.95, "reason": "tool_error_flag"}

    if turn_state.get("latency_ms", 0) > 3500:
        return {"code": DriftCode.D5_LATENCY, "confidence": 0.7, "reason": "latency_spike"}

    # TODO: add LLM classifier integration later
    return {"code": DriftCode.D0_NONE, "confidence": 1.0}
```

Key principles:
- Always return a code, never “nothing”
→ use 'D0_none' when no drift is detected.

- Start with rules (tool_error, latency spikes, explicit contradictions).
Add LLM evaluators once basic logging works.

- Treat drift detection as a separate concern from the LLM reply itself.

> Details: `02_pld_drift_repair_reference.md` + `quickstart/operator_primitives/`

---

### 3.2 Repair Policy
Once drift is detected, you need logic that decides:

- Soft repair vs hard repair
- How many times you retry
- When to give up and failover

At its simplest:

```python
from enum import Enum


class RepairMode(str, Enum):
    NONE = "R0_none"
    SOFT = "R1_soft_repair"
    HARD = "R3_hard_reset"


def choose_repair(drift: DriftSignal, repair_count: int) -> RepairMode:
    code = drift["code"]

    if code == DriftCode.D0_NONE:
        return RepairMode.NONE

    # Tool errors and latency spikes can often be retried softly first
    if code in {DriftCode.D4_TOOL, DriftCode.D5_LATENCY} and repair_count < 2:
        return RepairMode.SOFT

    # If we already tried soft repair and drift persists → escalate
    if repair_count >= 2:
        return RepairMode.HARD

    # Default soft repair for other drift types
    return RepairMode.SOFT
```

The actual repair behavior (what text you send, what tools you call) lives in:

- `quickstart/patterns/01_llm/`
- `quickstart/patterns/02_ux/ `
- `quickstart/patterns/03_system/`

From a code POV, what matters is:

- You mark soft vs hard repair as structured codes (R1_soft_repair, R3_hard_reset, etc.)
- You log each repair as a PLD event (see next section)

  ---

  ### 3.3 Reentry Confirmation
Reentry answers: “Did the repair actually stabilize the interaction?”  
There are two basic strategies:  
1.Implicit / auto reentry (`RE3_auto`)
- You assume success unless another drift is observed within N turns.
- Good for early-stage systems and low-risk domains.
2.Explicit / user-confirmed reentry (`RE1_intent`, `RE2_constraints`)
- You ask the user to confirm.
- Better for high-stakes flows or complex multi-step tasks.
Minimal reentry check pattern:
```python
from enum import Enum


class ReentryCode(str, Enum):
    RE0_NONE = "RE0_none"
    RE1_INTENT = "RE1_intent_reentry"
    RE2_CONSTRAINTS = "RE2_constraints_reentry"
    RE3_AUTO = "RE3_auto"


def mark_reentry_success(kind: ReentryCode, metadata: dict | None = None) -> dict:
    return {
        "phase": "reentry",
        "code": kind.value,
        "metadata": metadata or {}
    }
```

---

### 4. Logging: The Non-Negotiable Part

PLD is telemetry-first.  
If you don’t log, you don’t really have PLD — you just have nicer prompts.  

The canonical contract lives in:

- quickstart/metrics/schemas/pld_event.schema.json

At minimum, your runtime should emit one PLD event per turn:

```python
import uuid
from datetime import datetime, timezone


def log_pld_event(
    *,
    session_id: str,
    turn_id: int | str,
    event_type: str,          # "drift_detected", "repair_triggered", ...
    pld_phase: str,           # "drift", "repair", "reentry", "continue", "outcome", "none"
    pld_code: str,            # "D4_tool", "R2_soft_repair", "RE3_auto", "OUT3_abandoned", ...
    payload: dict | None = None,
    runtime: dict | None = None,
    metrics: dict | None = None,
) -> dict:
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": session_id,
        "turn_id": turn_id,
        "event_type": event_type,
        "pld": {
            "phase": pld_phase,
            "code": pld_code,
        },
    }

    if payload is not None:
        event["payload"] = payload
    if runtime is not None:
        event["runtime"] = runtime
    if metrics is not None:
        event["metrics"] = metrics

    # send to log sink (file, DB, OpenTelemetry, etc.)
    # e.g., print(json.dumps(event, ensure_ascii=False))
    return event
```

Examples:

- Drift detected:
  ```python
  log_pld_event(
    session_id=sess_id,
    turn_id=turn_id,
    event_type="drift_detected",
    pld_phase="drift",
    pld_code="D4_tool",
    payload={"error": "timeout"},
    runtime={"latency_ms": 4200, "tool_used": "hotel_search"},
)
```

- Soft repair:

```python
log_pld_event(
    session_id=sess_id,
    turn_id=turn_id,
    event_type="repair_triggered",
    pld_phase="repair",
    pld_code="R2_soft_repair",
    payload={"strategy": "retry_with_backoff"},
)
```

- Reentry:

  ```python
  log_pld_event(
    session_id=sess_id,
    turn_id=turn_id,
    event_type="reentry_observed",
    pld_phase="reentry",
    pld_code="RE3_auto",
)
```

- Failover (for MRBF / FR):

```python
log_pld_event(
    session_id=sess_id,
    turn_id=turn_id,
    event_type="failover_triggered",
    pld_phase="failover",
    pld_code="OUT3_abandoned",
    payload={"repair_attempts": repair_count},
)
```

> The demo file `quickstart/metrics/datasets/pld_events_demo.jsonl` shows a fully wired example.

---

## 5. How Metrics Feed Back Into Engineering

Once you log, the metrics in `07_pld_operational_metrics_cookbook.md` become runtime debugging tools:

### 5.1 Quick How-To

- **PRDR (Post-Repair Drift Recurrence)**
→ If this is high, your repairs aren’t durable. Examine repair templates and when they trigger.

- **VRL (Visible Repair Load)**
→ If this is high, UX is noisy.
Reduce visible repairs or soften tone and combine corrections.

- **FR (Failover Rate) & MRBF (Mean Repairs Before Failover)**
→ If FR is high and MRBF is low: you’re giving up too early.
→ If MRBF is very high: you’re looping; introduce earlier hard repair or failover.

You do not need to remember the formulas — the dashboard + queries in `quickstart/metrics/dashboards/` encode them.
You do need to make sure your events carry the signals those queries expect (`event_type`, `pld.phase`, `pld.code`, `runtime.latency_ms`, etc.).

---

## 6. Minimal Integration Blueprint
When in doubt, start with this flow for each user turn:

```text
1. Receive user message / tool results
2. Run detect_drift(state) → DriftSignal
3. Log drift_detected event if code != D0_none
4. Choose repair_mode based on drift + repair_count
5. If repair_mode != NONE:
      - apply repair LLM prompt / UX pattern
      - log repair_triggered event
      - (optionally) ask for confirmation
      - mark reentry (RE3_auto or RE1/RE2)
      - log reentry_observed event
   Else:
      - continue normal task execution
6. At session end, log an outcome event (complete / reset / abandoned / handoff)
```

You can see this pattern concretely in:

- `quickstart/patterns/03_system/runtime_policy_patterns.md`
- `quickstart/patterns/03_system/implementation_guides/langgraph_integration.md`
- `quickstart/patterns/04_integration_recipes/*`

---

## 7. Practical Checklist for Agent Engineers

Before you consider a system “PLD-integrated”, check:

□ ✅ You have a drift detection function that returns D0_none or D1–D5 codes
□ ✅ You have soft vs hard repair logic, not just “retry until it works”
□ ✅ You have at least one reentry strategy (RE3_auto or RE1/RE2)
□ ✅ Your runtime emits events conforming to pld_event.schema.json
□ ✅ You can compute PRDR, VRL, FR, MRBF on a sample log
□ ✅ You can answer:

> “When this system misbehaves, which phase failed, and what will it do next?”

If you can’t answer that last question, PLD is not yet “installed” — it’s just in the slides.

---

## 8. Where to Go Next

- For taxonomy & codes:
→ `02_pld_drift_repair_reference.md`

- For schema details & JSON examples:
→ `03_pld_event_schema.md`

- For metrics and dashboards (PRDR / VRL / FR / MRBF):
→ `07_pld_operational_metrics_cookbook.md`
→ `quickstart/metrics/`

- For concrete runtime patterns (LLM / UX / system):
→ `quickstart/patterns/`

---

> **Engineering summary**:
> PLD does not replace your agent framework.
> It gives you the phases, codes, logs, and metrics that turn a clever prototype into a system you can debug, tune, and trust over time.
