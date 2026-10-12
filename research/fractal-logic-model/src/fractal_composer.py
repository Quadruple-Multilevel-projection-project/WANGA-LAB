"""Deterministic V1 composer for source-backed fractal logic fragments.

The composer builds candidates, not truths. It validates references and typed
interfaces, preserves all parents and claim lineage, and derives a reproducible
content hash. It deliberately does not guess semantic equivalence.
"""
from __future__ import annotations
import hashlib
import json
import re
from typing import Any, Mapping, Sequence

STATUSES = {"CANDIDATE", "SPECIFIED", "BUILT", "TESTED", "NOT_YET_VERIFIED", "VERIFIED", "REJECTED"}
SOURCE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")


class FragmentError(ValueError):
    pass


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def content_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def _unique_strings(values: Any, field: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) or not v.strip() for v in values):
        raise FragmentError(f"{field} must be an array of non-empty strings")
    if len(values) != len(set(values)):
        raise FragmentError(f"{field} must not contain duplicates")
    return values


def validate_fragment(fragment: Mapping[str, Any], source_registry: Mapping[str, Any] | None = None) -> dict[str, Any]:
    if not isinstance(fragment, Mapping):
        raise FragmentError("fragment must be an object")
    required = ("fragment_id", "version", "status", "scale", "claims", "inputs", "outputs", "composition", "provenance", "tests")
    missing = [key for key in required if key not in fragment]
    if missing:
        raise FragmentError("missing required fields: " + ", ".join(missing))
    fid = fragment["fragment_id"]
    if not isinstance(fid, str) or not SOURCE_ID_RE.fullmatch(fid):
        raise FragmentError("fragment_id must be a stable identifier")
    if fragment["status"] not in STATUSES:
        raise FragmentError(f"unsupported status {fragment['status']!r}")
    if isinstance(fragment["scale"], bool) or not isinstance(fragment["scale"], int) or fragment["scale"] < 0:
        raise FragmentError("scale must be a non-negative integer")
    if not isinstance(fragment["claims"], list) or not fragment["claims"]:
        raise FragmentError("a fragment must contain at least one claim")
    if not isinstance(fragment["inputs"], list) or not isinstance(fragment["outputs"], list):
        raise FragmentError("inputs and outputs must be arrays")
    for field_name in ("inputs", "outputs"):
        names = []
        for item in fragment[field_name]:
            if not isinstance(item, Mapping) or not isinstance(item.get("name"), str) or not isinstance(item.get("type"), str):
                raise FragmentError(f"every {field_name} entry needs non-empty name and type")
            if not item["name"].strip() or not item["type"].strip():
                raise FragmentError(f"every {field_name} entry needs non-empty name and type")
            if item["name"] in names:
                raise FragmentError(f"duplicate {field_name} name {item['name']!r}")
            names.append(item["name"])
    claims = fragment["claims"]
    claim_ids = []
    source_registry = source_registry or {}
    for claim in claims:
        if not isinstance(claim, Mapping):
            raise FragmentError("claim must be an object")
        cid = claim.get("claim_id")
        text = claim.get("text")
        if not isinstance(cid, str) or not cid.strip() or not isinstance(text, str) or not text.strip():
            raise FragmentError("each claim requires a claim_id and text")
        claim_ids.append(cid)
        if claim.get("status", "CANDIDATE") not in STATUSES:
            raise FragmentError(f"unsupported claim status for {cid}")
        source_ids = claim.get("source_span_ids", [])
        if not isinstance(source_ids, list) or any(not isinstance(s, str) for s in source_ids):
            raise FragmentError(f"source_span_ids for {cid} must be an array of strings")
        if not source_ids and claim.get("assumption") is not True:
            raise FragmentError(f"claim {cid} needs a source span or assumption=true")
        for sid in source_ids:
            if source_registry and sid not in source_registry:
                raise FragmentError(f"claim {cid} references unknown source {sid!r}")
    if len(claim_ids) != len(set(claim_ids)):
        raise FragmentError("claim IDs must be unique within a fragment")
    provenance = fragment["provenance"]
    if not isinstance(provenance, list):
        raise FragmentError("provenance must be an array")
    for entry in provenance:
        if not isinstance(entry, Mapping) or not entry.get("source_id") or not entry.get("locator"):
            raise FragmentError("provenance entries require source_id and locator")
        if source_registry and entry["source_id"] not in source_registry:
            raise FragmentError(f"provenance references unknown source {entry['source_id']!r}")
    if not isinstance(fragment["composition"], Mapping):
        raise FragmentError("composition must be an object")
    parents = fragment["composition"].get("parent_ids", [])
    if not isinstance(parents, list) or any(not isinstance(parent, str) for parent in parents):
        raise FragmentError("composition.parent_ids must be an array of strings")
    _unique_strings(fragment["composition"].get("parent_ids", []), "composition.parent_ids")
    if not isinstance(fragment["tests"], list):
        raise FragmentError("tests must be an array")
    return {"status": "VALID_STRUCTURE", "fragment_id": fid, "claim_count": len(claims), "scale": fragment["scale"]}


