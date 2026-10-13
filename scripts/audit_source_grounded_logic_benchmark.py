"""Audit and execute only explicitly reviewed source-grounded formal benchmark cases."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

try:
    import jsonschema
except ImportError as exc:  # pragma: no cover - CI installs requirements-formal.txt
    raise RuntimeError("jsonschema is required; install requirements-formal.txt") from exc

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "formal_reasoning/examples/source_grounded_benchmark_manifest.json"
DEFAULT_SCHEMA = ROOT / "schemas/source-grounded-logic-benchmark-case-v1.schema.json"
DEFAULT_MANIFEST_SCHEMA = ROOT / "schemas/source-grounded-logic-benchmark-manifest-v1.schema.json"
DEFAULT_CATALOG = ROOT / "logic_wiki/data/articles.json"
DEFAULT_OUT = ROOT / "research/reports/formal-reasoning/source-grounded-benchmark-latest.json"
RISK_TYPES = {"NEGATIVE", "BOUNDARY", "COUNTEREXAMPLE"}


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _validate_schema(payload: Mapping[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(schema)
    validator = jsonschema.Draft202012Validator(schema)
    return [error.message for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path))]


def audit_manifest(
    manifest: Mapping[str, Any],
    case_schema_path: Path = DEFAULT_SCHEMA,
    manifest_schema_path: Path = DEFAULT_MANIFEST_SCHEMA,
    source_catalog: Mapping[str, Any] | None = None,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Validate source lineage and run reviewed cases; never formalize raw prose automatically."""
    started = time.perf_counter()
    manifest_errors = _validate_schema(manifest, manifest_schema_path)
    if manifest_errors:
        return {
            "schema_version": "wanga-source-grounded-benchmark-report/1.0",
            "status": "INVALID_MANIFEST",
            "manifest_errors": manifest_errors,
            "semantic_status": "NOT_YET_VERIFIED",
        }

    if source_catalog is None:
        catalog_path = root / str(manifest["source_registry"])
        source_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    sources = source_catalog.get("sources", [])
    source_by_id = {
        source.get("id"): source for source in sources
        if isinstance(source, Mapping) and isinstance(source.get("id"), str)
    }
    case_schema = json.loads(case_schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator.check_schema(case_schema)
    case_validator = jsonschema.Draft202012Validator(case_schema)

    seen_case_ids: set[str] = set()
    case_errors: list[dict[str, Any]] = []
    executable: list[Mapping[str, Any]] = []
    eligible_reviewed: list[Mapping[str, Any]] = []
    source_resolved_count = 0
    total_span_count = 0
    reviewed_span_count = 0

    for index, case in enumerate(manifest.get("cases", [])):
        if not isinstance(case, Mapping):
            case_errors.append({"case_index": index, "errors": ["case must be an object"]})
            continue
        case_id = case.get("case_id", f"CASE_INDEX_{index}")
        validation_errors = [error.message for error in sorted(case_validator.iter_errors(case), key=lambda e: list(e.path))]
        if validation_errors:
            case_errors.append({"case_id": case_id, "errors": validation_errors})
            continue
        if case_id in seen_case_ids:
            case_errors.append({"case_id": case_id, "errors": ["duplicate case_id"]})
            continue
        seen_case_ids.add(case_id)

        case_refs = set(case["source_refs"])
        missing_sources = sorted(case_refs - set(source_by_id))
        span_refs = {span["source_ref"] for span in case["source_spans"]}
        if missing_sources:
            case_errors.append({"case_id": case_id, "errors": [f"unknown source refs: {missing_sources}"]})
            continue
        if not span_refs.issubset(case_refs):
            case_errors.append({"case_id": case_id, "errors": ["source span refers to a source not listed in source_refs"]})
            continue
        if span_refs != case_refs:
            case_errors.append({"case_id": case_id, "errors": ["each source_ref must have at least one exact span locator and hash"]})
            continue
        source_resolved_count += 1
        total_span_count += len(case["source_spans"])

        reviewed = case["formalization_status"] == "REVIEWED_FORMALIZATION"
        if not reviewed:
            continue
        spec = case["formal_spec"]
        spec_refs = set(spec.get("source_refs", []))
        if not spec_refs or not spec_refs.issubset(case_refs):
            case_errors.append({"case_id": case_id, "errors": ["formal_spec.source_refs must be a non-empty subset of case source_refs"]})
            continue
        reviewed_span_count += len(case["source_spans"])
        executable.append(case)

        # Test-fixture refs are useful for unit tests, but never count toward source-grounded readiness.
        eligible = all(
            span["permission_scope"] != "TEST_FIXTURE_NOT_ELIGIBLE_FOR_READINESS"
            and source_by_id[span["source_ref"]].get("type") != "TEST_FIXTURE"
            for span in case["source_spans"]
        )
        if eligible:
            eligible_reviewed.append(case)

    if case_errors:
        return {
            "schema_version": "wanga-source-grounded-benchmark-report/1.0",
            "status": "INVALID_CASES",
            "case_count": len(manifest.get("cases", [])),
            "reviewed_case_count": len(executable),
            "case_errors": case_errors,
            "manifest_sha256": _hash(manifest),
            "semantic_status": "NOT_YET_VERIFIED",
        }

    if executable:
        from formal_reasoning.propositional import analyze_claim
    results: list[dict[str, Any]] = []
    for case in executable:
        if case["case_type"] in RISK_TYPES and case["expected_status"] == "ENTAILED_WITHIN_ENCODING":
            case_errors.append({
                "case_id": case["case_id"],
                "errors": ["risk-case expected status cannot be ENTAILED_WITHIN_ENCODING"],
            })
            continue
        try:
            observed = analyze_claim(case["formal_spec"])
            actual_status = observed.get("status", "UNKNOWN")
            expected_status = case["expected_status"]
            results.append({
                "case_id": case["case_id"],
                "case_type": case["case_type"],
                "split": case["split"],
                "status": "PASS" if actual_status == expected_status else "FAIL",
                "expected_status": expected_status,
                "observed_status": actual_status,
                "premise_consistency": observed.get("premise_consistency", "UNKNOWN"),
                "source_refs": case["source_refs"],
                "encoding_hash": observed.get("input_sha256") or observed.get("encoding_hash"),
                "semantic_status": "NOT_YET_VERIFIED",
            })
        except Exception as exc:
            results.append({
                "case_id": case["case_id"],
                "case_type": case["case_type"],
                "split": case["split"],
                "status": "ERROR",
                "expected_status": case["expected_status"],
                "error_type": type(exc).__name__,
                "error": str(exc),
                "semantic_status": "NOT_YET_VERIFIED",
            })
    if case_errors:
        return {
            "schema_version": "wanga-source-grounded-benchmark-report/1.0",
            "status": "INVALID_CASES",
            "case_count": len(manifest.get("cases", [])),
            "reviewed_case_count": len(executable),
            "case_errors": case_errors,
            "manifest_sha256": _hash(manifest),
            "semantic_status": "NOT_YET_VERIFIED",
        }

    case_count = len(manifest.get("cases", []))
    executed_count = len(results)
    passed_all = sum(1 for result in results if result["status"] == "PASS")
    eligible_ids = {case["case_id"] for case in eligible_reviewed}
    eligible_results = [r for r in results if r["case_id"] in eligible_ids]
    eligible_passed = sum(1 for result in eligible_results if result["status"] == "PASS")
    eligible_risk_results = [r for r in eligible_results if r["case_type"] in RISK_TYPES]
    eligible_counterexample_results = [r for r in eligible_results if r["case_type"] == "COUNTEREXAMPLE"]
    eligible_holdout_results = [r for r in eligible_results if r["split"] == "HOLDOUT"]
    reviewed_types = Counter(case["case_type"] for case in eligible_reviewed)
    reviewed_splits = {case["split"] for case in eligible_reviewed}
    source_classes = {
        source_by_id[ref].get("type")
        for case in eligible_reviewed for ref in case["source_refs"]
        if source_by_id[ref].get("type") and source_by_id[ref].get("type") != "TEST_FIXTURE"
    }

    eligible_span_count = sum(len(case["source_spans"]) for case in eligible_reviewed)
    metrics = {
        "source_coverage": source_resolved_count / case_count if case_count else None,
        "evidence_coverage": eligible_span_count / total_span_count if total_span_count else None,
        "benchmark_accuracy": eligible_passed / len(eligible_results) if eligible_results else None,
        "false_accept_rate": (
            sum(1 for r in eligible_risk_results if r["observed_status"] == "ENTAILED_WITHIN_ENCODING") / len(eligible_risk_results)
            if eligible_risk_results else None
        ),
        "counterexample_escape_rate": (
            sum(1 for r in eligible_counterexample_results if r["observed_status"] == "ENTAILED_WITHIN_ENCODING") / len(eligible_counterexample_results)
            if eligible_counterexample_results else None
        ),
        "holdout_score": (
            sum(1 for r in eligible_holdout_results if r["status"] == "PASS") / len(eligible_holdout_results)
            if eligible_holdout_results else None
        ),
    }

    policy_path = root / "formal_reasoning/config/evaluation_policy.json"
    evaluation_policy = json.loads(policy_path.read_text(encoding="utf-8"))
    thresholds = evaluation_policy["thresholds"]
    metric_gates = {
        "source_coverage": metrics["source_coverage"] is not None and metrics["source_coverage"] >= thresholds["min_source_coverage"],
        "evidence_coverage": metrics["evidence_coverage"] is not None and metrics["evidence_coverage"] >= thresholds["min_evidence_coverage"],
        "benchmark_accuracy": metrics["benchmark_accuracy"] is not None and metrics["benchmark_accuracy"] >= thresholds["min_benchmark_accuracy"],
        "false_accept_rate": metrics["false_accept_rate"] is not None and metrics["false_accept_rate"] <= thresholds["max_false_accept_rate"],
        "counterexample_escape_rate": metrics["counterexample_escape_rate"] is not None and metrics["counterexample_escape_rate"] <= thresholds["max_counterexample_escape_rate"],
        "holdout_score": metrics["holdout_score"] is not None and metrics["holdout_score"] >= thresholds["min_holdout_score"],
    }

    min_risk_cases = int(manifest["minimum_risk_cases"])
    required_risk_types = set(manifest["required_risk_case_types"])
    risk_counts = {key: reviewed_types.get(key, 0) for key in sorted(RISK_TYPES)}
    ready_requirements = {
        "minimum_reviewed_risk_cases": sum(risk_counts.values()) >= min_risk_cases,
        "required_risk_types_present": required_risk_types.issubset({key for key, count in risk_counts.items() if count > 0}),
        "required_splits_present": set(manifest["required_splits"]).issubset(reviewed_splits),
        "minimum_source_classes_present": len(source_classes) >= int(manifest["minimum_source_classes"]),
        "at_least_one_eligible_case_executed": bool(eligible_results),
        "all_eligible_expected_results_match": bool(eligible_results) and eligible_passed == len(eligible_results),
        "metric_gates_pass": all(metric_gates.values()),
        "no_case_errors": not case_errors,
    }
    ready = all(ready_requirements.values())
    if executed_count and passed_all < executed_count:
        status = "FAIL_CASE_EXPECTATION"
    elif ready:
        status = "PASS_BENCHMARK_CASES_READINESS_GATES"
    else:
        status = "BLOCKED_INSUFFICIENT_REVIEWED_CASES"

    return {
        "schema_version": "wanga-source-grounded-benchmark-report/1.0",
        "status": status,
        "dataset_id": manifest["dataset_id"],
        "dataset_version": manifest["dataset_version"],
        "manifest_sha256": _hash(manifest),
        "source_registry_sha256": _hash(source_catalog),
        "case_schema_sha256": hashlib.sha256(case_schema_path.read_bytes()).hexdigest(),
        "case_count": case_count,
        "reviewed_executable_case_count": executed_count,
        "eligible_reviewed_case_count": len(eligible_reviewed),
        "eligible_executed_case_count": len(eligible_results),
        "passed_cases": passed_all,
        "failed_cases": executed_count - passed_all,
        "eligible_passed_cases": eligible_passed,
        "eligible_failed_cases": len(eligible_results) - eligible_passed,
        "risk_case_counts": risk_counts,
        "source_class_count": len(source_classes),
        "source_classes": sorted(source_classes),
        "reviewed_splits": sorted(reviewed_splits),
        "metrics": metrics,
        "metric_gates": metric_gates,
        "metric_thresholds": thresholds,
        "threshold_status": evaluation_policy.get("status", "UNKNOWN"),
        "readiness_requirements": ready_requirements,
        "minimum_risk_cases": min_risk_cases,
        "case_results": results,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "false_accept_rate_semantics": "Known eligible risk cases observed as ENTAILED_WITHIN_ENCODING divided by eligible executed risk cases; null when no such cases exist.",
        "counterexample_escape_rate_semantics": "Eligible counterexample cases observed as ENTAILED_WITHIN_ENCODING divided by eligible executed counterexample cases; null when none exist.",
        "semantic_status": "NOT_YET_VERIFIED",
        "truth_boundary": "Results validate only the explicitly reviewed propositional encoding; source references and mapping review do not prove unrestricted natural-language truth. Synthetic/test-fixture sources are excluded from readiness metrics.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--case-schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--manifest-schema", default=str(DEFAULT_MANIFEST_SCHEMA))
    parser.add_argument("--catalog", default=str(DEFAULT_CATALOG))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args(argv)
    manifest_path = Path(args.manifest)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    case_schema_path = Path(args.case_schema)
    report = audit_manifest(
        manifest,
        case_schema_path=case_schema_path,
        manifest_schema_path=Path(args.manifest_schema),
        source_catalog=json.loads(Path(args.catalog).read_text(encoding="utf-8")),
        root=ROOT,
    )
    report_path = Path(args.out)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = {key: report.get(key) for key in (
        "status", "case_count", "reviewed_executable_case_count", "eligible_reviewed_case_count",
        "passed_cases", "failed_cases", "risk_case_counts", "source_class_count", "metrics", "semantic_status"
    )}
    summary["report_path"] = str(report_path)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if report["status"] in {"INVALID_MANIFEST", "INVALID_CASES", "FAIL_CASE_EXPECTATION"} else 0


if __name__ == "__main__":
    raise SystemExit(main())
