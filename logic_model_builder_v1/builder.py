"""Candidate -> compile -> critique -> refine -> executable artifact pipeline."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from .logic_native_language import compile_lnl
from .providers import ProposalProvider


def build_model(
    specification: Mapping[str, Any],
    provider: ProposalProvider,
    *,
    max_attempts: int = 3,
) -> dict[str, Any]:
    """Ask a proposal provider for LNL, then apply the deterministic compiler/critic.

    A valid result is still a model candidate for review, not a verified model.
    """
    if max_attempts < 1 or max_attempts > 5:
        raise ValueError("max_attempts must be between 1 and 5")
    critique: list[dict[str, Any]] = []
    attempt_log: list[dict[str, Any]] = []
    latest_candidate = ""
    latest_artifact: dict[str, Any] | None = None

    for attempt in range(1, max_attempts + 1):
        candidate = provider.propose(specification, critique, attempt)
        latest_candidate = candidate
        artifact = compile_lnl(candidate)
        diagnostics = artifact.get("diagnostics", [])
        errors = [d for d in diagnostics if d.get("severity") == "ERROR"]
        warnings = [d for d in diagnostics if d.get("severity") == "WARNING"]
        attempt_log.append({
            "attempt": attempt,
            "provider": provider.name,
            "candidate_sha256": hashlib.sha256(candidate.encode("utf-8")).hexdigest(),
            "compile_status": artifact.get("status"),
            "errors": errors,
            "warnings": warnings,
        })
        latest_artifact = artifact
        if artifact.get("status") == "COMPILED_FOR_REVIEW" and not errors:
            return {
                "builder": "WANGA Logic Model Builder V1",
                "status": "MODEL_BUILT_READY_FOR_REVIEW",
                "provider": provider.name,
                "attempt_count": attempt,
                "attempt_log": attempt_log,
                "model_artifact": artifact,
                "semantic_status": "NOT_YET_VERIFIED",
                "next_gate": "Review sources, run bounded inference, and execute acceptance tests before approval or publication.",
            }
        critique = errors or diagnostics

    return {
        "builder": "WANGA Logic Model Builder V1",
        "status": "MODEL_BUILD_BLOCKED",
        "provider": provider.name,
        "attempt_count": len(attempt_log),
        "attempt_log": attempt_log,
        "last_candidate": latest_candidate,
        "model_artifact": latest_artifact,
        "semantic_status": "NOT_YET_VERIFIED",
        "next_gate": "Resolve compiler/critic errors. Invalid models cannot be executed or published.",
    }


def execute_model_artifact(
    artifact: Mapping[str, Any],
    *,
    repo_root: str | Path,
    use_corpus: bool = True,
) -> dict[str, Any]:
    """Execute only a compiler-approved artifact using the existing WANGA kernel."""
    if artifact.get("status") != "COMPILED_FOR_REVIEW":
        raise ValueError("Only COMPILED_FOR_REVIEW artifacts may be executed.")
    bundle = artifact.get("execution_bundle")
    if not isinstance(bundle, Mapping):
        raise ValueError("Compiled artifact has no execution bundle.")

    try:
        from logic_engine_v1.logic_kernel import load_corpus_context, run_bundle
    except ImportError as exc:
        raise RuntimeError("WANGA logic_engine_v1 is required to execute this artifact.") from exc

    corpus = load_corpus_context(repo_root) if use_corpus else None
    inference = run_bundle(bundle, corpus_context=corpus)
    goals = artifact.get("goals", [])
    facts = inference.get("facts", [])
    unmet_goals = []
    for goal in goals:
        reached = any(
            fact.get("atom", {}).get("subject") == goal.get("subject")
            and fact.get("atom", {}).get("predicate") == goal.get("predicate")
            and fact.get("atom", {}).get("object") == goal.get("object")
            and fact.get("atom", {}).get("polarity", True) == goal.get("polarity", True)
            for fact in facts
        )
        if not reached:
            unmet_goals.append(goal)
    success = inference.get("status") == "COMPLETED" and not unmet_goals
    return {
        "model": artifact.get("model_name"),
        "status": "GOALS_MET" if success else "GOALS_NOT_MET_OR_REVIEW_REQUIRED",
        "runtime_status": inference.get("status"),
        "goals": goals,
        "unmet_goals": unmet_goals,
        "inference": inference,
        "epistemic_boundary": "Goal satisfaction under a bounded rule set is not independent truth verification.",
    }
