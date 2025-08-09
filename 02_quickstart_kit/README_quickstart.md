# 🚀 PLD Quickstart Guide (with Mathematical Foundations)

> This quickstart introduces **Phase Loop Dynamics (PLD)** for researchers and developers.  
> It now integrates references to the **formal mathematical model** from the *PLD Mathematical Appendix — Integrated Edition (2025-08-08)*.

---

## 1. What is PLD?

**Phase Loop Dynamics (PLD)** is a framework for modeling dialogue as a sequence of *phases* connected through dynamic feedback loops.  
It bridges **linguistic interaction** (alignment, repair, resonance) and **mathematical modeling** (phase spaces, operators, and loop algebra).

---

## 2. Core Concepts

| PLD Term | Description | Math Ref |
|----------|-------------|----------|
| **Structural Phase** | Bounded syntactic/interactional unit. | Σ (eq. 1.1) |
| **Drift** | Gradual, loop-driven change in structure or meaning. | 𝒟(σ,t) (eq. 1.3) |
| **Cue-Driven Repair** | Mechanism restoring interaction after trouble. | ℛ(σ) (eq. 1.5) |
| **Resonance** | Echoing of elements across turns. | Fixed point σ* (Theorem 2) |
| **Alignment** | Synchronization of linguistic forms/interpretations. | Alignment tensor 𝒜⊗𝒜 (sec. 3.2) |
| **Coherence** | Global semantic/logical stability. | C(σ,t) (eq. 1.4) |
| **Rhythm** | Temporal turn-taking pattern. | Oscillator coupling (sec. 2.3) |
| **Silence** | Interactional gap with significance. | Latent phase 𝓛₃ (sec. 3.2) |

See the [Academic Mapping](./01_phase_loop_dynamics/related_work/academic_to_pld_reverse.md) for cross-disciplinary terminology.

---

## 3. Mathematical Model Overview

PLD is defined over a **phase space** Σ, with:
- **State representation:** σ = (s, t, p) ∈ Σ, combining syntactic derivation *s*, temporal coordinate *t*, and prosodic parameters *p*. (eq. 1.1)
- **Distance metric:** d(σ₁, σ₂) combining embedding distance and temporal offset. (eq. 1.2)
- **Drift operator:** 𝒟(σ,t) measuring deviation via coherence gradients. (eq. 1.3)
- **Repair operator:** ℛ(σ) applying kernel-weighted adjustments. (eq. 1.5, 1.6)
- **Loop generators:** 𝓛₁…𝓛₅ composing into a loop algebra. (eq. 1.7)

### Key Theorems
- **Drift–Repair Duality** — The drift kernel matches the image of repair. (Theorem 1)
- **Resonance Fixed-Point** — There exists a unique stable resonance state σ*. (Theorem 2)
- **Loop Closure as Lie Algebra** — Generators satisfy closure under commutators. (Theorem 5)

For full derivations, see [`PLD_Mathematical_Appendix.md`](./01_phase_loop_dynamics/PLD_Mathematical_Appendix.md).

---

## 4. Quickstart Steps

### 4.1 Installation
Clone the repository:
```bash
git clone https://github.com/your-org/pld.git
cd pld
```

### 4.2 Load PLD Core
```python
from pld.core import PhaseLoopModel

model = PhaseLoopModel()
model.load_defaults()
```

### 4.3 Run a Simulation
```python
state = model.initialize_phase()
trajectory = model.run(duration=30.0)  # seconds
model.plot(trajectory)
```

### 4.4 Apply Drift–Repair Cycle
```python
from pld.math import drift, repair

sigma = state
sigma_drifted = drift(sigma, t=1.5)
sigma_repaired = repair(sigma_drifted)
```

---

## 5. References

- **Mathematical Appendix:** [PLD_Mathematical_Appendix.md](./01_phase_loop_dynamics/PLD_Mathematical_Appendix.md)  
- **Academic Mapping:** [academic_to_pld_reverse.md](./01_phase_loop_dynamics/related_work/academic_to_pld_reverse.md)  
- **Forward Mapping:** [pld_to_academic.md](./01_phase_loop_dynamics/related_work/pld_to_academic.md)

---

> **Tip for Researchers:** The *Mathematical Appendix* retains stable equation numbering. You can cite eq. (1.3) or Theorem 2 directly in your papers.
