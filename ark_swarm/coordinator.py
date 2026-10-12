"""Bounded coordinator connecting ARK-Swarm roles to the WANGA logic pipeline."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ark_swarm.logic_trader import canonical_hash, trade_logic
from ark_swarm.swarm_state import make_event, merge_event_sets, validation_credit
from logic_fractal.fragment_composer import compose_pair, validate_fragment
from logic_fractal.composer import load_contracts
from logic_proof.benchmark import run_formal_fixture_benchmark
from logic_proof.formalization_queue import queue_candidate_for_formalization


DEFAULT_TASK = (
    "Build a source-grounded fractal logic model by connecting evidence provenance, "
    "logical primitives, typed relations, recursive composition, verification, bounded "
    "agents, and model readiness. Select existing logic assets, assemble a candidate, "
    "keep source lineage, and reject unverified status promotion."
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _role(role_id: str, checks: Mapping[str, bool], details: Mapping[str, Any] | None = None) -> dict[str, Any]:
    normalized = {str(key): value is True for key, value in checks.items()}
    passed = bool(normalized) and all(normalized.values())
    return {
        "agent_id": role_id,
        "status": "PASS" if passed else "REVIEW",
        "passed": passed,
        "checks": normalized,
        "details": dict(details or {}),
    }


def _typed_composition_probe(root: Path) -> dict[str, Any]:
    fixture = read_json(root / "logic_fractal/data/typed_fragments_fixture.json")
    sources = fixture["source_registry"]
    by_id = {item["fragment_id"]: item for item in fixture["fragments"]}
    checks_base = [
        validate_fragment(fragment, sources)
        for fragment in fixture["fragments"]
    ]
    level_one = compose_pair(
        by_id["FL-OBSERVATION"], by_id["FL-RELATION-EXTRACT"], source_registry=sources
    )
    level_two = compose_pair(
        level_one["fragment"], by_id["FL-REVIEW"], source_registry=sources
    )
    replay = compose_pair(
        level_one["fragment"], by_id["FL-REVIEW"], source_registry=sources
    )
    candidate = level_two["fragment"]
    checks = {
        "all_fixture_fragments_validate": all(item.get("status") == "VALID_STRUCTURE" for item in checks_base),
        "two_scales_composed": level_one["fragment"]["scale"] == 1 and candidate["scale"] == 2,
        "all_source_ids_preserved": len(level_two["composition_trace"]["source_ids_preserved"]) == 3,
        "stable_replay_hash": candidate["model_hash"] == replay["fragment"]["model_hash"],
        "semantic_equivalence_not_established": candidate["composition"]["semantic_equivalence"] == "NOT_ESTABLISHED",
        "claim_status_not_promoted": all(claim.get("status") == "CANDIDATE" for claim in candidate["claims"]),
    }
    return {
        "probe_type": "SYNTHETIC_TYPED_FRAGMENT_COMPOSITION",
        "passed": all(checks.values()),
        "checks": checks,
        "level_one_hash": level_one["fragment"]["model_hash"],
        "level_two_hash": candidate["model_hash"],
        "source_ids_preserved": level_two["composition_trace"]["source_ids_preserved"],
        "semantic_status": "NOT_YET_VERIFIED",
        "limitation": "Fixture-only interface test. It is not evidence that the selected real-catalog package is semantically valid.",
    }


def _mirror_review(trader_output: Mapping[str, Any]) -> dict[str, Any]:
    package = trader_output["logic_package"]
    selected = package.get("composition_candidate")
    if not selected:
        return {
            "passed": False, "status": "BLOCKED_NO_COMPOSITION",
            "checks": {"composition_candidate_exists": False},
            "semantic_status": "NOT_YET_VERIFIED",
        }
    original_ids = list(selected.get("member_article_ids", []))
    mirror_ids = list(reversed(original_ids))
    original_sources = set(selected.get("source_refs", []))
    checks = {
        "candidate_has_two_or_more_members": len(original_ids) >= 2,
        "mirror_preserves_membership": set(mirror_ids) == set(original_ids),
        "source_lineage_preserved": original_sources == set(package.get("sources", []) and [s["id"] for s in package["sources"]]),
        "mirror_is_not_declared_truth": True,
    }
    return {
        "passed": all(checks.values()),
        "status": "COUNTER_READING_CANDIDATE",
        "original_member_ids": original_ids,
        "reversed_order_candidate": mirror_ids,
        "source_refs": sorted(original_sources),
        "checks": checks,
        "meaning_boundary": "Reversed order is a counter-reading candidate only; it does not assert inverse implication or semantic equivalence.",
        "semantic_status": "NOT_YET_VERIFIED",
    }


def build_cycle(
    task: str = DEFAULT_TASK,
    *,
    root: Path = ROOT,
    include_existing_agent_suite: bool = True,
) -> dict[str, Any]:
    """Run Logic Trader and the bounded swarm against repository-visible Logic Wiki data."""
    if not isinstance(task, str) or not task.strip():
        raise ValueError("task must be non-empty text")
    root = Path(root)
    catalog = read_json(root / "logic_wiki/data/articles.json")
    contracts = load_contracts(root / "logic_fractal/data/composition_rules.json")
    trader_output = trade_logic(
        task.strip(), catalog, contracts,
        max_depth=3, max_candidates=2000, top_assets=10, top_compositions=10
    )

    roles: list[dict[str, Any]] = []
    audit = trader_output["catalog_audit"]
    roles.append(_role("source-catalog-guard", {
        "unique_article_and_source_ids": audit["status"] == "PASS",
        "no_dangling_sources": audit["dangling_source_count"] == 0,
        "no_dangling_relations": audit["dangling_relation_count"] == 0,
    }, {"catalog_audit": audit}))

    logic_package = trader_output["logic_package"]
    formalization_queue_item = queue_candidate_for_formalization(logic_package)
    roles.append(_role("logic-trader", {
        "candidate_package_created": trader_output["status"] == "CANDIDATE_PACKAGE_ASSEMBLED",
        "package_has_members": bool(logic_package.get("member_articles")),
        "package_has_sources": bool(logic_package.get("sources")),
        "candidate_not_released": logic_package["status"] == "INTERNAL_CANDIDATE_NOT_RELEASED",
        "semantic_status_not_verified": logic_package["semantic_status"] == "NOT_YET_VERIFIED",
    }, {
        "package_id": logic_package["package_id"],
        "package_hash": trader_output["package_hash"],
        "member_ids": [item["id"] for item in logic_package["member_articles"]],
        "source_ids": [item["id"] for item in logic_package["sources"]],
        "candidate_composition_id": (logic_package.get("composition_candidate") or {}).get("candidate_id"),
    }))

    queue_source_ids = {
        source_id
        for claim in formalization_queue_item["candidate_claims"]
        for source_id in claim["source_refs"]
    }
    roles.append(_role("formalization-queue-gate", {
        "candidate_is_queued": formalization_queue_item["status"] in {"READY_FOR_FORMALIZATION", "BLOCKED_SOURCE_REVIEW"},
        "solver_not_run_without_formal_ast": formalization_queue_item["solver_execution_status"] == "NOT_RUN_NO_FORMAL_AST",
        "no_automatic_semantic_conversion": formalization_queue_item["automatic_semantic_conversion"] is False,
        "source_refs_resolve": formalization_queue_item["status"] == "READY_FOR_FORMALIZATION" and not formalization_queue_item["unresolved_sources"],
        "no_status_promotion": formalization_queue_item["semantic_status"] == "NOT_YET_VERIFIED",
    }, {
        "queue_item_id": formalization_queue_item["queue_item_id"],
        "status": formalization_queue_item["status"],
        "missing_fields": formalization_queue_item["missing_formal_fields"],
        "claim_count": len(formalization_queue_item["candidate_claims"]),
        "source_count": len(queue_source_ids),
        "solver_execution_status": formalization_queue_item["solver_execution_status"],
    }))

    provenance_errors = []
    source_ids = {source["id"] for source in catalog["sources"]}
    for article in logic_package["member_articles"]:
        missing = sorted(set(article.get("source_refs", [])) - source_ids)
        if not article.get("source_refs") or missing:
            provenance_errors.append({"article_id": article["id"], "missing_source_ids": missing,
                                      "has_any_source": bool(article.get("source_refs"))})
    package_source_ids = {source["id"] for source in logic_package["sources"]}
    expected_source_ids = {
        source_id for article in logic_package["member_articles"] for source_id in article.get("source_refs", [])
    }
    roles.append(_role("source-provenance-gate", {
        "every_member_has_resolved_sources": not provenance_errors,
        "package_source_union_preserved": expected_source_ids == package_source_ids,
    }, {"provenance_errors": provenance_errors, "source_count": len(package_source_ids)}))

    composition = trader_output["composition_graph"]
    roles.append(_role("fractal-composer", {
        "candidate_graph_built": composition["status"] == "CANDIDATE_MAP_BUILT_NOT_RELEASED",
        "candidate_compositions_exist": composition["candidate_composition_count"] > 0,
        "catalog_edges_not_treated_as_entailment": "not independently proven semantic entailment" in composition["source_boundary"],
    }, composition))

    formal_benchmark = None
    formal_benchmark_error = None
    try:
        formal_benchmark = run_formal_fixture_benchmark(root / "logic_proof/fixtures/formal_cases.json")
        formal_checks = {
            "fixture_suite_passes": formal_benchmark.get("status") == "PASS",
            "all_formal_fixtures_pass": formal_benchmark.get("passed_cases") == formal_benchmark.get("case_count"),
            "fixtures_not_mislabeled_as_real_world": "not source-grounded" in str(formal_benchmark.get("fixture_status", "")).lower(),
            "benchmark_keeps_verification_open": formal_benchmark.get("semantic_status") == "NOT_YET_VERIFIED",
        }
    except (RuntimeError, ValueError, OSError) as exc:
        formal_benchmark_error = f"{type(exc).__name__}: {exc}"
        formal_checks = {
            "fixture_suite_passes": False,
            "all_formal_fixtures_pass": False,
            "fixtures_not_mislabeled_as_real_world": True,
            "benchmark_keeps_verification_open": True,
        }
    roles.append(_role("formal-proof-fixture-gate", formal_checks, {
        "status": formal_benchmark.get("status") if formal_benchmark else "BLOCKED",
        "case_count": formal_benchmark.get("case_count") if formal_benchmark else 0,
        "passed_cases": formal_benchmark.get("passed_cases") if formal_benchmark else 0,
        "error": formal_benchmark_error,
        "semantic_status": "NOT_YET_VERIFIED",
        "limitation": "Synthetic formal fixtures test the adapter, not the truth of real Logic Trader candidates.",
    }))

    typed_probe = _typed_composition_probe(root)
    roles.append(_role("typed-fragment-composer", typed_probe["checks"], {
        "probe_type": typed_probe["probe_type"],
        "level_one_hash": typed_probe["level_one_hash"],
        "level_two_hash": typed_probe["level_two_hash"],
        "limitation": typed_probe["limitation"],
    }))

    mirror = _mirror_review(trader_output)
    roles.append(_role("mirror-counter-reader", mirror["checks"], {
        "status": mirror["status"],
        "original_member_ids": mirror.get("original_member_ids", []),
        "reversed_order_candidate": mirror.get("reversed_order_candidate", []),
        "meaning_boundary": mirror.get("meaning_boundary", ""),
    }))

    existing_suite = None
    if include_existing_agent_suite:
        from scripts.evaluate_logic_agent_bundle import run_evaluation
        existing_suite = run_evaluation()
        roles.append(_role("existing-six-agent-integration-suite", {
            "all_six_roles_pass": existing_suite.get("agent_count") == 6 and existing_suite.get("passed_agents") == 6,
            "suite_overall_pass": existing_suite.get("overall_status") == "PASS",
            "claims_not_auto_verified": "not establish correctness on arbitrary natural-language tasks" in " ".join(existing_suite.get("known_limits", [])),
        }, {
            "agent_count": existing_suite.get("agent_count"),
            "passed_agents": existing_suite.get("passed_agents"),
            "failed_agents": existing_suite.get("failed_agents"),
            "suite_status": existing_suite.get("overall_status"),
        }))

    cycle_id = "ARK-" + canonical_hash({
        "task": task.strip(),
        "catalog_hash": audit["catalog_sha256"],
        "logic_package_hash": trader_output["package_hash"],
        "include_existing_agent_suite": include_existing_agent_suite,
    })[:16]
    events = []
    for role in roles:
        events.append(make_event(
            cycle_id=cycle_id,
            agent_id=role["agent_id"],
            event_type="ROLE_RESULT",
            payload={
                "status": role["status"],
                "passed": role["passed"],
                "checks_hash": canonical_hash(role["checks"]),
                "details_hash": canonical_hash(role["details"]),
            },
        ))
    event_set = merge_event_sets(events)
    credit = validation_credit(roles)
    all_passed = all(role["passed"] for role in roles)

    model_candidate = {
        "schema_version": "wanga-logic-brain-candidate/1.0",
        "model_name": "WANGA Source-Grounded Logical Brain Candidate",
        "candidate_id": logic_package["package_id"],
        "status": "INTERNAL_CANDIDATE_NOT_RELEASED",
        "task_sha256": canonical_hash(task.strip()),
        "package_hash": trader_output["package_hash"],
        "logic_package": logic_package,
        "formalization_queue_item": formalization_queue_item,
        "composition_graph_summary": trader_output["composition_graph"],
        "typed_fixture_probe": typed_probe,
        "provenance_gate": next(role for role in roles if role["agent_id"] == "source-provenance-gate"),
        "mirror_review": mirror,
        "semantic_status": "NOT_YET_VERIFIED",
        "release_gate": {
            "automatically_released": False,
            "requires_real_source_review": True,
            "requires_formalization_queue_completion": True,
            "requires_semantic_benchmarks": True,
            "requires_counterexamples": True,
            "requires_independent_review": True,
            "decision": "BLOCKED_INTERNAL_CANDIDATE_ONLY",
        },
    }
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    report = {
        "schema_version": "ark-swarm-logic-trader-cycle/1.0",
        "generated_at_utc": now,
        "cycle_id": cycle_id,
        "status": "SWARM_CYCLE_PASS_CANDIDATE_BUILT" if all_passed else "SWARM_CYCLE_REVIEW",
        "execution_mode": "BOUNDED_LOCAL_DETERMINISTIC_COORDINATOR",
        "model_claim_boundary": (
            "These are deterministic software roles using the checked Logic Wiki and composition contracts; "
            "they are not separate biological connectomes or independent neural models. "
            "Candidate assembly and test passes do not prove semantic truth."
        ),
        "task": task.strip(),
        "agent_count": len(roles),
        "passed_agents": sum(1 for role in roles if role["passed"]),
        "failed_agents": sum(1 for role in roles if not role["passed"]),
        "agents": roles,
        "logic_trader": trader_output,
        "typed_fragment_probe": typed_probe,
        "formal_logic_fixture_benchmark": formal_benchmark or {
            "status": "BLOCKED",
            "error": formal_benchmark_error,
            "semantic_status": "NOT_YET_VERIFIED",
        },
        "formalization_queue_item": formalization_queue_item,
        "mirror_review": mirror,
        "existing_six_agent_suite": ({
            "status": existing_suite.get("overall_status"),
            "agent_count": existing_suite.get("agent_count"),
            "passed_agents": existing_suite.get("passed_agents"),
            "failed_agents": existing_suite.get("failed_agents"),
        } if existing_suite else {"status": "NOT_RUN_BY_REQUEST"}),
        "event_set": event_set,
        "shared_validation_credit": credit,
        "capability_boundaries": {
            "peer_to_peer_transport": "NOT_IMPLEMENTED",
            "network_crdt_sync": "NOT_IMPLEMENTED",
            "local_grow_only_event_set": "IMPLEMENTED",
            "external_llm_backend": "NOT_CONFIGURED",
            "connectome_execution": "NOT_IMPLEMENTED",
            "self_modifying_code": "NOT_IMPLEMENTED",
            "wix_write": "NOT_PERFORMED_BY_THIS_CYCLE",
            "logic_package_release": "BLOCKED_PENDING_SEMANTIC_BENCHMARKS_AND_REVIEW",
        },
        "next_actions": [
            "Add source-grounded formal cases; current seven-case Z3 suite is synthetic adapter validation only.",
            "Replace synthetic typed-fragment fixtures incrementally with source-reviewed logic fragments.",
            "Add task benchmark cases and negative/counterexample cases for the Logic Trader selection and composition outputs.",
            "Add a reviewer-gated acceptance registry before recursive composition may consume prior candidates.",
            "Implement network transport and distributed CRDT replication only after defining authentication, authorization and replay-conflict contracts.",
            "Connect an external model proposer only through explicit configuration and keep the deterministic source/evidence gate authoritative.",
        ],
        "semantic_status": "NOT_YET_VERIFIED",
    }
    return {
        "report": report,
        "model_candidate": model_candidate,
    }


def write_cycle(result: Mapping[str, Any], out_dir: Path) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = result["report"]
    candidate = result["model_candidate"]
    report_path = out_dir / "logic-trader-swarm-latest.json"
    candidate_path = out_dir / "logic-brain-candidate-latest.json"
    queue_path = out_dir / "logic-formalization-queue-latest.json"
    markdown_path = out_dir / "logic-trader-swarm-latest.md"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    candidate_path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# ARK-Swarm + Logic Trader — {report['generated_at_utc']}",
        "",
        f"- Cycle: `{report['cycle_id']}`",
        f"- Cycle status: **{report['status']}**",
        f"- Agents passing: **{report['passed_agents']}/{report['agent_count']}**",
        f"- Selected logic package: `{candidate['candidate_id']}`",
        f"- Candidate hash: `{candidate['package_hash']}`",
        f"- Semantic status: **{candidate['semantic_status']}**",
        f"- Formalization queue: `{candidate['formalization_queue_item']['queue_item_id']}` ({candidate['formalization_queue_item']['status']})",
        f"- Formal AST: **{candidate['formalization_queue_item']['solver_execution_status']}**",
        "",
        "## Agent results",
    ]
    lines += [f"- {role['agent_id']}: {role['status']}" for role in report["agents"]]
    lines += [
        "",
        "## Release boundary",
        "The candidate is internal only. Passing structural, composition, or synthetic fixture tests does not establish semantic correctness.",
        "",
        "## Next actions",
    ]
    lines += [f"- {item}" for item in report["next_actions"]]
    markdown_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "report": str(report_path.relative_to(ROOT)),
        "candidate": str(candidate_path.relative_to(ROOT)),
        "formalization_queue": str(queue_path.relative_to(ROOT)),
        "markdown": str(markdown_path.relative_to(ROOT)),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run ARK-Swarm + Logic Trader against WANGA source-grounded logic assets.")
    parser.add_argument("--task", default=None, help="Task text. Default comes from ark_swarm/examples/logic_trader_task.json.")
    parser.add_argument("--skip-existing-suite", action="store_true", help="Skip running the existing six-role suite.")
    parser.add_argument("--out-dir", default=str(ROOT / "research/reports/ark-swarm"))
    args = parser.parse_args(argv)
    if args.task:
        task = args.task
    else:
        payload = read_json(ROOT / "ark_swarm/examples/logic_trader_task.json")
        task = payload["task"]
    result = build_cycle(task, root=ROOT, include_existing_agent_suite=not args.skip_existing_suite)
    paths = write_cycle(result, Path(args.out_dir))
    report = result["report"]
    print(json.dumps({
        "status": report["status"],
        "cycle_id": report["cycle_id"],
        "agent_count": report["agent_count"],
        "passed_agents": report["passed_agents"],
        "failed_agents": report["failed_agents"],
        "logic_package_id": result["model_candidate"]["candidate_id"],
        "semantic_status": report["semantic_status"],
        "reports": paths,
    }, ensure_ascii=False, indent=2))
    return 0 if report["status"] == "SWARM_CYCLE_PASS_CANDIDATE_BUILT" else 2


if __name__ == "__main__":
    raise SystemExit(main())
