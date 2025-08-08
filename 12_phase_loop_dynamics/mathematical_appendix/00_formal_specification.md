# Formal Specification of Phase Loop Dynamics

This document defines the mathematical foundations of PLD.  
Symbols and operators are cross-referenced with [`../09_glossary_academic_mapping_math.md`](../09_glossary_academic_mapping_math.md).

---

## 1. Notation Reference

| Symbol | Meaning | Type |
|--------|---------|------|
| $\Sigma$ | Phase space | Metric space |
| $\mathcal{D}$ | Drift operator | $\Sigma \times \mathbb{R}^+ \to [0,1]$ |
| $\mathcal{R}$ | Repair operator | $\Sigma \to \Sigma$ |
| $\mathcal{L}_i$ | Loop generator | Phase transformation |
| $C(\sigma,t)$ | Coherence field | $\Sigma \times \mathbb{R}^+ \to \mathbb{R}^+$ |
| $\phi(\tau)$ | Repair kernel | $\mathbb{R} \to [0,1]$ |
| $d(\cdot,\cdot)$ | Phase distance | $\Sigma \times \Sigma \to \mathbb{R}^+$ |

---

## 2. Core Mathematical Objects

### 2.1 Phase Space
\[
\Sigma = \{\sigma = (s,t,p) \mid s \in \mathcal{S},\ t \in \mathcal{T},\ p \in \mathcal{P}\}
\]
- $\mathcal{S}$: Context-free grammar derivations  
- $\mathcal{T} \subseteq \mathbb{R}^+$: Temporal coordinates  
- $\mathcal{P}$: Prosodic parameter space

### 2.2 Phase Distance
\[
d(\sigma_1, \sigma_2) = \| \mathbf{e}_{\sigma_1} - \mathbf{e}_{\sigma_2} \|_2 + \alpha |t_1 - t_2|
\]
$\mathbf{e}_\sigma$: vector embedding; $\alpha$: temporal scaling factor.

### 2.3 Phase Transition Operators

**Drift Operator**
\[
\mathcal{D}(\sigma,t) = 1 - \frac{\|\nabla C(\sigma,t)\|}{K_{drift}}
\]
with coherence field:
\[
C(\sigma,t) = \mathrm{MI}(\sigma_{t-\delta t}, \sigma_t) + \lambda \cos(\theta_{\text{embed}})
\]
- $\mathrm{MI}$: mutual information between phases  
- $\theta_{\text{embed}}$: embedding vector angle

**Repair Operator**
\[
\mathcal{R}(\sigma) = \sigma + \lambda \int_{\tau \in T} \phi(\tau)\,\Delta(\sigma,\tau)\,d\tau
\]
with Gaussian attention kernel:
\[
\phi(\tau) = \exp\left(-\frac{(\tau-\tau_0)^2}{2s^2}\right)
\]

### 2.4 Loop Algebra
\[
\mathcal{L}_i \circ \mathcal{L}_j = \sum_{k=1}^5 c_{ijk}\mathcal{L}_k,\quad
[\mathcal{L}_i, \mathcal{L}_j] = \mathcal{L}_i\mathcal{L}_j - \mathcal{L}_j\mathcal{L}_i
\]
Generator mapping:
- $\mathcal{L}_1$: Segment detection  
- $\mathcal{L}_2$: Drift–repair  
- $\mathcal{L}_3$: Latent phase  
- $\mathcal{L}_4$: Feedback reflex  
- $\mathcal{L}_5$: Alignment–resonance

---

## 3. Axiomatic Foundation

1. **Phase Continuity**  
   Small changes in phase yield small changes in drift:
   \[
   \forall \epsilon > 0, \exists \delta > 0 : d(\sigma_1,\sigma_2) < \delta \Rightarrow |\mathcal{D}(\sigma_1)-\mathcal{D}(\sigma_2)| < \epsilon
   \]

2. **Repair Closure**  
   Repairs remain within the phase space:
   \[
   \mathcal{R}(\Sigma) \subseteq \Sigma
   \]

3. **Loop Compositionality**  
   Positive composition probability corresponds to positive structure constant:
   \[
   P(\mathcal{L}_k|\mathcal{L}_i,\mathcal{L}_j) > 0 \iff c_{ijk} > 0
   \]

---

## 4. Fundamental Theorems

1. **Drift–Repair Duality**  
   \[
   \ker(\mathcal{D}) \cong \operatorname{im}(\mathcal{R})
   \]
   The zero-drift subspace is isomorphic to the image of repair.

2. **Resonance Fixed-Point**  
   \[
   \exists!\sigma^* \in \Sigma : \mathcal{R}(\sigma^*) = \sigma^*
   \]
   There exists a unique fixed point representing a resonance phase.

---

## 5. Categorical Preview

Commutative diagram:
\[
\begin{CD}
\mathcal{C}_{\text{Seg}} @>\mathcal{L}_1>> \mathcal{C}_{\text{Cue}} \\
@V\mathcal{L}_3VV @AA\mathcal{L}_4A \\
\mathcal{C}_{\text{Lat}} @>>\mathcal{L}_5> \mathcal{C}_{\text{Res}}
\end{CD}
\]
- $\mathcal{C}_{\text{Seg}}$: Segment phases  
- $\mathcal{C}_{\text{Cue}}$: Cue phases  
- $\mathcal{C}_{\text{Lat}}$: Latent phases  
- $\mathcal{C}_{\text{Res}}$: Resonance phases
