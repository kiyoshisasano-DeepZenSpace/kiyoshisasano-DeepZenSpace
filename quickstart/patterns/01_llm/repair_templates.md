---
title: "Repair Template Library — PLD Runtime Edition"
version: 2025.1.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "patterns/llm"
tags:
  - PLD
  - repair actions
  - prompting
  - runtime alignment
---

# Repair Template Library  
_A standardized set of phrasing structures aligned with PLD runtime behavior._

Repairs exist to **correct drift without breaking task continuity.**  
This template library provides **predictable repair phrasing**, ensuring:

- smooth handoff between phases  
- consistent metric extraction  
- behavior alignment across models & orchestration frameworks  

These templates correspond to PLD repair classes:

| Repair Type | Code | Visibility | Use Case |
|-------------|------|------------|----------|
| Soft Repair — Clarification | `R1` | visible or silent | Missing parameters, misunderstood goal |
| Soft Repair — Constraint Confirmation | `R2` | visible | Conflicting or uncertain details |
| Soft Repair — Option Narrowing | `R3` | visible | Too many branching paths or ambiguity |
| Hard Repair — Reset/Checkpoint | `R9` | always visible | Unrecoverable task state |

> All repair text must be deterministic and machine-detectable.

---

## 1. Soft Repair — Clarification (`R1`)

Used when intent is partially understood but missing detail.

### Template (Visible)

```
I need one detail to continue:

❓ {question or missing parameter}

Once you confirm, I’ll proceed with the next step.
```

#### Micro-variants

| Tone | Example |
|------|--------|
| Light UX | `"Quick check — what size do you prefer?"` |
| Formal | `"Clarify the missing variable: {X}?"` |

### Silent Variant

```
(Silent: Apply safe default or inference)
```

Log as: `event_type = repair_triggered`, `tags = ["silent"]`.

---

## 2. Soft Repair — Constraint Confirmation (`R2`)

Use when the model detects conflicting constraints or ambiguous instructions.

### Standard Template

```
Before continuing, I need to confirm the constraints:

📌 Requirement: {restated_constraint}
📌 Context: {relevant_condition}

Please reply **Confirm** or provide an update.
```

#### Efficiency Variant (High-turn environments)

```
Confirm this constraint: {X}?  (yes/no)
```

---

## 3. Soft Repair — Option Narrowing (`R3`)

Use when the user intent is known but solution branching is wide.

### Template

```
Thanks — there are several possible options.

Which direction fits best?

1️⃣ {option A}  
2️⃣ {option B}  
3️⃣ {option C}  

Reply with the number or уточнしてください ("refine").
```

> This pattern reduces ambiguity and improves reentry stability.

---

## 4. Soft Repair — Misinterpretation Correction

(Used within D1–D3 drift when the model recognizes mistaken assumption.)

### Template

```
Correction applied — the correct interpretation is:

✔ {corrected understanding}

Continuing from there.
```

Optional trailing reassurance:

```
Let me know if you'd like to adjust it further.
```

---

## 5. Hard Repair — Alignment Reset (`R9`)

Triggered when **soft repair fails** or the task state becomes unrecoverable.

### Full Reset Template

```
Pausing to realign — the task state has become unclear.

Before continuing, please confirm:

🎯 Goal: {restated_goal}
📌 Constraints: {constraints_list}
🔄 Next step: {candidate_action}

Reply with **Confirm** or provide corrections.
```

### Emergency Variant  
(Use only when system stability requires immediate resolution.)

```
The workflow cannot continue as-is.  
I need a fresh alignment signal.

Please restate the goal and required constraints in one message.
```

---

## 6. Reentry Transition Phrase Library

Once the user confirms or the model auto-validates alignment, reenter execution using a consistent phrase.

| Variant | Example |
|---------|--------|
| Standard | `"Alignment confirmed — continuing."` |
| UX Smooth | `"Thanks — continuing now."` |
| Uncertain | `"Continuing, but I’ll recheck once the next step is complete."` |
| Tool-based | `"Acknowledged — resuming workflow execution."` |

> These are logged as `reentry_observed`.

---

## 7. Model Execution Rules

| Rule | Enforcement |
|------|------------|
| Repair must precede reentry, never reverse | Required |
| Repair phrasing must remain structured | Required |
| Silent repair only if user context unaffected | Allowed |
| Hard repair must be visible and explicit | Required |
| Repair must not overwrite session_id context | Forbidden |

---

## 8. Decision Tree (Runtime Use)

```
Drift detected?
│
├─ Minor? (intent preserved)
│    └─ Apply soft repair → reenter
│
├─ Repeated drift? (≥3 attempts)
│    └─ Escalate to R9 (hard repair)
│
└─ Catastrophic drift?
     └─ Require explicit re-alignment
```

---

## 9. Summary

| Phase | Action |
|-------|--------|
| Detect → Repair | Choose R1/R2/R3 based on drift class |
| Repair → Reentry | Signal stability and resume workflow |
| Escalation Path | R1 → R2/R3 → R9 if needed |

---

### Maintainer  
**Kiyoshi Sasano — Applied Runtime Systems**

---

> _“Repair isn’t fallback — it is governed continuity.”_
