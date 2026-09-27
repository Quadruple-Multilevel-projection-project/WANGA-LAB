# WANGA-LAB Agent Network

Infrastructure boundary model: 4 infrastructure agents × 3 depth layers = 12 operational cells.

Agents are roles; runtime instances and model slots are separate concerns.

## Boundary rule
Each infrastructure agent owns a 90° operational domain. Cross-domain movement requires an explicit interface/handoff. No agent may acquire another domain's authority merely by communicating with it.

## Core agents
- OR-01 Orchestrator — task, scheduling, routing, coordination; cannot alter evidence or determine truth.
- BR-01 Browser — external-world navigation, retrieval, forms, observations; cannot verify claims.
- DO-01 Documents — document extraction, OCR, structure; cannot determine meaning beyond extraction.
- AU-01 Audit Guardian — evidence, provenance, verification gates; cannot perform research in place of research agents.

## Path invariant
Every active agent must have: Current Position, Permitted Domain, Next Permitted Transition, Boundary Condition, Evidence of Transition.

## Status semantics
Observation ≠ Verification. Routing ≠ Authority. Symbol ≠ Model ≠ Physical Reality.
