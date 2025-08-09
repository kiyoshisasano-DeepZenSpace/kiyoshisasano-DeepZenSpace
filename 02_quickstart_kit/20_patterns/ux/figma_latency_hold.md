# 🕒 Latency Hold in Figma — PLD-Compliant Prototype Guide
**File:** `02_quickstart_kit/20_patterns/ux/figma_latency_hold.md`  
**Scope:** UX pattern spec + how-to in Figma + telemetry hooks  
**PLD anchor:** L3 Latency Operator → *Mathematical Appendix* §1.6 (𝓛₃)

---

## Why “Latency Hold” (L3)?
A **Latency Hold** is a *designed* pause that shapes interaction rhythm. It’s not technical lag; it’s a pacing primitive that:
- gives users space to think (structured **silence**),
- avoids abrupt transitions,
- smooths **drift → repair** handoffs,
- and supports trust by making system timing feel intentional.

**Use stable terms** (per Lexicon Guide): *phase*, *timing*, *cue*.  
If you mention **drift**, qualify it (e.g., “silence drift” / “low-confidence drift”).

---

## Quick Recipe (2 frames, 1 overlay)
**Goal:** Form submit → short hold → confirmation

1) Frames:  
   - `Form_Submitted`  
   - `Latency_Buffer` (blank/shimmer)  
   - `Confirmation_Message`

2) Prototype wires:  
   - `Form_Submitted` → `Latency_Buffer`  
     - Trigger: **After Delay** = `0ms` (instant jump)  
   - `Latency_Buffer` → `Confirmation_Message`  
     - Trigger: **After Delay** = `1200ms`  
     - Animation: **Smart Animate** (optional)

3) Visual polish: shimmer, three-dot pulse, or subtle “just a sec…” copy.

> **Operator mapping:** This is 𝓛₃ in action: a time-shift operator `e^{−τ∂_t}` that inserts a bounded pause.

---

## Hesitation Nudge (tooltip variant)
**Scenario:** user hesitates on a field → 1000 ms → helper tooltip

- Base frame + overlay `Tooltip_Prompt`  
- Link: **After Delay** = `1000ms` → **Open Overlay** (bottom-center) → **Fade-in**  
- Make overlay dismissible on click/typing (don’t trap).

---

## Timing Defaults (start here, then A/B)
| Situation           | Initial delay | Notes                          |
|---------------------|---------------|--------------------------------|
| Onboarding step     | 1200–1500 ms  | Slower tempo improves clarity. |
| Clarification hint  | 800–1000 ms   | Gentle, non-blocking prompt.   |
| Power-user flows    | ≤ 800 ms      | Keep momentum; avoid drag.     |

**Anti-patterns:** chaining multiple holds, blocking navigation, using “hold” to mask slow backends.

---

## Reusable Component: `LatencyHold_Frame`
Create a component with variants for quick drop-in:

- **Delay**: `800ms` / `1200ms` / `1500ms`  
- **Style**: `Dots` / `Shimmer` / `Blank`  
- **Overlay**: `Tooltip` / `Loading Icon` / `None`

This enables consistent pacing across screens and easy A/B.

---

## Interrupt Rules (don’t trap users)
If the user acts during a hold:
- **Cancel** the pending transition.
- **Bypass** the overlay and route to the user’s target.
- In Figma: set the overlay interaction to close on click/typing; avoid modal dead-ends.

---

## PLD Flow Snippets
### A. Drift → Hold → Soft Repair → Reentry
```text
User hesitates (silence / low-confidence)
 → LatencyHold(1000–1200ms, shimmer)
   → SoftRepair (gentle confirmation tooltip)
     → Reentry (restore prior context if confirmed)
```

### B. Submit → Hold → Confirmation (Resonance optional)
```text
Submit
 → LatencyHold(1200ms)
   → Confirmation ("Thanks — next step?")
     → Resonance echo (match tempo / phrasing)
```

---

## Telemetry Hooks (aligns with `/30_metrics`)
When you mirror this pattern in code (web/app), log the PLD events so design intent is measurable.

**Event:** `latency_hold`  
```json
{
  "event_type": "latency_hold",
  "timestamp": "2025-08-09T12:00:00Z",
  "session_id": "s-123",
  "metadata": {
    "duration_ms": 1200,
    "reason": "soft_repair_probe",
    "context_id": "frame:Form_Submitted",
    "ui_state": "prototype/form_submit"
  }
}
```

**Related events:**
- `drift_detected` (e.g., silence > 5s / low NLU confidence),
- `repair_triggered` (clarification shown),
- `reentry_success` (user resumes after confirmation).

**Validate logs:** see `/30_metrics/schemas/pld_event.schema.json` and the validator steps in `README_quickstart.md` (they check `metadata.duration_ms` is present).

---

## Accessibility & UX Notes
- Always allow **escape**: click, keypress, or focus change should cancel a hold.
- Communicate state briefly (“One moment…”), but avoid spinner-only ambiguity.
- Respect reduced-motion settings; offer a **Blank** variant.

---

## References & “See also”
- **Operators:** `10_operator_primitives/L3_latency_operator.md`  
- **Metrics:** `30_metrics/schemas/pld_event.schema.json`, `30_metrics/schemas/metrics_schema.yaml`  
- **Rasa demo (L2 + L3):** `20_patterns/rasa/`  
- **Theory anchors:** *PLD Mathematical Appendix* §1.6 (𝓛₃), Lexicon Safe Usage Guide

> **Design mantra:** Don’t fake slowness—**shape** time. The hold is a *phase tool*, not camouflage.
