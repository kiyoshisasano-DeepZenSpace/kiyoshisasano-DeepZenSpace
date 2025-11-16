---
title: "Integration Recipes Index"
version: "1.1"
status: "Entry Point"
maintainer: "Kiyoshi Sasano"
updated: "2025-01-15"
visibility: "Public"
scope: "Quickstart — Practical Implementation Patterns"
---

# Integration Recipes (PLD Applied)

> **If you're here directly:**  
> You likely came from the Quickstart or system patterns.  
> If not, recommended entry sequence:

```
/quickstart/README_quickstart.md → /patterns/README_patterns.md → (this folder)
```

These recipes demonstrate how to integrate the **PLD runtime loop** into real agent architectures.

Unlike conceptual docs, these files are:

| Principle | Meaning |
|----------|---------|
| 🧪 Runnable | Ready-to-run (local mode, no external infra required) |
| 🔍 Observable | Emits structured PLD signals (`D*`, `R*`, `RE*`, `OUT*`) |
| 📈 Measurable | Compatible with `07_pld_operational_metrics_cookbook.md` metrics |
| 🔧 Replaceable | LLM, retriever, tools, memory architecture can be swapped |
| ♻️ Loop-aware | Follows PLD: **Drift → Repair → Reentry → Continue → Outcome** |

These are not tutorials — they are **implementation starting points** for production-grade agents.

---

## 2 — Available Recipes

These recipes are divided into two categories:

> **Tier 1 → Component Patterns (How to make each part stable)**  
> **Tier 2 → System Pattern (How to assemble the whole agent)**

---

### **Tier 1 — Component Patterns (Building Blocks)**

These recipes make **individual agent subsystems PLD-aware**.

| File | Component | Operational Drift Type | Runtime Skill Demonstrated |
|------|-----------|------------------------|----------------------------|
| **`rag_repair_recipe.md`** | Retrieval | `D5_information` | Detect and repair retrieval failure without hallucination amplification |
| **`tool_agent_recipe.md`** | Tool Execution | `D4_tool` | Structured recovery from invalid/failed tool calls |
| **`memory_alignment_recipe.md`** | Memory | `D2_context` | Detect and repair memory or persona drift during multi-turn sessions |

> These files teach how to make a **single part reliable** — they are *not complete agents*.

---

### **Tier 2 — System Pattern (Capstone)**

Where Tier 1 components are assembled into a unified runtime.

| File | System Role | Drift/Reentry Focus | Runtime Capability |
|------|-------------|--------------------|--------------------|
| **`reentry_orchestration_recipe.md`** | **Orchestrator** | `RE* orchestration` | Centralized routing after any drift repair: continue, fallback, or terminate |

> 📌 If **Tier 1 = Components**, then **Tier 2 = Operational Control Plane**.

This represents an applied PLD agent running as a **closed-loop runtime**, not isolated handling logic.

---

## 3 — Recommended Learning Path

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

This reflects how real teams implement PLD:  
from **individual failure modes → coordinated runtime governance**.

---

## 4 — Maturity Mapping (Aligned with `07_cookbook`)

| Capability Level | Meaning | Reached After |
|------------------|---------|---------------|
| **Level 1 — Detect** | PLD drift signals emitted | After first recipe |
| **Level 2 — Repair** | Automated repair responses executed | After Tier 1 |
| **Level 3 — Reentry** | Controlled returns after repair | After Tier 2 |
| **Level 4 — Stability Monitoring** | Measurable improvement using PRDR / REI / VRL | After operational instrumentation |

---

## 5 — Before Modifying or Extending

Review:

- `/docs/06_pld_concept_reference_map.md`
- `/docs/07_pld_operational_metrics_cookbook.md`
- `/quickstart/_meta/MIGRATION.md`

These ensure consistency across:

- Canonical PLD vocabulary (`D*`, `R*`, `RE*`, `OUT*`)
- Drift/repair semantics
- Observability and evaluation flows

---

## Final Note

> These recipes are **reference implementations — not prescriptions.**  
> Adapt them based on domain, risk model, latency budget, and UX expectations.

If your variation demonstrates stability across **≥200 turns with improved PRDR**, consider contributing it upstream.

Maintainer: **Kiyoshi Sasano**
