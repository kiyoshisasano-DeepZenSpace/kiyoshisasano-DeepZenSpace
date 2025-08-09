# REDIRECTS — Quickstart Kit v2025-08-09

This file lists legacy → new paths for backward compatibility.  
Use it to configure redirects in static site generators, documentation tooling, or web server rules.

---

## Old → New Path Mapping

/01_getting_started/Quickstart.md              /00_overview/quickstart.md
/01_getting_started/pld_core_summary.md        /00_overview/pld_theory_summary.md
/01_getting_started/usage_notes.md             /00_overview/usage_notes.md

/02_pattern_examples/figma_latency_hold.md     /20_patterns/ux/figma_latency_hold.md
/02_pattern_examples/llm_reentry_prompt.json   /20_patterns/llm/reentry_prompt.json
/02_pattern_examples/rasa_soft_repair.yml      /20_patterns/rasa/soft_repair.yml
/02_pattern_examples/rasa_soft_repair_actions.py /20_patterns/rasa/soft_repair_actions.py
/02_pattern_examples/schema_mapping_table.md   /20_patterns/mapping/schema_mapping_table.md

/03_metrics_tracking/drift_event_logging.md    /30_metrics/guides/drift_event_logging.md
/03_metrics_tracking/metrics_schema.yaml       /30_metrics/schemas/metrics_schema.yaml
/03_metrics_tracking/pld_event.schema.json     /30_metrics/schemas/pld_event.schema.json
/03_metrics_tracking/reentry_success_dashboard.json /30_metrics/dashboards/reentry_success_dashboard.json

---

## Usage Example (Netlify `_redirects` file format)]

/01_getting_started/Quickstart.md /00_overview/quickstart.md 301
/02_pattern_examples/figma_latency_hold.md /20_patterns/ux/figma_latency_hold.md 301

---

## Usage Example (Apache `.htaccess`)
Redirect 301 /01_getting_started/Quickstart.md /00_overview/quickstart.md
Redirect 301 /02_pattern_examples/figma_latency_hold.md /20_patterns/ux/figma_latency_hold.md


---

## Maintenance

- Keep this list updated for **at least one full release cycle** after migration.
- Remove stale redirects only after confirming no external references remain.
