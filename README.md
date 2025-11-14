# 🚀 Phase Loop Dynamics (PLD) & Meta-Intelligence Research Hub  
*A unified space for timing-aware interaction design, multi-AI cognition, and empirical validation.*  
*(“Timing-aware” = detecting and correcting interaction state mismatches such as latency drift, LLM inconsistency, or lost intent.)*

This repository brings together two major research tracks:

1. **Phase Loop Dynamics (PLD)** — A timing-aware model for Drift → Repair → Resonance in AI/UX interactions, backed by empirical data.  
   *(Drift = timing/state mismatch; Repair = corrective adjustment; Resonance = restored stable pattern)*  

2. **Meta-Intelligence Integration Framework** — A multi-layer cognitive architecture for coordinating heterogeneous AI systems.  
   *(Designed for orchestrating multi-agent pipelines or model ensembles.)*

If you’re new here, start with the **Quickstart Kit**.

---

# 📌 Quick Navigation

| Goal | Start Here |
|------|------------|
| **Build or fix real-time AI interactions** | [▶︎ Quickstart Kit](./02_quickstart_kit/README_quickstart.md) |
| **See measured system performance (N=200)** | [Operational Insights](#-measured-performance--operational-insights-n200) |
| **Explore formal theory / academic mapping** | [Theory & Research](#-Theory--Research-for-joint-rd) |
| **Work with multiple AI agents** | [Meta-Intelligence Cognitive Framework](./04_meta-intelligence-framework) |

---

# ⚡ Quickstart — Build Better Interactive Systems in Hours

**[`02_quickstart_kit`](./02_quickstart_kit)**  

Ready-to-use patterns for:

- **Rasa** — Soft repair templates, intent reentry flows  
  *(Soft Repair = small correction without losing context; Reentry = restoring user intent after drift)*  

- **Figma** — Latency-hold UI patterns  
  *(Prevent perceived errors during backend delays)*  

- **LLMs** — Drift/Repair prompts & timing-aware templates  
  *(Drift detection via prompt structure & state grounding)*  

- **Logging** — Drift / Repair / Reentry event formats  
  *(Standard schemas for timing-aware analytics)*

**Purpose:**  
Get from theory → working prototype *immediately*.

---

# 📊 Measured Performance & Operational Insights (N=200)

*First empirical validation of the PLD/HCI model using 200 task-oriented dialogues (MultiWOZ 2.4).*

| Metric | Value | Insight |
|--------|-------|---------|
| **Outcome-Complete Rate** | **75.0%** | Standard task success rate |
| **Hard Repair Rate** | **10.0%** | **Critical:** 1 in 10 dialogues required full context reset *(Hard Repair = forced fallback when AI state becomes unrecoverable)* |
| **Highest Drift Type** | **Drift–Information** | **#1 System Risk:** DB errors / “no result” artifacts *(Information Drift = mismatch between system assumptions and true DB/knowledge-state)* |
| **UX Repair Rate** | **60.0%** | Soft Repair frequently stabilizes the dialogue *(Soft Repair = lightweight elaboration to keep user aligned)* |

### 📌 Core Mandate: Eliminate the *Information Drift Trap*

The largest structural failure arises when a system says *“no result”* and later contradicts itself.  
→ Users instantly lose trust. *(A typical Drift–Information pattern)*

### ✔ Mandatory Fix (Operational Recommendation)
**Ban generic “not found” responses.**  
Default to **Soft Repair (Repair–AddInfo)** with a viable alternative:

> “No 4-star hotels in the medium range — would a lower price range work?”

See full analysis:  
**→ [`07_empirical_studies/multiwoz_2.4_n200`](./07_empirical_studies/multiwoz_2.4_n200)**

---

# 🧰 Bridge-Hub — Detection & Measurement Engine

**[`03_pld-Bridge-Hub`](./03_pld-Bridge-Hub)** provides the analytics backbone:

Includes:

- `pause_classifier_bot.py` *(classifies pause types: latency vs cognitive vs drift)*  
- `latency_tracker.py` *(detects backend-induced timing mismatches)*  
- `reentry_detector.py` *(identifies when a user tries to restore earlier intent)*  
- Validation tools (`pld_event.schema.json`, `metrics_schema.yaml`)  
- Demo tools (`DEMORUN.md`)

Use this to build **timing-aware agents** that avoid cascading drift.

---

# 🎨 Design & Development Patterns

### For Industry
- Reduce drop-offs  
- Prevent drift failures *before* they propagate  
- Embed repair loops that stabilize multi-turn flows  

### For Designers
- Latency-hell UI patterns (prevent user mistrust)  
- Rhythm-friendly transitions (smooth pacing)  

### For Developers
- Rasa soft repair patterns  
- LLM drift/repair/reentry patterns *(implemented with state-grounding prompts)*  

---

# 🔬 Big Picture — PLD in 4 Stages

1. **Observation** *(detect timing/state anomalies)*  
2. **Structural Model** *(formal Drift/Repair/Resonance loops)*  
3. **Implementation Kit** *(patterns, detectors, event schemas)*  
4. **Applications** *(AI agents, multimodal systems, real-time UX)*  

---

# 🧠 Meta-Intelligence Integration Framework

[**View Project →**](./04_meta-intelligence-framework)

A four-layer cognitive system enabling **systematic multi-AI collaboration**  
*(model orchestration, role-based pipelines, and reflective oversight)*.

---

# 🧩 Theory & Research (for Joint R&D)

- Glossary & Academic Mapping  
- Mathematical Appendix  
- Academic-to-PLD Reverse Mapping  
- Category-theory mappings  

Located in `01_phase_loop_dynamics/`.

---

# 📚 Structural Rhythm — Core Concepts  
*(with Applied-AI supplements)*

1. **Drift (𝒟)** — *timing/state mismatch; delay, hallucination, or misalignment*  
2. **Repair (ℛ)** — *corrective adjustment; adding info, clarifying, or re-grounding*  
3. **Resonance (𝓛₅)** — *stable repeating interaction pattern that reinforces coherence*  

---

# 🎥 Supplemental Link Only — Minimal Demo (13s)

*This is a minimal execution preview, included only for completeness.*  
**[YouTube: Minimal Demo](https://youtu.be/nI0S8Aaywgc)**

---

# 🤝 Collaboration

| Role | First Step |
|------|------------|
| Industry Partner | Pilot Project |
| UX Researcher | Quickstart Kit |
| Academic Collaborator | Academic Mapping |

Contact: deepzenspace[at]gmail[dot]com  
X: @DeepZenSpace

---

# 📄 License

Creative Commons BY-NC 4.0  
Commercial use requires permission.

© 2025 Your Name / Organization
