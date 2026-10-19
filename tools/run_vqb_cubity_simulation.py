#!/usr/bin/env python3
"""Run a deterministic VQB Cubity simulation and write JSON/SVG artifacts."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape
import sys

# Permit direct execution from a checkout without package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.vqb_cubity_engine import VQBCubityEngine


def build_svg(report: dict, output_path: Path) -> None:
    width, height = 1100, 900
    center_x, center_y, radius = 430, 430, 300
    nodes = {}
    for i in range(36):
        angle = -math.pi / 2 + 2 * math.pi * i / 36
        nodes[i + 1] = (center_x + radius * math.cos(angle), center_y + radius * math.sin(angle))

    commands = report["commands"]
    route = [command["sub_space_id"] for command in commands]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#07111f"/>',
        '<text x="40" y="45" fill="#f4f8ff" font-family="Arial,sans-serif" font-size="25" font-weight="700">VQB Cubity — 36 Sub-Spaces / 120 Steps</text>',
        '<text x="40" y="73" fill="#93c5fd" font-family="Arial,sans-serif" font-size="14">Deterministic software simulation · one visible sub-space per step</text>',
    ]
    # Static multi-scale graph edges.
    edges = set()
    for i in range(1, 37):
        for offset in (1, 2, 4, 8, 16):
            j = ((i - 1 + offset) % 36) + 1
            edges.add(tuple(sorted((i, j))))
    for a, b in sorted(edges):
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        opacity = "0.10" if abs(a - b) not in (1, 35) else "0.48"
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#60a5fa" stroke-opacity="{opacity}" stroke-width="1.1"/>'
        )
    # Route sequence is drawn in order. The route may revisit a node over time.
    for a, b in zip(route, route[1:]):
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            'stroke="#fb7185" stroke-opacity="0.18" stroke-width="2.0"/>'
        )
    for node_id, (x, y) in nodes.items():
        color = "#fbbf24" if node_id == route[0] else "#38bdf8"
        lines.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{color}" '
            'fill-opacity="0.95" stroke="#e0f2fe" stroke-width="1.2"/>'
        )
        lines.append(
            f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" fill="#07111f" '
            f'font-family="monospace" font-size="10" font-weight="700">{node_id:02d}</text>'
        )
    info = [
        ("36", "sub-spaces configured"),
        (str(report["unique_sub_spaces_visited"]), "unique spaces visited"),
        (str(report["language_points_merged"]), "language points merged"),
        (str(report["composite_points_merged"]), "fixed-point composite merges"),
        (str(report["commands_generated"]), "commands generated"),
    ]
    y = 175
    for value, label in info:
        lines.append(
            f'<text x="800" y="{y}" fill="#f8fafc" font-family="monospace" '
            f'font-size="27" font-weight="700">{escape(value)}</text>'
        )
        lines.append(
            f'<text x="850" y="{y}" fill="#cbd5e1" font-family="Arial,sans-serif" '
            f'font-size="14">{escape(label)}</text>'
        )
        y += 55
    lines.extend([
        '<rect x="780" y="500" width="280" height="150" rx="14" fill="#0f172a" stroke="#334155"/>',
        '<text x="800" y="530" fill="#f8fafc" font-family="Arial,sans-serif" font-size="16" font-weight="700">Command schema</text>',
        '<text x="800" y="560" fill="#93c5fd" font-family="monospace" font-size="13">state: TUNNELED</text>',
        '<text x="800" y="585" fill="#93c5fd" font-family="monospace" font-size="13">command: MAJORANA_2</text>',
        '<text x="800" y="610" fill="#93c5fd" font-family="monospace" font-size="13">time_jump: true</text>',
        '<text x="40" y="850" fill="#fda4af" font-family="Arial,sans-serif" font-size="13">“Tunneling” / “time jump” are simulated labels, not experimentally validated physical effects.</text>',
        '</svg>',
    ])
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=120)
    parser.add_argument("--output-dir", default="artifacts")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report = VQBCubityEngine().simulate(args.steps).to_dict()
    json_path = output_dir / "vqb_cubity_simulation_120.json"
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    svg_path = output_dir / "vqb_cubity_36_subspaces.svg"
    build_svg(report, svg_path)
    print(
        "VQB Cubity Engine Initialized (software simulation). "
        f"{report['sub_spaces_configured']} Eulerian Sub-Spaces Mapped. "
        "Einstein Ring 5D: dimensionless embedding active. "
        "Tunneling & Time Jumps: simulated state labels active. "
        f"{report['language_points_merged']} Language Points Merged. "
        f"{report['commands_generated']} Commands Generated."
    )
    print(f"JSON: {json_path}")
    print(f"SVG: {svg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
