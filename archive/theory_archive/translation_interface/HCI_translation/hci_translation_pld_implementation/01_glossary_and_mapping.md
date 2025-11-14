# PLD → HCI Glossary and Mapping Guide  
**Folder:** `06_translation_interface/HCI_translation/hci_translation_pld_implementation/`  
**Version:** 1.0 • Last updated: 2025-10-13  
**License:** CC BY-NC 4.0  
**Maintainer:** Phase Loop Dynamics Research Group  

---

## 1. Purpose and Scope

This glossary defines how **Phase Loop Dynamics (PLD)** concepts translate into **HCI implementation constructs**.  
It establishes a consistent vocabulary between theoretical operators (L₁–L₅) and applied interaction systems, ensuring each phase and event type can be implemented, instrumented, and measured in computational terms.

The goal is not conceptual equivalence but **functional interoperability** — i.e., allowing PLD-based interaction models to be executed in real-time user interfaces, adaptive feedback systems, or conversational agents.

---

## 2. Core Term Mapping

| PLD Concept | HCI Implementation Term | Operational Context | Detectable Signal | Control Parameters |
|--------------|--------------------------|---------------------|-------------------|--------------------|
| **Drift (𝒟)** | Interaction deviation event | When user behavior diverges from the predicted or guided path | Idle time, low NLU confidence, premature exit | `θ_drift`, `silence_ms`, `confidence_min` |
| **Repair (ℛ)** | Adaptive recovery sequence | System-initiated clarification or correction to restore context | Repair prompt, fallback action, or redirect | `λ_repair_gain`, `max_repair_attempts` |
| **Reentry** | Contextual return after drift | User resumes task or interaction after dropout | Session resume, click-back, reengagement intent | `reentry_lag`, `reentry_window_s` |
| **Resonance (𝓡₅)** | Alignment stability loop | Sustained synchronization of rhythm and timing between user and system | Low drift rate, stable pacing, echo alignment | `τ_resonance`, `phase_sync_threshold` |
| **Latency (𝓛₃)** | Intentional pacing delay | Temporally modulated pause between system outputs to maintain rhythm | Controlled wait or animation hold | `τ_latency`, `σ_phase_dev`, `hold_reason` |
| **Feedback Reflex (𝓛₄)** | Rapid bidirectional correction | Instant micro-adjustment to user reaction | Immediate UI or language feedback | `t_reflex_ms`, `response_gain` |

---

## 3. Interaction Phase Descriptors

Each PLD phase is modeled as a **temporal state** in the HCI event machine.  
Transitions occur through **event-driven triggers** measured in timing, attention, or semantic drift metrics.

| Phase | Entry Condition | Exit Condition | Typical System Action | HCI Metric |
|--------|----------------|----------------|-----------------------|-------------|
| **Drift Phase** | Input silence > θ or intent confidence < 0.5 | Repair triggered or user resumes | Log `drift_detected` event | Drift frequency, mean silence |
| **Repair Phase** | Drift detected within active session | Repair success or timeout | Send clarification prompt | Drift-to-repair ratio (DRR) |
| **Latency Phase** | Soft hold triggered by system pacing controller | Timer expires or user cancels | Display visual delay or ellipsis | Mean latency hold (MLH) |
| **Resonance Phase** | Stable rhythm alignment detected | Context switch or drift onset | Sustain tempo alignment | Resonance duration |
| **Reentry Phase** | User reengages with prior context | Task completion or next drift | Load saved state, resume interaction | Reentry success rate |

---

## 4. Safe Usage Tiers (Temporal Control Levels)

| Tier | Description | Allowed Control Operations | Timing Responsibility | Risk Level |
|------|--------------|-----------------------------|-----------------------|-------------|
| **T₀ — Passive Observation** | System measures drift without altering behavior | `log_event()` only | None | Minimal |
| **T₁ — Interactive Correction** | User-triggered repair via prompt or hint | `trigger_repair()` | Shared | Low |
| **T₂ — Adaptive Timing Control** | System adjusts latency or rhythm adaptively | `set_latency(τ)`; `adjust_gain(λ)` | System-led | Moderate |
| **T₃ — Autonomic Modulation** | Self-adjusting rhythm and pacing with predictive drift suppression | `auto_sync(phase)` | System-led with audit logging | Elevated |

All PLD-based adaptive systems must **declare their active tier** in deployment manifests (`pld_mode: T1–T3`) to ensure ethical transparency and reproducibility.

---

## 5. Implementation Syntax Conventions

| Symbol | Implementation Name | Description |
|---------|--------------------|--------------|
| `σ` | `phase_state` | Encoded state of the temporal phase machine |
| `τ` | `latency_ms` | Time delay in milliseconds introduced by system pacing |
| `λ` | `repair_gain` | Proportional weight applied to correction intensity |
| `θ` | `drift_threshold` | Condition boundary for drift detection |
| `ρ` | `resonance_strength` | Real-time coherence index |
| `𝒟` | `detect_drift()` | Drift detection function (phase deviation trigger) |
| `ℛ` | `repair()` | Repair initiation and execution function |
| `φ(τ)` | `hold_kernel(τ)` | Latency kernel shaping function (Gaussian preferred) |

---

## 6. Event Type Alignment (Telemetry Contract)

| PLD Event | HCI Log Event | Required Metadata Fields | Notes |
|------------|----------------|---------------------------|--------|
| **Drift Detected** | `drift_detected` | `session_id`, `timestamp`, `confidence_score`, `ui_state` | Passive or adaptive mode |
| **Repair Triggered** | `repair_triggered` | `strategy`, `latency_before_repair`, `context_id` | Marks soft or hard correction |
| **Repair Failed** | `repair_failed` | `failed_attempts`, `context_id` | Escalation path candidate |
| **Reentry Success** | `reentry_success` | `reentry_lag`, `previous_context_id` | Confirms successful reengagement |
| **Latency Hold** | `latency_hold` | `duration_ms`, `reason` | Required for all intentional pauses |

---

## 7. Timing and Control Parameters (Empirical Defaults)

| Parameter | Description | Default | Range | Unit |
|------------|-------------|----------|--------|------|
| `θ_drift` | Minimum silence or inactivity before drift detection | 8 | 5–12 | s |
| `τ_latency` | Base latency for pacing hold | 900 | 600–1500 | ms |
| `λ_repair_gain` | Repair adjustment coefficient | 0.7 | 0.4–1.0 | — |
| `ρ_resonance_threshold` | Coherence index for resonance detection | 0.85 | 0.75–0.95 | — |
| `max_repair_attempts` | Maximum soft repair retries before escalation | 2 | 1–3 | count |

---

## 8. Design Implications for HCI Systems

- Drift signals are **first-class interaction events**, not errors.  
- All pacing delays (`τ_latency`) must be **visible and explainable** to the user.  
- Adaptive systems operating in Tier ≥T₂ must include **latency transparency indicators** (e.g., progress shimmer, typing ellipsis).  
- Resonance phases can be leveraged for **personalized rhythm calibration** (e.g., matching speech tempo or click frequency).  
- Repair sequences should be **non-blocking** — the user must always retain control of reentry timing.

---

> “Terminology becomes technology when it controls timing.”  
> — *Phase Loop Dynamics, 2025*
