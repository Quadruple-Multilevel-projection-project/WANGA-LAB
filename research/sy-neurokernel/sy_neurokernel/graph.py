from dataclasses import dataclass
from types import MappingProxyType
from .alphabet import AlphabetKernel
from .gates import GateSpace

@dataclass(frozen=True)
class RelationGraph:
    kernel: AlphabetKernel

    def __post_init__(self):
        gate_space = GateSpace(self.kernel.addresses)
        gate_space.assert_invariants()
        object.__setattr__(self, "_gate_space", gate_space)
        object.__setattr__(self, "_adjacency", MappingProxyType({
            a: tuple(b for b in self.kernel.addresses if b != a)
            for a in self.kernel.addresses
        }))

    @property
    def nodes(self):
        return self.kernel.addresses

    @property
    def gates(self):
        return self._gate_space.unordered

    @property
    def directed(self):
        return self._gate_space.directed

    @property
    def full(self):
        return self._gate_space.full

    @property
    def adjacency(self):
        return self._adjacency

    def supports(self, edge: tuple[int, int]) -> bool:
        return self._gate_space.contains_directed(edge)

    def neighbors(self, node: int):
        return self._adjacency[node]
