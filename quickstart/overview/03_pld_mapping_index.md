# 📚 PLD Mapping Index – Quick Reference

_Last updated: 2025-08-09_

This document serves as the **navigation hub** for all Phase Loop Dynamics (PLD) term mappings, linking interaction primitives to academic theory, mathematical definitions, and platform-specific equivalents.

---

## 🔍 How to Navigate

| Task | Go To | Notes |
|------|-------|-------|
| Find a PLD term’s academic equivalents | [`pld_to_academic.md`](../../01_phase_loop_dynamics/related_work/pld_to_academic.md) | Forward mapping |
| Look up an academic term to find the PLD concept | [`academic_to_pld_reverse.md`](../../01_phase_loop_dynamics/related_work/academic_to_pld_reverse.md) | Reverse mapping |
| Check symbol/operator-level definitions | [`PLD_Mathematical_Appendix.md`](../../01_phase_loop_dynamics/PLD_Mathematical_Appendix.md) | See eq. refs |
| Confirm stability & safe usage | [`PLD_LEXICON_SAFE_USAGE_GUIDE.md`](../../01_phase_loop_dynamics/PLD_LEXICON_SAFE_USAGE_GUIDE.md) | Tier/stability table |
| See inter-term edges (graph/table) | [`PLD_Lexicon_Connectivity_Map.md`](../../01_phase_loop_dynamics/PLD_Lexicon_Connectivity_Map.md) | Mermaid + table |

---

## 🧩 Key Mapping Resources

### 1. **Canonical Data & Sources**
- [`mapping.canonical.yaml`](../../01_phase_loop_dynamics/related_work/mapping.canonical.yaml) – **Single source of truth**
- [`references.bib`](../../01_phase_loop_dynamics/related_work/references.bib) – Auto-generated from canonical YAML

### 2. **Generated Views**
- **Forward Mapping:** [`pld_to_academic.md`](../../01_phase_loop_dynamics/related_work/pld_to_academic.md)  
- **Reverse Mapping:** [`academic_to_pld_reverse.md`](../../01_phase_loop_dynamics/related_work/academic_to_pld_reverse.md)

### 3. **Mathematical Operators**
| Symbol | Name | Equation Ref | Notes |
|--------|------|--------------|-------|
| 𝒟 | Drift operator | (1.3) | Linked to MI + vector angle |
| ℛ | Repair operator | (1.5) | Gaussian kernel φ(τ) |
| 𝓛ᵢ | Loop generator | (3.2) | 1–5 primitive loops |
| Σ | Phase space | (1.2) | Product of syntax × time × prosody |
| C(σ,t) | Coherence field | (1.4) | MI + embedding cosine |

---

## 🛠 Platform Mapping Quick Table

| Platform  | PLD Equivalent | Example |
|-----------|----------------|---------|
| **Rasa**  | Drift → Repair | FallbackAction + slot retention |
| **Figma** | Latency Hold   | Overlay delay (800–1500 ms) |
| **LLM**   | Reentry        | Context-anchored prompt |
| **EdTech**| Dropout repair | Resume lesson checkpoint |

→ For full mappings, see [`schema_mapping_table.md`](../02_pattern_examples/schema_mapping_table.md).

---

## 📌 Maintenance Rules

1. **Do not** hand-edit generated mapping files (`pld_to_academic.md`, `academic_to_pld_reverse.md`).  
2. Update `mapping.canonical.yaml` and run the generator:  
   ```bash
   python generate_mappings.py
   ```
3. Keep equation numbers stable for cross-references.

---

> “Mappings are not translations — they’re resonance bridges.”  
> — *Phase Loop Dynamics*
