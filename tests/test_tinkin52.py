from __future__ import annotations

import json
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "wanga_runtime" / "tinkin52.py"

spec = importlib.util.spec_from_file_location("tinkin52", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

Tinkin52 = mod.Tinkin52
WHEEL_DEFINITIONS = mod.WHEEL_DEFINITIONS


def test_exact_52_networks():
    machine = Tinkin52()
    assert len(machine.networks) == 52
    assert [sum(n.layer == i for n in machine.networks) for i in range(4)] == [13, 13, 13, 13]
    assert all(len(n.gates) == 33 for n in machine.networks)


def test_topology_totals():
    machine = Tinkin52()
    assert machine.topology == {
        "networks": 52,
        "layers": 4,
        "networks_per_layer": 13,
        "wheels": 156,
        "gates": 1716,
        "letter_endpoints": 3432,
    }
    assert all(len(pairs) == 11 for pairs in WHEEL_DEFINITIONS.values())


def test_replay_is_deterministic():
    a = Tinkin52()
    b = Tinkin52()
    ra = a.export(a.step())
    rb = b.export(b.step())
    assert json.dumps(ra, sort_keys=True, ensure_ascii=False) == json.dumps(
        rb, sort_keys=True, ensure_ascii=False
    )


def test_invalid_signal_creates_mismatch():
    machine = Tinkin52()
    result = machine.step([("א", "ת")])
    assert result.global_drift >= 0
    assert len(result.networks) == 52
    assert any(state.local_drift > 0 for state in result.networks)


def test_c0_and_axes_exist():
    result = Tinkin52().step()
    assert result.c0_status in {"BALANCED", "DRIFT_ALERT", "COMPENSATING"}
    assert set(result.axes) == {
        "alpha_up",
        "beta_down",
        "gamma_forward",
        "delta_backward",
        "epsilon_noise",
        "zeta_anomaly",
    }


def test_architecture_contract():
    machine = Tinkin52()
    contract = machine.architecture_contract()
    assert contract["envelope"]["vertices"] == 13
    assert contract["envelope"]["spatiotemporal_dimensions"] == 4
    assert len(contract["nested_levels"]) == 5
    assert contract["logic"]["declared_terms"] == 175
    assert contract["logic"]["computed_from_gate_counts"] == 188
    assert contract["logic"]["count_delta"] == 13
    assert contract["logic"]["count_consistent"] is False


def test_231_gate_registry_and_pending_groups():
    from importlib.util import spec_from_file_location, module_from_spec

    op_path = ROOT / "wanga_runtime" / "space_group_layer.py"
    spec2 = spec_from_file_location("space_group_layer_test", op_path)
    assert spec2 and spec2.loader
    op = module_from_spec(spec2)
    spec2.loader.exec_module(op)

    gates = op.build_231_global_gates()
    assert len(gates) == 231
    assert len({(g.letter_a, g.letter_b) for g in gates}) == 231

    registry = op.GateSpaceGroupRegistry(gates=gates)
    report = registry.validate()
    assert report["global_gate_count"] == 231
    assert report["space_group_slots"] == 230
    assert report["pending_space_group_payloads"] == 230

    with __import__("pytest").raises(ValueError):
        registry.get_group(231).apply((0.0, 0.0, 0.0))


def test_nested_configuration_bounds():
    from importlib.util import spec_from_file_location, module_from_spec

    op_path = ROOT / "wanga_runtime" / "space_group_layer.py"
    spec2 = spec_from_file_location("space_group_layer_config_test", op_path)
    assert spec2 and spec2.loader
    op = module_from_spec(spec2)
    spec2.loader.exec_module(op)

    cfg = op.NestedConfiguration(
        nesting_level=2,
        base_elements=(1, 50),
        space_group_id=45,
    )
    assert cfg.as_dict()["space_group_id"] == 45
