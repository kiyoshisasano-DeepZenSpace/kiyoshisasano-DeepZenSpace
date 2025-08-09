# 📊 schema_mapping_table.md  
**PLD Pattern Mapping Across Platforms**

_Last updated: 2025-07-31_

This schema maps **Phase Loop Dynamics (PLD)** interaction patterns to practical implementations across UX tools, AI systems, and learning platforms.

It serves as a **design-to-implementation crosswalk** — helping teams apply rhythm-aware, modular interaction logic using tool-native behaviors.

---

## 🧭 Pattern Mapping Table

| PLD Pattern     | Platform      | Implementation Hook / Mechanism                              | Trigger Logic / Notes                                      |
|------------------|----------------|---------------------------------------------------------------|-------------------------------------------------------------|
| **Drift**         | Rasa            | `out_of_scope` intent, low NLU confidence (< 0.4)             | Use `silence_timeout`, ambiguous phrasing, or fallback score |
|                  | LLM             | Short input (< 4 tokens), low-entity input                    | Detect lack of specificity or intent overlap                |
|                  | Figma           | No interaction after 2–3s, idle hover state                   | Trigger delayed overlay or visual shimmer                   |
|                  | EdTech / HCI    | Inactivity, tab loss, dropout logs                           | Use `last_activity_timestamp` gap detection                |
|                  | Mobile UX       | Idle pause, gesture abandonment                              | Long-press without release, back-swipe cancel              |

| **Soft Repair**   | Rasa            | `utter_soft_repair`, clarification rule                      | Slot: `repair_attempts`; use after drift or inform intent   |
|                  | LLM             | Prompt like: “Just to confirm — did you mean {{last_topic}}?” | Triggered by ambiguous or hedging input                     |
|                  | Figma           | Tooltip overlay after hover delay (1000ms+)                  | Use “After Delay” + Smart Animate                          |
|                  | EdTech UX       | Hint or retry after hesitation or incorrect step             | Contextual help layer; micro-animation or modal            |

| **Reentry**       | Rasa            | Re-activate intent with `resumed_from_repair` flag           | Use slot or checkpoint to retain prior context              |
|                  | LLM             | Rehydrate memory (`session_id`, `last_topic_segment`)        | See `llm_reentry_prompt.json`; resume on confirm            |
|                  | Figma           | Rewind overlay or return to previously open frame            | Use prototype link back to `Variant A` or `Frame X`         |
|                  | EdTech UX       | Reopen partially completed module or quiz                    | Resume at last checkpoint via log replay                   |

| **Latency Hold**  | Rasa            | Insert `latency_hold(delay=X)` in custom action               | Simulate system delay (800–1500ms) for rhythm               |
|                  | LLM             | Intentional pause before reply                                | Optional delay (≤ 1.2s) for timing modulation               |
|                  | Figma           | `After Delay` → `Latency_Buffer` frame → content              | Common in form feedback, tooltips, confirmation             |
|                  | EdTech UX       | Delayed nudge/hint after inactivity                           | Visual “thinking” feedback before next prompt               |
|                  | Mobile UX       | Delay on tap response to simulate system thought              | Can be tied to animation or haptic cue                      |

| **Resonance**     | Rasa            | Echo user phrasing in response (`utter_resonance_echo`)      | “You said: ___, let’s continue...”                          |
|                  | LLM             | Repeat user structure or tone in follow-up                    | Pacing match builds trust                                   |
|                  | Figma           | Micro-animation (pulse, shimmer) synced with last interaction | Use visual tempo as rhythm mirror                           |
|                  | EdTech UX       | Feedback pacing matches user tempo                            | Reuse prior sound or highlight tempo                        |

---

## 🧩 Example Interaction Microloop (Cross-Platform)

```plaintext
User hesitates (Drift)
  ↓
System waits 1000ms (Latency Hold)
  ↓
Displays gentle clarification (Soft Repair)
  ↓
User confirms intent
  ↓
System restores last context (Reentry)
  ↓
Echoes tone/pacing (Resonance)
```
## 🔧 Platform-Specific Notes

---

### 🛠 Rasa

- `Drift` via `fallback actions` and `out_of_scope`
- `Repair` loop capped using `repair_attempts` slot
- `Reentry` via **slot reactivation** or **conversation checkpoint**

---

### 🤖 LLMs (LangChain, DSPy, etc.)

- Use **token count**, **ambiguity heuristics**, and **session rehydration**  
- `Reentry` managed via **memory chains** or **prompt restoration**  
- Use **engagement scores** to modulate timing (e.g., dynamic `latency_hold`)

---

### 🎨 Figma

- `Overlay navigation + After Delay` = `Latency Hold`  
- `Tooltip` = `Soft Repair`  
- `Overlay variants` = `Reentry`  
- Components can use **Variants**: `[Shimmer]` × `[Delay]`

---

### 🎓 EdTech / HCI Systems

- `Drift` = Inactivity logs  
- `Reentry` = Session resume timestamp  
- `Repair` = Micro-intervention prompt  
- `Resonance` = Pacing match  
- Use telemetry events:  
  - `drift_detected`  
  - `repair_triggered`  
  - `reentry_success`

---

### 📱 Mobile UX (Preview Inclusion)

- `Gesture duration` = `Drift`  
- `Long-press` or **soft vibration** = `Latency Hold`  
- `Visual rollback` = `Reentry`  
- `Pulse/tap echo` = `Resonance`

---

### 🧱 Metadata Schema (for Future Export)

Each mapping row can be expressed as **structured config** — enabling export into formats like YAML or JSON for implementation or sharing.

```yaml
pattern: soft_repair
platform: LLM
trigger: ambiguous input (token < 4 OR lacks entity)
response: clarification prompt using {{last_topic}}
notes: "Reentry logic follows if confirmed"
difficulty: medium
recommended_delay: 900ms
```

## 📚 Glossary Reference

For term definitions and role-specific usage, see:  
→ [PLD Glossary](#)

---

## 🌱 Contribution Ideas

You can help extend this mapping table by:

- 🛠 **Adding tools**:  
  Dialogflow, Voiceflow, Notion AI, Adobe XD

- 🧩 **Introducing new patterns**:  
  `anticipation_prompt`, `loop_escape`, `temporal_reset`

- 📂 **Submitting artifacts**:  
  Structured YAML or screenshots from actual flows

> “A mapping table isn’t about control —  
> it’s about **conversation across tools**.”

