# 🧪 Generative Sandbox with Structural Controls

**Status**: Unresolved  
**Thread**: [`thread_generation_control`](../../thread_generation_control)

---

## 🎯 Key Question

Can we build an interactive sandbox where users directly manipulate structural features—like spiral depth, fault lines, or echo loops—and watch the model regenerate text accordingly?

---

## 🧠 Overview

This sandbox operationalizes the *Phase Drift* metaphor space. Instead of merely visualizing syntax maps, users become **topographic composers**—modulating recursion, rhythm, tone, and narrative structure through interactive controls.

Inspired by modular synthesis (e.g., Ableton Live, VCV Rack), this tool treats structure as a **generative instrument**.

---

## 🎛️ Parameter Mapping: Metaphor → Modulation

| Control           | Metaphor           | Effect                                                                 |
|-------------------|--------------------|------------------------------------------------------------------------|
| `Spiral Depth`    | Recursion           | Increases clause embedding and recursive phrasing                     |
| `Phase Jump`      | Rupture             | Triggers semantic or tonal shift                                      |
| `Resonance Loop`  | Repetition          | Re-invokes prior content thematically or rhythmically                 |
| `Fault Line`      | Disruption          | Introduces syntactic fracture or genre shift                          |
| `Flatten Syntax`  | Simplicity          | Reduces parse depth; uses shorter clauses                             |
| `Semantic Echo`   | Memory              | Periodically resurfaces earlier concepts                              |
| `Deformalize`     | Tone Shift          | Switches to colloquial or informal register                           |

These controls can be layered and chained for dynamic output shaping.

---

## ⚙️ Technical Foundations

### 1. Prompt Engineering as Control Tokens

Each control is implemented via prompt scaffolds or hidden tags.  
Examples:
- `#REPEAT_EVERY_50`: resurface concept every 50 tokens
- `#FLATTEN`: reduce syntactic depth progressively

### 2. Latent Modulation Techniques

- Prompt tuning or embedding injection to modulate generation styles
- Attention re-weighting for drift and echo behavior

### 3. Real-Time Feedback Loop

- Decode in token segments
- Evaluate rhythm, parse depth, or phase zone
- Use evaluation results to modify ongoing generation

---

## 🖥️ Interface Concept: The Generative Instrument

### 🔹 Modular Control Panel

Sliders and knobs for:

- Spiral depth
- Drift rate
- Loop intensity
- Syntax granularity

Each tweak updates output preview live.

### 🔹 Terrain View

- Topographic map (from `structure_topograph.svg`)
- Visual feedback for:
  - Fault lines
  - Echo nodes
  - Drift zones

### 🔹 Interaction Examples

- Drag “echo node” → reintroduces earlier phrase
- Dial “phase jump” to 80% → splits narrative path
- Draw fault line at token 150 → tone shifts to second-person reflection

---

## 🧪 Use Case Matrix

| Use Case           | Goal                             | Controls Used                  |
|--------------------|----------------------------------|--------------------------------|
| Narrative Forking  | Branch story midstream           | `Phase Jump + Doubling`        |
| Poetic Generation  | Induce recursive rhythm          | `Spiral + Resonance Loop`      |
| LLM Behavior Test  | Observe coherence under drift    | `Loop + Drift Modulation`      |
| Syntax Learning    | Visualize structural depth       | `Spiral + Flatten + Faultline` |

---

## ⚠️ Challenges & Design Notes

| Challenge                         | Solution Strategy                                                |
|----------------------------------|------------------------------------------------------------------|
| Metaphor ≠ Model Output          | Human-in-the-loop calibration, user testing of control accuracy  |
| Coherence loss from perturbation | Incremental generation with scaffolding re-anchoring             |
| UI complexity                    | Group controls into "Structure / Flow / Tone" modules            |
| Effect measurement               | Use live syntax visualization + optional user rating input       |

---

## 🚀 Roadmap

### ✅ MVP: Mini Generator

- [ ] OpenAI API + Streamlit or React UI  
- [ ] Controls: `Spiral`, `Echo`, `Flatten`  
- [ ] Output + parser overlay preview

### 🔄 Feedback-Linked Loop

- [ ] Integrate `spaCy` for syntax tree and zone mapping  
- [ ] Display terrain movement over token windows

### 🧩 Phase Drift Control Language (PDCL)

Define structural behavior inline via meta-tags:

```text
#DRIFT 0.3 | #REPEAT 40t | #JUMP @150 | #FLATTEN zone3
```
---

## 📁 Suggested Assets

| File Name                  | Purpose                                          |
|----------------------------|--------------------------------------------------|
| `generative_sandbox.md`    | Spec document (this file)                        |
| `pdcl_prompt_templates.txt`| Prompt scaffolding templates                     |
| `sandbox_ui_mockup.svg`    | Interface sketch                                |
| `drift_control_map.csv`    | Control–effect mapping table                     |
| `structure_topograph.svg`  | Phase Drift terrain base map                    |

---

## 🧠 Final Note

> “Structure is not fixed—it’s playable.”

The *Generative Sandbox* turns structural metaphors into expressive control levers, bridging analytical linguistics and real-time creative interaction.

Would you like help mocking up the UI (`sandbox_ui_mockup.svg`) or implementing a control scaffold (`pdcl_prompt_templates.txt`)?
