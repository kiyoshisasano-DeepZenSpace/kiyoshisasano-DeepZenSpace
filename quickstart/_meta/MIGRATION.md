# MIGRATION GUIDE — Quickstart Kit (2025 Structure)

This guide documents the transition from earlier ad-hoc folder organization to the current **role-based applied PLD format**.

---

## 1. File Moves

Use `git mv` when restructuring to retain commit history.

| Old Path | New Path |
|---------|----------|
| `/01_getting_started/*` | `/overview/*` |
| `/02_patterns/*` | `/patterns/*` |
| `/03_metrics/*` | `/metrics/*` |
| `/operator_primitives_v1/*` | `/operator_primitives/*` |

---

## 2. Naming Rules

| Rule | Example |
|------|---------|
| Sequential files use numbers | `01_detect_drift.md` |
| Folder-level entry file uses no prefix | `README_patterns.md` |
| Scripts/tools remain unversioned | `langgraph_example.md`, `rasa_soft_repair.yml` |

---

## 3. Backwards Compatibility

If hosting docs, configure redirects using `_meta/REDIRECTS.md`.  
Keep redirect mapping for **one major release cycle** before removal.

---

## 4. Terminology Updates

Replace legacy terms:

| Old term | New term |
|---------|----------|
| "repair strategy" | "Soft/Hard Repair primitive" |
| "classification flags" | "PLD event schema fields" |
| "stabilization" | "Resonance (L5)" |

---

## 5. Verification

After migration:

```bash
npx markdown-link-check '**/*.md'
```
Maintain this document only when structural changes occur.