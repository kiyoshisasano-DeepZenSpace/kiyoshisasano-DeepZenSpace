# PLD Logging Examples — Event & Metrics Patterns  
*(2025 Applied Implementation Edition)*

**Purpose**  
Provide concrete logging patterns aligned with:

- `quickstart/metrics/schemas/pld_event.schema.json`
- `quickstart/metrics/schemas/metrics_schema.yaml`
- `metrics/multiwoz_2.4_n200/*` (reference evaluation set)

These examples ensure Drift → Repair → Reentry → Outcome → Latency are:

- traceable  
- measurable  
- comparable across runs  
- usable in evaluation dashboards  

Logging is **not optional** in PLD systems — it is how stability is monitored.

---

## 01 — Minimal PLD Event Record

Use when you only need **drift frequency and classification**.

```json
{
  "session_id": "mwz_200_001",
  "turn_id": 4,
  "speaker": "system",
  "event_type": "drift_detected",
  "drift_type": "D5_information_drift",
  "timestamp": "2025-01-01T12:34:56Z"
}
```

---

## 02 — Full Drift Cycle (Soft Repair + Reentry)

One drift → repair → reentry sequence across turns:

```json
[
  {
    "session_id": "mwz_200_001",
    "turn_id": 4,
    "speaker": "system",
    "event_type": "drift_detected",
    "drift_type": "D2_context_drift",
    "latency_ms": 1800,
    "metadata": { "reason": "forgot user budget constraint" }
  },
  {
    "session_id": "mwz_200_001",
    "turn_id": 5,
    "speaker": "system",
    "event_type": "repair_triggered",
    "repair_type": "R1_soft_repair",
    "metadata": { "strategy": "clarify_constraints" }
  },
  {
    "session_id": "mwz_200_001",
    "turn_id": 6,
    "speaker": "user",
    "event_type": "reentry",
    "reentry_type": "RE1_user_guided",
    "metadata": { "confirmation": "Yes, keep the same budget." }
  }
]
```

This is the **canonical evaluation sequence** in PLD.

---

## 03 — Session Outcome Summary

Logged **once per completed session**:

```json
{
  "session_id": "mwz_200_001",
  "event_type": "outcome",
  "outcome_type": "complete",
  "total_turns": 14,
  "total_drifts": 2,
  "soft_repairs": 2,
  "hard_repairs": 0,
  "reentries": 2,
  "timestamp": "2025-01-01T12:39:33Z"
}
```

Allows tracking of:

- Completion rate  
- Repair type distribution  
- Drift-per-dialogue baseline  

---

## 04 — Latency + Drift Correlation Logging

Useful for discovering **latency-induced drift**:

```json
[
  {
    "session_id": "demo_latency_01",
    "turn_id": 3,
    "speaker": "system",
    "event_type": "latency",
    "latency_ms": 4200,
    "metadata": {
      "phase": "tool_call",
      "tool_name": "hotel_search"
    }
  },
  {
    "session_id": "demo_latency_01",
    "turn_id": 3,
    "speaker": "system",
    "event_type": "drift_detected",
    "drift_type": "D5_information_drift",
    "metadata": {
      "reason": "tool returned `no_results`, response suggested available hotels"
    }
  }
]
```

---

## 05 — Rasa Integration Example

```json
{
  "session_id": "rasa_session_123",
  "turn_id": 7,
  "speaker": "system",
  "event_type": "repair_triggered",
  "repair_type": "R1_soft_repair",
  "drift_type": "D2_context_drift",
  "metadata": {
    "slot": "constraint_price",
    "previous_value": "50",
    "corrected_to": "150"
  }
}
```

---

## 06 — LangGraph Node Logging Example

Task execution event:

```json
{
  "session_id": "langgraph_demo_01",
  "turn_id": 5,
  "event_type": "task_execution",
  "metadata": {
    "node": "main_task_node",
    "input": "find 4-star hotels under 120",
    "drift_state": "none"
  }
}
```

Associated drift event:

```json
{
  "session_id": "langgraph_demo_01",
  "turn_id": 4,
  "event_type": "drift_detected",
  "drift_type": "D1_information_drift",
  "metadata": { "details": "previously claimed no hotels, now found 3" }
}
```

---

## 07 — Aggregated Metrics Record

Compatible with `metrics_schema.yaml`:

```json
{
  "run_id": "multiwoz_n200_run_01",
  "dataset": "multiwoz_2.4_n200",
  "total_dialogues": 200,
  "metrics": {
    "drift_events_total": 312,
    "avg_drift_per_dialogue": 1.56,
    "soft_repair_rate": 0.62,
    "hard_repair_rate": 0.10,
    "outcome_complete_rate": 0.75,
    "outcome_incomplete_rate": 0.14,
    "reentry_success_rate": 0.81
  },
  "timestamp": "2025-01-01T10:00:00Z"
}
```

---

## 08 — Example Queries (Conceptual SQL)

### Drift frequency

```sql
SELECT drift_type, COUNT(*) 
FROM pld_events 
WHERE event_type = 'drift_detected'
GROUP BY drift_type;
```

### Soft vs Hard Repair ratio

```sql
SELECT repair_type, COUNT(*) 
FROM pld_events 
WHERE event_type = 'repair_triggered'
GROUP BY repair_type;
```

### Drift → Outcome correlation

```sql
SELECT outcome.outcome_type, AVG(stats.drift_count) AS avg_drift
FROM (
  SELECT session_id, COUNT(*) AS drift_count
  FROM pld_events
  WHERE event_type = 'drift_detected'
  GROUP BY session_id
) AS stats
JOIN pld_outcomes AS outcome
  ON stats.session_id = outcome.session_id
GROUP BY outcome.outcome_type;
```

---

## 09 — Logging Best Practices

✔ Emit logs every turn  
✔ Use monotonic `turn_id`  
✔ Include latency fields when relevant  
✔ Store metadata minimally but meaningfully  
✔ Log even when **no drift** occurs (baseline required)

---

## Attribution

Maintainer: **Kiyoshi Sasano**  
License: **CC BY-NC 4.0**

