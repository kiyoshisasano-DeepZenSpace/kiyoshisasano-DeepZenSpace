# Appendix A — Temporal Transparency Specifications

## A.1 Terminology
- **Confidence & Trust Transparency** — unified replacement for “Epistemic Transparency” and “Confidence Communication.”
- **Rhythm Layer** — sequence of Cue → Silence → Segment → Drift → Repair.
- **Temporal Transparency Feedback Loop** — integration of τ, hedge, and trust.

---

## A.2 Aggregation Windows
- **Per-turn metrics:** capture immediate interaction dynamics (τ, CD, trust input).
- **Per-session metrics:** provide holistic summaries (RCI, MR, TTR, TAI session means/medians).

---

## A.3 Metric Formulas

```text
RCI_turn  = DTW_sim(latency_seq_user, latency_seq_system) ∈ [0,1]
RCI_sess  = median(RCI_turn)                              target > 0.80

TAI_turn  = 1 − |trust_turn(0..100) − accuracy_turn(0..100)| / 100
TAI_sess  = mean(TAI_turn)                                target > 0.75

CD_turn   = |verbal_conf_turn − measured_accuracy_turn|    (0..1 scale)
CD_sess   = mean(CD_turn)                                 target < 0.10

MR_sess   = misaligned_turns / total_turns                target < 0.10

TTR_turn  = t(repair_end) − t(breakdown_start)            target < 1.5s (95th pct)
```

- **RCI:** rhythmic coherence (DTW or PLV-based); typical 0.6–0.9, ideal ≈0.8+.
- **TAI:** trust–accuracy coupling; difference form preferred for real-time computation.
- **CD:** calibration deviation; acceptable <0.10 for well-aligned confidence displays.

---

## A.4 Timing Policies (τ) and Repairs

### τ Pause Targets (Text Modality)
- **Baseline:** τ_base = clamp(300 ms, 150, 700) − RTT_p50
- **Voice:** add +100–150 ms
- **Streaming:** deliver first token <300 ms; continue in 200–250 ms chunks.

### State Machine (Pseudo-code)
```python
τ_base = clamp(300, 150, 700) - rtt_p50_ms

# Hedge-aware micro-delay
if model_conf < 0.70:
    τ_base += random.randint(150, 200)
elif 0.70 <= model_conf < 0.85:
    τ_base += random.randint(50, 100)

# Streaming
if predicted_tokens > N_stream_threshold:
    start_streaming(target_first_token_ms=300, chunk_ms=200)

# Repair triggers
if response_delay_ms > 700 or mr_spike(k=3, n=5):
    trigger_auto_repair()  # rephrase → clarify → hand-off (≤2 clicks)

# Success criteria
# MR ↓ post-repair, TAI ↑, no user abandonment
```

---

## A.5 Hedging Gates and UI Coherence

| Confidence | Example wording (EN) | Example wording (JA) | UI Band | Icon | System Action |
|-------------|----------------------|----------------------|----------|------|----------------|
| ≥0.85 | “I’m confident that …” | 「確信しています…」 | High | ✔ | Normal τ |
| 0.70–0.85 | “It’s likely that …” | 「おそらく…と思われます」 | Medium | ≈ | +50–100 ms τ |
| <0.70 | “Possibly … (source…)” | 「可能性があります（出典：…）」 | Low | ? | +150–200 ms τ + citation |

Lint check ensures wording–color–icon–% coherence at build time.

---

## A.6 Trust Measurement

- **Per-turn:** 0–100 trust slider for continuous feedback.
- **Post-task:** TIAS or S-TIAS (Cronbach α ≈ 0.85+).
- **Frequency:** each turn + post-task summary.
- **TAI safeguard:** if TAI_sess < 0.60 → automatic mitigation (stronger hedge, slight τ increase, source display).

---

## A.7 Telemetry Log Schema

```json
{
  "session_id": "uuid",
  "turn_id": 12,
  "timestamps": {
    "user_input": 1734012345.120,
    "system_start": 1734012345.220,
    "first_token": 1734012345.490,
    "system_end": 1734012347.010
  },
  "network": { "rtt_ms_p50": 120, "rtt_ms_p95": 240 },
  "latency": {
    "τ_base_applied_ms": 280,
    "response_delay_ms": 540,
    "stream_chunks": 6
  },
  "confidence": {
    "model_conf": 0.78,
    "verbal_conf": 0.75
  },
  "accuracy": {
    "predicted": 0.72,
    "measured": 0.70
  },
  "trust": {
    "user_trust_turn": 68,
    "user_trust_post_task": 74
  },
  "repair": {
    "triggered": true,
    "reason": "response_delay>700|mr_spike",
    "type": "clarification",
    "success": true
  },
  "derived_metrics": {
    "CD_turn": 0.05,
    "TAI_turn": 0.98,
    "misaligned_turn": false
  },
  "locale": "ja-JP",
  "modality": "text"
}
```

