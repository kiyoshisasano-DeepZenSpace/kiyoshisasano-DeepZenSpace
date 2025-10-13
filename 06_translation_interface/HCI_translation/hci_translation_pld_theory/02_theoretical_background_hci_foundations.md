# Part 2 — Core Concepts: Drift, Repair, Resonance, Latency, and Interaction States

## 2.1 Overview

In Human–Computer Interaction (HCI), interaction unfolds as temporal co-regulation rather than a mere exchange of messages. Phase Loop Dynamics (PLD) reframes co-regulation as a small set of recurrent coordination loops—regular patterns that explain how coordination stabilizes, degrades, and re-emerges. This section translates PLD constructs into standard HCI terms with operational definitions and conceptual measurement. Throughout, we use the canonical symbol set established in Part 5:  
δ (drift magnitude), t(ℛ) (repair latency), ρ (resonance strength), Δt₍L₃₎ (latency duration), S (cycle stability). See Part 5, Table 5.3 for the metric glossary.

---

## 2.2 Interaction State and Phase Loop (𝓛)

**Definition**  

- **Interaction State (phase)**: a locally stable configuration of turn-taking, grounding status, and activity orientation during a dialogue or interface episode.  
- **Phase Loop (𝓛ᵢ)**: a recurrent coordination pattern governing transitions among such states. Loops are empirically detectable via timing, turn structure, and feature reuse.

| Loop ID | HCI Analogue | Primary Function |
|----------|---------------|------------------|
| L₁ | Turn-opening / Segmentation | Detecting onset and boundaries |
| L₂ | Breakdown → Repair | Managing deviation from mutual understanding |
| L₃ | Pre-utterance Latency | Holding or delaying articulation |
| L₄ | Self-monitoring Repair | Within-turn self-correction |
| L₅ | Alignment / Resonance | Re-establishing synchrony or shared rhythm |

These loops correspond to well-documented mechanisms in Conversation Analysis (turn-taking, repair) and HCI (feedback, affordances, grounding).

---

## 2.3 Drift (𝒟) — Degradation of Alignment (cautious term)

**HCI Interpretation**  
Drift is a graded loss of coordination—the current frame no longer predicts the next action with sufficient confidence. It aligns with breakdown (Suchman 1987), extends system-image mismatch (Norman) into a temporal gradient, and quantifies misalignment in grounding (Clark 1996).

### Operational Dimensions

| Dimension | Description | Indicative Measure (conceptual) |
|------------|--------------|---------------------------------|
| Semantic drift | Divergence in referential meaning/intent | Clarification requests per turn; semantic distance of reformulations |
| Structural drift | Breakdown in expected syntactic/task sequence | Deviations from planned path; wrong state transitions |
| Temporal drift | Desynchronization of timing and latency | Turn-gap distribution; response-delay variance |

**Onset rule (conceptual):** mark drift when one or more indicators exceed local baselines. Magnitude is summarized as δ.

**Examples:**  
1. Voice: cut-offs + “huh?” tokens  
2. GUI: cursor stalls + undo clusters  
3. Collaborative editing: topic wobble + overlapping starts

---

## 2.4 Repair (ℛ) — Re-establishment of Grounding

**HCI Interpretation**  
Repair restores mutual intelligibility and course of action. In CA terms: self/other initiation and completion. In HCI: confirmation prompts, clarification dialogs, reformulations, undo.

### Taxonomy

| Type | Initiator | Mechanism | HCI Examples |
|------|------------|------------|---------------|
| Self-initiated self-repair (L₄) | User | Re-articulation before system acts | “Wait, I mean…”, quick undo |
| Self-initiated other-repair | User → System | Explicit re-query | Reformulated search |
| Other-initiated self-repair | System → User | Clarification prompt | “Did you mean…?” |
| Other-initiated other-repair | System | Automatic correction | Spell-check, autocorrect |

### Measurement Concepts

- **t(ℛ):** time from drift onset → confirmed repair  
- **Repair depth:** number of sub-repairs to reach alignment  
- **Success ratio:** fraction of repairs that yield confirmation without renewed drift  

**Intuition:** Repair performs a gradient descent on misalignment until the coherence of the episode stabilizes.

---

## 2.5 Resonance (L₅) — Alignment Through Echo (cautious term)

**HCI Interpretation**  
Resonance is alignment via echo—reusing lexical, structural, prosodic, gestural, or rhythmic features to consolidate common ground and often to hand off smoothly (Du Bois & Giora 2014). In HCI it corresponds to interactional entrainment and flow.

### Functional Mechanisms

- Lexical/syntactic echo (paraphrase, parallelism)  
- Prosodic/temporal entrainment (pacing match)  
- Affective alignment (tone mirroring)  
- Interactional handoff (seamless turn transfer)

