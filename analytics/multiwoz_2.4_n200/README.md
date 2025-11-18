# 📊 PLD Benchmark Dataset (MultiWOZ 2.4 — N=200)

> This repository does not redistribute or include the original MultiWOZ 2.4 dialogue text.
> Only derived metadata, annotations, and evaluation artifacts are included.
> Per CC-BY-SA 4.0 interpretation guidelines, annotation layers that do not reproduce or contain original text are considered separate works and thus may carry an > independent license.
> Users wishing to access or regenerate the evaluation dataset must obtain the original MultiWOZ dataset from the upstream repository and comply with its license.

Note: For an applied end-to-end implementation case (including runtime logging and repair orchestration), see `/analytics/case_study_end_to_end.md`.

---

**Evaluation Reference Set for Phase Loop Dynamics (PLD) Runtime**

This directory contains a curated evaluation set derived from:

> **MultiWOZ 2.4 Dataset (smartyfh, 2023)**  
> License: **CC BY-SA 4.0**  
> Source: https://github.com/smartyfh/MultiWOZ2.4

The subset includes **200 dialogs** selected to reflect:

- realistic failure patterns  
- recovery attempts  
- tool-use ambiguity  
- multi-turn conversational drift behaviors  

suitable for **Phase Loop Dynamics analysis**.

This benchmark provides the evidence layer used to evaluate:

> **Drift → Repair → Reentry → Outcome**

across real-world negotiation, reasoning, and task-oriented dialogue.

---

## 1. Purpose

This benchmark exists to:

- Validate PLD runtime behavior against **uncontrolled natural conversation**
- Provide a reproducible reference for:
  - drift detection accuracy  
  - repair timing  
  - reentry confirmation success rate  
- Enable fair comparison across:
  - agents  
  - orchestration pipelines  
  - LLM model architectures  

📌 This dataset is an **evaluation resource — not a training set.**

---

## 2. Contents

```
multiwoz_2.4_n200/
│
├── 01_pld_applied_report_summary.md    # High-level findings + operational insights
├── 02_pld_results_summary.md           # Quantitative metrics + phase distribution
├── 03_pld_casebook.md                  # Annotated dialog cases (raw style)
├── 04_pld_casebook_unified.md          # Normalized PLD annotation format
└── README.md                           # (this file)
```

### Artifact Roles

| File | Role |
|------|------|
| `01_pld_applied_report_summary.md` | Narrative analysis + operational implications |
| `02_pld_results_summary.md` | Aggregate phase frequency and metrics |
| `03_pld_casebook.md` | Direct annotated case examples |
| `04_pld_casebook_unified.md` | Canonical structured annotation format |

---

## 3. Annotation Model

All annotations follow the canonical **PLD phase taxonomy**:

| Phase | Meaning |
|-------|--------|
| Drift | System diverges from shared grounding |
| Repair | Attempt to restore alignment |
| Reentry | Verification that alignment has been restored |
| Outcome | Terminal state: success or failure |

These annotations are compatible with runtime schemas in:

```
pld_runtime/01_schemas/
```

and can be parsed directly by the PLD runtime pipeline.

---

#### 🔗 Metric Continuity

For operational metrics derived from these annotations, see:

```
/docs/07_pld_operational_metrics_cookbook.md
```

(PRDR, REI, VRL definitions and evaluation strategy)

---

## 4. Reproducibility

Raw conversation text **is not included** due to dataset licensing.

To regenerate this evaluation set:

1. Download MultiWOZ 2.4 from the source repository  
2. Apply the selection index stored in:

```
04_pld_casebook_unified.md
```

3. Use ingestion utilities in:

```
pld_runtime/02_ingestion/
```

A full replication guide will be added in:

```
metrics_studies/REPLICATION_GUIDE.md
```

---

## 5. Relationship to Runtime

This evaluation dataset aligns with the PLD runtime workflow:

```
Dataset → Ingestion → Detection → Enforcement → Controller → Logging
                                        │
                                        └── Comparison against benchmark annotations
```

Typical use cases include:

- runtime tuning  
- drift trigger calibration  
- repair timing evaluation  
- benchmark scoring  
- comparative agent evaluation (LLM / rule-based / hybrid)  

For runnable examples demonstrating runtime + repair orchestration, see:

```
/quickstart/patterns/04_integration_recipes/
```

---

## 6. Future Extensions

Planned additions include:

- multilingual evaluation set  
- tool-enabled conversation subset  
- mixed-modality dialogs  
- synthetic injected drift scenarios  

All expansions will maintain **schema backward compatibility.**

---

## 7. License

This dataset is derived from:

> **MultiWOZ 2.4 — CC BY-SA 4.0**

PLD annotations and metadata are released under:

> **CC BY-NC 4.0**

Commercial evaluation usage requires written approval.

---

> **This benchmark provides the empirical backbone of PLD.**  
> Where runtime enforces stability — this dataset tests whether that stability holds.

