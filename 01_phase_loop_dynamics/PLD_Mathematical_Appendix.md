# 📘 PLD Mathematical Appendix — Integrated Edition (Revised)
Version: 2025-08-11

---

## 1. Formal Specification of Phase Loop Dynamics  
*(from 00_formal_specification.md)*

### 1.1 Notation Reference

| Symbol | Meaning | Type | Glossary Ref |
|--------|---------|------|--------------|
| Σ | Phase space | Metric space | @core/Phase |
| 𝒟 | Drift operator | Σ × ℝ⁺ → [0,1] | @core/Drift |
| ℛ | Repair operator | Σ → Σ | @support/Repair |
| 𝓛ᵢ | Loop generator | Phase transformation | @core/Loop |
| C(σ,t) | Coherence field | Σ × ℝ⁺ → ℝ⁺ | @derived/Coherence |
| φ(τ) / ϕ(τ) | Repair kernel | ℝ → [0,1] (normalized) | @math/Kernel |
| d(·,·) | Phase distance | Σ × Σ → ℝ⁺ | @math/Distance |

> **Notation**: We use \( \varphi \) for the normalized repair kernel (revised §1.6).

---

### 1.2 Phase Space

(1.1) \( \Sigma = \{\, \sigma = (s,t,p) \mid s \in \mathcal{S},\ t \in \mathcal{T},\ p \in \mathcal{P} \,\} \)

- \( \mathcal{S} \): Context-free grammar derivations  
- \( \mathcal{T} \subseteq \mathbb{R}^+ \): Temporal coordinates  
- \( \mathcal{P} \): Prosodic parameter space

---

### 1.3 Phase Distance

(1.2) \( d(\sigma_1, \sigma_2) = \lVert e_{\sigma_1} - e_{\sigma_2} \rVert_2 + \alpha\, |t_1 - t_2| \)

- \( e_\sigma \): vector embedding  
- \( \alpha \): temporal scaling factor

---

### 1.4 Drift Operator

(1.3) \( \mathcal{D}(\sigma,t) = 1 - \big( \lVert \nabla C(\sigma,t) \rVert \,/\, K_{\text{drift}} \big) \)

with coherence field:

(1.4) \( C(\sigma,t) = \mathrm{MI}(\sigma_{t-\delta t}, \sigma_t) + \lambda \cos(\theta_{\text{embed}}) \)

- MI: mutual information between phases  
- \( \theta_{\text{embed}} \): embedding vector angle

---

### 1.5 Repair Operator

(1.5) \( \mathcal{R}(\sigma) = \sigma + \lambda \int_{\tau\in T} \varphi(\tau)\, \Delta(\sigma,\tau)\, d\tau \)

> **Interpretation**: With the normalized kernel (1.6), (1.5) implements a time-local **normalized averaging** of the discrepancy term \( \Delta(\sigma,\tau) \) around \( \tau_0 \) with bandwidth \( s \).

---

### 1.6 Gaussian Attention Kernel (Normalized) — **Revised**

(1.6) \( \displaystyle \varphi(\tau) \;=\; \frac{1}{\sqrt{2\pi}\,s}\,
\exp\!\left( -\,\frac{(\tau-\tau_0)^2}{2s^2} \right), \qquad s>0 \)

Properties:  
\( \int_{-\infty}^{\infty}\varphi(\tau)\,d\tau = 1 \),  
\( \varphi(\tau_0+\delta)=\varphi(\tau_0-\delta) \),  
\( \lVert \varphi \rVert_{L^1}=1 \).

**Lemma 1.6.A (Series approximation of kernel repair).**  
Assume \( \Delta(\sigma,\tau) \) is sufficiently smooth in \( \tau \) around \( \tau_0 \) and admits a Taylor expansion up to order \( m \):
\[
\Delta(\sigma,\tau_0+\delta)=\sum_{k=0}^{m}\frac{\delta^k}{k!}\,
\partial_\tau^{(k)}\Delta(\sigma,\tau_0)+\mathcal{O}(\delta^{m+1}).
\]
Then the kernel integral in (1.5) with the normalized Gaussian (1.6) satisfies
\[
\int_{\mathbb{R}}\varphi(\tau)\,\Delta(\sigma,\tau)\,d\tau
\;=\;
\sum_{k=0}^{m}\frac{\mu_k(\varphi)}{k!}\,
\partial_\tau^{(k)}\Delta(\sigma,\tau_0)\;+\;\mathcal{O}(s^{m+1}),
\]
where \( \mu_k(\varphi)=\int (\tau-\tau_0)^k \varphi(\tau)\,d\tau \) are the (centered) moments of \( \varphi \).  
For the Gaussian (1.6),
\[
\mu_{2n+1}(\varphi)=0,\qquad
\mu_{2n}(\varphi)=(2n-1)!!\,s^{2n}\quad (n\in\mathbb{N}).
\]

