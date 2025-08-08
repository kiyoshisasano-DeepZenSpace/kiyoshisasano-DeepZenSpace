# 📘 00_introduction.md  
*Phase Loop Dynamics: A Syntax-Centered Model of Structural Drift, Alignment, and Resonance*  

---

## 1. Overview

**Phase Loop Dynamics (PLD)** models conversational syntax as a system of **recursive phase transitions** driven by feedback, drift, and resonance.  
Unlike linear accounts, PLD treats interactional syntax as a **topographic structure** evolving in a *phase space* $\Sigma$ — the set of all possible syntactic states (see [Formal Specification §2.1](../mathematical_appendix/00_formal_specification.md#21-phase-space)).  

These states shift through **loop transformations** $\mathcal{L}_i$ (segment detection, drift–repair, latent phase, feedback reflex, and alignment–resonance), producing dynamic trajectories over *dialogic time*.  

PLD accounts for phenomena such as:  

- Abandoned or fragmented constructions  
- Hesitation, self-repair, and mid-turn revision  
- Syntactic mimicry and phase reentry  
- Silence, latency, and structural disjunction  
- Response chaining and dynamic alignment  

These are unified under a **loop-based account of emergent syntax**, where linguistic form is continuously shaped by internal ($\mathcal{D}$ drift) and external ($\mathcal{R}$ repair) feedback mechanisms.

---

## 2. Motivation

Traditional theories in syntax, pragmatics, and dialogue modeling have addressed:  

- Turn-taking structure (Sacks et al., 1974)  
- Repair initiation and coordination (Schegloff et al., 1977)  
- Structural priming (Bock & Griffin, 2000)  
- Alignment and adaptation in dialogue (Pickering & Garrod, 2004)  
- Ellipsis and syntactic deletion (Chomsky, 1981)  

However, these often treat interactional mechanisms in isolation from the **syntactic space $\Sigma$** in which they unfold, and without an explicit **distance metric $d(\sigma_1,\sigma_2)$** for tracking change between states.  

PLD offers an integrative framework that supports:  

- Fine-grained conversational annotation  
- Design of adaptive, feedback-sensitive dialogue agents  
- Visualization of syntax as a dynamic topography  
- Cross-linguistic modeling of feedback and repair structures

---

## 3. Key Concepts

| Term *(Lexicon Tier)* | Description | Stability | Formal Hook |
|-----------------------|-------------|-----------|-------------|
| **Phase** (`@core`) | Dynamic syntactic state or transition unit in $\Sigma$. | 🟢 | $ \sigma \in \Sigma $ |
| **Loop** (`@core`) | Recursive cycle triggered by repair, mimicry, or misalignment. | 🟢 | $\mathcal{L}_i$ |
| **Drift** (`@core`) | Gradual disalignment in syntax, meaning, or rhythm; quantified by $\mathcal{D}$. | 🔴 | $\mathcal{D}(\sigma,t)$ |
| **Resonance** (`@derived`) | Repetition or echo reinforcing prior structure. | 🔴 | $\mathcal{L}_5$ |
| **Latency** (`@derived`) | Temporarily delayed or unspoken syntactic action. | 🔴 | $\mathcal{L}_3$ |
| **Cue-driven Repair** (`@support`) | Repair triggered by silence, feedback, or internal monitoring; implemented as $\mathcal{R}$. | 🟡 | $\mathcal{R}(\sigma)$ |

> Full definitions and academic mappings are in [`09_glossary_academic_mapping.md`](../09_glossary_academic_mapping.md).  
> Mathematical formulations are in [`mathematical_appendix/00_formal_specification.md`](../mathematical_appendix/00_formal_specification.md).

---

## 4. Research Foundations

PLD draws on insights from:  

- **Generative Syntax** — hierarchical phase logic (Chomsky, Rizzi, Cinque)  
- **Conversation Analysis** — sequential structure and repair (Sacks, Schegloff, Jefferson)  
- **Cognitive Linguistics** — framing, alignment, conceptual blending (Fauconnier, Langacker)  
- **Pragmatic Interfaces** — user-centered linguistic coordination (Clark, Winograd)  
- **Dialogue Systems & Feedback Models** — alignment engines and discourse repair (Du Bois, Pickering & Garrod)  

These perspectives converge in PLD’s **feedback-sensitive phase topology**, which combines symbolic structure, temporal metrics, and interactional loops.

---

## 5. Repository Structure

- `00_introduction.md` – This document  
- `01_foundations.md` – Theoretical basis and terminology  
- `02_phase_structures.md` to `09_interface_affordance.md` – Core structural modules  
- `10_diagram/structure_topograph.svg` – Complete PLD system diagram  
- `11_conclusion.md` – Cross-domain outlook and future directions  
- `12_phase_loop_dynamics/` – Logs, glossary, academic citations  

For usage and file summaries, see [`../README_phase_loop_dynamics.md`](../README_phase_loop_dynamics.md).

---

## 6. Citation

```bibtex
@misc{phase_loop_dynamics_2025,
title = {Phase Loop Dynamics: Syntax Modeling through Drift, Alignment, and Resonance},
author = {The Phase Drift Language Systems Collective},
year = {2025},
url = {https://github.com/kiyoshisasano-DeepZenSpace/kiyoshisasano-DeepZenSpace/tree/main/12_phase_loop_dynamics}
}
```
“Not all syntax moves forward — some returns, loops, or waits.  
Phase Loop Dynamics maps where it loops $(\mathcal{L}_i)$, where it falters $(\mathcal{D})$, and where it stabilizes again $(\mathcal{R})$.”

---

**Key Changes in This Revision**  
- Inserted formal notation hooks (Σ, 𝒟, ℛ, 𝓛ᵢ) at first mention of corresponding concepts.  
- Added *Formal Hook* column to the Key Concepts table, linking prose terms to mathematical symbols.  
- Linked directly to math appendix sections for deeper detail.  
- Clarified syntactic space and distance metric in Motivation to connect to $d(\sigma_1,\sigma_2)$.  
- Maintained readability for non-math readers by keeping explanations plain before symbols.  
