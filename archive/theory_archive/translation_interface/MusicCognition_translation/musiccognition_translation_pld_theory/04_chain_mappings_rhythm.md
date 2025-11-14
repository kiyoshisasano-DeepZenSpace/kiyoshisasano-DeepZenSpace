# 🔗 Chain Mappings in Rhythm Cognition — Phase Transitions and Temporal Cycles

## 1. Introduction

Within *Phase Loop Dynamics (PLD)*, **chain mappings** represent sequential transitions among phase states — drift (𝒟), repair (ℛ), latency (𝓛₃), and resonance (𝓛₅).  
When translated into **music cognition**, these chains become **temporal adaptation cycles** that describe how listeners and performers move between deviation, correction, and stabilization.

Such phase chains reflect the **self-regulating ecology of rhythm** — a system continually negotiating between instability and entrainment.

---

## 2. Core Chain Types and Musical Equivalents

| PLD Chain | Music-Cognitive Equivalent | Description |
|------------|----------------------------|--------------|
| **Segment → Drift → Repair** | Beat detection → Phase deviation → Correction | Micro-timing instability followed by re-synchronization |
| **Latent → Cue → Segment → Resonance** | Silent beat → Onset cue → Re-entry → Flow stabilization | Emergence of rhythmic continuity after silence |
| **Resonance Collapse → Drift → Repair Failure → Latency** | Overcoupling → Phase slip → Desynchronization → Reset | Breakdown and reinitialization of temporal coordination |

Each sequence forms a **micro-cycle** of rhythmic adaptation — a closed feedback between prediction and recalibration.

---

## 3. Descriptions of Rhythmic Chains

### 3.1 Segment → Drift → Repair

**Trigger:** External perturbation or tempo fluctuation.  
**Process:** A deviation from the expected pulse elicits corrective realignment.  
**Musical Analogue:** A performer gradually lags behind a metronome, then readjusts phase.

\[
\text{Beat Onset} \rightarrow \text{Phase Drift} \rightarrow \text{Corrective Response}
\]

**Behavioral Correlates:**
- Negative lag correlation (phase correction gain)  
- Mean asynchrony returning toward zero after perturbation  
- Restoration of inter-onset interval stability  

---

### 3.2 Latent → Cue → Segment → Resonance

**Trigger:** Silent interval or delayed re-entry.  
**Process:** The latent oscillator maintains internal timing; a cue reinitializes external synchronization; resonance stabilizes the restored pulse.  
**Analogue:** A performer re-enters perfectly in time after a rest before the downbeat.

\[
\text{Silent Pulse} \rightarrow \text{Cue Onset} \rightarrow \text{Beat Re-entry} \rightarrow \text{Resonant Flow}
\]

**Behavioral Correlates:**
- Continuation tapping accuracy following silence  
- Predictive onset alignment after rest  
- Sustained groove following re-entry  

---

### 3.3 Resonance Collapse → Drift → Repair Failure → Latency

**Trigger:** Excessive coupling or over-synchronization.  
**Process:** Strong entrainment destabilizes when flexibility is lost, leading to phase slip and eventual reset.  
**Analogue:** Two musicians lose sync after over-adaptation, pause, and restart.

\[
\text{Resonant Flow} \rightarrow \text{Phase Slip} \rightarrow \text{Desynchronization} \rightarrow \text{Silent Reset}
\]

**Behavioral Correlates:**
- Loss of phase locking index (PLI)  
- Increased inter-tap interval variance  
- Pause followed by renewed synchronization  

---

## 4. Temporal Network Geometry

Rhythmic chains can be visualized as a **phase-transition network** of loop states:

```
 [L1: Beat] → [L2: Drift] → [L4: Repair] → [L3: Latent Reset]
      ↑                                   ↓
   [L5: Resonance] ←──────────────────────
```

