#!/usr/bin/env python3
"""Build a compact, source-preserving sentence and token registry from the pinned snapshot.

Sentence boundaries are candidates, not verified syntax. This module does not infer
structural links or assign semantic roles to tokens.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "milaot-hahigayon/source/milot_hahigayon_d1106d9a.html"
OUTPUT = ROOT / "artifacts/book_sentence_registry.json"
SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"
HEADING_RE = re.compile(r"<h3[^>]*>\s*שער\s*([^<]+)</h3>", re.I)
FOOTNOTE_RE = re.compile(r'<sup class="footnote-marker">[\s\S]*?</sup>\s*<i class="footnote">[\s\S]*?</i>', re.I)
TAG_RE = re.compile(r"<[^>]+>")
WORD_RE = re.compile(r"[\u0590-\u05FF]+(?:[״׳'־-][\u0590-\u05FF0-9]+)*|[0-9]+|[A-Za-z]+(?:[-'][A-Za-z]+)*", re.UNICODE)
SENTENCE_RE = re.compile(r"(?<=[.!?׃])\s+(?=[\u0590-\u05FFA-Z\"״׳*])", re.UNICODE)

def normalize_fragment(fragment: str) -> str:
    fragment = FOOTNOTE_RE.sub("", fragment)
    fragment = TAG_RE.sub("", fragment)
    fragment = html.unescape(fragment).replace("\xa0", " ")
    return re.sub(r"\s+", " ", fragment).strip()

def main() -> int:
    raw = SOURCE.read_text(encoding="utf-8")
    headings = list(HEADING_RE.finditer(raw))
    if len(headings) != 14:
        raise SystemExit(f"Expected 14 chapter headings; found {len(headings)}")
    chapters = []
    exact = fallback = missing = 0
    for i, match in enumerate(headings):
        end = headings[i + 1].start() if i + 1 < len(headings) else len(raw)
        text = normalize_fragment(raw[match.end():end])
        pieces = [piece.strip() for piece in SENTENCE_RE.split(text) if piece.strip()]
        chapter_number = i + 1
        cursor = 0
        units = []
        for sequence, piece in enumerate(pieces, 1):
            start = text.find(piece, cursor)
            span_status = "EXACT_SUBSTRING_MATCH"
            if start < 0:
                start = text.find(piece)
                span_status = "REPEATED_SUBSTRING_FALLBACK" if start >= 0 else "SPAN_NOT_FOUND"
            exact += span_status == "EXACT_SUBSTRING_MATCH"
            fallback += span_status == "REPEATED_SUBSTRING_FALLBACK"
            missing += span_status == "SPAN_NOT_FOUND"
            if start >= 0:
                cursor = start + len(piece)
            matches = list(WORD_RE.finditer(piece))
            unit = {
                "sentence_id": f"G{chapter_number:02d}-S{sequence:03d}",
                "sequence": sequence,
                "original_text": piece,
                "word_tokens": [m.group(0) for m in matches],
                "word_count": len(matches),
                "source_start_char": start,
                "source_end_char": start + len(piece) if start >= 0 else -1,
                "source_span_status": span_status,
                "segmentation_status": "CANDIDATE_SENTENCE_SEGMENTATION_NOT_VERIFIED",
                "structural_classification": None,
                "cross_references": []
            }
            if chapter_number == 14:
                unit["word_token_spans"] = [{
                    "index": j, "surface": token.group(0),
                    "sentence_start_char": token.start(), "sentence_end_char": token.end(),
                    "chapter_start_char": start + token.start() if start >= 0 else -1,
                    "chapter_end_char": start + token.end() if start >= 0 else -1,
                    "role_status": "UNCLASSIFIED"
                } for j, token in enumerate(matches)]
            units.append(unit)
        chapters.append({
            "chapter": chapter_number,
            "chapter_label": match.group(1).strip(),
            "source_heading": "שער " + match.group(1).strip(),
            "normalized_source_text": text,
            "character_count": len(text),
            "word_count": len(WORD_RE.findall(text)),
            "sentence_candidate_count": len(units),
            "sentence_units": units
        })
    output = {
        "schema": "WANGA_MILAOT_HAHIGAYON_SENTENCE_REGISTRY_V1",
        "work": "מילות ההגיון",
        "attribution": "רמב״ם (כפי שמופיע במקור)",
        "source": {
            "repository": "Sivan22/otzaria-library", "commit": SOURCE_COMMIT,
            "path": "אוצריא/מחשבת ישראל/ראשונים/מילות הגיון.txt",
            "source_snapshot": "milaot-hahigayon/source/milot_hahigayon_d1106d9a.html",
            "raw_source_preserved": True
        },
        "extraction_policy": {
            "source_text_authoritative": True, "source_snapshot_is_raw_html": True,
            "footnote_annotations_removed_from_normalized_text": True,
            "sentence_segmentation": "PUNCTUATION_BASED_CANDIDATE_ONLY",
            "word_tokenization": "UNICODE_HEBREW_LEXICAL_TOKENIZER",
            "source_offsets": "CHARACTER_OFFSETS_IN_NORMALIZED_SOURCE_TEXT",
            "word_token_roles": "UNCLASSIFIED_PENDING_MANUAL_STRUCTURAL_ASSIGNMENT",
            "interpretation_added": False, "structural_classification_added": False,
            "relations_inferred": False
        },
        "status": "SOURCE_SNAPSHOT_CAPTURED_CANDIDATE_SEGMENTATION",
        "chapter_count": len(chapters),
        "total_candidate_sentences": sum(c["sentence_candidate_count"] for c in chapters),
        "total_words": sum(c["word_count"] for c in chapters),
        "offset_validation": {
            "units": sum(c["sentence_candidate_count"] for c in chapters),
            "exact_substring_matches": exact, "fallback_matches": fallback, "not_found": missing
        },
        "chapters": chapters
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"], "chapters": output["chapter_count"],
        "candidate_sentences": output["total_candidate_sentences"], "words": output["total_words"],
        "offset_validation": output["offset_validation"],
        "output": str(OUTPUT.relative_to(ROOT))
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
