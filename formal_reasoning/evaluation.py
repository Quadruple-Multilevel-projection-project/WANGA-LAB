"""Hard-gated candidate evaluation; scores are measurements, not learning signals."""
from __future__ import annotations

from typing import Any, Mapping

DEFAULT_THRESHOLDS = {
    "min_source_coverage": 0.95,
    "min_benchmark_accuracy": 0.90,
    "max_counterexample_rate": 0.02,
    "min_holdout_score": 0.85,
    "max_compute_seconds": 30.0,
}


def evaluate_candidate(metrics: Mapping[str, Any], thresholds: Mapping[str, float] | None = None) -> dict[str, Any]:
    """Evaluate a candidate by vector and hard gates; never update weights or status to VERIFIED."""
    if not isinstance(metrics, Mapping):
        raise ValueError("metrics must be an object")
    policy = dict(DEFAULT_THRESHOLDS)
    if thresholds is not None:
        if not isinstance(thresholds, Mapping):
            raise ValueError("thresholds must be an object")
        policy.update(thresholds)
    bounded = {
        "source_coverage": (0.0, 1.0),
        "benchmark_accuracy": (0.0, 1.0),
        "counterexample_rate": (0.0, 1.0),
        "holdout_score": (0.0, 1.0),
        "compute_seconds": (0.0, float("inf")),
    }
    normalized = dict(metrics)
    for name, (minimum, maximum) in bounded.items():
        value = normalized.get(name)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not minimum <= value <= maximum:
            raise ValueError(f"{name} must be a numeric value in [{minimum}, {maximum}]")
        normalized[name] = float(value)
    for name in ("premises_consistent", "formal_checks_pass", "replay_stable"):
        if not isinstance(normalized.get(name), bool):
            raise ValueError(f"{name} must be an explicit boolean")
    gates = {
        "premises_consistent": normalized["premises_consistent"],
        "formal_checks_pass": normalized["formal_checks_pass"],
        "source_coverage": normalized["source_coverage"] >= policy["min_source_coverage"],
        "benchmark_accuracy": normalized["benchmark_accuracy"] >= policy["min_benchmark_accuracy"],
        "counterexample_rate": normalized["counterexample_rate"] <= policy["max_counterexample_rate"],
        "holdout_score": normalized["holdout_score"] >= policy["min_holdout_score"],
        "replay_stable": normalized["replay_stable"],
        "compute_budget": normalized["compute_seconds"] <= policy["max_compute_seconds"],
    }
    # A transparent descriptive index; hard gates, not this mean, determine eligibility.
    descriptive_score = round(
        0.20 * float(normalized["formal_checks_pass"])
        + 0.20 * normalized["source_coverage"]
        + 0.20 * normalized["benchmark_accuracy"]
        + 0.20 * normalized["holdout_score"]
        + 0.10 * float(normalized["replay_stable"])
        + 0.10 * (1.0 - normalized["counterexample_rate"]),
        6,
    )
    return {
        "schema_version": "wanga-candidate-evaluation/1.0",
        "status": "ELIGIBLE_FOR_INDEPENDENT_REVIEW" if all(gates.values()) else "BLOCKED_BY_HARD_GATE",
        "hard_gates": gates,
        "all_hard_gates_pass": all(gates.values()),
        "descriptive_score": descriptive_score,
        "score_semantics": "DESCRIPTIVE_INDEX_ONLY_NOT_TRUTH_CONFIDENCE_NOT_REWARD_UPDATE",
        "metrics": normalized,
        "thresholds": policy,
        "threshold_status": "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED",
        "weight_update_performed": False,
        "epistemic_status_promotion": "FORBIDDEN",
        "verification_status": "NOT_YET_VERIFIED",
    }