**Corollary 1.6.B (Mapping to series form).**  
Let the repair operator in (1.5) be written as
\( \mathcal{R}(\sigma) = \sigma + \lambda \int \varphi(\tau)\,\Delta(\sigma,\tau)\,d\tau \).
Under the assumptions of Lemma 1.6.A we obtain the local series:
\[
\mathcal{R}(\sigma)
= \sigma + \sum_{k=0}^{m} a_k\,\partial_\tau^{(k)}\Delta(\sigma,\tau_0)
\;+\;\mathcal{O}(s^{m+1}),
\quad
a_k \;=\; \lambda\,\frac{\mu_k(\varphi)}{k!}.
\]
In particular, for the Gaussian kernel, odd-order coefficients vanish (\( a_{2n+1}=0 \)) and
\( a_{2n}=\lambda\,\frac{(2n-1)!!}{(2n)!}\,s^{2n} \).
Hence the series-type formulation used in **02_phase_mechanics** (Taylor-type repair)
is an **asymptotic approximation** of the kernel form, with explicit coefficient identification via the kernel moments.

*Proof (sketch).* Expand around \( \tau_0 \) and integrate term-wise; use centered moments of the Gaussian. □

*Remark.* Coefficient sign conventions in the series form depend on the residual definition inside \( \Delta \) and the expansion point; in the paper, we state that series coefficients \( \tilde a_k \) **absorb** the kernel-moment identification \( a_k \).

---

### 1.7 Loop Algebra

(1.7) \( \mathcal{L}_i \circ \mathcal{L}_j = \sum_{k=1}^5 c_{ijk}\, \mathcal{L}_k \), \[ \,[\mathcal{L}_i,\mathcal{L}_j] = \mathcal{L}_i\mathcal{L}_j - \mathcal{L}_j\mathcal{L}_i \]

Generator mapping:  
- \( \mathcal{L}_1 \): Segment detection  
- \( \mathcal{L}_2 \): Drift–repair  
- \( \mathcal{L}_3 \): Latent phase  
- \( \mathcal{L}_4 \): Feedback reflex  
- \( \mathcal{L}_5 \): Alignment–resonance

---

### 1.8 Axioms

1. **Phase Continuity**  
 \( \forall \varepsilon>0,\, \exists \delta>0: d(\sigma_1,\sigma_2) < \delta \Rightarrow |\mathcal{D}(\sigma_1)-\mathcal{D}(\sigma_2)| < \varepsilon \)

2. **Repair Closure**  
 \( \mathcal{R}(\Sigma) \subseteq \Sigma \)

3. **Loop Compositionality**  
 \( P(\mathcal{L}_k \mid \mathcal{L}_i,\mathcal{L}_j) > 0 \iff c_{ijk} > 0 \)

---

### 1.9 Theorems

**Theorem 1 — Drift–Repair Duality**  
 \( \ker(\mathcal{D}) \cong \mathrm{im}(\mathcal{R}) \)

**Theorem 2 — Resonance Fixed-Point**  
 \( \exists!\, \sigma^* \in \Sigma : \mathcal{R}(\sigma^*) = \sigma^* \)

---

### 1.10 Categorical Preview

Commutative diagram mapping between loop categories (see `diagrams/pld_commutative_diagram.svg`).

---

## 2. Dynamical Systems Formulation of PLD  
*(from 01_dynamical_systems.md)*

### 2.1 State-Space Representation

(2.1) \( \dfrac{d\Psi}{dt} = A\,\Psi(t) + F_{\text{ext}}(t) \)

State vector: \( \Psi(t) = ( \psi_d, \psi_r, \psi_l )^\top \)  
Matrix \( A \) defined as per system parameters \( (\alpha,\beta,\gamma,\delta,\varepsilon,\zeta,\eta) \)

---

### 2.2 Phase Manifold Geometry

(2.2) \( g_{ij} = \partial^2 E / (\partial \psi_i\, \partial \psi_j) \)

Energy functional:  
(2.3) \( E(\Psi) = \tfrac{1}{2}\psi_d^2 + \tfrac{1}{4}\psi_r^4 + \lambda e^{-\psi_l} \)

---

### 2.3 Interaction Dynamics

External coupling:  
(2.4) \( F_{\text{ext}} = \sum_k \mathcal{J}_{ijk}\, \Psi^{(k)}(t-\tau) \)

---

### 2.4 Stability and Limit Cycles

- **Theorem 3:** Equilibrium stability conditions via Lyapunov exponents  
- **Theorem 4:** Limit cycle existence if \( \beta\gamma > \alpha\delta \)

---

### 2.5 Stochastic Formulation

