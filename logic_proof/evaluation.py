"""Auditable candidate gates using the shared policy; never promotes epistemic status."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Mapping

_POLICY_PATH = Path(__file__).resolve().parents[1] / "formal_reasoning" / "config" / "evaluation_policy.json"
_POLICY = json.loads(_POLICY_PATH.read_text(encoding="utf-8"))
if _POLICY.get("schema_version") != "wanga-candidate-evaluation-policy/1.0":
    raise ValueError("unsupported shared evaluation policy schema")
_SHARED = _POLICY["thresholds"]
DEFAULT_THRESHOLDS = {
    "min_evidence_coverage": float(_SHARED["min_evidence_coverage"]),
    "min_benchmark_accuracy": float(_SHARED["min_benchmark_accuracy"]),
    "max_false_accept_rate": float(_SHARED["max_false_accept_rate"]),
    "max_counterexample_escape_rate": float(_SHARED["max_counterexample_escape_rate"]),
    "min_holdout_score": float(_SHARED["min_holdout_score"]),
    "max_compute_seconds": float(_SHARED["max_compute_seconds"]),
}


def evaluate_candidate(
    *,
    formal_check: Mapping[str, Any],
    benchmark_metrics: Mapping[str, Any],
    evidence_coverage: float,
    replay_hash_match: bool,
    holdout_score: float | None = None,
    compute_seconds: float | None = None,
    thresholds: Mapping[str, float] | None = None,
) -> dict[str, Any]:
    """Return an auditable vector and review decision, never VERIFIED.

    This function consumes the same thresholds as the propositional frontend.
    Missing holdout/cost measurements block independent-review eligibility.
    Scores never override hard gates and never update weights.
    """
    config = dict(DEFAULT_THRESHOLDS)
    if thresholds is not None:
        for key, value in thresholds.items():
            if key not in config:
                raise ValueError(f"unknown threshold: {key}")
            if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
                raise ValueError(f"threshold {key} must be finite")
            if key == "max_compute_seconds":
                if value <= 0:
                    raise ValueError("max_compute_seconds must be positive")
            elif not 0 <= value <= 1:
                raise ValueError(f"threshold {key} must be in [0, 1]")
            config[key] = float(value)

    if not isinstance(evidence_coverage, (int, float)) or isinstance(evidence_coverage, bool) or not math.isfinite(float(evidence_coverage)) or not 0 <= evidence_coverage <= 1:
        raise ValueError("evidence_coverage must be finite and in [0, 1]")
    if not isinstance(replay_hash_match, bool):
        raise ValueError("replay_hash_match must be boolean")

    metrics: dict[str, float | None] = {}
    for key in ("accuracy", "false_accept_rate", "counterexample_escape_rate"):
        value = benchmark_metrics.get(key)
        if value is not None and (
            not isinstance(value, (int, float)) or isinstance(value, bool)
            or not math.isfinite(float(value)) or not 0 <= value <= 1
        ):
            raise ValueError(f"benchmark metric {key} must be finite and in [0, 1]")
        metrics[key] = float(value) if value is not None else None
    if holdout_score is not None and (
        not isinstance(holdout_score, (int, float)) or isinstance(holdout_score, bool)
        or not math.isfinite(float(holdout_score)) or not 0 <= holdout_score <= 1
    ):
        raise ValueError("holdout_score must be finite and in [0, 1]")
    if compute_seconds is not None and (
        not isinstance(compute_seconds, (int, float)) or isinstance(compute_seconds, bool)
        or not math.isfinite(float(compute_seconds)) or compute_seconds < 0
    ):
        raise ValueError("compute_seconds must be finite and non-negative")
    metrics["holdout_score"] = float(holdout_score) if holdout_score is not None else None
    metrics["compute_seconds"] = float(compute_seconds) if compute_seconds is not None else None

    formal_status = str(formal_check.get("entailment_status", formal_check.get("status", "MISSING")))
    premise_status = str(formal_check.get("premise_consistency", "MISSING"))
    gates = {
        "premises_consistent": premise_status == "SAT",
        "formal_entailment_supported": formal_status == "ENTAILED_WITHIN_ENCODED_FRAGMENT",
        "evidence_coverage_threshold_met": evidence_coverage >= config["min_evidence_coverage"],
        "benchmark_accuracy_threshold_met": metrics["accuracy"] is not None and metrics["accuracy"] >= config["min_benchmark_accuracy"],
        "false_accept_rate_within_limit": metrics["false_accept_rate"] is not None and metrics["false_accept_rate"] <= config["max_false_accept_rate"],
        "counterexample_escape_rate_within_limit": metrics["counterexample_escape_rate"] is not None and metrics["counterexample_escape_rate"] <= config["max_counterexample_escape_rate"],
        "holdout_score_threshold_met": metrics["holdout_score"] is not None and metrics["holdout_score"] >= config["min_holdout_score"],
        "compute_budget_within_limit": metrics["compute_seconds"] is not None and metrics["compute_seconds"] <= config["max_compute_seconds"],
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
        "threshold_status": str(_POLICY["status"]),
        "hard_gates": gates,
        "failed_gates": failed_gates,
        "score_vector": {
            "formal_check": formal_status,
            "evidence_coverage": float(evidence_coverage),
            "benchmark_accuracy": metrics["accuracy"],
            "false_accept_rate": metrics["false_accept_rate"],
            "counterexample_escape_rate": metrics["counterexample_escape_rate"],
            "holdout_score": metrics["holdout_score"],
            "compute_seconds": metrics["compute_seconds"],
            "deterministic_replay": replay_hash_match,
        },
        "learning_status": "EVALUATION_ONLY_NO_WEIGHTS_UPDATED",
        "reward_boundary": "SAT alone, score alone, or a passing software test never establishes semantic truth and cannot promote VERIFIED status.",
    }
