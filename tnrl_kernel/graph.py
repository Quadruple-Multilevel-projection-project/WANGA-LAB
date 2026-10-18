from __future__ import annotations
from dataclasses import dataclass, field
from .ir import ReasoningNode

@dataclass
class ReasoningGraph:
    nodes: dict[str, ReasoningNode] = field(default_factory=dict)

    def add(self,node:ReasoningNode)->None:
        if node.node_id in self.nodes:
            raise ValueError(f"duplicate node: {node.node_id}")
        for parent in node.parents:
            if parent not in self.nodes:
                raise ValueError(f"missing parent: {parent}")
        self.nodes[node.node_id]=node

    def edges(self)->list[tuple[str,str]]:
        return [(parent,node.node_id) for node in self.nodes.values() for parent in node.parents]

    def to_dict(self)->dict:
        return {"nodes":[{"node_id":n.node_id,"kind":n.kind,"parents":list(n.parents),"status":n.status.value,"payload":dict(n.payload)} for n in self.nodes.values()],"edges":[{"from":a,"to":b} for a,b in self.edges()]}
