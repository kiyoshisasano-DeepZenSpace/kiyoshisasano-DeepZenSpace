# PLD Drift–Repair Taxonomy (Applied-AI Edition, 2025)

This document defines the **public-facing, engineering-focused** taxonomy for detecting and labeling
Drift, Repair, and Reentry events in LLM agents, tool-using systems, task‑oriented dialogue (TOD),
and multi‑agent orchestration workflows.

It is designed for:
- LLM agent / tool-execution engineers  
- Task-oriented dialogue system developers  
- UX / conversation designers focused on timing and trust  
- Multi-agent / orchestration architects  

All terminology is restricted to **Applied-AI engineering vocabulary** only.  
No conversation-analysis or HCI-theory terms are used.

---

## 1. Overview

PLD categorizes interaction breakdowns and recovery behaviors into three classes:

- **Drift (D-series)** — System behavior diverges from user intent, task state, workflow, or timing expectations.  
- **Repair (R-series)** — The system performs corrective behavior.  
- **Reentry (RE-series)** — The interaction returns to the intended task or workflow after a divergence.

This taxonomy is used for:
- failure analysis  
- benchmark-style evaluation  
- agent debugging  
- training data labeling  
- workflow instrumentation  

---

## 2. Drift Categories (D-series)

### **D1 — Information Drift**
System outputs **factually or logically inconsistent information**, including:
- DB/API “no result” contradictions  
- inconsistent attributes  
- hallucinated world-state  
- mismatched tool-call results  

**Rule:**  
> The system contradicts prior truth, constraints, or its own earlier outputs.

---

### **D2 — Context Drift**
Loss or corruption of internal memory/state.

Includes:
- missing constraints  
- overwritten slots  
- ignoring previously supplied input  
- mixing states between turns  

**Rule:**  
> The system forgets or misuses previously established context.

---

### **D3 — Intent Drift**
The system misinterprets or diverges from the user’s goal.

Examples:
- switching task domains (hotel → taxi)  
- offering irrelevant actions  
- changing plan without user signal  

**Rule:**  
> The system moves away from the user's stated goal or task.

---

### **D4 — Procedural Drift (Workflow Drift)**
Breakdown in execution or multi-agent workflow structure.

Includes:
- repeated planning  
- stalled or looping tool-calls  
- missing postconditions  
- agent role drift (planner vs executor, critic ignored, etc.)  

**Rule:**  
> The workflow deviates from the expected operational sequence.

---

### **D5 — Pacing / Latency Drift**
Timing behavior disrupts perceived responsiveness.

Examples:
- long silence without indicator  
- abrupt or unnatural pacing  
- confusing streaming behavior  

**Rule:**  
> Timing mismatches cause user frustration or confusion.

---

## 3. Repair Categories (R-series)

### **R1 — Local Repair (Soft Repair)**
Light, context-preserving correction.

Examples:
- clarifying question  
- adding missing detail  
- retrying tool-call with corrected arguments  
- providing options  

**Rule:**  
> Fix the issue without discarding the session.

---

### **R2 — Structural Repair**
Fixes internal dependencies, memory, or workflow linkages.

Examples:
- recovering lost slot  
- restoring tool-call result  
- stabilizing planner/executor state  

**Rule:**  
> Repair internal structure while keeping the current context.

---

### **R3 — UX Repair**
Recovery through pacing, timing, or feedback.

Examples:
- “still checking…”  
- progressive disclosure  
- typing indicators / fillers  

**Rule:**  
> Restore perceived responsiveness and reduce uncertainty.

---

### **R4 — Hard Repair (Restart / Reset)**
Full session reset.

Examples:
- “Let’s start over.”  
- clearing memory  
- workflow reinitialization  

**Rule:**  
> Discard the entire context intentionally.

---

## 4. Reentry Categories (RE-series)

### **RE1 — Intent Reentry**
Returning to the original task/goal after divergence.

### **RE2 — Constraint Reentry**
Restoring previously stated constraints or parameters.

### **RE3 — Workflow Reentry**
System or agent re-aligns with the expected workflow sequence.

---

## 5. Annotation Output Format

Tools and evaluators should output JSON:

```json
{
  "label": "D1",
  "reason": "The system contradicted a previous DB result."
}
```

---

## 6. Examples

### Example A — Information Drift
System first says “no hotels available”  
Later shows three matching hotels  
→ **D1**

### Example B — Missing constraint  
System forgets user’s required price range  
→ **D2**

### Example C — Workflow loop  
Planner keeps re-planning despite successful tool execution  
→ **D4**

### Example D — Soft Repair  
System asks: “Do you prefer north or south area?”  
→ **R1**

### Example E — Workflow Reentry  
Planner/executor realigns after temporary divergence  
→ **RE3**

---

## 7. Versioning
**PLD Applied-AI Taxonomy v1.0 (2025)**  
Aligned with MultiWOZ 2.4 N=200 analysis and PLD Metrics Suite.

