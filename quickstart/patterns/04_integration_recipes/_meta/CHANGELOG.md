---
title: "Integration Recipes — CHANGELOG"
versioning: "Semantic Versioning (SemVer)"
status: "Pre-Release"
maintainer: "Kiyoshi Sasano"
---

# Changelog — Integration Recipes

This changelog documents the evolution of the integration recipe set within the Quickstart section.

> **Public versioning begins at `1.0`.**  
> Versions below `1.0` reflect planning and structuring — not published revisions.

---

## 🏁 Version `1.0` — Initial Public Release  
**Status:** Pending publication  
**Date:** TBA

### Included Files

| File | Purpose |
|------|---------|
| `README_recipes.md` | Entry point and learning path |
| `rag_repair_recipe.md` | Component recipe: retrieval drift (`D5_information`) |
| `tool_agent_recipe.md` | Component recipe: tool drift (`D4_tool`) |
| `memory_alignment_recipe.md` | Component recipe: context drift (`D2_context`) |
| `reentry_orchestration_recipe.md` | System recipe: unified runtime orchestration (`RE*`) |

### Intent for v1.0

- Examples are runnable using **local dependencies only**
- Recipes illustrate canonical PLD event handling (`D*`, `R*`, `RE*`, `OUT*`)
- Recipes align with operational metrics described in:  
  `docs/07_pld_operational_metrics_cookbook.md`

---

## 🧩 Pre-Release Notes (Design Rationale — Not Versioned Changes)

These notes document architectural reasoning that informed the structure of v1.0.

### Decision #01 — Recipe Scope
- Recipes demonstrate **real agent behaviors**, not abstract templates
- Examples include the full PLD cycle:  
  **Detection → Repair → Reentry → Continue → Outcome**

### Decision #02 — Folder Placement
Recipes reside under:

```
/quickstart/patterns/04_integration_recipes/
```


Rationale: supports a coherent learning arc:  
`overview → primitives → patterns → recipes`.

### Decision #03 — Two-Tier Structure
- Tier 1: Component patterns (RAG, Tools, Memory)
- Tier 2: Orchestration pattern (runtime control)

This avoids misinterpretation: recipes are **compositional building blocks**, not alternatives.

### Decision #04 — Repair UX Default
- Default pattern uses **visible repair messaging**
- Silent repair is documented as an **optional advanced variation**

### Decision #05 — Observability Principle
- Examples emit structured PLD logs aligned with:

```
pld_runtime/01_schemas/pld_event.schema.json
```


---

## Contribution Guidelines

Future revisions should:

- Maintain alignment with core PLD vocabulary
- Preserve metric compatibility (`PRDR`, `VRL`, `REI`)
- Remain runnable in a minimal local environment

Changes to taxonomy or orchestration behavior must also update:  
`/quickstart/_meta/MIGRATION.md`

---

Maintainer: **Kiyoshi Sasano**
