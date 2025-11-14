# 03 — Reentry Confirmation Patterns  
*Stability Re-Anchoring After Repair (PLD Applied)*

Reentry is the moment where the system transitions from **repair mode → task execution mode**.  
It is not just a sentence — it is a **state checkpoint**.

A repair is not complete until the system has confirmed alignment and re-established task continuity.

---

## 1. Core Reentry Confirmation Template (Default)

Use after Soft or Hard Repair unless context continuation is obvious.

```
Great — correction applied.

Before we continue, here’s the current task state:

Goal: <goal>
Constraints: <constraints>
Next step: <planned action>

Should I proceed? (Yes / Adjust)
```

Why it works:  
It bridges repair → action without assuming intent.

---

## 2. Lightweight Reentry (Minimal Impact)

Used when correction was mild and flow should remain smooth.

```
Update applied — continuing with:

<next action>

If anything needs adjusting, tell me anytime.
```

Tone: **confident, not hesitant.**

---

## 3. Ambiguity Collapse Reentry

Used after clarification or ambiguity resolution.

```
Thanks — based on your confirmation, we're continuing with:

<selected option>

Next: <next step>
```

Optional: include branch name  
(e.g., *Route A: Budget Hotels*)

---

## 4. Scope-Switch Reentry

Used when repair involved a confirmed change of direction.

```
Understood — we've switched to the new task focus:

New goal: <goal>
Relevant constraints: <constraints if any>

Would you like:
1) Full restart with new constraints
2) Continue using previous data
```

Prevents **silent context bleed.**

---

## 5. Tool/DB Correction Reentry

Used after tool conflict, API error, or corrected source-of-truth.

```
Correction applied based on the latest data.

Updated result:
<corrected or verified information>

Continuing from here — should I proceed with <next action>?
```

Protects **trust and grounding.**

---

## 6. Latency-Aware Reentry (Voice/UI Agents)

Use when delay risks user uncertainty.

```
Thanks for waiting — I’m back on track.

We’re continuing with:
<summary>

Ready to proceed?
```

Pairs well with typing indicators or streaming signals.

---

## 7. Partial Recovery Reentry

Used when not all constraints or details could be restored.

```
I resolved most of the previous issue, but one detail needs confirmation.

Everything is aligned except:
<missing or conflicting parameter>

Which option should we use?
```

Avoid pretending everything is fixed — **partial repair must be explicit.**

---

## 8. Autonomous Reentry (High Confidence)

Used only when:

- constraints unchanged  
- no branching ambiguity present  
- drift fully resolved  

```
Adjustment made — continuing with the plan.

<next step or result>
```

This pattern is efficient but should not silence uncertainty.

---

## 9. Anti-Patterns (Avoid)

| Anti-Pattern | Risk |
|--------------|------|
| ❌ Silent reset | Creates invisible drift |
| ❌ Asking user to restate everything | Increases cognitive burden |
| ❌ Apology chains | Signals instability |
| ❌ Continuing after changed assumptions | High cascading failure risk |

Reentry is a **checkpoint, not a courtesy phrase.**

---

## 10. Optional Telemetry Event (PLD Schema Compatible)

```
{
  "event_type": "reentry",
  "repair_state": "resolved",
  "user_confirmation_required": true,
  "confidence": 0.87
}
```

---

### Summary

Reentry patterns ensure:

- ✔ Alignment is explicit  
- ✔ Repair transitions are stabilized  
- ✔ Task state is visible and traceable  
- ✔ Flow resumes confidently  

Without Reentry, repair is not recovery — it is **just a pause.**

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**