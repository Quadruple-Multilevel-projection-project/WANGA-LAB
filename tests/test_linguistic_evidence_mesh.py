from wanga_runtime.linguistic_evidence_mesh import (
    DerivationEdge,
    LexicalEvidence,
    LogicRelation,
    SourceRecord,
)


def test_lexical_evidence_digest_is_deterministic():
    source = SourceRecord("TEST", "doc:1", "FIXTURE", payload_digest="a" * 64)
    record = LexicalEvidence(
        record_id="lex:1",
        term="דוגמה",
        language="he",
        lemma="דוגמה",
        surface_forms=("דוגמה",),
        sources=(source,),
        derivations=(
            DerivationEdge("דוגמה", "דוגמאות", "INFLECTIONAL", "FIXTURE", "TESTED"),
        ),
        relations=(
            LogicRelation("דוגמה", "מושג", "GENUS", "OUTBOUND", "SPECIFIED"),
        ),
        logical_roles=("TERM",),
        extraction_method="FIXTURE",
        evidence_status="TESTED",
    )
    assert record.with_digest().record_sha256 == record.with_digest().record_sha256
    assert len(record.with_digest().record_sha256) == 64


def test_missing_evidence_is_not_promoted_to_verified():
    source = SourceRecord("TEST", "doc:2", "FIXTURE")
    record = LexicalEvidence(
        record_id="lex:2",
        term="מושג",
        language="he",
        sources=(source,),
        extraction_method="MODEL_INFERENCE",
        evidence_status="HYPOTHETICAL",
    ).with_digest()
    assert record.evidence_status == "HYPOTHETICAL"
