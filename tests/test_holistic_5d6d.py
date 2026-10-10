import torch

from wanga_runtime import (
    DynamicNameConfiguration,
    DistributedFractalGraphLayer,
    Holistic5D6DNetwork,
    MetaLogicalLoss,
    build_231_gate_directions,
)


def test_gate_direction_count_and_norm():
    directions = build_231_gate_directions()
    assert len(directions) == 231
    for item in directions:
        vec = torch.tensor(item.vector_5d)
        assert vec.shape == (5,)
        assert torch.isfinite(vec).all()
        assert abs(float(torch.linalg.vector_norm(vec)) - 1.0) < 1e-5


def test_fractal_graph_preserves_node_count():
    layer = DistributedFractalGraphLayer(dim=16)
    x = torch.randn(13, 16)
    y, energy = layer(x, depths=2)
    assert y.shape == x.shape
    assert energy.ndim == 0
    adjacency = layer.ring_adjacency(13)
    assert adjacency.shape == (13, 13)
    assert torch.all(adjacency.sum(dim=1) == 2)


def test_holistic_network_has_ten_evolution_layers():
    model = Holistic5D6DNetwork(dim=16)
    assert len(model.layers) == 10
    assert model.drift_thresholds.shape == (6,)


def test_meta_loss_returns_all_components():
    loss_fn = MetaLogicalLoss()
    source = torch.randn(1, 16)
    reconstruction = torch.randn(1, 16)
    logits = torch.randn(14)
    torsion = torch.randn(1, 6)
    thresholds = torch.tensor([[0.02,0.02,0.03,0.03,0.04,0.01]])
    result = loss_fn(
        source=source,
        reconstruction=reconstruction,
        logic_logits=logits,
        target_gate=1,
        torsion_6d=torsion,
        drift_thresholds=thresholds,
        topology_error=torch.tensor(0.1),
        cycle_error=torch.tensor(0.1),
    )
    assert set(result) == {
        "total",
        "reconstruction",
        "logic",
        "torsion",
        "drift",
        "topology",
        "cycle",
    }
    assert all(torch.isfinite(v) for v in result.values())


def test_holistic_forward_contract():
    model = Holistic5D6DNetwork(dim=16)
    cfg = DynamicNameConfiguration(
        name_id=118,
        letter_combination=(0, 12, 20),
        assigned_space_group=214,
    )
    result = model(cfg)
    assert result["torsion_6d"].shape == (1, 6)
    assert result["state_5d_control"].shape == (1, 5)
    assert result["gate_direction_5d"].shape == (1, 5)
    assert result["logic_logits"].shape == (14,)
    assert 1 <= result["selected_logic_gate"] <= 14
