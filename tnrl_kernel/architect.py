from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping

@dataclass(frozen=True)
class ArchitectureSpec:
    name: str
    version: str
    layers: tuple[str, ...]
    operators: tuple[str, ...]
    kernel_contract: Mapping[str, Any]

class Architect:
    """Meta-layer: turns a declarative architecture specification into a manifest."""
    def compile(self, spec: ArchitectureSpec) -> dict[str, Any]:
        if not spec.layers or "fol" not in spec.layers:
            raise ValueError("TNRL architecture requires an FOL kernel layer")
        if "rational_logic" in spec.layers:
            raise ValueError("rational_logic is an upper layer and is not compiled into the kernel")
        return {
            "architecture": spec.name,
            "version": spec.version,
            "layers": list(spec.layers),
            "operators": list(spec.operators),
            "kernel_contract": dict(spec.kernel_contract),
            "status": "SPECIFIED",
        }
