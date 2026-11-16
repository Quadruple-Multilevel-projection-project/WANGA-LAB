#!/usr/bin/env python3
"""Prioritize unresolved Gate XIV pairs with content-term overlap; never promote links."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "artifacts/gate14_full_relation_matrix.json"
OUTPUT = ROOT / "artifacts/gate14_relation_review_queue.json"
SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"
STOPWORDS = set("""הוא היא הם הן זה זאת זו אלה אלו כל הכל לא אלא אם כי גם או אך אבל עד אשר של שלו שלה שלהם על אל מן עם בין לפי כמו אחרי לפני אז מה מי כן עוד רק יותר פחות כך שכן שלא לכן הרי אף הנה יש אין היה היו הייתה היות והוא והיא ואשר ואם ולא ולכן וגם וכו וכו׳ מהן מהם אותו אותם אנו אנחנו אני אתה את היי יהיה ויהי הזה הזאת כלל מכל שאר אחר אחרת לכולם לכל בכל במכל הדבר דברים""".split())

def main() -> int:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    if matrix.get("source_commit") != SOURCE_COMMIT:
        raise SystemExit("Pinned source commit mismatch")
    items = []
    no_surface = 0
    only_stopwords = 0
    for cell in matrix.get("cells", []):
        if cell.get("structural_link_status") != "UNRESOLVED":
            continue
        overlaps = cell.get("exact_surface_overlap_terms", [])
        if not overlaps:
            no_surface += 1
            continue
        content = [t for t in overlaps if t.get("surface_term") not in STOPWORDS
                   and len(t.get("surface_term", "")) > 1
                   and not re.fullmatch(r"\d+", t.get("surface_term", ""))]
        if not content:
            only_stopwords += 1
            continue
        items.append({
            "review_id": f'{cell["gate14_sentence_id"]}-TO-G{cell["prior_gate"]:02d}',
            "gate14_sentence_id": cell["gate14_sentence_id"],
            "gate14_source_span": cell["gate14_source_span"],
            "prior_gate": cell["prior_gate"],
            "prior_gate_label": cell["prior_gate_label"],
            "structural_link_status": "UNRESOLVED",
            "review_status": "UNREVIEWED_CONTENT_TERM_OVERLAP",
            "candidate_terms": content,
            "exact_overlap_count": cell["exact_surface_overlap_count"],
            "source_sentence_reference": "artifacts/gate14_sentence_structure.json#" + cell["gate14_sentence_id"],
            "prior_sentence_references": sorted({sid for term in content for sid in term["prior_sentence_ids"]}),
            "rule": "Exact surface content-term overlap after configurable stopword filtering; no conceptual relation asserted.",
            "promotion_rule": "Do not promote to STRUCTURAL_LINK_CANDIDATE without source-grounded structural evidence."
        })
    unresolved = matrix.get("structural_status_counts", {}).get("UNRESOLVED", 0)
    output = {
        "schema": "WANGA_GATE14_UNRESOLVED_RELATION_REVIEW_QUEUE_V1",
        "work": "מילות ההגיון",
        "target_gate": 14,
        "source_commit": SOURCE_COMMIT,
        "status": "LEXICAL_REVIEW_QUEUE_NOT_STRUCTURAL_LINKS",
        "full_matrix_cell_count": matrix.get("cell_count", 0),
        "unresolved_pair_count": unresolved,
        "review_item_count": len(items),
        "unresolved_no_surface_overlap": no_surface,
        "unresolved_only_stopword_overlap": only_stopwords,
        "unresolved_with_content_term_overlap": len(items),
        "policy": {
            "queue_items_are_not_verified_links": True,
            "exact_surface_overlap_is_not_semantic_relation": True,
            "stopword_filter_is_configurable": True,
            "source_sentence_references_preserved": True
        },
        "items": sorted(items, key=lambda item: (-len(item["candidate_terms"]), item["gate14_sentence_id"], item["prior_gate"]))
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"], "full_matrix_cell_count": output["full_matrix_cell_count"],
        "unresolved_pairs": unresolved, "review_items": len(items),
        "unresolved_with_content_term_overlap": len(items),
        "unresolved_only_stopword_overlap": only_stopwords,
        "unresolved_no_surface_overlap": no_surface
    }, ensure_ascii=False, indent=2))
    if len(items) + only_stopwords + no_surface != unresolved:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
