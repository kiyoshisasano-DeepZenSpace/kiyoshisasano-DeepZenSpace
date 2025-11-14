#  Soft Repair Patterns  
*(Stabilization Phase Templates — PLD Applied)*

Soft Repair is the preferred first response after drift detection.  
The goal is not to restart — but to re-align the conversation with minimal disruption, preserve continuity, and maintain user confidence.

Soft Repair should feel like **course correction**, not **failure recovery**.

---

## 1. Core Soft Repair Template (Universal)

This is the default fallback pattern — short, neutral, stabilizing.

```
It looks like my last response may not fully match your request.
Let me adjust based on your constraints:

<corrected response>

To confirm, are we still working toward <goal> with <constraints>?
```

Notes:

- Avoid apology stacking — prefer neutral acknowledgment.
- Reinforce goal + constraint alignment.

---

## 2. Missing / Incorrect Constraint Repair

Use when numbers, limits, or filters were forgotten or contradicted.

```
Thanks — I missed one detail.
Based on your constraint (<repeat constraint>), here are the correct options:

<corrected content>

Is this aligned with what you're looking for?
```

Best for:

- RAG mismatch  
- Database/lookup mismatch  
- Slot misalignment  

---

## 3. Ambiguity Repair (Clarification Required)

Used when unclear requests appear.

```
I need one clarification before continuing.

When you say "<phrase>", do you mean:
1) <option A>
2) <option B>
3) Something else?

I'll proceed once confirmed.
```

This prevents branching drift before it begins.

---

## 4. Scope Change Repair

When user intent shifts mid-task.

```
It seems the focus may have changed.

Should we continue with the original goal (<goal>),
or switch to the new request (<new scope>)?

Reply: (Continue / Switch)
```

Never assume scope — confirm it.

---

## 5. Evidence-Based Repair

Used when tool/API data contradicts earlier reasoning.

```
I checked the latest results and they conflict with my earlier message.

Correct information:
<verified truth>

Continuing with updated context.
```

Confirm only if task direction changes.

---

## 6. Latency-Based Repair (Timing Stabilization)

Used when delay risks trust or context loss.

```
Thanks for waiting — I’m still working with your last instruction.

Here’s what I have so far:
<partial progress or summary>

Continue as planned? (Yes / Modify request)
```

Ideal for streaming/voice agents.

---

## 7. Soft Repair + Reentry Stitch

Use when the repair alters trajectory or state content.

```
Correction applied. We’re now continuing from here:

<state summary>
<next step>
```

This restores flow without repeating earlier context.

---

## 8. Anti-Patterns (Avoid)

| Anti-Pattern | Why It Breaks Flow |
|-------------|--------------------|
| ❌ Excessive apologies | Signals uncertainty and lowers trust |
| ❌ Multiple corrections in a single turn | Repair becomes new drift |
| ❌ Restarting too early | Users perceive incompetence |
| ❌ Silent corrections | Creates invisible divergence |

Soft Repair should be **visible, minimal, and stabilizing.**

---

## 9. Telemetry Structure (Optional)

```
{
  "repair_type": "soft",
  "trigger": "constraint_mismatch | ambiguity | contradiction | scope_shift",
  "confidence": 0.00–1.00,
  "resolved": true
}
```

Compatible with:

- `pld_event.schema.json`  
- MultiWOZ N200 analysis  
- Drift chain stability scoring  

---

### Summary

Soft Repair patterns allow the system to:

- Maintain continuity  
- Prevent cascading drift  
- Re-align context with user intent  
- Protect UX pacing and trust  

Soft Repair is the operational backbone of applied PLD.

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**