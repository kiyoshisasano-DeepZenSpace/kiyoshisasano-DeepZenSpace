---
title: "Integration Recipes Index"
version: "1.0"
status: "Entry Point"
maintainer: "Kiyoshi Sasano"
updated: "2025-01-15"
visibility: "Public"
scope: "Quickstart — Practical Implementation Patterns"
---

# Integration Recipes (PLD Applied)

> **If you're here directly:**  
> Recommended entry path:


```
/quickstart/README_quickstart.md → /patterns/README_patterns.md → (this folder)
```


These recipes demonstrate how to integrate the **PLD runtime loop** into real agent components and orchestration layers.

They are **reference implementation patterns** — not tutorials — showing how PLD behaviors appear in an applied environment.

---

## Framework Context

⚠️ **These recipes use LangGraph for demonstration purposes.**

PLD itself is **framework-agnostic**.  
The same integration concepts apply to:

- OpenAI Assistants API
- AutoGen / CrewAI
- Rasa
- Swarm
- Custom orchestrators or step-based policy controllers

LangGraph is used here because it provides a clear and modular execution graph for illustrating the runtime loop.

---

## 2 — Available Recipes

Recipes are grouped into two functional tiers:

> **Tier 1 → Component Patterns (Stabilize each subsystem)**  
> **Tier 2 → System Pattern (Assemble components into a governed runtime)**

---

### **Tier 1 — Component Patterns (Building Blocks)**

These recipes make individual subsystems **PLD-aware and recoverable.**

| File | Component | Operational Drift Type | PLD Pattern Illustrated |
|------|-----------|------------------------|-------------------------|
| `rag_repair_recipe.md` | Retrieval | `D5_information` | Detect + repair retrieval failure without hallucination amplification |
| `tool_agent_recipe.md` | Tool Execution | `D4_tool` | Structured response to invalid/failed tool calls with retry logic |
| `memory_alignment_recipe.md` | Memory | `D2_context` | Detect and repair misaligned state, constraints, persona, or intent |

> These modules stabilize single components — they do *not* form a full runtime agent yet.

---

### **Tier 2 — System Pattern (Capstone)**

This recipe shows **how to assemble the Tier 1 components under a unified control loop.**

| File | System Role | Drift Focus | Integration Focus |
|------|-------------|-------------|-------------------|
| `reentry_orchestration_recipe.md` | **Orchestrator** | `RE* orchestration` | Central routing after repair: continue, retry, fallback, or exit |

> 📌 If **Tier 1 = parts**, then **Tier 2 = the operational control plane.**

This is where an agent becomes a **closed-loop runtime**, not just a set of behaviors.

---

## 3 — Recommended Adoption Path

```
langgraph_example.md  
        ↓
rag_repair_recipe.md  
        ↓  
tool_agent_recipe.md  
        ↓  
memory_alignment_recipe.md  
        ↓  
reentry_orchestration_recipe.md  ← (capstone)
```


This reflects how real-world teams adopt PLD:

🔹 First stabilize individual failure modes →  
🔹 Then enable centralized governance.

---

## 4 — Maturity Mapping (Aligned with `07_cookbook`)

| Level | Capability | Achieved After |
|-------|------------|----------------|
| **1 — Detect** | Drift signals emitted (`D*`) | After first recipe |
| **2 — Repair** | Soft/hard repairs executed (`R*`) | After Tier 1 |
| **3 — Reentry** | Controlled continuation (`RE*`) | After Tier 2 |
| **4 — Monitor** | Stability tracked w/ PRDR / VRL / REI | After operational instrumentation |

---

## 5 — Before Extending

Review:

- `/docs/06_pld_concept_reference_map.md`
- `/docs/07_pld_operational_metrics_cookbook.md`
- `/quickstart/_meta/MIGRATION.md`

This ensures:

- Consistent taxonomy (`D*`, `R*`, `RE*`, `OUT*`)
- Alignment with runtime governance semantics
- Measurability across deployments

---

## Final Note

> These patterns are **reference implementations — not prescriptive recipes.**  
> Adapt them based on your domain complexity, reliability targets, latency budget, and user experience expectations.

If your implementation shows stability improvements over **≥200 turns** with reduced PRDR, consider contributing it upstream.

Maintainer: **Kiyoshi Sasano**
