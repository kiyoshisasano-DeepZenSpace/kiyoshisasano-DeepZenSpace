---
title: "Integration Recipes — CHANGELOG"
versioning: "Semantic Versioning (SemVer)"
status: "Active"
maintainer: "Kiyoshi Sasano"
---

# Changelog — Integration Recipes

This changelog documents the evolution of the integration recipe set within the Quickstart section.

> **Public versioning begins at `1.0`.**  
> Versions below `1.0` reflect planning and structuring — not published revisions.

---

## Version `1.1` — Terminology & Framing Refinement  
**Status:** Applied  
**Date:** 2025-11-17

### Summary

This update improves clarity, tone, and positioning across the recipe set.  
All updates maintain backward compatibility — no behavior, structure, or execution flow was changed.

### Changes Included

| Category | Update |
|----------|--------|
| Framework positioning | Added clarification that LangGraph is used as the **demonstration implementation**, not a hard requirement |
| Tone adjustment | Replaced prescriptive wording (`must`, `required`, `production-grade`) with neutral, descriptive phrasing |
| Section naming | Updated `"Runtime Skill Demonstrated"` → `"Example Integration Focus"` |
| Recipe headers | Added framework-agnostic notice to minimal runnable code sections |
| UX semantics | Clarified that visible repair is the **default demonstration style**, while silent repair is an **optional variation** |

### Non-breaking Change Notice

- No taxonomy changes (`D*`, `R*`, `RE*`, `OUT*`)
- No file renaming
- No migration steps required

### Migration Guidance

If downstream projects reference earlier labels such as:

```md
Runtime Skill Demonstrated
Recipes must be runnable
Production-ready agents
```


update them to the new neutral terminology for consistency.

---

## Version `1.0` — Initial Public Release  
**Status:** Published  
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

- Examples runnable with **local dependencies only**
- Recipes demonstrate the complete PLD loop:  
  `Detection → Repair → Reentry → Continue → Outcome`
- PLD logging aligns with operational metrics (`PRDR`, `VRL`, `REI`)  
  and schema under:  
  `pld_runtime/01_schemas/pld_event.schema.json`

---

## Pre-Release Notes (Historical Rationale — Not Versioned)

These notes document key design decisions made before `1.0`.

### Decision #01 — Scope
Recipes demonstrate **real agent behavior**, not abstract templates.

### Decision #02 — Folder Placement

```bash
/quickstart/patterns/04_integration_recipes/
```


Placement supports progressive onboarding:  
`Overview → Patterns → Recipes`.

### Decision #03 — Two-Tier Model

- Tier 1 = Component behavior recipes  
- Tier 2 = System orchestration recipe

Ensures clarity: pieces are composed, not alternatives.

### Decision #04 — UX Defaults

Visible repair is the **default instructional style**.  
Silent repair is documented as **optional advanced UX**.

### Decision #05 — Observability Rule

All recipes emit structured PLD event logs for downstream telemetry.

---

## Contribution Guidelines

Future revisions should:

- Maintain alignment with PLD vocabulary and schema
- Preserve operational metric compatibility
- Remain runnable locally without external infra

Changes affecting runtime control, taxonomy, or orchestration require an entry in:

```bash
/quickstart/_meta/MIGRATION.md
```

---

Maintainer: **Kiyoshi Sasano**
