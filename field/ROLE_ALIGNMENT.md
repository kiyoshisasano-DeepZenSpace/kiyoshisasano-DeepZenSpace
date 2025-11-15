# ROLE ALIGNMENT — PLD Collaboration Context

This document clarifies the roles, responsibilities, and boundaries  
for collaboration around PLD (Phase Loop Dynamics).

It exists to set expectations and avoid ambiguity between:

- **Architect (Framework Owner / Author)**
- **Implementers (Engineers, Applied AI Teams, Integrators)**
- **Collaborators (Research, Ops, Evaluation, Product Stakeholders)**

---

## 1. The Role of the Architect (Repository Maintainer)

The repository owner **defines the PLD framework**, including:

- The conceptual foundation (Drift → Repair → Reentry → Outcome)
- The runtime model and interaction logic
- The shared vocabulary, metrics, and evaluation criteria
- Pattern-level guidelines for implementation and operation

The architect:

✔ designs the structure  
✔ defines the intent and reasoning  
✔ maintains conceptual coherence across contributions  

The architect **does not own**:

✘ implementation work for partner systems  
✘ product-specific tuning  
✘ infrastructure, deployment, or localization  
✘ organizational compliance or risk acceptance

Instead, the architect acts as:

> **A system-level thinker who provides structure, language, and alignment — not execution.**

---

## 2. The Role of Implementers

Implementers include:

- LLM/Agent engineers  
- Tooling and orchestration developers  
- RAG + agent integrators  
- Conversation system owners  

Their role is to:

- Apply PLD operators to their systems
- Build runtime implementations
- Collect logs and metrics
- Adapt PLD to domain constraints and UX expectations

They:

✔ write code  
✔ deploy systems  
✔ validate runtime behavior  
✔ contribute improvements or operational patterns  

They **do not** modify the conceptual model without governance review.

---

## 3. The Role of Collaborators (Optional)

Some projects involve additional roles:

- Evaluation teams  
- Applied AI researchers  
- Product owners  
- AgentOps / QA reviewers  

Their role is to:

- Analyze traces and metrics
- Provide behavioral feedback
- Compare PLD performance to baselines
- Recommend adjustments based on risk, UX, or operational constraints

They typically do **not**:

- modify runtime code  
- define PLD taxonomy  
- change framework semantics  

---

## 4. Collaboration Boundaries

| Area | Architect | Implementer | Collaborator |
|-------|----------|-------------|--------------|
| PLD conceptual model | **Owner** | Contributor (via proposals) | Optional |
| Code / runtime implementation | Advisor | **Owner** | Optional |
| Metrics and evaluation | Defines schema | Generates logs | **Interprets or compares** |
| Operational decisions | No | Yes | Yes (shared) |
| Final go/no-go for product usage | No | **Yes** | Yes (context-dependent) |

---

## 5. Change Governance

To maintain consistency, changes follow:
```text
Proposal → Review → Approval → Adoption → Version Note
```

Changes affecting:

- terminology
- runtime structure
- event semantics
- metrics schema

require review by the architect.

Changes affecting:

- code implementation
- adapters or integrations
- dataset extensions
- UX variants

may proceed via PR with light governance.

---

## 6. Why This Alignment Exists

PLD is a **runtime interaction model**, not a single implementation.

Without role clarity:

- Organizations may treat PLD as a product instead of an execution model  
- Implementers may attempt private interpretations that break compatibility  
- Collaboration may stall due to unclear ownership of decisions  

This document ensures:

> **Shared language, shared expectations, shared contribution structure — without role collision.**

---

## 7. Summary

- The architect **defines and maintains PLD.**
- Implementers **apply and operationalize PLD.**
- Collaborators **evaluate and contextualize results.**

This alignment preserves:

- conceptual integrity  
- reproducibility  
- interoperability  
- responsible iteration  

---

> PLD succeeds when roles complement — not overlap.  
> The framework is the shared spine, not the implementation.


