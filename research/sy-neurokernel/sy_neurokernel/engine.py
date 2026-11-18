from dataclasses import dataclass
from .graph import RelationGraph
from .neural import FixedTopologyMessagePassing, NeuralState
from .provenance import Provenance

@dataclass(frozen=True)
class EngineState:
    neural: NeuralState
    provenance: Provenance

class NeuroSymbolicEngine:
    def __init__(self, graph: RelationGraph):
        self.graph = graph
        self.model = FixedTopologyMessagePassing(graph)

    def initial_state(self) -> EngineState:
        return EngineState(self.model.initial(), Provenance.VERIFIED_FROM_SOURCE)

    def step(self, state: EngineState) -> EngineState:
        next_neural = self.model.step(state.neural)
        # Support is invariant by construction; provenance changes because a derived score exists.
        self.verify_support(next_neural)
        return EngineState(next_neural, Provenance.COMPUTATIONAL_HYPOTHESIS)

    def verify_support(self, neural_state: NeuralState) -> None:
        allowed = set(self.graph.directed)
        if set(neural_state.edge_scores) - allowed:
            raise ValueError("Neural output contains unsupported relation(s)")
