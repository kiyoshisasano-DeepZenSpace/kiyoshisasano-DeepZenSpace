# 🕒 figma_latency_hold.md  
**Simulating "Latency Hold" in Figma Prototypes**

_Last updated: 2025-07-31_

---

## 🎯 What Is Latency Hold?

**Latency Hold** is a deliberate pause inserted into a user flow. It is not technical lag — it is a **designed rhythm buffer** that helps:

- Mirror user hesitation  
- Build anticipation or intentional delay  
- Avoid abrupt transitions  
- Establish flow pacing and trust  

Used properly, it transforms perceived waiting into **intentional, tempo-aware UX**.

---

## 🧪 How to Prototype in Figma

Figma supports latency simulation using:

- **After Delay** triggers  
- **Overlay frames**  
- **Smart Animate** with shimmer or pulse  
- **Component Variants** with timing options

---

### 📘 Use Case 1: “Wait Before Prompt”

**Scenario:**  
User submits a form → brief hold → soft confirmation appears

**Steps:**

1. Create 3 frames:  
   - `Form_Submitted`  
   - `Latency_Buffer` (blank or shimmer animation)  
   - `Confirmation_Message`  

2. In Prototype tab:  
   - `Form_Submitted` → `Latency_Buffer`  
     - After Delay: `0ms`  
     - Navigate To: `Latency_Buffer`  

   - `Latency_Buffer` → `Confirmation_Message`  
     - After Delay: `1200ms`  
     - Smart Animate (optional)

**Optional Enhancements:**  
- Add subtle animated dot or pulse to `Latency_Buffer`  
- Use micro-feedback (e.g. “Just a sec…”) to align timing expectations

---

### 📘 Use Case 2: “Soft Prompt Timing”

**Scenario:**  
User hesitates → after 1000ms → assistive tooltip fades in

**Steps:**

1. Create base frame + overlay:  
   - Main UI  
   - `Tooltip_Prompt` (semi-transparent, hint-style)

2. Connect using:  
   - Trigger: `After Delay`  
   - Delay: `1000ms`  
   - Action: Show overlay (position: bottom-center)  
   - Opacity: ~50%  
   - Animation: Fade-in

---

## 🎨 Design Tips

| Situation             | Recommended Timing | Visual Feedback     |
|-----------------------|--------------------|----------------------|
| Onboarding Step       | 1200–1500ms        | Dots, shimmer, delay |
| Error Clarification   | 800–1000ms         | Fade-in hint         |
| Power User Flow       | ≤800ms             | Quick fade or none   |

- Use animation, not jump cuts  
- LatencyHold is most effective when it **feels intentional**, not idle  
- Match feedback tempo to user type or task complexity

---

## 🔁 Example Pattern: Latency Loop

```plaintext
Frame: SubmitAction
  → Frame: LatencyHold (1200ms delay)
  → Frame: SoftConfirmation ("Thanks! Ready for next step?")
```
Design Note:Users perceive **“rhythm”** in how feedback arrives.  
A slight pause before response can **increase clarity and trust**.

---

## 🔄 Multi-Pattern Integration

`Latency Hold` often works best in combination with other PLD primitives:

```plaintext
Drift (user hesitates)
  → LatencyHold (pause with shimmer)
    → SoftRepair (clarification tooltip)
      → Reentry (user resumes flow)
```
This layered design models hesitation → nudge → resumption without forcing.
## ⚠️ Edge Case Handling: Interrupts During Latency Hold

If a user clicks **"Back"** or navigates away during a `Latency Hold`:

- 🛑 Cancel or bypass the delayed step  
- ✅ Ensure navigation isn’t blocked or visually frozen  
- 🔁 Use conditional logic (e.g., *Prototype → Interaction → Bypass overlay on click*)

---

## 🧩 Build as Reusable Component

To increase flexibility, create a component named:  
**`LatencyHold_Frame`**

| Variant         | Value                              |
|-----------------|------------------------------------|
| **Delay Duration** | 800ms / 1200ms / 1500ms             |
| **Style**          | Dots / Shimmer / Blank              |
| **Overlay**        | Tooltip / Loading Icon / None      |

This enables:

- ♻️ Reuse of timing behaviors across flows  
- 🧪 A/B testing of pacing for **power users vs. new users**

---

## 🔗 Related PLD Patterns

- **`soft_repair`**: Friendly clarification if hesitation continues  
- **`resonance_echo`**: Repeat pacing structure to maintain rhythm  
- **`reentry_link`**: Resume interaction after dropout with context memory

---

## 📈 Design Ops Note

To test or calibrate latency:

- Use **Figma’s Prototype Testing** to A/B delay durations  
- Start with **longer delays (~1200ms)** for onboarding  
- Shorten for **returning/expert users (≤800ms)**  
- Gather feedback on **perceived responsiveness vs. trust**

---

## 📌 Why It Matters

- Prevents **abrupt transitions** that confuse or overwhelm  
- Supports **phased UX** where pacing = user comprehension  
- Reinforces PLD’s **rhythm-first design mindset**

> “Don’t just show the next step — give space for it.”
