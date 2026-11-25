from scripts.vitruvius_branch_architecture_orchestrator import (
    OFFICES,
    SLOTS_PER_OFFICE,
    TARGET_TOTAL,
    canonical_family,
)


def test_capacity_model():
    assert len(OFFICES) == 15
    assert SLOTS_PER_OFFICE == 1500
    assert TARGET_TOTAL == 22500


def test_family_routing_examples():
    assert canonical_family("agent/wanga/vitruvius-architecture-graph-automation") == "architecture-intelligence-vitruvius"
    assert canonical_family("agent/codex/fractal-github-neural-network") == "algorithmic-neural-governance"
    assert canonical_family("drift/global-network/evidence-infrastructure") == "ai-drift-forensics"
    assert canonical_family("runtime/nano/virtual-gpu-fabric") == "compute-infrastructure"
    assert canonical_family("unknown/unrelated") is None


def test_specific_family_rules_beat_generic_rules():
    """Regression guard for ordered first-match routing semantics."""
    assert canonical_family("runtime/model-fabric/virtual-gpu") == "compute-infrastructure"
    assert canonical_family("agent/runtime/orchestration") == "compute-infrastructure"
    assert canonical_family("drift/evidence/forensic-audit") == "ai-drift-forensics"
    assert canonical_family("vitruvius/model-fabric-architecture") == "architecture-intelligence-vitruvius"


def test_routing_is_case_insensitive_and_deterministic():
    branch = "AGENT/WANGA/Runtime-Virtual-GPU"
    assert canonical_family(branch) == canonical_family(branch.lower()) == "compute-infrastructure"
