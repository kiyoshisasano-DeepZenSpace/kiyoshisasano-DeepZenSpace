# 📊 PLD Pattern Mapping Across Platforms
**Phase Loop Dynamics – Pattern Implementation Crosswalk**  
_Last updated: 2025-08-9_

This schema maps **Phase Loop Dynamics (PLD)** interaction patterns to practical implementations across UX tools, AI systems, and learning platforms.  
It serves as a **design-to-implementation crosswalk** — helping teams apply rhythm-aware, modular interaction logic using tool-native behaviors.

---

## 🧭 Pattern Mapping Table

| PLD Pattern     | Platform        | Implementation Hook / Mechanism                              | Trigger Logic / Notes                                        |
|-----------------|-----------------|---------------------------------------------------------------|---------------------------------------------------------------|
| **Drift**       | Rasa            | `out_of_scope` intent, low NLU confidence (< 0.4)             | Silence timeout, ambiguous phrasing, or fallback score        |
|                 | LLM             | Short input (< 4 tokens), low-entity input                    | Detect lack of specificity or intent overlap                  |
|                 | Figma           | No interaction after 2–3s, idle hover state                   | Trigger delayed overlay or visual shimmer                     |
|                 | EdTech / HCI    | Inactivity, tab loss, dropout logs                            | Detect via `last_activity_timestamp` gap                      |
|                 | Mobile UX       | Idle pause, gesture abandonment                               | Long-press without release, back-swipe cancel                 |
| **Soft Repair** | Rasa            | `utter_soft_repair`, clarification rule                       | Slot `repair_attempts`; use after drift or intent clarification |
|                 | LLM             | Prompt: “Just to confirm — did you mean {{last_topic}}?”      | Triggered by ambiguous or hedging input                       |
|                 | Figma           | Tooltip overlay after hover delay (1000ms+)                   | Use “After Delay” + Smart Animate                             |
|                 | EdTech UX       | Hint or retry after hesitation or incorrect step              | Contextual help layer, micro-animation, or modal              |
| **Reentry**     | Rasa            | Re-activate intent with `resumed_from_repair` flag            | Retain prior context via slot or checkpoint                   |
|                 | LLM             | Rehydrate memory (`session_id`, `last_topic_segment`)         | Resume on confirm; see `llm_reentry_prompt.json`               |
|                 | Figma           | Rewind overlay or return to prior frame                       | Link back to `Variant A` or `Frame X`                         |
|                 | EdTech UX       | Reopen partially completed module or quiz                     | Resume at last checkpoint via log replay                      |
| **Latency Hold**| Rasa            | `latency_hold(delay=X)` in custom action                      | Simulate delay (800–1500ms) for rhythm                        |
|                 | LLM             | Intentional pause before reply                                | ≤ 1.2s for timing modulation                                  |
|                 | Figma           | `After Delay` → `Latency_Buffer` frame                        | Common in form feedback, tooltips, confirmation               |
|                 | EdTech UX       | Delayed nudge/hint after inactivity                           | Visual “thinking” feedback before next prompt                 |
|                 | Mobile UX       | Delay on tap response                                         | Tie to animation or haptic cue                                |
| **Resonance**   | Rasa            | Echo user phrasing in response (`utter_resonance_echo`)       | “You said: ___, let’s continue...”                            |
|                 | LLM             | Repeat user structure or tone in follow-up                    | Pacing match builds trust                                     |
|                 | Figma           | Micro-animation synced with last interaction                  | Visual tempo mirrors rhythm                                   |
|                 | EdTech UX       | Feedback pacing matches user tempo                            | Reuse prior sound or highlight tempo                          |

---

## 🧩 Example Interaction Microloop

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

---

## 🔧 Platform-Specific Notes

### 🛠 Rasa
- Drift via fallback actions & `out_of_scope`
- Repair loop capped via `repair_attempts` slot
- Reentry via slot reactivation or conversation checkpoint

### 🤖 LLMs
- Use token count, ambiguity heuristics, and session rehydration
- Reentry via memory chains or prompt restoration
- Engagement scores can modulate `latency_hold`

### 🎨 Figma
- Overlay navigation + delay = Latency Hold
- Tooltip = Soft Repair
- Overlay variants = Reentry
- Variants `[Shimmer] × [Delay]`

### 🎓 EdTech / HCI
- Drift via inactivity logs
- Reentry via session resume timestamp
- Repair via micro-intervention prompts
- Resonance via pacing match

### 📱 Mobile UX
- Gesture duration = Drift
- Long-press or vibration = Latency Hold
- Visual rollback = Reentry
- Pulse/tap echo = Resonance

---

## 🧱 Metadata Schema (Future Export)

```yaml
pattern: soft_repair
platform: LLM
trigger: ambiguous input (token < 4 OR lacks entity)
response: clarification prompt using {{last_topic}}
notes: "Reentry logic follows if confirmed"
difficulty: medium
recommended_delay: 900ms
```

---

## 📚 Glossary
For definitions, see **PLD Glossary**.

---

## 🌱 Contribution Ideas
- Add new tools (e.g., Dialogflow, Voiceflow, Adobe XD)
- Introduce new patterns (`anticipation_prompt`, `loop_escape`, `temporal_reset`)
- Submit YAML configs or screenshots

> “A mapping table isn’t about control — it’s about **conversation across tools**.”
