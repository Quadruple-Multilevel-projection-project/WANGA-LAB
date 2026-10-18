#!/usr/bin/env python3
"""Publish a machine-readable status snapshot for the live Wix dashboard."""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"

def read_json(name: str) -> dict:
    path = ARTIFACTS / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"_read_error": f"{name}: {exc}"}

def main() -> int:
    integration = read_json("gate14_structural_integration.json")
    audit = read_json("gate14_execution_audit.json")
    registry = read_json("book_sentence_registry.json")
    analysis = read_json("gate14_sentence_structure.json")
    overlap = read_json("gate14_word_occurrence_matrix.json")
    roles = read_json("gate14_word_role_candidates.json")
    coverage = integration.get("coverage", {})
    source_coverage = integration.get("canonical_source_coverage", {})
    audit_status = audit.get("audit_status", "MISSING")
    coverage_status = coverage.get("coverage_status", "MISSING")
    canonical_status = source_coverage.get("status", "MISSING")
    findings = audit.get("findings", [])
    mechanical_pass = (
        audit_status == "PASS"
        and coverage_status == "PASS"
        and source_coverage.get("full_source_match") is True
        and not findings
    )
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    repository = os.environ.get("GITHUB_REPOSITORY", "Quadruple-Multilevel-projection-project/WANGA-LAB")
    server = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    branch = os.environ.get("GITHUB_REF_NAME", "")
    report = {
        "schema": "WANGA_LIVE_STRUCTURAL_AUDIT_STATUS_V1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "overall_mechanical_status": "PASS" if mechanical_pass else "FAIL",
        "integration_status": integration.get("status", "MISSING"),
        "coverage_status": coverage_status,
        "canonical_source_coverage_status": canonical_status,
        "canonical_source_full_match": source_coverage.get("full_source_match", False),
        "legacy_gate14_registry_coverage": source_coverage.get("legacy_registry_coverage", "MISSING"),
        "legacy_gate14_exact_quote_matches": source_coverage.get("legacy_exact_quote_matches"),
        "legacy_gate14_unit_count": source_coverage.get("legacy_units"),
        "source_commit": registry.get("source", {}).get("commit"),
        "source_gate_count": registry.get("chapter_count", 0),
        "candidate_sentence_count": registry.get("total_candidate_sentences", 0),
        "lexical_word_count": registry.get("total_words", 0),
        "gate14_sentence_candidate_count": source_coverage.get("canonical_sentence_candidates", 0),
        "gate14_word_token_count": roles.get("token_count", 0),
        "gate14_structural_annotations": len(analysis.get("units", [])),
        "gate14_exact_surface_overlap_terms": overlap.get("terms_with_prior_gate_overlap", 0),
        "word_role_counts": roles.get("role_counts", {}),
        "audit_status": audit_status,
        "audit_findings": findings,
        "warnings": [
            "READY_FOR_REVIEW is not VERIFIED.",
            "Punctuation-based sentence boundaries remain candidates.",
            "Legacy Gate XIV excerpts cover only part of the canonical text.",
            "Exact word overlap is not a semantic relationship.",
            "Word-role labels are rule-based candidates; unassigned tokens require review."
        ],
        "run": {
            "id": run_id,
            "number": os.environ.get("GITHUB_RUN_NUMBER", ""),
            "url": f"{server}/{repository}/actions/runs/{run_id}" if run_id else "",
            "branch": branch,
            "commit": os.environ.get("GITHUB_SHA", ""),
            "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
            "event": os.environ.get("GITHUB_EVENT_NAME", "")
        }
    }
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    output = ARTIFACTS / "current_audit_status.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "overall_mechanical_status": report["overall_mechanical_status"],
        "integration_status": report["integration_status"],
        "coverage_status": coverage_status,
        "canonical_source_coverage_status": canonical_status,
        "legacy_gate14_registry_coverage": report["legacy_gate14_registry_coverage"],
        "audit_status": audit_status,
        "findings": findings
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
