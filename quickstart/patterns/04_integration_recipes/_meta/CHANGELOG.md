---
title: "Integration Recipes — CHANGELOG"
versioning: "Semantic Versioning (SemVer)"
status: "Pre-Release"
maintainer: "Kiyoshi Sasano"
---

# Changelog — Integration Recipes

This changelog documents the evolution of the integration recipes folder inside the Quickstart section.

> **Public versioning starts at `1.0`.**  
> Versions below `1.0` represent **planning and formation notes**, not published changes.

---

## 🏁 Version `1.0` — Initial Public Release  
**Status:** Not yet published  
**Date:** TBA

### Contents included in first release:

| File | Purpose |
|------|---------|
| `README_recipes.md` | Entry point and learning path |
| `rag_repair_recipe.md` | Component recipe: retrieval drift (`D5_information`) |
| `tool_agent_recipe.md` | Component recipe: tool drift (`D4_tool`) |
| `memory_alignment_recipe.md` | Component recipe: memory/state drift (`D2_context`) |
| `reentry_orchestration_recipe.md` | System recipe: unified orchestration (`RE*`) |

### Design Intent for v1.0

- Recipes must be runnable with **local dependencies only**
- All examples emit canonical PLD signals (`D*`, `R*`, `RE*`, `OUT*`)
- Recipes align operationally with metrics in:  
  `docs/07_pld_operational_metrics_cookbook.md`

---

## 🧩 Pre-Release Notes (Planning History)

> These are not version changes — they document reasoning that led to the final structure.

### Decision #01 — Recipe Scope
- Recipes must demonstrate **real agent behaviors** (not theoretical templates)
- Each recipe should show:  
  **Detection → Repair → Reentry → Continue → Outcome**

### Decision #02 — Folder Placement
- Recipes are placed under:  

```
/quickstart/patterns/04_integration_recipes/
```

- Rationale: consolidates learning flow into a single discoverable path  
  (`overview → primitives → patterns → recipes`)

### Decision #03 — Two-Tier Structure
- Tier 1 = Component patterns (RAG / Tools / Memory)
- Tier 2 = System pattern (orchestration)
- Rationale: avoids misinterpretation (recipes are not alternatives, but building blocks + assembly).

### Decision #04 — Default Repair UX
- Default implementation uses **visible repair messaging**
- Silent repair is included as an **optional advanced variation**

### Decision #05 — Observability Constraint
- All recipes must log structured PLD events compatible with:

```
pld_runtime/01_schemas/pld_event.schema.json
```

---

## Contribution Rules

- All future modifications must:
  - Preserve PLD vocabulary alignment
  - Maintain metric compatibility (`PRDR`, `REI`, `VRL`)
  - Remain locally runnable
- Changes affecting structure or signals require a note in:  
  `/quickstart/_meta/MIGRATION.md`

---

Maintainer: **Kiyoshi Sasano**
