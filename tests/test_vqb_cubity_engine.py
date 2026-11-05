import pytest

from engine.quantum_bridge import (
    LanguagePoint,
    map_to_5d_ring,
    merge_three_language_points,
    unified_language_point,
)
from engine.vqb_cubity_engine import (
    DEFAULT_COMMAND,
    DEFAULT_MODE,
    SUB_SPACE_COUNT,
    VQBCubityEngine,
    build_eulerian_sub_spaces,
)


def test_unified_language_point_fuses_three_vectors_by_mean():
    point = unified_language_point([1, 2], [2, 3], [3, 4])
    assert point.vector == (2.0, 3.0)


def test_unified_language_point_rejects_dimension_mismatch():
    with pytest.raises(ValueError):
        unified_language_point([1, 2], [1], [1, 2])


def test_fixed_point_merge_requires_exactly_three_points_and_converges():
    result = merge_three_language_points([
        LanguagePoint((0.2, -0.8)),
        LanguagePoint((0.3, -0.6)),
        LanguagePoint((0.1, -0.7)),
    ])
    assert result.converged is True
    assert result.iterations >= 1
    assert result.point.vector[0] > 0.99
    assert result.point.vector[1] < -0.99
    with pytest.raises(ValueError):
        merge_three_language_points([LanguagePoint((1.0,))])


def test_five_dimensional_ring_mapping():
    ring = map_to_5d_ring(LanguagePoint((1, 0, 0, 1, 0)))
    assert len(ring.coordinates) == 5
    assert all(isinstance(value, float) for value in ring.coordinates)


def test_graph_has_36_spaces_with_inner_and_outer_nodes_and_edges():
    spaces = build_eulerian_sub_spaces()
    assert len(spaces) == SUB_SPACE_COUNT == 36
    assert len({space.internal_node_id for space in spaces}) == 36
    assert len({space.external_node_id for space in spaces}) == 36
    assert all(space.neighbor_ids for space in spaces)
    assert all(space.self_similar_template_ref == "VQB_36_TEMPLATE" for space in spaces)
    assert all(1 <= neighbor <= 36 for space in spaces for neighbor in space.neighbor_ids)
    assert all(space.sub_space_id not in space.neighbor_ids for space in spaces)


def test_120_step_simulation_visits_all_36_spaces_and_generates_120_commands():
    report = VQBCubityEngine().simulate(120)
    assert report.sub_spaces_configured == 36
    assert report.unique_sub_spaces_visited == 36
    assert report.language_points_merged == 120
    assert report.composite_points_merged == 40
    assert report.commands_generated == 120
    assert len(report.commands) == 120
    assert all(command.command == DEFAULT_COMMAND for command in report.commands)
    assert all(command.mode == DEFAULT_MODE for command in report.commands)
    assert all(command.state == "TUNNELED" and command.time_jump for command in report.commands)
    assert all(command.visibility == ("ON", "OFF") for command in report.commands)
    assert all(len(command.ring_5d) == 5 for command in report.commands)


def test_simulation_requires_triplets_for_composite_merges():
    with pytest.raises(ValueError):
        VQBCubityEngine().simulate(5)
