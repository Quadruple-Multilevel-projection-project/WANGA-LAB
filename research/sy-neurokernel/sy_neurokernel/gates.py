from dataclasses import dataclass
from typing import Iterator

@dataclass(frozen=True)
class GateSpace:
    addresses: tuple[int, ...]

    @property
    def unordered(self) -> tuple[tuple[int, int], ...]:
        return tuple((a, b) for i, a in enumerate(self.addresses) for b in self.addresses[i+1:])

    @property
    def directed(self) -> tuple[tuple[int, int], ...]:
        return tuple((a, b) for a in self.addresses for b in self.addresses if a != b)

    @property
    def full(self) -> tuple[tuple[int, int], ...]:
        return tuple((a, b) for a in self.addresses for b in self.addresses)

    def contains_directed(self, edge: tuple[int, int]) -> bool:
        return edge in set(self.directed)

    def contains_unordered(self, edge: tuple[int, int]) -> bool:
        a, b = edge
        return (min(a, b), max(a, b)) in set(self.unordered)

    def assert_invariants(self) -> None:
        assert len(self.unordered) == 231
        assert len(self.directed) == 462
        assert len(self.full) == 484
