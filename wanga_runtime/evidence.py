from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class EvidenceEnvelope:
    workstream_key: str
    evidence_type: str
    source_ref: str | None = None
    extraction_ref: str | None = None
    interpretation_ref: str | None = None
    hypothesis_ref: str | None = None
    verification_state: str = "NOT_YET_VERIFIED"
    payload: Mapping[str, Any] | None = None

    def to_supabase_row(self) -> dict[str, Any]:
        return {
            "workstream_key": self.workstream_key,
            "evidence_type": self.evidence_type,
            "source_ref": self.source_ref,
            "extraction_ref": self.extraction_ref,
            "interpretation_ref": self.interpretation_ref,
            "hypothesis_ref": self.hypothesis_ref,
            "verification_state": self.verification_state,
            "payload": dict(self.payload or {}),
        }
