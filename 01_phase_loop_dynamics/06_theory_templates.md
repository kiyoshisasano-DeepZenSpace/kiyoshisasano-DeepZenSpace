# 🧪 Theory Templates — Guided Syntax and Structural Triggers (Integrated Edition)

This module defines **Phase Loop Dynamics (PLD) templates** that act as reusable structural blueprints for:

- Dialogue generation
- Structural annotation
- Drift–feedback loop modeling

Templates capture **recurring interactional structures** across loops $(\mathcal{L}_i)$, enabling simulation and analysis of drift $(\mathcal{D})$, mimicry, silence, and reentry $(\mathcal{R})$.  
They may be embedded in **annotated logs**, **synthetic dialogue agents**, or **loop-aware NLP systems**.

---

## 🎭 Template Types and Functions

| Template Type       | Function                                             | Example Start                                    | Loop Affiliation |
|---------------------|------------------------------------------------------|--------------------------------------------------|------------------|
| Drift Induction     | Triggers deviation from structural clarity           | “It started making sense, but then…”             | $\mathcal{L}_2$  |
| Mimicry Alignment   | Recalls tone/syntax from earlier segment              | “It feels like I said this already…”             | $\mathcal{L}_5$  |
| Silence Recovery    | Resurfaces from withheld phrase or blank segment      | “There was something I didn’t say…”              | $\mathcal{L}_3$  |
| Cue-Based Restart   | Prompts reentry into interrupted or failed phase      | “Actually, maybe what I meant was…”               | $\mathcal{L}_2$, $\mathcal{L}_4$ |
| Feedback Reflex     | Redirects structure via self-monitoring repair        | “I think that wasn’t quite right…”               | $\mathcal{L}_4$  |

---

## 🧩 Structural Skeletons

### 🌀 Drift Induction
- **Pattern**: `[Initial Clarity] → [Interruption] → [Semantic Slip] → [Reformulation or Silence]`  
- **Example**: “I thought I had it… but somehow it slipped.”  
- **Loop**: $\mathcal{L}_2$  
- **Safe Terms**: `Drift`, `Segment`

### 🎯 Mimicry–Resonance
- **Pattern**: `[Reference to Prior Tone] → [Echo Phrase] → [Emotive Anchor or Drift]`  
- **Example**: “It sounded like what I said earlier… but I wasn’t trying to repeat it.”  
- **Loop**: $\mathcal{L}_5$  
- **Safe Terms**: `Resonance`, `Alignment`

### 🤐 Latent Phase
- **Pattern**: `[Blocked Intent] → [Pause] → [Surfacing Cue or Segment]`  
- **Example**: “There was a phrase I meant to say… but it never came out.”  
- **Loop**: $\mathcal{L}_3$  
- **Safe Terms**: `Silence`, `Latent Phase`, `Cue`

### 🔄 Cue–Repair
- **Pattern**: `[Incomplete Phrase] → [Self-Cue Insertion] → [Clarification Attempt]`  
- **Example**: “Wait—what I really meant was…”  
- **Loop**: $\mathcal{L}_2$, $\mathcal{L}_4$  
- **Safe Terms**: `Cue`, `Feedback`

---

## 🛠 Template Parameters

| Parameter       | Example Value               | Type         |
|-----------------|-----------------------------|--------------|
| Cue Strength    | `soft`, `urgent`, `implicit`| Qualitative  |
| Drift Direction | `semantic`, `tonal`, `structural` | Categorical |
| Mimicry Target  | `last phrase`, `prior speaker`, `self` | Referential |
| Silence Marker  | `pause`, `ellipsis`, `missing term` | Symbolic    |
| Feedback Mode   | `internal`, `explicit`, `looped`     | Behavioral  |

Templates can be dynamically composed from these parameters to model discourse variation.

---

## 📚 Applications

### 🏷 Annotation
- Tagging utterances with structural labels (`Cue`, `Drift`, etc.)
- Marking loop boundaries and transitions

### 🧠 Simulation
- Generating failure–repair cycles in synthetic corpora
- Stress-testing loop chaining under latent-phase conditions

### 🤖 Generation
- Producing loop-aware utterances in conversational AI
- Implementing mimicry- and reentry-aware response strategies

---

## 🧬 Template Set References

| Template ID                        | Loop             | Description                           | File Path                                          |
|------------------------------------|------------------|---------------------------------------|----------------------------------------------------|
| `loop02_driftrepair_002`           | $\mathcal{L}_2$  | Cue-based reentry from segment loss   | `/loop_templates/loop02_driftrepair_002.j2`        |
| `loop03_latentsilence_003`         | $\mathcal{L}_3$  | Silence before structure emergence    | `/loop_templates/loop03_latentsilence_003.j2`      |
| `loop04_feedbackinternal_004`      | $\mathcal{L}_4$  | Feedback reflex for prior phase       | `/loop_templates/loop04_feedbackinternal_004.j2`   |
| `loop05_alignmentresonance_003`    | $\mathcal{L}_5$  | Mimicry with tone anchoring           | `/loop_templates/loop05_alignmentresonance_003.j2` |

**Naming convention**:  
`loop[loopID]_[description]_[version]` → supports version control and automated parsing.

---

## 🔗 Related Modules
- [`04_structural_units_index.md`](./04_structural_units_index.md) — Unit data with loop alignments  
- [`05_chain_mappings.md`](./05_chain_mappings.md) — Loop sequence patterns  
- [`/templates/term_entry.*.j2`](./templates/) — Reusable Jinja2 variants  
- [`09_glossary_academic_mapping.md`](./09_glossary_academic_mapping.md) — Definitions and theoretical lineage

---

> *“Each template is a map of possibility — showing how a phrase can break, return, or echo.”*
