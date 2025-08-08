# 🔍 PLD Trace Analysis Demo

**Visualizing Conversational Structures in UX Flows**

This demo provides a lightweight analyzer based on [Phase Loop Dynamics (PLD)](https://zenodo.org/records/16736820).  
It identifies and annotates structural rhythm patterns such as:

- ⏸️ **Pauses** – UI friction, hesitation, or intent re-alignment
- 🔄 **Reentries** – Resumption of prior user intents
- 🌀 *Drifts* – _(Planned feature; not yet implemented in this demo)_

---

## 🗂 File Structure

| Path                          | Description                            |
|-------------------------------|----------------------------------------|
| `input_trace.txt`            | Sample conversation log (User/Bot)     |
| `generate_trace.py`          | Main processing script                 |
| `outputs/`                   | Generated output files                 |
| ├─ `pld_trace.md`            | Markdown + Mermaid visualization       |
| └─ `pld_trace.json`          | Structured analysis result (JSON)      |
| `utils/`                     | Supporting analyzers                   |
| ├─ `pause_classifier.py`     | Rule-based pause detection             |
| └─ `reentry_detector.py`     | Reentry detection via intent match     |

---

## 🚀 Quick Start

### 1. Prepare Input

Edit `input_trace.txt` with a conversational flow:

```text
[User] How do I export the invoice as PDF?
[Bot] You can select it from the "Document Export" menu.
[User] Wait, I can't find the export option.
[User] Never mind, I'll just export first.
```

### 2. Run Analysis
```bash
python generate_trace.py
```
### 3. View Results

- 📄 Human-readable → `outputs/pld_trace.md`
- 🧩 Machine-readable → `outputs/pld_trace.json`

---

## 🔬 Sample Output (Excerpt)

**Markdown: `pld_trace.md`**

```mermaid
graph TD
    U0["How do I export the invoice as PDF?"]
    U1["Wait, I can't find the export option"]
    style U1 stroke:#f00,stroke-width:2px
    U2["Never mind, I'll just export first"]
    style U2 stroke:#f00,stroke-width:2px
```

**Tags:**

- [User] Wait, I can't find the export option  
  - ⏸️ UI Friction  
  - 💬 User cannot find UI element

- [User] Never mind, I'll just export first  
  - ⏸️ Repair Pause  
  - 🔄 Reentry to: "How do I export the invoice as PDF?"

---

## 🎯 Design Goals

| Feature              | Status                     |
|----------------------|----------------------------|
| Pause Detection      | ✅ Heuristic + GPT-ready    |
| Reentry Analysis     | ✅ Intent matching across turns |
| Visualization        | ✅ Mermaid.js + Markdown     |
| Latency Tracking     | 🔜 Future integration        |
| Drift Detection      | 🔜 Under development         |

---

## ⚠️ Known Limitations

- 🌀 **Drift classification** is not yet implemented in this version.
- Time-based latency detection is not included (pause classification is heuristic-only).
- Mermaid visual IDs may overlap with long logs (currently simple U0/U1 indexing).

---

## 📚 Related Resources

- 🧠 **PLD Framework Documentation** — [structure_generators/](https://github.com/kiyoshisasano-DeepZenSpace/tree/e6278c2a9eb82006fd2aa68326829adafd942d9c/14_PLD-Bridge-Hub/structure_generators)  
- ⏱️ **Latency Tracker** — [`latency_tracker.py`](https://github.com/kiyoshisasano-DeepZenSpace/blob/e6278c2a9eb82006fd2aa68326829adafd942d9c/14_PLD-Bridge-Hub/structure_generators/latency_tracker.py)  
- 🔁 **Reentry Detector** — [`reentry_detector.py`](https://github.com/kiyoshisasano-DeepZenSpace/blob/e6278c2a9eb82006fd2aa68326829adafd942d9c/14_PLD-Bridge-Hub/structure_generators/reentry_detector.py)

---

> 💡 Note: This is a **demonstration tool** for analyzing UX dialogue rhythm, intended for prototyping and exploration.
> For production-grade integration, refer to the full **PLD-Bridge-Hub** suite and latency-aware structural modules.

---
## 📜 License & Use Conditions

**License:** Creative Commons BY-NC 4.0  
Non-commercial use permitted with attribution:  
→ _"Phase Loop Dynamics — Kiyoshi Sasano / DeepZenSpace"_

