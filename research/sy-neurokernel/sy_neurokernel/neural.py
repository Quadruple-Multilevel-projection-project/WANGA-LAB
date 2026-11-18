from dataclasses import dataclass
import math
from .graph import RelationGraph

@dataclass(frozen=True)
class NeuralState:
    embeddings: tuple[tuple[float, ...], ...]
    edge_scores: dict[tuple[int, int], float]

class FixedTopologyMessagePassing:
    """Minimal deterministic message passing over the pre-defined topology.

    It cannot create nodes or edges. Scores are a ranking surface only.
    """

    def __init__(self, graph: RelationGraph, width: int = 16):
        self.graph = graph
        self.width = width

    def initial(self) -> NeuralState:
        rows = []
        for node in self.graph.nodes:
            rows.append(tuple(math.sin(node * (j + 1)) for j in range(self.width)))
        return NeuralState(tuple(rows), {})

    def step(self, state: NeuralState) -> NeuralState:
        rows = []
        for i, node in enumerate(self.graph.nodes):
            own = state.embeddings[i]
            neigh = [state.embeddings[n - 1] for n in self.graph.neighbors(node)]
            if neigh:
                mean = tuple(sum(v[j] for v in neigh) / len(neigh) for j in range(self.width))
            else:
                mean = own
            rows.append(tuple((own[j] + mean[j]) / 2.0 for j in range(self.width)))

        scores = {}
        for a, b in self.graph.directed:
            # Deterministic bounded score; never changes support.
            x = sum(rows[a-1]) - sum(rows[b-1])
            scores[(a, b)] = 1.0 / (1.0 + math.exp(-max(-20.0, min(20.0, x))))
        return NeuralState(tuple(rows), scores)
