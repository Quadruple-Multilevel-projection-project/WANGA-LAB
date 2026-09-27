# CLUSTER CHANGE FEED PROTOCOL

The feed is the shared update channel for all 60 routing units.

## Event envelope
event_id: EVT-...
cluster_revision: integer
generated_at: ISO-8601
source:
  type: github|project_site|orchestrator|group|root|system
  ref: string
change_type: architecture|instruction|code|evidence|verification|incident|recovery|handoff
affected_units: [GROUP-01, ROOT-01]
summary: string
evidence_refs: []
commit_ref: null
issue_ref: null
verification_state: NOT_YET_VERIFIED
required_action: string

## Rules
1. Revisions are monotonic.
2. Units acknowledge every event they consume.
3. Missing revisions trigger replay.
4. Duplicate events are idempotent by event_id.
5. Acknowledgement is not verification of the event's claim.
6. Failed delivery creates UPDATE_DELIVERY_FAILURE.
7. Repeated unchanged incidents are deduplicated.
8. A recovered CRITICAL/HIGH incident creates a recovery event.
9. No unit may invent missing evidence to close an event.
10. Events requiring owner authority are escalated instead of silently decided.

## Initial project-context sources
The project-site map is authoritative for current project-context discovery; GitHub is authoritative for repository state and implementation history. A conflict is preserved as a discrepancy and escalated when material.

## Operational invariant
Every unit should be able to answer:
- What is the latest cluster revision I know?
- What revision have I acknowledged?
- What changed since my last acknowledgement?
- Which evidence supports that change?
- Am I connected to the orchestrator, relay, feed, and Alert Manager?