def compose_pair(
    first: Mapping[str, Any],
    second: Mapping[str, Any],
    *,
    source_registry: Mapping[str, Any],
    composition_rule_id: str = "COMPOSE-INTERFACE-SEQUENTIAL-V1",
) -> dict[str, Any]:
    """Compose first.outputs into second.inputs using exact type compatibility."""
    validate_fragment(first, source_registry)
    validate_fragment(second, source_registry)
    if first["fragment_id"] == second["fragment_id"]:
        raise FragmentError("a fragment cannot compose with itself in V1")
    out_by_type: dict[str, list[Mapping[str, Any]]] = {}
    for port in first["outputs"]:
        out_by_type.setdefault(port["type"], []).append(port)
    matched = []
    unmatched_required = []
    for port in second["inputs"]:
        options = out_by_type.get(port["type"], [])
        if not options:
            if port.get("required", True):
                unmatched_required.append({"fragment": second["fragment_id"], "input": port["name"], "type": port["type"]})
            continue
        matched.append({
            "from_fragment": first["fragment_id"],
            "from_output": options[0]["name"],
            "to_fragment": second["fragment_id"],
            "to_input": port["name"],
            "type": port["type"],
            "status": "TYPE_COMPATIBLE_INTERFACE_NOT_SEMANTICALLY_PROVEN",
        })
    if unmatched_required:
        raise FragmentError("required interface mismatch: " + json.dumps(unmatched_required, ensure_ascii=False))

    combined_claims = []
    for parent in (first, second):
        for claim in parent["claims"]:
            record = dict(claim)
            record["origin_fragment_id"] = parent["fragment_id"]
            record["claim_id"] = parent["fragment_id"] + "::" + claim["claim_id"]
            record["inherited_status"] = claim.get("status", parent["status"])
            record["status"] = "CANDIDATE"
            combined_claims.append(record)
    merged_provenance = []
    seen_prov = set()
    for parent in (first, second):
        for entry in parent["provenance"]:
            item = dict(entry)
            key = canonical_json(item)
            if key not in seen_prov:
                seen_prov.add(key)
                merged_provenance.append(item)
    inputs = [dict(p) for p in first["inputs"]]
    outputs = [dict(p) for p in second["outputs"]]
    composition_payload = {
        "parent_ids": [first["fragment_id"], second["fragment_id"]],
        "rule_id": composition_rule_id,
        "interface_checks": matched,
        "interface_result": "TYPE_COMPATIBLE_CANDIDATE",
        "semantic_equivalence": "NOT_ESTABLISHED",
    }
    candidate = {
        "fragment_id": "FL-COMPOSE-" + content_hash({
            "parents": [first.get("model_hash") or content_hash(first), second.get("model_hash") or content_hash(second)],
            "rule": composition_rule_id,
            "interfaces": matched,
        })[:16],
        "version": "0.1",
        "status": "CANDIDATE",
        "scale": max(first["scale"], second["scale"]) + 1,
        "claims": combined_claims,
        "inputs": inputs,
        "outputs": outputs,
        "composition": composition_payload,
        "provenance": merged_provenance,
        "tests": [],
        "counterexamples": [],
        "model_hash": "",
        "assumptions": [
            "Type compatibility is necessary but not sufficient for semantic composition.",
            "A candidate inherits lineage but does not inherit VERIFIED status.",
        ],
    }
    candidate["model_hash"] = content_hash(candidate)
    validation = validate_fragment(candidate, source_registry)
    return {
        "status": "COMPOSITION_CANDIDATE_READY_FOR_TESTS",
        "fragment": candidate,
        "validation": validation,
        "composition_trace": {
            "parent_ids": candidate["composition"]["parent_ids"],
            "rule_id": composition_rule_id,
            "matched_interfaces": matched,
            "unmatched_optional_inputs": [
                {"fragment": second["fragment_id"], "input": p["name"], "type": p["type"]}
                for p in second["inputs"] if not p.get("required", True) and p["type"] not in out_by_type
            ],
            "source_ids_preserved": sorted({p["source_id"] for p in merged_provenance}),
            "claim_origin_ids_preserved": [c["origin_fragment_id"] for c in combined_claims],
            "model_hash": candidate["model_hash"],
            "semantic_status": "NOT_YET_VERIFIED",
        },
    }


def build_wiki_backlinks(index: Mapping[str, Any], existing_paths: set[str]) -> dict[str, Any]:
    if not isinstance(index, Mapping) or not isinstance(index.get("pages"), list):
        raise FragmentError("wiki index must have pages array")
    pages = index["pages"]
    ids = [p.get("page_id") for p in pages]
    if any(not isinstance(pid, str) or not pid for pid in ids) or len(ids) != len(set(ids)):
        raise FragmentError("wiki page IDs must be unique and non-empty")
    known = set(ids)
    missing_files = [p["path"] for p in pages if p.get("path") not in existing_paths]
    bad_related = [
        {"page_id": p["page_id"], "related_id": rid}
        for p in pages for rid in p.get("related_ids", []) if rid not in known
    ]
    backlinks: dict[str, list[str]] = {pid: [] for pid in ids}
    for page in pages:
        for target in page.get("related_ids", []):
            if target in backlinks:
                backlinks[target].append(page["page_id"])
    return {
        "status": "PASS" if not missing_files and not bad_related else "REVIEW",
        "page_count": len(pages),
        "missing_files": missing_files,
        "unknown_related_ids": bad_related,
        "backlinks": {key: sorted(values) for key, values in backlinks.items()},
        "index_hash": content_hash(index),
    }
