# PLD Field Collaboration & PoC Guide

This folder is for **working with other people or organizations** on PLD.

While the rest of the repository focuses on:

- understanding the PLD runtime loop  
- implementing operators and patterns  
- logging and evaluating behavior  

`field/` focuses on:

- how to **run a shared PoC**  
- how to **align interpretation of drift / repair / reentry**  
- how to **exchange traces and metrics safely**  
- how to **decide whether a PLD integration “works” in a real setting**  

It is not a legal document.  
It is a **technical and operational playbook** for collaboration.

---

## When to Use This Folder

Use `field/` when:

- you are involving **another team or company** in a PLD experiment  
- you want to share **traces, metrics, and configs** with someone else  
- you need a **lightweight protocol** for “what we look at together” in a PoC  

Roughly, this comes **after**:

1. You have a local PLD prototype (via `quickstart/`)
2. You are logging PLD events (via `quickstart/metrics/`)
3. You have at least a few sessions worth of traces (via `analytics/`-style logs)

Then:

```
local prototype → shared PoC → field deployment
                  ↑
                this folder
```

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `pld_minimal_collaboration_protocol.md` | A lightweight agreement on scope, data, and evaluation for PLD PoCs |
| `pld_onboarding_and_diagnostics.md` | How to bring a new team up to speed and run the first joint diagnostics |
| `pld_trace_examples.md` | Small, annotated trace examples to align “what drift / repair / reentry look like” |

---

## Who This Is For

- External collaborators exploring PLD with you  
- Partner teams inside a larger organization  
- Applied AI / product teams running joint PoCs  
- Anyone who needs a shared operational language for drift / repair / reentry  

> PLD is a runtime model — but collaboration around it is social.  
> `field/` exists to make that collaboration predictable, lightweight, and repeatable.

> [!NOTE]
> PLD terminology refers to observable conversational behavior, not model psychology, intention inference, or emotional state attribution.

---

## `field/pld_minimal_collaboration_protocol.md`

```markdown
# PLD Minimal Collaboration Protocol

This document describes a **minimal, practical protocol** for running a shared PoC or field study with PLD.

It is meant to answer:

- What are we testing together?
- How will we look at traces and metrics?
- When do we say “this worked” or “this needs rework”?

It is intentionally lightweight.  
You can copy, adapt, or specialize it for your own collaborations.

---

## 1. Shared Scope

Before starting, both parties should agree on:

1. **Target System**
   - What system are we applying PLD to?
   - Examples: support assistant, RAG agent, tool-using orchestrator, workflow bot.

2. **Interaction Type**
   - Multi-turn chat, API-driven tasks, scripted scenarios, etc.

3. **Risk Level**
   - Prototype only (no end users)
   - Staging with internal users
   - Limited production trial with guardrails

4. **Time Box**
   - Example: “Run this experiment for 2–4 weeks, then review.”

Write this down in a simple table:

| Item | Value |
|------|-------|
| System | e.g., “Support agent with tools X + Y” |
| Environment | Prototype / Staging / Limited Prod |
| Time Box | e.g., 3 weeks |
| Owner (Partner A) | Name / team |
| Owner (Partner B) | Name / team |

---

## 2. Shared PLD Definitions

To avoid talking past each other, align on these **operational definitions**:

- **Drift**  
  When the system’s behavior diverges from its intended task, context, or user intent.

- **Repair**  
  A system-level correction step:  
  - *Soft Repair* = clarify, correct, restate constraints  
  - *Hard Repair* = reset, change strategy, or restart

- **Reentry**  
  The checkpoint where the system confirms alignment before continuing.

- **Outcome**  
  The final status for a task: complete, partial, failed, or abandoned.

Both sides should confirm:

```
We will label and discuss behavior using these PLD terms.
We will not invent separate private vocabularies.
```

---

## 3. Minimal Data Protocol

### 3.1 What We Share

At minimum, both sides should be able to share:

- **PLD event logs** for selected sessions  
  - drift: present / type / reason  
  - repair: present / mode / code  
  - reentry: present / success  
  - outcome: status  
  - timing: latency, high-latency markers

- **Anonymized transcripts** of relevant sessions  
  - Enough to understand why drift happened  
  - Sensitive content redacted if required

- **Configuration snapshot**  
  - High-level description of prompts, tools, and routings  
  - No proprietary weights or secrets required

### 3.2 What We Do Not Require

This protocol does **not** require:

- Model weights  
- Full source code  
- Raw production logs  
- Personally identifiable information  

Only behavioral traces and metrics are required.

---

## 4. Joint Evaluation Ritual

A minimal joint review session should cover:

### Step 1 — Pick 5–10 sessions

- 3 where PLD behaved as desired  
- 3 where drift/repair was messy but recoverable  
- 3 where the system “failed” or required escalation  

### Step 2 — Walk the Phase Loop

For each session:

- Where did drift appear?  
- Was repair attempted? Soft? Hard?  
- Did reentry succeed or fail?  
- What was the outcome?

### Step 3 — Look at Metrics

- Drift rate  
- Soft vs hard repair ratio  
- Reentry success  
- Outcome distribution  
- Latency / abandonment signals  

### Step 4 — Decide Next Action

- UX adjustment  
- Prompt / operator refinement  
- Routing change  
- Monitoring rule  

---

## 5. Success Criteria Template

Define a shared notion of “success”:

| Dimension | Example Target |
|----------|----------------|
| Drift rate | ≤ 15% of turns on target flows |
| Repair effectiveness | ≥ 70% soft repair recovery |
| Reentry success | ≥ 80% stable return to intent |
| Outcome complete | ≥ 75% completion or acceptable partial |
| Critical failures | 0 catastrophic failures in N sessions |

These are adjustable depending on domain and risk.

---

## 6. Roles & Cadence

Example distribution:

| Role | Responsibility |
|------|---------------|
| Partner A | Owns implementation + log export |
| Partner B | Owns PLD review + metrics dashboards |
| Both | Bi-weekly review + deployment decision |

Minimal protocol = minimal friction.  
The goal is shared **interpretation**, not shared infrastructure.

```


