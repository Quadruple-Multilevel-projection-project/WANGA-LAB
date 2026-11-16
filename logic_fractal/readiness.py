"""Readiness eligibility rules shared by Wiki and agent-cycle evaluators."""


def is_readiness_eligible(unit, source_record):
    """Exclude explicit test fixtures from source-grounded readiness counts."""
    return (
        unit.get("permission_scope") != "TEST_FIXTURE_NOT_ELIGIBLE_FOR_READINESS"
        and source_record.get("type") != "TEST_FIXTURE"
    )
