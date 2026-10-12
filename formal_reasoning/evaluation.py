"""Hard-gated candidate evaluation; scores are measurements, not learning signals."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

POLICY_PATH = Path(__file__).resolve().parent / "config" / "evaluation_policy.json"


def load_evaluation_policy(path: Path | str | None = None) -> tuple[dict[str, float], str]:
    config_path = Path(path) if path is not None else POLICY_PATH
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "wanga-candidate-evaluation-policy/1.0":
        raise ValueError("unsupported candidate evaluation policy schema")
    thresholds = payload.get("thresholds")
    if not isinstance(thresholds, dict):
        raise ValueError("policy thresholds must be an object")
    required = {
        "min_source_coverage", "min_benchmark_accuracy", "max_counterexample_rate",
        "min_holdout_score", "max_compute_seconds"
    }
    if set(thresholds) != required:
        raise ValueError("policy must define exactly the required evaluation thresholds")
    for name in required - {"max_compute_seconds"}:
        value = thresholds[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) or not 0 <= value <= 1:
            raise ValueError(f"policy threshold {name} must be a finite number in [0, 1]")
    max_compute = thresholds["max_compute_seconds"]
    if not isinstance(max_compute, (int, float)) or isinstance(max_compute, bool) or not math.isfinite(float(max_compute)) or max_compute <= 0:
        raise ValueError("policy max_compute_seconds must be a positive finite number")
    if payload.get("status") != "INITIAL_CONFIG_NOT_EMPIRICALLY_CALIBRATED":
        raise ValueError("policy must explicitly state that thresholds are uncalibrated")
    return {key: float(value) for key, value in thresholds.items()}, str(payload["status"])


DEFAULT_THRESHOLDS, DEFAULT_THRESHOLD_STATUS = load_evaluation_policy()


def evaluate_candidate(metrics: Mapping[str, Any], thresholds: Mapping[str, float] | None = None) -> dict[str, Any]:
    """Evaluate a candidate by vector and hard gates; never update weights or status to VERIFIED."""
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
    for name in ("min_source_coverage", "min_benchmark_accuracy", "max_counterexample_rate", "min_holdout_score"):
        value = policy[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a finite number in [0, 1]")
    if not isinstance(policy["max_compute_seconds"], (int, float)) or isinstance(policy["max_compute_seconds"], bool) or not math.isfinite(float(policy["max_compute_seconds"])) or policy["max_compute_seconds"] <= 0:
        raise ValueError("max_compute_seconds must be a positive finite number")
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
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)) or not minimum <= value <= maximum:
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
        "threshold_status": DEFAULT_THRESHOLD_STATUS,
        "weight_update_performed": False,
        "epistemic_status_promotion": "FORBIDDEN",
        "verification_status": "NOT_YET_VERIFIED",
    }
