# PLD Documentation Index (Applied-AI)

This folder contains the core documentation required to understand, label, evaluate, and integrate Phase Loop Dynamics (PLD) into applied LLM systems, tool-based agents, and multi-turn orchestration workflows.

The documents are structured so that engineers can read them **in order**, apply them to real systems, and return as needed while building or evaluating agents.

---

## How to Use This Folder

If you are new to PLD or implementing it for the first time, follow this reading order:

| Step | File | Purpose |
|------|------|---------|
| **1** | `01_pld_for_agent_engineers.md` | Entry strategy: what PLD solves, how it works, and how to integrate it. |
| **2** | `02_pld_drift_repair_reference.md` | Canonical dictionary of Drift, Repair, and Reentry codes — used in labeling and detection. |
| **3** | `04_pld_labeling_prompt_llm.md` | LLM-ready prompt for automated PLD annotation of logs and transcripts. |
| **4** | (optional) future: evaluation schemas or human annotation guidance | Only needed if extending PLD to datasets or research. |

After reading the core documents, continue into:

| Category | Destination | Purpose |
|----------|------------|---------|
| Runtime integration | `/quickstart/operator_primitives/` | Add repair/reflex logic into control loops. |
| Logging and evaluation | `/quickstart/metrics/` | Track drift frequency, repair outcomes, and stability over time. |
| Applied examples | `/metrics/multiwoz_2.4_n200/` | See real annotated dialogues and analysis patterns. |

> **Optional but recommended:**  
For a higher-level architectural understanding before implementation, see:

📄 `architecture_layers.md` — PLD as a layered runtime governance model  
(Helps map phases → responsibilities → implementation boundaries.)

---

## File Overview

| File | Status | Role |
|------|--------|------|
| `01_pld_for_agent_engineers.md` | Core | Starting point — conceptual and practical overview. |
| `02_pld_drift_repair_reference.md` | Core | Source of truth for all labeled codes. |
| `04_pld_labeling_prompt_llm.md` | Core | The official machine-usable labeling prompt template. |
| `architecture_layers.md` | Reference | High-level conceptual architecture (not implementation-specific). |


Additional files may be added in future versions, but the **core three documents will remain stable** and form the basis of:

- PLD metrics
- operator behaviors
- dataset labeling
- debugging frameworks
- workflow validation

---

## Update Rules

All files in this directory must follow:

- **Stable terminology**: values must match the taxonomy file (`02_...`).
- **No hidden synonyms**: code values must remain single-source-of-truth.
- **Reverse compatibility**: if a code is deprecated, document it explicitly.
- **Footer required**: each file ends with:

```
Maintainer: Kiyoshi Sasano
```

---

## Contribution Notes

If adding new documentation, ask:

- Does this change a definition or code value?  
  → If yes, update `02_pld_drift_repair_reference.md`.

- Does this describe how to apply PLD?  
  → If yes, ensure consistency with `01_pld_for_agent_engineers.md`.

- Is this instructions for annotation or automation?  
  → Place it next to (not inside) `04_pld_labeling_prompt_llm.md`.

- Is it experimental or early research?  
  → Place in `/research/` or do **not** include in core docs.

---

## Placement

```
docs/
  ├── README_docs.md                ← (this file)
  ├── 01_pld_for_agent_engineers.md
  ├── 02_pld_drift_repair_reference.md
  └── 04_pld_labeling_prompt_llm.md
```

---


Maintainer: Kiyoshi Sasano
