import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("extractor", Path("scripts/run_extractor.py"))
mod = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(mod)

def test_exactly_231_unique_unordered_pairs():
    gates = mod.gate_catalog()
    assert len(gates) == 231
    assert len({g["pair"] for g in gates}) == 231

def test_matrix_is_exact_21_by_11_bijection():
    cells = {(g["matrix_21x11"]["row"], g["matrix_21x11"]["col"]) for g in mod.gate_catalog()}
    assert len(cells) == 231
    assert min(r for r, _ in cells) == 1 and max(r for r, _ in cells) == 21
    assert min(c for _, c in cells) == 1 and max(c for _, c in cells) == 11

def test_no_gate_is_locked_without_verified_semantics():
    assert all(g["ternary_status"] == "ABSTAIN" for g in mod.gate_catalog())

def test_phase_slots_are_bounded_but_not_claimed_as_space_groups():
    gates = mod.gate_catalog()
    assert all(1 <= g["phase_wheel"]["slot_230"] <= 230 for g in gates)
    assert all(g["phase_wheel"]["slot_semantics"].startswith("UNVERIFIED") for g in gates)
