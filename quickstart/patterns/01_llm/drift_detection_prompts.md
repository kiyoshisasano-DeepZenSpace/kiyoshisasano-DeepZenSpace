# Drift Detection Prompt Library  
*(PLD Applied — LLM Pattern Edition v1.1 Canonical Schema)*

This file defines **internal reasoning scaffolds** for LLM-driven drift detection.  
These prompts are **not user-facing responses** — they run inside the reasoning pipeline before output generation.

Drift detection informs whether to:

- apply Soft Repair,
- request clarification,
- trigger reentry checkpoints, or
- escalate to `R5_hard_reset` (only if unrecoverable).

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
  "confidence": <0.0-1.0>,
  "evidence": "<short justification>"
}
```

---

## 🧪 Drift Detection Templates (By Canonical Category)

### **1. `D5_information`**

Trigger when the candidate response contradicts verified knowledge.

```
Check whether the response conflicts with verified memory or tool output.
If contradiction exists, classify as D5_information and include the conflicting evidence.
```

---

### **2. `D2_context`**  
(*Former: Drift-Constraint + Drift-Memory*)

```
Verify that the response respects stored constraints (budget, preference, policy)
and includes required context.
If constraint violations or context loss occur → classify as D2_context.
```

---

### **3. `D1_instruction`**

Detect replacement or loss of the user's objective.

```
Compare task intent with the candidate response.
If the intended goal is ignored, replaced, or altered → classify as D1_instruction.
```

---

### **4. `D3_flow`**

Identify sequencing or workflow misalignment.

```
Compare expected workflow step with the output.
If the model jumps ahead, repeats steps, or disrupts pacing → classify as D3_flow.
```

---

## 📊 Output Format (Schema-Aligned)

This format is intentionally simple — the detection stage will convert it to full telemetry format.

```json
{
  "drift_detected": true,
  "pld_code": "D2_context",
  "confidence": 0.91,
  "evidence": "Budget limit $100 was violated with a $240 option."
}
```

---

## 🧠 Lightweight Variant (Latency-Optimized)

Use when running under streaming or high-latency inference constraints:

```
Check contradiction, constraint violation, or topic shift.
If any condition is true → drift = yes.
Else → no drift.
```

---

## ❌ Anti-Patterns

| Avoid | Reason |
|---|---|
| Detecting drift **after** user-visible response | Repair must precede output |
| Treating all drift as **critical** | Causes unnecessary resets |
| Logging without canonical codes | Breaks analytics + evaluation |
| Apologetic or meta reasoning | Weakens confidence signals |

---

## ✔ Sanity Test

### Input  
User: “Budget under $100.”  
Candidate response: “A great $240 hotel is available.”

### Expected internal detection

```json
{
  "drift_detected": true,
  "pld_code": "D2_context",
  "confidence": 0.91,
  "evidence": "Response violates budget constraint ($100)."
}
```

---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025 — v1.1 Canonical Codes**

