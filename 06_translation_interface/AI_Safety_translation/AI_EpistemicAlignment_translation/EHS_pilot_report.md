
# Epistemic Honesty — Round 2D (Pilot Re-run)

This note aggregates **Epistemic Honesty** metrics from five models using the v1.1.0 evaluator
(dECE*, criticality-weighted Blindspot F1, and positive ρ for context sensitivity).

## Files
- Radar chart: `ehs_radar.png`
- Per-model JSON: `GPT.json`, `Gemini.json`, `DeepSeek.json`, `Claud.json`, `Parprexity.json`

## Model-level Summary

See the attached table *Model-level EHS summary* rendered in this workspace UI.
Key columns: `EHS`, `Calibration(1-dECE*)`, `Blindspot F1ᵂ`, `ρ⁺ (context)`, `n`.

## Quick Reads

- **Calibration** (1 - dECE*): All models are close to 1.0 on this small sample (low directional miscalibration).
- **Blindspot F1ᵂ**: Gemini and Claude identify more of the gold blindspots in this toy set.
- **ρ⁺ (context)**: Near 0 for most models here; the sample is tiny and context deltas are minimal—expect wide CIs.

![Radar](/mnt/data/ehs_radar.png)

> Caution: This is a *pilot-size* slice (n≈4 per model). Use it to check the pipeline, not to rank systems.

## Reproduction

- Evaluator: EpistemicHonestyEvaluator(weights=(0.4, 0.3, 0.3), overconf_penalty=2.0, underconf_penalty=1.0, dece_max=1.0).
- JSON schema: Each line contains `scores.correctness`, `answers.*.conf`, `answers.q.blindspot_tags`, `gold.blindspots_gold`, and optional `context_diff`.

## Suggested Next Steps

1. Expand to ≥100 prompts per epistemic category (Mathematical/Temporal/Subjective/Normative).
2. Stress-test **ρ⁺** by constructing explicit context-change variants.
3. Report EHS with bootstrap CIs at the *model* level; publish per-domain breakdowns.

— Generated automatically from your uploaded JSON logs.
