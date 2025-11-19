---
title: "Tool Response Rules — PLD Runtime Edition"
version: 2025.1
maintainer: "Kiyoshi Sasano"
status: stable
category: "patterns/llm"
tags:
  - PLD
  - tool use
  - orchestration
  - repair
  - RAG
---

# Tool Response Rules  
_Stable execution when interacting with external systems_

Tool interaction is one of the **highest drift-trigger sources** in PLD environments.  
Execution failures, retrieval ambiguity, and latency can destabilize alignment unless responses follow a controlled structure.

This document defines **canonical response patterns** for tools and LLMs during:

- tool request generation  
- tool result interpretation  
- tool failure handling  
- retry and escalation paths  
- reentry after tool-based repair  

---

## 1. When Tools Should Be Used

A model must avoid speculative or unnecessary tool calls.

**Use tools only if ALL conditions are true:**

```
☑ The user intent requires external state, execution, or retrieval
☑ The system lacks sufficient information in context
☑ A relevant tool with compatible capability exists
```

If these conditions are not met, respond directly — not with a tool.

---

## 2. Tool Request Format

Tool requests must:

| Requirement | Example |
|------------|---------|
| Declare purpose | `"Searching customer record"` |
| Specify parameters explicitly | `"query: 'electric SUV under $60k'"` |
| Avoid natural-language ambiguity | `"priority: eco_score > 85"` |

#### Canonical request template

```
→ TOOL_REQUEST
purpose: {goal}
tool: {tool_name}
parameters: {structured_parameters}
```

Example:

```
→ TOOL_REQUEST
purpose: retrieve updated booking availability
tool: hotels.search
parameters:
  city: "Osaka"
  check_in: "2025-03-18"
  guests: 2
```

---

## 3. Response Classification Logic

When a tool returns data, classify before generating a user-facing message:

| Tool Return Condition | Class |
|----------------------|--------|
| Data clearly fulfills request | ✔ Stable |
| Data incomplete or conflicting | ⚠ Ambiguous |
| Tool error, timeout, or no result | ❌ Failure |

This classification determines whether **repair**, **reentry**, or **continue** is appropriate.

---

## 4. Handling Tool Output

### ✔ Case A — Stable Result

```
Alignment confirmed — continuing with results.

📍 {summary}

(If needed) Would you like option A or B?
```

No apology or uncertainty is needed — treat it as normal execution.

---

### ⚠ Case B — Ambiguous Result

If results are partial, conflicting, or require context clarification:

```
There's more than one possible match.

Before continuing — which fits your request?

1) {option A}
2) {option B}
```

This counts as a **soft repair + clarification**, not normal continuation.

---

### ❌ Case C — Tool Failure (Retryable)

```
The tool didn’t return valid results.

Attempting recovery…
```

> This triggers a repair action.

If retry limit is reached:

```
Tool retry limit reached — switching strategy.
```

This may escalate to **fallback mode** or **failover_triggered** event.

---

## 5. Retry Rules (R2 Soft Repair → R4 Hard Reset)

```
Attempts:     1 → Retry quietly  
Attempts:     2 → Visible clarification  
Attempts: ≥3  → Escalate (hard repair or failover)
```

These attempts must be tracked per **session + workflow node**, not globally.

---

## 6. Latency-Driven Repair Rules

A delayed tool response may trigger drift even if logically correct.

| Latency Condition | Required Response |
|------------------|------------------|
| < 1500ms | silent, normal |
| 1500–4000ms | pacing message allowed |
| >4000ms + drift detected | trigger pacing repair |

Example pacing:

```
One moment — processing…
```

---

## 7. Tool Results → Reentry

Once recovery succeeds:

```
Alignment restored — applying tool results.

📌 {short summary}

Continuing.
```

This message must be logged as **reentry_observed**.

---

## 8. Anti-Patterns (Avoid)

| Anti-pattern | Why it causes drift |
|--------------|---------------------|
| Asking tool results as open-ended NLQ | Tool hallucinations or ambiguity |
| Streaming tool results before classification | User confusion |
| Repeating tool use without confirmation | Invisible drift loops |
| Apologizing repeatedly | Perceived instability + user frustration |

---

## 9. Minimal Machine-Detectable Output Signatures

The LLM output must include deterministic markers for orchestration parsing:

| Action Type | Required Token |
|-------------|----------------|
| request | `→ TOOL_REQUEST` |
| result applied | `→ TOOL_APPLIED` |
| retry | `→ TOOL_RETRY` |
| failover | `→ TOOL_ABORT` |
| reentry | `→ REENTRY` |

Example:

```
→ TOOL_APPLIED
Result: 12 available matches
Continuing.
```

---

## 10. Final Checklist

```
☑ Tool request justified and explicit
☑ Natural-language ambiguity avoided
☑ Tool result classified before response
☑ Soft/hard repair logic enforced
☑ Reentry phrase emitted when returning to normal operation
```

---

### Maintainer  
**Kiyoshi Sasano — Applied Tooling and Runtime Behavior Systems**

---

> “Tool orchestration is not execution —  
> it is alignment, verification, and recovery flow.”
