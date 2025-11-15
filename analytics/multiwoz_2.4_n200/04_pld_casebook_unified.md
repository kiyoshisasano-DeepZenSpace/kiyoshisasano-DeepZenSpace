# PLD Casebook — Unified Engineering Template  
Dataset: MultiWOZ 2.4 (N=200)  
Version: 1.0  
Maintainer: Kiyoshi Sasano  

---

## 1. Purpose

This document provides a **standardized case structure** for evaluating multi-turn agent behavior.

⚠️ **Important:**
- This is a **documentation template**, not a code implementation standard
- YAML/JSON snippets are **examples only** - your implementation may differ
- PLD is a runtime governance pattern; this template helps you record behavioral observations

The template enables:
- Consistent failure pattern documentation across teams
- Machine-readable event logging for observability
- Actionable engineering insights

The evaluation pipeline follows the PLD operational cycle:

**Drift → Repair → Reentry → Outcome → Root Cause → Engineering Rule**

---

## 2. Case Template (Copy-Paste Format)

Use the following structure verbatim when documenting new cases:

```
CASE ID:
PATTERN CLASSIFICATION:
OUTCOME:

SCENARIO
<one concise sentence>

DRIFT SEQUENCE  
Step | Drift Code | Description

REPAIR ACTIONS  
Repair Code | Applied? | Notes

REENTRY  
Reentry Code | Status | Signal Type

OUTCOME CLASSIFICATION  
COMPLETE / PARTIAL / FAIL

ROOT CAUSE PATTERN  
<one sentence>

ENGINEERING RECOMMENDATION  
<operational rule or guardrail>

OPTIONAL: MACHINE RULE SNIPPET (JSON or YAML)
```

---

## 3. Applied Examples (5 Cases)

The following are canonical MultiWOZ examples rewritten using the unified structure.

---

### **Case 01 — D1R1-01**  
Pattern: **D1 → R1 → RE3**  
Outcome: **COMPLETE**

1) **SCENARIO**  
A slow system response creates hesitation and perceived breakdown.

2) **DRIFT SEQUENCE**  

Step | Drift Code | Description  
-----|------------|------------  
1    | D1         | Latency exceeds expected threshold (4.5s) with no placeholder  

3) **REPAIR ACTIONS**

Repair Code | Applied? | Notes  
------------|----------|------  
R1          | yes      | Sends filler message: “Still checking…”  

4) **REENTRY**

Reentry Code | Status | Signal Type  
-------------|--------|------------  
RE3          | yes    | Automatic continuation  

5) **OUTCOME**  
COMPLETE  

6) **ROOT CAUSE PATTERN**  
Missing latency pacing guard.

7) **ENGINEERING RECOMMENDATION**  
Always display a placeholder if response time exceeds 2–2.5 seconds.

8) **MACHINE RULE (YAML Example)**

```yaml
latency_guard:
  threshold_seconds: 2.2
  placeholder: "Still checking — one moment..."
```

---

### **Case 02 — D2R2-01**  
Pattern: **D2 → R2 → RE1**  
Outcome: **COMPLETE**

**SCENARIO**  
The system proposes results outside the user’s stated price constraint.

#### DRIFT SEQUENCE

Step | Drift Code | Description  
-----|------------|------------  
1    | D2         | Price constraint not persisted across turns  

#### REPAIR ACTIONS

Repair Code | Applied? | Notes  
------------|----------|------  
R2          | yes      | Generates corrected list filtered by constraint  

#### REENTRY

Reentry Code | Status | Signal Type  
-------------|--------|------------  
RE1          | yes    | User-initiated clarification  

#### OUTCOME  
COMPLETE  

#### ROOT CAUSE PATTERN  
Constraint loss across turns.

#### ENGINEERING RECOMMENDATION  
Surface key active constraints every 3–4 turns (price, dates, location).

---

### **Case 03 — D3R3-01**  
Pattern: **D3 → R3 → RE2**  
Outcome: **PARTIAL**

**SCENARIO**  
The system contradicts an earlier claim ("no availability" vs. "3 rooms available").

#### DRIFT SEQUENCE  
Step | Drift Code | Description  
-----|------------|------------  
1    | D3         | Internal contradiction between system responses  

#### REPAIR ACTIONS  
Repair Code | Applied? | Notes  
------------|----------|------  
R3          | yes      | Attempts self-correction after updated tool output  

#### REENTRY  
Reentry Code | Status | Signal Type  
-------------|--------|------------  
RE2          | yes    | System acknowledges error and re-anchors task  

#### OUTCOME  
PARTIAL — task proceeds, but trust degradation occurs.

#### ROOT CAUSE PATTERN  
Silent contradiction before acknowledgment.

#### ENGINEERING RECOMMENDATION  
Always explicitly acknowledge contradiction before correction.

---

### **Case 04 — D5R1R4-01**  
Pattern: **D5 → R1 → R4**  
Outcome: **FAIL**

**SCENARIO**  
System first claims “no matching results,” then later provides valid results.

#### DRIFT SEQUENCE  
Step | Drift Code | Description  
-----|------------|------------  
1    | D5         | False negative treated as final output  
2    | D5         | Later tool call reveals contradiction  

#### REPAIR ACTIONS  

Repair Code | Applied? | Notes  
------------|----------|------  
R1          | yes      | Suggests irrelevant alternatives  
R4          | yes      | Hard reset  

#### REENTRY  
Reentry Code | Status | Signal Type  
-------------|--------|------------  
—           | no     | No reentry attempt  

#### OUTCOME  
FAIL — user abandons interaction.

#### ROOT CAUSE PATTERN  
The Information-Drift Trap triggered premature certainty.

#### ENGINEERING RECOMMENDATION  
Ban plain “no result.” Fallback to constraint relaxation or clarification request.

#### Example Implementation Snippet (YAML)

```yaml
no_result_policy:
  allow_empty_response: false
  fallback: soft_constraint_relaxation
```

---

### **Case 05 — D4R1-01**  
Pattern: **D4 → R1 → RE3**  
Outcome: **COMPLETE**

**SCENARIO**  
A tool response is misinterpreted due to schema mismatch.

#### DRIFT SEQUENCE  
Step | Drift Code | Description  
-----|------------|------------  
1    | D4         | Tool/action drift from incorrect schema assumption  

#### REPAIR ACTIONS  
Repair Code | Applied? | Notes  
------------|----------|------  
R1          | yes      | Retry with corrected key mapping  

#### REENTRY  
Reentry Code | Status | Signal Type  
-------------|--------|------------  
RE3          | yes    | System stabilizes automatically  

#### OUTCOME  
COMPLETE — user unaware of underlying failure.

#### ROOT CAUSE PATTERN  
Schema mismatch unchecked prior to parsing.

#### ENGINEERING RECOMMENDATION  
Validate schema before executing or parsing tool responses.

---

## 4. Recommended Usage

Use Case | Recommended  
---------|------------  
Dataset Benchmarking | ✔  
Synthetic Training | ✔  
Evaluation | ✔  
Policy + Prompt Debugging | ✔  
Academic Use | ⚠ requires context  

---

## 5. File Location

```
metrics/multiwoz_2.4_n200/04_pld_casebook_unified.md
```


Maintainer: **Kiyoshi Sasano**
