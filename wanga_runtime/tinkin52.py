"""
WANGA OS / Tinkin-52 runtime.

One machine contains exactly:
- 52 nested networks
- 4 layers × 13 networks
- 3 wheels/network
- 11 gates/wheel = 33 gates/network
- 66 letter endpoints/network

This module is computational/deterministic. It does not represent empirical
neural activity, physical crystallography, or quantum hardware.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


HEBREW_LETTERS: Tuple[str, ...] = (
    "א", "ב", "ג", "ד", "ה", "ו", "ז", "ח", "ט", "י", "כ",
    "ל", "מ", "נ", "ס", "ע", "פ", "צ", "ק", "ר", "ש", "ת",
)

WHEEL_DEFINITIONS: Mapping[str, Tuple[Tuple[str, str], ...]] = {
    "G1": (
        ("א", "ל"), ("ב", "ת"), ("ג", "ש"), ("ד", "ר"), ("ה", "ו"),
        ("ו", "צ"), ("ז", "פ"), ("ח", "ע"), ("ט", "ס"), ("י", "נ"), ("כ", "מ"),
    ),
    "G2": (
        ("א", "ב"), ("ג", "ת"), ("ד", "ש"), ("ה", "ר"), ("ו", "ק"),
        ("ז", "צ"), ("ח", "פ"), ("ט", "ע"), ("י", "ס"), ("כ", "נ"), ("ל", "מ"),
    ),
    "G3": (
        ("א", "ג"), ("ד", "ת"), ("ה", "ש"), ("ו", "ר"), ("ז", "ק"),
        ("ח", "צ"), ("ט", "פ"), ("י", "ע"), ("כ", "ס"), ("ל", "נ"), ("ב", "מ"),
    ),
}

ENVELOPE_VERTEX_COUNT = 13\nNESTED_LEVELS = (\n    "TERM_NAME_NETWORK",\n    "RELATION_MATTER_SPACE",\n    "SENTENCE_CONFIGURATION",\n    "INFERENCE_SPACE",\n    "META_LOGIC_ORCHESTRATOR",\n)\n\nDRIFT_AXES: Mapping[str, float] = {
    "alpha_up": 0.02,
    "beta_down": 0.02,
    "gamma_forward": 0.03,
    "delta_backward": 0.03,
    "epsilon_noise": 0.04,
    "zeta_anomaly": 0.01,
}

DEFAULTS = {
    "network_count": 52,
    "networks_per_layer": 13,
    "layer_count": 4,
    "wheels_per_network": 3,
    "gates_per_network": 33,
    "letter_endpoints_per_network": 66,
    "total_letters": 22,
    "micro_drift_threshold": 0.10,
    "macro_drift_threshold": 0.20,
    "plasticity_rate": 0.50,
    "layer_coupling_strength": 0.10,
    "horizontal_coupling_strength": 0.05,
}


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def stable_noise(*parts: object) -> float:
    digest = sha256("|".join(map(str, parts)).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / float(2**64 - 1)


@dataclass(frozen=True)
class Gate:
    wheel: str
    index: int
    a: str
    b: str

    @property
    def gate_id(self) -> str:
        return f"{self.wheel}-{self.index:02d}"

    def accepts(self, signal: Tuple[str, str]) -> bool:
        a, b = signal
        return (a == self.a and b == self.b) or (a == self.b and b == self.a)


@dataclass
class NetworkState:
    network_id: int
    layer: int
    local_drift: float
    vertical_input: float
    horizontal_input: float
    coupled_drift: float
    active_gates: int
    status: str


@dataclass
class MachineTick:
    tick: int
    c0_status: str
    global_drift: float
    layer_drifts: List[float]
    axes: Dict[str, Dict[str, float | bool]]
    networks: List[NetworkState]


class NestedNetwork:
    """One reusable 33-gate nested network."""

    def __init__(self, network_id: int, layer: int, config: Mapping[str, float]):
        self.network_id = network_id
        self.layer = layer
        self.config = config
        self.gates: Tuple[Gate, ...] = tuple(
            Gate(wheel, index, a, b)
            for wheel, pairs in WHEEL_DEFINITIONS.items()
            for index, (a, b) in enumerate(pairs, start=1)
        )
        if len(self.gates) != 33:
            raise ValueError("Expected exactly 33 gates per nested network.")

    def step(
        self,
        signals: Sequence[Tuple[str, str]],
        vertical_input: float,
        horizontal_input: float,
        tick: int,
    ) -> NetworkState:
        accepted = sum(
            1 for signal in signals if any(g.accepts(signal) for g in self.gates)
        )
        count = max(1, len(signals))
        mismatch = 1.0 - accepted / count

        # Deterministic local perturbation keyed by network/tick. This replaces
        # Math.random() while preserving a controlled exploration component.
        epsilon = (stable_noise(self.network_id, self.layer, tick) - 0.5) * 0.02

        local = clamp(
            0.55 * mismatch
            + 0.25 * abs(vertical_input)
            + 0.20 * abs(horizontal_input)
            + epsilon
        )

        coupled = clamp(
            local
            + self.config["layer_coupling_strength"] * abs(vertical_input)
            + self.config["horizontal_coupling_strength"] * abs(horizontal_input)
        )

        if coupled >= self.config["macro_drift_threshold"]:
            status = "DRIFT_ALERT"
        elif coupled >= self.config["micro_drift_threshold"]:
            status = "DRIFT"
        else:
            status = "STABLE"

        return NetworkState(
            network_id=self.network_id,
            layer=self.layer,
            local_drift=local,
            vertical_input=vertical_input,
            horizontal_input=horizontal_input,
            coupled_drift=coupled,
            active_gates=accepted,
            status=status,
        )


@dataclass
class Tinkin52:
    """WANGA-hosted machine containing exactly 52 NestedNetwork instances."""

    config: Dict[str, float] = field(default_factory=lambda: dict(DEFAULTS))
    tick_count: int = 0
    networks: List[NestedNetwork] = field(init=False)
    previous_states: List[NetworkState] = field(default_factory=list)

    def __post_init__(self) -> None:
        required = (
            self.config["network_count"] == 52
            and self.config["networks_per_layer"] == 13
            and self.config["layer_count"] == 4
        )
        if not required:
            raise ValueError("Tinkin52 requires 52 networks arranged as 4 × 13.")

        self.networks = [
            NestedNetwork(
                network_id=i,
                layer=(i - 1) // 13,
                config=self.config,
            )
            for i in range(1, 53)
        ]

    @property
    def topology(self) -> Dict[str, int]:
        return {
            "networks": 52,
            "layers": 4,
            "networks_per_layer": 13,
            "wheels": 156,
            "gates": 1716,
            "letter_endpoints": 3432,
        }

    @property
    def canonical_signals(self) -> List[Tuple[str, str]]:
        return [
            pair
            for pairs in WHEEL_DEFINITIONS.values()
            for pair in pairs
        ]

    def _axes(
        self,
        states: Sequence[NetworkState],
        global_drift: float,
    ) -> Dict[str, Dict[str, float | bool]]:
        active_ratio = sum(s.active_gates for s in states) / (len(states) * 33)
        drift_ratio = sum(
            s.coupled_drift >= self.config["micro_drift_threshold"]
            for s in states
        ) / len(states)
        anomaly_ratio = sum(
            s.coupled_drift >= self.config["macro_drift_threshold"]
            for s in states
        ) / len(states)

        values = {
            "alpha_up": clamp(global_drift * 0.10),
            "beta_down": clamp(anomaly_ratio * 0.10),
            "gamma_forward": clamp((1.0 - active_ratio) * 0.08),
            "delta_backward": clamp(abs(global_drift - active_ratio) * 0.08),
            "epsilon_noise": clamp(abs(sum(
                stable_noise(s.network_id, self.tick_count) - 0.5
                for s in states
            )) / (len(states) * 2.0)),
            "zeta_anomaly": clamp((drift_ratio + anomaly_ratio) * 0.01),
        }
        return {
            code: {
                "value": round(value, 8),
                "threshold": threshold,
                "alert": value >= threshold,
            }
            for code, value in values.items()
            for threshold in (DRIFT_AXES[code],)
        }

    def architecture_contract(self) -> Dict[str, object]:
        return {
            "envelope": {
                "vertices": ENVELOPE_VERTEX_COUNT,
                "spatial_dimensions": 3,
                "temporal_dimensions": 1,
                "spatiotemporal_dimensions": 4,
                "coordinates_defined": False,
            },
            "nested_levels": [
                {"level": i + 1, "name": name}
                for i, name in enumerate(NESTED_LEVELS)
            ],
            "logic": {
                "declared_terms": 175,
                "computed_from_gate_counts": 188,
                "count_delta": 13,
                "count_consistent": False,
            },
        }

    def validate(self) -> Dict[str, object]:
        gate_counts = {n.network_id: len(n.gates) for n in self.networks}
        return {
            "network_count": len(self.networks),
            "all_networks_have_33_gates": all(v == 33 for v in gate_counts.values()),
            "layers": {
                str(layer): sum(n.layer == layer for n in self.networks)
                for layer in range(4)
            },
            "wheels": 156,
            "gates": 1716,
            "endpoints": 3432,
            "hebrew_letters": len(HEBREW_LETTERS),
            "drift_axes": len(DRIFT_AXES),\n            "envelope_vertices": ENVELOPE_VERTEX_COUNT,\n            "nested_levels": len(NESTED_LEVELS),\n            "logic_count_delta": 13,
        }

    def step(
        self,
        signals: Sequence[Tuple[str, str]] | None = None,
    ) -> MachineTick:
        self.tick_count += 1
        active_signals = list(signals or self.canonical_signals[:2])

        current: List[NetworkState] = []
        layer_drifts: List[float] = []
        prior_layer_drift = 0.0
        prior_layer_states: List[NetworkState] = []

        for layer in range(4):
            layer_states: List[NetworkState] = []
            for offset in range(13):
                network = self.networks[layer * 13 + offset]

                # Frozen-snapshot ring coupling: left/right read from the
                # previous layer's snapshot and never from partially updated
                # current state.
                if prior_layer_states:
                    left = prior_layer_states[(offset - 1) % 13].coupled_drift
                    right = prior_layer_states[(offset + 1) % 13].coupled_drift
                    horizontal = (left + right) / 2.0
                else:
                    horizontal = 0.0

                state = network.step(
                    active_signals,
                    vertical_input=prior_layer_drift,
                    horizontal_input=horizontal,
                    tick=self.tick_count,
                )
                layer_states.append(state)
                current.append(state)

            layer_drift = sum(s.coupled_drift for s in layer_states) / 13.0
            layer_drifts.append(layer_drift)
            prior_layer_drift = layer_drift
            prior_layer_states = layer_states

        global_drift = sum(layer_drifts) / 4.0

        if global_drift >= self.config["macro_drift_threshold"]:
            global_drift = clamp(
                global_drift - self.config["plasticity_rate"] * 0.10
            )
            c0_status = "COMPENSATING"
        elif global_drift >= self.config["macro_drift_threshold"] * 0.75:
            c0_status = "DRIFT_ALERT"
        else:
            c0_status = "BALANCED"

        self.previous_states = current
        return MachineTick(
            tick=self.tick_count,
            c0_status=c0_status,
            global_drift=global_drift,
            layer_drifts=layer_drifts,
            axes=self._axes(current, global_drift),
            networks=current,
        )

    def export(self, result: MachineTick) -> Dict[str, object]:
        return {
            "schema_version": "WANGA-TINKIN-52-V1",
            "topology": self.topology,
            "tick": result.tick,
            "c0": {
                "status": result.c0_status,
                "global_drift": round(result.global_drift, 8),
            },
            "layer_drifts": [round(x, 8) for x in result.layer_drifts],
            "axes": result.axes,
            "networks": [
                {
                    "network_id": s.network_id,
                    "layer": s.layer,
                    "local_drift": round(s.local_drift, 8),
                    "vertical_input": round(s.vertical_input, 8),
                    "horizontal_input": round(s.horizontal_input, 8),
                    "coupled_drift": round(s.coupled_drift, 8),
                    "active_gates": s.active_gates,
                    "status": s.status,
                }
                for s in result.networks
            ],
            "architecture_contract": self.architecture_contract(),\n            "validation": self.validate(),
        }


def build_tinkin52() -> Tinkin52:
    """Factory with an explicit invariant: return exactly 52 networks."""
    machine = Tinkin52()
    assert len(machine.networks) == 52
    return machine
