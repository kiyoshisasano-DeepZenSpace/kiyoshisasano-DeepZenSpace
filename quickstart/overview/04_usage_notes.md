# 04 — Practical Usage Notes & Guardrails  
**PLD Applied Edition (2025)**  

This document provides **working rules, constraints, and usage patterns** for applying Phase Loop Dynamics (PLD) in engineering environments.  
It is not theory — it exists to prevent incorrect assumptions and misuse.

If you are building, integrating, testing, or evaluating PLD-aligned agents: **read this before implementation.**

---

## 🔧 **1 — What PLD Is (Applied Context)**

PLD is:

- a state-aware interaction framework  
- a method to detect, classify, and repair conversational drift  
- a workflow model for agent stability and continuity  

PLD is **not**:

- ❌ a theory-first linguistics framework  
- ❌ a conversational design aesthetic  
- ❌ a philosophical treatment of meaning  
- ❌ a metaphor-driven mental model  

PLD exists because **multi-turn LLM systems fail silently.**  
PLD makes failures:

> **traceable → repairable → measurable**

---

## ⚠️ **2 — When PLD Should Be Applied**

Use PLD when:

| Condition | Example |
|-----------|---------|
| State matters | restaurant booking, RAG agents, multi-step assistants |
| Tool/API calls affect state | price lookup → booking workflow |
| Latency impacts UX | streaming agent / pacing problems |
| Conversation stores memory | Assistants API, workflow orchestration |
| Repair matters more than perfection | customer service, automation |

Do **NOT** use PLD where:

| Situation | Example |
|-----------|---------|
| Single-turn QA | simple factual lookups |
| Output is not interactive | text-to-image prompts |
| State resets by design | ephemeral demos |
| Drift is desirable | brainstorming, storytelling |

---

## 🪜 **3 — Operational Rules**

These rules prevent misuse and ensure consistent PLD implementation.

---

### **Rule 1 — Drift MUST be classified before repair**

Repair without classification results in chaotic or inconsistent compensation behavior.

```
❌ detect → repair → classify  
✔️ detect → classify → repair → reentry
```

---

### **Rule 2 — Soft Repair is the default**

Hard repair should be deliberate — not reactive.

| Repair Type | Purpose |
|------------|---------|
| Soft Repair | Preserve context and continuity |
| Hard Repair | Reinitialize corrupted or unstable context |

---

### **Rule 3 — Reentry must be explicit**

No repair is complete until the agent **verifies shared alignment**.

Example:

> “To confirm — we’re still booking the train from Cambridge to London, correct?”

---

## 🧭 **4 — Human UX Constraints**

PLD assumes:

- Users accept repair **if acknowledged**
- Silence longer than **~2.5s feels like failure**
- Reentry must be:

  - brief  
  - goal-oriented  
  - confirmation-based (not apologetic)

| Bad | Good |
|-----|------|
| “Sorry, let me retry.” | “Let me confirm details before proceeding.” |
| “My mistake.” | “Updating with corrected information — confirming intent.” |

---

## 📡 **5 — Integration Notes**

PLD aligns with:

| Platform | Compatible |
|----------|------------|
| LangChain / LangGraph | ✔️ Yes |
| Agents API (OpenAI) | ✔️ Yes |
| Autogen | ✔️ Yes |
| Rasa | ⚠️ Partial (extensions required) |
| Custom orchestration engines | ✔️ Fully supported |

Telemetry required:

```
session_id
turn_id
speaker
drift_type
repair_type
latency
outcome
```

> You **cannot** measure PLD effectiveness without logs.

---

## 📊 **6 — What Changes as Maturity Increases**

| System Stage | Behavior | Notes |
|--------------|----------|-------|
| Level 0 | No repair, no classification | baseline chatbot |
| Level 1 | Drift detected but not repaired | passive observation |
| Level 2 | Soft repair reliably applied | user trust increases |
| Level 3 | Hard repair decision logic | stable long-horizon tasks |
| Level 4 | Predictive repair & proactive guidance | **target state** |

Most commercial agents today are between **Level 0.5 → 1.5**.

---

## 📁 **7 — Related Files**

| File | Relationship |
|------|-------------|
| `01_overview_quickstart.md` | Orientation |
| `02_pld_core_summary.md` | Lifecycle definition |
| `03_pld_mapping_index.md` | Repository navigation |
| `operator_primitives/*.md` | Implementation layer |

---

### Attribution

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
