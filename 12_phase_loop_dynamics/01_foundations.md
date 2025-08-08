# 📘 01_foundations.md  
## Phase Loop Dynamics – Foundational Framework (Integrated Theory + Mathematical Specification)

---

## 🔹 Overview

**Phase Loop Dynamics (PLD)** is a framework for modeling the *microstructural dynamics* of language as it unfolds in interaction.  
Rather than treating syntax as a static or purely generative process, PLD describes it as a system of **feedback-based phase transitions** $(\Sigma)$,  
in which alignment, silence, cue, repair $(\mathcal{R})$, and resonance interact recursively within **loop structures** $(\mathcal{L}_i)$.

These interactional loops give rise to observable shifts in syntax and structure, including:

- Hesitation, fragmentation, and mid-turn revisions  
- Structural mimicry and syntactic echo  
- Latent activation and delayed alignment $(\mathcal{L}_3)$  
- Silence-induced cueing and recursive repair $(\mathcal{R})$

PLD serves as a bridge between generative syntax, cognitive interaction, and discourse-internal alignment.

---

## 🔸 1. Structural Foundation: From Generative Layers to Loop Topographies

| Core Term          | Academic Lineage                         | Functional Role in PLD | Formal Hook |
|--------------------|-------------------------------------------|------------------------|-------------|
| **Structural Phase** | Cartographic Syntax (Rizzi, Cinque)       | Projects layered zones of syntactic scope. | $\sigma \in \Sigma$ |
| **Loop Topography** | Interface Syntax + Mental Space Models    | Represents recursive spatial logic of phase traversal. | $\mathcal{L}_i$ |
| **Trace & Residue** | Generative Grammar (Chomsky); Construction Grammar (Goldberg) | Latent remnants influencing future form and alignment. | $p \in \mathcal{P}$ |

**Phase Space Axiom**  
\[
\Sigma \triangleq \mathcal{S} \times \mathcal{T} \times \mathcal{P}
\quad \text{(Syntax × Time × Prosody)}
\]

**Phase Topology**  
\[
H_n(\Sigma) =
\begin{cases}
\mathbb{Z} & n = 0,1 \\
0 & \text{otherwise}
\end{cases}
\]

Example:  
- Structural Phase: $(\text{SOV}, t=1.2s, \text{pitch}=120\text{Hz})$  
- Loop Topography: $\mathcal{L}_2: \Sigma \to \Sigma$ repairs drift

---

## 🔸 2. Cognitive Dynamics: Drift, Mimicry, and Latency

| PLD Concept         | Academic Parallel                  | Disciplinary Field | Formal Hook |
|---------------------|-------------------------------------|--------------------|-------------|
| **Syntax Infection** | Structural Priming (Pickering & Garrod) | Psycholinguistics | — |
| **Drift Transfer**   | Concept Drift (Widmer); Variation (Labov) | NLP, Historical Linguistics | $\mathcal{D}$ |
| **Latency**          | Residual Activation (Segaert et al.) | Cognitive Psychology | $\mathcal{L}_3$ |

Drift $(\mathcal{D})$ is not a breakdown, but a **signal of disalignment**—a movement between stable phases.  
*Syntax infection* describes unintended mimicry across speakers. *Latency* captures temporary suppression of form awaiting activation.

**Drift Metric**  
\[
\mathcal{D}(\sigma,t) = 1 - \frac{\|\nabla C(\sigma,t)\|}{K_{\text{drift}}} 
\quad (0 \leq \mathcal{D} \leq 1)
\]

**Latency Activation Probability**  
\[
P_{\text{emergence}}(\psi_l) = 1 - e^{-\lambda \psi_l}, \quad (\lambda \approx 0.35)
\]

---

## 🔸 3. Feedback Loops: Silence, Cue, and Repair

