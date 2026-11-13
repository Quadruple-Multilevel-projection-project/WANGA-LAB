#!/usr/bin/env python3
"""Run bounded deterministic research roles over repository-visible Logic Wiki data."""
from __future__ import annotations
import datetime, hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from logic_fractal.composer import build_candidate_model, load_contracts
from logic_fractal.readiness import is_readiness_eligible

def read(path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def source_span_gap_message(actual, required):
    """Describe the observed source-span count without stale zero-unit claims."""
    missing = max(0, required - actual)
    if actual == 0:
        return "No admitted source-span logic units are registered; %s are required." % required
    if missing:
        return "%s admitted source-span logic units are registered; %s more are required to reach %s." % (actual, missing, required)
    return "%s admitted source-span logic units are registered; configured threshold %s is met." % (actual, required)

def main():
    catalog = read(ROOT / "logic_wiki/data/articles.json")
    gate = read(ROOT / "logic_wiki/data/readiness_gate.json")
    contracts = load_contracts(ROOT / "logic_fractal/data/composition_rules.json")
    wix_manifest = read(ROOT / "logic_wiki/data/wix_sync_manifest.json", {})
    evidence_dir = ROOT / "research/inbox/conversations"
    inbox_files = sorted(p for p in evidence_dir.rglob("*.json") if p.is_file()) if evidence_dir.exists() else []
    imported, intake_errors = [], []
    for path in inbox_files:
        try:
            data = read(path, {})
            if not data.get("record_id") or not data.get("segments") or not data.get("source_type"):
                intake_errors.append({"file": str(path.relative_to(ROOT)), "status": "BLOCKED_INVALID_INTAKE_SCHEMA"})
            else:
                raw = path.read_bytes()
                imported.append({"record_id": data["record_id"], "file": str(path.relative_to(ROOT)),
                                 "sha256": hashlib.sha256(raw).hexdigest(), "segment_count": len(data["segments"]),
                                 "status": "REGISTERED_NOT_SEMANTICALLY_VERIFIED"})
        except Exception as exc:
            intake_errors.append({"file": str(path.relative_to(ROOT)), "status": "FAILED_PARSE", "reason": str(exc)})

    contracts_path = ROOT / "logic_fractal/data/composition_rules.json"
    model_a = build_candidate_model(catalog, contracts)
    model_b = build_candidate_model(read(ROOT / "logic_wiki/data/articles.json"), load_contracts(contracts_path))
    deterministic_rebuild = sha(model_a) == sha(model_b)

    articles, sources = catalog.get("articles", []), catalog.get("sources", [])
    source_ids, article_ids = [x.get("id") for x in sources], [x.get("id") for x in articles]
    source_id_set, article_id_set = set(source_ids), set(article_ids)
    dangling_sources = sorted({ref for article in articles for ref in article.get("sources", []) if ref not in source_id_set})
    dangling_relations = sorted({f"{article.get('id')}->{ref}" for article in articles for ref in article.get("relations", []) if ref not in article_id_set})
    duplicate_source_ids = len(source_ids) - len(source_id_set)
    duplicate_article_ids = len(article_ids) - len(article_id_set)
    source_classes = sorted({str(x.get("type", "UNCLASSIFIED")) for x in sources})
    source_linked_articles = sum(1 for article in articles if article.get("sources"))
    logic_unit_registry = read(ROOT / "logic_fractal/data/logic_units.json", {"units": []})
    logic_units = logic_unit_registry.get("units", [])
    source_by_id = {item.get("id"): item for item in sources}
    logic_unit_errors, unit_ids, span_ids = [], [], []
    valid_logic_units = 0
    excluded_test_fixture_units = 0
    required_unit_fields = ("unit_id", "source_span_id", "source_id", "source_version", "source_uri",
                            "exact_locator", "literal_excerpt", "language", "permission_scope")
    for unit in logic_units:
        if not isinstance(unit, dict):
            logic_unit_errors.append("Logic unit record must be an object.")
            continue
        missing = [field for field in required_unit_fields
                   if not isinstance(unit.get(field), str) or not unit.get(field).strip()]
        if missing:
            logic_unit_errors.append("Logic unit %r missing provenance fields: %s." %
                                     (unit.get("unit_id"), ", ".join(missing)))
            continue
        uid, span_id = unit["unit_id"], unit["source_span_id"]
        if uid in unit_ids or span_id in span_ids:
            logic_unit_errors.append("Duplicate logic unit or source span ID: %s / %s." % (uid, span_id))
            continue
        unit_ids.append(uid)
        span_ids.append(span_id)
        source_record = source_by_id.get(unit["source_id"])
        if source_record is None or unit["source_uri"] != source_record.get("uri"):
            logic_unit_errors.append("Logic unit %s has an unresolved source ID/URI." % uid)
            continue
        if not is_readiness_eligible(unit, source_record):
            excluded_test_fixture_units += 1
            continue
        valid_logic_units += 1
    units_with_provenance = valid_logic_units
    typed_candidate_artifact = read(ROOT / "research/reports/logic-fractal/source-grounded-fractal-candidates.json", {"candidates": []})
    typed_candidates = typed_candidate_artifact.get("candidates", [])
    active_contracts = [r for r in contracts if str(r.get("status", "")).startswith("ACTIVE") and r.get("inputs") and r.get("output") and r.get("invariants")]

    counterexample_data = read(ROOT / "logic_fractal/data/counterexamples.json", {"cases": []})
    semantic_benchmark = read(ROOT / "logic_fractal/data/semantic_benchmark_cases.json", {"cases": []})
    benchmark_suites = read(ROOT / "logic_fractal/data/benchmark_suites.json", {"suites": []})
    review_dir = ROOT / "research/reports/logic-fractal/reviews"
    reviews = []
    if review_dir.exists():
        for path in sorted(review_dir.glob("*.json")):
            try:
                item = read(path, {})
                if item.get("review_type") == "INDEPENDENT_REVIEW" and item.get("reviewer") and item.get("status") in {"PASS", "REVIEW", "FAIL"}:
                    reviews.append({"file": str(path.relative_to(ROOT)), "status": item["status"], "reviewer": item["reviewer"]})
            except Exception:
                pass
    contradiction_path = ROOT / "logic_fractal/data/core_contradictions.json"
    unresolved_contradictions = read(contradiction_path, None)
    contradiction_inventory_available = unresolved_contradictions is not None
    critical_contradictions = None if unresolved_contradictions is None else sum(
        1 for item in unresolved_contradictions.get("items", [])
        if item.get("critical") is True and item.get("resolved") is not True
    )

    thresholds = gate.get("thresholds", {})
    metrics = {
        "source_records": len(sources), "source_classes": len(source_classes),
        "source_linked_articles": source_linked_articles, "logic_units_with_provenance": units_with_provenance,
        "logic_unit_registry_errors": len(logic_unit_errors), "test_fixture_logic_units_excluded": excluded_test_fixture_units,
        "composition_rules_with_contracts": len(active_contracts), "typed_composition_candidates": len(typed_candidates),
        "counterexample_cases": len(counterexample_data.get("cases", [])),
        "semantic_test_cases": len(semantic_benchmark.get("cases", [])),
        "benchmark_suites": len(benchmark_suites.get("suites", [])),
        "independent_review_cycles": len(reviews),
        "unresolved_dangling_source_refs": len(dangling_sources),
        "unresolved_dangling_relation_refs": len(dangling_relations),
        "unresolved_duplicate_stable_ids": duplicate_source_ids + duplicate_article_ids,
        "critical_core_contradictions": critical_contradictions,
        "contradiction_inventory_available": contradiction_inventory_available,
        "deterministic_build": deterministic_rebuild,
        "holdout_split_available": (ROOT / "logic_fractal/data/holdout_manifest.json").exists(),
        "mirror_review_available": len(reviews) > 0
    }
    requirements = {
        "source_records": thresholds.get("min_source_records", 20),
        "source_classes": thresholds.get("min_source_classes", 3),
        "logic_units_with_provenance": thresholds.get("min_logic_units_with_provenance", 50),
        "composition_rules_with_contracts": thresholds.get("min_composition_rules_with_contracts", 20),
        "counterexample_cases": thresholds.get("min_counterexample_cases", 30),
        "semantic_test_cases": thresholds.get("min_test_cases", 100),
        "benchmark_suites": thresholds.get("min_benchmark_suites", 3),
        "independent_review_cycles": thresholds.get("min_independent_review_cycles", 2)
    }
    deficits = []
    for name, required in requirements.items():
        actual = metrics[name]
        if actual < required:
            deficits.append({"gate": name, "actual": actual, "required": required, "missing": required - actual})
    if logic_unit_errors:
        deficits.append({"gate": "logic_unit_registry_validation", "actual": len(logic_unit_errors), "required": 0})
    for name in ("unresolved_dangling_source_refs", "unresolved_dangling_relation_refs", "unresolved_duplicate_stable_ids"):
        if metrics[name] != 0:
            deficits.append({"gate": name, "actual": metrics[name], "required": 0})
    if critical_contradictions is None:
        deficits.append({"gate": "critical_core_contradictions", "actual": "NOT_MEASURED_NO_INVENTORY", "required": 0})
    elif critical_contradictions != 0:
        deficits.append({"gate": "critical_core_contradictions", "actual": critical_contradictions, "required": 0})
    if thresholds.get("deterministic_build_required") and not deterministic_rebuild:
        deficits.append({"gate": "deterministic_build", "actual": False, "required": True})
    if thresholds.get("holdout_split_required") and not metrics["holdout_split_available"]:
        deficits.append({"gate": "holdout_split", "actual": False, "required": True})
    if thresholds.get("mirror_review_required") and not metrics["mirror_review_available"]:
        deficits.append({"gate": "independent_mirror_review", "actual": False, "required": True})

    edge_set = {(edge["source"], edge["target"]) for edge in model_a["graph"]["edges"]}
    reciprocal = []
    for left, right in sorted(edge_set):
        if left != right and (right, left) in edge_set:
            reciprocal.append({"pair": [left, right], "status": "RECIPROCAL_EDGE_REVIEW_CANDIDATE"})

    agents = [
        {"agent": "conversation-collector", "status": "COMPLETED_WITH_NO_EXPORTS" if not imported and not intake_errors else ("COMPLETED" if not intake_errors else "REVIEW"), "record_count": len(imported), "errors": intake_errors, "boundary": "Only repository-visible exports are scanned; private chat history is not fetched automatically."},
        {"agent": "source-registrar", "status": "PASS" if not dangling_sources and not duplicate_source_ids else "FAIL", "source_records": len(sources), "source_classes": len(source_classes), "dangling_source_refs": dangling_sources, "duplicate_source_ids": duplicate_source_ids},
        {"agent": "logic-extractor", "status": "NO_LOGIC_UNITS_REGISTERED" if not logic_units else ("COMPLETED" if not logic_unit_errors else "REVIEW"),
         "unit_records": len(logic_units), "valid_units_with_provenance": units_with_provenance,
         "errors": logic_unit_errors, "conversation_exports": len(imported), "semantic_status": "NOT_YET_VERIFIED"},
        {"agent": "logic-normalizer", "status": "COMPLETED" if not dangling_relations else "REVIEW", "article_nodes": len(model_a["graph"]["nodes"]), "declared_editorial_edges": len(model_a["graph"]["edges"]), "dangling_relations": dangling_relations, "semantic_status": "EDITORIAL_STRUCTURAL_MAP_ONLY"},
        {"agent": "fractal-pattern-miner", "status": "CANDIDATE_MAP_BUILT", "taxonomy_levels": 4, "catalog_hash": sha(catalog), "candidate_substructures": model_a.get("candidate_composition_count", 0), "semantic_status": "STRUCTURAL_CANDIDATES"},
        {"agent": "fractal-composer", "status": "COMPLETED", "candidate_compositions": model_a.get("candidate_composition_count", 0), "active_contract_count": len(active_contracts), "status_contract": "CANDIDATE_COMPOSITION_NOT_SEMANTICALLY_VERIFIED"},
        {"agent": "typed-fractal-composer", "status": "CANDIDATE_COMPOSITIONS_BUILT" if typed_candidates else "BLOCKED_NO_TYPED_CANDIDATE_ARTIFACT", "candidate_count": len(typed_candidates), "candidate_hash": typed_candidate_artifact.get("model_hash"), "semantic_status": "NOT_YET_VERIFIED", "note": "Exact typed-interface compatibility and provenance only; no semantic entailment is claimed."},
        {"agent": "mirror-reviewer", "status": "REVIEW_REQUIRED" if not reviews else "REVIEW_LOG_PRESENT", "reciprocal_edge_candidates": reciprocal, "independent_review_count": len(reviews), "note": "Reciprocal links are review candidates, not proof of logical equivalence."},
        {"agent": "benchmark-evaluator", "status": "BLOCKED_NO_GROUNDED_BENCHMARKS" if not semantic_benchmark.get("cases") else "BENCHMARK_CASES_REGISTERED", "semantic_test_cases": len(semantic_benchmark.get("cases", [])), "benchmark_suites": len(benchmark_suites.get("suites", [])), "note": "Unit tests validate software contracts; they do not count as semantic ground-truth cases."},
        {"agent": "readiness-gatekeeper", "status": "NOT_READY_INTERNAL_CANDIDATE_ONLY" if deficits else "READY_FOR_HUMAN_REVIEW", "metrics": metrics, "deficits": deficits, "threshold_policy": gate.get("status", "NOT_RECORDED")},
        {"agent": "wiki-curator", "status": "READY_FOR_REVIEW", "articles": len(articles), "sources": len(sources), "taxonomy_status": "EDITORIAL_RELATIONS_NOT_ENTAILMENT"},
        {"agent": "wix-sync-auditor", "status": "READ_BACK_VERIFIED" if wix_manifest.get("status") == "READ_BACK_VERIFIED" else ("PARTIAL_READ_BACK_REQUIRES_FURTHER_CHECK" if wix_manifest.get("status") == "PUBLISHED_READ_BACK_PARTIAL" else "BLOCKED_OR_STALE_MANIFEST"), "last_sync_date": wix_manifest.get("last_sync_date"), "synced_articles": wix_manifest.get("synced_article_count", 0), "live_write_performed_by_this_cycle": False, "note": "GitHub runner has no Wix credentials; connected Wix sync must be performed separately and read back."},
        {"agent": "report-publisher", "status": "REPORT_GENERATED", "wix_write_performed": False, "note": "This run records status and artifacts; it does not perform a Wix deployment."}
    ]
    operational_pass = not intake_errors and not logic_unit_errors and not dangling_sources and not dangling_relations and not duplicate_source_ids and not duplicate_article_ids and deterministic_rebuild
    readiness = "NOT_READY_INTERNAL_CANDIDATE_ONLY" if deficits else "CANDIDATE_RELEASE_READY_FOR_HUMAN_REVIEW"
    report = {
        "date": datetime.date.today().isoformat(), "run_status": "PASS" if operational_pass else "REVIEW",
        "research_scope": "repository-visible catalog and explicitly supplied conversation exports",
        "access_boundary": "No automatic access to unavailable private ChatGPT history. Add an explicit export through the private intake utility, review/redact, then commit only approved derivatives.",
        "catalog_hash": sha(catalog), "agent_count": len(agents), "agents": agents,
        "source_coverage": {"source_records": len(sources), "source_classes": len(source_classes), "classes": source_classes,
                            "article_count": len(articles), "source_linked_articles": source_linked_articles,
                            "logic_units_with_provenance": units_with_provenance},
        "conversation_records_ingested": imported,
        "model_candidate": {"hash": sha(model_a), "status": "CANDIDATE_NOT_RELEASED", "deterministic_rebuild": deterministic_rebuild, "candidate_composition_count": model_a.get("candidate_composition_count", 0), "typed_composition_candidate_count": len(typed_candidates), "typed_composition_hash": typed_candidate_artifact.get("model_hash")},
        "first_model_gate": readiness, "readiness_metrics": metrics, "readiness_deficits": deficits,
        "wix_sync": {"manifest_status": wix_manifest.get("status", "NOT_RECORDED"), "last_sync_date": wix_manifest.get("last_sync_date"), "current_cycle_write_performed": False, "note": "Wix is updated only through the connected authorized tool followed by read-back."},
        "open_gaps": [
            "Scheduled jobs cannot fetch private ChatGPT history; they scan only explicit repository-visible export records.",
            "Semantic benchmark cases, named benchmark suites, a holdout manifest and independent review logs are not yet registered.",
            "A core-contradiction inventory is required before zero unresolved critical contradictions can be claimed.",
            "The L0-L3 fractal taxonomy is a research contract; recursive composition semantics remain partly specified and not empirically validated.",
            source_span_gap_message(units_with_provenance, thresholds.get("min_logic_units_with_provenance", 50))
        ]
    }
    out = ROOT / "logic_wiki/generated/agent_cycle_report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ROOT / "logic_wiki/generated/agent_cycle_report.md"
    lines = [
        f"# Logic Fractal Agent Cycle — {report['date']}", "",
        f"- Operational run: **{report['run_status']}**",
        f"- Model readiness: **{readiness}**",
        f"- Wiki articles / sources / source classes: **{len(articles)} / {len(sources)} / {len(source_classes)}**",
        f"- Conversation exports ingested this run: **{len(imported)}**",
        f"- Executed agent roles: **{len(agents)}**",
        f"- Candidate compositions: **{model_a.get('candidate_composition_count', 0)}**",
        f"- Candidate model hash: {sha(model_a)}", "", "## Readiness deficits"
    ]
    lines += [f"- {item['gate']}: actual={item['actual']}, required={item.get('required')}" for item in deficits] or ["- None recorded."]
    lines += ["", "## Agent statuses"] + [f"- {item['agent']}: {item['status']}" for item in agents]
    lines += ["", "## Access and publication boundaries", report["access_boundary"], "", "This generated report does not publish to Wix; a connected Wix write requires a separate read-back check."]
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["run_status"], "agents": len(agents), "conversation_records": len(imported),
                      "articles": len(articles), "sources": len(sources), "compositions": model_a.get("candidate_composition_count", 0),
                      "readiness_deficits": len(deficits), "first_model_gate": readiness,
                      "report": str(out.relative_to(ROOT)), "markdown_report": str(md.relative_to(ROOT))}, ensure_ascii=False))
    return 0 if operational_pass else 2

if __name__ == "__main__":
    raise SystemExit(main())
