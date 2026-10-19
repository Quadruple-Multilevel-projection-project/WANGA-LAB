from wanga_runtime.algorithmic_genealogy import AlgorithmicGenealogyGate, GenealogyArtifact


def make_artifact(**changes):
    data = dict(
        artifact_id="child",
        kind="MODEL",
        parents=("parent",),
        transformation="FINE_TUNE",
        source_refs=("source:parent",),
        weight_lineage_declared=True,
        evidence_status="TESTED",
        sha256="a" * 64,
    )
    data.update(changes)
    return GenealogyArtifact(**data)


def parent():
    return GenealogyArtifact(
        artifact_id="parent",
        kind="MODEL",
        transformation="FROM_SCRATCH",
        source_refs=("source:parent",),
        evidence_status="VERIFIED",
        sha256="b" * 64,
    )


def test_clean_lineage_is_accepted():
    result = AlgorithmicGenealogyGate().evaluate(make_artifact(), (parent(),))
    assert result.decision == "ACCEPT_FOR_EVALUATION"


def test_missing_parent_blocks():
    result = AlgorithmicGenealogyGate().evaluate(make_artifact(), ())
    assert result.decision == "BLOCK_PROMOTION"


def test_missing_weight_lineage_holds():
    result = AlgorithmicGenealogyGate().evaluate(
        make_artifact(weight_lineage_declared=False), (parent(),)
    )
    assert result.decision == "HOLD_FOR_EVIDENCE"


def test_drift_escalates():
    result = AlgorithmicGenealogyGate().evaluate(
        make_artifact(known_drift=True, drift_score=0.8), (parent(),)
    )
    assert result.decision == "ESCALATE_TO_RATIONAL_LOGIC"


def test_integrity_is_required():
    result = AlgorithmicGenealogyGate().evaluate(
        make_artifact(sha256="bad"), (parent(),)
    )
    assert result.decision == "BLOCK_PROMOTION"


def test_same_input_produces_same_decision_hash():
    gate = AlgorithmicGenealogyGate()
    first = gate.evaluate(make_artifact(), (parent(),))
    second = gate.evaluate(make_artifact(), (parent(),))
    assert first.decision == second.decision
    assert first.decision_hash == second.decision_hash
