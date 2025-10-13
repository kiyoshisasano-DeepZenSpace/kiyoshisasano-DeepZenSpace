# Appendix B — HCI Conceptual Connectivity Map (v1.0)

## Purpose

This appendix visualizes the conceptual relationships among the core, support, and derived terms of the **Phase Loop Dynamics → HCI** translation framework.  
It functions as a conceptual topology connecting timing, coordination, and repair processes across **Conversation Analysis (CA)** and **Human–Computer Interaction (HCI)**.

All relations are **functional rather than strictly causal** — they represent theoretical dependencies between coordination phenomena.

---

## B.1 Legend

| Symbol / Tag | Meaning | HCI Analogy |
|---------------|----------|--------------|
| @core | Foundational element of interaction dynamics | Turn-taking, repair, latency |
| @support | Contextual modulator of temporal flow | Rhythm, silence |
| @derived | Emergent phenomenon arising from loops | Resonance, coherence |
| 🟢 | Stable term | Established in HCI & CA |
| 🟡 | Cautious term | Requires contextual framing |
| 🔴 | Avoid / metaphorical | Not empirically validated |

---

## B.2 Connectivity Diagram

```mermaid
graph TD
    Drift["@core Drift (interactional misalignment) 🟡"] --> Repair["@core Repair (re-alignment) 🟢"]
    Drift --> PhaseBoundary["@derived Phase Boundary 🟡"]
    Repair --> Resonance["@derived Resonance (synchrony) 🟡"]
    Phase["@core Phase (interaction segment) 🟢"] --> PhaseBoundary
    Rhythm["@support Rhythm 🟡"] --> Phase
    Silence["@support Silence 🟡"] --> Repair
    Coherence["@derived Coherence 🟡"] --> Phase
    Latency["@derived Latency (anticipatory pause) 🟡"] --> Coherence
```

### Interpretation

- **Drift → Repair → Resonance** forms the *temporal recovery loop*: misalignment triggers re-alignment, which stabilizes into synchrony.  
- **Phase / Phase Boundary** organize these transitions, while **Rhythm** and **Silence** modulate their pacing.  
- **Coherence** evaluates alignment within a phase; **Latency** sustains predictive readiness between turns.

---

## B.3 Relationship Table

| Source Term | Target Term | Relation Type | HCI Interpretation |
|--------------|--------------|---------------|--------------------|
| Drift (@core) | Repair (@core) | Sequential | Misalignment triggers recovery → parallels breakdown → repair cycles (Suchman 1987). |
| Drift | Phase Boundary | Causal | High drift magnitude marks topical or task transitions. |
| Repair | Resonance (@derived) | Recursive | Re-alignment enhances mutual prediction → temporal synchrony. |
| Phase (@core) | Phase Boundary | Structural | Segments continuous interaction into analyzable units. |
| Rhythm (@support) | Phase | Modulatory | Regular pacing stabilizes transitions between segments. |
| Silence (@support) | Repair | Trigger | Pauses cue self- or other-initiated repair. |
| Coherence (@derived) | Phase | Evaluative | Degree of semantic / temporal alignment within a segment. |
| Latency (@derived) | Coherence | Hypothetical | Predictive delay supports smoother continuation and coherence. |

---

## B.4 Interpretive Notes

### Temporal Causality vs Functional Dependency

Arrows indicate *functional dependence*, not deterministic cause.  
**Drift** statistically precedes **Repair** but may co-occur within the same segment.

### Bidirectionality

Relations are often reversible.  
**Repair** reduces **Drift**, yet excessive or premature **Repair** can re-induce **Drift** (e.g., over-correction in adaptive interfaces).

### Cross-Modality Applicability

Each link generalizes across speech, gesture, and interface events.  
Example: *Silence → Repair* covers both pause-before-rephrase and idle-before-click behaviors.

### Measurement Anchors

Every edge aligns with an empirical **PLD → HCI metric:** δ, t(ℛ), ρ, Δt₍L₃₎.  
Hence, the map is both conceptual and analytically testable.

---

## B.5 Usage Scenarios

| Stakeholder | Purpose | Example Application |
|--------------|----------|--------------------|
| HCI Researchers | Identify dependencies among temporal constructs before modeling. | Select relevant measures (δ, t(ℛ), ρ) for analysis. |
| Interaction Designers | Visualize timing relations to guide pacing. | Map silence thresholds to repair cues. |
| Cognitive Modelers | Parameterize simulation loops. | Define transition probabilities in timing models. |
| Educators / Writers | Illustrate conceptual coherence visually. | Teach the drift–repair–resonance cycle. |

---

## B.6 Evolution and Maintenance

**Version 1.0 (2025)** — First HCI translation of PLD v0.6; all relations reframed in human–computer coordination terms.  
Future updates may add quantitative weights or empirical coefficients derived from timing datasets.  
All extensions must comply with lexical stability standards (see Appendix A).

---

## B.7 Citation

**Phase Loop Dynamics — HCI Conceptual Connectivity Map (v1.0)**  
<https://github.com/kiyoshisasano-DeepZenSpace>

> “Coordination is not a line of dialogue but a loop of timing.”
