# Latency and Adaptive Timing (L₃) — Implementation Guide  
**Folder:** `06_translation_interface/HCI_translation/hci_translation_pld_implementation/`  
**Version:** 1.0 • Last updated: 2025-10-13  
**License:** CC BY-NC 4.0  
**Maintainer:** Phase Loop Dynamics Research Group

---

## 1) Purpose

This guide specifies **intentional latency control (L₃)** and **adaptive timing** strategies for PLD-based HCI systems.  
Scope: timing policies, control loops, personalization, interrupt rules, telemetry, and safety caps. LLMs must **only suggest** latency; the **UI/Orchestrator** executes real-time holds and logging.

---

## 2) Responsibilities and Contracts

- **Model/Policy (LLM or server)** → emits *hints* only:  
  `telemetry.suggest_latency_ms` and `telemetry.reason` (e.g., `soft_repair_probe`).  
- **UI/Orchestrator** → renders holds, enforces interrupts, logs `latency_hold` with `duration_ms` (see §7).  
- **Non-blocking contract** → any user action cancels the hold within **≤ 50 ms**.

**Hint contract (example):**
```json
{
  "action": "soft_repair",
  "message": "Just to confirm...",
  "telemetry": { "suggest_latency_ms": 900, "reason": "soft_repair_probe" }
}
```

---

## 3) Timing Policy Layers

| Layer | Goal | Inputs | Output |
|------|------|--------|--------|
| **L3.0 — Static Defaults** | Safe baseline pacing | domain defaults | τ := {600, 900, 1200, 1500} ms |
| **L3.1 — Contextual Heuristics** | Scene-specific τ | UI state, task complexity | τ := f(context) |
| **L3.2 — Personalized Baseline** | User-calibrated τ | user tempo (typing rate, pause hist) | τ := f(user) |
| **L3.3 — Adaptive Control** | Online optimization | success/error signals | τₜ₊₁ := g(τₜ, feedback) |

Recommended order of precedence: **L3.3 → L3.2 → L3.1 → L3.0** (fallback to safer, simpler rules when signal is weak).

---

## 4) Control Algorithms (choose per product maturity)

### 4.1 PID-style latency controller (fast, interpretable)
Adjust τ based on error between **target interaction tempo** and **observed tempo**.

- **State:** `τ` (ms)  
- **Error:** `e_t = tempo_target - tempo_observed` (Hz or s/turn)  
- **Update:** `τ_{t+1} = clamp(τ_t + Kp*e_t + Ki*Σe + Kd*(e_t - e_{t-1}))`

**Recommended bounds:** `τ ∈ [600, 1500] ms`; clamp every step.  
**Signals:** tempo from keypress cadence, response inter-onset intervals, or speech rate.

```python
def update_latency(tau, e_t, e_sum, e_prev, Kp=120, Ki=4, Kd=80):
    delta = Kp*e_t + Ki*e_sum + Kd*(e_t - e_prev)
    return max(600, min(1500, tau + delta))
```

### 4.2 Two-armed bandit (fast A/B between short/long)
Maintain short (`τ_s`) and long (`τ_l`) options; choose via ε-greedy on immediate utility (e.g., reentry success, dropout).

```python
def choose_tau(stats, eps=0.1):
    if random() < eps: arm = choice(['s','l'])
    else: arm = 's' if stats['s'].reward_mean >= stats['l'].reward_mean else 'l'
    return 900 if arm=='s' else 1200
```

### 4.3 Bayesian Thompson Sampling (robust exploration)
Model reward of candidate τ values (e.g., Beta or Gaussian). Draw samples and pick argmax. Suitable when utility signals are noisy.

### 4.4 Contextual bandit (feature-aware)
Features: `task_type`, `ui_state`, `user_segment`, `drift_type`. Output best τ for the current context. Start with LinUCB or logistic UCB.

> **Implementation note:** keep adaptation **stateless per session** unless user consent permits persistent personalization.

---

## 5) Personalization Signals (privacy-preserving)

