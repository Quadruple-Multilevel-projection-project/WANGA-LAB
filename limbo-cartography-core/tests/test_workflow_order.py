from pathlib import Path


def test_limbo_workflow_rebuilds_generated_map_before_baseline_check():
    repo_root = Path(__file__).resolve().parents[2]
    workflow = (repo_root / ".github" / "workflows" / "daily-limbo-cartography-agent.yml").read_text(encoding="utf-8")
    rebuild = workflow.index("Rebuild existing cumulative map before baseline validation")
    baseline = workflow.index("Validate repository baseline")
    tests = workflow.index("Run software tests")
    assert rebuild < baseline < tests


def test_limbo_workflow_rebuilds_again_after_ingesting_new_records():
    repo_root = Path(__file__).resolve().parents[2]
    workflow = (repo_root / ".github" / "workflows" / "daily-limbo-cartography-agent.yml").read_text(encoding="utf-8")
    tuning = workflow.index("Build bounded tuning candidates from recorded passing retests")
    final_rebuild = workflow.index("Rebuild cumulative iterative crash map and current recorded-state estimate")
    final_validation = workflow.index("Validate resulting state")
    assert tuning < final_rebuild < final_validation
