"""Fail-closed validator for source-grounded logic package lifecycle contracts."""
from __future__ import annotations

import re
from typing import Any, Mapping

_SCHEMA = "wanga-logic-package/1.0"
_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_REQUIRED = {
    "schema_version", "package_id", "version", "status", "formal_semantics",
    "premises", "conclusion", "source_refs", "tests", "known_limits", "semantic_status", "release_approval",
}


def validate_package_contract(package: Mapping[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(package, Mapping):
        return {"status": "INVALID", "errors": ["package must be an object"], "release_allowed": False}
    missing = sorted(_REQUIRED - set(package))
    if missing:
        errors.append(f"missing required fields: {missing}")
    if package.get("schema_version") != _SCHEMA:
        errors.append(f"schema_version must be {_SCHEMA}")
    if package.get("status") not in {"SPECIFIED", "PROTOTYPED", "TESTED", "VERIFIED", "INTERNAL_CANDIDATE_NOT_RELEASED"}:
        errors.append("unsupported lifecycle status")
    if package.get("semantic_status") not in {"NOT_YET_VERIFIED", "VERIFIED_WITHIN_ENCODED_FRAGMENT"}:
        errors.append("unsupported semantic_status")

    semantics = package.get("formal_semantics")
    if not isinstance(semantics, Mapping):
        errors.append("formal_semantics must be an object")
    else:
        if not isinstance(semantics.get("logic_fragment"), str) or not semantics.get("logic_fragment"):
            errors.append("formal_semantics.logic_fragment is required")
        if not isinstance(semantics.get("variables"), Mapping):
            errors.append("formal_semantics.variables must be an object")
        if not isinstance(semantics.get("supported_operators"), list) or not semantics.get("supported_operators"):
            errors.append("formal_semantics.supported_operators must be a non-empty list")

    premises = package.get("premises")
    if not isinstance(premises, list):
        errors.append("premises must be a list")
        premises = []
    seen = set()
    for index, premise in enumerate(premises):
        if not isinstance(premise, Mapping):
            errors.append(f"premise[{index}] must be an object")
            continue
        premise_id = premise.get("id")
        if not isinstance(premise_id, str) or not premise_id or premise_id in seen:
            errors.append(f"premise[{index}] requires a unique non-empty id")
        seen.add(premise_id)
        if not isinstance(premise.get("expr"), Mapping):
            errors.append(f"premise[{index}].expr must be an AST object")
        refs = premise.get("source_refs")
        if not isinstance(refs, list) or any(not isinstance(x, str) or not x for x in refs):
            errors.append(f"premise[{index}].source_refs must be a list of strings")
            refs = []
        if not refs and premise.get("assumption") is not True:
            errors.append(f"premise[{index}] must cite source_refs or be explicit assumption=true")
        if not isinstance(premise.get("assumption", False), bool):
            errors.append(f"premise[{index}].assumption must be boolean")

    conclusion = package.get("conclusion")
    if not isinstance(conclusion, Mapping):
        errors.append("conclusion must be a formal AST object")
    source_refs = package.get("source_refs")
    if not isinstance(source_refs, list) or any(not isinstance(x, str) or not x for x in source_refs):
        errors.append("source_refs must be a list of non-empty source IDs")
        source_refs = []
    if not isinstance(package.get("tests"), list):
        errors.append("tests must be a list")
    if not isinstance(package.get("known_limits"), list) or not package.get("known_limits"):
        errors.append("known_limits must be a non-empty list")

    status = package.get("status")
    semantic_status = package.get("semantic_status")
    approval = package.get("release_approval")
    if status == "VERIFIED" or semantic_status == "VERIFIED_WITHIN_ENCODED_FRAGMENT":
        if (status == "VERIFIED") != (semantic_status == "VERIFIED_WITHIN_ENCODED_FRAGMENT"):
            errors.append("VERIFIED lifecycle and semantic statuses must agree")
        if not isinstance(approval, Mapping):
            errors.append("verified status requires an independent release_approval record")
        else:
            for key in ("reviewer_id", "approved_at", "benchmark_report_sha256", "evidence_refs", "independent_review_pass"):
                if key not in approval:
                    errors.append(f"release_approval missing {key}")
            if not isinstance(approval.get("reviewer_id"), str) or not approval.get("reviewer_id"):
                errors.append("release_approval.reviewer_id must be non-empty")
            if not isinstance(approval.get("approved_at"), str) or not approval.get("approved_at"):
                errors.append("release_approval.approved_at must be non-empty")
            if not isinstance(approval.get("benchmark_report_sha256"), str) or not _SHA256.fullmatch(approval.get("benchmark_report_sha256", "")):
                errors.append("release_approval.benchmark_report_sha256 must be a SHA-256 hex digest")
            if not isinstance(approval.get("evidence_refs"), list) or not approval.get("evidence_refs"):
                errors.append("release_approval.evidence_refs must be a non-empty list")
            if approval.get("independent_review_pass") is not True:
                errors.append("release_approval.independent_review_pass must be true")
            if status == "VERIFIED" and semantic_status != "VERIFIED_WITHIN_ENCODED_FRAGMENT":
                errors.append("VERIFIED lifecycle status requires VERIFIED_WITHIN_ENCODED_FRAGMENT")

    if status == "INTERNAL_CANDIDATE_NOT_RELEASED" and package.get("release_approval") is not None:
        errors.append("internal candidate must not include release_approval")
    unique_sources = sorted(set(source_refs))
    return {
        "schema_version": "wanga-logic-package-validation/1.0",
        "status": "VALID_CONTRACT" if not errors else "INVALID",
        "errors": errors,
        "package_id": package.get("package_id"),
        "unique_source_ref_count": len(unique_sources),
        "release_allowed": not errors and status == "VERIFIED" and semantic_status == "VERIFIED_WITHIN_ENCODED_FRAGMENT",
        "validation_boundary": "Contract shape and release approval fields are checked; source truth and proof correctness require independent checks.",
    }
