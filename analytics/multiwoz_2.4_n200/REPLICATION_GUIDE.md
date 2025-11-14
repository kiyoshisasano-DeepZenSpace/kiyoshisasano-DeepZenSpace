# REPLICATION_GUIDE.md  
Replication Protocol for PLD Evaluation (MultiWOZ 2.4 — N=200 Subset)

**Status:** Stable  
**Scope:** Reproduce the evaluation pipeline, scoring results, and qualitative PLD annotation process used in this repository.

---

## 1. Purpose

This guide enables researchers and engineers to:

- Reproduce the N=200 evaluation set selection
- Apply PLD annotation rules consistently
- Benchmark live models or agent systems using the same methodology
- Compare results to the baseline contained in this folder

The intent is to ensure **methodological consistency**, not to prescribe a specific model or runtime configuration.

---

## 2. Requirements

### 2.1 Dataset Source

| Item | Value |
|------|-------|
| Dataset | MultiWOZ 2.4 |
| Author | smartyfh (2023) |
| License | CC BY-SA 4.0 |
| Link | https://github.com/smartyfh/MultiWOZ2.4 |

Download the dataset locally before proceeding.

### 2.2 Runtime Requirements

| Component | Version |
|----------|---------|
| `pld_runtime` | 2025.1 or newer |
| Python | ≥ 3.10 |
| Optional | Jupyter Notebook for interactive annotation |

---

## 3. Sample Selection Criteria (N=200)

The subset was selected using the following filters:

| Rule | Applied |
|------|---------|
| Dialogue length ≥ 8 turns | ✔ |
| Contains at least one system–user correction or clarification | ✔ |
| Includes at least one clear task objective (booking, request, confirmation) | ✔ |
| Excludes incomplete or corrupted logs | ✔ |

Sampling method: **Stratified random selection across domains**  
(domains: hotel, train, taxi, attraction, restaurant, misc).

A manifest of included dialogues is located at:

```
00_manifest_selection.csv
```

---

## 4. Preprocessing

Before annotation or runtime evaluation, normalize conversations using:

```
pld_runtime/02_ingestion/normalization.py
```

Normalization enforces:

- Unified role labels (`user`, `system`)
- Text cleaning (whitespace, markup)
- Turn sequencing and indexing
- Runtime metadata injection

Example transformation:

```
Raw → NormalizedTurn(session_id, turn_id, role, text, runtime)
```

---

## 5. Annotation Procedure (PLD Model)

Each turn is evaluated sequentially and labeled using:

> **Drift → Repair → Reentry → Outcome**

### 5.1 Annotation Rules

| Phase | Required Evidence |
|-------|------------------|
| **Drift** | Hallucination, contradiction, tool mismatch, context loss |
| **Repair** | Correction, clarification request, re-alignment attempt |
| **Reentry** | Explicit validation confirming shared understanding |
| **Outcome** | Successful completion OR controlled termination |

Annotation examples are provided in:

```
03_pld_casebook.md
04_pld_casebook_unified.md
```

---

## 6. Runtime Comparison Benchmarking

To evaluate a model or orchestration system, run:

```
python run_pld_eval.py \
--dataset multiwoz_2.4 \
--subset manifest=00_manifest_selection.csv \
--runtime pld_runtime \
--mode benchmark
```

### Outputs

| File | Meaning |
|------|---------|
| `runtime_trace.jsonl` | Event-level trace |
| `pld_metrics.json` | Drift, repair ratio, reentry success rate |
| `session_scores.csv` | Per-dialogue summary |

---

## 7. Expected Outputs

Successful replication should yield:

- Comparable **drift detection sensitivity**
- Equivalent repair recognition patterns
- Consistent reentry checkpoint timing
- Similar distribution of **Outcome categories**

Runtime variance is allowed — **label methodology must match.**

---

## 8. Versioning and Extensions

Future datasets should replicate this structure:

```
analytics/
└── multiwoz_2.4_n200/
    ├── data/
    │   └── conversations.json
    ├── 01_pld_applied_report_summary.md
    ├── 02_pld_results_summary.md
    ├── 03_pld_casebook.md
    ├── 04_pld_casebook_unified.md
    ├── REPLICATION_GUIDE.md
    └── README.md


This guide is version-controlled and updates follow:

```
_meta/CHANGELOG.md
```

---

> Replication is not about matching numbers —  
> it is about matching **methodology, signal semantics, and evaluation process.**
