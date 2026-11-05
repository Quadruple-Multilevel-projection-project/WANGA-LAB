# TZERUF CONSTELLATION — TWO-PLANE ORCHESTRATION

Status: ARCHITECTURE_SPECIFIED

## Purpose

This layer coordinates the two primary orchestration nodes:

- PRIMARY-28-ORCHESTRATOR: coordinates GROUP-01..GROUP-28.
- PRIMARY-32-ORCHESTRATOR: coordinates ROOT-01..ROOT-32.

They are not independent islands. They form one coordinated routing fabric through the shared Constellation Bus, Relay, Thinking Machine, Derivation Graph, Drift Forensics, Evidence/Receipts, and Alert Manager.

## Topology

```text
                         CONSTELLATION CONTROL PLANE
                                   │
                 ┌─────────────────┴─────────────────┐
                 │                                   │
     PRIMARY-28-ORCHESTRATOR             PRIMARY-32-ORCHESTRATOR
                 │                                   │
        ┌────────┼────────┐                  ┌───────┼────────┐
        │   GROUP-01..28  │                  │   ROOT-01..32 │
        └────────┬────────┘                  └───────┬────────┘
                 │                                   │
                 └──────────────┬────────────────────┘
                                │
                         CONSTELLATION BUS
                                │
          RELAY → THINKING MACHINE → DERIVATION GRAPH
                                │
                         DRIFT FORENSICS
                                │
                   EVIDENCE / RECEIPTS
                                │
                         ALERT MANAGER
```

The diagram expresses logical routing and coordination. It is not a claim about physical neural architecture.

## Round-robin scheduling

The two primary orchestrators share a deterministic orchestration cycle:

1. DISCOVER — load current revision, task, source context, and unit state.
2. RECEIVE — accept an event or task for the local plane.
3. CLASSIFY — identify source/name/operation/state and required verification.
4. DERIVE — execute the authorized work and preserve the derivation path.
5. HANDOFF — route the result to the next unit, peer plane, or common engine.
6. ACK — record acknowledgement and evidence receipt.
7. NEXT — advance to the next eligible unit/event.

Scheduling keys:

- cluster_revision
- task_id
- unit_id
- sequence_no
- event_id
- receipt_id

A missed revision creates UPDATE_GAP and REPLAY_FROM_LAST_ACK. A duplicate event is idempotent by event_id.

## Cross-plane routing

The 28 plane owns the Thinking Machine group namespace and task distribution.

The 32 plane owns the root/provenance namespace and root-level research distribution.

A task may cross planes when its derivation requires both a Thinking Machine representation and a root/provenance relation. The cross-plane handoff must retain:

SOURCE → PRIMITIVES → OPERATIONS → RELATIONS → TRANSFORMATIONS → ABSTRACTION → OUTPUT

and the full evidence/provenance chain.

## Letter propagation model

The project may describe this coordination as propagation of letters that understand what they are doing. The implementation definition is narrower and testable:

```text
LETTER / PRIMITIVE
      ↕
COMBINATION
      ↕
RELATION
      ↕
STATE
      ↕
NEW COMBINATION
```

A unit does not receive an unexplained semantic signal. It receives an explicitly represented combination, relation, state transition, task context, and provenance.

Therefore:

- no classical feed-forward propagation assumption;
- no fixed conventional neural-network weights;
- no claim that letters themselves possess cognition;
- no claim of biological neural behavior;
- every transition is represented and replayable.

## Coordination invariants

1. No unit is outside its parent orchestrator.
2. No parent orchestrator bypasses the shared evidence and alert layer for material incidents.
3. No cross-plane handoff loses provenance.
4. No acknowledgement promotes verification state.
5. No missing evidence is filled by assumption.
6. No revision gap is silently skipped.
7. No drift correction is silently applied.
8. No computational analogy is promoted to physical reality.

## Unit state

Each unit exposes:

`DISCOVERING → READY → WORKING → HANDOFF_PENDING → ACKED → NEXT`

Failure states:

`ERROR → ESCALATION → ISOLATED/REPLAY → RECOVERY`

A unit may not report READY when a required connection or evidence receipt is unavailable.

## Continuous update path

`SOURCE CHANGE → CHANGE EVENT → CONTROL PLANE → PRIMARY ORCHESTRATOR → UNIT → ACK → RECEIPT → NEXT EVENT`

Material project changes must be visible to both primary planes unless explicitly scoped to one plane.

## Verification boundary

This topology is currently ARCHITECTURE_SPECIFIED until runtime heartbeat, event acknowledgements, replay, and deterministic multi-agent tests provide evidence for later states.
