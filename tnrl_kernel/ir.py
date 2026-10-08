from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Tuple

class TruthStatus(str, Enum):
    ASSERTED = "asserted"
    DENIED = "denied"
    UNKNOWN = "unknown"
    CONTRADICTED = "contradicted"
    CONDITIONAL = "conditional"

@dataclass(frozen=True)
class Term:
    name: str
    sort: str = "Entity"
    value: Any = None

@dataclass(frozen=True)
class Predicate:
    name: str
    arity: int
    argument_sorts: Tuple[str, ...] = ()

@dataclass(frozen=True)
class Proposition:
    predicate: Predicate
    arguments: Tuple[Term, ...]
    status: TruthStatus = TruthStatus.UNKNOWN
    provenance: Tuple[str, ...] = ()

    def validate(self) -> None:
        if len(self.arguments) != self.predicate.arity:
            raise ValueError("predicate arity mismatch")
        if self.predicate.argument_sorts and tuple(t.sort for t in self.arguments) != self.predicate.argument_sorts:
            raise TypeError("predicate argument sort mismatch")

@dataclass
class ReasoningNode:
    node_id: str
    kind: str
    payload: Mapping[str, Any]
    parents: Tuple[str, ...] = ()
    status: TruthStatus = TruthStatus.UNKNOWN
    metadata: dict[str, Any] = field(default_factory=dict)
