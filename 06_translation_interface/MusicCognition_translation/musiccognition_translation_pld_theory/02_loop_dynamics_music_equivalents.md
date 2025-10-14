# 🔁 Loop Dynamics and Music Cognition Equivalents

## 1. Overview

This section translates the **five core phase loops** (𝓛₁–𝓛₅) of *Phase Loop Dynamics (PLD)* into **music cognition and rhythmic synchronization terminology**.  
Each loop is recast as a process within temporal perception, prediction, and entrainment, forming a cyclical ecology of **phase deviation, correction, resonance, and latency**.

---

## 2. Core Mapping Table

| PLD Loop | Music Cognition Process | Functional Role | Empirical Equivalent |
|-----------|-------------------------|-----------------|----------------------|
| 𝓛₁ Segment | Beat boundary detection | Demarcation of rhythmic cycles | Meter induction, segmentation tasks |
| 𝓛₂ Drift | Phase deviation / microtiming error | Generates instability and drives correction | Asynchrony drift in tapping |
| 𝓛₃ Latent | Internal pulse maintenance | Sustains rhythm during silence or delay | Continuation tapping, silent beat |
| 𝓛₄ Feedback | Phase correction and re-entrainment | Restores synchrony after temporal error | Error correction gain (PCG) |
| 𝓛₅ Resonance | Entrainment and groove coupling | Stabilizes rhythmic flow through resonance | Phase locking index (PLI), groove perception |

---

## 3. Loop-by-Loop Translation

### 3.1 𝓛₁ — Segment Loop: Beat and Meter Segmentation

**Concept:** Identifies perceptual units within rhythmic flow.  
**Music Cognition Equivalent:** Beat boundary detection and metric parsing.

In rhythm perception, segmentation arises when listeners infer periodic structure (e.g., the “beat” or “downbeat”).  
PLD’s segmentation loop aligns with **metrical parsing** — detecting phase boundaries through temporal expectancy peaks.

**Operationalization:**
- Event-related potentials (P3b) during meter induction  
- Behavioral segmentation accuracy  
- ITI clustering (inter-tap interval regularity)

---

### 3.2 𝓛₂ — Drift Loop: Microtiming Deviation and Temporal Error

**Concept:** Captures destabilization within rhythmic coherence.  
**Music Cognition Equivalent:** Phase drift — progressive desynchronization of internal pulse from stimulus.

Phase drift reflects the difference \(\phi = t_{response} - t_{stimulus}\).  
In PLD, drift is not an error per se, but the *source of rhythmic energy* — it drives the system into corrective engagement.

**Measurement:**  
- Mean asynchrony and variance  
- Drift rate (Hz/s)  
- Correlation with corrective lag

**Empirical References:** Repp (2005), Large & Jones (1999)

---

### 3.3 𝓛₃ — Latent Loop: Silent Pulse and Predictive Continuation

**Concept:** Describes structure beneath silence.  
**Music Cognition Equivalent:** Maintenance of internal rhythm during absence of auditory cues.

During rhythmic silence, the internal oscillator continues to evolve, sustaining *temporal expectancy*.  
This is seen in *continuation tapping* and *missing-beat paradigms*, where performance resumes in-phase after silence.

**Neural Correlates:**
- Sustained oscillations in beta band (13–30 Hz)
- Predictive activity in supplementary motor area (SMA)
- BOLD persistence during imagined continuation

**Empirical References:** Fujioka et al. (2012), Nozaradan (2016)

---

### 3.4 𝓛₄ — Feedback Loop: Reactive Correction and Re-entrainment

**Concept:** Models how the system responds to detected phase error.  
**Music Cognition Equivalent:** Phase correction and adaptive synchronization.

The feedback loop quantifies the *gain* with which internal timing adjusts to minimize phase deviation:

\[
\Delta\phi_{t+1} = (1 - \alpha)\Delta\phi_t
\]
where \(\alpha\) = correction gain (0 < α < 1).

**Operational Signatures:**
- Correction slope in lag-one autocorrelation
- Asymmetry between delay vs. advance corrections
- EEG error potentials (ERN)

**Empirical References:** Repp & Keller (2004), Schulze et al. (2005)

---

### 3.5 𝓛₅ — Resonance Loop: Groove and Temporal Coupling

**Concept:** Encodes mutual stabilization of oscillatory agents.  
**Music Cognition Equivalent:** Entrainment resonance — sustained phase-locking between oscillators.

Resonance represents the system’s ability to enter **phase-synchronous attractor states**, experienced subjectively as *groove*, *flow*, or *coherence*.

**Formalization:**  
Coupled oscillator model:
\[
\frac{d\phi}{dt} = \omega_i - \omega_j + K\sin(\phi)
\]
where \(K\) expresses coupling strength (entrainment).

**Empirical Measures:**
- Phase Locking Index (PLI)
- Cross-wavelet coherence
- fMRI coherence in auditory–motor loops

**Empirical References:** Large (2008), Keller (2014)

---

## 4. Inter-Loop Dynamics and Transitions

Transitions between loops (e.g., Drift → Repair → Resonance) correspond to real-time **phase state shifts**.  
Empirical analogues appear as alternations between stable entrainment and corrective action.

| Transition | Cognitive Process | Observed Behavior |
|-------------|------------------|------------------|
| 𝓛₁ → 𝓛₂ | Segmentation to drift | Onset of asynchrony, loss of predictability |
| 𝓛₂ → 𝓛₄ | Drift to feedback | Reactive phase correction |
| 𝓛₃ → 𝓛₁ | Silence to segmentation | Resurfacing of rhythm after pause |
| 𝓛₅ → 𝓛₂ | Resonance decay | Over-adaptation causing phase slip |

These transitions form a **Markovian phase chain**, measurable through sequence probability of loop states (cf. `05_chain_mappings.md`).

---

## 5. Experimental Translation Framework

Each PLD loop can be **operationalized** as a measurable temporal process:

| Loop | Experimental Paradigm | Dependent Variable | Expected Pattern |
|------|-----------------------|--------------------|------------------|
| 𝓛₁ | Beat segmentation task | ERP latency, accuracy | Periodic peak at metrical accents |
| 𝓛₂ | Perturbed tapping | Mean asynchrony drift | Gradual phase lag accumulation |
| 𝓛₃ | Silent continuation | Temporal error post-gap | In-phase reentry after silence |
| 𝓛₄ | Delayed auditory feedback | Correction gain (α) | Partial compensation (0.3–0.6) |
| 𝓛₅ | Groove entrainment task | Phase locking index | Stable synchronization plateau |

---

## 6. Synthesis

PLD’s loop topology provides a **cognitive grammar of rhythm** — mapping linguistic drift and repair dynamics to **sensorimotor entrainment** processes.  
Each loop represents a distinct **phase-regulation mode**, and together they constitute a recursive rhythm-perception network.

> *“Each beat is a negotiation — between drift and return, silence and pulse.”*

---

## References

- Large, E. W. & Jones, M. R. (1999). *The dynamics of attending.* Psychological Review.  
- Repp, B. H. (2005). *Sensorimotor synchronization: A review of the tapping literature.* Psychonomic Bulletin & Review.  
- Keller, P. E. (2014). *Ensemble performance: Interpersonal entrainment and coordination.* Current Opinion in Psychology.  
- Fujioka, T. et al. (2012). *Beta-band oscillations represent auditory beat prediction.* Journal of Neuroscience.  
- Sasano, K. (2025). *Phase Loop Dynamics: A Syntax of Drift, Repair, and Resonance.*
