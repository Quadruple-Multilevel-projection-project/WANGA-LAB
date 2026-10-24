from engine.drift_validator import validate_drift_status


def test_repository_layout_is_intact():
    report = validate_drift_status()
    assert report["status"] == "STRUCTURALLY_VALID", report["errors"]
    assert report["drift_detected"] is False
