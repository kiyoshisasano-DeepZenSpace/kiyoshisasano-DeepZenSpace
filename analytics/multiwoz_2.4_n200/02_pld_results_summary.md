# 02 — PLD Applied Evaluation Results  
Dataset: MultiWOZ 2.4 (N=200)

Version: 1.0  
Maintainer: **Kiyoshi Sasano**

---

## 1. Evaluation Scope

This document provides quantitative results from applying the **PLD Applied Interaction Evaluation Standard** across **200 task-oriented dialogues**.

The measurements follow the defined event model:

```
Drift (D*) → Repair (R*) → Reentry (RE*) → Resonance → Outcome (OUT*)
```

This file is intended for:

- Runtime evaluation dashboards  
- Benchmark comparison  
- Failure pattern monitoring  
- CI-based conversational agent regression testing  

---

## 2. Global Distribution Metrics

| Metric Key | Metric | Value | Notes |
|-----------|--------|-------|-------|
| `global.dialogues_total` | Total Dialogues | 200 | Full dataset |
| `global.events_total` | Total Annotated Events | 1,142 | Includes D*, R*, RE*, OUT* |
| `global.drift_total` | Total Drift Events | **312** | High frequency indicator |
| `global.repair_total` | Total Repair Events | **241** | Includes soft + hard repair |
| `global.reentry_total` | Total Reentry Events | **119** | Signals recovery attempts |
| `global.resonance_success_rate` | Resonance Achieved | **41%** | After RE* step |
| `global.outcome_complete_rate` | OUT1_Complete | **75%** | Primary success measure |

---

## 3. Drift Distribution (D*)

| Drift Type | Code | Occurrence (%) | Notes |
|-----------|-------|----------------|-------|
| Information Drift | `D2_information` | **44%** | Tool/DB contradiction after earlier claim |
| Task Misalignment | `D1_task` | 22% | Wrong interpretation or implicit assumption |
| Procedural Drift | `D4_procedural` | 18% | Missing steps / incorrect sequencing |
| Latency-Induced Drift | `D5_latency` | 9% | Timing disruption (silence → hallucinated continuation) |
| Other/Unclassified | `D0_misc` | 7% | Requires schema extension |

**Operational interpretation:**  
> Drift is **not rare and typically recoverable**, but correction timing determines whether outcome remains stable.

---

## 4. Repair Effectiveness (R*)

| Repair Type | Code | Usage Rate | Effectiveness |
|-------------|------|------------|--------------|
| Clarification / Soft Repair | `R2_soft_clarify` | **38%** | High success when early |
| Grounding Correction | `R3_grounding_reset` | **17%** | Frequently fixes D2_information |
| Optioning / Constraint Relaxation | `R1_constraint_relief` | 7% | Works best with DB/tool failures |
| Hard Reset | `R5_reset_state` | **10%** | Necessary only when corruption persists |
| Micro Acknowledgment | `R4_acknowledge` | 20% | Smoother conversational flow, but weak alone |
| None Applied | — | **8%** | Often leads to OUT2 or OUT3 |

> The **timing** of repair mattered more than type:  
> Early R2/R3 prevented >50% escalation cases.

---

## 5. Reentry Success Rate (RE*)

| Metric | Value |
|--------|-------|
| Reentry Attempted | 119 cases |
| Reentry Success | **73 cases (61%)** |
| Reentry → Resonance Transition | **49 cases (41%)** |

Reentry success increased significantly when the agent used:

```
(1) Acknowledgment → (2) Corrected content → (3) Constraint reconfirmation question
```

---

## 6. Outcome Breakdown (OUT*)

| Outcome Type | Code | % | Meaning |
|--------------|------|----|--------|
| **Task Complete** | `OUT1_complete` | **75%** | Fully resolved, stable final state |
| Partial Success | `OUT2_partial` | 14% | Requirements met, but interaction unstable |
| User Exit / Abandonment | `OUT3_exit` | 7% | Negative experience or drift overload |
| System Fail / No Resolution | `OUT4_fail` | 4% | Terminal breakdown |

---

## 7. Correlation Highlights

| Pattern | Result |
|---------|--------|
| Early Soft Repair (R2) → OUT1 | **+28.4% improvement** |
| Tool error + no Soft Repair → OUT3/OUT4 | **4.6× more likely** |
| Reentry applied after R5 → Resonance | Rare (≈8%) |
| Latency Drift + no acknowledgment | High probability of hallucination continuation |

---

## 8. Operational Benchmarks (Recommended)

| Indicator | Target Threshold | Status (Dataset) |
|-----------|------------------|------------------|
| Drift per Dialogue | ≤ 1.0 | **1.56 ❌** |
| Soft Repair Responsiveness | ≥ 70% | **62% ⚠** |
| Reentry Enforcement | ≥ 85% when repair applied | **49% ❌** |
| Resonance Success Rate | ≥ 60% | **41% ❌** |
| OUT1_Complete | ≥ 80% | **75% ⚠** |

---

## 9. Reproducibility

Evaluation requires:

- `/docs/03_pld_event_schema.md`  
- `/docs/04_pld_labeling_prompt_llm.md`  
- `/metrics/.../pld_events_demo.jsonl` (optional tool input format)

---

## 10. Study Limitations

### Sample Size and Domain
- N=200 dialogues (task-oriented only)
- Single domain: MultiWOZ 2.4
- Language: English
- Context: Hotel/restaurant/train booking

### Generalization Constraints
⚠️ **These patterns may not generalize to:**
- Open-domain conversation
- Code generation agents
- Creative/subjective tasks
- Non-English languages

### Statistical Considerations
- Confidence intervals not computed (descriptive analysis)
- Correlation ≠ Causation
- Effect sizes are observational, not experimental

### Recommended Use
✅ Use this data to:
- Validate PLD methodology in similar domains
- Establish baseline behavioral metrics
- Guide implementation decisions

❌ Do not use to:
- Claim universal performance improvements
- Guarantee production outcomes
- Compare across fundamentally different domains

Maintainer: **Kiyoshi Sasano**

---
