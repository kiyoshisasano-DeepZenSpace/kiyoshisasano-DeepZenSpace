---
title: "Logging & Schema Examples — PLD System Layer"
version: 2025.1
status: stable
maintainer: "Kiyoshi Sasano"
category: "patterns/system"
tags:
  - PLD
  - logging
  - schema
  - observability
  - runtime governance
---

# 🧩 Logging & Schema Examples (PLD System Layer)

Logging is how a PLD-enabled system becomes **observable, measurable, and improvable.**  
This guide shows **correct, schema-aligned examples** for runtime logging across:

- Drift detection  
- Repair attempts  
- Reentry success measurement  
- Outcome boundaries  
- Latency & execution metadata  
- Cross-runtime implementation patterns  

All examples comply with:

📌 `quickstart/metrics/schemas/pld_event.schema.json`  
📌 `quickstart/metrics/schemas/metrics_schema.yaml`

---

## 1. Minimal Valid Turn Event

Use when the system emits a turn with **no drift, no repair, no tool execution**.

```json
{
  "event_id": "b07cc93c-0178-4a59-b9c4-f1d78afe25fd",
  "timestamp": "2025-02-01T13:22:41Z",
  "session_id": "demo_001",
  "turn_id": 1,
  "event_type": "info",
  "source": "assistant",
  "pld": { "phase": "none", "code": "NONE" },
```

---

## 2. Drift → Repair → Reentry Example

This is the canonical PLD life cycle.
```json
[
  {
    "event_type": "drift_detected",
    "event_id": "a3f15c05-a257-4410-a5d1-513da3b2ab20",
    "timestamp": "2025-02-01T13:22:51Z",
    "session_id": "demo_001",
    "turn_id": 3,
    "source": "assistant",
    "pld": {
      "phase": "drift",
      "code": "D2_context",
      "confidence": 0.83
    },
    "metrics": { "latency_ms": 1850 }
  },
  {
    "event_type": "repair_triggered",
    "event_id": "9eb2f09d-9b43-49fc-b67c-4ad1c9ab6611",
    "timestamp": "2025-02-01T13:22:54Z",
    "session_id": "demo_001",
    "turn_id": 4,
    "source": "assistant",
    "pld": {
      "phase": "repair",
      "code": "R1_soft_repair",
      "confidence": 0.91
    },
    "payload": {
      "strategy": "clarify_constraints",
      "prompt": "Sorry — can you confirm the price range?"
    }
  },
  {
    "event_type": "reentry_observed",
    "event_id": "621f426f-e5be-4acc-b393-7ea4db5cb029",
    "timestamp": "2025-02-01T13:23:05Z",
    "session_id": "demo_001",
    "turn_id": 5,
    "source": "user",
    "pld": {
      "phase": "reentry",
      "code": "RE1_intent"
    }
  }
]
```

---

## 3. Outcome Event (Session Boundary)
Logged only **once per dialogue**.

```json
{
  "event_id": "644e8113-2b14-4e61-b5ff-9821c5cecc1b",
  "timestamp": "2025-02-01T13:27:11Z",
  "session_id": "demo_001",
  "turn_id": "final",
  "event_type": "outcome",
  "source": "system",
  "pld": { "phase": "outcome", "code": "OUT1_complete" },
  "metrics": {
    "summary": {
      "drift_count": 1,
      "repairs": { "soft": 1, "hard": 0 },
      "reentries": 1
    }
  }
}
```

---

## 4. Schema Validation Example (Python)

```python
from jsonschema import validate, ValidationError
import json

with open("quickstart/metrics/schemas/pld_event.schema.json") as f:
    schema = json.load(f)

def validate_event(event: dict):
    try:
        validate(event, schema)
        return True
    except ValidationError as e:
        print("❌ Schema validation failed:", e)
        return False
```

---

## 5. DuckDB Ingestion Pattern

```sql
CREATE TABLE events AS
SELECT * FROM read_json_auto('logs/*.jsonl');
```

Example query:
```sql
SELECT 
  pld->>'code' as pld_code,
  COUNT(*) 
FROM events
WHERE event_type='drift_detected'
GROUP BY 1;
```

---

## 6. Best Practices Checklist

| Rule                                                               | Status               |
| ------------------------------------------------------------------ | -------------------- |
| Each event has `event_id`, `timestamp`, `session_id`, `event_type` | ✅                    |
| Drift → Repair → Reentry sequences logged independently            | ✅                    |
| Outcome logged once per session                                    | ✅                    |
| Latency + execution metadata included where relevant               | Recommended          |
| Schema validation used prior to ingestion                          | Strongly recommended |

---

## Summary

> Logging is the bridge between runtime behavior and measurable stability.
This file ensures all PLD systems produce **consistent, analyzable, interoperable logs**.
  "payload": { "text": "Hello! How can I help?" }
}
