# Operator Specifications — L₁…L₅ (PLD → HCI)  
**Folder:** `06_translation_interface/HCI_translation/hci_translation_pld_implementation/`  
**Version:** 1.0 • Last updated: 2025-10-13  
**License:** CC BY-NC 4.0  
**Maintainer:** Phase Loop Dynamics Research Group

---

## 0. Purpose

This document specifies the **five PLD operators** as **implementable HCI components**.  
Each section defines **inputs/outputs, control parameters, detection/actuation logic, logging, metrics, and failure modes**, with contracts aligned to `05_logging_schema_and_contracts.md`.

Operators: **L₁ Segment Detection**, **L₂ Drift–Repair**, **L₃ Latency (Hold)**, **L₄ Feedback Reflex**, **L₅ Alignment–Resonance**.

---

## L₁ — Segment Detection (Boundary Operator)

**Role:** Detect interaction **segment boundaries** using syntactic/temporal/prosodic evidence. Often precedes L₂.  
**State impact:** emits `SEGMENT_START/END` signals to the temporal state machine (TSM).

### I/O Contract
| Channel | Name | Type | Description |
|--------|------|------|-------------|
| In | `stream.text` | tokens / transcript | Live or buffered text |
| In | `stream.audio` | PCM / prosody features | Optional prosodic cues |
| In | `timing.silence_ms` | number | Rolling silence window |
| Out | `signal.boundary` | enum{start,end} + index | Emits boundary markers |
| Out | `event.log` | `drift_detected?` | If boundary co-occurs with drift |

### Control Parameters
| Param | Default | Range | Notes |
|------|---------|-------|------|
| `θ_pause_ms` | 800 | 500–1500 | Silence threshold for boundary |
| `θ_topic` | 0.35 | 0.2–0.5 | Embedding distance threshold |
| `win_tokens` | 32 | 16–64 | Window for TextTiling/segmentation |

### Reference Algorithm (pseudo)
```python
def detect_boundary(emb_prev, emb_cur, silence_ms, pause_thr=800, topic_thr=0.35):
    if silence_ms >= pause_thr: 
        return 'end'
    if cosine_distance(emb_prev, emb_cur) >= topic_thr:
        return 'start'
    return None
```

### Logging (if boundary causes drift probe)
- Emit `drift_detected` when boundary aligns with low confidence / off-path indicators.

### Metrics
- Boundary **Precision/Recall**, Pk / WindowDiff; mean pause at boundary.

### Failure Modes
- Over-segmentation on noisy pauses; under-segmentation without pauses.

---

## L₂ — Drift–Repair (Sequential Operator)

**Role:** Detect **drift** and initiate **repair** with capped attempts.  
**State impact:** transition `DRIFT → REPAIR → (REENTRY|HANDOFF|SEGMENT)`.

### I/O Contract
| Channel | Name | Type | Description |
|--------|------|------|-------------|
| In | `tsm.signal.drift` | score | Aggregated drift score |
| In | `nlu.confidence` | 0–1 | Intent confidence |
| In | `history.embedding_drift` | distance | Contextual shift |
| Out | `ui.prompt.repair` | message/options | Clarification UI |
| Out | `tsm.transition` | enum | `REPAIR|REENTRY|HANDOFF` |
| Out | `event.log` | events | `drift_detected`, `repair_triggered` etc. |

### Control Parameters
| Param | Default | Range | Notes |
|------|---------|-------|------|
| `θ_drift` | 0.5 | 0.4–0.6 | Confidence floor |
| `max_repair_attempts` | 2 | 1–3 | Cap to avoid loops |
| `repair_timeout_ms` | 12000 | 8000–15000 | Wait for response |

### Decision Logic (pseudo)
```python
def handle_drift(ctx):
    log('drift_detected', {...})
    if ctx.repair_attempts >= MAX_ATTEMPTS:
        log('repair_failed', {'failed_attempts': ctx.repair_attempts})
        return HANDOFF
    suggest_latency(900)  # hint only; UI renders hold
    log('repair_triggered', {'attempt': ctx.repair_attempts + 1, 'strategy': 'soft_repair'})
    show_clarification()
```

### Logging
- `drift_detected` (with `confidence_score`, `ui_state`, `attempt`)  
- `latency_hold` (UI logs with `duration_ms`)  
- `repair_triggered` / `repair_failed`  
- On success: `reentry_success` (with `previous_context_id`, `reentry_lag`)

### Metrics
- **DRR** (drift→repair ratio), **RSR** (repair success), **MTD→R** (mean time drift→reentry).

### Failure Modes
- Over-trigger on minor deviations; infinite loops if cap missing.

---

## L₃ — Latency Operator (Hold/Pacing)

**Role:** Introduce **intentional delay** (τ) to shape rhythm, before/after repair. UI responsibility.  
**State impact:** `LATENCY_HOLD` with **cancellable** timer.

