from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
import json


EVIDENCE_STATUSES = {
    "BUILT", "SPECIFIED", "PROTOTYPED", "TESTED",
    "VERIFIED", "PLANNED", "HYPOTHETICAL",
}

TRANSFORMATIONS = {
    "FROM_SCRATCH", "FINE_TUNE", "DISTILLATION", "DEPTH_UPSCALING",
    "MODEL_MERGE", "ADAPTER_COMPOSITION", "QUANTIZATION", "PRUNING",
    "CHECKPOINT_CONVERSION", "UNKNOWN_TRANSFORMATION",
}


@dataclass(frozen=True)
class GenealogyArtifact:
    artifact_id: str
    kind: str
    parents: tuple[str, ...] = ()
    transformation: str = "UNKNOWN_TRANSFORMATION"
    source_refs: tuple[str, ...] = ()
    weight_lineage_declared: bool = False
    evidence_status: str = "SPECIFIED"
    sha256: str = ""
    known_drift: bool = False
    drift_score: float | None = None
    conflict_refs: tuple[str, ...] = ()


@dataclass(frozen=True)
class GatePolicy:
    version: str = "LINEAGE_GATE_V1"
    require_provenance: bool = True
    drift_escalation_threshold: float = 0.5


@dataclass(frozen=True)
class RuleResult:
    rule_id: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class GateDecision:
    artifact_id: str
    policy_version: str
    decision: str
    rules: tuple[RuleResult, ...]
    conflicts: tuple[str, ...]
    decision_hash: str


class AlgorithmicGenealogyGate:
    """Deterministic pre-integration gate for model/component lineage."""

    _WEIGHTED_TRANSFORMS = {
        "FINE_TUNE", "DISTILLATION", "DEPTH_UPSCALING",
        "MODEL_MERGE", "ADAPTER_COMPOSITION", "QUANTIZATION", "PRUNING",
        "CHECKPOINT_CONVERSION",
    }

    def __init__(self, policy: GatePolicy | None = None):
        self.policy = policy or GatePolicy()

    @staticmethod
    def _digest(value: object) -> str:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
        return sha256(payload.encode("utf-8")).hexdigest()

    def evaluate(self, artifact: GenealogyArtifact, registry: tuple[GenealogyArtifact, ...] = ()) -> GateDecision:
        index = {item.artifact_id: item for item in registry}
        rules = [
            RuleResult(
                "R1_SCHEMA",
                bool(artifact.artifact_id and artifact.kind and artifact.evidence_status in EVIDENCE_STATUSES),
                "identity, kind and evidence status",
            ),
            RuleResult(
                "R2_PARENT_INTEGRITY",
                all(parent in index for parent in artifact.parents),
                "all declared parents exist",
            ),
            RuleResult(
                "R3_PROVENANCE",
                bool(artifact.source_refs) if self.policy.require_provenance else True,
                "source references present",
            ),
            RuleResult(
                "R4_WEIGHT_LINEAGE",
                artifact.transformation not in self._WEIGHTED_TRANSFORMS or artifact.weight_lineage_declared,
                "weighted transformation lineage declared",
            ),
            RuleResult(
                "R5_TRANSFORMATION",
                artifact.transformation in TRANSFORMATIONS and artifact.transformation != "UNKNOWN_TRANSFORMATION",
                "transformation disclosed",
            ),
            RuleResult(
                "R6_INTEGRITY",
                len(artifact.sha256) == 64 and all(c in "0123456789abcdefABCDEF" for c in artifact.sha256),
                "SHA-256 record is well formed",
            ),
            RuleResult(
                "R7_DRIFT",
                not (artifact.known_drift and (artifact.drift_score or 0.0) >= self.policy.drift_escalation_threshold),
                "no escalation-level drift evidence",
            ),
        ]

        conflicts = list(artifact.conflict_refs)
        failed = {rule.rule_id for rule in rules if not rule.passed}

        if {"R1_SCHEMA", "R2_PARENT_INTEGRITY", "R6_INTEGRITY"} & failed:
            decision = "BLOCK_PROMOTION"
        elif conflicts or "R7_DRIFT" in failed:
            decision = "ESCALATE_TO_RATIONAL_LOGIC"
        elif {"R3_PROVENANCE", "R4_WEIGHT_LINEAGE", "R5_TRANSFORMATION"} & failed:
            decision = "HOLD_FOR_EVIDENCE"
        else:
            decision = "ACCEPT_FOR_EVALUATION"

        canonical = {
            "artifact_id": artifact.artifact_id,
            "policy_version": self.policy.version,
            "decision": decision,
            "rules": [asdict(rule) for rule in rules],
            "conflicts": conflicts,
        }
        return GateDecision(
            artifact_id=artifact.artifact_id,
            policy_version=self.policy.version,
            decision=decision,
            rules=tuple(rules),
            conflicts=tuple(conflicts),
            decision_hash=self._digest(canonical),
        )
