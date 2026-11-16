#!/usr/bin/env python3
"""Build all Gate XIV x preceding-gate pairs without inferring semantic relations."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "artifacts/book_sentence_registry.json"
ANALYSIS = ROOT / "artifacts/gate14_sentence_structure.json"
OUTPUT = ROOT / "artifacts/gate14_full_relation_matrix.json"
SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"

def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    corpus = read_json(REGISTRY)
    analysis = read_json(ANALYSIS)
    if corpus.get("source", {}).get("commit") != SOURCE_COMMIT:
        raise SystemExit("Pinned source commit mismatch")
    chapters = corpus.get("chapters", [])
    if len(chapters) != 14 or len(analysis.get("units", [])) != 34:
        raise SystemExit("Expected 14 chapters and 34 Gate XIV sentence candidates")
    annotation_by_id = {u["sentence_id"]: u for u in analysis["units"]}
    prior_maps = []
    for chapter in chapters[:13]:
        term_map = {}
        for sentence in chapter["sentence_units"]:
            for term in set(sentence.get("word_tokens", [])):
                term_map.setdefault(term, []).append(sentence["sentence_id"])
        prior_maps.append(term_map)
    cells = []
    for source in chapters[13]["sentence_units"]:
        annotation = annotation_by_id.get(source["sentence_id"], {})
        for gate, prior in enumerate(chapters[:13], 1):
            term_map = prior_maps[gate - 1]
            overlaps = sorted(
                {term for term in source.get("word_tokens", []) if term in term_map}
            )
            overlap_evidence = [
                {"surface_term": term, "prior_sentence_ids": sorted(set(term_map[term]))}
                for term in overlaps
            ]
            links = [link for link in annotation.get("prior_gate_links", []) if link.get("gate") == gate]
            explicit = [link for link in links if link.get("status") == "EXPLICIT_REFERENCE"]
            if explicit:
                structural_status = "EXPLICIT_SCOPE_REFERENCE"
                relation_type = "GLOBAL_SCOPE_REFERENCE"
                evidence = [{"type": link.get("type"), "status": link.get("status"),
                             "source_evidence": link.get("evidence")} for link in explicit]
            elif links:
                structural_status = "STRUCTURAL_LINK_CANDIDATE"
                relation_type = "; ".join(sorted({link.get("type", "UNSPECIFIED") for link in links}))
                evidence = [{"type": link.get("type"), "status": link.get("status"),
                             "source_evidence": link.get("evidence")} for link in links]
            else:
                structural_status = "UNRESOLVED"
                relation_type = None
                evidence = []
            cells.append({
                "gate14_sentence_id": source["sentence_id"],
                "gate14_source_span": {"start_char": source.get("source_start_char"),
                                       "end_char": source.get("source_end_char")},
                "prior_gate": gate,
                "prior_gate_label": prior["chapter_label"],
                "structural_link_status": structural_status,
                "structural_relation_type": relation_type,
                "structural_evidence": evidence,
                "exact_surface_overlap_count": len(overlaps),
                "exact_surface_overlap_terms": overlap_evidence,
                "lexical_overlap_status": "EXACT_SURFACE_OVERLAP" if overlaps else "NO_EXACT_SURFACE_OVERLAP",
                "lexical_overlap_warning": "Exact surface overlap is lexical evidence only and does not establish conceptual identity or a structural relation."
            })
    counts = {}
    for cell in cells:
        status = cell["structural_link_status"]
        counts[status] = counts.get(status, 0) + 1
    lexical_only = sum(c["structural_link_status"] == "UNRESOLVED" and c["exact_surface_overlap_count"] > 0 for c in cells)
    no_overlap = sum(c["structural_link_status"] == "UNRESOLVED" and c["exact_surface_overlap_count"] == 0 for c in cells)
    expected = 34 * 13
    output = {
        "schema": "WANGA_GATE14_FULL_RELATION_MATRIX_V1",
        "work": "מילות ההגיון",
        "target_gate": 14,
        "preceding_gates": list(range(1, 14)),
        "source_commit": SOURCE_COMMIT,
        "status": "COMPLETE_PAIRWISE_MATRIX_STRUCTURAL_LINKS_NOT_VERIFIED",
        "cell_count": len(cells),
        "expected_cell_count": expected,
        "complete_pairwise_coverage": len(cells) == expected,
        "structural_status_counts": counts,
        "unresolved_with_lexical_overlap": lexical_only,
        "unresolved_without_lexical_overlap": no_overlap,
        "policy": {
            "all_pairs_present": True,
            "explicit_scope_reference_distinguished_from_conceptual_relation": True,
            "structural_link_candidates_are_not_verified": True,
            "exact_surface_overlap_is_not_semantic_link": True,
            "unresolved_means_no_structural_link_asserted": True
        },
        "cells": cells
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"], "cell_count": output["cell_count"],
        "expected_cell_count": expected, "structural_status_counts": counts,
        "unresolved_with_lexical_overlap": lexical_only,
        "unresolved_without_lexical_overlap": no_overlap
    }, ensure_ascii=False, indent=2))
    if len(cells) != expected:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