| Interactional Feature | Theoretical Reference                  | Role in PLD | Formal Hook |
|-----------------------|----------------------------------------|-------------|-------------|
| **Silence**           | Turn-taking Theory (Sacks, Schegloff); Wait Time (Rowe) | Triggers recalibration or expectancy reset. | — |
| **Cue-Driven Repair** | Repair Sequences (Schegloff); Feedback Cues (Dingemanse) | Initiates loop restart via monitoring. | $\mathcal{R}$ |
| **Alignment Anchoring** | Grounding (Clark & Brennan); Alignment Theory (Pickering & Garrod) | Ensures loop closure. | $\mathcal{L}_5$ |

Recursive model: **Silence → Cue → Repair $(\mathcal{R})$ → Alignment $(\mathcal{L}_5)$ → Loop Reentry $(\mathcal{L}_i)$**

**Repair Operator**  
\[
\mathcal{R}(\sigma) = \sigma + \lambda \int_{\tau \in T} \phi(\tau)\Delta(\sigma,\tau) \, d\tau
\]
where $\phi(\tau)$ is a Gaussian kernel:
\[
\phi(\tau) = \frac{1}{\sqrt{2\pi s^2}} \exp\left(-\frac{(\tau - \tau_0)^2}{2s^2}\right)
\]

**Drift–Repair Duality**  
\[
\ker(\mathcal{D}) \cong \operatorname{im}(\mathcal{R})
\]

---

## 🔸 4. Resonance and Reentry: Mimicry as Structural Recovery

Resonance $(\mathcal{L}_5)$ is treated not as redundancy, but as **functional reentry** of suppressed or unresolved structures.  
Syntax may loop back to re-activate unanchored prior forms.

- **Resonance Reentry** builds on Dialogic Syntax (Du Bois) and repetition phenomena  
- **Echoic Syntax** involves latent mimicry of form, stance, or prosody  
- These mechanisms stabilize phases through structural reactivation

**Resonance Fixed-Point Theorem**  
\[
\exists \sigma^* \in \Sigma \ \text{s.t.} \ \mathcal{L}_5 \sigma^* = \sigma^*
\]

**Convergence Bound**  
\[
\| \mathcal{L}_5^n \sigma - \sigma^* \| \leq C e^{-\beta n}
\]

---

## 🔸 5. Interface Perspective: Syntax as Participatory Structure

PLD extends syntax into the interface domain, where syntactic structure is:

- A **shared cognitive topology** $(\Sigma, d(\sigma_1,\sigma_2))$  
- Modulated by affordance, perception, and alignment  
- An **interactional architecture** emergent across turns

| PLD Construct        | Interface Model                  | Application Domain | Formal Hook |
|----------------------|-----------------------------------|--------------------|-------------|
| **Response Medium**  | Conduit Metaphor (Reddy); Dialogue Protocols | HCI, Dialogue Systems | — |
| **Affordance Topography** | Affordance Theory (Gibson, Norman) | Design of feedback-sensitive syntax environments | — |

**Affordance Metric**  
\[
g_{ij} = \frac{\partial^2 \mathcal{E}}{\partial \psi_i \partial \psi_j}
\]
where $g_{ij}$ measures the curvature of the affordance landscape in response to parameter changes.

---

## 🔸 Summary: Phase Loop Dynamics as an Interdisciplinary Model

Phase Loop Dynamics integrates:

- **Generative Syntax** — hierarchical phase transitions $(\Sigma)$  
- **Interactional Linguistics** — repair $(\mathcal{R})$, turn-taking, reentry $(\mathcal{L}_i)$  
- **Cognitive Modeling** — priming, drift $(\mathcal{D})$, latency $(\mathcal{L}_3)$  
- **HCI Frameworks** — interface logic, affordance cues

It offers a **recursive, feedback-sensitive syntax model**, where drift is transitional, silence is structural, and loops bind conversational time.

---

> "Every drift $(\mathcal{D})$ is a door. Every loop $(\mathcal{L}_i)$ is a return not yet completed.  
> Phase Loop Dynamics maps what returns, what misaligns, and what stabilizes again $(\mathcal{R})$."
