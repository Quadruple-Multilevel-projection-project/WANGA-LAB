"""Auditable candidate gates; scores cannot auto-promote epistemic status."""
from __future__ import annotations

from typing import Any, Mapping


DEFAULT_THRESHOLDS = {
    "min_evidence_coverage": 0.95,
    "min_benchmark_accuracy": 0.90,
    "max_false_accept_rate": 0.05,
    "max_counterexample_escape_rate": 0.05,
}


def evaluate_candidate(
    *,
    formal_check: Mapping[str, Any],
    benchmark_metrics: Mapping[str, Any],
    evidence_coverage: float,
    replay_hash_match: bool,
    thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Return an auditable vector and review decision, never VERIFIED.

    Hard gates are not averaged together. Missing metrics block acceptance.
    This function records evaluation only; it does not update model parameters.
    """
    config = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        for key, value in thresholds.items():
            if key not in config:
                raise ValueError(f"unknown threshold: {key}")
            if not isinstance(value, (int, float)) or not 0 <= value <= 1:
                raise ValueError(f"threshold {key} must be in [0, 1]")
            config[key] = float(value)
    if not isinstance(evidence_coverage, (int, float)) or not 0 <= evidence_coverage <= 1:
        raise ValueError("evidence_coverage must be in [0, 1]")
    if not isinstance(replay_hash_match, bool):
        raise ValueError("replay_hash_match must be boolean")

    metrics = {}
    for key in ("accuracy", "false_accept_rate", "counterexample_escape_rate"):
        value = benchmark_metrics.get(key)
        if value is not None and (not isinstance(value, (int, float)) or not 0 <= value <= 1):
            raise ValueError(f"benchmark metric {key} must be in [0, 1]")
        metrics[key] = float(value) if value is not None else None

    formal_status = str(formal_check.get("entailment_status", formal_check.get("status", "MISSING")))
    premise_status = str(formal_check.get("premise_consistency", "MISSING"))
    gates = {
        "premises_consistent": premise_status == "SAT",
        "formal_entailment_supported": formal_status == "ENTAILED_WITHIN_ENCODED_FRAGMENT",
        "evidence_coverage_threshold_met": evidence_coverage >= config["min_evidence_coverage"],
        "benchmark_accuracy_threshold_met": metrics["accuracy"] is not None and metrics["accuracy"] >= config["min_benchmark_accuracy"],
        "false_accept_rate_within_limit": metrics["false_accept_rate"] is not None and metrics["false_accept_rate"] <= config["max_false_accept_rate"],
        "counterexample_escape_rate_within_limit": metrics["counterexample_escape_rate"] is not None and metrics["counterexample_escape_rate"] <= config["max_counterexample_escape_rate"],
        "deterministic_replay_matches": replay_hash_match,
    }
    failed_gates = [name for name, passed in gates.items() if not passed]
    if formal_status == "NOT_ENTAILED_COUNTERMODEL" or premise_status == "UNSAT":
        decision = "REJECT_OR_REFORMULATE"
    elif failed_gates:
        decision = "HOLD_FOR_EVIDENCE_OR_REVIEW"
    else:
        decision = "ELIGIBLE_FOR_INDEPENDENT_REVIEW"
    return {
        "schema_version": "wanga-logic-candidate-evaluation/1.0",
        "decision": decision,
        "verification_status": "NOT_YET_VERIFIED",
        "formal_status": formal_status,
        "premise_consistency": premise_status,
        "evidence_coverage": float(evidence_coverage),
        "benchmark_metrics": metrics,
        "replay_hash_match": replay_hash_match,
        "thresholds": config,
        "hard_gates": gates,
        "failed_gates": failed_gates,
        "score_vector": {
            "formal_check": formal_status,
            "evidence_coverage": float(evidence_coverage),
            "benchmark_accuracy": metrics["accuracy"],
            "false_accept_rate": metrics["false_accept_rate"],
            "counterexample_escape_rate": metrics["counterexample_escape_rate"],
            "deterministic_replay": replay_hash_match,
        },
        "learning_status": "EVALUATION_ONLY_NO_WEIGHTS_UPDATED",
        "reward_boundary": "SAT alone, score alone, or a passing software test never establishes semantic truth and cannot promote VERIFIED status.",
    }
