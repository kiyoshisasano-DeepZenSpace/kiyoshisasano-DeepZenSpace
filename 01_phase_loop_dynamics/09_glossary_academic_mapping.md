# 📘 Phase Loop Dynamics × Academic Frameworks — Academic Glossary Index (v0.6)

This page is a **lightweight index** that points to the authoritative sources for PLD term mappings and formal definitions.

- **Canonical data & mappings:** maintained in `related_work/mapping.canonical.yaml`
- **Auto-generated mapping (forward):** `related_work/pld_to_academic.md` (PLD ➜ Academic)
- **Auto-generated mapping (reverse):** `related_work/academic_to_pld_reverse.md` (Academic ➜ PLD)
- **Mathematical definitions & theorems:** `PLD_Mathematical_Appendix.md`
- **Lexicon stability & usage guardrails:** `PLD_LEXICON_SAFE_USAGE_GUIDE.md`
- **Term connectivity (graph/table):** `PLD_Lexicon_Connectivity_Map.md`

---

## 🔎 How to Use

1. **Find a PLD term’s academic equivalents**  
   → See **Forward Mapping**: `related_work/pld_to_academic.md`

2. **Look up a discipline term to find the PLD concept**  
   → See **Reverse Mapping**: `related_work/academic_to_pld_reverse.md`

3. **Check symbol/operator-level definitions**  
   → See **Mathematical Appendix**: `PLD_Mathematical_Appendix.md`  
   - 𝒟 (Drift operator): §1.4  
   - ℛ (Repair operator): §1.5  
   - 𝓛ᵢ (Loop generators): §1.6 / §3.2  
   - Σ (Phase space): §1.2  
   - C(σ,t) (Coherence field): §1.4

4. **Confirm stability & safe usage**  
   → `PLD_LEXICON_SAFE_USAGE_GUIDE.md` (v0.6)

5. **See inter-term edges (graph/table)**  
   → `PLD_Lexicon_Connectivity_Map.md` (v0.6)

---

## 🔁 Removed Redundant Sections (What moved where?)

The previous integrated glossary duplicated materials now **centralized** elsewhere:

- **Term-to-academic tables (e.g., Segment Drift, Latent Phase, Resonance, Alignment, Repair, Phase Boundary, Coherence, Rhythm, Silence)**  
  → **Consolidated** into `mapping.canonical.yaml` and auto-generated:  
  `related_work/pld_to_academic.md` (forward) / `related_work/academic_to_pld_reverse.md` (reverse).

- **Mathematical mappings, theorems, empirical validation, code snippets**  
  → **Authoritative** in `PLD_Mathematical_Appendix.md` (no change needed).

This page now serves as a **navigation index** to avoid divergence between hand-written glossaries and generated mappings.

---

## 🔮 Appendix: Future Mappings (Exploratory)

> These are **tentative hypotheses** for future inclusion. Do **not** treat as canonical mappings.

| PLD Term             | Tentative Academic Equivalent | Field                          |
|----------------------|--------------------------------|--------------------------------|
| `Drift Shell`        | Topic Continuity Envelope     | Discourse Modeling             |
| `Syntax Fog Field`   | Parse Entropy Field           | Computational Linguistics      |
| `Resonance Bridge`   | Echo Trigger                  | Discourse Theory, Cognitive Poetics |
| `Phase Rupture`      | Transitional Grammar Fault    | Prompt Engineering, Psycholinguistics |
| `Recursive Topology` | Fractal Construction Modeling | Complexity Science, Syntax Theory |

> When any of the above matures, add to `mapping.canonical.yaml` and regenerate mappings.

---

## 📝 Maintenance Note

- **Single source of truth:** `related_work/mapping.canonical.yaml`  
- **Do not** hand-edit: `pld_to_academic.md`, `academic_to_pld_reverse.md`  
- References emitted to: `related_work/references.bib` (auto-generated from YAML `references:`)
