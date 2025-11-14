# PLD Core Model — The Lifecycle and How It Works in Practice

This file explains the core logic of **Phase Loop Dynamics (PLD)** in its applied form.  
If you read only one conceptual file, this should be it.

The goal is to give you a clear, *operational* understanding of the PLD lifecycle — with practical examples showing how it applies to real systems.

---

## **1 — The PLD Lifecycle at a Glance**

> **Drift → Repair → Reentry → Resonance → Outcome**

Each state represents a checkpoint in **interaction stability**, not a theoretical abstraction.

| Stage | What It Represents | System Behavior |
|-------|--------------------|----------------|
| Drift | Something diverges from expected meaning, constraints, or workflow | System no longer aligns with user intent or stored task state |
| Repair | Attempt to correct drift | Model clarifies, retries, or resets |
| Reentry | Verify alignment before continuing | System confirms task, intent, or constraints |
| Resonance | Stable continuation without misalignment | Interaction progresses smoothly |
| Outcome | End state of the task | Complete, incomplete, abandoned, unresolved |

---

## **2 — Drift: The Trigger Condition**

Drift occurs when:

- the agent contradicts earlier content  
- a tool call fails and the system continues as if it succeeded  
- memory propagates incorrect state  
- user intent is misunderstood or replaced  

Examples:

| Drift Type | Example |
|-----------|---------|
| Information Drift | System: “No hotels available.” → later: “Here are 3 hotels.” |
| Intent Drift | User: “Modify booking.” → System restarts new booking |
| Reasoning Drift | Agent changes constraints silently |
| Tool Drift | API failure → hallucinated answer instead of repair |

> PLD does **not** prevent drift —  
it makes drift **observable, correctable, and trackable.**

---

## **3 — Repair: Fixing Without Breaking the Conversation**

Two repair categories:

| Type | Purpose | Example Trigger |
|------|---------|----------------|
| Soft Repair | Local correction that preserves context | Recoverable misunderstanding |
| Hard Repair | Controlled reset when context is corrupted | Contradictions, repeated failure |

Soft repair examples:

> “To clarify — you're still looking for a 4-star hotel downtown, correct?”

Hard repair examples:

> “It looks like early information may be inconsistent. I’ll restart using confirmed details.”

A well-designed agent escalates only when required.

---

## **4 — Reentry: The Step Most Agents Skip**

Reentry prevents **redrift**.

Format:

> **Restate → Confirm → Continue**

Example:

```
So your current constraints are:

• 4-star  
• city center  
• budget ≤ $120  

Should I continue searching with those?
```

If the user corrects → the system prevents a new failure branch.

---

## **5 — Resonance: Smooth Execution After Correction**

Once alignment is confirmed:

- flow becomes predictable  
- responses shorten  
- retries decrease  
- tool usage stabilizes  

Log patterns during resonance:

| Signal | Meaning |
|--------|---------|
| No contradictions | State is consistent |
| Short responses | High confidence |
| Low processing cost | No repeated tool calls |

Resonance improves reliability **and compute efficiency.**

---

## **6 — Outcome: Ending Conditions**

An interaction ends in one of four states:

| Outcome Type | Meaning |
|--------------|---------|
| Complete | Task success |
| Incomplete | Progress made but missing closure |
| Abandoned | User disengaged |
| Unresolved | System failure without recovery |

PLD tracks outcomes relative to prior drift + recovery attempts.

---

## **7 — Why This Model Works**

PLD enables systems to have:

- a predictable fallback policy  
- a consistent recovery strategy  
- a shared operational language across teams  

As a result, it reduces:

- contradiction loops  
- memory corruption  
- unnecessary resets  
- user frustration  

---

## **Next Step**

Continue to:

👉 `03_mapping_index.md`  
(Repository navigation guide — maps concepts to implementation)

---

Maintainer: **Kiyoshi Sasano**  
Version: **Applied-AI Edition (2025)**  
License: **CC-BY-NC 4.0**