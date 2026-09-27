# WANGA-LAB Agent Network

**Status:** ARCHITECTURE_SPECIFIED  
**Issue:** #79

## Purpose
Define the bounded agent-network architecture for WANGA-LAB: twelve research/system groups, twenty-four specialist roles, four infrastructure agents, controlled cross-group relay, evidence gates, and deterministic routing.

## Group Registry

| Group | Scope | Agents |
|---|---|---|
| 01 Rational Logic | definitions, distinctions, validity | RL-01, RL-02 |
| 02 Contradiction Forensics | contradiction detection/taxonomy/reasoning operators | CF-01, CF-02, CF-03 |
| 03 Algorithmic Genealogy | model/source lineage | AG-01, AG-02 |
| 04 Vitruvius | architecture graph/lineage gates | V-01, V-02 |
| 05 WANGA Computer | composition/model fabric | WC-01, WC-02 |
| 06 Evidence & Provenance | collection/provenance/verification | EP-01, EP-02, EP-03 |
| 07 AI Drift Forensics | detection/reconstruction | DF-01, DF-02 |
| 08 Pre-Field / AIPREFIELD | representation/model/reality boundaries | PF-01, PF-02 |
| 09 TANTA | source/symbolic structure | TA-01, TA-02 |
| 10 231 / Combinatorics | combinatorics/gate registry | CO-01, CO-02 |
| 11 Abulafia / Historical Sources | extraction/historical context | HS-01, HS-02 |
| 12 Memory / Working Memory | state/checkpoints/context integrity | WM-01, WM-02 |

## Infrastructure

- OR-01 — Orchestrator
- BR-01 — Browser
- DO-01 — Documents
- AU-01 — Audit / Evidence Guardian

Infrastructure roles are bounded to their operational domains. Cross-domain work requires an explicit interface/handoff.

## Relay

The cross-group relay is a coordination/transport layer. It routes, delivers, receives, tracks and returns messages; it does not independently authorize, verify, or invent.

Required message identity:
`message_id, task_id, source_agent, source_group, destination_agent, destination_group, message_type, payload, context_refs, evidence_refs, verification_state, requires_response, requires_human_approval, timestamp`

## Stellar Path Orchestration

Celestial paths are a routing/reference-frame abstraction only:

`Position → Path → Next Position → Boundary Check → Handoff`

They do not provide authority, causal power, or an astrological inference.

## Routing

`Letter Combination → Address → Boundary Check → Agent → Operation`

Letter combinations are address/route identifiers. No causal efficacy is assumed.

## Path invariant

Every active agent must expose:
- Current Position
- Permitted Domain
- Next Permitted Transition
- Boundary Condition
- Evidence of Transition

If transition evidence is missing, state is `NOT_YET_VERIFIED`.

## State model

Work:
`DISCOVERED → CANDIDATE → MAPPED → IMPLEMENTED → TESTED → VERIFIED`

Evidence:
`UNKNOWN → SOURCED → PRESERVED → CROSS_CHECKED → VERIFIED`

No automatic `SPECIFIED → VERIFIED` transition.

## Boundary separations

`Agent Role ≠ Agent Instance ≠ Model Slot ≠ Runtime`

`Symbol ≠ Model ≠ Physical Reality`

`Routing ≠ Authority`

`Observation ≠ Verification`

## Prototype gate

Build order:
`Protocol → Registry → Relay → Research↔Relay↔Document test → Evidence → Browser → expansion`

Large-scale autonomous behavior is deferred until the message contract, routing, context boundaries, receipts, and verification gates have passed the prototype tests.
