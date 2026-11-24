from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import uuid
from typing import Any, Dict, Sequence, Tuple

from .tinkin52 import Tinkin52


@dataclass(frozen=True)
class WangaRunManifest:
    run_id: str
    experiment_id: str
    method_version: str
    probe_registry_version: str
    baseline: str
    observation_schema_version: str
    provenance_policy: str
    timestamp_policy: str
    credential_boundary: str


class WangaTinkinSession:
    """BOOT → CONFIG → RUN → OBSERVE → VALIDATE → ANALYSIS."""

    def __init__(self, machine: Tinkin52 | None = None):
        self.machine = machine or Tinkin52()
        self.manifest: WangaRunManifest | None = None

    def boot(
        self,
        *,
        experiment_id: str = "TINKIN-52",
        method_version: str = "WANGA-TINKIN-52-V1",
        probe_registry_version: str = "computational-probes-v1",
    ) -> WangaRunManifest:
        self.manifest = WangaRunManifest(
            run_id=f"RUN-{uuid.uuid4().hex.upper()}",
            experiment_id=experiment_id,
            method_version=method_version,
            probe_registry_version=probe_registry_version,
            baseline="deterministic-computational-baseline-v1",
            observation_schema_version="WANGA-TINKIN-52-V1",
            provenance_policy="raw-computation-distinguished-from-analysis",
            timestamp_policy="UTC",
            credential_boundary="no-credentials-in-runtime-payload",
        )
        return self.manifest

    def execute(
        self,
        signals: Sequence[Tuple[str, str]] | None = None,
    ) -> Dict[str, Any]:
        if self.manifest is None:
            raise RuntimeError("WANGA session must be booted before execution.")

        result = self.machine.step(signals)
        return {
            "run_id": self.manifest.run_id,
            "experiment_id": self.manifest.experiment_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "observation_state": "AVAILABLE",
            "analysis_state": "SEPARATE",
            "tinkin": self.machine.export(result),
        }

    def message(self, message_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Shape compatible with the WANGA Agent Bridge message contract."""
        if self.manifest is None:
            raise RuntimeError("WANGA session must be booted before messaging.")

        allowed = {
            "TASK",
            "RESULT",
            "REQUEST_REVIEW",
            "SPECIALIST_REQUIRED",
            "ARCHITECTURE_FINDING",
            "DRIFT_SIGNAL",
        }
        if message_type not in allowed:
            raise ValueError(f"Unsupported WANGA message type: {message_type}")

        return {
            "message_id": f"MSG-{uuid.uuid4().hex.upper()}",
            "run_id": self.manifest.run_id,
            "sender": "WANGA-TINKIN-52",
            "message_type": message_type,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
            "status": "OPEN",
        }


__all__ = ["WangaRunManifest", "WangaTinkinSession"]
