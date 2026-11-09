"""Run explicit structural removal/substitution cases without declaring semantic truth."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "cartography" / "inbox" / "keystone_cases"


def evaluate_case(case: dict) -> dict:
    required = {"case_id", "candidate_id", "baseline_anchors", "removal_anchors", "substitution_anchors"}
    missing = sorted(required - case.keys())
    if missing:
        return {"case_id": case.get("case_id"), "status": "FAILED", "errors": [f"MISSING:{x}" for x in missing]}
    baseline = case["baseline_anchors"]
    removal = case["removal_anchors"]
    substitution = case["substitution_anchors"]
    if not all(isinstance(x, list) for x in (baseline, removal, substitution)):
        return {"case_id": case["case_id"], "status": "FAILED", "errors": ["ANCHOR_FIELDS_MUST_BE_LISTS"]}
    if not all(isinstance(x, str) and x for x in baseline + removal + substitution):
        return {"case_id": case["case_id"], "status": "FAILED", "errors": ["ANCHORS_MUST_BE_NONEMPTY_STRINGS"]}
    removed = set(baseline) - set(removal)
    substituted = set(baseline) - set(substitution)
    return {
        "case_id": case["case_id"],
        "candidate_id": case["candidate_id"],
        "status": "STRUCTURALLY_TESTED",
        "removed_anchor_ids": sorted(removed),
        "changed_by_substitution": sorted(substituted),
        "keystone_verified": False,
        "interpretation": "Structural difference only. No axiom or semantic truth is inferred."
    }


def run_cases() -> dict:
    results = []
    for path in sorted(INBOX.glob("*.json")):
        try:
            case = json.loads(path.read_text(encoding="utf-8"))
            results.append(evaluate_case(case))
        except Exception as exc:
            results.append({"file": path.name, "status": "FAILED", "errors": [f"{type(exc).__name__}:{exc}"]})
    failures = [r for r in results if r.get("status") == "FAILED"]
    output = {"status": "FAILED" if failures else ("STRUCTURALLY_TESTED" if results else "NO_INPUTS"),
              "case_count": len(results), "results": results,
              "semantic_verification": False}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return output


if __name__ == "__main__":
    raise SystemExit(1 if run_cases()["status"] == "FAILED" else 0)
