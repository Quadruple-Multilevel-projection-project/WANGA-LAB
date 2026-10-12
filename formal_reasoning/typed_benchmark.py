"""Replayable synthetic typed-AST benchmark runner for the bounded formal-logic adapter."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .typed_fragment import FormalSpecError, check_entailment

FIXTURE_STATUS = "SYNTHETIC_FORMAL_FIXTURES_NOT_SOURCE_GROUNDED"


def run_typed_benchmark_suite(path: Path | str) -> dict[str, Any]:
    fixture_path = Path(path)
    payload = json.loads(fixture_path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "wanga-formal-benchmark/1.0":
        raise ValueError("unsupported formal benchmark schema_version")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("formal benchmark must have a non-empty cases array")
    results = []
    for case in cases:
        case_id = case.get("id")
        expected = case.get("expected", {})
        try:
            result = check_entailment(case["spec"])
            if "error" in expected:
                passed = False
                observed = {"unexpected_result": result.get("entailment_status")}
            else:
                observed = {
                    "premise_consistency": result.get("premise_consistency"),
                    "entailment_status": result.get("entailment_status"),
                }
                passed = all(observed.get(key) == value for key, value in expected.items())
            results.append({
                "case_id": case_id,
                "status": "PASS" if passed else "FAIL",
                "expected": expected,
                "observed": observed,
                "semantic_status": result.get("semantic_status", "NOT_YET_VERIFIED"),
            })
        except FormalSpecError as exc:
            passed = expected.get("error") == "FormalSpecError"
            results.append({
                "case_id": case_id,
                "status": "PASS" if passed else "FAIL",
                "expected": expected,
                "observed": {"error": type(exc).__name__, "message": str(exc)},
                "semantic_status": "NOT_YET_VERIFIED",
            })
    passed = sum(1 for result in results if result["status"] == "PASS")
    total = len(results)
    return {
        "schema_version": "wanga-formal-benchmark-result/1.0",
        "status": "PASS" if passed == total else "FAIL",
        "fixture_status": payload.get("status", FIXTURE_STATUS),
        "case_count": total,
        "passed_cases": passed,
        "failed_cases": total - passed,
        "results": results,
        "claim_boundary": "Synthetic formal fixtures verify adapter behavior only; they are not source-grounded semantic benchmarks and do not verify Logic Trader packages.",
        "semantic_status": "NOT_YET_VERIFIED",
    }