Each node represents a phase condition in the timing process, and each edge indicates a **transition probability** within the rhythmic field.  
The network behaves like a **Markov chain**, where stability depends on transition likelihoods \(T_{ij}\):

\[
T_{ij} = \frac{e^{-E_{ij}/K}}{Z}
\]

\(E_{ij}\) denotes the “energy cost” — the temporal or attentional effort required for a given transition.

---

## 5. Empirical Parameters and Temporal Stability

| Chain Type | Mean Duration (s) | Transition Stability | Observed Outcome |
|-------------|------------------|----------------------|------------------|
| Drift–Repair | 1.3–1.6 | Moderate | Adaptive phase correction |
| Latent–Emergence | 2.0–2.3 | High | Accurate re-entry after silence |
| Resonance–Collapse | 1.8–2.5 | Low | Loss and reformation of synchrony |

**Phase stability** of each state can be modeled as:

\[
\pi_i = \frac{e^{-E_i}}{\sum_j e^{-E_j}}
\]

Higher \(\pi_i\) corresponds to more persistent temporal states (e.g., resonance or steady groove).

---

## 6. Markov Chain Approximation

Example transition matrix (empirical illustration):

\[
T =
\begin{pmatrix}
0.70 & 0.15 & 0.10 & 0.05 & 0.00 \\\\
0.25 & 0.40 & 0.20 & 0.10 & 0.05 \\\\
0.10 & 0.05 & 0.60 & 0.15 & 0.10 \\\\
0.08 & 0.25 & 0.12 & 0.40 & 0.15 \\\\
0.00 & 0.10 & 0.20 & 0.10 & 0.60
\end{pmatrix}
\]

Interpretation:  
- **Resonance (𝓛₅)** exhibits high persistence, consistent with groove stability.  
- **Drift–Repair** cycles show adaptive mobility, facilitating synchronization.  
- **Latent states (𝓛₃)** act as temporal attractors, resetting internal timing.

---

## 7. Temporal Energy Landscape

Each transition incurs an “energy” proportional to perceptual or attentional cost:

| Transition | Energy (kT units) | Interpretation |
|-------------|-------------------|----------------|
| L1 → L2 | 0.38 | Perturbation onset |
| L3 → L1 | 0.22 | Re-entry from silence |
| L5 → L2 | 0.45 | Resonance decay |
| L2 → L4 | 0.31 | Engagement of correction |

These gradients shape the **temporal topography** of rhythmic adaptation.

---

## 8. Rhythmic Ecology and Phase Adaptation

The interaction among drift, repair, silence, and resonance forms an **ecology of entrainment**.  
- *Feedback* loops (Drift–Repair) sustain synchronization through continual correction.  
- *Latent chains* (Silence–Cue–Re-entry) preserve continuity through predictive expectancy.  
- *Collapse cycles* (Resonance–Drift–Reset) enable recovery from excessive coupling.

Together, they constitute a **phase grammar of rhythm**, describing how temporal coherence is lost, regained, and stabilized.

---

## 9. Summary

By reinterpreting PLD’s chain mappings within rhythm cognition, we obtain a unified **loop-based theory of temporal coordination**.  
Each phase transition encodes a distinct rhythm-regulatory function, and their chaining explains the fluid resilience of musical time.

> *“Rhythm breathes through its errors — each drift invites a return.”*

---

## References

- Large, E. W. & Jones, M. R. (1999). *The dynamics of attending: How people track time-varying events.* *Psychological Review.*  
- Repp, B. H. (2005). *Sensorimotor synchronization: A review of the tapping literature.* *Psychonomic Bulletin & Review.*  
- Keller, P. E. (2014). *Ensemble performance and interpersonal coordination.* *Current Opinion in Psychology.*  
- Palmer, C. (1997). *Music performance.* *Annual Review of Psychology.*  
- Sasano, K. (2025). *Phase Loop Dynamics: A Syntax of Drift, Repair, and Resonance.*
