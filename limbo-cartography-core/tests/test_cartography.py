from engine.axiomatic_stress_tester import evaluate_case


def test_keystone_case_records_structure_change_without_claiming_truth():
    case = {
        "case_id": "SYNTHETIC-CASE-001",
        "candidate_id": "SYNTHETIC-KEYSTONE-001",
        "baseline_anchors": ["A", "B"],
        "removal_anchors": ["A"],
        "substitution_anchors": ["A", "C"]
    }
    result = evaluate_case(case)
    assert result["status"] == "STRUCTURALLY_TESTED"
    assert result["removed_anchor_ids"] == ["B"]
    assert result["changed_by_substitution"] == ["B"]
    assert result["keystone_verified"] is False


def test_incomplete_case_fails_closed():
    result = evaluate_case({"case_id": "SYNTHETIC-INCOMPLETE"})
    assert result["status"] == "FAILED"
    assert result["errors"]
