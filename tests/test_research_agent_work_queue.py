import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run():
    p = subprocess.run(
        [sys.executable, "scripts/build_research_agent_work_queue.py"],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    return json.loads(p.stdout)

def test_network_has_six_specialists_and_orchestrator():
    data = run()
    assert data["agents"] == 7
    assert data["orchestrator"] == "OR-01"

def test_pipeline_dependencies_are_ordered():
    data = run()
    stages = {x["stage"]: x for x in data["stages"]}
    assert stages["FORMALIZATION"]["depends_on"] == ["SOURCE"]
    assert stages["CROSS_CORPUS"]["depends_on"] == ["SOURCE", "FORMALIZATION"]
    assert stages["DELTA"]["depends_on"] == ["SOURCE", "FORMALIZATION", "CROSS_CORPUS", "CLAIM_FORENSICS"]

def test_hard_gates_present():
    data = run()
    assert set(data["gates"]) == {
        "EVIDENCE_CHAIN",
        "STATUS_OWNERSHIP",
        "HISTORICAL_ISOLATION",
        "CORPUS_COVERAGE",
        "NEGATIVE_FINDINGS",
    }
