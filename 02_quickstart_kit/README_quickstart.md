# 🚀 PLD Quickstart Kit

The **Phase Loop Dynamics (PLD)** kit provides reusable interaction design patterns for designers, engineers, and product teams. It bridges theory and practice across NLU, LLMs, UI prototypes, and metrics logging.

---

## 📁 Folder Structure

```
13_quickstart_kit/
├── README_quickstart.md          ← You are here
│
├── 01_getting_started/           ← Start here: key principles + usage advice
│   ├── Quickstart.md             ← Intro to PLD: loop overview and principles (5 min read)
│   ├── pld_core_summary.md       ← Core PLD concepts: drift, repair, reentry (3 min read)
│   └── usage_notes.md            ← Tips for implementation, testing, extensibility (5–8 min)
│
├── 02_pattern_examples/          ← Drop-in patterns for real platforms
│   ├── figma_latency_hold.md         ← UX latency buffers in Figma flows
│   ├── llm_reentry_prompt.json       ← Reentry prompt template for LLM flows
│   ├── rasa_soft_repair.yml          ← Repair logic (NLU/rules) for Rasa bots
│   ├── rasa_soft_repair_actions.py   ← Custom repair loop handling via Rasa actions
│   └── schema_mapping_table.md       ← PLD patterns mapped to platform behaviors
│
├── 03_metrics_tracking/          ← Logging + dashboard templates
│   ├── drift_event_logging.md        ← How to detect, log, and interpret drift
│   ├── metrics_schema.yaml           ← YAML schema for PLD event logging
│   ├── pld_event.schema.json         ← JSON Schema version of metrics spec
│   └── reentry_success_dashboard.json← Example analytics dashboard (e.g. PostHog)
```

---

## 🔁 PLD Pattern Microloop

PLD defines interaction rhythm as a **loop** of signal and adaptation:

```
User hesitates or diverges → [Drift]
      ↓
System probes softly       → [Repair]
      ↓
User resumes               → [Reentry]
      ↓
System modulates tempo     → [Latency Hold / Resonance]
                             (e.g., pause, shimmer, echo phrase)
```

This replaces rigid fallback logic with **graceful recovery patterns**.

---

## 🧪 Pattern Examples (02_pattern_examples)

| File                         | Description                                              |
|------------------------------|----------------------------------------------------------|
| `rasa_soft_repair.yml`       | PLD-style fallback logic in Rasa using repair_attempts   |
| `rasa_soft_repair_actions.py`| Custom repair escalation logic (prevents infinite loops) |
| `figma_latency_hold.md`      | Prototyping hesitation delays using frames & overlays    |
| `llm_reentry_prompt.json`    | LLM prompt templates for context-aware reentry           |
| `schema_mapping_table.md`    | Crosswalk between PLD terms and tool-specific mappings   |

---

## 📊 Metrics & Logging (03_metrics_tracking)

| File                          | Role                                                        |
|-------------------------------|-------------------------------------------------------------|
| `metrics_schema.yaml`         | Event + metric structure (drift, repair, reentry, latency)  |
| `pld_event.schema.json`       | JSON Schema for event log validation                        |
| `drift_event_logging.md`      | Logging strategy and trigger mechanisms                     |
| `reentry_success_dashboard.json` | Sample dashboard to visualize recovery flows              |

⏱ Metrics like `drift_to_repair_ratio`, `reentry_success_rate`, and `avg_latency_hold` help track **system rhythm and resilience**.

---

## 📚 Foundational Reading (01_getting_started)

Start with:

- `Quickstart.md`: High-level PLD introduction and flow sketch (5 min read)
- `pld_core_summary.md`: Concept definitions with examples (3 min read)
- `usage_notes.md`: Best practices, edge cases, implementation caveats (5–8 min)

---

## 🔗 Tool-Specific Highlights

| Platform     | PLD Mapping Examples                                 |
|--------------|------------------------------------------------------|
| **Rasa**     | `out_of_scope`, `repair_attempts`, fallback layering |
| **LLM**      | time-gap reentry triggers, ambiguity detection       |
| **Figma**    | `after delay`, `opacity fade`, shimmer overlays      |
| **PostHog**  | Drift heatmaps, funnel tracking, reentry latency plots |

→ See `schema_mapping_table.md` for a full breakdown.

---

## 🧠 Who Is This For?

| Role            | Value                                               |
|------------------|----------------------------------------------------|
| Conversation UX  | Repair/reentry scaffolds, pacing-aware design      |
| LLM Engineers    | Reentry prompts, ambiguity handling scaffolds      |
| Product Analysts | Drift heatmaps, latency metrics, recovery rates    |
| QA/Support       | Dropout → recovery flow validation                  |
| EdTech Designers | Dropout → return logic, engagement pacing          |

---

## 🛠 Getting Started

Start with `Quickstart.md`, then try a live pattern:

- Rasa bot repair logic → `rasa_soft_repair.yml` + `rasa_soft_repair_actions.py`
- UI prototype delay → `figma_latency_hold.md`
- LLM memory recovery → `llm_reentry_prompt.json`
- Drift observability → `drift_event_logging.md`

💡 All pattern examples are file-based — no live server needed to explore the logic.

---

## 🧩 Extending PLD

You can add new pattern primitives:

```yaml
pattern: anticipation_prompt
trigger: hesitation OR context_switch
action: preload_response_option
log_event: anticipation_prompt_triggered
```

→ See `metrics_schema.yaml` or `pld_event.schema.json` for logging field templates.

---

## 📬 Feedback / Contributing

Found an edge case or want to contribute?

- Fork and add a new pattern example (e.g. for mobile UI, AR, call center UX)
- Suggest a new metric, pattern, or platform mapping
- Submit a PR or open an issue on [GitHub](https://github.com/kiyoshisasano-DeepZenSpace)

---

> PLD is not a rulebook.  
> It’s a rhythm you can work with.  
> Don’t force it — feel it, adapt it.
