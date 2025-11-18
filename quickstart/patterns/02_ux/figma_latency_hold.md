# Figma Pattern — Latency-Hold Interaction  
*Applied-AI Agent UX Pattern (PLD Aligned)*

**Audience:** Product designers, UX engineers, and agent developers.  
**Purpose:** Prevent mistrust or abandonment during backend latency, tool execution, or multi-step reasoning.  
This pattern ensures the user perceives **progress**, not **failure**.

---

## 01 — When to Use This Pattern

Trigger latency-hold when:

- Tool call exceeds **600–900ms**
- Multi-step reasoning (ReAct / retrieval / planning) is active
- A retry or Soft Repair path is executing
- The UI cannot confirm success immediately

⚠ The goal is **not to hide slowness** — but to communicate system state honestly.

---

## 02 — Core Interaction Model

Latency-hold follows a **3-stage loop aligned with PLD lifecycle behavior**:

| Stage | Timing | System Behavior | Intent |
|-------|--------|----------------|--------|
| **Hold** | 0–1.2s | Micro-status animation | Prevent perceived freeze |
| **Reveal** | 1.2–3.5s | Inform user of processing | Set expectations |
| **Confirm/Repair** | ≥3.5s | Deliver output or request confirmation | Maintain alignment |

This stabilizes pacing even when backend runtime varies.

---

## 03 — Required UI Elements

A latency-safe interaction includes:

- **State Indicator** (visual transition into processing)
- **Progress Signal** (animation or short phrase)
- **Expectation Line** (why delay exists)
- **Fallback Action Slot** (user agency if delay persists)
- **Silence Guard** (prevents blank or static screen)

---

## 04 — Recommended Microcopy

| Context | Example Copy |
|--------|--------------|
| Initial delay (<1s) | _“Working on that…”_ |
| Tool / retrieval process | _“Checking available options…”_ |
| Uncertain latency | _“Still processing — this step takes a moment.”_ |
| Repair attempt | _“Let me verify and adjust.”_ |
| Awaiting confirmation | _“Almost done — just verifying.”_ |

Tone rules:

- Neutral → confident → concise  
- Avoid apology stacking  
- Avoid filler phrases without informational value  

---

## 05 — PLD-Aware Variants

| Condition | UI Copy Variant |
|-----------|----------------|
| Drift-Information detected | _“Checking alternative results…”_ |
| Drift-Instruction detected | _“Before continuing — did you mean A or B?”_ |
| Soft Repair in progress | _“Updating based on your last input…”_ |
| Hard Repair triggered | _“Restarting the workflow cleanly…”_ |

This ensures the UI reflects internal agent state.

---

## 06 — Figma Layout Recipe

```
[ Animation / Icon ]
[ Primary Status Text ]
[ Optional Sub-Status ]
[ Optional Button / Fallback ]
[ Invisible Timeout Logic ]
```

**Spacing guidelines:**
- Primary text: 16–18px  
- Secondary: 12–14px  
- Padding: ≥24px  

**Motion guidance:**
- Avoid infinite spinner loops  
- Prefer pulsing gradients or low-intensity motions  
- Never imply progress that isn’t real  

---

## 07 — Example Variants

### 🔹 Standard Reasoning Delay

```
🤖 Thinking...
This may take a few seconds.
```

### 🔹 Tool Execution with Context Awareness

```
🔍 Searching available hotels...
You can continue typing — I won’t lose context.
```

### 🔹 Latency + Soft Repair Interaction

```
⚠ Reviewing response...
There may have been conflicting constraints.
```

---

## 08 — Engineering Integration Notes

Latency-hold performs best when tied to:

- Tool execution futures/promises  
- LangGraph node state transitions  
- Drift classifier events  
- Telemetry logs (OpenTelemetry / Posthog / Mixpanel)

Suggested API pattern:

```ts
ui.updateLatencyState({
  phase: "HOLD",
  source: "tool_call",
  expected_ms: 2100,
  can_interact: true
});
```

---

## 09 — Anti-Patterns (Avoid)

| Anti-Pattern | Failure Result |
|--------------|----------------|
| ❌ Silent wait | User assumes crash |
| ❌ Pure spinner, no text | Cognitive uncertainty |
| ❌ Fake progress bar | Trust erosion |
| ❌ UI freeze until completion | Perceived instability |
| ❌ Immediate reset after error | Lost context + drift recurrence |

---

## 10 — Success Criteria

Latency-hold is successful when:

- User **does not repeat the command**
- **Abandonment rate decreases**
- Reentry after repair feels natural
- Memory continuity is preserved across delays
- Drift frequency remains stable or decreases

---

### Attribution

Maintainer: **Kiyoshi Sasano**  
File: `patterns/02_ux/figma_latency_hold.md`  

License: **CC BY 4.0**