### Conceptual Metrics

| Indicator | Meaning | HCI Proxy |
|------------|----------|------------|
| ρ (resonance strength) | Degree of echo/entrainment | n-gram overlap; latency cross-correlation |
| Δρ/Δt (decay) | Stability of alignment | Slope of correlation decay |
| τ (transfer index) | Seamless handoff probability | Turn-transfer success rate |

**Failure case:** Degenerate resonance: surface echo without semantic progress (ρ high, grounding unchanged) → predicts renewed drift. Analysts should distinguish productive vs degenerate resonance.

---

## 2.6 Latency (L₃) — Structured Silence (cautious term)

**HCI Interpretation**  
Latency is coordinated withholding—intention is present but articulation is delayed. It is not mere absence: latency can invite uptake, stage repair, or prevent premature commitment.

### Types

| Type | Interactional Role | Observable Marker |
|-------|---------------------|--------------------|
| Preparatory latency | Planning before action | In-breath, gaze fixation, hover, pen lift |
| Hesitation latency | Uncertainty / repair preface | Fillers; pause > baseline (e.g., > ~500 ms speech) |
| Systemic latency | Machine processing delay | Spinners, progress indicators |
| Conversational latency | Turn-exchange timing | Gap between turns (Stivers 2009) |

### Measurement Notes

- **Δt₍L₃₎:** measured against local baselines (task, skill, culture)  
- Optimal windows vary by modality; beyond them, latency provokes temporal drift  
- Adaptive latency can be beneficial (reflection, self-repair)

**Cultural/experience note:** Pause norms differ cross-culturally; experts show shorter anticipatory latencies than novices. Always normalize within-participant/task.

---

## 2.7 Inter-relations: Drift, Repair, Resonance, Latency

A cyclic dynamic organizes the four constructs:

```
[Drift] → [Repair] → [Resonance] → [Latency] → [Drift]
```

- **Drift** signals loss of predictive fit (δ↑).  
- **Repair** reduces misalignment (t(ℛ) characterizes responsiveness).  
- **Resonance** stabilizes alignment (ρ↑, Δρ/Δt ≤ 0).  
- **Latency** provides temporal scaffolding (Δt₍L₃₎) for the next initiative.

This extends Clark’s grounding by adding temporal layers (latency, entrainment) and failure paths (resonance collapse → renewed drift), consistent with CA repair organization and Dourish’s temporal embodiment.

---

## 2.8 Conceptual Measurement Summary

| Construct | Primary Metric | Interpretive Range | Typical Data Sources |
|------------|----------------|--------------------|----------------------|
| Drift (𝒟) | δ: deviation rate (semantic/temporal/structural) | 0 = stable → 1 = severe misalignment | Dialog logs, UI traces |
| Repair (ℛ) | t(ℛ), success ratio, depth | Short t(ℛ) + high success = effective | Clarifications, undo/redo, re-queries |
| Resonance (L₅) | ρ, Δρ/Δt, τ | ρ > ~0.8 indicates strong entrainment | Feature reuse; timing correlation |
| Latency (L₃) | Δt₍L₃₎ vs baseline | Optimal ranges are context-dependent | Speech timing; hover/idle logs |
| Cycle Stability (S) | Resonant time / cycle time | Higher S = more sustained fluency | Segmented state sequences |

See Part 5 for model variants (Markov transitions; decay functions) and ethics notes on timing as a design parameter.

---

## 2.9 Theoretical Contribution (Recap)

- **Temporal grounding theory:** grounding is dynamic and looped, not binary.  
- **Multi-dimensional drift metric:** semantic/structural/temporal facets under one umbrella (δ).  
- **Quantified repair/resonance:** bridges CA typologies with measurable HCI indicators (t(ℛ), ρ).  
- **Silence as phase:** latency becomes a designable temporal resource rather than a void.

---

## 2.10 References (Indicative)

Clark, H. H. (1996). *Using Language.* Cambridge University Press.  
Dourish, P. (2001). *Where the Action Is: The Foundations of Embodied Interaction.* MIT Press.  
Du Bois, J. W., & Giora, R. (2014). Dialogic resonance and language usage. *Language and Cognition, 6*(4), 321–350.  
Norman, D. A. (2013). *The Design of Everyday Things* (Rev. ed.). Basic Books.  
Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). A simplest systematics for the organization of turn-taking for conversation. *Language, 50*(4), 696–735.  
Suchman, L. A. (1987). *Plans and Situated Actions.* Cambridge University Press.  
Stivers, T. (2009). How important is the gap? Timing as a resource for interdependence in conversation. *Discourse Processes, 46*(2–3), 117–149.
