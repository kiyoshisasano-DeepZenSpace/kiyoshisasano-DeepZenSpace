# 📘 Academic → PLD Reverse Mapping

This document provides a **reverse lookup**: starting from an academic or domain-specific term, you can find the corresponding **Phase Loop Dynamics (PLD)** concept and symbol.  
It is intended as a quick reference for readers coming from linguistics, HCI, AI research, or other disciplines who want to align their terminology with PLD’s phase–loop framework.

---

## 🔄 How to Use

- **Look up** the academic term in the left-hand column  
- **Identify** the PLD equivalent in the middle column  
- **Follow** the symbol reference to find its formal definition in the [Mathematical Appendix](../PLD_Mathematical_Appendix.md) or prose explanation in [`00_introduction.md`](../00_introduction.md)

---

| Academic Term | PLD Term | Symbol / Operator |
|---------------|----------|-------------------|
| Structural priming | Resonance loop | 𝓛₅ |
| Turn-taking repair | Cue-driven repair | ℛ |
| Syntactic drift | Drift operator | 𝒟 |
| Prosodic alignment | Alignment tensor | 𝒜⊗𝒜 |
| Disfluency repair | Drift–repair cycle | 𝓛₂ |
| Latent planning phase | Latent phase | 𝓛₃ |
| Sequential organization | Phase topology | Σ |
| Mimicry in dialogue | Resonance loop | 𝓛₅ |
| Interactional echo | Resonance | 𝓛₅ |
| Self-monitoring | Feedback reflex | 𝓛₄ |

> This table is a condensed example. The full mapping is generated from `mapping.canonical.yaml`.

---

## 🛠 Updating This Mapping

1. **Edit** `mapping.canonical.yaml` in the repository root  
2. **Run** the mapping generator script:
   ```bash
   python tools/update_mappings.py
```
3. This will update both:
- `pld_to_academic.md` (forward mapping)  
- `academic_to_pld_reverse.md` (this file)

---

## 🤝 Contribution Guidelines

- Always add **citations** where the academic term is drawn from published work  
- Use **stable references** (DOI, permanent archives)  
- Maintain **one-to-one or one-to-many clarity** — avoid ambiguous mappings without explanatory notes

---

## 📜 License

This mapping is released under **Creative Commons BY-NC 4.0**.  
Non-commercial use is permitted with attribution.

---

> *The reverse mapping is a **bridge** — helping external researchers orient themselves within PLD’s conceptual and formal space.*
