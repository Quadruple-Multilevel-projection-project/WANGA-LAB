import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_forensic_planner_dry_run():
    p = subprocess.run(
        [sys.executable, "scripts/vitruvius_forensic_research.py"],
        cwd=ROOT, capture_output=True, text=True, check=True
    )
    data = json.loads(p.stdout)
    assert data["tasks"] >= 10
    assert data["mode"] == "dry-run"

def test_forensic_contract_exists():
    assert (ROOT / "vitruvius/VITRUVIUS_FORENSIC_RESEARCH_SPEC_V2.yml").exists()
    assert (ROOT / "vitruvius/VITRUVIUS_FORENSIC_SCHEMA_V1.json").exists()
