#!/usr/bin/env python3
"""Build deterministic typed composition candidates from admitted literal source spans."""
from __future__ import annotations
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from logic_fractal.fragment_composer import FragmentError, compose_pair, content_hash, validate_fragment


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_candidates(root=ROOT):
    catalog = read(root / "logic_wiki/data/articles.json")
    unit_registry = read(root / "logic_fractal/data/logic_units.json")
    contract_data = read(root / "logic_fractal/data/composition_rules.json")
    fragment_data = read(root / "logic_fractal/data/source_grounded_fragments.json")
    source_registry = {}
    for source in catalog.get("sources", []):
        source_registry[source["id"]] = {
            "source_id": source["id"], "locator": source["uri"],
            "source_version": source.get("status"),
            "git_blob_sha": source.get("blob_sha")
        }
    unit_by_span = {}
    for unit in unit_registry.get("units", []):
        unit_by_span[unit["source_span_id"]] = unit
        source_registry[unit["source_span_id"]] = {
            "source_id": unit["source_id"], "locator": unit["exact_locator"],
            "source_version": unit["source_version"], "git_blob_sha": unit.get("source_blob_sha")
        }
    rules = contract_data.get("rules", [])
    rule_id = "COMPOSE-INTERFACE-SEQUENTIAL-V1"
    rule = next((item for item in rules if item.get("id") == rule_id), None)
    if not rule or rule.get("status") != "ACTIVE_SPECIFIED" or not rule.get("invariants"):
        raise FragmentError("The typed interface composition contract is not active and specified.")
    fragments = fragment_data.get("fragments", [])
    by_id = {item.get("fragment_id"): item for item in fragments}
    if len(by_id) != len(fragments) or None in by_id:
        raise FragmentError("Fragment IDs must be unique and non-empty.")
    for fragment in fragments:
        for claim in fragment.get("claims", []):
            for span_id in claim.get("source_span_ids", []):
                if span_id not in unit_by_span:
                    raise FragmentError("Claim references a span that is not admitted in logic_units.json: " + span_id)
        validate_fragment(fragment, source_registry)
    candidates = []
    for plan in fragment_data.get("composition_plan", []):
        if plan.get("rule_id") != rule_id:
            raise FragmentError("Composition plan references an undeclared rule.")
        first = by_id[plan["first"]]
        second = by_id[plan["second"]]
        result = compose_pair(first, second, source_registry=source_registry, composition_rule_id=rule_id)
        repeated = compose_pair(first, second, source_registry=source_registry, composition_rule_id=rule_id)
        candidate = result["fragment"]
        expected_parent_ids = [first["fragment_id"], second["fragment_id"]]
        expected_source_ids = sorted({entry["source_id"] for entry in first["provenance"] + second["provenance"]})
        checks = {
            "parent_ids_preserved": candidate["composition"]["parent_ids"] == expected_parent_ids,
            "source_lineage_preserved": result["composition_trace"]["source_ids_preserved"] == expected_source_ids,
            "type_interfaces_match": bool(result["composition_trace"]["matched_interfaces"]) and all(
                item["status"] == "TYPE_COMPATIBLE_INTERFACE_NOT_SEMANTICALLY_PROVEN"
                for item in result["composition_trace"]["matched_interfaces"]
            ),
            "claims_reset_to_candidate": all(claim["status"] == "CANDIDATE" for claim in candidate["claims"]),
            "semantic_equivalence_not_established": candidate["composition"]["semantic_equivalence"] == "NOT_ESTABLISHED",
            "deterministic_rebuild": candidate["model_hash"] == repeated["fragment"]["model_hash"]
        }
        if not all(checks.values()):
            raise FragmentError("Composition invariants failed: " + json.dumps(checks, ensure_ascii=False))
        candidates.append({
            "candidate_id": candidate["fragment_id"],
            "candidate_hash": candidate["model_hash"],
            "status": "CANDIDATE_NOT_SEMANTICALLY_VERIFIED",
            "composition_rule_id": rule_id,
            "parent_ids": expected_parent_ids,
            "source_ids": expected_source_ids,
            "source_span_ids": sorted({sid for claim in candidate["claims"] for sid in claim.get("source_span_ids", [])}),
            "invariants_checked": checks,
            "test_outcomes": {"structural_validation": "PASS", "deterministic_rebuild": "PASS", "semantic_ground_truth": "NOT_RUN"},
            "semantic_status": "NOT_YET_VERIFIED",
            "scope": "Typed interface compatibility and provenance preservation only.",
            "non_applicability": fragment_data.get("non_applicability", []),
            "fragment": candidate
        })
    aggregate_hash = content_hash([item["candidate_hash"] for item in candidates])
    return {
        "schema_version": "wanga-source-grounded-fractal-candidates/1.0",
        "status": "CANDIDATE_COMPOSITIONS_BUILT_NOT_SEMANTICALLY_VERIFIED",
        "source_fragment_count": len(fragments),
        "composition_candidate_count": len(candidates),
        "composition_rule_id": rule_id,
        "composition_rule_status": rule["status"],
        "model_hash": aggregate_hash,
        "deterministic_rebuild": all(item["invariants_checked"]["deterministic_rebuild"] for item in candidates),
        "semantic_entailments_claimed": 0,
        "semantic_benchmarks_run": 0,
        "candidates": candidates,
        "limits": [
            "Source text is evidence for what the project protocol states, not proof that the protocol's claims are true.",
            "Type compatibility does not establish semantic entailment, equivalence or causal relation.",
            "No weights are generated; no neural model is trained by this builder."
        ]
    }


def main():
    artifact = build_candidates(ROOT)
    out = ROOT / "research/reports/logic-fractal/source-grounded-fractal-candidates.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({"status": artifact["status"], "candidate_count": artifact["composition_candidate_count"], "model_hash": artifact["model_hash"], "deterministic_rebuild": artifact["deterministic_rebuild"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
