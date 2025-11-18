# Drift Detection Prompt Library  
*(PLD Applied — LLM Pattern Edition · v1.1 Canonical Schema)*

This file defines **internal reasoning scaffolds** for LLM-driven drift detection.  
These prompts are **not user-visible outputs** — they operate inside the reasoning layer before response generation.

Drift detection determines whether to:

- apply a soft repair strategy,
- request clarification from the user,
- trigger a reentry checkpoint, or
- escalate to `R5_hard_reset` when the runtime cannot recover alignment.

---

## 🧩 Core Detection Logic (Canonical)

Internal reasoning procedure executed on every turn:

> **Compare the user goal, verified context, and planned response.  
> If misalignment exists, classify the drift using canonical PLD codes and assign confidence.**

Reasoning scaffold:

```
SYSTEM CHECK:
- User goal: {{goal}}
- Active constraints: {{constraints}}
- Verified facts: {{facts}}
- Candidate response: {{draft_response}}

DRIFT ASSESSMENT:
- Evidence contradiction? (include specific example if yes)
- Constraint violated? (budget, rules, policy, or user preference)
- Intent missing, altered, or replaced?
- Unexpected workflow jump, regression, or off-topic shift?

OUTPUT (for internal use only):
{
"drift_detected": true/false,
"pld_code": "<canonical_code_or_null>",
"confidence": <0.0-1.0>,
"evidence": "<brief justification>"
}
```

---

## 🧪 Canonical Drift Detection Templates

### **1. `D5_information` — Factual or Retrieval Contradiction**

Trigger when the response conflicts with verified memory, retrieval output, or external factual grounding.


```
Check whether the response contradicts validated information.
If contradiction exists → classify as D5_information and reference evidence.
```

---

### **2. `D2_context` — Missing or Violated Context**

*(Supersedes: Drift-Constraint / Drift-Memory)*

```
Verify adherence to stored constraints (budget, policy, preferences) and required context.
If context loss or constraint violation is detected → classify as D2_context.
```

---

### **3. `D1_instruction`**

Detect replacement or loss of the user's objective.

```
Compare the user’s explicit intent with the candidate response.
If the original task is ignored, substituted, or misinterpreted → classify as D1_instruction.
```

---

### **4. `D3_flow`**

Identify sequencing or workflow misalignment.

```
Check whether the response aligns with the expected workflow stage.
If steps are skipped, repeated, or pacing breaks occur → classify as D3_flow.
```

---

## 📊 Output Format (Schema-Aligned)

This format intentionally mirrors the minimal structure prior to full telemetry logging defined in  
`quickstart/metrics/schemas/pld_event.schema.json`.

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


pgsql```
Check: contradiction, constraint violation, or topic shift.
If any condition is true → drift = yes.
Else → drift = no.

```

---

## ❌ Anti-Patterns

| Avoid                                            | Why                                           |
| ------------------------------------------------ | --------------------------------------------- |
| Detecting drift **after** a user-visible message | Repair must occur before output               |
| Treating all drift as **critical**               | Causes unnecessary resets and user fatigue    |
| Logging without PLD taxonomy codes               | Breaks consistency, analytics, and evaluation |
| Apologetic meta-reasoning                        | Weakens execution authority and clarity       |

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


