# CLUSTER CHANGE FEED PROTOCOL

The feed is the shared update channel for all 60 routing units and both primary orchestrators.

## Event envelope

event_id: EVT-...
cluster_revision: integer
generated_at: ISO-8601
source:
  type: github|project_site|orchestrator|group|root|system
  ref: string
change_type: architecture|instruction|code|evidence|verification|incident|recovery|handoff|orchestration
affected_units: [GROUP-01, ROOT-01]
affected_orchestrators: [PRIMARY-28-ORCHESTRATOR]
summary: string
evidence_refs: []
commit_ref: null
issue_ref: null
verification_state: NOT_YET_VERIFIED
required_action: string

## Routing rules

1. Revisions are monotonic.
2. Primary orchestrators receive and sequence events for their unit planes.
3. Units acknowledge every event they consume.
4. Missing revisions trigger replay.
5. Duplicate events are idempotent by event_id.
6. Acknowledgement is not verification of the event claim.
7. Failed delivery creates UPDATE_DELIVERY_FAILURE.
8. Cross-plane events are routed through CONSTELLATION-BUS and preserve provenance.
9. Repeated unchanged incidents are deduplicated.
10. A recovered CRITICAL/HIGH incident creates a recovery event.
11. No unit may invent missing evidence to close an event.
12. Events requiring owner authority are escalated instead of silently decided.

## Round-robin sequencing

The two primary orchestrators run:

DISCOVER → RECEIVE → CLASSIFY → DERIVE → HANDOFF → ACK → NEXT

A unit's sequence number is retained with task_id, event_id, cluster_revision, and receipt_id.

## Project-context sources

The project-site map is authoritative for current project-context discovery; GitHub is authoritative for repository state and implementation history. A conflict is preserved as a discrepancy and escalated when material.

## Operational invariant

Every unit and both primary orchestrators should be able to answer:
- What is the latest cluster revision known?
- What revision has been acknowledged?
- What changed since the last acknowledgement?
- Which evidence supports the change?
- Which orchestrator owns the current task?
- Am I connected to the required control-plane services?
