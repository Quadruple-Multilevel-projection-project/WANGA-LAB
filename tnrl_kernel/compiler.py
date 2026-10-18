from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .fol import FOLStore
from .ir import Predicate, Proposition, ReasoningNode, Term, TruthStatus
from .operators import Operator, apply_operator
from .parser import TNRLProgram

_STATUS={"assert":TruthStatus.ASSERTED,"deny":TruthStatus.DENIED,"unknown":TruthStatus.UNKNOWN}

@dataclass
class CompiledProgram:
    facts: FOLStore
    nodes: dict[str, ReasoningNode]
    sources: dict[str, Any]

class TNRLCompiler:
    """Compiles the textual TNRL boundary into typed IR + FOL + reasoning graph."""
    def compile(self, program: TNRLProgram) -> CompiledProgram:
        terms={x.name:Term(x.name,x.sort) for x in program.terms}
        predicates={x.name:Predicate(x.name,len(x.argument_sorts),x.argument_sorts) for x in program.predicates}
        facts=FOLStore()
        nodes={}
        for fact in program.facts:
            if fact.predicate not in predicates:
                raise ValueError(f"unknown predicate: {fact.predicate}")
            pred=predicates[fact.predicate]
            args=tuple(terms[a] for a in fact.arguments)
            prop=Proposition(pred,args,_STATUS[fact.status],fact.provenance)
            prop.validate()
            facts.assert_fact(prop)
            node_id=f"fact:{fact.predicate}({','.join(fact.arguments)})"
            nodes[node_id]=ReasoningNode(node_id,"proposition",{"proposition":prop},status=prop.status)
        for decl in program.operators:
            try: op=Operator(decl.operator)
            except ValueError as e: raise ValueError(f"unknown operator: {decl.operator}") from e
            parents=tuple(self._require_node(nodes,p) for p in decl.parents)
            result=apply_operator(op,parents,decl.node_id,{"source_payload":decl.payload})
            nodes[decl.node_id]=result.node
        return CompiledProgram(facts,nodes,{s.source_id:s for s in program.sources})

    @staticmethod
    def _require_node(nodes:dict[str,ReasoningNode], node_id:str)->ReasoningNode:
        if node_id not in nodes:
            raise ValueError(f"unknown reasoning parent: {node_id}")
        return nodes[node_id]
