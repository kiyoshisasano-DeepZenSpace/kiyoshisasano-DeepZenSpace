# 🗺️ PLD Lexicon Connectivity Map (v0.5)

> **Purpose:**  
> This document provides a **structural overview of lexical relationships** within the  
> Phase Loop Dynamics (PLD) framework. It is designed to help researchers, developers,  
> and collaborators navigate **core**, **support**, and **derived** terms, and to understand  
> how they interact in models, implementations, and theoretical mappings.

---

## 📖 How to Read This Map

- **@core** → Foundational concepts that anchor other terms and model logic.  
- **@support** → Contextual terms that rely on core terms for structure.  
- **@derived** → Emergent concepts formed by interaction between terms or states.  
- **Stability Indicators** (🟢 🟡 🔴) follow the [Lexicon Tiering Guide](./LEXICON_TIERING_GUIDE.md).

> **Reference:**  
> - [Lexicon Tiering & Usage Stability Guide](./LEXICON_TIERING_GUIDE.md)  
> - [PLD Glossary & Academic Mapping](./12_phase_loop_dynamics/09_glossary_academic_mapping.md)  

---

## 🔗 Connectivity Overview

```mermaid
graph TD
    Drift["@core Drift 🔴"] --> Repair["@core Repair 🟢"]
    Drift --> PhaseBoundary["@derived Phase Boundary 🟡"]
    Repair --> Resonance["@derived Resonance 🔴"]
    Phase["@core Phase 🟢"] --> PhaseBoundary
    Rhythm["@support Rhythm 🟡"] --> Phase
    Silence["@support Silence 🟡"] --> Repair
    Coherence["@derived Coherence 🟡"] --> Phase
    LatentPhase["@derived Latent Phase 🔴"] --> Coherence
```
---

## 🧩 Term Relationship Table

| Source Term              | Target Term                | Relation Type    | Notes                                                     |
|--------------------------|----------------------------|------------------|-----------------------------------------------------------|
| Drift `@core` 🔴         | Repair `@core` 🟢          | Sequential link  | Drift often triggers repair events.                      |
| Drift `@core` 🔴         | Phase Boundary `@derived` 🟡 | Causal link      | High drift magnitude can mark boundaries.                 |
| Repair `@core` 🟢        | Resonance `@derived` 🔴    | Recursive link   | Repair can create rhythmic echoes.                        |
| Phase `@core` 🟢         | Phase Boundary `@derived` 🟡 | Structural link  | Boundaries segment the phase space.                       |
| Rhythm `@support` 🟡     | Phase `@core` 🟢           | Modulatory link  | Temporal pacing influences phase transitions.             |
| Silence `@support` 🟡    | Repair `@core` 🟢          | Trigger link     | Silence can initiate repair sequences.                    |
| Coherence `@derived` 🟡  | Phase `@core` 🟢           | Evaluative link  | Coherence measures phase alignment.                       |
| Latent Phase `@derived` 🔴 | Coherence `@derived` 🟡   | Hypothetical link| Possible but unverified relationship.                     |

---

## 🧭 Usage Scenarios

- **Researchers** → Map conceptual dependencies before extending the PLD framework.  
- **Engineers** → Identify stable anchor terms for API or SDK parameter naming.  
- **Designers** → See how timing and rhythm terms connect to core structures.  

---

## 📌 Update Notes

- **v0.5** — Added stability indicators, inline role tags, and links to related docs.  
- Diagram converted to Mermaid for GitHub compatibility.  
- Added “How to Read” section for onboarding.  

---

## 📘 Citation

**Phase Loop Dynamics — Lexicon Connectivity Map (v0.5)**  
<https://github.com/kiyoshisasano-DeepZenSpace>  

> These mappings are **structural guides**, not fixed taxonomies.  
> Lexical connectivity is a **field map** — it evolves as the framework matures.
