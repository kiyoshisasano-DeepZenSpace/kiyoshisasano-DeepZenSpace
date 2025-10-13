# Designing Temporal Transparency
### Interaction Rhythm and **Confidence & Trust Transparency (CTT)** for Human–AI Dialogue

> **Terminology Policy (Read First)**  
> In this practitioner edition, we use **Confidence & Trust Transparency (CTT)** as the primary implementation term.  
> **Epistemic Transparency** is treated as a **synonym** in academic contexts. When you see "CTT", read it as the concrete, product-facing form of epistemic transparency.

**Figure 1:** *Dual-Layer Interaction Loop* (Rhythm ↔ CTT)  
`06_translation_interface//HCI_translation/dual_layer_interaction_loop_v2.svg`

---

## 0. Executive Summary (for product & UX leads)

**Why now:** Conversational and embodied AI products win or lose on **two coupled levers**:  
1) **Interaction Rhythm** (timing, pauses, repair) → signals attentiveness.  
2) **CTT** (confidence display & trust calibration) → signals competence & honesty.  

**Business value:** Teams that tune these levers together see higher **task completion**, **retention**, and **trust** with **lower support load**. This doc gives you defaults that ship and metrics that prove it.

**Start here (90‑day plan)**  
- **Week 1–2:** Enable **latency control** (τ_pause 300±200 ms with RTT compensation) and **CTT gates** (hedging bands).  
- **Week 3–4:** Log **RCI/MR/TTR/CD/TAI** and add a light **trust input** slider (0–100) per turn.  
- **Week 5–8:** Run a pilot (n≥10), tune thresholds; ship **auto‑repair** for delays >700 ms.  
- **Week 9–12:** Dashboard & guardrails (ethics gates), localize timing & hedges per language.

---

## 1. Core Concepts (kept practical)

### 1.1 Interaction Rhythm (Layer A)
Micro‑timing that maintains conversational flow.

| Element | Function | Typical Window (text UI) |
|---|---|---|
| **Cue** | readiness signal | < 100 ms |
| **Silence** | deliberate/computational pause | **200–500 ms** |
| **Segment** | coherent response unit | 1–3 s |
| **Drift** | loss of alignment | > 500 ms lag |
| **Repair** | restore flow | ≤ 2 turns |

### 1.2 Confidence & Trust Transparency (CTT, Layer B)
How systems **express** uncertainty and **collect** trust signals.

- **Confidence Indicator:** %/band + icon or color.  
- **Hedging Language:** verbal tone matched to confidence band.  
- **Trust Input:** lightweight 0–100 slider per turn.

> **One system, one story:** Visual confidence, wording, and timing must align.

---

## 2. Single Vocabulary (prevents confusion)

- **Primary term (product):** **Confidence & Trust Transparency (CTT)**  
- **Academic synonym:** *Epistemic Transparency*  
- **In code & logs:** use `confidence_indicator`, `hedge_band`, `trust_input`, `tai`

**Rationale:** Practitioners gravitate to confidence/trust wording. We keep the academic synonym in Appendix A for citation parity, but **we do not mix terms in UI text**.

---

## 3. Quick‑Start Priorities (what to ship first)

1) **Timing control with safety defaults**  
```text
τ_pause_base = clamp(300 ms, min=150, max=700) − RTT_p50
if model_confidence < 0.70: τ_pause_base += 150–200 ms   # “deliberation” micro‑delay
```

2) **CTT gates (hedge bands)**  
| Model Confidence | Band | UI Color/Icon | Wording Examples |
|---|---:|---|---|
| ≥ 0.85 | **Assert** | solid/✓ | “I’m confident that…”, “This is likely correct.” |
| 0.70–0.85 | **Light Hedge** | medium/≈ | “It seems…”, “Probably…”, “About…” |
| < 0.70 | **Medium Hedge** | pale/? | “Possibly…”, “I might be wrong…”, link to source |

3) **Auto‑repair triggers**  
- If **response_delay > 700 ms** (after RTT compensation) → `repair_prompt` (rephrase/ask/hand‑off).  
- If **MR spikes** (≥3 misalignments in last 5 turns) → same as above.  
- **Target:** repair_success ≥ **80%**.

4) **Trust input (per turn)**  
- Slider 0–100, tiny footprint. Persist as `trust_input`.  
- Use to compute **TAI** and adapt future timing/hedge.

---

## 4. Metrics (definitions you can implement)

**Aggregation:** compute **per turn**, report **per session mean** unless noted.

```text
MR  = misaligned_turns / total_turns                 # 0..1
TTR = t_repair_end - t_breakdown                     # seconds
RCI = dtw_similarity(inter_turn_latencies)           # 0..1, >0.80 desired
CD  = abs(model_confidence - measured_accuracy)      # 0..1, <0.10 desired
TAI = 1 - abs(trust_input - measured_accuracy)/100   # 0..1, >0.75 desired
```

- **Measured accuracy** can be offline (gold labels) or proxied (expert rating).  
- **Windowing:** turn‑level for adaptation; session mean for reporting; p95 for SLOs.

**Acceptance (pilot):** MR < 10%, TTR p95 < 1.5 s, RCI median > 0.80, CD < 0.10, TAI > 0.75.

---

## 5. Operational Policies (ship‑ready)

### 5.1 Timing (τ) & streaming
- Subtract **RTT p50** from observed delays to normalize environment.  
- For long outputs, **stream**: first token < **300 ms**; chunk cadence 200–350 ms.  
- Voice UIs: add **+100–150 ms** to τ baselines.

