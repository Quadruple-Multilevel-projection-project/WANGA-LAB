#!/usr/bin/env python3
"""Run a deterministic VQB Cubity simulation and write JSON/SVG/HTML artifacts."""
from __future__ import annotations

import argparse
import json
import math
import sys
from html import escape
from pathlib import Path

# Permit direct execution from a checkout without package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engine.vqb_cubity_engine import VQBCubityEngine


def _node_positions(cx: float, cy: float, radius: float) -> dict[int, tuple[float, float]]:
    return {
        i + 1: (
            cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / 36),
            cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / 36),
        )
        for i in range(36)
    }


def build_svg(report: dict, output_path: Path) -> None:
    """Write a legible static topology map with a 36-transition route preview."""
    width, height = 1100, 900
    nodes = _node_positions(430, 430, 300)
    commands = report["commands"]
    route = [command["sub_space_id"] for command in commands]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#07111f"/>',
        '<text x="40" y="45" fill="#f4f8ff" font-family="Arial,sans-serif" font-size="25" font-weight="700">VQB Cubity — 36 Sub-Spaces / 120 Steps</text>',
        '<text x="40" y="73" fill="#93c5fd" font-family="Arial,sans-serif" font-size="14">Static topology and first 36-step route preview · use HTML file for animation</text>',
    ]
    edges = set()
    for i in range(1, 37):
        for offset in (1, 2, 4, 8, 16):
            j = ((i - 1 + offset) % 36) + 1
            edges.add(tuple(sorted((i, j))))
    for a, b in sorted(edges):
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        opacity = "0.26" if abs(a - b) in (1, 35) else "0.08"
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#60a5fa" stroke-opacity="{opacity}" stroke-width="1.1"/>'
        )
    # Draw only the first 36 appearances in the static preview; the HTML animation covers all steps.
    for a, b in zip(route[:36], route[1:36]):
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            'stroke="#fb7185" stroke-opacity="0.43" stroke-width="2.0"/>'
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
            f'<text x="875" y="{y}" fill="#cbd5e1" font-family="Arial,sans-serif" '
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


def build_html(report: dict, output_path: Path) -> None:
    """Write a self-contained browser animation with play, pause, and step controls."""
    commands_json = json.dumps(report["commands"], separators=(",", ":"))
    document = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>VQB Cubity — Animated 36 Sub-Spaces</title>
