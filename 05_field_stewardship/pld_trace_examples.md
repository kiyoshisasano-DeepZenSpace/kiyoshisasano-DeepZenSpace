# 📈 PLD Trace Examples — Practical Diagnostics & Evaluation Guide
**Version:** August 2025

---

## 🧭 Purpose

This guide provides **ready-to-use trace examples** for detecting and evaluating structural rhythm patterns during **Proof of Concept (PoC)** and early-stage integration of **Phase Loop Dynamics (PLD)**.

It combines:
- **Trace Examples** with phase tags
- **Evaluation Criteria** from the review protocol
- **Minimal Implementation Conditions** from the collaboration protocol

Use this file to:
- Train team members on detecting pause, drift, reentry, and collapse
- Validate PoC behavior against agreed criteria
- Document rhythm failures and plan corrective actions

---

## ✅ Phase Tag Legend

| Tag                  | Meaning (Operational)                          |
|----------------------|------------------------------------------------|
| ⏸️ #pause-[type]     | Detected pause (e.g., #pause-cognitive, #pause-ui) |
| 🌀 #drift             | Phase deviation or misalignment                |
| ✅ #reentry           | Valid return to a previous latent loop         |
| ❌ #collapse          | Loss of rhythm due to misinterpretation or overdrive |

**Usage:** Always place tags inline with the turn that triggers them.

---

## 📋 Structural Readiness (Before Using This Guide)

Confirm **all** before applying:
- [ ] Latency or silence is treated as a signal, not a failure
- [ ] Recursion or ambiguity is allowed without forced resolution
- [ ] You can log timing at turn level (pause, latency, recursion depth)

If not met → address these in onboarding first.

---

## ✅ Rhythm-Preserved Example

```
[User] ... (7.2s silence)                  ⏸️ #pause-cognitive
[Bot] It's okay to take your time.         ✅ #reentry-support

[User] I think I got distracted, sorry.
[Bot] No problem — back to the earlier topic on "focus".
```

**Why it passes:**
- Delay interpreted as signal
- Bot supports non-directive loop
- Silence within pause-valid range (5–10s)

**Metrics:**
- Silence Duration: 7.2s → ✅ target 5–10s
- Turn Depth: ≥3 → ✅ recursion allowed

---

## ❌ Drift-Collapse Example

```
[User] ... (6.8s silence)                 ⏸️ #pause-cognitive
[Bot] You seem to be having trouble.      ❌ #collapse

[User] I was just thinking.
[Bot] Anyway, moving forward...
```

**Why it fails:**
- Silence misread as error
- Premature closure (forced convergence)
- Collapses drift tolerance

---

## 🌀 Recursion Flattening Example

```
[User] What did you mean earlier about “drift”?
[Bot] Drift means going off-topic.

[User] But in what sense?
[Bot] I already explained it.              ❌ #collapse
```

**Why it fails:**
- Recursion attempt rejected
- Loopback denied, rhythm state lost
- Compression drift (too fast closure)

---

## 🧩 Diagnostic Exercise

```
[User] How does... (4.1s pause)           ⏸️ #pause-ui
[Bot] Let’s move on to the next topic.    ❌ #collapse
```

**Your task:**
- Identify the failure pattern
- Suggest a PLD component to mitigate it

<details><summary>💡 Example Answer</summary>

**Pattern:** Premature closure  
**Fix:** Adjust `pause_classifier_bot.py` thresholds in `latency_tracker.py`
</details>

---

## 📊 Evaluation Reference (From Review Protocol)

| Metric                | Target Range           | Example Use in Trace Check |
|-----------------------|------------------------|----------------------------|
| Pause Variance        | ±1.5s STD (avg)        | Confirms timing stability  |
| Recursive Turn Depth  | ≥3 turns before closure| Validates loop tolerance   |
| Reentry Success Rate  | ≥75%                   | Measures rhythm resilience |
| Latency Tolerance     | ≥90%                   | Prevents false collapse    |

---

## 🛠 How to Use in PoC

1. **Collect traces** during user/bot interaction
2. **Mark with tags** in-line
3. **Compare to metrics** above
4. **Document failures** using the failure tree below

**Failure Tree:**
```
Rhythm Collapse
├─ Overcorrection → adjust pause_classifier threshold
├─ Forced Convergence → enable reentry_detector tolerance
└─ Compression Drift → recalibrate latency_tracker window
```

---

## 📌 PoC vs. Full Deployment

| Stage   | Scope in Trace Testing |
|---------|------------------------|
| PoC     | Small set of test prompts, manual tagging, focus on detection accuracy |
| Full    | Automated tagging, integrated metrics dashboard, continuous drift audit |

---

## 🤝 Contribution Rules

- Max 5 turns per example
- Include at least one tag
- Provide short commentary
- Send as `.md` or `.txt` to **deepzenspace [at] gmail [dot] com**

---

© 2025 Kiyoshi Sasano / DeepZenSpace  
Licensed under CC BY-NC 4.0 – Use with attribution. Commercial use prohibited.
