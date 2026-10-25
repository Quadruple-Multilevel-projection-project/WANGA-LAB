#!/usr/bin/env python3
"""Create source-offset clause candidates for Gate XIV; no syntax is inferred."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ANALYSIS = ROOT / "artifacts/gate14_sentence_structure.json"
REGISTRY = ROOT / "artifacts/book_sentence_registry.json"
OUTPUT = ROOT / "artifacts/gate14_clause_registry.json"
SOURCE_COMMIT = "d1106d9a66528dc3e39cf1ea0732782927d9f678"
WORD_RE = re.compile(r"[\u0590-\u05FF]+(?:[״׳'־-][\u0590-\u05FF0-9]+)*|[0-9]+|[A-Za-z]+(?:[-'][A-Za-z]+)*", re.UNICODE)
SPLIT_RE = re.compile(r";|:|׃|,(?=\s+(?:ואם|אבל|אלא|או|כי|עד|ולא|ולפעמים|והוא|והיא|ואשר|כאשר|לפי|במה|גם|ולכן|אחרי|אשר)\s+)", re.UNICODE)

def boundary_kind(marker: str) -> str:
    return {";": "SEMICOLON", ":": "COLON", "׃": "SOF_PASUQ"}.get(marker, "COMMA_BEFORE_CONNECTIVE")

def main() -> int:
    analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry.get("source", {}).get("commit") != SOURCE_COMMIT:
        raise SystemExit("Pinned source commit mismatch")
    source_text = registry["chapters"][13]["normalized_source_text"]
    clauses = []
    span_failures = 0
    for sentence in analysis.get("units", []):
        text = sentence["original_text"]
        base = sentence["source_span"]["start_char"]
        start = 0
        seq = 1
        for match in SPLIT_RE.finditer(text):
            end = match.end()
            raw = text[start:end]
            leading = len(raw) - len(raw.lstrip())
            trailing = len(raw) - len(raw.rstrip())
            local_start = start + leading
            local_end = end - trailing
            clause_text = text[local_start:local_end]
            if clause_text:
                absolute_start = base + local_start
                absolute_end = base + local_end
                exact = source_text[absolute_start:absolute_end] == clause_text
                span_failures += not exact
                tokens = [{
                    "index": i,
                    "surface": token.group(0),
                    "start_char": absolute_start + token.start(),
                    "end_char": absolute_start + token.end()
                } for i, token in enumerate(WORD_RE.finditer(clause_text))]
                clauses.append({
                    "clause_id": f'{sentence["sentence_id"]}-C{seq:02d}',
                    "sentence_id": sentence["sentence_id"],
                    "source_span": {"start_char": absolute_start, "end_char": absolute_end},
                    "original_text": clause_text,
                    "word_token_count": len(tokens),
                    "word_tokens": tokens,
                    "boundary_after": boundary_kind(match.group(0)),
                    "source_span_status": "EXACT" if exact else "MISMATCH",
                    "boundary_status": "PUNCTUATION_BASED_CANDIDATE_NOT_SYNTAX_VERIFIED",
                    "structural_role_status": "UNCLASSIFIED_PENDING_CLAUSE_REVIEW"
                })
                seq += 1
            start = match.end()
            while start < len(text) and text[start].isspace():
                start += 1
        raw = text[start:]
        leading = len(raw) - len(raw.lstrip())
        trailing = len(raw) - len(raw.rstrip())
        local_start = start + leading
        local_end = len(text) - trailing
        clause_text = text[local_start:local_end]
        if clause_text:
            absolute_start = base + local_start
            absolute_end = base + local_end
            exact = source_text[absolute_start:absolute_end] == clause_text
            span_failures += not exact
            tokens = [{
                "index": i,
                "surface": token.group(0),
                "start_char": absolute_start + token.start(),
                "end_char": absolute_start + token.end()
            } for i, token in enumerate(WORD_RE.finditer(clause_text))]
            clauses.append({
                "clause_id": f'{sentence["sentence_id"]}-C{seq:02d}',
                "sentence_id": sentence["sentence_id"],
                "source_span": {"start_char": absolute_start, "end_char": absolute_end},
                "original_text": clause_text,
                "word_token_count": len(tokens),
                "word_tokens": tokens,
                "boundary_after": "END_OF_SENTENCE",
                "source_span_status": "EXACT" if exact else "MISMATCH",
                "boundary_status": "PUNCTUATION_BASED_CANDIDATE_NOT_SYNTAX_VERIFIED",
                "structural_role_status": "UNCLASSIFIED_PENDING_CLAUSE_REVIEW"
            })
    word_count = sum(c["word_token_count"] for c in clauses)
    expected_words = sum(u["word_token_count"] for u in analysis["units"])
    output = {
        "schema": "WANGA_GATE14_CLAUSE_CANDIDATE_REGISTRY_V1",
        "work": "מילות ההגיון",
        "target_gate": 14,
        "source_commit": SOURCE_COMMIT,
        "status": "CANDIDATE_CLAUSE_SEGMENTATION_NOT_VERIFIED",
        "policy": {
            "source_text_preserved": True,
            "split_rules": "SEMICOLON_COLON_SOF_PASUQ_AND_COMMA_BEFORE_SELECTED_CONNECTIVES",
            "boundaries_are_candidates": True,
            "no_semantic_relations_inferred": True,
            "word_offsets_use_normalized_gate14_source_text": True
        },
        "sentence_candidate_count": len(analysis["units"]),
        "clause_candidate_count": len(clauses),
        "word_token_count": word_count,
        "expected_word_token_count": expected_words,
        "token_coverage_complete": word_count == expected_words,
        "source_span_failures": span_failures,
        "clauses": clauses
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": output["status"], "sentences": output["sentence_candidate_count"],
        "clauses": output["clause_candidate_count"], "word_tokens": word_count,
        "expected_word_tokens": expected_words, "span_failures": span_failures
    }, ensure_ascii=False, indent=2))
    return 0 if word_count == expected_words and span_failures == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