<style>
:root{color-scheme:dark;font-family:system-ui,Arial,sans-serif;background:#07111f;color:#e5edf8}
body{margin:0;padding:24px}h1{margin:0 0 6px;font-size:clamp(22px,3vw,32px)}.sub{color:#93c5fd;margin-bottom:20px}
.layout{display:grid;grid-template-columns:minmax(340px,1fr) 280px;gap:20px;align-items:start;max-width:1200px;margin:auto}
.panel{background:#0f172a;border:1px solid #334155;border-radius:16px;padding:18px}.network{width:100%;height:auto;display:block}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}button{background:#1d4ed8;color:white;border:0;border-radius:8px;padding:10px 14px;font-size:14px;cursor:pointer}button.secondary{background:#334155}button:focus{outline:2px solid #7dd3fc;outline-offset:2px}
.kv{display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid #263449;padding:9px 0}.v{font-family:ui-monospace,monospace;color:#93c5fd;text-align:right;overflow-wrap:anywhere}.warn{color:#fda4af;font-size:13px;line-height:1.45;margin-top:18px}.meter{height:5px;background:#263449;border-radius:4px;overflow:hidden;margin-top:14px}.meter>div{height:100%;width:0;background:#38bdf8;transition:width .1s linear}
@media(max-width:800px){.layout{grid-template-columns:1fr}body{padding:14px}}
</style></head>
<body><main class="layout"><section><h1>VQB Cubity — 36 Sub-Spaces</h1><div class="sub">120-step deterministic software animation · one active sub-space per appearance</div>
<div class="panel"><svg id="network" class="network" viewBox="0 0 800 800" role="img" aria-label="36-node multi-scale sub-space graph"></svg>
<div class="controls"><button id="play">Play</button><button id="pause" class="secondary">Pause</button><button id="prev" class="secondary">Previous</button><button id="next" class="secondary">Next</button><button id="reset" class="secondary">Reset</button></div><div class="meter"><div id="progress"></div></div></div></section>
<aside class="panel"><h2 style="margin-top:0">Current appearance</h2><div class="kv"><span>Step</span><span id="step" class="v">1 / 120</span></div><div class="kv"><span>Sub-space</span><span id="space" class="v">01</span></div><div class="kv"><span>Visibility</span><span id="visibility" class="v">ON</span></div><div class="kv"><span>State</span><span id="state" class="v">TUNNELED</span></div><div class="kv"><span>Command</span><span id="command" class="v">MAJORANA_2</span></div><div class="kv"><span>Mode</span><span id="mode" class="v">MAJORANA_2_ENTANGLE</span></div><div class="kv"><span>Amplitude</span><span id="amplitude" class="v">0</span></div><div class="kv"><span>Time jump</span><span id="timejump" class="v">true</span></div><h3>5D ring-like coordinates</h3><pre id="ring" class="v" style="text-align:left;white-space:pre-wrap"></pre><div class="warn">This animation visualizes software state only. TUNNELED and time_jump are labels, not experimentally validated physical effects. The 5D mapping is dimensionless, not a solved spacetime geometry.</div></aside></main>
<script>
const commands = __COMMANDS__;
const ns = 'http://www.w3.org/2000/svg';
const svg = document.getElementById('network');
const coords = {};
for(let i=1;i<=36;i++){const a=-Math.PI/2+2*Math.PI*(i-1)/36;coords[i]=[400+345*Math.cos(a),400+345*Math.sin(a)];}
function line(x1,y1,x2,y2,color,opacity,width){const e=document.createElementNS(ns,'line');Object.entries({x1,y1,x2,y2,stroke:color,'stroke-opacity':opacity,'stroke-width':width}).forEach(([k,v])=>e.setAttribute(k,v));svg.appendChild(e);return e;}
const edgeSet=new Set();for(let i=1;i<=36;i++){for(const offset of [1,2,4,8,16]){const j=((i-1+offset)%36)+1;edgeSet.add([Math.min(i,j),Math.max(i,j)].join(':'));}}
for(const key of edgeSet){const [a,b]=key.split(':').map(Number);line(...coords[a],...coords[b],'#60a5fa',Math.abs(a-b)===1||Math.abs(a-b)===35?0.28:0.09,1.2);}
const routeLayer=document.createElementNS(ns,'g');svg.appendChild(routeLayer);
const nodeEls={};
for(let i=1;i<=36;i++){const [x,y]=coords[i];const g=document.createElementNS(ns,'g');const c=document.createElementNS(ns,'circle');c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',15);c.setAttribute('fill','#38bdf8');c.setAttribute('stroke','#e0f2fe');c.setAttribute('stroke-width','1.5');g.appendChild(c);const t=document.createElementNS(ns,'text');t.setAttribute('x',x);t.setAttribute('y',y+4);t.setAttribute('text-anchor','middle');t.setAttribute('font-family','monospace');t.setAttribute('font-size','10');t.setAttribute('font-weight','700');t.setAttribute('fill','#07111f');t.textContent=String(i).padStart(2,'0');g.appendChild(t);svg.appendChild(g);nodeEls[i]={g,c};}
let index=0,phase='ON',timer=null;
function drawRoute(){while(routeLayer.firstChild)routeLayer.removeChild(routeLayer.firstChild);const upto=Math.min(index,commands.length-1);for(let j=Math.max(0,upto-35);j<upto;j++){const a=commands[j].sub_space_id,b=commands[j+1].sub_space_id;lineInRoute(a,b,j===upto-1?0.9:0.18);}}
function lineInRoute(a,b,opacity){const [x1,y1]=coords[a],[x2,y2]=coords[b];const e=document.createElementNS(ns,'line');Object.entries({x1,y1,x2,y2,stroke:'#fb7185','stroke-opacity':opacity,'stroke-width':2.2}).forEach(([k,v])=>e.setAttribute(k,v));routeLayer.appendChild(e);}
function render(){const c=commands[index];Object.entries(nodeEls).forEach(([id,obj])=>{const active=Number(id)===c.sub_space_id;obj.c.setAttribute('fill',active?(phase==='ON'?'#fbbf24':'#475569'):'#38bdf8');obj.c.setAttribute('fill-opacity',active&&phase==='OFF'?'0.18':'1');obj.c.setAttribute('r',active&&phase==='ON'?'20':'15');});
document.getElementById('step').textContent=(index+1)+' / '+commands.length;document.getElementById('space').textContent=String(c.sub_space_id).padStart(2,'0');document.getElementById('visibility').textContent=phase;document.getElementById('state').textContent=c.state;document.getElementById('command').textContent=c.command;document.getElementById('mode').textContent=c.mode;document.getElementById('amplitude').textContent=String(c.amplitude);document.getElementById('timejump').textContent=String(c.time_jump);document.getElementById('ring').textContent=c.ring_5d.map((v,i)=>'x'+(i+1)+': '+v).join('\\n');document.getElementById('progress').style.width=((index+1)/commands.length*100)+'%';drawRoute();}
function stop(){if(timer!==null){clearInterval(timer);timer=null;}document.getElementById('play').textContent='Play';}
function next(){index=(index+1)%commands.length;phase='ON';render();}
document.getElementById('play').addEventListener('click',()=>{if(timer===null){document.getElementById('play').textContent='Playing…';timer=setInterval(()=>{phase=phase==='ON'?'OFF':'ON';if(phase==='ON')index=(index+1)%commands.length;render();},350);}});
document.getElementById('pause').addEventListener('click',stop);document.getElementById('next').addEventListener('click',()=>{stop();next();});document.getElementById('prev').addEventListener('click',()=>{stop();index=(index-1+commands.length)%commands.length;phase='ON';render();});document.getElementById('reset').addEventListener('click',()=>{stop();index=0;phase='ON';render();});render();
</script></body></html>'''
    output_path.write_text(document.replace("__COMMANDS__", commands_json), encoding="utf-8")


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
    html_path = output_dir / "vqb_cubity_36_subspaces.html"
    build_html(report, html_path)
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
    print(f"HTML animation: {html_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
