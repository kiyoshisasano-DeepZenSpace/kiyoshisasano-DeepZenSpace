# 04 — Latency Operator  
*Operator Primitive (Applied-AI Edition)*  

> **Purpose:** Maintain interaction rhythm stability during system delays, tool execution waits, processing uncertainty, or slow inference.  
> Latency is not just wait time — it is a **temporal alignment factor** that influences trust and perceived competence.

---

## **1 — Why Latency Matters**

Human conversation follows implicit timing rhythms.  
When responses exceed expected pacing, users assume:

- uncertainty  
- failure  
- loss of control  
- disengagement  

Unmanaged latency creates drift patterns:

| Latency Effect | Resulting Drift Pattern |
|----------------|------------------------|
| Hesitation gap | Drift-Engagement |
| Silent processing | Drift-Expectation |
| Tool timeout | Drift-Information |
| Message stacking | Drift-Procedural |

Latency management is therefore part of **interaction stability**, not UI decoration.

---

## **2 — Human-Perception Timing Thresholds**

| Delay Range | User Interpretation | System Strategy |
|------------|---------------------|----------------|
| **0–700ms** | Feels instant | Normal reply |
| **0.7–2.5s** | Slight delay | Optional micro-acknowledge |
| **2.5–6s** | System feels uncertain | **Latency Hold required** |
| **6s+** | Perceived breakdown | **Status message + expectation reset** |

These ranges are grounded in:

- conversational pause research  
- HCI latency tolerance studies  
- task-oriented agent evaluation  

---

## **3 — Latency Operator Forms**

| Operator Type | Definition | Use Case |
|---------------|------------|----------|
| **Hold** | Short placeholder signaling processing | Tool calls, moderate delay |
| **Progressive Update** | Multi-step status report | Long-running search or multi-layer action |
| **Expectation Reset** | Clarifies upcoming waiting time as intentional | Slow inference models / large DB |

---

## **4 — Canonical Interaction Patterns**

### **A. Latency Hold (Default)**  
Triggered at predicted delay > **2.5s**.

> “One moment — checking that now…”

---

### **B. Progressive Update**

> “Still working — now filtering results by your price range…”

Used when discrete processing stages exist.

---

### **C. Expectation Reset**

> “This may take ~10 seconds because the dataset is large.  
> I’ll update you as soon as results are ready.”

Used when:  
⚠ unavoidable latency  
⚠ user-facing workflow  
⚠ large context operations  

---

## **5 — Implementation Examples**

### **Python (Async Wrapper)**

```python
async def run_with_latency_operator(task):
    notify_after = 2.5
    task_result = await task.with_timeout(notify_after)

    if not task_result.ready:
        yield "Working on that — one moment..."
        task_result = await task.wait()

    return task_result.output
```

---

### **Rasa Policy Example**

```yaml
rules:
  - rule: Latency Hold
    condition:
      - slot_was_set: { action_latency: high }
    steps:
      - action: utter_latency_hold
```

---

### **OpenAI Assistants API Log Schema**

```json
{
  "event_type": "latency_operator",
  "strategy": "hold",
  "delay_seconds": 3.14
}
```

---

## **6 — Anti-Patterns**

| Anti-Pattern | Resulting Drift |
|--------------|----------------|
| ❌ Silent waiting | Drift-Expectation |
| ❌ Multiple “typing…” cycles | Drift-Engagement |
| ❌ Response reset mid-processing | Drift-Procedural |
| ❌ Apology stacking | Trust erosion |

---

## **7 — Latency × Repair Interaction Rules**

Latency modifies perceived system confidence.  
Correct handling depends on context:

| Scenario | Correct Strategy |
|----------|-----------------|
| Delay after incorrect output | Acknowledge + Soft Repair |
| Delay after repeated failure | Hard Repair + Expectation Reset |
| Delay before uncertain response | Pre-Hold + Confidence Check |

---

## **8 — Validation Checklist**

| Condition | Requirement |
|-----------|------------|
| Delay > 2.5s | ✔ Latency Operator required |
| Context preserved | ✔ |
| No new contradictions | ✔ |
| Operator type matched to scenario | ✔ |
| Interaction resumed smoothly | ✔ |

Latency handling is complete only once **normal pacing resumes** and the user perceives stability.

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
