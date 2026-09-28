import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def run():
    p = subprocess.run([sys.executable, "scripts/vitruvius_forensic_research.py"], cwd=ROOT, capture_output=True, text=True, check=True)
    return json.loads(p.stdout)

def test_forensic_planner_dry_run():
    data = run()
    assert data["mode"] == "dry-run"
    assert data["tasks"] >= 100
    assert data["books"] == 10
    assert data["concepts"] >= 20
    assert data["relations"] >= 10

def test_forensic_contract_exists():
    assert (ROOT / "vitruvius/VITRUVIUS_FORENSIC_RESEARCH_SPEC_V3.yml").exists()
    assert (ROOT / "vitruvius/VITRUVIUS_FORENSIC_SCHEMA_V2.json").exists()

def test_claims_are_isolated():
    data = run()
    ids = {t["task_id"] for t in data["tasks"]}
    assert "VIT-CLAIM-50-CHAPTERS" in ids
    assert "VIT-CLAIM-32-CORE" in ids

def test_all_representations_are_tested():
    data = run()
    reps = {t["representation"] for t in data["tasks"] if t["track"] == "representation_test"}
    assert reps == {"GRAPH","HYPERGRAPH","DAG","TREE","RELATION_MATRIX"}
