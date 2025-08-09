# LLM Patterns — Reentry & Soft Repair (PLD-aligned)

This folder provides **drop-in prompt patterns** for Phase Loop Dynamics (PLD), focusing on:
- **L2:** Drift → Repair loop (soft clarification, capped)
- **L3:** Latency operator (optional timing hints to the UI layer)
- **Reentry:** “Resume where you left off” with an anchored context

The patterns are aligned with:
- **Lexicon & Stability:** `01_phase_loop_dynamics/PLD_LEXICON_SAFE_USAGE_GUIDE.md` (v0.6)
- **Operators:** 𝒟 (Drift), ℛ (Repair), 𝓛₃ (Latency), 𝓛₅ (Alignment/Resonance)
- **Metrics schema:** `02_quickstart_kit/30_metrics/schemas/pld_event.schema.json` and `metrics_schema.yaml`

## What’s inside

- `reentry_prompt.json` — A structured prompt template with slots/guards:
  - Performs soft clarification (**ℛ**) when confidence is low or input is ambiguous
  - Emits **reentry candidates** when prior context is available
  - Avoids infinite clarification loops by enforcing **attempt caps**
  - Suggests optional **latency hold** to the UI layer (𝓛₃ hint only; no actual sleep in LLM)

## Quick Use

1. Load `reentry_prompt.json` and fill the placeholders (ALL_CAPS).
2. Pass `session_state` with:
   - `prior_context_id` (if any),
   - `drift_count` (integer, capped at 2),
   - `ui_state` (optional),
   - `last_user_utterance`.
3. Log events on your side according to the PLD schema:
   - `drift_detected`, `repair_triggered`, `repair_failed`, `reentry_success`, `latency_hold`.

> Validation:
> Use `02_quickstart_kit/30_metrics/datasets/pld_events_demo.jsonl` with  
> `02_quickstart_kit/30_metrics/schemas/pld_event.schema.json`.

## Output Contract (recommended)

Your LLM orchestration should expect **JSON** from the model:

```json
{
  "action": "soft_repair" | "reentry" | "answer" | "handoff",
  "message": "string (user-facing text)",
  "reentry": {
    "prior_context_id": "uuid-or-stable-id",
    "resume_hint": "string (optional)"
  },
  "telemetry": {
    "suggest_latency_ms": 900,
    "reason": "soft_repair_probe"
  }
}
```
## LLM Pattern Operational Rules

- **If** `action = "soft_repair"` → Show clarification UI; log `repair_triggered`.
- **If** `action = "reentry"` → Restore context; log `reentry_success`.
- **If** `telemetry.suggest_latency_ms` is present → UI may render latency hold; log `latency_hold` with `duration_ms`.

### Safety Notes
- Do **not** let the model sleep or loop — timing is a UI responsibility (𝓛₃).
- Cap repair attempts: after two failed clarifications, switch to `"handoff"` or `"answer"` fallback.
- Never fabricate `prior_context_id`. If missing, perform a single soft repair and then handoff.

### See Also
- `20_patterns/rasa/` — Minimal L2 demo wired to the same metrics.
- `30_metrics/` — Schema, validator, demo datasets, dashboards.

---

# 20_patterns/llm/reentry_prompt.json

```json
{
  "name": "PLD Reentry / Soft Repair Prompt",
  "version": "1.1",
  "role_system": "You are an interaction assistant implementing PLD (Phase Loop Dynamics). You must:\n- Treat hesitation/ambiguity as structural drift (D), not failure.\n- Use soft clarification (R) at most 2 times.\n- If a prior context anchor exists, propose a safe reentry.\n- Do not perform delays; only SUGGEST latency_ms to the UI when helpful (L3 hint).\n- Return a single JSON object matching the output contract. Do not include explanations.",
  "instructions": [
    "Given the current user input and session_state, decide whether to:",
    "1) ask a gentle clarification (soft_repair),",
    "2) resume prior context (reentry),",
    "3) answer directly (answer), or",
    "4) escalate/handoff (handoff).",
    "Constraints:",
    "- If session_state.drift_count >= 2 → avoid more repair; prefer 'handoff' or minimal 'answer'.",
    "- If session_state.prior_context_id is present and input aligns → prefer 'reentry'.",
    "- If input is short/ambiguous and drift_count < 2 → prefer 'soft_repair'.",
    "- Never block; never wait. Timing is suggested via telemetry.suggest_latency_ms.",
    "Output ONLY valid JSON per the contract."
  ],
  "placeholders": {
    "PRODUCT_OR_DOMAIN": "string: what this assistant is about, e.g., 'course enrollment' or 'support triage'",
    "PRIOR_CONTEXT_SNIPPET": "string: brief summary of prior context if available, may be empty",
    "CONFIDENCE": "number in [0,1] from upstream ranker or heuristic",
    "MAX_REPAIR_ATTEMPTS": "integer, usually 2"
  },
  "input_schema": {
    "session_state": {
      "type": "object",
      "required": ["session_id", "drift_count"],
      "properties": {
        "session_id": { "type": "string" },
        "drift_count": { "type": "integer" },
        "prior_context_id": { "type": "string" },
        "ui_state": { "type": "string" },
        "last_user_utterance": { "type": "string" }
      }
    },
    "env": {
      "type": "object",
      "properties": {
        "product_or_domain": { "type": "string" },
        "max_repair_attempts": { "type": "integer" },
        "confidence": { "type": "number" }
      }
    }
  },
  "few_shots": [
    {
      "comment": "Low confidence + no prior context → soft repair, with latency suggestion (UI will render, not the model).",
      "input": {
        "session_state": {
          "session_id": "S1",
          "drift_count": 0,
          "last_user_utterance": "asdfgh"
        },
        "env": {
          "product_or_domain": "support triage",
          "max_repair_attempts": 2,
          "confidence": 0.28
        }
      },
      "target": {
        "action": "soft_repair",
        "message": "Just to confirm — are you asking about our services, billing, or technical support?",
        "telemetry": {
          "suggest_latency_ms": 900,
          "reason": "soft_repair_probe"
        }
      }
    },
    {
      "comment": "User affirms and we have a prior context → propose reentry.",
      "input": {
        "session_state": {
          "session_id": "S1",
          "drift_count": 1,
          "prior_context_id": "4e42a31c-da05-4f35-be08-dea7cc4f6912",
          "last_user_utterance": "yes"
        },
        "env": {
          "product_or_domain": "support triage",
          "max_repair_attempts": 2,
          "confidence": 0.84
        }
      },
      "target": {
        "action": "reentry",
        "message": "Great, resuming your previous context.",
        "reentry": {
          "prior_context_id": "4e42a31c-da05-4f35-be08-dea7cc4f6912",
          "resume_hint": "Continue the triage flow from the last confirmed step."
        }
      }
    },
    {
      "comment": "Exceeded repair cap → handoff.",
      "input": {
        "session_state": {
          "session_id": "S2",
          "drift_count": 2,
          "last_user_utterance": "??"
        },
        "env": {
          "product_or_domain": "course enrollment",
          "max_repair_attempts": 2,
          "confidence": 0.19
        }
      },
      "target": {
        "action": "handoff",
        "message": "Let me route you to a safer option. Would you like a quick menu or a human handoff?"
      }
    }
  ],
  "runtime_notes": [
    "When 'soft_repair' is returned: log 'repair_triggered'.",
    "When 'reentry' is returned: log 'reentry_success' with prior_context_id.",
    "When 'telemetry.suggest_latency_ms' exists: log 'latency_hold' with 'duration_ms'.",
    "Always validate your event logs using the provided schema and validator."
  ]
}
