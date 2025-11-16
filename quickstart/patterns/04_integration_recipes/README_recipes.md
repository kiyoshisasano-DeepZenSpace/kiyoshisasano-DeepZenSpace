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

These recipes demonstrate how to integrate the **PLD runtime loop** into real agent architectures.

Unlike conceptual docs, these files are:

| Principle | Meaning |
|----------|---------|
| 🧪 Runnable | Ready-to-run (local mode, no external infra required) |
| 🔍 Observable | Emits structured PLD signals (`D*`, `R*`, `RE*`, `OUT*`) |
| 📈 Measurable | Works with metrics from `07_pld_operational_metrics_cookbook.md` |
| 🔧 Replaceable | Each component can be swapped (LLM, RAG, Tools, Memory) |
| ♻️ Loop-aware | Follows PLD: **Drift → Repair → Reentry → Continue → Outcome** |

These are not tutorials — they are **implementation starting points** for production-grade agents.

---

## 2 — Available Recipes

These recipes are divided into two categories:

> **Tier 1 → Component Patterns (How to make each part behave correctly)**  
> **Tier 2 → System Pattern (How to assemble them into a resilient agent)**

---

### **Tier 1 — Component Patterns (Building Blocks)**  
These recipes make **individual agent subsystems PLD-aware**.

| File | Component | Drift Focus | Runtime Skill Demonstrated |
|------|-----------|------------|----------------------------|
| **`rag_repair_recipe.md`** | Retrieval | `D5_information` | Detect and repair retrieval failure without hallucination amplification |
| **`tool_agent_recipe.md`** | Tool Execution | `D4_tool` | Structured recovery from invalid/failed tool calls |
| **`memory_alignment_recipe.md`** | Memory | `D2_context` | Detect and repair memory or persona drift during multi-turn sessions |

> These files teach how to make a **single part reliable** — they are not full agents.

---

### **Tier 2 — System Pattern (Capstone)**  
This is where components from Tier 1 are **assembled into a unified runtime**.

| File | System Role | Drift/Reentry Focus | Runtime Skill Demonstrated |
|------|-------------|--------------------|----------------------------|
| **`reentry_orchestration_recipe.md`** | **Orchestrator** | `RE* orchestration` | Centralized routing after any drift repair: continue, fallback, or terminate |

> 📌 **If Tier 1 is “hardware,” Tier 2 is the operating system.**

This is the **most important recipe**:  
It represents the applied PLD agent model running as a **closed-loop runtime**, not isolated behaviors.

---

## 3 — Learning Path Recommendation

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

This progression reflects real implementation order:  
From **single failure handling** → **multi-component orchestration**.

---

## 4 — Maturity Mapping (Based on 07_cookbook)

| Capability Level | Meaning | Achieved After |
|------------------|---------|----------------|
| **Level 1 — Detect** | PLD drift signals emitted | After first recipe implemented |
| **Level 2 — Repair** | Automated repair strategy applied | After Tier 1 completion |
| **Level 3 — Reentry** | Controlled continuation after repair | After capstone |
| **Level 4 — Stability Monitoring** | Metrics improve & regressions detected | After integration with PRDR / REI / VRL dashboards |

---

## 5 — Before Modifying or Extending

Review:

- `/docs/06_pld_concept_reference_map.md`
- `/docs/07_pld_operational_metrics_cookbook.md`
- `/quickstart/_meta/MIGRATION.md`

These ensure consistency with:

- Vocabulary discipline (`D*`, `R*`, `RE*`, `OUT*`)
- Logging schemas
- Repair strategy evaluation

---

## Final Note

> These recipes are **reference implementations, not constraints.**  
> Use them to bootstrap production agents and tune based on your domain.

If your variation demonstrates stable improvement (≥200 turns with PRDR trend reduction), consider contributing it.

Maintainer: **Kiyoshi Sasano**
