#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLD Bridge Hub — One-Command Demo Bootstrap
- Creates a minimal demo dataset
- Validates each event against pld_event.schema.json (if found)
- Falls back to an embedded minimal schema if the repo file is not found
- Prints a tiny metrics summary and writes demo_report.md

Usage:
  python bootstrap_demo.py
"""
import json, sys, datetime
from pathlib import Path

# ---------- Paths ----------
HERE = Path(__file__).resolve().parent
# Bridge Hub 直下に置く前提：リポジトリ直下の 02_quickstart_kit を参照
REPO_SCHEMA = (HERE / "../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json").resolve()
OUT_DIR = HERE / "demo_quick"
OUT_DIR.mkdir(parents=True, exist_ok=True)
EVENTS_PATH = OUT_DIR / "events_demo.jsonl"
REPORT_PATH = OUT_DIR / "demo_report.md"

# ---------- Optional import (jsonschema) ----------
try:
    import jsonschema
    from jsonschema import Draft7Validator
    HAS_JSONSCHEMA = True
except Exception:
    HAS_JSONSCHEMA = False

# ---------- Embedded minimal fallback schema ----------
FALLBACK_SCHEMA = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["event_type", "timestamp"],
  "properties": {
    "event_type": {
      "type": "string",
      "enum": [
        "drift_detected",
        "repair_triggered",
        "repair_failed",
        "reentry_success",
        "reentry_anchor_set",
        "reentry_missing_anchor",
        "repair_escalation",
        "latency_hold"
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
        "required": ["event_type", "timestamp", "session_id"],
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

def load_schema():
    if REPO_SCHEMA.exists():
        try:
            return json.loads(REPO_SCHEMA.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[warn] Failed to read schema at {REPO_SCHEMA}: {e}\nUsing fallback schema.", file=sys.stderr)
    else:
        print(f"[info] Repo schema not found at {REPO_SCHEMA}. Using fallback schema.", file=sys.stderr)
    return FALLBACK_SCHEMA

def now_iso():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

# ---------- Create a tiny, valid demo ----------
def write_demo_events():
    sid = "sess_demo_001"
    uid = "user_demo_001"
    rows = [
        {"event_type":"drift_detected","timestamp":now_iso(),"session_id":sid,
         "metadata":{"user_id":uid,"context_id":"screen:search","drift_type":"silence","confidence_score":0.31,"attempt":1}},
        {"event_type":"repair_triggered","timestamp":now_iso(),"session_id":sid,
         "metadata":{"strategy":"soft_repair","latency_before_repair":1.4,"context_id":"screen:search","attempt":1}},
        {"event_type":"latency_hold","timestamp":now_iso(),"session_id":sid,
         "metadata":{"duration_ms": 900.0, "reason":"soft_repair_probe","context":"search_shimmer","user_cancelled": False}},
        {"event_type":"reentry_success","timestamp":now_iso(),"session_id":sid,
         "metadata":{"previous_context_id":"screen:search","reentry_lag":2.3,"reentry_method":"user_initiated","goal_completed": True}},
        {"event_type":"drift_detected","timestamp":now_iso(),"session_id":sid,
         "metadata":{"user_id":uid,"context_id":"screen:checkout","drift_type":"ambiguity","confidence_score":0.29,"attempt":1}},
        {"event_type":"repair_escalation","timestamp":now_iso(),"session_id":sid,
         "metadata":{"from":"soft_repair","to":"hard_repair","reason":"no_response"}}
    ]
    with EVENTS_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(rows)

def validate_events(schema):
    errors = []
    valid = 0
    all_rows = []
    if not HAS_JSONSCHEMA:
        print("[warn] 'jsonschema' not installed. Skipping validation step. Install with: pip install jsonschema", file=sys.stderr)
        return valid, errors, all_rows
    validator = Draft7Validator(schema)
    with EVENTS_PATH.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            obj = json.loads(line)
            all_rows.append(obj)
            errs = sorted(validator.iter_errors(obj), key=lambda e: e.path)
            if errs:
                for e in errs:
                    errors.append((i, e.message))
            else:
                valid += 1
    return valid, errors, all_rows

def summarize(rows):
    from statistics import mean
    by_type = {}
    for r in rows:
        by_type[r["event_type"]] = by_type.get(r["event_type"], 0) + 1

    drift = by_type.get("drift_detected", 0)
    repair = by_type.get("repair_triggered", 0) or 1  # avoid div by zero for demo
    drift_to_repair_ratio = drift / repair

    latency_values = [r.get("metadata",{}).get("duration_ms") for r in rows
                      if r["event_type"] == "latency_hold" and isinstance(r.get("metadata",{}).get("duration_ms"), (int, float))]
    avg_latency_hold = mean(latency_values) if latency_values else 0.0

    reentry_success = by_type.get("reentry_success", 0)
    reentry_success_rate_demo = reentry_success  # demo: numerator only

    return by_type, drift_to_repair_ratio, avg_latency_hold, reentry_success_rate_demo

def write_report(by_type, dtr, avg_lat, re_rate, valid, total, errors):
    lines = []
    lines.append("# PLD Demo Report\n")
    lines.append(f"- Valid events: **{valid}/{total}**")
    if not HAS_JSONSCHEMA:
         lines.append("> NOTE: Validation was skipped because 'jsonschema' is not installed.")
    if errors:
        lines.append("## Validation errors")
        for ln, msg in errors:
            lines.append(f"- line {ln}: {msg}")
    lines.append("\n## Event counts")
    for k,v in sorted(by_type.items()):
        lines.append(f"- {k}: {v}")
    lines.append("\n## Metrics (demo-calculated)")
    lines.append(f"- drift_to_repair_ratio: `{dtr:.2f}`")
    lines.append(f"- avg_latency_hold (ms): `{avg_lat:.1f}`")
    lines.append(f"- reentry_success_rate (demo numerator): `{re_rate}`")
    lines.append("\n> NOTE: `reentry_success_rate` is a demo placeholder (numerator only).")
    lines.append("> NOTE: `drift_to_repair_ratio` uses 1 as denominator fallback when no repair events are present.")
    lines.append("\n---\n_This demo writes UTC ISO8601 timestamps (RFC3339)._")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

def main():
    created = write_demo_events()
    print(f"[ok] Wrote {created} demo events to {EVENTS_PATH}")
    schema = load_schema()
    valid, errors, rows = validate_events(schema)
    total = len(rows) if rows else created
    if HAS_JSONSCHEMA:
        if errors:
            print(f"[fail] {len(errors)} validation error(s):")
            for ln, msg in errors:
                print(f"  - line {ln}: {msg}")
        else:
            print(f"[ok] All {valid}/{total} events validated against schema.")
    else:
        print("[skip] Validation skipped (jsonschema not installed).")

    by_type, dtr, avg_lat, re_rate = summarize(rows if rows else [])
    write_report(by_type, dtr, avg_lat, re_rate, valid, total, errors)
    print(f"[ok] Wrote report to {REPORT_PATH}")
    print("\nNext steps:")
    print("  - Open the report markdown file.")
    print(f"    {REPORT_PATH}")
    print("  - Compare metrics with your dashboard expectations.")
    print("  - Tweak thresholds in your generators/configs if needed.")

if __name__ == "__main__":
    main()
