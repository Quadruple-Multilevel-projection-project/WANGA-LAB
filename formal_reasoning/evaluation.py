"""Hard-gated candidate evaluation; scores are measurements, not learning signals."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

POLICY_PATH = Path(__file__).resolve().parent / "config" / "evaluation_policy.json"
PROBABILITY_METRICS = (
    "source_coverage", "evidence_coverage", "benchmark_accuracy",
    "counterexample_rate", "false_accept_rate", "counterexample_escape_rate",
    "holdout_score",
)
THRESHOLD_KEYS = (
    "min_source_coverage", "min_evidence_coverage", "min_benchmark_accuracy",
    "max_counterexample_rate", "max_false_accept_rate",
    "max_counterexample_escape_rate", "min_holdout_score", "max_compute_seconds",
)
BOOLEAN_METRICS = ("premises_consistent", "formal_checks_pass", "replay_stable")


def _bounded_probability(value: Any, name: str) -> float:
    if (
        not isinstance(value, (int, float))
        or isinstance(value, bool)
        or not math.isfinite(float(value))
        or not 0.0 <= float(value) <= 1.0
    ):
        raise ValueError(f"{name} must be a finite numeric value in [0, 1]")
    return float(value)


def load_evaluation_policy(path: Path | str | None = None) -> tuple[dict[str, float], str]:
    config_path = Path(path) if path is not None else POLICY_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "wanga-candidate-evaluation-policy/1.0":
        raise ValueError("unsupported candidate evaluation policy schema")
    thresholds = payload.get("thresholds")
    if not isinstance(thresholds, dict):
        raise ValueError("policy thresholds must be an object")
    if set(thresholds) != set(THRESHOLD_KEYS):
        raise ValueError("policy must define exactly the required evaluation thresholds")
    for name in THRESHOLD_KEYS:
        value = thresholds[name]
        if name == "max_compute_seconds":
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
                or float(value) <= 0
            ):
                raise ValueError("max_compute_seconds must be a positive finite number")
        else:
            _bounded_probability(value, name)
    if payload.get("status") != "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED":
        raise ValueError("policy must explicitly state that thresholds are uncalibrated")
    required_gates = {
        "premises_consistent", "formal_checks_pass", "source_coverage", "evidence_coverage",
        "benchmark_accuracy", "counterexample_rate", "false_accept_rate",
        "counterexample_escape_rate", "holdout_score", "replay_stable", "compute_budget",
    }
    if not isinstance(payload.get("hard_gates"), list) or set(payload["hard_gates"]) != required_gates:
        raise ValueError("policy hard_gates must exactly match the configured evaluator gates")
    rules = payload.get("rules")
    required_rules = (
        "hard_gates_cannot_be_offset_by_descriptive_score", "no_weight_updates",
        "no_epistemic_status_promotion", "solver_result_not_truth",
        "missing_metrics_fail_closed", "rates_require_labeled_benchmark_denominators",
    )
    if not isinstance(rules, dict) or any(rules.get(key) is not True for key in required_rules):
        raise ValueError("policy must enable all mandatory evaluation safety rules")
    return {key: float(value) for key, value in thresholds.items()}, str(payload["status"])


DEFAULT_THRESHOLDS, DEFAULT_THRESHOLD_STATUS = load_evaluation_policy()


def evaluate_candidate(metrics: Mapping[str, Any], thresholds: Mapping[str, float] | None = None) -> dict[str, Any]:
    """Evaluate explicit metrics; never update weights or promote epistemic status.

    false_accept_rate is the share of known-invalid benchmark candidates accepted.
    counterexample_escape_rate is the share of registered counterexamples not detected
    by the candidate's applicable gates. They must be measured, not defaulted to zero.
    """
    if not isinstance(metrics, Mapping):
        raise ValueError("metrics must be an object")
    policy = dict(DEFAULT_THRESHOLDS)
    if thresholds is not None:
        if not isinstance(thresholds, Mapping):
            raise ValueError("thresholds must be an object")
        unknown_thresholds = set(thresholds) - set(policy)
        if unknown_thresholds:
            raise ValueError(f"unknown thresholds: {sorted(unknown_thresholds)}")
        policy.update(thresholds)

    for name in THRESHOLD_KEYS:
        value = policy[name]
        if name == "max_compute_seconds":
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not math.isfinite(float(value))
                or float(value) <= 0
            ):
                raise ValueError("max_compute_seconds must be a positive finite number")
        else:
            _bounded_probability(value, name)

    normalized = dict(metrics)
    for name in PROBABILITY_METRICS:
        normalized[name] = _bounded_probability(normalized.get(name), name)
    compute = normalized.get("compute_seconds")
    if (
        not isinstance(compute, (int, float))
        or isinstance(compute, bool)
        or not math.isfinite(float(compute))
        or float(compute) < 0
    ):
        raise ValueError("compute_seconds must be a finite non-negative number")
    normalized["compute_seconds"] = float(compute)

    for name in BOOLEAN_METRICS:
        if not isinstance(normalized.get(name), bool):
            raise ValueError(f"{name} must be an explicit boolean")

    gates = {
        "premises_consistent": normalized["premises_consistent"],
        "formal_checks_pass": normalized["formal_checks_pass"],
        "source_coverage": normalized["source_coverage"] >= policy["min_source_coverage"],
        "evidence_coverage": normalized["evidence_coverage"] >= policy["min_evidence_coverage"],
        "benchmark_accuracy": normalized["benchmark_accuracy"] >= policy["min_benchmark_accuracy"],
        "counterexample_rate": normalized["counterexample_rate"] <= policy["max_counterexample_rate"],
        "false_accept_rate": normalized["false_accept_rate"] <= policy["max_false_accept_rate"],
        "counterexample_escape_rate": normalized["counterexample_escape_rate"] <= policy["max_counterexample_escape_rate"],
        "holdout_score": normalized["holdout_score"] >= policy["min_holdout_score"],
        "replay_stable": normalized["replay_stable"],
        "compute_budget": normalized["compute_seconds"] <= policy["max_compute_seconds"],
    }
    descriptive_score = round(
        0.15 * float(normalized["formal_checks_pass"])
        + 0.12 * normalized["source_coverage"]
        + 0.12 * normalized["evidence_coverage"]
        + 0.16 * normalized["benchmark_accuracy"]
        + 0.16 * normalized["holdout_score"]
        + 0.10 * float(normalized["replay_stable"])
        + 0.07 * (1.0 - normalized["counterexample_rate"])
        + 0.06 * (1.0 - normalized["false_accept_rate"])
        + 0.06 * (1.0 - normalized["counterexample_escape_rate"]),
        6,
    )
    return {
        "schema_version": "wanga-candidate-evaluation/1.0",
        "status": "ELIGIBLE_FOR_INDEPENDENT_REVIEW" if all(gates.values()) else "BLOCKED_BY_HARD_GATE",
        "hard_gates": gates,
        "all_hard_gates_pass": all(gates.values()),
        "descriptive_score": descriptive_score,
        "score_semantics": "DESCRIPTIVE_INDEX_ONLY_NOT_TRUTH_CONFIDENCE_NOT_REWARD_UPDATE",
        "metric_definitions": {
            "source_coverage": "Fraction of package claims/components with resolvable source references.",
            "evidence_coverage": "Fraction of benchmarked claims whose cited evidence spans were reviewed against the claim.",
            "false_accept_rate": "Fraction of known-invalid benchmark candidates incorrectly accepted.",
            "counterexample_escape_rate": "Fraction of registered counterexamples not detected by the candidate's applicable gates.",
        },
        "metrics": normalized,
        "thresholds": policy,
        "threshold_status": DEFAULT_THRESHOLD_STATUS,
        "weight_update_performed": False,
        "epistemic_status_promotion": "FORBIDDEN",
        "verification_status": "NOT_YET_VERIFIED",
    }
