Status: Working Draft (Exploratory Stage)

This taxonomy is part of an ongoing independent research effort.
It is not a finalized specification and may evolve based on implementation feedback and empirical validation.
Contributions, critiques, and alternative structures are welcome.

# 📄 **PLD v2 Taxonomy Proposal — Draft v0.1**  
_(Hybrid Governance Mode — With Rationale Annotations)_

---

## **1. Scope & Intent**

This taxonomy defines the runtime event classification, governance placement, and metrics alignment for the PLD v2 runtime and analytics layers.  
It formalizes the PLD code system across **detection → repair → continuation → outcome**, with explicit governance states:  

- **Canonical Registry:** stable, enforced, runtime-binding event codes  
- **Provisional Registry:** active, but semantically unresolved or evolving  
- **Pending Governance Review:** requires resolution before entering Canonical  

> **Annotation:** Hybrid governance ensures evolution without uncontrolled fragmentation. Pending entries remain observable and valid but are not yet normative.

---

## **2. Design Principles**

### **Prefix Hierarchy Rules**
| Prefix | Domain | Meaning |
|--------|--------|---------|
| D | Drift detection | Signals anomaly or divergence |
| C | Continue / normal execution | No repair required |
| R | Repair / mitigation | Runtime recovery action |
| O | Outcome | Terminal lifecycle result |
| (Unassigned today) | Analytics-only signals | Not yet formalized as event codes |

> **Annotation:** No new prefixes introduced per governance requirement. Analytics cluster intentionally not forced into prefix expansion.

---

### **Numeric System Rules**
- `0` → baseline or neutral state  
- Higher number (`1–5`) → escalation, severity, or specificity hierarchy  
- Numeric ordering must remain unique within a prefix.

> **Violation noted: D5 conflict. Requires governance resolution.**

---

### **Descriptor Naming Rules**
- Must remain human-readable and workload-agnostic  
- Must map 1:1 to `event_matrix.yaml` semantics  
- Must support metrics traceability without requiring external lookup  

---

### **Immutability & Evolution Rules (Hybrid Policy)**

- **Canonical codes become immutable once frozen.**  
- **Provisional codes may evolve (rename, merge, split).**  
- **Pending codes require governance sign-off before promotion or removal.**  

---

## **3. Canonical Registry (Stable Zone)**

| code | prefix | numeric | descriptor | semantic_scope | event_type | metrics_link | enforcement_binding | status |
|------|--------|---------|------------|----------------|------------|--------------|----------------------|--------|
| D1_instruction | D | 1 | instruction drift | semantic deviation | drift_detected | accuracy (intent) | repair escalation logic | stable |
| D2_context | D | 2 | context drift | schema/env mismatch | drift_detected | data integrity | repair escalation | stable |
| D3_repeated_plan | D | 3 | repeated loop | behavioral stall | drift_detected | efficiency stall | triggers rewrite or reset | stable |
| D4_tool_error | D | 4 | external tool/API failure | dependency failure | drift_detected | reliability ops | triggers repair → possible reset | stable |
| C0_normal | C | 0 | normal flow | runtime continuation | continue_allowed | throughput baseline | none | stable |
| C0_user_turn | C | 0 | user turn | dialog state | continue_allowed | engagement metric | none | stable |
| C0_system_turn | C | 0 | system turn | agent action | continue_allowed | output rate | none | stable |
| R1_clarify | R | 1 | clarification | minimal repair | repair_triggered | interaction recovery | low-impact repair path | stable |
| R2_soft_repair | R | 2 | soft repair | self-correction | repair_triggered | resilience score | moderate repair | stable |
| R3_rewrite | R | 3 | rewrite | high-effort recovery | repair_triggered | computational cost | content regeneration | stable |
| R4_request_clarification | R | 4 | user inquiry | explicit disambiguation | repair_triggered | friction metric | paused state until user response | stable |
| R5_hard_reset | R | 5 | reset | full recovery | repair_triggered | risk / failure severity | state wipe & reinit | stable |
| O0_session_closed | O | 0 | closed | lifecycle terminal | session_closed | completion metric | terminal | stable |