Langevin dynamics:  
(2.5) \( d\Psi = (A\Psi + F_{\text{ext}})\, dt + \sigma\, dW_t \)

Fokker–Planck:  
(2.6) \( \partial P/\partial t = -\nabla\cdot(vP) + \tfrac{1}{2} \sum_{i,j} D_{ij}\, \partial^2 P/(\partial \psi_i \partial \psi_j) \)

---

## 3. Phase Algebra: Structural Operators and Loop Composition  
*(from 02_phase_algebra.md)*

### 3.1 Space Decomposition

(3.1) \( \Sigma = \bigoplus_{k=1}^5 \Sigma_k \)

---

### 3.2 Generator Definitions

\( \mathcal{L}_1 = \partial_{\text{seg}} \) (Boundary detection)  
\( \mathcal{L}_2 = \mathcal{D}\,\mathcal{R} \) (Drift–repair cycle)  
\( \mathcal{L}_3 = e^{-\tau \partial_t} \) (Latency operator)  
\( \mathcal{L}_4 = \mathcal{F}^\dagger\mathcal{F} \) (Feedback adjoint)  
\( \mathcal{L}_5 = \mathcal{A}\otimes\mathcal{A} \) (Alignment tensor)

---

### 3.3 Composition Laws

(3.2) \( \mathcal{L}_i \circ \mathcal{L}_j = \sum c_{ijk}\, \mathcal{L}_k + \varepsilon_{ij} \)

---

### 3.4 Key Theorems

**Theorem 5:** Loop closure as Lie algebra  
**Theorem 6:** Resonance stability via minimal \( n \)

---

## 4. Topological Analysis of PLD  
*(from 03_topological_analysis.md)*

### 4.1 Phase Space Topology

(4.1) \( \Sigma \cong S^1 \times \mathbb{R}^2 \)

---

### 4.2 Homology, Fundamental Group

\( H_n(\Sigma) = \mathbb{Z} \) for \( n=0,1 \); otherwise 0  
\( \pi_1(\Sigma) = \mathbb{Z} \)

---

### 4.3 Loop Invariants

Winding number:  
(4.2) \( \nu(\Gamma) = \frac{1}{2\pi} \oint_\Gamma \big(\frac{d\phi}{dt}\big)\, dt \)

Drift–repair index: \( I_{\text{DR}} = \#(\text{drift}) - \#(\text{repair}) \)

---

### 4.4 Theorems

**Theorem 7:** Topological rigidity  
**Theorem 8:** Loop separation (geodesic constraint)

---

## 5. Metric Space Analysis of PLD  
*(from 04_metric_spaces.md)*

### 5.1 Phase Distance Metric

(5.1) \( d_\Sigma(\sigma_1, \sigma_2) = \inf_\gamma \int_0^1 \sqrt{ g_{\gamma(t)}(\dot\gamma, \dot\gamma) }\, dt \)

---

### 5.2 Local Metric Tensor

(5.2) \( g_{ij}(\sigma) = \big[\text{matrix form with } \alpha, \beta, \lambda \big] \)

---

### 5.3 Properties

- Completeness of \( (\Sigma, d_\Sigma) \)  
- Geodesic equations and Christoffel symbols

---

### 5.4 Concentration Phenomena

Modulus of continuity: \( \omega(\delta) \)  
Doubling condition for \( \mu(B_r) \)

---

### 5.5 Fractal Analysis

Hausdorff dimension \( \dim_H(\Sigma_k) \)  
Spectral dimension \( d_s \)

---

### 5.6 Stability Theorems

**Theorem 9:** Lipschitz continuity of \( d_\Sigma \)  
**Theorem 10:** Gromov–Hausdorff convergence \( \Sigma_n \to \Sigma \)

---

## Appendix A — Cross-reference Index

This index maps each mathematical object to its prose introduction in `00_introduction.md` and `01_foundations.md`.  
Theorems retain their original numbering for citation stability.

- \( \Sigma \) — Introduction §1; Foundations §1  
- \( \mathcal{D} \) — Introduction §3; Mechanics §1; Appendix §1.4  
- \( \mathcal{R} \) — Foundations §3; Mechanics §2; Appendix §1.5–1.6  
- \( \mathcal{L}_i \) — Loop Structures; Appendix §1.7; Algebra §3  
- \( C(\sigma,t) \) — Appendix §1.4  
- Kernels/Series link — Appendix §1.6 Lemma 1.6.A / Cor. 1.6.B; Mechanics §2 (series)

---

**Change Log (2025-08-11):**  
- §1.6 kernel **normalized**; properties stated explicitly.  
- Added **Lemma 1.6.A** and **Corollary 1.6.B** (kernel–series correspondence).  
- §1.5 note updated to clarify normalized averaging semantics.  
- Notation table updated (ϕ).
