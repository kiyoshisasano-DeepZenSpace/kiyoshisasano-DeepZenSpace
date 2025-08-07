# 🧠 Design Rationale for PLD Structure Generators

This document outlines the key design decisions behind the structure generators in the **Phase Loop Dynamics (PLD)** project.  
It links practical implementation constraints with theoretical grounding from PLD Papers #1 and #2.

---

## 📘 Theory-Backed Decisions

### Pause Threshold Selection
- **Default:** `800ms`  
- **Source:** PLD Paper1 Fig.3 (cognitive delay threshold)  
- **Adjustment:** Scaled with a correction factor derived from modified Fitts' Law for UI latency friction.

---

## 🧩 Modularity & Extensibility

All core generators (pause classifier, reentry detector, latency tracker) emit interpretable results as simple dictionaries.

They may be chained, customized, or embedded into UI agents or research environments.

### JSON Schema Example
```json
{
  "phase": "drift|repair|reentry",
  "timestamp": "ISO8601",
  "confidence": 0.0-1.0
}
```
This format ensures interoperability across bots, Notion dashboards, and log visualizers.

---

## ⚖️ Design Tradeoffs

| Design Option     | Theoretical Strength | Practical Cost |
|------------------|----------------------|----------------|
| Use GPT-4 only    | ✅ Stable reasoning  | 💸 Expensive    |
| Add fallback model | ⚠️ Variable nuance  | ✅ Fast         |
| Log to memory     | ✅ Fast & flexible   | ⚠️ Volatile     |
| Log to CSV        | ✅ Persistent        | ✅ Cheap        |

The current release prioritizes:  
→ **Clarity of output** over compute optimization  
→ **Alignment with PLD constructs** over general-purpose classification

---

## 🔄 Implementation Scope

Each generator addresses a specific PLD phase dynamic:

| Tool                | PLD Phase Focus   |
|---------------------|------------------|
| `pause_classifier.py` | ⏸️ Pause / Drift    |
| `reentry_detector.py` | 🔁 Reentry          |
| `latency_tracker.py`  | 🕒 Latency Hold     |

Extensions may introduce:  
- Loop closure tracking  
- Multimodal signal fusion (e.g., gaze, touch, biometric drift)

---

## 🧭 Theory Mapping

| Concept         | Implementation Reflection                        |
|----------------|--------------------------------------------------|
| Drift           | Pause exceeding threshold                        |
| Repair          | Classification of cue response or retry action   |
| Reentry         | Semantic return to earlier latent segment        |
| Latency Hold    | Explicitly designed waiting or suspense region   |

See [`docs/zenodo_paper_links.md`](../docs/zenodo_paper_links.md) for mapping to PLD publications.

---

## 🌐 Design for Open Collaboration

- Configurable via environment variables and constants
- Errors return structured fallbacks
- CLI usage & integration examples included in each module

---

## 📜 Versioning

This generator suite follows **semantic versioning**, with major version bumps when core theory shifts:

- PLD Paper update ⇒ Generator `v2.x.x`  
- Minor tooling fix ⇒ `v1.3.x`  
- New modality added ⇒ `v1.x.0`

See `docs/version_mapping.md` for PLD-paper-to-code alignment.

---

## 🔬 Performance Benchmarks

Target responsiveness:

| Component        | Time Budget |
|------------------|-------------|
| GPT classification | < 500ms     |
| CSV logging        | < 100ms     |

These thresholds reflect PLD Paper1's real-time drift/repair envelope.
