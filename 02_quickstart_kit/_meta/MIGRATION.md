# MIGRATION — Quickstart Kit v2025-08-09

This document describes the migration from the **old Quickstart Kit directory structure** to the **new, role-oriented structure**.  
Follow these steps to preserve Git history, avoid link breakage, and align terminology with the PLD core theory.

---

## 1. File Moves (with `git mv`)

Refer to the **Old → New Mapping Table** below. Always use `git mv` to retain history.

| Old Path | New Path |
|---|---|
| `01_getting_started/Quickstart.md` | `00_overview/quickstart.md` |
| `01_getting_started/pld_core_summary.md` | `00_overview/pld_theory_summary.md` |
| `01_getting_started/usage_notes.md` | `00_overview/usage_notes.md` |
| `02_pattern_examples/figma_latency_hold.md` | `20_patterns/ux/figma_latency_hold.md` |
| `02_pattern_examples/llm_reentry_prompt.json` | `20_patterns/llm/reentry_prompt.json` |
| `02_pattern_examples/rasa_soft_repair.yml` | `20_patterns/rasa/soft_repair.yml` |
| `02_pattern_examples/rasa_soft_repair_actions.py` | `20_patterns/rasa/soft_repair_actions.py` |
| `02_pattern_examples/schema_mapping_table.md` | `20_patterns/mapping/schema_mapping_table.md` |
| `03_metrics_tracking/drift_event_logging.md` | `30_metrics/guides/drift_event_logging.md` |
| `03_metrics_tracking/metrics_schema.yaml` | `30_metrics/schemas/metrics_schema.yaml` |
| `03_metrics_tracking/pld_event.schema.json` | `30_metrics/schemas/pld_event.schema.json` |
| `03_metrics_tracking/reentry_success_dashboard.json` | `30_metrics/dashboards/reentry_success_dashboard.json` |

---

## 2. Update Internal References

- Update all **relative links** in `README_quickstart.md` to match the new directory structure.
- In each `.md` file, update “See also” sections to reference:
  - `../01_phase_loop_dynamics/PLD_Mathematical_Appendix.md`
  - `../01_phase_loop_dynamics/related_work/pld_to_academic.md`
  - `../01_phase_loop_dynamics/related_work/academic_to_pld_reverse.md`

---

## 3. Compatibility Redirects

- Maintain backward compatibility for automated documentation builds and external links.
- List all old → new paths in `_meta/REDIRECTS.md`.
- If hosting on GitHub Pages, configure `.htaccess` or `_redirects` accordingly.

---

## 4. Terminology Alignment (PLD Lexicon v0.6)

- **Drift** → “Structural Drift” (𝒟) — specify type (topic / structural / semantic)
- **Repair** → “Cue-Driven Repair” (ℛ) — specify self/other-initiated
- **Latent Phase** → “Latent Phase” (𝓛₃) — specify cognitive/system context
- **Resonance** → “Resonance” (𝓛₅) — specify level (lexical, prosodic, stance)
- **Coherence** → “Coherence Field” (C(σ,t))

---

## 5. Metrics Schema Consistency

- Ensure all fields in `30_metrics/schemas/*` match the notation in the Mathematical Appendix.
- Add explicit links to formula references for:
  - `drift_to_repair_ratio`
  - `reentry_success_rate`
  - `avg_latency_hold`

---

## 6. Validation

After migration:

```bash
# Check moved files
git status

# Verify all markdown links
npx markdown-link-check '**/*.md'

# Commit migration
git add .
git commit -m "Migrate Quickstart Kit to role-oriented structure"
```

---


## 7. Versioning Note
This migration corresponds to Quickstart Kit v2025-08-09.
Future changes to directory layout should be documented in _meta/CHANGELOG.md and appended here.
