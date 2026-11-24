import torch

from wanga_runtime import (
    DriftGrid6D,
    StructuralNode,
    deterministic_structural_update,
    TiedWeightAdaptiveNeuron,
    HyperNeuron,
    build_hexa_complexes,
    DeterministicSatisfiabilityConsensus,
)


def test_drift_grid_has_six_axes():
    grid = DriftGrid6D(1, 2, 3, 4, 5, 6)
    assert grid.as_tensor().shape == (6,)


def test_structural_update_is_deterministic():
    node = StructuralNode(1, (0.0, 0.0, 0.0))
    ref = StructuralNode(2, (1.0, 0.0, 0.0))
    drift = DriftGrid6D(0.1, 0.02, 0.03, 0.01, 0.04, 0.02)

    a = deterministic_structural_update(
        node=node,
        reference=ref,
        logical_distance=1.5,
        drift=drift,
    )
    b = deterministic_structural_update(
        node=node,
        reference=ref,
        logical_distance=1.5,
        drift=drift,
    )
    assert a.as_dict() == b.as_dict()


def test_tied_weight_reconstruction_shape_and_drift_flag():
    torch.manual_seed(1)
    neuron = TiedWeightAdaptiveNeuron(8, 4)
    x = torch.randn(2, 8)
    result = neuron(x, drift_threshold=1e9)
    assert result["hidden"].shape == (2, 4)
    assert result["reconstruction"].shape == (2, 8)
    assert result["stable"] is True


def test_hyper_neuron_generates_target_weight_shape():
    hyper = HyperNeuron(state_dim=6, weight_shape=(4, 8))
    drift = torch.randn(1, 6)
    candidate = hyper.generate(drift)
    assert candidate.shape == (4, 8)


def test_hexa_complex_is_3_fol_plus_3_sol():
    complexes = build_hexa_complexes()
    assert len(complexes) == 6
    assert sum(c.order == "FOL" for c in complexes) == 3
    assert sum(c.order == "SOL" for c in complexes) == 3
    assert all(len(c.pillars) == 3 for c in complexes)


def test_consensus_is_discrete_and_deterministic():
    consensus = DeterministicSatisfiabilityConsensus()
    result = consensus.decide(
        conditions={"A": False, "B": True, "C": True},
        priorities=("C", "B", "A"),
    )
    assert result["selected"] == "C"
    assert result["is_consistent"] is True
