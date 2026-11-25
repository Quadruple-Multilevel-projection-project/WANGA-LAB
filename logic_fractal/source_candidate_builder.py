from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .fragment_composer import FragmentError, compose_pair, content_hash, validate_fragment

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "logic_fractal" / "data" / "source_backed_fragments_v1.json"
RULES_PATH = ROOT / "logic_fractal" / "data" / "composition_rules.json"
DEFAULT_OUTPUT = ROOT / "research" / "reports" / "logic-fractal" / "source-backed-gate13-candidate.json"


def build_candidate_artifact(
    fixture: dict[str, Any] | None = None,
    rules_document: dict[str, Any] | None = None,
) -> dict[str, Any]:
    fixture = fixture or json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    rules_document = rules_document or json.loads(RULES_PATH.read_text(encoding="utf-8"))

    source_registry = fixture["source_registry"]
    fragments = {item["fragment_id"]: item for item in fixture["fragments"]}
    plan = fixture["composition_plan"]
    rule_id = plan["rule_id"]
    rule = next((item for item in rules_document["rules"] if item["id"] == rule_id), None)
    if rule is None:
        raise FragmentError(f"composition rule is not registered: {rule_id}")
    if rule.get("status") != "ACTIVE_SPECIFIED":
        raise FragmentError(f"composition rule is not active/specifed: {rule_id}")

    parent_ids = plan["parents"]
    if len(parent_ids) != 2 or any(parent_id not in fragments for parent_id in parent_ids):
        raise FragmentError("composition plan must reference exactly two existing parent fragments")

    parents = [fragments[parent_id] for parent_id in parent_ids]
    base_results = [validate_fragment(parent, source_registry) for parent in parents]
    if any(result.get("status") != "VALID_STRUCTURE" for result in base_results):
        raise FragmentError("one or more source-backed parent fragments failed structural validation")

    first, second = parents
    composed = compose_pair(
        first,
        second,
        source_registry=source_registry,
        composition_rule_id=rule_id,
    )
    replay = compose_pair(
        first,
        second,
        source_registry=source_registry,
        composition_rule_id=rule_id,
    )
    trace = composed["composition_trace"]
    replay_trace = replay["composition_trace"]
    expected_sources = sorted({
        provenance["source_id"]
        for parent in parents
        for provenance in parent.get("provenance", [])
    })
    source_lineage_ok = sorted(trace["source_ids_preserved"]) == expected_sources
    parent_ids_ok = trace["parent_ids"] == parent_ids
    interface_match_ok = bool(trace["matched_interfaces"]) and not trace["unmatched_optional_inputs"]
    deterministic_ok = (
        composed["fragment"]["model_hash"] == replay["fragment"]["model_hash"]
        and trace == replay_trace
    )
    semantic_equivalence = composed["fragment"]["composition"].get("semantic_equivalence", "NOT_ESTABLISHED")

    artifact: dict[str, Any] = {
        "schema_version": "source-backed-fractal-candidate/1.0",
        "candidate_id": composed["fragment"]["fragment_id"],
        "status": "CANDIDATE_NOT_RELEASED",
        "source_registry": source_registry,
        "parent_fragments": parents,
        "composition_rule": {
            "id": rule_id,
            "status": rule["status"],
            "git_blob_sha": None,
        },
        "composition": composed,
        "scope": fixture["scope"],
        "non_applicability": fixture["non_applicability"],
        "invariants": {
            "parent_ids_preserved": parent_ids_ok,
            "source_lineage_preserved": source_lineage_ok,
            "required_interface_type_match": interface_match_ok,
            "semantic_equivalence": semantic_equivalence,
            "no_verified_promotion": composed["fragment"].get("status") == "CANDIDATE",
        },
        "test_outcomes": {
            "base_fragment_structural_validation": "PASS",
            "typed_composition": "PASS" if composed.get("status") == "COMPOSITION_CANDIDATE_READY_FOR_TESTS" else "FAIL",
            "deterministic_rebuild": "PASS" if deterministic_ok else "FAIL",
            "source_lineage": "PASS" if source_lineage_ok else "FAIL",
            "semantic_ground_truth": "NOT_RUN",
            "holdout": "NOT_CREATED",
            "independent_mirror_review": "NOT_ADJUDICATED",
        },
        "counterexample_candidates": fixture["counterexample_candidates"],
        "semantic_benchmark_candidates": fixture["semantic_benchmark_candidates"],
        "readiness_contribution": {
            "source_grounded_counterexamples_counted": 0,
            "semantic_benchmark_cases_counted": 0,
            "reason": "Candidates are not independently adjudicated and therefore do not count toward the FIRST_MODEL_ALPHA gate.",
        },
        "semantic_status": "NOT_YET_VERIFIED",
        "release_decision": "BLOCKED_PENDING_EDITION_CHECK_SEMANTIC_BENCHMARKS_HOLDOUT_AND_INDEPENDENT_REVIEW",
    }
    artifact["artifact_hash"] = content_hash(artifact)
    return artifact


def write_candidate_artifact(output_path: Path | None = None) -> dict[str, Any]:
    artifact = build_candidate_artifact()
    target = output_path or DEFAULT_OUTPUT
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return artifact
