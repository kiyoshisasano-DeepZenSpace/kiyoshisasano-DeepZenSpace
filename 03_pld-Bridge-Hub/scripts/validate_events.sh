#!/usr/bin/env bash
# PLD Bridge Hub — Event Validator
# Usage:
#   ./scripts/validate_events.sh
#     -> runs bootstrap_demo.py (generate + validate + report)
#
#   ./scripts/validate_events.sh /path/to/events.jsonl [/path/to/pld_event.schema.json]
#     -> validates an existing JSONL against the schema (jsonschema required)

set -euo pipefail

# --- prerequisites ---
if ! command -v python >/dev/null 2>&1; then
  echo "[error] Python is required (python not found in PATH)." >&2
  exit 1
fi

# --- paths ---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --- MODE A: no args -> run bootstrap_demo.py as-is ---
if [ $# -eq 0 ]; then
  echo "[info] No args: running bootstrap_demo.py (generate + validate + report)"
  python "${REPO_ROOT}/bootstrap_demo.py"
  exit $?
fi

# --- MODE B: validate an existing JSONL ---
EVENTS_PATH="$1"
SCHEMA_PATH="${2:-${REPO_ROOT}/../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json}"

if [ ! -f "${EVENTS_PATH}" ]; then
  echo "[error] Events file not found: ${EVENTS_PATH}" >&2
  exit 2
fi

python - "$EVENTS_PATH" "$SCHEMA_PATH" <<'PY'
import sys, json, pathlib
events_path = pathlib.Path(sys.argv[1]).resolve()
schema_path = pathlib.Path(sys.argv[2]).resolve()

FALLBACK_SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["event_type", "timestamp"],
  "properties": {
    "event_type": {
      "type": "string",
      "enum": [
        "drift_detected","repair_triggered","repair_failed",
        "reentry_success","reentry_anchor_set","reentry_missing_anchor",
        "repair_escalation","latency_hold"
      ]
    },
    "timestamp": { "type": "string", "format": "date-time" },
    "session_id": { "type": "string" },
    "metadata": { "type": "object" }
  },
  "additionalProperties": True,
  "allOf": [
    {
      "if": { "properties": { "event_type": { "const": "latency_hold" } } },
      "then": {
        "required": ["event_type","timestamp","session_id"],
        "properties": {
          "metadata": {
            "type": "object",
            "properties": {
              "duration_ms": { "type": "number", "minimum": 0 },
              "reason": { "type": "string" }
            },
            "additionalProperties": True
          }
        }
      }
    }
  ]
}

try:
    import jsonschema
    from jsonschema import Draft7Validator
except Exception:
    print("[error] Python package 'jsonschema' is required for validation.\n"
          "        Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(3)

# Load schema (repo schema preferred)
if schema_path.exists():
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        print(f"[info] Using schema: {schema_path}")
    except Exception as e:
        print(f"[warn] Failed to read schema at {schema_path}: {e}\n"
              f"       Falling back to embedded minimal schema.", file=sys.stderr)
        schema = FALLBACK_SCHEMA
else:
    print(f"[info] Repo schema not found at {schema_path}. Using fallback schema.", file=sys.stderr)
    schema = FALLBACK_SCHEMA

validator = Draft7Validator(schema)
valid = 0
errors = []
counts = {}
total_lines = 0

with events_path.open("r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if not line.strip():
            continue
        total_lines += 1
        try:
            obj = json.loads(line)
        except Exception as e:
            errors.append((i, f"Invalid JSON: {e}"))
            continue
        errs = list(validator.iter_errors(obj))
        if errs:
            for err in errs:
                errors.append((i, err.message))
        else:
            valid += 1
            et = obj.get("event_type", "<none>")
            counts[et] = counts.get(et, 0) + 1

print(f"[ok] Valid events: {valid}/{total_lines}")
if errors:
    print("[fail] Validation errors:")
    for ln, msg in errors:
        print(f"  - line {ln}: {msg}")

if counts:
    print("\n[stats] Event counts:")
    for k in sorted(counts):
        print(f"  - {k}: {counts[k]}")
PY
