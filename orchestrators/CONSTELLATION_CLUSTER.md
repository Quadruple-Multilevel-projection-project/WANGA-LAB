# CONSTELLATION CLUSTER — LIVE UPDATE CONTROL PLANE

Status: IMPLEMENTED_ARCHITECTURE

## Purpose
One shared control-plane through which every GROUP and ROOT discovers current project state, receives updates, publishes health, preserves evidence receipts, and escalates material failures.

This is a routing/coordination mechanism, not a physical-architecture claim.

## Population
- 28 Thinking/Personal GROUP units
- 32 ROOT units
- parent orchestrators
- relay layer
- shared Alert Manager
- system-owner escalation channel

## Bootstrap contract
Every unit MUST on startup:
1. load its GROUP_ID / ROOT_ID and registry record;
2. load the current cluster manifest and revision;
3. load the current handoff and project-site map;
4. verify orchestrator connectivity;
5. verify relay connectivity;
6. verify the update-feed source;
7. publish a startup health receipt;
8. report READY only after required checks pass.

A missing required connection produces ERROR/ESCALATION. A unit must not claim READY by assumption.

## Continuous update contract
The cluster maintains a monotonic CLUSTER_REVISION.

Each material project change produces a CHANGE_EVENT containing:
- event_id
- cluster_revision
- generated_at
- source
- change_type
- affected_units
- summary
- evidence_refs
- commit_ref / issue_ref when applicable
- verification_state
- required_action

Units MUST consume changes in revision order. A revision gap produces UPDATE_GAP and requests replay from the last acknowledged revision.

## State propagation
SOURCE → CHANGE EVENT → CLUSTER FEED → GROUP/ROOT → LOCAL ACK → RECEIPT

There is no silent propagation failure.

## Health
Each unit periodically publishes:
- unit_id
- orchestrator_id
- last_seen
- cluster_revision_seen
- cluster_revision_acknowledged
- connector states
- current task
- verification state
- receipt reference

A stale or contradictory health state becomes an operational incident.

## Evidence
Every startup, update acknowledgement, replay, escalation, and recovery event gets a receipt containing event identity, observed revision, source reference, timestamp, and verification state.

Receipts prove observation/recording; they do not prove the underlying scientific or technical claim.

## Alerting
Material failures route:
UNIT → ORCHESTRATOR → ALERT MANAGER → EMAIL CONNECTOR → SYSTEM OWNER

Deduplication key:
INCIDENT_ID + EVENT_TYPE + AFFECTED_NODE

No group creates a private email subsystem.

## Decision boundary
The cluster automatically handles propagation, retries, health checks, receipts, deduplication, replay requests, and escalation. Only decisions requiring system-owner authority are returned as decision requests.
