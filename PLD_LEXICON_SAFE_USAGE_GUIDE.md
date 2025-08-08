# 📘 PLD Lexicon — Safe Usage & Tiering Guidelines (v0.6)

> ⚠️ This document defines **lexical tier classification**, **usage stability**,  
> and a **safe-term appendix** for concepts used in the *Phase Loop Dynamics (PLD)* framework.  
> It supports theoretical consistency, safe reuse, and cross-domain intelligibility.

---

## 🧭 Tag System

| Tag        | Description |
|------------|-------------|
| `@core`    | **Foundational** concept – anchors other terms and system logic |
| `@support` | **Contextual** term – depends on core terms for structure or clarity |
| `@derived` | **Emergent** concept – manifests from interaction between terms or states |

---

## ✅ Usage Stability Levels

| Symbol | Stability Label               | Description |
|--------|-------------------------------|-------------|
| 🟢     | Stable with minor annotation  | Coherent enough for cautious use across threads |
| 🟡     | Cautious use – frame required | Needs interpretive anchoring or contextual boundary |
| 🔴     | High instability – avoid      | Too fluid or metaphorical for reliable reuse |

---

## 🔡 Lexicon Tier Table — Tentative & Unstable Terms (Updated)

| Term                  | Tier        | Stability | Usage Notes |
|-----------------------|-------------|-----------|-------------|
| **Drift (𝒟)**         | `@core`     | 🟡        | **Updated**: Now strictly linked to the mathematical definition (Appendix §1.4) and the ML concept of *concept drift*. Avoid standalone use; explicitly state target and dimension (e.g., topic / structural / semantic). |
| **Phase (Σ, 𝓛ᵢ)**     | `@core`     | 🟢        | Link to phase space and loop generators in the Mathematical Appendix. Avoid metaphorical use for CP/vP phases unless clearly contextualized. |
| **Structural Tension**| `@support`  | 🔴        | *(No change)* |
| **Rhythm**            | `@support`  | 🟡        | Reference Wilson & Wilson (2005) and specify the timing metric used. |
| **Field**             | `@core`     | 🔴        | *(No change)* |
| **Phase Boundary**    | `@derived`  | 🟡        | Include detection criteria, e.g., TextTiling. |
| **Resonance (𝓛₅)**    | `@derived`  | 🟡        | **Updated**: Ground in *Dialogic Resonance* as primary source; treat as an empirical phenomenon, not just a metaphor. |
| **Silence**           | `@support`  | 🟡        | Cite Jefferson (1989) metrics or Stivers (2009) thresholds. |
| **Coherence (C(σ,t))**| `@derived`  | 🟡        | Specify using DRT/RST references or an explicit measurement. |
| **Latent Phase (𝓛₃)** | `@derived`  | 🟡        | **Updated**: Stability changed from 🔴 to 🟡. Now supported by CA research on silence and psycholinguistic delay thresholds. |

### Symbol Links
- 𝒟 (Drift operator) → *Mathematical Appendix* §1.4  
- ℛ (Repair operator) → §1.5  
- 𝓛ᵢ (Loop generators) → §1.6 / §3.2  
- Σ (Phase space) → §1.2  

### References
- For detailed definitions and mappings, see `01_phase_loop_dynamics/related_work/pld_to_academic.md`

---

## 📌 Tier × Stability Matrix

| Usage Context           | 🟢 Safe Terms    | 🟡 Cautious Terms                | 🔴 Unstable – Avoid |
|-------------------------|------------------|----------------------------------|---------------------|
| Internal documentation  | Phase            | Drift, Rhythm, Silence, Coherence| Field               |
| Public explanation      | Phase (w/ note)  | Drift, Phase Boundary (w/ model) | Resonance, Tension  |
| Structural modeling     | Phase            | Drift, Rhythm (defined)          | *(none)*            |
| Academic papers         | Phase (anchored) | Drift, Silence (linked to CA)    | *(none)*            |

---

## ✅ Safe-Term Appendix v0.1

> **Safe terms** are structurally stable and externally explainable,  
> suitable for documentation, educational use, and cross-disciplinary modeling.

### 🔑 Criteria
- Supported in existing literature (linguistics, HCI, cognitive science)
- Low metaphorical ambiguity
- Stable scope and transferable structure
- Usable without heavy framing

---

| Term            | Tier        | Scope Description                             | External Usability      |
|-----------------|-------------|-----------------------------------------------|--------------------------|
| **Turn**        | `@support`  | Atomic unit of interaction/discourse          | ✅ Widely used in CA      |
| **Attention**   | `@support`  | Shared focus structure in discourse           | ✅ Cross-disciplinary     |
| **Segment**     | `@derived`  | Delimited unit of speech or gesture           | ✅ Structural modeling    |
| **Timing**      | `@support`  | Relative temporal pacing                      | ✅ UI, UX, psycholinguistics |
| **Cue**         | `@support`  | Observable trigger for state/shift            | ✅ Broad applicability    |
| **Feedback**    | `@derived`  | Reactive update or acknowledgment pattern     | ✅ Stable across domains  |
| **Modality**    | `@core`     | Communicative channel (e.g., voice, gesture)  | ✅ Multimodal interaction |
| **Alignment**   | `@derived`  | Semantic or structural convergence            | ✅ Discourse analysis     |
| **Reference**   | `@support`  | Referential relation (pronouns, deixis, etc.) | ✅ Semantics, pragmatics  |

---

## 📌 Deployment Scenarios

| Use Case                   | Recommendation        |
|----------------------------|------------------------|
| Internal docs              | ✅ Use freely           |
| Academic writing           | ✅ Use with citations   |
| Cross-domain collaboration | ✅ Use as shared layer  |
| PLD theory core            | ❌ Do not anchor models |

---

## 🔏 Safety Note

This lexicon defines **operational scaffolding terms**, not the core generative metaphors of PLD.  
Unlike `Drift` or `Latent Phase`, these terms can stand alone with minimal risk of misinterpretation.

---

## 📘 Citation

**Phase Loop Dynamics — PLD Lexicon Safe Usage & Tiering Guidelines (v0.6)**  
_Phase Drift / PLD Language Systems Collective, 2025_  
[Repository Link](https://github.com/kiyoshisasano-DeepZenSpace)

> These guidelines are **structural drift guards**.  
> Lexical integrity is a **pacing function**, not a fixed taxonomy.
