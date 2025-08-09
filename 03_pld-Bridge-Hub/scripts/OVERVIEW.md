<!--
Revision notes (2025-08-09)
- Script entrypoint list with safety notes.
-->

# Scripts Overview — PLD Bridge Hub

Minimal helpers to run the demo and validations.

## Files
- `validate_events.sh` — wrapper that calls `python bootstrap_demo.py`  
  - Use when you prefer a shell one-liner (`bash scripts/validate_events.sh`).
  - Windows (PowerShell) users: run `python .\bootstrap_demo.py` directly.

## Notes
- The demo writes outputs under `./demo_quick/`:
  - `events_demo.jsonl` — synthetic PLD events
  - `demo_report.md` — simple counts & demo metrics
- If you keep a **local copy of `pld_event.schema.json`** alongside `bootstrap_demo.py`, the validator will pick it up automatically (repo path is checked first, then local).