### 5.2 Repair UX (two clicks to resolution)
Trigger → show **three** options: *rephrase*, *ask a clarifying question*, *hand‑off*.  
Guarantee resolution in ≤2 clicks. Log `repair_triggered`, `repair_type`, `repair_success`.

### 5.3 Ethics gates (anti‑patterns)
- **No deceptive fluency:** (short delay + strong assertion) with **acc < 70%** should be < **2%** of turns.  
- Auto‑disclose uncertainty when acc < 70% or after repair.

### 5.4 Internationalization
- Localize τ baselines & hedges (e.g., JP allows longer silences; hedging lexicon differs).  
- Keep color semantics culturally safe (avoid red/green without labels).

---

## 6. Dashboards (what PMs should see)

- **Overview:** MR/TTR/RCI/TAI/CD over time; facet by τ & hedge bands.  
- **Coupling View:** latency vs confidence scatter with repair markers; overlay trust curve.  
- **Cohorts:** device/network/language heatmaps for RCI & TAI.  
- **Funnel:** repair_triggered → repair_success; top 3 causes.

---

## 7. Implementation Snippets

### 7.1 τ controller (state machine)
```python
def compute_pause(conf, rtt_p50, segment_len_tokens):
    base = max(150, min(700, 300)) - rtt_p50
    if conf < 0.70:
        base += 150  # deliberation cue
    if segment_len_tokens > 80:
        return max(0, base)  # plus streaming policy below
    return max(0, base)

def should_stream(segment_len_tokens):
    return segment_len_tokens > 80  # aim first token < 300 ms

def auto_repair_needed(response_delay_norm, mr_spikes):
    return (response_delay_norm > 700) or (mr_spikes >= 3)
```

### 7.2 CTT gates (hedge selector)
```python
def hedge_band(conf):
    if conf >= 0.85: return "assert"
    if conf >= 0.70: return "light_hedge"
    return "medium_hedge"
```

### 7.3 Metric computation (per turn)
```python
def tai(trust_input, measured_accuracy):
    # trust_input: 0..100 ; measured_accuracy: 0..100
    return 1 - abs(trust_input - measured_accuracy)/100.0
```

---

## 8. Pilot Plan (1–2 weeks)

**Participants:** n=8–12 (mixed internal/external; JA/EN ok).  
**Tasks:** 2 tasks × 3–5 turns: (1) low‑uncertainty FAQ; (2) high‑uncertainty info‑seeking.  
**Manipulations:** τ = 250/400/650 ms (post‑RTT), hedge = assert/light/medium.  
**Logging:** `trust_input, model_conf, predicted_acc, τ_applied, response_delay, MR, TTR, RCI, CD, TAI, repair_*`  
**Decisions:** **Go** if MR<10%, TTR p95<1.5 s, RCI>0.80, CD<0.10, TAI>0.75; **Hold** otherwise.

---

## 9. Figure Redlines (align your SVG)

- Rename **Layer A** label to: “**Rhythm (Cue–Silence–Segment–Drift–Repair)**”.  
- Under each node, add time hints: Cue <100 ms; Silence 200–500 ms; Segment 1–3 s; Drift >500 ms lag; Repair ≤ 2 turns.  
- Change “Confidence display” → “**Confidence Indicator (%/icon)**”; “User trust” → “**User Trust (0–100)**”.  
- Make the vertical purple arrow a **double line** and label: “**Temporal Transparency Feedback Loop (τ, hedge, trust)**”.  
- Add mini‑label “**RCI>0.8**” near the Rhythm ring; add “**TAI = 1 − |trust − acc|/100**” near the CTT badge.  
- In legend, add “**Telemetry APIs: latency, confidence, trust_input**”.  
- Dotted lines to Repair: change to dashed **with arrowheads** + label “**auto‑repair triggers**”.

---

## Appendix A — Term Mapping (CTT ⇄ Epistemic Transparency)

| Practitioner Term | Academic Term | Notes |
|---|---|---|
| **Confidence & Trust Transparency (CTT)** | *Epistemic Transparency* | CTT is the product‑facing term; same construct. |
| Confidence Indicator | Confidence Display | Visual numeric/band indicator. |
| Hedge Band | Linguistic Uncertainty | Maps wording to confidence. |
| Trust Input | Trust Rating / Scale | TIAS/S‑TIAS compatible. |
| Trust Alignment Index (TAI) | Trust–Accuracy Calibration | Turn‑level coupling metric. |

---

## Appendix B — References (practitioner picks)
- Suchman (1987); Dourish (2001); Norman (2013); Clark (1996).  
- Bansal et al. (2019, CHI); Liao et al. (2018, CSCW); Hoffman et al. (2021, TOCHI).  
- Xu et al. (2025, TOCHI/Frontiers); McGrath et al. (2025, Frontiers); Afroogh et al. (2024, Nat Comm).  
- Zhang (2024, arXiv): timing & entrainment measurements.

---

## License

This document and accompanying figures are licensed under  
**Creative Commons Attribution–NonCommercial 4.0 International (CC BY-NC 4.0)**.  

You are free to share and adapt the material for any non-commercial purpose,  
provided that appropriate credit is given to the original author.  

**Commercial or for-profit use requires prior written permission or a formal collaboration agreement with the author.**

© 2025 [Kiyoshi Sasano / Organization]
