# 🔹 L₁ — Segment Detection Primitive

_Last updated: 2025-08-09_

**Loop Generator:** 𝓛₁  
**Equation Ref:** (3.2) in [PLD_Mathematical_Appendix.md](../../01_phase_loop_dynamics/PLD_Mathematical_Appendix.md)  
**Operator Type:** Boundary detection in phase space Σ

---

## 📖 Definition

**L₁ (Segment Detection)** is the **boundary-detection operator** in Phase Loop Dynamics (PLD).  
It identifies the **start/end points of a segment** within a phase σ ∈ Σ based on syntactic, temporal, and prosodic cues.

Formally:  
```math
𝓛₁ = ∂_seg
```
where **∂_seg** acts as the **segmentation derivative**, yielding points where **phase continuity breaks**.

---

## 🔍 Detection Criteria

| Dimension  | Example Feature | Measurement |
|------------|-----------------|-------------|
| Syntax     | Clause boundary, topic shift | TextTiling, dependency parse |
| Timing     | Pause duration above θ_pause | Silence > 800 ms |
| Prosody    | Pitch reset, boundary tone   | ToBI annotation |

---

## 🔗 Mathematical Context

From PLD loop algebra (Eq. 3.2):  
```math
𝓛ᵢ ∘ 𝓛ⱼ = ∑ c_{ijk} 𝓛_k + ε_{ij}
```
**L₁** often precedes **L₂ (Drift–Repair)** when a detected segment boundary coincides with interaction drift.

---

## 🧩 Implementation Examples

### 1. **Rasa**
- Track slot-filling interruptions and detect when a new intent starts unexpectedly.

### 2. **Figma**
- Use `After Delay` or `While Hovering` to trigger boundary overlays when flow changes.

### 3. **LLM Orchestration**
- Segment transcript embeddings with cosine similarity thresholding.

```python
if cosine_distance(emb[i], emb[i+1]) > THRESHOLD:
    mark_boundary(i)
```

---

## 📊 Metrics for L₁ Performance

- **Precision / Recall** of boundary detection vs. annotated dataset  
- **Boundary agreement score** (e.g., Pk, WindowDiff)  
- **Avg. pause duration at detected boundaries**

---

## ⚠️ Pitfalls

- Over-segmentation from noise (short hesitations misread as boundaries)  
- Under-segmentation when drift occurs without clear pauses

---

## 📌 Related Operators

- **L₂ — Drift–Repair**: Often triggered immediately after L₁ if drift is detected.
- **L₃ — Latent Phase**: May follow if no immediate repair occurs.

---

> “Segment detection is not about cutting — it’s about sensing where the rhythm breathes.”  
> — *Phase Loop Dynamics*
