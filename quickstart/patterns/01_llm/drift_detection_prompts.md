# Drift Detection Prompt Library  
*(PLD Applied — LLM Pattern Edition v1.1 Canonical Schema)*

This file defines **internal reasoning scaffolds** for LLM-driven drift detection.  
These prompts are **not user-facing responses** — they run inside the reasoning pipeline before output generation.

Drift detection informs whether to:

- apply Soft Repair,
- request clarification,
- trigger reentry checkpoints, or
- escalate to R5_hard_reset (only if unrecoverable).

---

## 🧩 Core Detection Logic (Canonical Pattern)

Internal reasoning procedure (executed each turn):

> **Compare: user intent → verified context → candidate response.  
> If misalignment exists, classify drift using canonical codes and confidence.**

Reasoning template:

```
SYSTEM CHECK:
- User goal: {{goal}}
- Active constraints: {{constraints}}
- Verified facts: {{facts}}
- Candidate response: {{draft_response}}

DRIFT ASSESSMENT:
- Contradiction with evidence? (example if yes)
- Constraint violated? (example if yes)
- Intent missing or replaced? (example if yes)
- Unexpected topic or workflow shift? (example if yes)

OUTPUT (for system use only):
{
"drift_detected": true/false,
"pld_code": "<canonical_code_or_null>",
"confidence": 0.0-1.0,
"evidence": "<short justification>"
}

---

## 🧪 Drift Detection Templates (By Canonical Category)

### **1. D5_information**

Trigger when the candidate response contradicts verified knowledge.

```
Check whether the response conflicts with verified memory or tool output.
If contradiction exists, classify as D5_information and include the conflicting evidence.
```

### **2. D2_context**

Covers former Drift-Constraint and Drift-Memory.

```
Verify that the response respects stored constraints (budget, preference, policy)
and includes required context.
If constraint violations or context loss occur → classify as D2_context.
```



### **3. D1_instruction**

Detects replacement or loss of the user's objective.

```
Compare task intent with the candidate response.
If the intended goal is ignored, replaced, or altered → classify as D1_instruction.
```



### **4. D3_flow**

Used when workflow order, pacing, or interaction cadence breaks.

```
Compare expected step or timing with the output.
If the model jumps ahead, repeats steps, or creates rhythm disruption → classify as D3_flow.
```



---

## 📊 Output Format (Schema-Aligned)

This format is intentionally simple because the detector node will convert it into a full PLD event log.

```
{
"drift_detected": true/false,
"pld_code": "<canonical_code_or_null>",
"confidence": 0.0-1.0,
"evidence": "<one sentence justification>"
}
```


Examples:

❌ Old format (deprecated):

```json
{ "drift_detected": true, "drift_type": "Drift-Constraint" }
```

✅ Correct (canonical-compliant):
{
  "drift_detected": true,
  "pld_code": "D2_context",
  "confidence": 0.91,
  "evidence": "Budget limit $100 was violated by proposing a $240 option."
}

---

## 🧠 Lightweight Variant (Latency-Optimized)
Use when running under streaming or high-efficiency inference constraints:
```sql
Check contradiction, constraint violation, or topic shift.
If any are true → classify drift.
Else → no drift.
```

---

## ❌ Anti-Patterns

| Avoid                                 | Reason                                             |
| ------------------------------------- | -------------------------------------------------- |
| Detecting drift **after user output** | Repair must precede user-visible response          |
| Treating all drift as critical        | Causes unnecessary resets (violates PLD lifecycle) |
| Logging without canonical codes       | Breaks analytics + evaluation comparability        |
| Injecting apologetic reasoning        | Weakens confidence signals                         |

---

## ✔ Sanity Test

### Input:
User: “Budget under $100.”
Candidate response: “A great $240 hotel is available.”

### Expected internal detection:

```bash
{
  "drift_detected": true,
  "pld_code": "D2_context",
  "confidence": 0.91,
  "evidence": "Output violates user constraint: $100 budget."
}
```

---

Maintainer: Kiyoshi Sasano
Version: PLD Applied 2025 v1.1
