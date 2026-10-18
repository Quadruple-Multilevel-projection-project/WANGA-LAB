from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable
from .ir import ReasoningNode, TruthStatus

class Operator(str, Enum):
    KUSHYA = "kushya"
    TERUTZ = "terutz"
    REAYA = "reaya"
    DEHIYA = "dehiya"
    STIRA = "stira"
    HAVDALA = "havdalah"
    MEKOR = "mekor"
    MAHLOKET = "mahloket"
    HACHRAA = "hachraa"

@dataclass(frozen=True)
class OperatorResult:
    operator: Operator
    node: ReasoningNode
    obligations: tuple[str, ...] = ()

def apply_operator(operator: Operator, parents: Iterable[ReasoningNode], node_id: str, payload=None) -> OperatorResult:
    ps = tuple(parents)
    payload = dict(payload or {})
    if operator is Operator.STIRA:
        status = TruthStatus.CONTRADICTED
    elif operator in (Operator.REAYA, Operator.TERUTZ, Operator.HACHRAA):
        status = TruthStatus.CONDITIONAL
    else:
        status = TruthStatus.UNKNOWN
    obligations = () if operator in (Operator.MEKOR, Operator.HAVDALA) else (f"validate:{operator.value}",)
    return OperatorResult(operator, ReasoningNode(node_id=node_id, kind=operator.value, payload=payload, parents=tuple(p.node_id for p in ps), status=status), obligations)