- **Typing tempo**: median keypress interval; robust to outliers.  
- **Hesitation profile**: histogram of pauses per UI state.  
- **Interrupt rate**: % of holds canceled by user (→ shorten τ).  
- **Repair friction**: time-to-confirm in repair prompts (→ lengthen τ if rushed/overwhelmed).  
- **Modal preference**: mouse vs. keyboard vs. voice (affects visibility affordances).

**Baseline estimator (per session):**
```python
tau_base = quantile(user_pause_distribution, 0.6)  # middle-high comfort
tau_base = clamp(tau_base, 600, 1500)
```

---

## 6) Interrupt Rules (non-blocking by design)

- **Immediate cancel** on **keypress/click/speech onset**.  
- **Bypass rule:** if user issues a command during hold, **skip** repair UI and route to the user target.  
- **Graceful fallback:** if hold is canceled, log `latency_hold` with `user_cancelled=true`.  
- **Chaining ban:** avoid consecutive holds without user action in between (max 1 hold per 5 s unless repair is pending).

---

## 7) Telemetry Schema (logging requirements)

Emit `latency_hold` **every time** a UI hold is rendered.

```json
{
  "event_type": "latency_hold",
  "timestamp": "2025-10-13T12:00:00Z",
  "session_id": "S-12345",
  "metadata": {
    "duration_ms": 1200,
    "reason": "soft_repair_probe",
    "context_id": "frame:Form_Submitted",
    "user_cancelled": false
  }
}
```

**Key requirements:**
- `metadata.duration_ms` is **required** by policy (normalize legacy `latency_ms` → `duration_ms`).
- Log **interrupts** with `user_cancelled=true` to compute **latency_interrupt_rate**.
- Associate holds with **context IDs** for pathway analysis.

---

## 8) Safety & Fairness Limits

- **Upper cap:** `τ_max = 1500 ms` (unless accessibility settings justify longer).  
- **Lower cap:** `τ_min = 600 ms` (avoid clipped feedback perception).  
- **Session budget:** total hold time per minute ≤ **5 s** for Tier ≤ T₂.  
- **Tier transparency:** disclose active tier (T₀–T₃) and explain pacing intent in UI copy.  
- **A11y:** honor reduced-motion/system preferences; provide **Blank** variant (no animation).

---

## 9) Evaluation Metrics (bound to analytics)

- `avg_latency_hold`  
- `latency_interrupt_rate`  
- `time_to_repair` (drift → repair)  
- `reentry_success_rate`  
- `dropout_delta_with_latency` (A/B)  
- `per_user_tau_variance` (stability of personalization)

---

## 10) A/B and Calibration Playbook

1. **Start** with two τ buckets (900 vs. 1200 ms).  
2. **Measure** reentry success and interrupt rate for each bucket.  
3. **Calibrate** PID or bandit priors with early results.  
4. **Ramp** contextual/bandit models once confidence is established.  
5. **Audit** for subgroup fairness (e.g., input modality, language, accessibility settings).

---

## 11) Reference UI Pseudocode

```ts
async function renderLatencyHold(ms: number, ctx: Ctx) {
  const token = startCancellableTimer(ms);
  showShimmer(ctx.variant); // or ellipsis/blank
  const cancelled = await waitForEither(token, userInputEvent());
  if (cancelled) {
    log('latency_hold', { duration_ms: ms, reason: ctx.reason, context_id: ctx.id, user_cancelled: true });
    hideShimmer();
    return;
  }
  log('latency_hold', { duration_ms: ms, reason: ctx.reason, context_id: ctx.id, user_cancelled: false });
  hideShimmer();
  proceed();
}
```

---

## 12) Compliance Checklist

- [ ] LLM never sleeps; only suggests `suggest_latency_ms`.  
- [ ] UI cancels holds within **≤ 50 ms** on input.  
- [ ] `latency_hold` always logs `duration_ms` (+ `user_cancelled`).  
- [ ] τ stays within `[600, 1500]` ms unless A11y overrides are explicit.  
- [ ] No chained holds without user action between them.  
- [ ] Per-session personalization resets unless the user opts in for persistence.

---

> “Latency is a design instrument, not a side effect.”  
> — *Phase Loop Dynamics, 2025*
