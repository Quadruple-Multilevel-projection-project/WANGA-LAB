"""Small fixed benchmark suite for the bounded propositional solver adapter."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .propositional import analyze_claim

DEFAULT_CASES = Path(__file__).resolve().parent / "examples" / "benchmark_cases.json"


def run_benchmark_suite(cases_path: Path | str | None = None) -> dict[str, Any]:
    path = Path(cases_path) if cases_path is not None else DEFAULT_CASES
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "wanga-formal-benchmark/1.0":
        raise ValueError("unsupported formal benchmark schema version")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("formal benchmark must contain a non-empty cases list")
    results = []
    for case in cases:
        case_id = case.get("case_id")
        expected = case.get("expected_status")
        claim = case.get("claim")
        if not isinstance(case_id, str) or not case_id or not isinstance(expected, str) or not isinstance(claim, dict):
            results.append({
                "case_id": case_id,
                "passed": False,
                "status": "INVALID_BENCHMARK_CASE",
                "expected_status": expected,
                "verification_status": "NOT_YET_VERIFIED",
            })
            continue
        try:
            actual = analyze_claim(claim)
            results.append({
                "case_id": case_id,
                "passed": actual.get("status") == expected,
                "expected_status": expected,
                "actual_status": actual.get("status"),
                "premise_consistency": actual.get("premise_consistency"),
                "entailment": actual.get("entailment"),
                "countermodel": actual.get("countermodel"),
                "input_sha256": actual.get("input_sha256"),
                "verification_status": actual.get("verification_status", "NOT_YET_VERIFIED"),
            })
        except Exception as exc:
            results.append({
                "case_id": case_id,
                "passed": False,
                "expected_status": expected,
                "actual_status": "ERROR",
                "error": f"{type(exc).__name__}: {exc}",
                "verification_status": "NOT_YET_VERIFIED",
            })
    passed = sum(row.get("passed") is True for row in results)
    failed = len(results) - passed
    return {
        "schema_version": "wanga-formal-benchmark-report/1.0",
        "status": "PASS" if failed == 0 else "FAIL",
        "suite_id": payload.get("suite_id", "wanga-propositional-smoke-v1"),
        "case_count": len(results),
        "passed": passed,
        "failed": failed,
        "cases": results,
        "scope": "SYNTHETIC_PROPOSITIONAL_FIXTURES_ONLY",
        "natural_language_truth_verified": False,
        "epistemic_status_promotion": "FORBIDDEN",
        "verification_status": "NOT_YET_VERIFIED",
        "next_gate": "Expand to source-grounded cases and independent holdout before using this suite for candidate release.",
    }
