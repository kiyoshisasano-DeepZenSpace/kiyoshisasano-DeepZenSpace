# PLD Casebook — Applied Interaction Failures & Recoveries
Dataset: MultiWOZ 2.4 (N=200)  
Version: 1.0  
Maintainer: Kiyoshi Sasano  

---

## 📍 Purpose

This Casebook provides **representative examples of drift–repair–reentry patterns** observed in the evaluation dataset.  
Unlike narrative examples, these are structured for:

- engineering replication  
- repair policy tuning  
- agent behavior debugging  
- training set generation  

---

## 📊 Case Coverage Summary

| Pattern Type | Count | % of Sample |
|-------------|-------|-------------|
| D1 → R1 → RE3 → OUT-COMPLETE | 1 | 20% |
| D2 → R2 → RE1 → OUT-COMPLETE | 1 | 20% |
| D3 → R3 → RE2 → OUT-PARTIAL | 1 | 20% |
| D5 → R1 → R4 → OUT-FAIL | 1 | 20% |
| D4 → R1 → RE3 → OUT-COMPLETE | 1 | 20% |

Each case below follows the same applied engineering format.

---

## 🧪 Case 01 — `D1R1-01`  
**Pattern:** Latency Drift → Soft Repair → Automatic Reentry  
Outcome: **OUT-COMPLETE**

### 1. Scenario
User requests available hotels. System response latency exceeds threshold with no placeholder messaging.

### 2. Drift

| Code | Type | Trigger |
|------|------|---------|
| D1 | Latency Drift | Response delay > 4.5s, no pacing indicator |

### 3. Repair

| Code | Applied | Mechanism |
|------|---------|-----------|
| R1 | ✔ | Sends filler: "Still checking…" |

### 4. Reentry

| Code | Result | Notes |
|------|--------|-------|
| RE3 | ✔ | Flow naturally resumes without additional repair |

### 5. Outcome  
**COMPLETE — task finished normally.**

### 6. Engineering Lesson  
Implement latency-hold threshold:

```json
{
  "rule": "latency_guard",
  "threshold_seconds": 2.2,
  "fallback_message": "Working on it..."
}
```

---

## 🧪 Case 02 — `D2R2-01`  
**Pattern:** Context Drift → Options/Constraint Repair → User-Guided Reentry  
Outcome: **OUT-COMPLETE**

### 1. Scenario
System forgets previously stated price constraint.

### 2. Drift

| Code | Type | Details |
|------|------|---------|
| D2 | Context Drift | Suggests hotels > stated max price |

### 3. Repair

| Code | Applied | Notes |
|------|---------|-------|
| R2 | ✔ | Offers adjusted constraints + viable options |

### 4. Reentry

| Code | Result | Signal Type |
|------|--------|-------------|
| RE1 | ✔ | User explicitly restores constraint: "No, keep it under £60." |

### 5. Outcome
**COMPLETE — recovered successfully.**

### 6. Engineering Lesson
```
Rule: Confirm active slot constraints every 3–4 turns.
```

---

## 🧪 Case 03 — `D3R3-01`  
**Pattern:** Memory Drift → Local Self-Correction → System-Guided Reentry  
Outcome: **OUT-PARTIAL**

### 1. Scenario
System contradicts earlier statement about room availability.

### 2. Drift

| Code | Type | Details |
|------|------|---------|
| D3 | Memory Drift | "No rooms" → later "3 rooms available" |

### 3. Repair

| Code | Applied | Result |
|------|---------|--------|
| R3 | ✔ | System acknowledges contradiction and retries tool |

### 4. Reentry

| Code | Status |
|------|--------|
| RE2 | ✔ |

### 5. Outcome
**PARTIAL — user abandons due to trust loss.**

### 6. Engineering Lesson
```
Never correct silently — always acknowledge contradictions.
```

---

## 🧪 Case 04 — `D5R1R4-01`  
**Pattern:** Information Drift Trap → Soft Repair Attempt → Hard Reset  
Outcome: **OUT-FAIL**

### 1. Scenario
System asserts "no result" while results exist.

### 2. Drift

| Code | Type | Trigger |
|------|------|---------|
| D5 | Information Drift | False negative DB return |

### 3. Repair

| Stage | Code | Result |
|-------|------|--------|
| Attempt 1 | R1 | Offers irrelevant alternative |
| Final | R4 | Full reset triggered |

### 4. Reentry

| Code | Status |
|------|--------|
| — | ✘ No reentry |

### 5. Outcome
**FAIL — unrecoverable interaction failure.**

### 6. Engineering Lesson
```json
{
  "rule": "ban_no_result",
  "replacement": "soft_repair_options"
}
```

---

## 🧪 Case 05 — `D4R1-01`  
**Pattern:** Tool Drift → Clarification → Automatic Reentry  
Outcome: **OUT-COMPLETE**

### 1. Scenario
System misreads JSON format returned by tool.

### 2. Drift

| Code | Type | Details |
|------|------|---------|
| D4 | Tool/Action Drift | JSON schema mismatch |

### 3. Repair

| Code | Applied | Notes |
|------|---------|-------|
| R1 | ✔ | Retries with corrected key/value mapping |

### 4. Reentry

| Code | Status |
|------|--------|
| RE3 | ✔ Automatic |

### 5. Outcome
**COMPLETE — full recovery.**

---

## 🧩 Summary Table

| Case | Pattern | Reentry | Outcome |
|------|---------|---------|---------|
| 01 | D1 → R1 → RE3 | ✔ | COMPLETE |
| 02 | D2 → R2 → RE1 | ✔ | COMPLETE |
| 03 | D3 → R3 → RE2 | ✔ | PARTIAL |
| 04 | D5 → R1 → R4 | ✘ | FAIL |
| 05 | D4 → R1 → RE3 | ✔ | COMPLETE |

---

## 🏁 Document Role

This Casebook is intended for:

- failure benchmarking  
- repair policy refinement  
- synthetic evaluation dataset generation  
- drift-informed prompting and architecture design  

Use together with:

- `02_results_summary.md`  
- `04_pld_labeling_prompt_llm.md`  
- `pld_event_schema.json`  

Maintainer: **Kiyoshi Sasano**

