#!/usr/bin/env python3
"""Deterministic forensic planner for the Vitruvius daily research agent.

This component does not decide historical truth. It generates bounded search
queries, validation tasks, and evidence-state transitions from the active
research specification.
"""

from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "vitruvius" / "VITRUVIUS_FORENSIC_RESEARCH_SPEC_V2.yml"
OUT = ROOT / "vitruvius" / "VITRUVIUS_FORENSIC_WORK_QUEUE.json"

BOOKS = list(range(1, 11))
CONCEPTS = [
    "firmitas", "utilitas", "venustas", "ordinatio", "dispositio",
    "eurythmia", "symmetria", "decor", "distributio", "proportion",
    "module", "ratio", "geometry", "number", "music", "acoustics",
    "optics", "water", "mechanics", "machines", "urban planning",
    "temples", "public buildings", "housing", "materials",
    "construction", "planning methods",
]
REPRESENTATIONS = ["GRAPH", "HYPERGRAPH", "DAG", "TREE", "RELATION_MATRIX"]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rid(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def make_tasks() -> list[dict]:
    tasks = []
    for book in BOOKS:
        tasks.append({
            "task_id": f"VIT-CORPUS-B{book}",
            "track": "corpus_structure",
            "book": book,
            "query": f'De Architectura Book {book} chapters Vitruvius primary text edition',
            "required_evidence": ["edition_or_primary_text_locator"],
            "acceptance": ["book identity verified", "chapter boundaries recorded", "edition identified"],
        })
    for concept in CONCEPTS:
        tasks.append({
            "task_id": f"VIT-CONCEPT-{rid(concept)}",
            "track": "concept_extraction",
            "concept": concept,
            "query": f'Vitruvius De Architectura "{concept}" primary text context',
            "required_evidence": ["book", "chapter", "source_locator"],
            "acceptance": ["unit extracted", "relation candidates recorded", "provenance preserved"],
        })
    tasks += [
        {
            "task_id": "VIT-CLAIM-50-CHAPTERS",
            "track": "forensic_claim",
            "claim": "De Architectura has 50 chapters",
            "query": '"De Architectura" "50 chapters" Vitruvius',
            "method": "reconcile actual chapter boundaries across editions/translations; do not infer count from a secondary summary",
            "result_states": ["SUPPORTED", "NOT_SUPPORTED", "EDITION_DEPENDENT", "UNRESOLVED"],
        },
        {
            "task_id": "VIT-CLAIM-32-CORE",
            "track": "forensic_claim",
            "claim": "32-core",
            "query": '"Vitruvius" "32-core" architecture',
            "method": "locate an explicit source and context; classify as historical, scholarly, technical, or WANGA-internal",
            "result_states": ["SUPPORTED", "NOT_SUPPORTED", "UNRESOLVED", "WANGA_INTERNAL_ONLY"],
        },
        {
            "task_id": "VIT-COMP-MAIMONIDES",
            "track": "comparative",
            "query": "Vitruvius Maimonides structural comparison order proportion logic",
            "method": "compare extracted structures only; never transfer attribution or proof status",
        },
        {
            "task_id": "VIT-COMP-WANGA",
            "track": "comparative",
            "query": "Vitruvius WANGA architecture structural correspondence",
            "method": "compare source-derived structures to WANGA interfaces; similarity is not implementation evidence",
        },
    ]
    for rep in REPRESENTATIONS:
        tasks.append({
            "task_id": f"VIT-REP-{rep}",
            "track": "representation_test",
            "representation": rep,
            "method": "attempt a representation from extracted units/relations and record fit or failure",
            "acceptance": ["input provenance retained", "mapping classified as observed/derived/hypothesis/not_supported"],
        })
    return tasks

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    queue = {
        "schema_version": "1.0.0",
        "generated_at": now(),
        "spec": str(SPEC.relative_to(ROOT)),
        "agent_policy": {
            "existing_daily_agent": "RETAIN_ACTIVE",
            "mode": "INCREMENTAL_FORENSIC_RESEARCH",
            "truth_authority": "SOURCE_EVIDENCE_ONLY",
            "structural_similarity_is_proof": False,
        },
        "tasks": make_tasks(),
    }
    if args.write:
        OUT.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"mode": "write" if args.write else "dry-run", "tasks": len(queue["tasks"])}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
