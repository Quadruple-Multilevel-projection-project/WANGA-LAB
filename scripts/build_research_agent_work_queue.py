#!/usr/bin/env python3
"""Build the deterministic work queue for the six-agent research network.

This planner routes work only. It does not perform research, verify claims,
or promote evidence statuses.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "vitruvius" / "RESEARCH_AGENT_WORK_QUEUE.json"

STAGES = [
    ("SOURCE", ["VIT-SOURCE", "RAMBAM-SOURCE"], []),
    ("FORMALIZATION", ["FORMALIZER"], ["SOURCE"]),
    ("CROSS_CORPUS", ["CROSS-CORPUS"], ["SOURCE", "FORMALIZATION"]),
    ("CLAIM_FORENSICS", ["CLAIM-FORENSIC"], ["SOURCE"]),
    ("DELTA", ["DELTA-REPORTER"], ["SOURCE", "FORMALIZATION", "CROSS_CORPUS", "CLAIM_FORENSICS"]),
]

def now() -> str:
    return datetime.now(timezone.utc).isoformat()

def main() -> int:
    queue = {
        "schema_version": "1.0.0",
        "generated_at": now(),
        "orchestrator": "OR-01",
        "source_of_truth": "agents/AGENT_RESPONSIBILITY_MATRIX_V1.yaml",
        "mode": "ROUTE_ONLY",
        "stages": [
            {"stage": stage, "agents": agents, "depends_on": deps}
            for stage, agents, deps in STAGES
        ],
        "gates": [
            "EVIDENCE_CHAIN",
            "STATUS_OWNERSHIP",
            "HISTORICAL_ISOLATION",
            "CORPUS_COVERAGE",
            "NEGATIVE_FINDINGS",
        ],
    }
    OUT.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"stages": len(STAGES), "agents": 7, "mode": "ROUTE_ONLY"}))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
