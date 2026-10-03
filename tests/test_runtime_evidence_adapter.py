from wanga_runtime.evidence import EvidenceEnvelope


def test_provenance_fields_remain_separate_in_control_plane_row():
    envelope = EvidenceEnvelope(
        workstream_key="runtime",
        evidence_type="RUNTIME_EVIDENCE",
        source_ref="source:runtime",
        extraction_ref="extract:runtime",
        interpretation_ref="interpretation:pending",
        hypothesis_ref="hypothesis:pending",
        verification_state="TESTED",
        payload={"stage": "VERIFY"},
    )
    row = envelope.to_supabase_row()
    assert row["source_ref"] == "source:runtime"
    assert row["extraction_ref"] == "extract:runtime"
    assert row["interpretation_ref"] == "interpretation:pending"
    assert row["hypothesis_ref"] == "hypothesis:pending"
    assert row["verification_state"] == "TESTED"
