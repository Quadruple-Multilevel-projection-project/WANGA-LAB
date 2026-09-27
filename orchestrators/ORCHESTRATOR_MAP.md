# Orchestrator Map

## Primary orchestration topology

Two primary orchestration nodes coordinate the full constellation:

1. **PRIMARY-28-ORCHESTRATOR** — coordinates GROUP-01..GROUP-28.
2. **PRIMARY-32-ORCHESTRATOR** — coordinates ROOT-01..ROOT-32.

They are peers inside one shared control plane, not isolated systems.

```text
PRIMARY-28-ORCHESTRATOR ──┐
                          ├──> CONSTELLATION BUS
PRIMARY-32-ORCHESTRATOR ──┘          │
                                     ▼
                         RELAY → THINKING MACHINE
                                     │
                                     ▼
                              DERIVATION GRAPH
                                     │
                                     ▼
                              DRIFT FORENSICS
                                     │
                                     ▼
                         EVIDENCE / RECEIPTS
                                     │
                                     ▼
                              ALERT MANAGER
```

## Unit fan-out

`PRIMARY-28-ORCHESTRATOR → GROUP-01..GROUP-28`

`PRIMARY-32-ORCHESTRATOR → ROOT-01..ROOT-32`

Each primary orchestrator maintains the identity, sequence, task state, health, and handoff state of its units.

## Round-robin cycle

`DISCOVER → RECEIVE → CLASSIFY → DERIVE → HANDOFF → ACK → NEXT`

Scheduling is deterministic by cluster revision, task ID, unit ID, and sequence number. Missing revisions require replay.

## Cross-plane handoff

When a task requires both letter/Thinking Machine processing and root/provenance processing:

`28-PLANE ↔ CONSTELLATION BUS ↔ 32-PLANE`

The handoff retains source references, derivation path, evidence, verification state, and receipt identity.

## Letter/state propagation semantics

`אות ↔ צירוף ↔ יחס ↔ מצב ↔ צירוף חדש`

This is the project's relational/state-transition semantics. It is not a claim of classical feed-forward propagation, fixed neural weights, biological neural tissue, or literal propagation of letters.

## Shared infrastructure

Both planes use:
- shared cluster revision
- shared change feed
- shared relay
- shared Alert Manager
- shared evidence receipts
- shared drift/replay contracts

No group or root creates an independent alerting or provenance system.

## Status boundary

The topology is **ARCHITECTURE_SPECIFIED**. Runtime connectivity, heartbeats, acknowledgements, replay, and deterministic multi-agent execution must be observed before promoting status.
