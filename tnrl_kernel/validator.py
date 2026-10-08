from __future__ import annotations
from .graph import ReasoningGraph
from .ir import TruthStatus

class TNRLValidator:
    """Checks structural invariants without deciding substantive halakhic truth."""
    def validate_graph(self, graph:ReasoningGraph)->list[str]:
        errors=[]
        for node in graph.nodes.values():
            for parent in node.parents:
                if parent not in graph.nodes:
                    errors.append(f"{node.node_id}: missing parent {parent}")
            if node.status is TruthStatus.CONTRADICTED and node.kind!="stira":
                errors.append(f"{node.node_id}: contradiction must be explicit stira or FOL contradiction")
        return errors

    def require_valid(self, graph:ReasoningGraph)->None:
        errors=self.validate_graph(graph)
        if errors:
            raise ValueError("; ".join(errors))
