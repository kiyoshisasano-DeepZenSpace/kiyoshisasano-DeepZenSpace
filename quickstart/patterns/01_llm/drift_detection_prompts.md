# Drift Detection Prompt Library  
*(PLD Applied — LLM Pattern Edition)*

This file provides prompt-level patterns for detecting conversational drift
before it escalates into repair, reset, or failure.

These prompts are **not responses to the user** —  
they are **internal reasoning scaffolds** used by the agent during generation.

Drift detection occurs *before* output formulation and informs:

- whether Soft Repair is needed,
- whether context is still aligned,
- whether the user's goal remains intact,
- whether memory or constraint validation is required.

---

## 🧩 Core Detection Logic (Baseline Pattern)

Use this structure internally each turn:

> **“Compare: user intent → stored context → planned response.
> If misalignment exists, label drift type and confidence.”**

Internal reasoning format (not user-visible):

```
SYSTEM CHECK:
- Current user goal: {{goal}}
- Stored constraints: {{constraints}}
- Previous validated facts: {{facts}}
- My next candidate response: {{draft_response}}

DRIFT ASSESSMENT:
- Does the draft response contradict previous facts? (yes/no → example)
- Does it violate constraints? (yes/no → example)
- Does it ignore or replace the user’s stated goal? (yes/no → example)
- Did the topic shift unexpectedly? (yes/no → example)

OUTPUT:
{ "drift_detected": true/false,
  "type": "<type or null>",
  "confidence": 0.0–1.0,
  "notes": "<brief justification>" }
```

---

## 🧪 Drift Detection Templates (By Category)

### 1. **Drift-Information**

Trigger when facts contradict prior validated evidence.

```
Evaluate whether the candidate response contradicts verified tool or memory data.
If contradiction exists, label as Drift-Information and provide short evidence.
```


### 2. **Drift-Constraint**

Trigger when output violates user-specified limits.

```
Check if the candidate response respects all active constraints
(e.g., budget, price, dates, preferences).
If any conflict exists, classify as Drift-Constraint.
```


### 3. **Drift-Intent**

Detect when the system switches topics or goal unintentionally.

```
Compare the intended task with the candidate response.
If the task goal is missing or replaced, classify as Drift-Intent.
```


### 4. **Drift-Memory**

Detect forgotten or overwritten information.

```
Verify candidate response includes required known context.
If previously confirmed details are missing or contradicted,
flag as Drift-Memory.
```


### 5. **Drift-Procedural**

Use when workflow steps are skipped or altered.

```
Compare current step to expected workflow sequence.
If the output jumps ahead, repeats, or skips steps,
mark as Drift-Procedural.
```

---

## 📊 Output Format (LLM-Readable Schema)

Always emit drift detection first (in hidden reasoning), then generate the user response normally.

```
{
  "turn_id": "{{turn}}",
  "drift_detected": true/false,
  "drift_type": "<type or null>",
  "confidence": 0.0–1.0,
  "evidence": "<1 sentence summary>"
}
```

---

## 🧠 Lightweight (Fast Inference) Variant

For latency-sensitive models:

```
Check for: contradiction, constraint violation, topic shift.
If any are true → drift = yes.
Else → no drift.
```

---

## ❌ Anti-Patterns

| Pattern to Avoid | Why |
|------------------|-----|
| Detecting drift after response is sent | Drift must precede repair |
| Treating every mismatch as critical | Causes unnecessary resets |
| Hiding drift state from telemetry | Breaks evaluation & reproducibility |
| Adding apologies in reasoning output | Weakens conversational stability |

---

## ✔ Quick Sanity Test

**Input:**  
User: “Budget is under $100.”  
Draft response: “A great $240 hotel is available.”

**Expected detection result:**

```
{ "drift_detected": true,
  "drift_type": "Drift-Constraint",
  "confidence": 0.91 }
```

---

Maintainer: **Kiyoshi Sasano**  
Version: **PLD Applied 2025**