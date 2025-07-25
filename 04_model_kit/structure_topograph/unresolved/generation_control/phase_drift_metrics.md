# 📊 Phase Drift Metrics and Detection

> **Toward a Unified Phase Drift Scoring Framework (PDSF)**

---

## ❓ Core Question

How can we **numerically detect, measure, and track** Phase Drift phenomena in LLMs—such as spirals, semantic faults, resonance zones, or coherence collapses—across time and across models?

---

## 🔢 Core Metric Suite: Phase Drift Profile (PDP)

| **Metric Name**                 | **Target Phenomenon**              | **Method**                                                                 | **Output**                            |
|--------------------------------|------------------------------------|----------------------------------------------------------------------------|---------------------------------------|
| **Resonance Index (RI)**       | Rhythmic or lexical repetition     | N-gram repetition, POS pattern cadence                                     | `0.0–1.0` (higher = more repetition)  |
| **Loopiness (L)**              | Recursive phrasing or clause loops | Levenshtein/self-similarity over sliding token windows                     | Count / score                         |
| **Semantic Drift Index (SDI)** | Topic divergence                   | Cosine distance between sentence embeddings (e.g. SBERT)                   | Float (higher = more drift)           |
| **Phase Change Score (PCS)**   | Structural/mode shift              | Parse tree edit distance, discourse type switch (e.g. narrative → list)    | Float                                 |
| **Coherence Disruption Score (CDS)** | Logical breakdown          | Entity grid breaks, coreference loss, discourse relation discontinuity     | Float / classifier score              |
| **Activation Gradient Divergence (AGD)** | Internal model rupture   | Divergence in attention or neuron activation between adjacent segments     | Layer-wise delta score                |

> Each generation yields a **Phase Drift Profile (PDP)** composed of these modular signals.

---

## 🧪 Detection Techniques

### ✅ Sliding Window Comparison

- Apply windowed analysis (e.g. 30–50 tokens)
- Compare adjacent segments using:
  - Parse tree structure
  - Embedding drift (e.g., SBERT, BERTScore)
  - Entity and topic continuity

### ✅ Structural Signature Extraction

- Use libraries like `spaCy`, `Stanza` to extract:
  - Parse tree depth
  - Embedding layers
  - Punctuation rhythm and cadence

### ✅ Attention-Based Detection

- If model internals are accessible:
  - Track shifts in attention centroids
  - Monitor neuron activation patterns layer by layer

---

## 📈 Phase Trajectory Visualization

**Real-time Plotting UI:**

- **X-axis** = token index
- **Y-axis** = metric values (RI, SDI, PCS, etc.)
- **Color overlays:**
  - 🔴 = Spiral zone
  - 🟡 = Fault zone
  - 🔵 = Stable basin
- Optional: prompt markers, structural annotations

---

## 🧩 Applications

| **Use Case**             | **Example**                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| Generation Diagnostics   | Detect hallucination onset, incoherence drop-off                           |
| Prompt Engineering       | Compare prompts by phase stability and drift trajectories                   |
| Model Comparison         | Visualize GPT vs Claude vs open-source model phase signatures              |
| Fine-tuning & Curation   | Score training samples by drift/noise profile                               |
| Real-time LLM UX         | Alert user when drift or loop regions emerge during generation              |

---

## 🚧 Challenges & Safeguards

| **Challenge**                    | **Mitigation Strategy**                                             |
|----------------------------------|---------------------------------------------------------------------|
| Threshold setting                | Use clustering / anomaly detection across metric distributions      |
| False positives for style shifts | Combine metrics (e.g. SDI + CDS must spike together)               |
| Compute cost                     | Use lightweight similarity + windowed heuristics                   |
| Cross-model variability          | Normalize scores per architecture or training regime               |

---

## 🧰 Future Extensions

- 📦 **Phase Drift Benchmark Suite** – Texts annotated with spirals, jumps, faults  
- 🧭 **Drift Compass UI** – Embeddable widget showing live phase state  
- 🔐 **Phase Stability Index (PSI)** – Model-level resilience rating  
- 🕹 **Sandbox Control Feedback Loop** – Metrics drive live generation controls

---

## 🔗 Related Work & Inspiration

- *Entity Grid Coherence Models* (Barzilay & Lapata)  
- *Lexical Cohesion* (Halliday & Hasan)  
- *Stylometry & Rhythm* (Yule’s K, cadence tracking)  
- *LLM Entropy & Loop Detection*  
- *Visual Music Tools* (Spectrograms, MIDI overlays)  

---

## 🚀 Want to Start?

We can help you:

- 🛠 Prototype a **Phase Drift Detector** in Python (`spaCy` + `SBERT`)
- 📈 Generate a **Drift Profile Report** from LLM output
- 🧪 Build a **Benchmark Corpus** for metric calibration
- 📄 Define a **JSON Schema** for drift tagging and control feedback

> Let’s turn metaphor into mechanism.

---
