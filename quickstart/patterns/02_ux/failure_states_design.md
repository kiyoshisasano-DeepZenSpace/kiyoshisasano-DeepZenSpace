# Failure State Design — Applied-AI Interaction Patterns  
*(PLD-Aligned UX Behavior Specification)*

**Audience:** Designers and engineers working on LLM agents, multi-agent systems, or tool-driven automation.

**Purpose:**  
Define repeatable UX patterns for failure states so users understand:

- **what went wrong,**
- **what is happening now,**
- **what happens next** —

without losing trust or abandoning the task.

---

## 01 — Why Failure States Matter

In applied LLM systems, **silence behaves like friction.**  
Users interpret failure as:

- ❓ confusion  
- 🚫 unreliability  
- 🔁 need to retry manually  
- 🧱 broken workflow  

A well-designed failure response must:

| Goal | Meaning |
|------|---------|
| **Maintain context** | Avoid unnecessary resets |
| **Communicate state** | Explain, don’t hide uncertainty |
| **Preserve trust** | Keep emotional stability |
| **Enable recovery** | Provide clear actionable next steps |

Failure handling is not messaging — it is **continuity engineering.**

---

## 02 — PLD-Aligned Failure Types

Mapped to PLD applied taxonomy:

| Failure Type | Meaning | Common Triggers |
|--------------|---------|-----------------|
| **Execution Failure** | System cannot complete an operation | API timeout / runtime error |
| **Logic Failure** | Internal belief state incorrect | Contradiction / hallucination |
| **Instruction Failure** | Intent unclear or incomplete | Ambiguous or partial user input |
| **Constraint Failure** | Task impossible under given rules | No matching options |
| **Resonance Loss** | Trust or rhythm collapse | Repeated drift + confusion |

Each type maps to a **Soft Repair** or **Hard Repair** pathway.

---

## 03 — Failure Response Template (PLD Standard)

Every visible failure state must use the following structure:

```
[State Signal] +
[Acknowledgment] +
[Context Anchor] +
[Recovery Action]
```

Example:

```
⚠ Something didn’t work.
Let me check where the process drifted.
We're still working on booking accommodation with your original preferences.
Would you like to adjust the price range or try a different area?
```

This preserves trust and task continuity.

---

## 04 — Microcopy Library (Production-Ready)

| Scenario | Recommended Copy |
|----------|------------------|
| Tool/API Failure | _“That request didn’t finish — retrying now.”_ |
| Unresolvable Constraints | _“Nothing fits those filters — want to adjust the criteria?”_ |
| Contradiction or hallucination detected | _“I may have misinterpreted — let me correct that.”_ |
| Missing information | _“One detail is missing — which date did you mean?”_ |
| Compounded confusion | _“Resetting just this step — your goal stays the same.”_ |

Tone: neutral, confident, non-apologetic unless required.

---

## 05 — Soft vs Hard Repair Pathways

| Condition | Recommended Response |
|-----------|----------------------|
| **Recoverable & isolated** | → Soft Repair |
| **State corrupted or contradictory** | → Hard Repair |

### Soft Repair Example

```
⚠ Minor issue detected.
Adjusting this step — no restart needed.
```

### Hard Repair Example

```
🔄 Resetting this part so we continue cleanly.
Your goal remains the same: booking a hotel in Cambridge.
```

---

## 06 — Timing Rules

Timing determines perception quality:

| Delay Threshold | User Interpretation | Required Behavior |
|-----------------|--------------------|------------------|
| 0–800ms | Mild uncertainty | Acknowledge processing |
| 800ms–2.5s | Expectation forming | Provide clarity + what’s happening |
| >2.5s | Concern or distrust | Explicit fallback, retry, or reframe |

Never allow silent uncertainty beyond **2.5–3.2s**.

---

## 07 — UI Component Structure (Figma-Ready)

```
[Icon / Animation]
[Primary Message]
[Secondary Context]
[Action Choices: Retry / Adjust / Continue / Reset]
```

Guidelines:

- Avoid modal traps — allow parallel user input
- Maintain scroll position (avoid jump-to-top resets)
- Support streaming where appropriate

---

## 08 — Anti-Patterns (Avoid)

- ❌ Generic “Something went wrong.”
- ❌ Full restart when partial repair suffices
- ❌ User-blaming tone (“Invalid input”)
- ❌ Long silent spinner with no context
- ❌ Overconfident corrections without acknowledgment

---

## 09 — Measurement & Success Criteria

A failure design is successful when:

- Duplicate commands decrease  
- Repair success rate increases  
- Reentry transitions feel natural  
- User trust stabilizes after failures  
- Task abandonment decreases  

---

### Attribution

Maintainer: **Kiyoshi Sasano**  
File: `patterns/02_ux/failure_states_design.md`  
License: **CC BY-NC 4.0**