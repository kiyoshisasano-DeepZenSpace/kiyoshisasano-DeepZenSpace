---
title: "Drift Event Logging Guide — Applied-AI Edition"
version: 2025.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "metrics/logging"
tags:
  - PLD
  - logging
  - drift detection
  - repair logging
  - applied AI
---

# Drift Event Logging Guide (Applied-AI Edition)

This guide explains **how to capture PLD-aligned interaction events** during live execution of LLM agents, tool-using systems, or multi-turn applications.

The goal is to ensure every agent produces **structured, machine-readable evidence** of:

- Drift  
- Repair  
- Reentry  
- Latency patterns  
- Outcome signals  

This enables **benchmarking, dashboards, and automated drift-aware improvements.**

---

## 1. What Should Be Logged?

Every interaction turn must generate a log entry following the schema:

| Field | Purpose |
|-------|---------|
| `session_id` | Identifies conversation or task thread |
| `turn_id` | Monotonic index of utterances |
| `speaker` | `user` / `system` / `tool` |
| `text` | Raw natural-language content |
| `drift` | `null` or subtype (e.g., `Drift-Information`) |
| `repair` | `null` or subtype (e.g., `SoftRepair-AddOptions`) |
| `latency_ms` | Execution + response latency |

📄 **Reference:** `schemas/pld_event.schema.json`

---

## 2. Minimal Logging Implementation

```python
import json
import time
from pathlib import Path

LOG_PATH = Path("logs/pld_events.jsonl")

def log_event(session_id, turn_id, speaker, text, drift=None, repair=None, latency_ms=None):
    event = {
        "session_id": session_id,
        "turn_id": turn_id,
        "speaker": speaker,
        "text": text,
        "drift": drift,
        "repair": repair,
        "latency_ms": latency_ms
    }
    
    LOG_PATH.parent.mkdir(exist_ok=True)
    if not LOG_PATH.exists():
        LOG_PATH.write_text("", encoding="utf-8")

    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
```

---

## 3. Drift + Repair Detection Injection Point

Example integration as middleware:

```python
def system_response(agent, session_id, turn_id, user_message):
    start = time.time()
    
    response, drift_type = agent.generate(user_message)
    repair_action = agent.detect_repair(response, drift_type)
    latency = int((time.time() - start) * 1000)
    
    log_event(
        session_id=session_id,
        turn_id=turn_id,
        speaker="system",
        text=response,
        drift=drift_type,
        repair=repair_action,
        latency_ms=latency
    )
    
    return response
```

📌 This ensures logging happens **before output delivery**, preventing silent drift.

---

## 4. Recommended Logging Frequency

| Event Type | Log? | Notes |
|------------|------|-------|
| Normal turn | ✔ | Drift may occur later |
| Tool call execution | ✔ | Tools are high drift-risk |
| Soft repair | ✔ | Required |
| Hard repair | ✔ | Required |
| Silence / timeout | ✔ | Treated as drift candidate |

---

## 5. Operational Quality Rules

| Rule | Description |
|------|------------|
| No missing fields | Use `null`, don’t omit |
| Controlled vocabulary | `drift` / `repair` must use taxonomy values |
| Preserve ordering | Logs must be chronological |
| Session continuity | Hard repair must not reset `session_id` |
| Latency required | Strong predictor of drift and repair |

---

## 6. Validation Workflow

Use the schema validator:

```python
from jsonschema import validate
import json

def validate_log_line(line, schema):
    validate(instance=line, schema=schema)
```

Schema file path:

```
quickstart/metrics/schemas/pld_event.schema.json
```

---

## 7. Next Steps

Once drift logging is operational:

| Next Task | Reference File |
|-----------|---------------|
| Aggregation | `datasets/pld_events_demo.jsonl` |
| Schema validation | `schemas/pld_event.schema.json` |
| Visualization | `dashboards/reentry_success_dashboard.json` |
| Case interpretation | `../reports/pld_events_demo_report.md` |

---

### Maintainer  
**Kiyoshi Sasano**  
Applied-AI Interaction Systems — 2025