### I/O Contract
| Channel | Name | Type | Description |
|--------|------|------|-------------|
| In | `telemetry.suggest_latency_ms` | number | Hint from policy/LLM |
| In | `ui.user_input` | events | Interrupt signal |
| Out | `ui.render.hold` | animation | Shimmer/ellipsis/overlay |
| Out | `event.log` | `latency_hold` | Required metadata |

### Control Parameters
| Param | Default | Range | Notes |
|------|---------|-------|------|
| `τ_latency_ms` | 900 | 600–1500 | Base hold duration |
| `σ_kernel_ms` | 200 | 100–400 | Gaussian kernel width |
| `interrupt_window_ms` | 50 | ≤50 | Cancel latency on input |

### Rendering Contract (UI)
```ts
if (hint.suggest_latency_ms) {
  log('latency_hold', { duration_ms: hint.suggest_latency_ms, reason: hint.reason, context_id });
  await renderHold(hint.suggest_latency_ms, { cancellable: true });
}
```

### Metrics
- Mean Latency Hold (MLH), dropout change, drift suppression during pacing.

### Failure Modes
- Excessive latency (frustration), fixed τ feels artificial, non-cancellable holds.

---

## L₄ — Feedback Reflex (Adjoint Correction)

**Role:** **Immediate micro-adjustment** after user feedback to preserve stability.  
**State impact:** subtle pace/phrase correction without leaving current task state.

### I/O Contract
| Channel | Name | Type | Description |
|--------|------|------|-------------|
| In | `feedback.signal` | event | Confirm/deny/affect cues |
| In | `telemetry.latency/tempo` | ms/Hz | Current pacing |
| Out | `ui.adjust` | params | Tempo/intensity/language echo |
| Out | `event.log` | custom | `reflex_latency_ms`, `adjust_type` |

### Control Parameters
| Param | Default | Range | Notes |
|------|---------|-------|------|
| `t_reflex_ms` | 120 | 50–250 | Time to first adjustment |
| `gain_reflex` | 0.5 | 0.2–0.8 | Adjustment magnitude |
| `echo_depth` | 1 | 0–2 | Language echo strength |

### Reflex Loop (pseudo)
```python
def reflex(feedback, tempo, gain=0.5):
    start = now()
    adjust = compute_adjustment(feedback, tempo, gain)
    apply(adjust)
    log('reflex', {'reflex_latency_ms': now()-start, 'adjust_type': adjust.kind})
```

### Metrics
- Reflex latency, re-alignment success, post-reflex drift recurrence.

### Failure Modes
- Overfitting to transient behavior; mistimed reflex breaks pacing.

---

## L₅ — Alignment–Resonance (Stability Window)

**Role:** Maintain **synchronized rhythm/structure**; exit on topic change or drift.  
**State impact:** `RESONANCE` window with monitoring.

### I/O Contract
| Channel | Name | Type | Description |
|--------|------|------|-------------|
| In | `monitor.coherence` | 0–1 | Real-time coherence / tempo match |
| In | `events.topic_shift` | boolean | Exit trigger |
| Out | `ui.echo.pacing` | params | Maintain alignment cues |
| Out | `event.log` | custom | `resonance_start/end`, `duration_s` |

### Control Parameters
| Param | Default | Range | Notes |
|------|---------|-------|------|
| `ρ_threshold` | 0.85 | 0.75–0.95 | Resonance entry |
| `window_s` | 6 | 4–10 | Minimum stability to enter |
| `max_resonance_s` | 45 | 15–120 | Safety upper bound |

### Monitor (pseudo)
```python
if coherence >= ρ_threshold for >= window_s:
    enter_resonance()
# Exit
if topic_shift or drift_signal or t_in_state > max_resonance_s:
    exit_resonance()
```

### Metrics
- Resonance duration, coherence gain, drift probability during resonance.

### Failure Modes
- Unnatural mirroring (“mocking”), stagnation without progress.

---

## Cross-Operator Notes

1. **Cancellability:** Any user input interrupts L₃ holds within `interrupt_window_ms` (≤50ms).  
2. **Loop Safety:** L₂ repair attempts are capped; exceeding emits `repair_failed`.  
3. **Schema Consistency:** Log keys follow `duration_ms` for latency; support backward-compat (`latency_ms` → mapped).  
4. **Privacy:** Use pseudonymous `session_id`; avoid PII in logs.  
5. **A/B Readiness:** Expose thresholds as remotely configurable for experiments.

---

## Minimal Conformance Checklist

- [ ] L₂ caps repair attempts at `max_repair_attempts` (default 2).  
- [ ] L₃ logs `latency_hold` with `duration_ms` and `reason`.  
- [ ] L₁ boundaries produce measurable deltas (pause/topic) with precision/recall tracking.  
- [ ] L₅ only enters when `coherence ≥ ρ_threshold` for `window_s`.  
- [ ] All state transitions emit schema-compliant log events.

---

> “Operators are levers on time; measurement is how we feel their weight.”  
> — *Phase Loop Dynamics, 2025*
