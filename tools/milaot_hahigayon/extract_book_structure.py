#!/usr/bin/env python3
"""Rebuild source-preserving sentence candidates from the pinned source snapshot.
Sentence boundaries and tokens are candidates; this tool does not interpret or verify relations.
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
    matches = list(HEADING_RE.finditer(raw))
    if len(matches) != 14:
        raise SystemExit(f"Expected 14 chapter headings; found {len(matches)}")
    chapters = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        fragment = raw[match.end():end]
        text = normalize_fragment(fragment)
        pieces = [p.strip() for p in SENTENCE_RE.split(text) if p.strip()]
        number = i + 1
        units = []
        for j, piece in enumerate(pieces, 1):
            words = WORD_RE.findall(piece)
            units.append({
                "sentence_id": f"G{number:02d}-S{j:03d}",
                "sequence": j,
                "original_text": piece,
                "whitespace_tokens": piece.split(),
                "word_tokens": words,
                "word_count": len(words),
                "segmentation_status": "CANDIDATE_SENTENCE_SEGMENTATION_NOT_VERIFIED",
                "structural_classification": None,
                "cross_references": []
            })
        chapters.append({
            "chapter": number,
            "chapter_label": match.group(1).strip(),
            "source_heading": "שער " + match.group(1).strip(),
            "source_html_fragment": fragment,
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
            "repository": "Sivan22/otzaria-library",
            "commit": SOURCE_COMMIT,
            "path": "אוצריא/מחשבת ישראל/ראשונים/מילות הגיון.txt",
            "source_snapshot": "milaot-hahigayon/source/milot_hahigayon_d1106d9a.html",
            "raw_source_preserved": True
        },
        "extraction_policy": {
            "source_text_authoritative": True,
            "source_snapshot_is_raw_html": True,
            "footnote_annotations_removed_from_normalized_text": True,
            "sentence_segmentation": "PUNCTUATION_BASED_CANDIDATE_ONLY",
            "word_tokenization": "UNICODE_HEBREW_LEXICAL_TOKENIZER",
            "interpretation_added": False,
            "structural_classification_added": False,
            "relations_inferred": False
        },
        "status": "SOURCE_SNAPSHOT_CAPTURED_CANDIDATE_SEGMENTATION",
        "chapter_count": len(chapters),
        "total_candidate_sentences": sum(c["sentence_candidate_count"] for c in chapters),
        "total_words": sum(c["word_count"] for c in chapters),
        "chapters": chapters
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"],
        "chapters": output["chapter_count"],
        "candidate_sentences": output["total_candidate_sentences"],
        "words": output["total_words"],
        "output": str(OUTPUT.relative_to(ROOT))
    }, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
