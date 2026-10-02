from wanga_runtime import (
    DynamicNameConfiguration,
    MaimonidesCombinatorialCrystalNetwork,
    SeferHaTzirufManifold,
)


def test_tziruf_generation_is_reproducible():
    source = SeferHaTzirufManifold()
    a = source.generate_name_weights(777)
    b = source.generate_name_weights(777)
    assert a == b
    assert len(a) == 3
    assert all(0 <= x < 22 for x in a)


def test_dynamic_name_routes_to_fourteen_gates():
    model = MaimonidesCombinatorialCrystalNetwork()
    config = DynamicNameConfiguration(
        name_id=999,
        letter_combination=(0, 11, 4),
        assigned_space_group=214,
    )
    result = model.process_dynamic_name(config)
    probs = result["gate_probabilities"]
    assert probs.shape == (14,)
    assert abs(float(probs.sum()) - 1.0) < 1e-6
    assert 1 <= result["routing_gate"] <= 14
    assert result["outer_gate_slot_count"] == 231
    assert result["space_group_slot_count"] == 230
    assert result["verification_state"] == "NOT_YET_VERIFIED"


def test_source_mapping_does_not_get_invented():
    model = MaimonidesCombinatorialCrystalNetwork()
    assert model.outer_gate_slot_ids.numel() == 231
    assert model.space_group_slot_ids.numel() == 230


def test_reversible_three_letter_routing():
    from wanga_runtime import DynamicNameConfiguration, ReversibleCombinatorialRouter

    router = ReversibleCombinatorialRouter()
    config = DynamicNameConfiguration(
        name_id=118,
        letter_combination=(0, 12, 20),  # א מ ת
        assigned_space_group=214,
    )

    route = router.route(config)
    assert 1 <= route.gate_id <= 231
    assert 0 <= route.residual <= 46
    assert 1 <= route.space_group_slot <= 230

    reconstructed = router.reconstruct(route)
    assert reconstructed.letter_combination == config.letter_combination


def test_all_22_cube_index_space_is_lossless():
    from wanga_runtime import decode_triple, encode_triple

    seen = set()
    for a in range(22):
        for b in range(22):
            for c in range(22):
                code = encode_triple((a, b, c))
                assert decode_triple(code) == (a, b, c)
                seen.add(code)

    assert len(seen) == 22 ** 3
