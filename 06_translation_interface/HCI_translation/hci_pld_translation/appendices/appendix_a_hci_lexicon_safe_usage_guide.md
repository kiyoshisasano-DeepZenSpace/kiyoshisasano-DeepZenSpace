# Appendix A — HCI Lexicon Safe Usage Guide (v1.0)

## Purpose

This appendix defines the lexical stability framework governing the translation of Phase Loop Dynamics (PLD) into Human–Computer Interaction (HCI) terminology.  
It clarifies how temporal-interaction concepts should be used, what interpretive context they require, and how they correspond to established HCI and Conversation Analysis (CA) vocabulary.

---

## A.1 Lexical Tier System

| Tier | Description | Analogy in HCI Theory |
|------|--------------|----------------------|
| @core | Foundational terms anchoring the theoretical structure | Fundamental coordination primitives (e.g., turn, latency, repair) |
| @support | Contextual terms refining or qualifying core constructs | Supplementary timing or modality descriptors |
| @derived | Emergent terms arising from dynamic interaction | Higher-order phenomena such as resonance or coherence |

**Core → measurable • Support → contextual • Derived → emergent pattern.**  
This tiering preserves conceptual discipline across publications.

---

## A.2 Stability Levels

| Symbol | Label | Description | HCI Interpretation |
|---------|--------|-------------|--------------------|
| 🟢 | Stable | Reliable across contexts; minimal theoretical risk | Safe for general or cross-disciplinary use |
| 🟡 | Cautious | Requires framing or citation | Use with explicit grounding (e.g., CA or cognitive source) |
| 🔴 | Unstable | Metaphorical / ambiguous; avoid in formal writing | Not yet empirically validated |

Use the stability index to maintain terminological consistency when mapping PLD to HCI.

---

## A.3 Lexical Tier Table (Translated for HCI)

| Term | Tier | Stability | Recommended HCI Usage | Conceptual Boundary |
|------|------|------------|-----------------------|----------------------|
| Drift (𝒟) | @core | 🟡 | Use for interactional misalignment (timing / semantic / structural); specify domain. | Comparable to breakdown in Suchman (1987). |
| Phase (Σ, 𝓛ᵢ) | @core | 🟢 | Temporal segment or loop state within interaction. | Equivalent to episode or activity frame. |
| Repair (ℛ) | @core | 🟢 | Self- or system-initiated recovery after drift. | Matches CA repair sequence. |
| Resonance (𝓛₅) | @derived | 🟡 | Synchrony / mutual alignment between interlocutors. | Ground in dialogic resonance (Du Bois & Giora 2014). |
| Latency (𝓛₃) | @derived | 🟡 | Anticipatory pause or processing delay before response. | Cite psycholinguistic thresholds (Stivers 2009). |
| Rhythm | @support | 🟡 | Temporal pacing of actions or speech; interval regularity. | Link to Wilson & Wilson (2005). |
| Silence | @support | 🟡 | Measurable pause marking transition or reflection. | Specify duration metric (e.g., ≥ 0.5 s). |
| Coherence (C(σ,t)) | @derived | 🟡 | Temporal / semantic continuity indicator. | Reference RST or grounding theory. |
| Phase Boundary | @derived | 🟡 | Segment break detected by drift threshold or topic shift. | Comparable to TextTiling (Hearst 1997). |
| Field / Structural Tension | @support | 🔴 | Metaphorical; avoid in formal HCI writing. | None – historical only. |

---

## A.4 Safe-Term Appendix (Validated for HCI Use)

| Term | Tier | Scope | External Reference |
|------|------|--------|--------------------|
| Turn | @support | Atomic conversational unit | Sacks et al. (1974) |
| Cue | @support | Observable trigger for state transition | Norman (1988); Clark (1996) |
| Feedback | @derived | Reactive acknowledgment or update | Winograd & Flores (1986) |
| Alignment | @derived | Semantic / attentional convergence | Clark (1996) |
| Timing | @support | Relative pacing of user–system events | Dourish (2001) |
| Attention | @support | Shared focus structure | Hutchins (1995) |
| Modality | @core | Communicative channel (speech, gesture, display) | Multimodal HCI literature |
| Segment | @derived | Delimited sequence of coordinated actions | Interaction episode models |
| Reference | @support | Referential link / deixis in discourse | Pragmatics literature |

These are cross-disciplinary constants usable beyond PLD contexts.

---

## A.5 Recommended Use Contexts

| Context | 🟢 Safe Terms | 🟡 Cautious Terms | 🔴 Avoid |
|----------|---------------|------------------|-----------|
| Internal documentation | Phase, Turn | Drift, Rhythm, Silence | Field |
| Academic writing | Phase, Repair | Drift (with domain), Coherence | Field, Tension |
| Design evaluation | Phase, Timing | Latency, Rhythm | — |
| Cross-disciplinary collaboration | Phase, Cue, Feedback | Resonance (with definition) | — |

This matrix promotes transparency and consistency across research teams.

---

## A.6 Operational Criteria for Term Safety

A term qualifies as **safe for HCI discourse** when it:

- Is supported by at least one recognized literature (CA, cognitive, or design).  
- Is measurable or observable in interaction data.  
- Has low metaphorical load, interpretable without specialized theory.  
- Applies across modalities (speech, gesture, interface events).  

---

## A.7 Interpretive Boundaries and Ethical Use

- **Avoid metaphor inflation:** Terms like *field* or *tension* imply physical analogies unsuited to empirical HCI.  
- **Preserve provenance:** Cite original CA or psycholinguistic sources.  
- **Maintain human pacing:** Use drift / latency metrics to inform, not dictate, design tempo.  
- **Transparency in adaptation:** When using PLD terms in UX evaluation, include operational definitions in the *Methods* section.

---

## A.8 References (Indicative)

Clark, H. H. (1996). *Using Language.* Cambridge University Press.  
Dourish, P. (2001). *Where the Action Is.* MIT Press.  
Hearst, M. (1997). “TextTiling: Segmenting Text into Multi-Paragraph Subtopic Passages.” *Computational Linguistics.*  
Sacks, H., Schegloff, E., & Jefferson, G. (1974). “A Simplest Systematics for the Organization of Turn-Taking.” *Language.*  
Stivers, T. (2009). “How Important Is the Gap?” *Discourse Processes, 46*(1).  
Wilson, M., & Wilson, T. (2005). “An Oscillator Model of Timing in Turn-Taking.” *Psychonomic Bulletin & Review.*  
Winograd, T., & Flores, F. (1986). *Understanding Computers and Cognition.* Ablex.
