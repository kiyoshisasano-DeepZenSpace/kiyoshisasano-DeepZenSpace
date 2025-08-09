# Implementation Contract — Events & Metrics (Runtime)

**This file is the single source of truth for runtime contracts.**

## Event Schema (JSON)
- Canonical JSON Schema: `../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`
- **latency_hold** events MUST include:
  - `session_id` (string)
  - `metadata.duration_ms` (number ≥ 0)

## Metrics (Naming & Formulas)
- Canonical YAML: `../02_quickstart_kit/30_metrics/schemas/metrics_schema.yaml`
- Key metrics: `drift_to_repair_ratio`, `reentry_success_rate`, `avg_latency_hold`, `time_to_repair`

## Emission Rules
- Timestamps: ISO8601 (UTC)
- Pseudonymize user identifiers before aggregation
- Keep `context_id` stable across reentry

## Validation
- Preferred: run `jsonschema` against the canonical schema
- Demo path: `DEMORUN.md` (one-command)

## Versioning
- Changes to schemas require: docs update + minor version bump + demo regeneration