---

## A.8 SDK Helpers

```python
def compute_rci_session(lat_user, lat_sys):
    return median([dtw_similarity(u, s) for u, s in zip(lat_user, lat_sys)])

def compute_cd_turn(verbal_conf, measured_acc):
    return abs(verbal_conf - measured_acc)

def compute_tai_turn(trust_0_100, acc_0_100):
    return 1.0 - abs(trust_0_100 - acc_0_100) / 100.0

def mr_spike(history, k=3, n=5):
    return sum(history[-n:]) >= k

def τ_policy(rtt_p50_ms, model_conf, modality, pred_tokens):
    base = max(150, min(700, 300 - rtt_p50_ms))
    if modality == "voice": base += 100
    if model_conf < 0.70: base += 150
    elif model_conf < 0.85: base += 75
    if pred_tokens > 80: start_stream(first_token_ms=300, chunk_ms=200)
    return base
```

---

## A.9 Pilot Acceptance & Ethics Gates

**Pilot (n ≥ 10, 1–2 weeks):**
- MR < 10% (session mean)
- TTR < 1.5 s (95th percentile)
- RCI > 0.80 (median)
- CD < 0.10
- TAI > 0.75
- ΔTAI(650–400 ms) < 0

**Runtime thresholds:**
- τ_pause = 300 ± 200 ms (RTT corrected, min 150, max 700)
- Repair success ≥ 80% (trigger → success)

**Ethics Gate:**
If short delay < 250 ms + assertive ≥ 0.85 + measured accuracy < 0.70 →
system must auto-hedge, show citation, and log the event.

---

## A.10 Figure Update Notes

- **Layer A:** “Rhythm (Cue–Silence–Segment–Drift–Repair)” with micro-time hints under each node (Cue < 100 ms, Silence 200–500 ms, Segment 1–3 s, Drift > 500 ms lag, Repair ≤ 2 turns).
- **Layer B:** “Confidence & Trust Transparency.”
- Update labels:
  - “Confidence display” → “Confidence Indicator (%) / icon”
  - “User trust” → “User Trust (0–100)”
- Central arrow: double-line “Temporal Transparency Feedback Loop (τ, hedge, trust).”
- RCI > 0.8 tag near “Resonant Closure.”
- Gray formula under TAI badge: *TAI = 1 − |trust − acc| / range*.
- Legend: *Telemetry APIs – latency, confidence, trust_input*.
- Repair links: dashed arrows labeled *auto-repair triggers*.

---

## A.11 Implementation Priority

| Tier | Focus | Deliverables |
|------|--------|--------------|
| **0 – Essential (Week 1)** | τ policy, hedging gates, per-turn trust slider | MR, TTR, RCI, CD, TAI |
| **1 – Extended (Week 2–3)** | Dashboard (latency–confidence–trust coupling), auto-repair, ethics gate | Real-time monitoring |
| **2 – Advanced (Later)** | Cultural/language tuning, voice modality adaptation, public case study | Cross-locale refinement |

---

## A.12 Business Impact Summary

- **Trust stability:** TAI > 0.75 → ↑ user retention, ↓ churn.
- **Efficiency:** TTR < 1.5 s → ↓ re-query / correction effort.
- **Quality assurance:** CD < 0.10 → ↓ false trust and support overhead.
- **Accountability:** Telemetry + Ethics Gate → transparent, auditable interactions.

---

### References
Bansal et al. (2019), *CHI* — Uncertainty displays and trust  
Liao et al. (2018), *CSCW* — Grounding and repair in dialogue  
Zhang (2024), *arXiv:2405.02045* — Rhythmic synchrony metrics  
Hoffman et al. (2021), *TOCHI* — Transparency dashboards  
Xu et al. (2025), *Frontiers in AI* — Linguistic uncertainty and trust  
McGrath et al. (2025), *Frontiers in AI* — TIAS/S-TIAS validation  
Afroogh et al. (2024), *Nature Communications* — Adaptive trust calibration  
Noh (2025), *Social Cognition Journal* — Cross-cultural timing  
Glikson & Woolley (2020), *Annual Review of Psychology* — Trust and AI ethics
