---
title: "Drift Event Logging Guide — Applied-AI Edition"
version: 2025.1.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "metrics/logging"
tags:
  - PLD
  - telemetry
  - alignment
  - runtime logging
---

# Drift Event Logging Guide (Applied Runtime Edition)

This guide defines how to record **PLD-aligned runtime interaction events** using the canonical schema:

📄 `quickstart/metrics/schemas/pld_event.schema.json`

Logging with a shared schema enables:

- Drift / repair / failover tracking  
- Operational stability metrics (PRDR, VRL, MRBF, FR, REI)
- A/B evaluation of recovery strategies
- Dashboard-based monitoring (`reentry_success_dashboard.json`)

---

## 1. What Must Be Logged?

Every turn MUST emit a PLD event containing:

| Field | Requirement | Source |
|-------|------------|--------|
| `event_id` | required | UUID |
| `timestamp` | required | Runtime clock |
| `session_id` | required | Conversation or task identifier |
| `turn_id` | required | Monotonic sequence |
| `event_type` | required | Drift / repair / outcome / failover / info |
| `pld.phase` | required | none / drift / repair / reentry / failover / complete |
| `pld.code` | required | Canonical code from taxonomy |

Optional but recommended fields:

| Field | Usage |
|-------|-------|
| `payload.text` | Debugging, UX attribution |
| `runtime.latency_ms` | Correlation with drift / repair patterns |
| `metrics.cost_tokens` | Enables REI + MRBF trending |
| `tags[]` | Feature flags, rollout phases |

---

## 2. Logging Convention

- **No missing keys** → use `null`, do not omit  
- **Events must be chronological**  
- **Identity continuity:** `session_id` never resets during repair loops  
- **Event type must reflect agent intent** (not UI wording)

Example mapping:

| Agent behavior | event_type | example pld.code |
|----------------|------------|------------------|
| Drift detected | `drift_detected` | `D5_information` |
| Soft repair | `repair_triggered` | `R2_soft_repair` |
| Visible repair message | `repair_visible` | `R1_clarify` |
| Successful reentry | `reentry_observed` | `RE3_auto` |
| Hard failure / abandon | `failover_triggered` | `OUT3_abandoned` |

---

## 3. Minimal Logging Implementation (Python)

```python
import uuid, time, json
from jsonschema import validate
from pathlib import Path

SCHEMA_PATH = "quickstart/metrics/schemas/pld_event.schema.json"
LOG_PATH     = Path("logs/pld_events.jsonl")

schema = json.loads(Path(SCHEMA_PATH).read_text())

def log_pld_event(session_id, turn_id, event_type, pld_code, payload=None, runtime=None):
    event = {
        "event_id": str(uuid.uuid4()),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "session_id": session_id,
        "turn_id": turn_id,
        "event_type": event_type,
        "pld": {
            "phase": pld_code.split("_")[0].lower().replace("d","drift").replace("r","repair"),
            "code": pld_code
        },
        "payload": payload or {},
        "runtime": runtime or {}
    }

    validate(event, schema)

    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")
```

---

## 4. Recommended Logging Frequency

| Situation | Log event? | Notes |
|-----------|------------|-------|
| Every turn | ✔ | Ensures baseline |
| Drift detection triggered | ✔ | Required |
| Any repair attempt | ✔ | Counted in VRL + MRBF |
| Failover / abandonment | ✔ | Mandatory |
| Tool call execution | ✔ | High-risk drift source |

---

## 5. Validation Workflow

```python
from jsonschema import validate
validate(instance=event, schema=schema)
```

For batch ingestion:

```
duckdb  🡪  parquet 🡪 supabase table 🡪 dashboards
```

---

## 6. Next Steps

| Task | Reference |
|------|----------|
| Test logging sample | `datasets/pld_events_demo.jsonl` |
| Confirm schema compliance | `schemas/pld_event.schema.json` |
| Enable monitoring | `dashboards/reentry_success_dashboard.json` |
| Interpret drift patterns | Operational Metrics Cookbook |

---

Maintainer:  
**Kiyoshi Sasano — Applied AI Runtime Systems (2025)**



