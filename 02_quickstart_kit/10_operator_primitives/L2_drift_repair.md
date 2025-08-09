# 🔹 L₂ — Drift–Repair Primitive

_Last updated: 2025-08-09_

**Loop Generator:** 𝓛₂  
**Equation Ref:** (3.2) and (1.3)–(1.5) in [PLD_Mathematical_Appendix.md](../../01_phase_loop_dynamics/PLD_Mathematical_Appendix.md)  
**Operator Type:** Sequential drift detection and repair initiation

---

## 📖 Definition

**L₂ (Drift–Repair)** is the **paired operator** that detects interaction drift (𝒟) and applies the repair operator (ℛ) to restore coherence.

Formally:  
```math
𝓛₂ = 𝒟ℛ
```
where:

- **𝒟**: Drift operator — measures deviation from the coherence field C(σ,t)  
- **ℛ**: Repair operator — applies corrective adjustment to return σ to a stable state in Σ

---

## 🔍 Drift Detection Criteria

| Dimension       | Example Metric                                  | Equation Ref |
|-----------------|------------------------------------------------|--------------|
| Semantic Shift  | Drop in mutual information MI                   | (1.4)        |
| Temporal Delay  | Silence exceeding θ_drift                       | (1.3)        |
| Structural Gap  | Phase distance d(σ₁, σ₂) above threshold        | (1.2)        |

---

## 🛠 Repair Strategies

| Repair Type   | UX Example                                | Implementation Note |
|---------------|-------------------------------------------|----------------------|
| Soft Repair   | “Did you mean…?” prompt                    | Low friction, retry path |
| Hard Repair   | Reset to safe default                      | Use only after soft repair fails |
| Contextual    | Suggest based on last valid σ              | Requires state persistence |

---

## 🔗 Mathematical Context

Drift operator:  
```math
𝒟(σ,t) = 1 − (‖∇C(σ,t)‖ / K_drift)
```
Repair operator:  
```math
ℛ(σ) = σ + λ ∫ φ(τ) Δ(σ,τ) dτ
```
Combined as sequential operation:  
```math
𝓛₂(σ) = ℛ(  detect_drift(σ)  )
```

---

## 🧩 Implementation Examples

### 1. **Rasa**
- Use `FallbackAction` with intent confidence threshold + history-based trigger

### 2. **Figma**
- Overlay “clarification card” after prolonged hover or idle state

### 3. **LLM Orchestration**
- Monitor embedding drift; if cosine distance > threshold, inject clarification prompt

```python
if drift_score(σ) > DRIFT_THRESHOLD:
    σ = repair(σ)
```

---

## 📊 Metrics for L₂ Performance

- Drift-to-repair ratio (DRR)  
- Repair success rate (RSR)  
- Mean time from drift to reentry (MTD→R)

---

## ⚠️ Pitfalls

- Over-triggering repair on minor deviations  
- Failing to cap repair attempts (infinite loop risk)  
- Ignoring latent phase transitions after drift

---

## 📌 Related Operators

- **L₁ — Segment Detection**: Can trigger L₂ if a boundary is accompanied by drift.  
- **L₃ — Latent Phase**: May follow if drift is left unresolved.

---

> “Drift is an invitation; repair is the response.”  
> — *Phase Loop Dynamics*
