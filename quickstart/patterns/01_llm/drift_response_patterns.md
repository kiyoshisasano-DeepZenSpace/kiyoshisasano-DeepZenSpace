---
title: "Drift Response Patterns — PLD Prompting Edition"
version: 2025.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "patterns/llm"
tags:
  - PLD
  - prompting
  - drift response
  - alignment
  - runtime behavior
---

# Drift Response Patterns  
_Phase-aware response strategies for LLM execution environments_

> **Purpose:**  
This document defines standard response scaffolds the model must follow when detecting conversational drift.  
Patterns are aligned with the PLD runtime phases: **Drift → Repair → Reentry → Continue.**

These templates ensure:
- Predictable semantic behavior  
- Minimal user friction  
- Transparent repair signaling (when needed)  
- Compatibility with downstream metrics and dashboards  

---

## 1. Behavioral Philosophy

Drift responses follow three principles:

| Principle | Meaning |
|----------|---------|
| 🧭 Maintain task trajectory | Avoid rewriting or restarting unless necessary |
| 🎯 Be specific, not generic | Reference the user’s last valid goal or constraint |
| 🪶 Soft first, hard only if needed | Escalate repair strength based on drift severity |

> These response patterns are **behavioral contracts**, not UI copy.

---

## 2. Drift Types and Response Strategies

Each drift category requires a specific corrective action.

| Drift Class | Code Prefix | Typical Cause | First Action |
|------------|-------------|---------------|--------------|
| Information Drift | `D1` | Incorrect assumption or fact | Clarify or correct softly |
| Context Drift | `D2` | Lost variables, constraints, or memory | Restate grounded context |
| Intent Drift | `D3` | Misinterpreted user goal | Mirror back intended objective |
| Tool / Workflow Drift | `D4` | Execution mismatch or tool misuse | Acknowledge failure and adjust plan |
| Latency-Induced Drift | `D5` | Response pacing or asynchronous mismatch | Confirm continuity |

---

## 3. Soft Repair Templates (Default)

Soft repairs are used when drift is correctable without restarting flow.

> **Goal:** Maintain continuity while correcting direction.

### Example Template

```
Thanks — I need to adjust based on your last instruction.

✔ Intended goal: {restated_intent_or_constraint}   
🔧 Updated step: {corrected_action_or_information}

Continuing now…
```

#### Variants

| Scenario | Template Variant |
|---------|-----------------|
| Misread constraint | `"Let me correct that — the right value is {X}, not {Y}."` |
| Missing definition | `"Before I continue, I need one detail: {required_field}?"` |
| Wrong workflow step | `"You're right — the next step should be {X}, not {Y}."` |

---

## 4. Hard Repair Templates (Escalation)

Use only when:  
- 3+ soft repair attempts fail,  
- conflicting constraints persist, or  
- the task state becomes ambiguous.

### Standard Hard Repair Copy

```
I need to pause and realign to ensure accuracy.

Before continuing, please confirm:

📌 Goal: {restated_goal}
📌 Key constraints: {bullet_list}

Reply: **“Confirmed”** or update the details.
```

This ensures measurable stabilization for metrics such as **MRBF, VRL, and FR.**

---

## 5. Reentry Confirmation Patterns

After a repair, the model must **signal alignment** and transition back to execution.

```
Alignment confirmed — I’m continuing the task.

Next step: {next_action}
```

Optional micro-variants based on confidence:

| Confidence Level | Pattern |
|------------------|---------|
| 1.0 | `"All set — continuing."` |
| 0.6–0.9 | `"Proceeding, but let me know if this step needs adjustment."` |
| <0.6 | `"I’m continuing, but before finalizing I'll reconfirm."` |

---

## 6. Optional UX Microcopy Layer

These short transitions reduce perceived interruption fatigue:

| Tone | Example |
|------|--------|
| Neutral | `"Let me adjust that."` |
| Polite | `"Thanks — updating now."` |
| Expert | `"Correction applied — continuing."` |
| Safety-focused | `"To avoid an error, I’m confirming the constraint first."` |

---

## 7. Implementation Notes

| Requirement | Reason |
|------------|--------|
| Copy must be consistent across models | Enables metric comparability |
| Patterns must map to PLD `phase` values | Required for runtime instrumentation |
| Visible repairs (`repair_visible`) must remain detectable | Required for VRL monitoring |
| Minimal verbosity when stable | Avoid UI fatigue |

---

## 8. When NOT to Repair

Avoid a repair message when:

- The correction is **internal and silent**, and
- The update does not affect the user’s mental model.

Example:

```
(No visible message — silent repair)
```

This logs as `repair_triggered`, not `repair_visible`.

---

## 9. Summary

| Phase | Required Behavior |
|-------|------------------|
| Drift Detected | Acknowledge + contextual alignment |
| Soft Repair | Correct gently while continuing workflow |
| Hard Repair (Escalation) | Structured confirmation request |
| Reentry | Signal alignment + resume execution |
| Continue | Operate silently unless new drift emerges |

---

### Maintainer
**Kiyoshi Sasano — Applied Runtime Systems**

---

> _“Repair is not interruption —  
it is alignment maintenance.”_


---

Maintainer: **Kiyoshi Sasano**  

Edition: **PLD Applied 2025**

