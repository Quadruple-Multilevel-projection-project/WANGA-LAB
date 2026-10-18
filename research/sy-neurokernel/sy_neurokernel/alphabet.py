from dataclasses import dataclass
from typing import Mapping

# Addresses are deliberately opaque. Labels are metadata, not semantic embeddings.
DEFAULT_ADDRESSES = tuple(range(1, 23))

@dataclass(frozen=True)
class AlphabetKernel:
    addresses: tuple[int, ...] = DEFAULT_ADDRESSES
    partitions: Mapping[str, tuple[int, ...]] = None
    phonetic_places: Mapping[str, tuple[int, ...]] = None

    def __post_init__(self):
        if len(self.addresses) != 22 or len(set(self.addresses)) != 22:
            raise ValueError("AlphabetKernel requires exactly 22 unique addresses")
        if self.partitions is None:
            object.__setattr__(self, "partitions", {
                "mothers": (1, 2, 3),
                "doubles": (4, 5, 6, 7, 8, 9, 10),
                "simples": tuple(range(11, 23)),
            })
        if self.phonetic_places is None:
            object.__setattr__(self, "phonetic_places", {
                "place_1": tuple(),
                "place_2": tuple(),
                "place_3": tuple(),
                "place_4": tuple(),
                "place_5": tuple(),
            })
        self._validate_partitions()

    def _validate_partitions(self):
        flat = [x for xs in self.partitions.values() for x in xs]
        if sorted(flat) != sorted(self.addresses):
            raise ValueError("Structural partitions must cover the 22 addresses exactly once")
        if len(self.phonetic_places) != 5:
            raise ValueError("Exactly five phonetic-place tags are required")

    @property
    def n_nodes(self) -> int:
        return len(self.addresses)

    @property
    def n_gates(self) -> int:
        return self.n_nodes * (self.n_nodes - 1) // 2

    @property
    def n_directed(self) -> int:
        return self.n_nodes * (self.n_nodes - 1)

    @property
    def n_full(self) -> int:
        return self.n_nodes * self.n_nodes
