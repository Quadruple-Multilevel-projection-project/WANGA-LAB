#!/usr/bin/env python3
"""Deterministic forensic planner for the Vitruvius daily research agent.

It expands the existing daily queue with full ten-book coverage, source discovery,
formal-kernel extraction, composition tests, representation tests, and isolated
claim verification. It plans searches; it does not decide historical truth.
"""

from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "vitruvius" / "VITRUVIUS_FORENSIC_RESEARCH_SPEC_V3.yml"
OUT = ROOT / "vitruvius" / "VITRUVIUS_FORENSIC_WORK_QUEUE.json"

BOOK_TOPICS = {
  1:["architecture_definition","architectural_principles","education","knowledge_domains","site_and_material_context"],
  2:["origins_of_building","materials","construction_methods","natural_materials"],
  3:["temple_principles","symmetry","proportion","module","human_body_analogy"],
  4:["orders","temple_forms","origin_and_classification","codex_organization"],
  5:["public_buildings","forums","basilicas","theatres","acoustics","waterfront_or_port_context"],
  6:["private_houses","site_adaptation","symmetry","proportion","diminutions","additions"],
  7:["materials","finishes","pigments","waterproofing_or_surface_methods"],
  8:["water","aqueducts","hydraulics","quality","measurement"],
  9:["astronomy","sundials","numbers","geometry","music_or_harmonics"],
  10:["machines","mechanics","lifting","water_machines","pneumatics_or_related_devices"],
}
CONCEPTS = [
  "firmitas","utilitas","venustas","ordinatio","dispositio","eurythmia",
  "symmetria","decor","distributio","proportion","module","ratio","geometry",
  "number","music","acoustics","optics","water","mechanics","machines",
  "urban planning","temples","public buildings","housing","materials",
  "construction","planning methods",
]
RELATIONS = ["part_whole","measure_standard","proportional","symmetric","ordered","arranged","contextual","functional","dependency","transformation","constraint","sequence","representation"]
REPRESENTATIONS = ["GRAPH","HYPERGRAPH","DAG","TREE","RELATION_MATRIX"]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def rid(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def task(task_id, track, query, **extra):
    return {"task_id": task_id, "track": track, "query": query, **extra}

def make_tasks() -> list[dict]:
    tasks = []
    for book in range(1, 11):
        tasks.append(task(
            f"VIT-CORPUS-B{book}", "corpus_structure",
            f'De Architectura Book {book} chapters Vitruvius primary text critical edition translation',
            book=book,
            required_evidence=["book_identity","chapter_boundaries","edition_or_primary_locator"],
            acceptance=["chapter boundaries recorded","edition identified","stable locator recorded"],
        ))
        for topic in BOOK_TOPICS[book]:
            tasks.append(task(
                f"VIT-BOOK-{book}-{rid(topic)}", "book_level_coverage",
                f'Vitruvius De Architectura Book {book} "{topic}" primary text scholarly',
                book=book, topic=topic,
                required_evidence=["book","chapter","source_locator"],
                acceptance=["topic occurrence or explicit negative finding","provenance preserved"],
            ))

    for concept in CONCEPTS:
        tasks.append(task(
            f"VIT-CONCEPT-{rid(concept)}", "concept_extraction",
            f'Vitruvius De Architectura "{concept}" primary text context definition relation',
            concept=concept, required_evidence=["book","chapter","source_locator"],
            acceptance=["unit extracted or negative finding","relation candidates recorded","provenance preserved"],
        ))

    for relation in RELATIONS:
        tasks.append(task(
            f"VIT-REL-{rid(relation)}", "relation_extraction",
            f'Vitruvius De Architectura {relation} units parts whole proportion arrangement',
            relation=relation,
            acceptance=["source span recorded","relation status classified"],
        ))

    for layer in ["UNITS","RELATIONS","ORDER","ARRANGEMENT","MODULE","PROPORTION","SYMMETRY","COMPOSITION","TRANSFORMATION","VALIDATION"]:
        tasks.append(task(
            f"VIT-KERNEL-{layer}", "vitruvius_logic_kernel",
            f'Vitruvius De Architectura {layer.lower()} source grounded structure',
            kernel_layer=layer,
            acceptance=["historical concept separated from modern label","source or derivation recorded"],
        ))

    tasks += [
        task("VIT-COMP-LEVEL-1","composition_tests","Vitruvius units relations combinations parts whole",composition_level="units_to_combinations"),
        task("VIT-COMP-LEVEL-2","composition_tests","Vitruvius combinations composition of compositions",composition_level="compositions_of_compositions"),
        task("VIT-CORRESPONDENCE","composition_tests","Vitruvius structural correspondence preserved relations","acceptance":["correspondence relation named","evidence refs retained"]),
        task("VIT-CLAIM-50-CHAPTERS","forensic_claim",'"De Architectura" "50 chapters" Vitruvius',
             claim="De Architectura has 50 chapters",
             method="reconcile actual chapter boundaries across books and editions; never infer from a secondary summary",
             result_states=["SUPPORTED","NOT_SUPPORTED","EDITION_DEPENDENT","UNRESOLVED"]),
        task("VIT-CLAIM-32-CORE","forensic_claim",'"Vitruvius" "32-core" architecture',
             claim="32-core", isolation_rule=True,
             method="search primary corpus, scholarly literature, and WANGA-internal records as separate evidence pools",
             result_states=["SUPPORTED","NOT_SUPPORTED","UNRESOLVED","WANGA_INTERNAL_ONLY"]),
        task("VIT-COMP-MAIMONIDES","comparative","Vitruvius Maimonides structural comparison order proportion composition",
             method="compare extracted structures only; preserve independent provenance"),
        task("VIT-COMP-WANGA","comparative","Vitruvius WANGA structural correspondence architecture codex",
             method="compare source-derived structures with WANGA interfaces; similarity is not implementation evidence"),
    ]
    for rep in REPRESENTATIONS:
        tasks.append(task(
            f"VIT-REP-{rep}", "representation_test",
            f'Vitruvius De Architectura {rep} structural representation',
            representation=rep,
            acceptance=["input provenance retained","status classified as observed/derived/hypothesis/not_supported"],
        ))

    return tasks

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true")
    args = p.parse_args()
    queue = {
        "schema_version":"2.0.0",
        "generated_at":now(),
        "spec":str(SPEC.relative_to(ROOT)),
        "agent_policy":{
            "existing_daily_agent":"RETAIN_ACTIVE",
            "mode":"INCREMENTAL_FORENSIC_RESEARCH",
            "truth_authority":"SOURCE_EVIDENCE_ONLY",
            "structural_similarity_is_proof":False,
            "modern_formalization_is_historical_attribution":False,
            "negative_findings_are_first_class":True,
        },
        "coverage":{
            "books":list(range(1,11)),
            "book_topics":BOOK_TOPICS,
            "concepts":len(CONCEPTS),
            "relations":len(RELATIONS),
            "representations":REPRESENTATIONS,
        },
        "tasks":make_tasks(),
    }
    if args.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(queue, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"mode":"write" if args.write else "dry-run","tasks":len(queue["tasks"]),"books":10,"concepts":len(CONCEPTS),"relations":len(RELATIONS)}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
