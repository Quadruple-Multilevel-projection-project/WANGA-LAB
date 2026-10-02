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
