<!--
Revision: 2025-08-09
Role: Code entry for generators. Mirrors theory(01) ↔ quickstart(02).
-->

# Structure Generators — Overview

Use these modules to turn PLD theory into working behaviors.

## Modules
- `latency_tracker.py` — log pause durations to CSV (maps to latency_hold).
- `pause_classifier_bot.py` — classify pause type via LLM (Cognitive / UI Friction / etc.).
- `reentry_detector.py` — detect intent reentry against past segments.

## Quick run
- Latency tracker (local): `python structure_generators/latency_tracker.py`
- Pause classifier (LLM): set `OPENAI_API_KEY` then  
  `python structure_generators/pause_classifier_bot.py`
- Reentry detector (LLM): set `OPENAI_API_KEY` then  
  `python structure_generators/reentry_detector.py`

## Links
- Theory → `../docs/zenodo_paper_links.md`
- Partner index → `../INDEX.md`
- One-command demo → `../DEMORUN.md`

**License:** CC BY-NC 4.0 (attribution required; no commercial use)
