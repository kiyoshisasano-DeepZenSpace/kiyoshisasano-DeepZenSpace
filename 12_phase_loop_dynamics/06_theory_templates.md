# 🧪 Theory Templates – Guided Syntax and Structural Triggers

This module defines foundational **PLD templates** that support:
- Dialogue generation
- Structural annotation
- Drift-feedback loop modeling

Templates reflect recurring **interactional structures** across loops, enabling simulation and interpretation of phenomena like drift, mimicry, silence, and reentry.  
Templates may be used in **annotated logs**, **synthetic dialogue agents**, or **loop-aware NLP models**.

---

## 🎭 Template Types and Functions

| Template Type         | Function Description                                 | Example Start                               | Loop Affiliation |
|-----------------------|------------------------------------------------------|----------------------------------------------|------------------|
| Drift-Induction       | Triggers deviation from structural clarity           | “It started making sense, but then…”         | Loop_02          |
| Mimicry-Alignment     | Recalls tone/syntax from earlier segment             | “It feels like I said this already…”         | Loop_05          |
| Silence-Recovery      | Resurfaces from withheld phrase or blank segment     | “There was something I didn’t say…”          | Loop_03          |
| Cue-Based Restart     | Prompts reentry into interrupted or failed phase     | “Actually, maybe what I meant was…”          | Loop_02, Loop_04 |
| Feedback Reflex       | Redirects structure through self-monitoring repair   | “I think that wasn’t quite right…”           | Loop_04          |

---

## 🧩 Structural Skeletons

### 🌀 Drift-Induction Template
- **Pattern**: `[Initial Clarity] → [Interruption] → [Semantic Slip] → [Reformulation or Silence]`  
- **Example**: “I thought I had it… but somehow it slipped. Now I’m not sure what I was saying.”  
- **Loop**: Loop_02  
- **Safe Terms**: `Drift`, `Segment`

---

### 🎯 Mimicry–Resonance Template
- **Pattern**: `[Reference to Prior Tone] → [Echo Phrase] → [Emotive Anchor or Drift]`  
- **Example**: “It sounded like what I said earlier… but I wasn’t really trying to repeat it.”  
- **Loop**: Loop_05  
- **Safe Terms**: `Resonance`, `Alignment`

---

### 🤐 Latent Phase Template
- **Pattern**: `[Blocked Intent] → [Pause or Blank] → [Surfacing Cue or Segment]`  
- **Example**: “There was a phrase I meant to say… but it never came out.”  
- **Loop**: Loop_03  
- **Safe Terms**: `Silence`, `Latent Phase`, `Cue`

---

### 🔄 Cue–Repair Template
- **Pattern**: `[Incomplete Phrase] → [Self-Cue Insertion] → [Clarification Attempt]`  
- **Example**: “Wait—what I really meant was…”  
- **Loop**: Loop_02, Loop_04  
- **Safe Terms**: `Cue`, `Feedback`

---

## 🛠 Template Generation Parameters

| Parameter        | Value Example         | Type         |
|------------------|------------------------|--------------|
| Cue Strength     | `soft`, `urgent`, `implicit` | Qualitative |
| Drift Direction  | `semantic`, `tonal`, `structural` | Categorical |
| Mimicry Target   | `last phrase`, `prior speaker`, `self` | Referential |
| Silence Marker   | `pause`, `ellipsis`, `missing term` | Symbolic |
| Feedback Mode    | `internal`, `explicit`, `looped` | Behavioral |

Templates can be dynamically selected or composed based on these parameters to model variation in discourse patterns.

---

## 📚 Applications

PLD templates enable:

### 🏷️ Annotation
- Tagging speech data with structural labels (e.g., `Cue`, `Drift`)
- Identifying loop boundaries and transitions

### 🧠 Simulation
- Creating failure-repair cycles in synthetic corpora
- Testing loop chaining under latent conditions

### 🤖 Generation
- Producing loop-aware utterances in chat agents
- Building mimicry or reentry-aware response strategies

---

## 🧬 Template Set References

| Template ID                  | Loop | Description                               | File Path                                |
|-----------------------------|------|-------------------------------------------|-------------------------------------------|
| `loop02_driftrepair_002`    | 02   | Cue-based reentry from segment loss       | `/loop_templates/loop02_driftrepair_002.j2` |
| `loop03_latentsilence_003`  | 03   | Silence before structure emergence        | `/loop_templates/loop03_latentsilence_003.j2` |
| `loop04_feedbackinternal_004` | 04   | Feedback reflex for prior phase           | `/loop_templates/loop04_feedbackinternal_004.j2` |
| `loop05_alignmentresonance_003` | 05   | Mimicry with tone anchoring               | `/loop_templates/loop05_alignmentresonance_003.j2` |

Template naming convention: `loop[loopID]_[description]_[version]`  
→ This enables version control and automated parsing.

---

## 🔗 Related Modules

- [`04_structural_units_index.md`](./04_structural_units_index.md): Unit data with loop alignments
- [`05_chain_mappings.md`](./05_chain_mappings.md): Loop sequence patterns
- [`/templates/term_entry.*.j2`](./templates/): Reusable Jinja2 variants
- [`glossary_academic_mapping_v2.md`](./glossary_academic_mapping_v2.md): Definitions and theoretical lineage

---

> “Every template is a map of possibility — how a phrase can break, return, or echo.”
