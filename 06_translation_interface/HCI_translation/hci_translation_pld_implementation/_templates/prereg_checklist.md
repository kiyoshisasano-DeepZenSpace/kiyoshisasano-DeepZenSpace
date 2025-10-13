# Pre-Registration Checklist — PLD→HCI Study

**Version:** 1.0 • Last updated: 2025-10-13  
**Scope:** Pre-study registration of hypotheses, design, metrics, analysis plan, and safety for PLD-based temporal interaction experiments.

---

## 1) Study Overview
- [ ] **Title:** _e.g.,_ “Latency Holds Improve Reentry Success in PLD-guided Conversational UX”
- [ ] **PI / Team:** _Name(s), affiliation, contact_
- [ ] **Design Type:** Between-subjects / Within-subjects / Mixed
- [ ] **Registration Platform:** OSF / IRB ID / Internal registry link
- [ ] **Software Version / Build Hash:** _commit SHA_

---

## 2) Hypotheses (Directional & Specific)
- [ ] **H1:** Longer latency holds (τ = 1200 ms) increase **reentry_success_rate** vs. τ = 900 ms.
- [ ] **H2:** Adaptive timing (PID/bandit) reduces **latency_interrupt_rate** compared to static τ.
- [ ] **H3:** Sessions with resonance (ρ_tempo ≥ 0.7) show lower **drift_count** and higher task completion.

_Optional (exploratory):_
- [ ] Resonance duration predicts reentry lag deceleration.

---

## 3) Experimental Conditions
- [ ] **Factors:** τ ∈ {900, 1200}, Repair Strategy ∈ {soft, soft+reentry}, Personalization ∈ {off, on}
- [ ] **Randomization:** Method and seed
- [ ] **Counterbalancing / Block Order:** For within-subject design
- [ ] **Inclusion/Exclusion Criteria:** _e.g.,_ language proficiency, device type
- [ ] **Sample Size & Power:** target N, power analysis method
- [ ] **Stopping Rules:** sequential bound / max sessions / safety halt

---

## 4) Outcome Measures (Primary/Secondary)
**Primary Outcomes**
- [ ] **Reentry Success Rate** = reentry_success.count / attempts
- [ ] **Time to Repair** (s) = mean(Δt drift→repair)

**Secondary Outcomes**
- [ ] **Avg Latency Hold** (ms)
- [ ] **Latency Interrupt Rate**
- [ ] **Repair Loop Depth**
- [ ] **Task Completion (goal_completed)**

**Exploratory Signals**
- [ ] **Tempo Coherence (ρ_tempo)**
- [ ] **User-reported Rhythm Comfort** (Likert)

---

## 5) Telemetry & Data Integrity
- [ ] **Schema Compliance:** validate against `pld_event.schema.json`
- [ ] **Clock Sync:** server and client NTP checked (±10 ms)
- [ ] **Session IDs:** pseudonymized; no PII in metadata
- [ ] **Event Completeness:** 100% state transitions logged
- [ ] **Data Checks:** missingness thresholds, duplicate filtering
- [ ] **Storage:** encrypted at rest; access controls documented

---

## 6) Analysis Plan
- [ ] **Primary Tests:** logistic regression for reentry_success ~ τ + strategy + covariates
- [ ] **Mixed-Effects (if within-subject):** random intercepts for participant/session
- [ ] **Corrections:** multiple comparison control (e.g., Holm/Benjamini–Hochberg)
- [ ] **Effect Sizes:** OR, Cohen’s d where applicable
- [ ] **Robustness Checks:** sensitivity to drift thresholds; excluding outliers
- [ ] **Visualization:** pre-specified plots (reentry vs τ, latency vs interrupts)

**Model Specifications (examples)**
```text
Logit(reentry_success) ~ tau_ms + adaptive_on + repair_strategy + device_type + (1|participant_id)
OLS(time_to_repair_s) ~ tau_ms + drift_count + device_type + ui_state
```

---

## 7) Safety & Ethics
- [ ] **Repair Cap:** max 2 soft repairs per drift episode
- [ ] **Latency Bounds:** 600–1500 ms; cancel on user input (≤50 ms)
- [ ] **Consent & Debrief:** visible and plain-language
- [ ] **Accessibility:** honor reduced-motion; alternative cues (visual/audio/haptic)
- [ ] **Incident Handling:** loop oscillation → damping; escalation/handoff path
- [ ] **Privacy:** data minimization; retention policy documented

---

## 8) Blinding & Bias Control
- [ ] **Condition Blindness:** participants blind to τ condition where feasible
- [ ] **Analyst Blinding:** analysis scripts run with masked condition labels
- [ ] **Pre-specification:** no p-hacking; commit analysis notebook hash

---

## 9) Materials & Artifacts
- [ ] **Stimuli/UX Screens:** versioned assets link
- [ ] **Mermaid State Machine:** `_templates/state_machine_template.mmd`
- [ ] **Event Log Example:** `_templates/event_log_minimal.jsonl`
- [ ] **Experiment Sheet Template:** `_templates/experiment_sheet.csv`
- [ ] **Dashboard Config:** `30_metrics/dashboards/reentry_success_dashboard.json`

---

## 10) Deviations & Amendments
- [ ] **Change Log:** describe and timestamp any deviations from plan
- [ ] **Justification:** rationale and risk assessment
- [ ] **Approval:** reviewer sign-off

---

## 11) Sign-off
- [ ] **PI/Owner:** ______________________  **Date:** __________
- [ ] **Ethics Reviewer:** ________________  **Date:** __________
- [ ] **Data Steward:** ___________________  **Date:** __________

---

**License:** CC BY-NC 4.0 • **Maintainers:** PLD–HCI Implementation Working Group
