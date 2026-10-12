#!/usr/bin/env python3
"""Run a bounded integration test across WANGA's logic packages.

These are deterministic software agents/roles, not separate neural models.
The script exercises existing implementations, emits a machine-readable report,
and fails non-zero if a required invariant does not hold.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import sys
import traceback
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from logic_engine_v1.logic_kernel import gate_action, run_bundle
from logic_fractal.fragment_composer import FragmentError, compose_pair
from logic_model_builder_v1.builder import build_model, execute_model_artifact
from logic_model_builder_v1.logic_native_language import compile_lnl
from logic_model_builder_v1.providers import StructuredSpecProvider


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _scope_agent() -> dict[str, Any]:
    base = {
        "action": "typo_fix",
        "target": "approved-page-1",
        "allowed_actions": ["typo_fix"],
        "allowed_targets": ["approved-page-1"],
        "permission_granted": True,
        "publish": False,
        "publish_permission_granted": False,
        "evidence_complete": True,
    }
    allowed = gate_action(dict(base))
    out_of_scope = gate_action({**base, "action": "change_price"})
    incomplete = gate_action({**base, "evidence_complete": False})
    checks = {
        "allowed_within_scope": allowed.get("decision") == "ALLOW_WITHIN_DECLARED_SCOPE",
        "out_of_scope_denied": out_of_scope.get("decision") == "DENY",
        "incomplete_evidence_reviewed": incomplete.get("decision") == "REVIEW",
    }
    return {"passed": all(checks.values()), "checks": checks, "observed_decisions": {
        "allowed": allowed.get("decision"),
        "out_of_scope": out_of_scope.get("decision"),
        "incomplete_evidence": incomplete.get("decision"),
    }}


def _evidence_agent() -> dict[str, Any]:
    bundle = {
        "case_id": "MULTI-AGENT-EVIDENCE-001",
        "description": "Synthetic rule-premise eligibility and non-verification test.",
        "evidence": [{
            "id": "E-TEST-001", "source_uri": "fixture://multi-agent/evidence-001",
            "source_version": "fixture-v1", "location": "tests/test_multi_agent_logic_evaluation.py",
            "status": "TEST_FIXTURE"
        }],
        "claims": [
            {"id": "C-ELIGIBLE", "atom": {"subject":"request","predicate":"action","object":"typo_fix"},
             "epistemic_status":"TEST_FIXTURE","evidence_refs":["E-TEST-001"]},
            {"id": "C-UNSUPPORTED", "atom": {"subject":"request","predicate":"action","object":"change_price"},
             "epistemic_status":"TEST_FIXTURE","evidence_refs":[]}
        ],
        "rules": [{
            "id":"R-ACTION-CANDIDATE","status":"ACTIVE_SPECIFIED",
            "description":"The rule only derives a candidate from a source-referenced fixture.",
            "antecedents":[{"subject":"request","predicate":"action","object":"typo_fix"}],
            "consequent":{"subject":"action","predicate":"candidate","object":"typo_fix"},
            "source_refs":["fixture://multi-agent/rule-001"]
        }]
    }
    result = run_bundle(bundle)
    reports = {item["claim_id"]: item for item in result.get("input_claims", [])}
    derived = result.get("derived_claims", [])
    checks = {
        "valid_fixture_eligible": reports.get("C-ELIGIBLE", {}).get("engine_status") == "INPUT_ELIGIBLE_WITH_REFERENCED_EVIDENCE",
        "unsupported_claim_blocked": reports.get("C-UNSUPPORTED", {}).get("engine_status") == "UNSUPPORTED_NO_EVIDENCE",
        "derived_claim_exists": len(derived) == 1,
        "derived_claim_not_verified": len(derived) == 1 and derived[0].get("status") == "DERIVED_NOT_VERIFIED",
    }
    return {"passed": result.get("status") == "COMPLETED" and all(checks.values()), "checks": checks,
            "result_status": result.get("status"), "input_reports": reports,
            "derived_claim_count": len(derived), "unsupported_input_count": result.get("summary", {}).get("unsupported_or_ineligible_claims")}


def _lnl_builder_agent() -> dict[str, Any]:
    spec = read_json(ROOT / "logic_model_builder_v1" / "examples" / "site_change_spec.json")
    built = build_model(spec, StructuredSpecProvider(), max_attempts=3)
    if built.get("status") != "MODEL_BUILT_READY_FOR_REVIEW":
        return {"passed": False, "builder_status": built.get("status"), "attempt_log": built.get("attempt_log", [])}
    artifact = built["model_artifact"]
    runtime = execute_model_artifact(artifact, repo_root=ROOT)
    checks = {
        "compiler_accepted_candidate": artifact.get("status") == "COMPILED_FOR_REVIEW",
        "goal_reached": runtime.get("status") == "GOALS_MET",
        "runtime_completed": runtime.get("runtime_status") == "COMPLETED",
        "derived_claim_not_verified": all(
            claim.get("status") == "DERIVED_NOT_VERIFIED"
            for claim in runtime.get("inference", {}).get("derived_claims", [])
        ),
        "semantic_status_not_verified": built.get("semantic_status") == "NOT_YET_VERIFIED",
    }
    return {"passed": all(checks.values()), "checks": checks, "builder_status": built.get("status"),
            "attempt_count": built.get("attempt_count"), "runtime_status": runtime.get("runtime_status"),
            "goal_status": runtime.get("status"), "derived_claim_count": len(runtime.get("inference", {}).get("derived_claims", []))}


def _fractal_composer_agent() -> dict[str, Any]:
    fixture = read_json(ROOT / "logic_fractal" / "data" / "typed_fragments_fixture.json")
    sources = fixture["source_registry"]
    fragments = {item["fragment_id"]: item for item in fixture["fragments"]}
    first = compose_pair(fragments["FL-OBSERVATION"], fragments["FL-RELATION-EXTRACT"], source_registry=sources)
    second = compose_pair(first["fragment"], fragments["FL-REVIEW"], source_registry=sources)
    mismatch = json.loads(json.dumps(fragments["FL-REVIEW"]))
    mismatch["inputs"] = [{"name":"candidate","type":"UnrelatedType","required":True}]
    blocked = False
    try:
        compose_pair(fragments["FL-OBSERVATION"], mismatch, source_registry=sources)
    except FragmentError:
        blocked = True
    candidate = second["fragment"]
    checks = {
        "first_scale_composed": first["fragment"]["scale"] == 1,
        "recursive_scale_composed": candidate["scale"] == 2,
        "parentage_preserved": first["fragment"]["fragment_id"] in candidate["composition"]["parent_ids"],
        "semantics_not_claimed": candidate["composition"]["semantic_equivalence"] == "NOT_ESTABLISHED",
        "type_mismatch_blocked": blocked,
        "claim_status_downgraded_to_candidate": all(c["status"] == "CANDIDATE" for c in candidate["claims"]),
    }
    return {"passed": all(checks.values()), "checks": checks, "scale_1_id": first["fragment"]["fragment_id"],
            "scale_2_id": candidate["fragment_id"], "scale_2_hash": candidate["model_hash"],
            "claim_count": len(candidate["claims"]), "semantic_equivalence": candidate["composition"]["semantic_equivalence"]}


def _wiki_curator_agent() -> dict[str, Any]:
    catalog = read_json(ROOT / "logic_wiki" / "data" / "articles.json")
    articles = catalog.get("articles", [])
    sources = catalog.get("sources", [])
    article_ids = {article.get("id") for article in articles}
    source_ids = {source.get("id") for source in sources}
    dangling_relations = []
    dangling_sources = []
    for article in articles:
        dangling_relations.extend((article.get("id"), target) for target in article.get("relations", []) if target not in article_ids)
        dangling_sources.extend((article.get("id"), source) for source in article.get("sources", []) if source not in source_ids)
    ids = [article.get("id") for article in articles]
    source_list = [source.get("id") for source in sources]
    checks = {
        "articles_have_unique_ids": len(ids) == len(set(ids)),
        "sources_have_unique_ids": len(source_list) == len(set(source_list)),
        "relations_resolve": not dangling_relations,
        "sources_resolve": not dangling_sources,
        "catalog_nonempty": bool(articles) and bool(sources),
    }
    return {"passed": all(checks.values()), "checks": checks, "article_count": len(articles),
            "source_count": len(sources), "dangling_relations": dangling_relations[:20], "dangling_sources": dangling_sources[:20],
            "catalog_sha256": _hash(catalog)}


def _rejection_agent() -> dict[str, Any]:
    path = ROOT / "logic_model_builder_v1" / "examples" / "site_change.lnl"
    source = path.read_text(encoding="utf-8").replace("evidence=E_REQUEST", "evidence=E_DOES_NOT_EXIST", 1)
    artifact = compile_lnl(source)
    codes = {item.get("code") for item in artifact.get("diagnostics", [])}
    checks = {
        "invalid_source_candidate_rejected": artifact.get("status") == "REJECTED",
        "missing_source_reason_returned": "MISSING_SOURCE_REFERENCE" in codes,
        "no_execution_bundle_on_rejection": artifact.get("execution_bundle") is None,
    }
    return {"passed": all(checks.values()), "checks": checks, "artifact_status": artifact.get("status"),
            "diagnostic_codes": sorted(c for c in codes if c)}


AGENTS: list[tuple[str, Callable[[], dict[str, Any]]]] = [
    ("scope-binder-action-gate", _scope_agent),
    ("evidence-gatekeeper", _evidence_agent),
    ("lnl-model-builder-runtime", _lnl_builder_agent),
    ("recursive-fractal-composer", _fractal_composer_agent),
    ("wiki-source-curator", _wiki_curator_agent),
    ("adversarial-source-rejection", _rejection_agent),
]


def run_evaluation() -> dict[str, Any]:
    results = []
    for name, execute in AGENTS:
        try:
            result = execute()
            passed = result.get("passed") is True
            results.append({"agent": name, "status": "PASS" if passed else "FAIL", "result": result})
        except Exception as exc:
            results.append({"agent": name, "status": "ERROR", "error": f"{type(exc).__name__}: {exc}",
                            "traceback": traceback.format_exc(limit=5)})
    passed_count = sum(item["status"] == "PASS" for item in results)
    report = {
        "schema_version": "wanga-agent-evaluation/1.0",
        "generated_date_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "test_type": "DETERMINISTIC_MULTI_ROLE_INTEGRATION_EVALUATION",
        "model_claim_boundary": "These are deterministic software roles, not separate neural models. A pass validates only the tested code paths and synthetic fixtures.",
        "agent_count": len(results),
        "passed_agents": passed_count,
        "failed_agents": len(results) - passed_count,
        "overall_status": "PASS" if passed_count == len(results) else "FAIL",
        "agent_results": results,
        "known_limits": [
            "The structured provider is not an LLM; no external model endpoint was called.",
            "Fixtures are synthetic and do not establish correctness on arbitrary natural-language tasks.",
            "A composed fractal is a candidate structure; type compatibility does not prove semantic equivalence.",
            "The evidence gate validates referenced evidence structure, not source authenticity.",
        ],
        "next_test_batch": [
            "Add source-grounded positive/negative/ambiguous natural-language benchmark cases.",
            "Compare deterministic outputs across different configured LLM providers, if explicitly configured.",
            "Measure false accepts and false rejects for each agent role.",
        ],
    }
    return report


def main() -> int:
    report = run_evaluation()
    out = ROOT / "research" / "reports" / "agent-evaluation" / "multi-agent-evaluation-latest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"overall_status": report["overall_status"], "agent_count": report["agent_count"],
                      "passed_agents": report["passed_agents"], "failed_agents": report["failed_agents"],
                      "report": str(out.relative_to(ROOT)),
                      "agents": [{"agent": item["agent"], "status": item["status"]} for item in report["agent_results"]]},
                     ensure_ascii=False))
    return 0 if report["overall_status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
