# 🛰️ Drift Event Logging – Operational Guidelines

_Last updated: 2025-08-01_

This guide describes how to detect and log **drift events** in systems that adopt the **Phase Loop Dynamics (PLD)** framework. Drift is not treated as an error — it’s recognized as **structural rhythm** or a signal of misalignment that invites **repair** or **reentry**.

---

## 🔍 What Is a Drift Event?

A **drift** occurs when user behavior deviates from the expected flow. Common causes include:

- Hesitation or silence (e.g., no input for 10s)
- Low NLU confidence (e.g., < 0.4)
- Misdirected clicks (e.g., skipping steps)
- UI abandonment (e.g., premature close or modal exit)
- Ambiguous or short utterances

These moments signal **opportunities** — not failure — to adapt rhythm, clarify context, or reorient interaction.

---

## 🧾 Minimum Fields to Log

```yaml
event: drift_detected
timestamp: 2025-08-01T16:42:00Z
user_id: ab23f-xy91
session_id: s8791-33zx
drift_type: silence
source: rasa_server
ui_state: /checkout/payment
```

| Field            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| timestamp        | When drift was detected (ISO8601)                                           |
| user_id          | User/session identifier (pseudonymized if needed)                           |
| session_id       | Conversation or interaction session ID (optional but recommended)           |
| drift_type       | Type of drift: silence, low_confidence, misclick, off_path, input_divergence, unexpected_exit |
| source           | Origin of detection: rasa_server, figma_web, mobile_ui, etc.                |
| ui_state         | Screen, node, or component at the time of drift                             |
| confidence_score | System certainty (e.g., NLU confidence, intent match, LLM risk score)       |
| resolved_by      | Outcome: soft_repair, latency_hold, reentry_link, or none                   |

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

Drift does not require immediate fallback. Response options include:

- 💤 Passive logging only — observe behavior over time  
- 💬 soft_repair — “Want to clarify?” prompt  
- ⏸️ latency_hold — pause with visual rhythm signal  
- 🔁 reentry_link — re-invite user back to prior topic after pause  
- 🚫 No action — if drift is minor or self-correcting

---

## 📊 Suggested Metrics

| Metric Name              | Description                                                     |
|--------------------------|-----------------------------------------------------------------|
| drift_count              | Total drift events detected                                     |
| drift_to_repair_ratio    | % of drift events followed by a recovery attempt                |
| avg_time_to_repair       | Average delay between drift and repair                          |
| reentry_after_drift_rate | % of users who reengage after a drift                           |
| drift_resolution_rate    | % of drift events resolved by any PLD pattern                   |

---

## 🔄 Optional Fields for Traceability

| Field                 | Use Case                                                          |
|-----------------------|-------------------------------------------------------------------|
| drift_count_in_session| Track cumulative drifts to trigger escalation                     |
| preceding_event_id    | Reference the trigger event before this drift                     |
| triggered_repair_id   | Correlate repair attempts caused by this drift                    |
| device_type           | e.g., mobile, desktop, IVR, voice_app                             |

---

## 🧠 Interpretative Notes

- Not every drift is bad — hesitation may reflect thoughtful intent  
- New users may show more drift due to onboarding unfamiliarity  
- Visualize drift using session replays or journey maps  
- You may want to soft-branch based on drift intensity or frequency

📌 Example:  
On a form, a user pauses for 7 seconds and hovers back and forth before clicking submit — this may be drift due to doubt, not confusion.

---

## 📚 Related Patterns

```markdown
- soft_repair       → Clarify gently  
- latency_hold      → Use time rhythm to reduce pressure  
- reentry_link      → Invite back after delay  
```

“Drift isn't the problem — it's the rhythm between expectation and expression.”
— Phase Loop Dynamics

```yaml
status: production_ready
version: 1.1
```
