# 01 — PLD Applied Interaction Report Summary  
Dataset: MultiWOZ 2.4 (N=200)

Version: 1.0  
Maintainer: **Kiyoshi Sasano**

---

## 1. Purpose

This report summarizes interaction stability, failure types, and repair behavior observed in **200 task-oriented dialogues.**  
All annotations follow the **PLD Applied Standard**:

```
Drift → Repair → Reentry → Resonance → Outcome
( D*    R*       RE*      resonance:true/false   OUT* )
```

The report is designed for:

- LLM agent engineers  
- Tool-using orchestration developers  
- Runtime supervisors and evaluation pipeline designers  

---

## 2. Key Metrics (N=200)

| Metric | Value | Engineering Meaning |
|--------|-------|---------------------|
| **Total Drift Events (D*)** | 312 | Drift events appear frequently and accumulate if untreated. |
| **Avg Drift per Dialogue** | 1.56 | Most dialogues contain ≥1 stability break. |
| **Top Drift Type** | `D2_information` | Tool/DB contradictions and incorrect assumptions dominate. |
| **Soft Repair Rate (R1/R2)** | 62% dialogues | Effective but inconsistently timed. |
| **Hard Repair Rate (R5)** | 10% dialogues | Mostly used after late or failed soft repairs. |
| **Outcome: OUT1_Complete** | 75% | Majority succeed, but trust and pacing vary. |
| **Outcome: OUT2_Partial** | 14% | Task partially recovered but not fully resolved. |

---

## 3. System Behavior Patterns

### 3.1 Drift (D*)

The most frequent pattern is:

```
D2_information  → D3_context_compounding → R5_hard_repair
```

Typical trigger scenarios:

- `"No result"` followed by later contradiction  
- Incorrect assumptions about available slots  
- Overconfidence after failed tool calls or latency delay  

Result:

> High risk of compounding divergence → user mistrust → forced reset.

---

### 3.2 Repair (R*)

**Soft Repair (R1/R2/R3)** is highly correlated with successful outcomes — **when triggered early.**  
However, most repairs occur *after* drift escalates.

Conversely:

- **R5_Hard Repair** works when context corruption is real  
- But ~35% were **premature**, indicating missing guard logic

---

### 3.3 Reentry (RE*)

Successful reentry events consistently included:

- Explicit acknowledgment of mistake  
- A corrected alternative  
- A short confirming question

Example effective pattern:

```
R2_soft → RE3_auto → resonance:true (2 turns later)
```

Failing cases often skipped acknowledgment and continued generating responses as if aligned.

---

## 4. Engineering Insights

| Insight | Meaning for Production Systems |
|--------|--------------------------------|
| **The Information Drift Trap dominates** | Prevent contradictions after “no result.” |
| **Soft Repair is under-used early** | Add timing triggers, not just conditional logic. |
| **Hard Repair misuse indicates missing gating logic** | Condition evaluation must differentiate recoverable vs unrecoverable drift. |

---

## 5. Recommendations

| Priority | Action | Expected Impact |
|----------|--------|----------------|
| **P1** | Mandatory soft repair on tool/DB failure | Prevents 30–40% escalation cases |
| **P2** | Insert checkpoint confirmation before slot-dependent execution | Reduces misalignment by early constraint grounding |
| **P3** | Require post-repair reconfirmation phrase | Enables consistent reentry pattern |

Example required phrasing:

> _“To confirm, we are still working on **{goal}** with constraints **{x/y/z}**, correct?”_

---

## 6. Provenance

```
metrics/multiwoz_2.4_n200/
  ├── 01_pld_applied_report_summary.md  ← (this file)
  ├── 02_results_summary.md
  ├── 03_casebook.md
  └── 04_casebook_unified.md
```

This report references:

- `/docs/03_pld_event_schema.md`  
- `/docs/04_pld_labeling_prompt_llm.md`  
- `/docs/06_pld_concept_reference_map.md`

---

Maintainer: **Kiyoshi Sasano**