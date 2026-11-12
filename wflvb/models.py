from dataclasses import dataclass
from enum import Enum
from typing import Any

class Status(str, Enum):
    PASS="PASS"; FAIL="FAIL"; REVIEW="REVIEW"; UNRESOLVED="UNRESOLVED"; BLOCKED="BLOCKED"

@dataclass(frozen=True)
class SourceRef:
    source_id: str
    uri: str
    locator: str
    content_sha256: str

@dataclass(frozen=True)
class LogicNode:
    node_id: str
    symbol: str
    source_ids: tuple[str, ...]
    formal_type: str | None = None

@dataclass(frozen=True)
class Relation:
    relation_id: str
    source_node: str
    target_node: str
    relation_type: str
    source_ids: tuple[str, ...]
    formal_statement: str | None = None

@dataclass(frozen=True)
class StructuralInput:
    structure_id: str
    sources: tuple[SourceRef, ...]
    nodes: tuple[LogicNode, ...]
    relations: tuple[Relation, ...]
    assumptions: tuple[str, ...] = ()

@dataclass(frozen=True)
class Specification:
    specification_id: str
    structure_id: str
    source_ids: tuple[str, ...]
    nodes: tuple[dict[str, Any], ...]
    relations: tuple[dict[str, Any], ...]
    assumptions: tuple[str, ...]
    unresolved: tuple[str, ...]
    specification_sha256: str

@dataclass(frozen=True)
class ProofObligation:
    obligation_id: str
    specification_sha256: str
    statement: str
    source_ids: tuple[str, ...]

@dataclass(frozen=True)
class VerificationResult:
    status: Status
    specification_sha256: str
    approved_specification_sha256: str | None
    command: tuple[str, ...] = ()
    return_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    reason: str = ""
