import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "first-order-logic" / "part-1"),
)

from ai231_task import ai231_task  # noqa: E402


def test_neural_proposal_cannot_override_formal_reject():
    result = ai231_task(
        formal_decision="REJECT",
        source_ref="G14:SENTENCE-TEST-FIXTURE",
        source_ref_resolved=True,
        neural_proposal="ACCEPT",
    )
    assert result.status == "REJECT"
    assert result.reason == "FORMAL_GATE_RESULT"


def test_neural_proposal_cannot_override_formal_accept():
    result = ai231_task(
        formal_decision="ACCEPT",
        source_ref="INTRO:SENTENCE-TEST-FIXTURE",
        source_ref_resolved=True,
        neural_proposal="REJECT",
    )
    assert result.status == "ACCEPT"


def test_missing_source_ref_halts_for_review():
    result = ai231_task(
        formal_decision="ACCEPT",
        source_ref=None,
        source_ref_resolved=False,
        neural_proposal="ACCEPT",
    )
    assert result.status == "REQUIRES_REVIEW"
    assert result.reason == "SOURCE_REFERENCE_MISSING_OR_UNRESOLVED"


def test_unresolved_source_ref_halts_for_review():
    result = ai231_task(
        formal_decision="ACCEPT",
        source_ref="UNKNOWN:SENTENCE",
        source_ref_resolved=False,
        neural_proposal="ACCEPT",
    )
    assert result.status == "REQUIRES_REVIEW"


def test_unknown_formal_decision_fails_closed():
    result = ai231_task(
        formal_decision="MAYBE",
        source_ref="G14:SENTENCE-TEST-FIXTURE",
        source_ref_resolved=True,
        neural_proposal="ACCEPT",
    )
    assert result.status == "REQUIRES_REVIEW"
    assert result.reason == "UNKNOWN_FORMAL_DECISION"
