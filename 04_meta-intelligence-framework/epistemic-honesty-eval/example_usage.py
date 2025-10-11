"""
Example usage of the Epistemic Honesty Evaluation Framework (v1.1.0)

Demonstrates:
1. Basic evaluation
2. Domain-specific evaluation
3. Reading Round-2D logs
"""

import numpy as np
from epistemic_honesty import (
    EpistemicHonestyEvaluator,
    EvaluationBatch,
    compute_brier_score,
    compute_ece,
    evaluate_from_jsonl,
)


def example_1_basic():
    print("=" * 60)
    print("Example 1: Basic Evaluation")
    print("=" * 60)
    evaluator = EpistemicHonestyEvaluator()
    batch = EvaluationBatch(
        confidences=np.array([0.74, 0.48, 0.47, 0.56]),
        correctness=np.array([1.0, 0.0, 0.5, 0.7]),
        predicted_blindspots=[
            {"numerical_error", "precision"},
            {"temporal_context", "definition_change"},
            {"definition_ambiguity", "measurement_method"},
            {"normative_foundation", "value_conflict"},
        ],
        gold_blindspots=[
            {"numerical_error", "precision", "discrete_vs_continuous"},
            {"temporal_context", "definition_change", "cultural_difference"},
            {"definition_ambiguity", "measurement_method", "long_term_effects"},
            {"normative_foundation", "value_conflict", "value_pluralism"},
        ],
        confidence_changes=np.array([0.004, 0.038, 0.045, 0.050]),
        context_changes=np.array([0.05, 0.80, 0.70, 0.60]),
    )
    results = evaluator.evaluate(batch)
    print(f"EHS: {results['epistemic_honesty_score']:.3f}")
    print(f"Calibration: {results['calibration_score']:.3f}")
    print(f"Blindspot F1: {results['blindspot_f1']:.3f}")
    print(f"Context Sensitivity: {results['context_sensitivity']:.3f}")
    print(f"95% CI: {results['context_sensitivity_ci']}")
    print()


def example_2_domain_specific():
    print("=" * 60)
    print("Example 2: Domain-Specific Evaluation")
    print("=" * 60)
    medical = EpistemicHonestyEvaluator(overconf_penalty=3.0)
    general = EpistemicHonestyEvaluator(overconf_penalty=2.0)
    batch = EvaluationBatch(
        confidences=np.array([0.85, 0.90, 0.80, 0.75]),
        correctness=np.array([0.5, 0.3, 0.6, 0.8]),
        predicted_blindspots=[
            {"numerical_error"},
            {"temporal_context"},
            {"definition_ambiguity"},
            {"normative_foundation"},
        ],
        gold_blindspots=[
            {"numerical_error", "discrete_vs_continuous"},
            {"temporal_context", "cultural_difference"},
            {"definition_ambiguity", "long_term_effects"},
            {"normative_foundation", "value_pluralism"},
        ],
        confidence_changes=np.array([0.01, 0.02, 0.015, 0.012]),
        context_changes=np.array([0.1, 0.2, 0.15, 0.12]),
    )
    med_r = medical.evaluate(batch)
    gen_r = general.evaluate(batch)
    print("Medical domain (strict):", med_r["epistemic_honesty_score"])
    print("General domain (balanced):", gen_r["epistemic_honesty_score"])
    print("Interpretation: stronger over-confidence penalty lowers EHS.\n")


def example_3_from_jsonl(path="sample_round2d.jsonl"):
    print("=" * 60)
    print("Example 3: Evaluate from Round-2D JSONL")
    print("=" * 60)
    evaluator = EpistemicHonestyEvaluator()
    try:
        results = evaluate_from_jsonl(path, evaluator)
        print("Aggregated EHS:", results["epistemic_honesty_score"])
    except FileNotFoundError:
        print("Sample file not found (optional demo).")
    print()


if __name__ == "__main__":
    example_1_basic()
    example_2_domain_specific()
    example_3_from_jsonl()
    print("✓ All examples completed successfully.")
