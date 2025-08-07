# ⏱️ Latency Tracker — UI Pause Logger for PLD

This module detects and logs user interaction pauses in web UIs  
as defined by **Phase Loop Dynamics (PLD)** — specifically as indicators of:

- ⏸️ Cognitive delay  
- ⏸️ UI friction  
- ⏸️ Intent suppression or micro-hesitation  

Used to support pattern-aware UX design and rhythm-resonant system feedback.

---

## 🛠️ Configuration

- `PAUSE_THRESHOLD_MS`: Default `800` milliseconds

> **Rationale**:
> - PLD Paper 1, Fig.3 — Cognitive drift begins after ~750ms  
> - Modified Fitts' Law for UI delay friction  
> - Practical UX thresholds for latency awareness  

You can modify this value in `latency_tracker.py` to suit your interaction environment.

---

## ⚙️ How It Works

```text
[User Action A]
↓ (pause of 1.2s)
[User Action B]
→ Logged as: PauseEvent(type="⏸️ Latency Hold", duration=1.2s, timestamp=...)
```
The script compares timestamps between interactions.
If the pause exceeds PAUSE_THRESHOLD_MS, it logs the pause event to CSV.

---

## 🚀 Quick Example

```bash
python latency_tracker.py
```
Then perform sample UI inputs (or simulate).
Output will be saved to: latency_log.csv

# Sample log:
```bash
timestamp,pause_duration_ms,label
2025-08-07 14:22:05,1250,⏸️ Cognitive
```
---

## 🧠 Notes on Interpretation

**Pause ≠ Failure** — in PLD, pauses are structural rhythm markers.  

They indicate **intent latency**, **micro-transition**, or **repair opportunity**,  
and may lead to loop realignment (see `reentry_detector.py` for next stage).

---

### 🔭 Extended Sensing (Planned)

Future versions may support:

| Modality           | PLD Mapping       | Example              |
|--------------------|------------------|----------------------|
| 👁️ Eye tracking     | ⏸️ Cognitive       | Gaze fixed, no input |
| 🖱️ Scroll Stalling  | ⏸️ UI Friction     | Scroll → stop        |
| 📱 Touch idle gap   | ⏸️ Latency Hold    | Mobile finger hover  |

---

## 🤝 Contributing

**Theoretical Consistency Checklist**:

- [ ] Does your change correspond to a PLD concept (Drift / Pause / Repair)?  
- [ ] Cite the related section in [`zenodo_paper_links.md`](../docs/zenodo_paper_links.md)  
- [ ] If you introduce new thresholds or labels, document the rationale.

---

## 📚 References

- 🧠 [`docs/zenodo_paper_links.md`](../docs/zenodo_paper_links.md)  
- 🔄 [`structure_generators/README_structure_generators.md`](../structure_generators/README_structure_generators.md)  
- 💬 [`pause_classifier_bot.py`](./pause_classifier_bot.py)  
- 🔁 [`reentry_detector.py`](./reentry_detector.py)

---

## 📜 License

This project is licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).  
See [`LICENSE`](../LICENSE) for full details.
