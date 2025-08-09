# 🛰️ Drift Event Logging – Operational Guidelines

_Last updated: 2025-08-09_

This guide describes how to detect and log **drift events** and related **repair/reentry patterns** in systems using the **Phase Loop Dynamics (PLD)** framework. Drift is not treated as an error — it’s recognized as **structural rhythm** or a signal of misalignment that invites **repair** or **reentry**.

---

## 🔍 What Is a Drift Event?

A **drift** occurs when user behavior deviates from the expected flow. Common causes include:

- Hesitation or silence (e.g., no input for 10s)
- Low NLU confidence (e.g., < 0.4–0.5)
- Misdirected clicks (e.g., skipping steps)
- UI abandonment (e.g., premature close or modal exit)
- Ambiguous or short utterances

These moments signal **opportunities** — not failures — to adapt rhythm, clarify context, or reorient interaction.

---

## 🧾 Minimum Fields to Log

Example: **drift_detected**

```yaml
event_type: drift_detected
timestamp: 2025-08-09T16:42:00Z
session_id: s8791-33zx
drift_type: silence
source: rasa_server
ui_state: /checkout/payment
confidence_score: 0.38
```

Example: **latency_hold** (required: `duration_ms`)

```yaml
event_type: latency_hold
timestamp: 2025-08-09T16:42:05Z
session_id: s8791-33zx
metadata:
  duration_ms: 900
  reason: soft_repair_probe
```

---

### Required Fields (by schema)

| Field         | Description |
|---------------|-------------|
| event_type    | One of: `drift_detected`, `repair_triggered`, `repair_failed`, `reentry_success`, `reentry_anchor_set`, `reentry_missing_anchor`, `repair_escalation`, `latency_hold` |
| timestamp     | ISO8601 datetime in UTC (`...Z`) |
| session_id    | Unique conversation/session identifier |
| metadata      | Object with additional details (e.g., `duration_ms` for `latency_hold`) |

> **Special case:** `latency_hold` must include `metadata.duration_ms` (number, ms). A `reason` string is recommended for context.

---

## ⚙️ Drift Detection Triggers

| Method                  | Example                                                          |
|-------------------------|------------------------------------------------------------------|
| Inactivity Timer        | No input for 8–12 seconds                                       |
| NLU Confidence Threshold| Intent confidence < 0.5                                         |
| Click Path Anomaly      | Jump from step 1 → 4 without intermediate steps                 |
| Input Pattern Divergence| Token sequence doesn't match expected entity pattern            |
| Premature Exit          | Modal closed or user navigated away unexpectedly                |

---

## 🔗 What Happens After Drift?

Drift may trigger:

- 💤 Passive logging — observe behavior over time  
- 💬 `repair_triggered` — “Want to clarify?” prompt  
- ⏸️ `latency_hold` — deliberate pause with rhythm signal  
- 🔁 `reentry_success` — resuming a prior abandoned intent  
- 🚫 No action — if drift is minor/self-correcting

---

## 📊 Suggested Metrics

| Metric Name              | Description |
|--------------------------|-------------|
| drift_count              | Total drift events detected |
| drift_to_repair_ratio    | % of drift events followed by repair |
| avg_time_to_repair       | Avg. delay between drift and repair |
| reentry_success_rate     | % of users reengaging after drift |
| latency_interrupt_rate   | % of pacing holds cancelled by user |

---

## 🔄 Optional Fields for Traceability

| Field                 | Use Case |
|-----------------------|----------|
| drift_count_in_session| Trigger escalation after N drifts |
| preceding_event_id    | Link to triggering event |
| triggered_repair_id   | Correlate repair attempts |
| device_type           | mobile, desktop, IVR, etc. |

---

## 🛠 Implementation Example (Rasa actions.py)

```python
log_event("latency_hold", tracker, {
    "duration_ms": float(tracker.get_slot("latency_ms") or 900),
    "reason": "soft_repair_probe"
})
```

Ensure every `latency_hold` event includes `duration_ms` in metadata, or validation will fail.

---

## ✅ Validation

To check event logs against the schema:

```powershell
.alidator_venv\Scripts\python.exe .\pld_metrics_validator\pld_metrics_validator.py `
  --schema ".\pld_metrics_validator\pld_event.schema.json" `
  --input "._quickstart_kit\pld_events_demo.jsonl" `
  --report "._quickstart_kit\pld_events_demo_report.md" `
  --strict
```

Review the generated `pld_events_demo_report.md` to ensure all events are valid.

---

“Drift isn't the problem — it's the rhythm between expectation and expression.”  
— Phase Loop Dynamics

```yaml
status: production_ready
version: 1.2
```
