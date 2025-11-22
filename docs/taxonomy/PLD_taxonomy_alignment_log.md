# PLD Taxonomy Alignment Log

**Status:** Working Draft — Exploratory Alignment Record
**Audience:** Contributors, reviewers, and implementation testers involved in PLD v2 alignment work.

---

## 1. Purpose of This Log

This document serves as a traceable record of the alignment work conducted between the following layers of the PLD v2 model:

* **Level 1 — Structural Specification** (`pld_event.schema.json`)
* **Level 2 — Semantic Matrix** (`event_matrix.yaml`)
* **Level 3 — Taxonomy Proposal** (`PLD_taxonomy_v2.0.md`)
* **Level 4 — Observational and Example Data** (optional, non-normative)

The intent is to document decisions, clarifications, and open questions as the system evolves. This record is exploratory and subject to revision based on feedback and implementation experience.

---

## 2. Alignment Scope

This alignment focuses on the following areas:

| Scope Area                 | Included            | Notes                                                     |
| -------------------------- | ------------------- | --------------------------------------------------------- |
| Prefix governance          | Yes                 | Ensures consistency across schema and taxonomy.           |
| Lifecycle mapping          | Yes                 | Confirmed based on Level 2 semantic rules.                |
| Numeric classifier meaning | Yes (advisory only) | Meaning remains taxonomy-controlled, not schema-enforced. |
| Event type mapping         | Yes                 | Verified against matrix constraints.                      |
| Analytics-only signals     | Partially           | Recorded as pending governance. Not enforced.             |

---

## 3. Layer Boundary Summary

The alignment effort confirmed that each layer maintains a specific responsibility boundary:

| Layer                              | Role                                                                             | Enforcement Strength   |
| ---------------------------------- | -------------------------------------------------------------------------------- | ---------------------- |
| **Level 1: Schema**                | Defines the full structural contract for valid runtime events.                   | MUST                   |
| **Level 2: Event Matrix**          | Defines semantic interpretation rules for event types and lifecycle consistency. | MUST / SHOULD          |
| **Level 3: Taxonomy**              | Proposes naming, categorization, and governance evolution patterns.              | PROPOSED / MAY         |
| **Level 4: Observational Signals** | Used for research and evaluation purposes.                                       | Optional, not required |

This separation supports clarity, extensibility, and safe iteration.

---

## 4. Final Alignment Result

The alignment produced the following outcome:

> **No schema structural changes were required.** Numeric classifiers remain fully allowed by the existing pattern and do not require additional enforcement.

The only update applied was a **non-functional clarification to documentation language**, ensuring that numeric classifiers are acknowledged as:

* syntactically valid in Level 1,
* semantically advisory in Level 2,
* and meaningfully defined by Level 3.

No validator, ingestion system, or runtime logic is affected by this clarification.

---

## 5. Cross-Layer Consistency Table

| Element                               | Schema (L1)        | Matrix (L2)          | Taxonomy (L3)                  | Final State                |
| ------------------------------------- | ------------------ | -------------------- | ------------------------------ | -------------------------- |
| Prefix families (`D/R/RE/C/O/F`)      | Allowed & required | Enforced             | Used                           | Aligned                    |
| Numeric classifiers (`1–5`)           | Allowed (optional) | Not enforced         | Semantically meaningful        | Aligned under Hybrid Model |
| Non-lifecycle codes (`INFO_`, `SYS_`) | Allowed            | Phase must be `none` | Used for runtime states        | Aligned                    |
| Descriptor naming                     | Pattern-controlled | Meaning referenced   | Human-readable semantic intent | Aligned                    |

---

## 6. Known Ambiguities and Pending Governance

Some taxonomy entries remain unfinalized. These are intentionally preserved as “pending” and not rejected by Level 1 or Level 2.

| Case                                   | Issue Type         | Notes                                                       |
| -------------------------------------- | ------------------ | ----------------------------------------------------------- |
| `D5_latency_spike` vs `D5_information` | Numeric collision  | Requires taxonomy resolution. Schema does not block either. |
| `D0_none` vs `D0_unspecified`          | Semantic ambiguity | Future ingestion rules may clarify meaning.                 |
| Analytics-derived clusters             | Scope question     | May remain non-runtime annotations unless elevated.         |

These items will be revisited when taxonomy maturity increases.

---

## 7. Compatibility and Impact Summary

| Area                   | Impact                                                                              |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Existing logs          | Fully compatible — no reprocessing required.                                        |
| Validator behavior     | Unchanged.                                                                          |
| Runtime logic          | No required changes. Optional improvements may reference taxonomy numeric guidance. |
| Tooling and dashboards | May optionally display numeric classifier semantics in future.                      |

---

## 8. Next Review Stage

This document is expected to evolve as implementation feedback becomes available.

Future checkpoints may include:

* stability of the taxonomy numeric hierarchy,
* evaluation of edge-case events in production test data,
* potential candidate promotion from provisional to canonical status,
* investigation of whether analytics clusters should remain outside runtime encoding.

---

## 9. Feedback Invitation

Feedback, implementation reports, and proposed revisions are welcome. Perspectives from runtime engineers, annotation teams, and observability researchers are especially valuable.

> "This log represents the current understanding and remains open to refinement."