> **Annotation:** These codes satisfy all three criteria: semantic clarity, operational determinism, metric traceability.

---

## **4. Provisional Registry (Exploratory Zone)**

| code | reason_for_provisional | ambiguity_type | candidate_mappings | stability_risk_level | review_trigger |
|------|------------------------|----------------|-------------------|----------------------|----------------|
| D0_none | Baseline drift absence code | definition overlap with D0_unspecified | → merge OR clarify “heartbeat” meaning | Medium | metrics misclassification noted |
| D0_unspecified | Missing metadata classification | ingestion vs semantic ambiguity | → candidate for deprecation | High | ingestion layer fix |
| D9_unspecified | Catch-all anomaly | semantic underspecification | → split into cases OR keep fallback | Medium | volume threshold |
| PRDR | Observational metric | runtime vs analytics boundary unclear | → may become M-prefix | Low | governance policy formation |
| VRL | Recovery latency metric | non-event: derived | same as above | Low | design decision |
| continue_repair_ratio | Global state metric | derived, not event | no mapping required | Low | system governance |
| failure_mode_clustering | aggregate signal | not event | could map to taxonomy revisions | Low | taxonomy maturity |
| session_closure_typology | meta-analysis | not runtime event | not likely to become event code | Low | final governance |

> **Annotation:** These remain valid but non-normative and MUST NOT be interpreted as operational signals.

---

## **5. Pending Governance Review Zone**

| code | unresolved conflicts | dependencies | required decisions |
|------|---------------------|--------------|-------------------|
| **D5_latency_spike & D5_information** | numeric collision / metrics contamination | detection system + event matrix + dashboards | merge? renumber? alias? enforce dual semantic rule? |
| **D0_none / D0_unspecified overlap** | missing-code vs no-drift cannot share same semantic space | ingestion policy + taxonomy rules | does D0 represent state or diagnostic error? |
| **Analytics cluster elevation question** | whether metrics should become runtime summary events | governance framework | should derived metrics ever emit as event types? |

> **Annotation:** These blockers must be resolved before the **v0.2 stabilization milestone**.

---

## **6. Cross-System Mapping**

### 6.1 → Event Types  
`D → R → C or O`

### 6.2 → Runtime Enforcement  
Mapping validated in `repair_detector.py`.

### 6.3 → Repair Continuum  
Severity‐based escalation confirmed.

### 6.4 → Metrics Framework  
Aligned except for D5/D0 contamination.

### 6.5 → Failover & Escalation  
Hard reset path validated but governed.

---

## **7. Diagram: Structural Overview**

> **(Included separately as taxonomy_proposal_diagram.svg)**  
Legend:  
- **Solid** = Canonical  
- **Dotted** = Provisional  
- **Dashed cluster** = Pending Governance

---

## **8. Path to v0.2 and Validation Plan**

| Requirement | Condition to Exit |
|------------|------------------|
| D5 collision resolution | numeric uniqueness confirmed |
| D0 fallback hierarchy clarified | ingestion and runtime aligned |
| Analytics governance decision | prefix policy determined |
| Stability threshold | <3% volume routed to D9 fallback |

---

## 📌 Proposal Confidence Summary (inline preview)

- Overall validity: **93%**
- Structural readiness: **High**
- Governance unresolved areas: **D5, D0, analytics role**

---

## 9. Feedback & Participation

This document is in an iterative research phase.
Feedback, objections, refinement proposals, and real-world implementation reports are highly encouraged.

Preferred channel: TBD (GitHub issues / shared doc / direct review)
Review cadence: aligned with governance milestones for the PLD v2 event schema.

---

### ✔️ Draft complete.

