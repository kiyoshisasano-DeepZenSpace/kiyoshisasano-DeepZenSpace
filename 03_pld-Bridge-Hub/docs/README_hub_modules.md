<!--
Revision notes (2025-08-09)
- Consolidates module/template overviews into a single, skimmable index.
- Keeps legacy pages for link-compatibility; updates will happen here first.
- Do NOT rename to README.md (reserved elsewhere).
-->

# PLD Bridge Hub — Modules & Templates Index

**One-line role:** The hub that connects **PLD theory (01)** to **implementation kits (02)**, gathering modules and UI templates partners actually use.

---

## Quick Access
- 🧰 **Notion UI Templates**  
  → [ UX Pause & Rhythm Tracker – Starter Kit](https://platinum-arch-69c.notion.site/UX-Pause-Rhythm-Tracker-Starter-Kit-2430fc4951e8809481f6c77478a64535)

- 📘 **Theoretical Foundations**  
  → [Zenodo Papers & Definitions](../docs/zenodo_paper_links.md)

- ▶️ **One-command Demo**  
  → `./DEMORUN.md` (generates 6 sample events, validates, writes a mini report)

- 📊 **Metrics Schemas**  
  → YAML: `../02_quickstart_kit/30_metrics/schemas/metrics_schema.yaml`  
  → JSON Schema: `../02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`

- 🧮 **Math Appendix**  
  → `../01_phase_loop_dynamics/PLD_Mathematical_Appendix.md`

- 🗺 **PLD Flow Diagram**  
  → `../01_phase_loop_dynamics/10_phase_loop_dynamics.svg`

---

## Module Index (this folder)
> Pick a module below; when emitting events, conform to the schemas linked above.

- **Pause Classifier Bot**  
  File: `./structure_generators/pause_classifier_bot.py`  
  Classifies pause types (e.g., cognitive vs UI friction) for pacing decisions.

- **Latency Tracker**  
  Guide: `./structure_generators/README_latency_tracker.md`  
  Script: `./latency_tracker.py`  
  Detects pause durations and logs `latency_hold`–style signals.

- **Reentry Detector**  
  Guide: `./structure_generators/README_reentry_detector.md`  
  Script: `./reentry_detector.py`  
  Finds when users resume an earlier intent (reentry success/anchor).

- **Trace Generator**  
  Script: `./generate_trace.py` (input: `./input_trace.txt`)  
  Produces toy traces you can further classify or validate.

- **Pause Classifier (heuristic)**  
  Script: `./pause_classifier.py`  
  Labels pauses with simple thresholds; useful for non-LLM pipelines.

---

## Recommended Workflow
1. **Scope in Notion** → define contexts (screens/intents), cues (silence, ambiguity), thresholds (e.g., silence > 5s).  
2. **Run the Demo** → `DEMORUN.md` to see valid PLD events & the mini report.  
3. **Choose a Module** → classifier/tracker/reentry as needed for your platform.  
4. **Emit Events** → log fields that match the **YAML/JSON schemas**.  
5. **Validate & Inspect** → re-run the demo validator; compare with your dashboards.

---

## Compatibility & Updates
- This page **consolidates** content previously split across:
  - `notion_ui_templates/NOTION_TEMPLATES_OVERVIEW.md` (kept for link compatibility)
  - `structure_generators/GENERATOR_MODULES_OVERVIEW.md`
  - `structure_generators/README_structure_generators.md`
- As we simplify, **updates will land here first**. Legacy pages may be retired later, but links above will remain valid until then.

---

## License
**CC BY-NC 4.0** — attribution required; **no commercial use**.  
See `../LICENSE` for details.

---

## See also
- Landing & role routing → `./INDEX.md`  
- Hub overview → `./README_stub.md`
