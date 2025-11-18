# 04 — Latency Operator  
*Operator Primitive (Applied-AI Edition v1.1 — Canonical Code Compliant)*  

> **Purpose:** Prevent drift caused by timing mismatch, slow inference, or long-running tool execution.  
> Latency management is a **pre-emptive stabilization mechanism**, not a repair action.

---

## 1 — Why Latency Matters

Human interaction relies on timing expectations.  
When an agent responds too slowly without signaling intent, users assume:

- confusion  
- instability  
- disengagement  
- task failure  

Unmanaged latency increases risk of drift, especially during tool calls, indexing, or multi-step reasoning.

---

## 2 — Drift Risk Model (Updated)

Latency does **not define its own drift type**.  
Instead, it increases the likelihood of existing canonical drift categories:

| Latency Effect | Risk Outcome | Canonical Code |
|---------------|-------------|----------------|
| Hesitation gap | Loss of rhythm / degraded engagement | **D3_flow** |
| Silent processing | User expectation diverges from system state | **D1_instruction** |
| Delayed tool result | User believes previous context is invalid | **D5_information** |
| Message batching / stacking | Perceived workflow discontinuity | **D3_flow** |

> **Rule:** Latency Operators run *before* drift classification to reduce avoidable repair events.

---

## 3 — Human Timing Thresholds

| Delay Window | User Interpretation | System Action |
|-------------|--------------------|--------------|
| **0–700ms** | Feels instant | Normal reply |
| **0.7–2.5s** | Slight hesitation | Optional micro-acknowledge |
| **2.5–6s** | Uncertainty forming | **Latency Hold required** |
| **>6s** | Perceived breakdown | **Expectation Reset** |

---

## 4 — Operator Types

| Operator | Definition | Usage |
|---------|------------|-------|
| **Latency Hold (default)** | Short acknowledgment | Predicted delay >2.5s |
| **Progressive Update** | Multi-step structured status | Long-running tool or inference |
| **Expectation Reset** | Clarifies duration and control | Slow reasoning / large datasets |

---

### Canonical Examples

#### A. Latency Hold

> “One moment — processing that…”

#### B. Progressive Update

> “Still working — now filtering results…”

#### C. Expectation Reset

> “This may take ~10 seconds. I’ll update you as results complete.”

---

## 5 — Implementation Examples

### Python (Async Pattern)

```python
async def run_with_latency_operator(task, notify_at=2.5):
    result = await task.with_timeout(notify_at)

    if not result.ready:
        yield "Working on that — one moment..."
        result = await task.wait()

    return result.output
```

---

### Rasa Rule

```yaml
rules:
  - rule: Latency Hold
    condition:
      - slot_was_set: { predicted_delay: high }
    steps:
      - action: utter_latency_hold
```

---

## 6 — Logging Format (Schema Aligned)
```json
{
  "event_type": "latency_operator",
  "pld": {
    "phase": "alignment_support",
    "code": "latency_hold",
    "confidence": 0.98
  },
  "payload": {
    "delay_seconds": 3.14,
    "strategy": "hold"
  }
}
```

---

## 7 — Anti-Patterns

| Anti-Pattern                  | Impact                                      |
| ----------------------------- | ------------------------------------------- |
| ❌ silent delay                | ↑ risk of **D1_instruction** drift          |
| ❌ typing indicator spam       | perceptual instability → **D3_flow**        |
| ❌ abrupt reset without update | perceived failure → triggers repair cascade |
| ❌ apology stacking            | decreases trust                             |

---

## 8 — Interaction Rules

| Situation                     | Correct Action                                               |
| ----------------------------- | ------------------------------------------------------------ |
| Delay before uncertain output | Latency Hold → (optional) R1_clarify                         |
| Delay after repeated failure  | Expectation Reset → consider escalation to **R5_hard_reset** |
| Delay during tool execution   | Progressive Update                                           |

Latency handling is complete only when normal pacing and task continuity resume.

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
