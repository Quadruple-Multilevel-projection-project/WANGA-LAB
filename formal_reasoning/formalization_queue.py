"""Create a fail-closed formalization queue item from a lexical Logic Trader package."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


MISSING_FORMAL_FIELDS = [
    "logic_fragment",
    "variable_declarations",
    "formal_premises",
    "formal_conclusion",
    "assumption_scope",
    "counterexample_suite",
    "solver_result",
]


def _hash(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def queue_candidate_for_formalization(candidate: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, Mapping):
        raise ValueError("candidate must be an object")
    package_id = candidate.get("package_id")
    if not isinstance(package_id, str) or not package_id:
        raise ValueError("candidate.package_id must be a non-empty string")
    members = candidate.get("member_articles")
    sources = candidate.get("sources")
    if not isinstance(members, list) or not members:
        raise ValueError("candidate must include member_articles")
    if not isinstance(sources, list):
        raise ValueError("candidate.sources must be a list")
    source_ids = {item.get("id") for item in sources if isinstance(item, Mapping) and isinstance(item.get("id"), str)}
    entries = []
    unresolved_sources = []
    for article in members:
        if not isinstance(article, Mapping):
            raise ValueError("member_articles items must be objects")
        article_id = article.get("id")
        refs = article.get("source_refs", [])
        if not isinstance(article_id, str) or not article_id:
            raise ValueError("each member article requires an id")
        if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
            raise ValueError(f"{article_id}: source_refs must be a list of strings")
        missing = sorted(set(refs) - source_ids)
        if not refs or missing:
            unresolved_sources.append({"article_id": article_id, "missing_source_ids": missing, "has_source_refs": bool(refs)})
        entries.append({
            "claim_ref": article_id,
            "surface_definition": str(article.get("definition", "")),
            "source_refs": sorted(set(refs)),
            "source_status": "RESOLVED" if refs and not missing else "SOURCE_REVIEW_REQUIRED",
            "formalization_status": "NOT_FORMALIZED",
        })
    payload = {
        "schema_version": "wanga-formalization-queue-item/1.0",
        "queue_item_id": "FORM-" + _hash({
            "package_id": package_id,
            "member_ids": [x["claim_ref"] for x in entries],
            "source_ids": sorted(source_ids),
        })[:16],
        "candidate_package_id": package_id,
        "candidate_package_version": str(candidate.get("version", "unknown")),
        "status": "READY_FOR_FORMALIZATION" if not unresolved_sources else "BLOCKED_SOURCE_REVIEW",
        "candidate_claims": entries,
        "source_ids": sorted(source_ids),
        "unresolved_sources": unresolved_sources,
        "missing_formal_fields": list(MISSING_FORMAL_FIELDS),
        "solver_execution_status": "NOT_RUN_NO_FORMAL_AST",
        "formal_fragment_schema": "wanga-formal-fragment/1.0",
        "semantic_status": "NOT_YET_VERIFIED",
        "automatic_semantic_conversion": False,
        "boundary": (
            "Definitions are kept as source-linked surface text. No AST, premise, conclusion, "
            "proof, or entailment has been invented. A reviewer or a configured proposer must "
            "draft a formal representation that passes the formal-fragment contract."
        ),
    }
    payload["queue_item_sha256"] = _hash(payload)
    return payload
