from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Iterable

@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    kind: str
    text: str

@dataclass(frozen=True)
class TermDecl:
    name: str
    sort: str

@dataclass(frozen=True)
class PredicateDecl:
    name: str
    argument_sorts: tuple[str, ...]

@dataclass(frozen=True)
class FactDecl:
    status: str
    predicate: str
    arguments: tuple[str, ...]
    provenance: tuple[str, ...]

@dataclass(frozen=True)
class OperatorDecl:
    node_id: str
    operator: str
    parents: tuple[str, ...]
    payload: str = ""

_CALL = re.compile(r"^([A-Za-z_][\\w-]*)\\((.*)\\)$")
class TNRLProgram:
    sources: tuple[SourceRecord, ...] = ()
    terms: tuple[TermDecl, ...] = ()
    predicates: tuple[PredicateDecl, ...] = ()
    facts: tuple[FactDecl, ...] = ()
    operators: tuple[OperatorDecl, ...] = ()

_CALL = re.compile(r"^([A-Za-z_][\\w-]*)\\((.*)\\)$")

def _csv(value: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in value.split(",") if x.strip())

def _call(value: str) -> tuple[str, tuple[str, ...]]:
    m = _CALL.match(value.strip())
    if not m:
        raise ValueError(f"invalid call expression: {value}")
    return m.group(1), _csv(m.group(2))

def parse(text: str) -> TNRLProgram:
    sources=[]; terms=[]; predicates=[]; facts=[]; operators=[]
    for raw in text.splitlines():
        line=raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("source "):
            rest=line[7:].strip()
            parts=rest.split(None,2)
            if len(parts)<2: raise ValueError("source requires id and kind")
            sources.append(SourceRecord(parts[0],parts[1],parts[2] if len(parts)==3 else ""))
        elif line.startswith("term "):
            name, sort = line[5:].strip().split(":",1)
            terms.append(TermDecl(name.strip(),sort.strip()))
        elif line.startswith("predicate "):
            name,args=_call(line[10:].strip())
            predicates.append(PredicateDecl(name,tuple(args)))
        elif line.startswith(("assert ","deny ","unknown ")):
            status,expr=line.split(None,1)
            prov=()
            if "[" in expr and expr.endswith("]"):
                expr,tail=expr.rsplit("[",1)
                prov=_csv(tail[:-1])
            pred,args=_call(expr.strip())
            facts.append(FactDecl(status,pred,args,prov))
        elif line.startswith("operator "):
            rest=line[9:].strip()
            if "=" not in rest: raise ValueError("operator requires id = call")
            node_id,expr=rest.split("=",1)
            op,args=_call(expr.strip())
            operators.append(OperatorDecl(node_id.strip(),op,args))
        else:
            raise ValueError(f"unknown TNRL statement: {line}")
    return TNRLProgram(tuple(sources),tuple(terms),tuple(predicates),tuple(facts),tuple(operators))
