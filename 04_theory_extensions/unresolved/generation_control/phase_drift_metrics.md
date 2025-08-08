# 📊 Phase Drift Metrics and Detection  
**Toward a Unified Phase Drift Scoring Framework (PDSF)**  
*Status*: Proposed Core Module  
*Location*: `/metrics/phase_drift_detection.md`

---

## ❓ Core Question

How can we **detect**, **quantify**, and **track** Phase Drift phenomena in LLMs—including spirals, semantic rupture, coherence collapse, and syntactic loop traps?

This module defines a unified metric suite for mapping **structural deformation over time**, enabling both **evaluation** and **interactive guidance**.

---

## 🧠 Core Metric Suite: *Phase Drift Profile (PDP)*

| **Metric**                        | **Targeted Signal**              | **Methodology**                                                      | **Output Format**                    |
|----------------------------------|----------------------------------|----------------------------------------------------------------------|--------------------------------------|
| `Resonance Index (RI)`           | Rhythmic/lexical repetition      | N-gram / POS recurrence analysis                                     | Float `0.0–1.0`                       |
| `Loopiness Score (L)`            | Recursive phrasing               | Levenshtein loop detection, phrase reentry scoring                   | Integer / scaled float               |
| `Semantic Drift Index (SDI)`     | Conceptual divergence            | SBERT/embedding cosine delta over sliding windows                    | Float (↑ = more drift)               |
| `Phase Change Score (PCS)`       | Structural mode shift            | Tree edit distance, sentence type classification                     | Float                                |
| `Coherence Disruption Score (CDS)` | Logical failure                 | Entity grid entropy, coref disruption, discourse classifier          | Confidence score / binary flag       |
| `Activation Gradient Divergence (AGD)` | Internal routing rupture    | Delta of attention centroids or neuron clusters                      | Vector / scalar trendline            |

Together, these form a **Phase Drift Profile (PDP)** that can be tracked across generative sequences.

---

## 🧪 Detection Techniques

### 🔁 Sliding Window Evaluation

- Token windows (e.g., 30–50 tokens)  
- Track entropy shifts, syntax volatility, semantic trajectory  

### 🌳 Structural Signature Extraction

Use dependency parsers (e.g., spaCy, Trankit) to extract:

- POS cadence  
- Parse tree volatility  
- Clause depth and balance  

### 🎯 Attention + Embedding Divergence

For model-internal access:

- Compute per-layer centroid drift  
- Compare attention maps across spans  
- Identify trajectory rupture zones

---

## 📈 Visualizations: *Phase Trajectory Plot*

- **X-axis**: Token index or generation timestep  
- **Y-axis**: One or more drift metric values  
- **Overlay Regions**:
  - 🔴 Spiral Zones (high RI + L)  
  - 🟡 Semantic Faultlines (SDI spikes)  
  - 🟢 Stable Basins (low CDS, stable RI)

Optionally paired with **prompt onset markers** or **user-intervention flags**.

---

## 🧩 Application Matrix

| **Scenario**              | **Use**                                                       | **Metrics Emphasized**               |
|---------------------------|---------------------------------------------------------------|--------------------------------------|
| Generation Debugging      | Catch incoherence, loop traps, or hallucinatory spirals       | RI, CDS, PCS                         |
| Prompt Evaluation         | Score drift potential of prompt templates                     | SDI, RI                              |
| Model Comparison          | Analyze phase behavior across GPT, Claude, Mistral, etc.       | All PDP metrics                      |
| Corpus Filtering          | Identify degraded samples in fine-tuning datasets              | CDS, L, PCS                          |
| Real-Time UI Guidance     | Alert users to onset of drift or collapse                      | RI + SDI trendlines                  |

---

## ⚠️ Challenges & Mitigation

| **Challenge**                         | **Response Strategy**                                                |
|--------------------------------------|----------------------------------------------------------------------|
| Style ≠ Degradation (false positives) | Require convergence of ≥3 metrics for drift classification           |
| Model-variant sensitivity             | Normalize scores relative to model class and generation length       |
| Interpretability of raw metrics      | Use visual overlays and human-labeled baselines for validation       |
| Cost of multi-pass metrics           | Use distilled models (e.g., MiniLM) and batch inference strategies   |

---

## 📂 Suggested Output Schema (`phase_drift_report.json`)

```json
{
  "metrics": {
    "RI": 0.74,
    "L": 2,
    "SDI": 0.42,
    "PCS": 0.21,
    "CDS": 0.66
  },
  "zones": [
    {"type": "spiral", "start": 120, "end": 170},
    {"type": "faultline", "position": 210}
  ],
  "summary": {
    "drift_class": "moderate",
    "coherence_risk": "high"
  }
}
```
## 🔮 Future Extensions

| Tool                       | Description                                                   |
|----------------------------|---------------------------------------------------------------|
| `phase_drift_benchmark.md` | Manually annotated test set with labeled drift zones         |
| `drift_compass_widget.js`  | Interactive UI showing real-time drift levels                |
| `psi_model_comparison.csv` | Phase Stability Index scores per model                      |
| `sandbox_feedback_bridge.py` | Live feedback loop to Generative Sandbox / PDCL           |

---

## 📚 Theoretical Anchors

- **Halliday & Hasan (1976)**: Cohesion and coherence theory  
- **Barzilay & Lapata (2008)**: Entity grid coherence modeling  
- **Echo State Networks**: Long-tail recurrence modeling  
- **Prompt Injection Studies**: Semantic shift under control prompts  

---

## ✅ Ready to Implement?

We can support:

- 🧪 **Building a Python-based Phase Drift Scorer** (e.g., using `spaCy` + `SBERT`)  
- 📊 **Generating metric-rich drift visualizations** from your model outputs  
- 🧾 **Designing tagging formats** for drift-aware dataset curation  
- 🧩 **Integrating PDP** into the `generative_sandbox.md` live controls  

> Drift is measurable. Collapse is preventable.  
> **Let’s build tools that map—and modulate—the generative terrain.**
