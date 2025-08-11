# 🚀 PLD Onboarding & Diagnostics Guide
**Version:** August 2025

---

## 📌 Purpose
This guide covers the **pre-deployment preparation** and **initial diagnostics** for teams starting a Proof-of-Concept (PoC) with **Phase Loop Dynamics (PLD)** modules.

It ensures:
- Your system meets the basic requirements for PLD
- You can perform a minimal setup and run an initial rhythm diagnostic
- You know the next steps toward production deployment

---

## 1️⃣ Pre-Deployment Checklist

Proceed only if you can confirm all items below:

- [ ] Latency, silence, or pause can be **interpreted as a signal**, not treated as error  
- [ ] Ambiguity or recursion can persist without forced resolution  
- [ ] Output timing is **not always** directly linked to input timing  
- [ ] No stylistic or branding “fake delays” are in place  
- [ ] You have reviewed [`pld_structural_scope_and_conditions.md`](./pld_structural_scope_and_conditions.md) for applicability  
- [ ] You are aware of prohibited uses:
  - HR evaluation, productivity tracking, or employee monitoring
  - Systems with no structural meaning in timing
  - Simulated delays without measurement intent

If any item above is **No**, stop here — PLD is likely not suitable.

---

## 2️⃣ Onboarding Sequence

1. **Initial Contact** – Confirm project scope and technical context via email or shared doc.  
2. **Charter Review** – Read [`pld_field_stewardship_charter.md`](./pld_field_stewardship_charter.md) for collaboration values and responsibilities.  
3. **Environment Prep** – Ensure system can log timing events and accept PLD modules.  
4. **Module Selection** – Start with minimal PoC modules (see next section).  
5. **Initial Diagnostics** – Run provided trace examples and validate event tagging.

---

## 3️⃣ PoC Minimal Setup

**Recommended starting modules:**
1. `latency_tracker.py` – Detect and log structured delays  
2. `pause_classifier_bot.py` – Classify pauses by type (cognitive, UI, disengagement)  
3. (optional) `reentry_detector.py` – Track reentry into prior intents after a gap  

**Quick setup:**
```python
from pld_tools import enable_pld

enable_pld(modules=[
    'latency_tracker',
    'pause_classifier_bot',
    'reentry_detector'
])
```
You may omit unused modules.  
Begin with `latency_tracker` for a lightweight start.

---

## 4️⃣ Initial Diagnostics

### Phase Tag Legend
| Tag                | Meaning |
|--------------------|---------|
| ⏸️ `#pause-[type]` | Detected pause (e.g. `#pause-cognitive`) |
| 🌀 `#drift`         | Timing irregularity / phase deviation |
| ✅ `#reentry`       | Valid reentry to prior latent state |
| ❌ `#collapse`      | Rhythm breakdown |

### Example — Rhythm Preserved
```pld-trace
[User] ... (7.2s silence)         ⏸️ #pause-cognitive  
[Bot] It's okay to take your time. ✅ #reentry-support
```
✅ Delay interpreted as signal, not error.

### Example — Rhythm Collapse
```pld-trace
[User] ... (6.8s silence)        ⏸️ #pause-cognitive  
[Bot] You seem to be having trouble. ❌ #collapse
```
❌ Silence misinterpreted, causing premature closure.

---

## 5️⃣ Quick Diagnostic Procedure
1. Run at least 3 test traces from [`pld_trace_examples.md`](./pld_trace_examples.md) in your system.  
2. Confirm tags match expected classifications.  
3. Review results against the **Drift Warning Signs**:
   - Pause inflation without phase meaning
   - Loop evasion (recursion denied)
   - Reentry suppression
   - Forced resolution

If ≥75% of test cases produce correct tags, you can proceed to extended PoC scenarios.

---

## 6️⃣ Next Steps Toward Production
After PoC validation:
- Apply [`pld_latency_calibration_protocols.md`](./pld_latency_calibration_protocols.md) to tune for your UX context.  
- Set up ongoing monitoring with [`pld_internal_review_protocol.md`](./pld_internal_review_protocol.md).  
- Formalize collaboration scope and responsibilities via [`pld_collaboration_terms.md`](./pld_collaboration_terms.md).

---

## 📬 Contact
For setup questions or diagnostic review:  
📧 **deepzenspace [at] gmail [dot] com**

---

© 2025 Kiyoshi Sasano / DeepZenSpace  
Licensed under CC BY-NC 4.0 – Use with attribution. Commercial use prohibited.
