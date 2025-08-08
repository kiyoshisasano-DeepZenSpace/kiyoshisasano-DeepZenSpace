# ⚡ Quickstart – Phase Loop Dynamics (PLD)

**Phase Loop Dynamics (PLD)** is a modular interaction model that treats **drift**, **repair**, and **reentry** as designable, reusable structures — not system failures.  
It helps teams build adaptive, resilient, and rhythm-aware UX across AI tools, learning flows, and dialogue systems.

This quickstart is for **UX designers, AI engineers, and prototypers** who want to implement PLD patterns without reading the full theory.

---

## ▶️ 01. What Is PLD?

PLD models interaction not as a straight line, but as a **looping rhythm** — full of pauses, clarifications, and returns.

> “Drift is not deviation — it’s rhythm under construction.”

**Core idea:**  
When users pause, hesitate, or go off-script…  
Don’t treat it as error — treat it as **structure**.

---

## ▶️ 02. Core Concepts

| Term           | Meaning                                                  | UX Equivalent                    |
|----------------|----------------------------------------------------------|----------------------------------|
| **Drift**        | Delay, ambiguity, or off-path behavior                     | User hesitation, silent exit     |
| **Repair**       | Clarification or re-alignment maneuver                    | Retry prompt, paraphrasing       |
| **Reentry**      | Return to a dropped state or interrupted flow             | “Resume where you left off”      |
| **Latency Hold** | Intentional pause to simulate rhythm or give space        | Delayed tooltip, slow animation  |
| **Resonance**    | Echo or pacing match that affirms timing or intent       | Feedback that mirrors flow tempo |

These are **UX pattern units** — composable across platforms and domains.

---

## ▶️ 03. Sample Loop Pattern

### 🔁 Example: Drift → Repair → Reentry (YAML-style logic)

```yaml
- state: drift_probe
  trigger:
    silence_timeout: 5s
    low_NLU_confidence: <0.45
  action: latency_hold(delay=900ms)

- state: soft_repair
  prompt: "Just to confirm — did you mean [X] or something else?"
  transition:
    user_confirms: reentry_link
    user_denies: repair_escalation

- state: reentry_link
  resume_from: prior_context_id  # Must persist across sessions or form dropouts

- state: repair_escalation
  action: handoff_or_reset_prompt
```
## 🔧 Tip
In Rasa, implement this via `FallbackAction` + slot retention.  
In Figma, simulate reentry via overlay variants keyed to `frame_id`.

---

## ▶️ 04. Adjacent Research & Influences

### Domain vs. PLD Concepts

| Domain                | PLD Concepts                               |
|----------------------|--------------------------------------------|
| Conversation Analysis| repair, latency_hold, drift-loop           |
| Temporal Interaction | resonance, timed pacing                    |
| Cognitive UX         | drift as overload, reentry as relief       |
| Embodied Interaction | field stewardship, relational UX           |

> **PLD reframes rhythm as a design primitive — not just a UX side effect.**

### Selected References

- Drew (1997), *Repair in Conversation*
- Wendy Ju (2015), *Temporal Interaction Design*
- Odom et al. (2014), *Designing for Slowness*
- Sha Xin Wei, *Rhythmic Computation*
- Nielsen, Norman, Raskin — *Error Recovery Models*

---

## ▶️ 05. How to Apply PLD in Existing Platforms

### 🧪 Try These Starter Points

| Platform   | Start With                                                        |
|------------|-------------------------------------------------------------------|
| Rasa Pro   | Fallback + slot retention for repair and reentry                  |
| Maze       | Detect drift via exit behavior or looping screen patterns         |
| Figma      | Reentry via overlays, delayed transitions, pacing overlays        |
| EdTech UX  | Log dropout → repair → return sequences via session metrics       |

---

### 🤝 Contribute Patterns / Demos

You can submit:

- 🧩 New pattern units (e.g., `anticipation_link`, `interrupt_fade`)
- 💬 Alternative terms or simplified developer mappings
- 🎬 Demo GIFs or YAML prompt templates
- 📊 Analytics schema extensions:  
  `drift_detected`, `repair_failed`, `reentry_lag`

- [See `metrics_schema.yaml`](#)  
- [See `llm_reentry_prompt.json`](#)

---

## ▶️ 06. Safety & Loop Handling

PLD emphasizes **recovery without getting stuck in infinite fallback cycles**.

### When implementing:

- ✅ Set max repair attempts or fallback escalation paths  
- ✅ Detect unresolved drift (e.g., no input after repair)  
- ✅ Persist context IDs for reentry logic  
- ✅ Log unresolved loops (`drift_unrecovered`) for dashboard tracking  

- [See `reentry_success_dashboard.json`](#)

---

## ▶️ 07. Visual Overview
```text
PLD Quickstart Flow:
┌────────────────────────────┐
│ 01_getting_started         │ → Theory, onboarding
└────────────┬───────────────┘
             ↓
┌────────────┴───────────────┐
│ 02_pattern_examples        │ → Code, prompts, prototypes
└────────────┬───────────────┘
             ↓
┌────────────┴───────────────┐
│ 03_metrics_tracking        │ → Logging + dashboard specs
└────────────────────────────┘
```
## 📖 Glossary & Term Reference

For complete definitions of PLD pattern terms and roles:  
→ [View the PLD Glossary](#)

---

## 📜 License

**Creative Commons BY-NC 4.0**  
(Open for remixing, research, and non-commercial adaptation)

---

## 📫 Contact

**Created by:** Kiyoshi Sasano  
📩 deepzenspace[at]gmail[dot]com  
🔗 [PLD GitHub Repository](#)

> “Don’t fix the flow — listen to it.”  
> — *Phase Loop Dynamics*

