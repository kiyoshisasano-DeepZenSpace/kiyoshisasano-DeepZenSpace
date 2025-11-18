# 03 — Hard Repair  
*Operator Primitive (Canonical Code Edition — 2025)*  

> **Purpose:** Restore stability when system state becomes structurally corrupted — beyond what Soft Repair (R1–R2) can safely resolve.  
> Hard Repair is a **controlled reset**, not a failure. It prevents error propagation and restores reliable execution.

---

## **1 — When Hard Repair Is Required**

Hard Repair should only occur when **continuing the current task risks compounding error**.

| Trigger Code | Condition | Example |
|--------------|-----------|---------|
| **D1_instruction (repeated)** | System repeatedly misinterprets original objective | Wrong task despite clarifications |
| **D2_context (critical)** | Memory contradiction or corrupted constraint state | User constraints overwritten |
| **D3_flow** | Agent trapped in procedural/tool loop | Retry loops, broken step order |
| **D5_information (persistent)** | Facts remain incorrect despite correction | Conflicting factual state |

Operational Target: **Hard Repair < 12–15% of total repair events**  
If higher → Soft Repair detection or drift classification requires review.

---

## **2 — PLD Taxonomy Alignment (Updated)**

Hard Repair corresponds to a **single canonical code**:

| Allowed Hard Repair Code | Meaning | Notes |
|--------------------------|---------|-------|
| **R5_hard_reset** | Reset corrupted state and re-establish shared reality | 🚨 replaces all legacy categories (Repair-Reset, Repair-Recontextualize, Repair-Restart, Repair-ContextDrop) |

> ⛔ Legacy labels are deprecated.  
> Hard Repair must use the single canonical code: **R5_hard_reset**.

---

## **3 — Canonical Hard Repair Sequence**

Hard Repair follows a **four-step protocol**:


---

Maintainer: **Kiyoshi Sasano**  
Edition: **PLD Applied 2025**  
License: **CC-BY 4.0**
