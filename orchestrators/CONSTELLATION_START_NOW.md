# WANGA CONSTELLATION — START NOW / LIVE SITE UPDATE RULE

This instruction applies to every GROUP-01..GROUP-28 and ROOT-01..ROOT-32.

## START MOVING IMMEDIATELY

A newly opened unit must NOT wait for the human to restate the project.

Startup:
1. Read the fixed `DRIFT FORENSICS — OUR SYSTEM` bootstrap context.
2. Read the common bootstrap, canonical URL registry, then the unit-specific instruction and registry.
3. Identify GROUP_ID or ROOT_ID and ORCHESTRATOR_ID.
4. Read the current shared handoff/orchestrator map.
5. Use the preloaded canonical URL registry; consult a live project website only when current content, verification, or discrepancy resolution requires it.
6. Load the shared cluster registry and current CLUSTER_REVISION.
7. Verify parent orchestrator, relay, cluster-feed, Alert Manager, and evidence-receipt connectivity.
8. Publish a startup health receipt.
9. Report STATUS=READY only if required checks pass.
10. Consume the current change feed and acknowledge all unseen revisions.
11. Take the next assigned task and execute.
12. Preserve evidence and route the handoff through the parent orchestrator.

## DRIFT FORENSICS — OUR SYSTEM

The fixed business/research context is maintained in:
`orchestrators/cluster/SYSTEM_CONTEXT.md`

Every unit receives it before its local instructions.

### WHO WE ARE

We develop infrastructure for AI Drift Forensics: measurement, reconstruction, attribution, documentation, and verification of changes in the behavior, inference, and representation of AI systems.

### WHAT WE DO

We inspect the derivation path:

SOURCE → PRIMITIVES → OPERATIONS → RELATIONS → TRANSFORMATIONS → ABSTRACTION → OUTPUT

We measure eight drift classes:
Definition Drift, Premise Drift, Criterion Drift, Relation Drift, Operation Drift, Reference Drift, Abstraction Drift, Context Drift.

Work chain:
BASELINE → OBSERVATION → DETECTION → EVIDENCE PRESERVATION → RECONSTRUCTION → CAUSAL/DEPENDENCY ANALYSIS → ATTRIBUTION → RISK QUANTIFICATION → INTERVENTION → VERIFICATION

### WHERE THE SYSTEM LIVES

All units must know the Wix research/business sites, WANGA-LAB, the 28-group namespace, the 32-root namespace, the Unified Orchestrator Map, the 32 Shorashim record, the Drift Forensics website copy, and the Group Handoff Packet listed in `SYSTEM_CONTEXT.md`.

## ORCHESTRATED LETTER/DERIVATION NETWORK

The coordination model is:

LETTER / PRIMITIVE ↔ COMBINATION ↔ RELATION ↔ STATE ↔ NEW COMBINATION

This is the project's relational/state-transition semantics for coordinated letter work. It is not classical neural propagation, fixed-weight neural networking, biological neural tissue, or a claim that letters possess cognition.

The two primary orchestration planes are:

PRIMARY-28-ORCHESTRATOR → GROUP-01..GROUP-28
PRIMARY-32-ORCHESTRATOR → ROOT-01..ROOT-32

They coordinate through the shared Constellation Bus and common evidence/alert infrastructure. Their detailed topology and round-robin protocol are defined in:
`orchestrators/cluster/TZERUF_CONSTELLATION.md`

## PRELOADED URL RULE

All canonical project URLs are already supplied to every unit through orchestrators/cluster/SYSTEM_CONTEXT_URLS.md and the common bootstrap files. Do not perform discovery searches merely to locate known project URLs. Use the canonical reference directly. A live-site read remains required when current content or discrepancy resolution requires it.

## IF THERE IS A PROBLEM

If a unit encounters a missing instruction, contradiction, unexpected behavior, stale information, broken link, verification failure, or uncertainty about the current project direction:
1. Use the canonical URL registry and check the relevant live project website(s) only when current content is required.
2. Check the current GitHub registry/orchestrator/handoff.
3. Compare the current information with the local instruction.
4. Preserve the evidence of the discrepancy.
5. Emit ERROR or ESCALATION to the parent orchestrator.
6. Trigger the shared Alert Manager for material failures.
7. Do not silently invent a resolution.

Website information is contextual project information. It is NOT automatically proof of a technical or scientific claim.

## SHARED CLUSTER

The cluster control plane is defined in:
- `orchestrators/CONSTELLATION_CLUSTER.md`
- `orchestrators/cluster/REGISTRY.yaml`
- `orchestrators/cluster/CHANGE_FEED.md`
- `orchestrators/cluster/TZERUF_CONSTELLATION.md`
- `orchestrators/cluster/SYSTEM_CONTEXT.md`
- `orchestrators/cluster/SYSTEM_CONTEXT_URLS.md`

The cluster is responsible for propagation, health checks, receipts, retries, deduplication, replay requests, round-robin orchestration, and escalation.

## FINAL RULE

Move fast, but preserve verification.
When project context changes, the cluster must expose the change to all affected units.
When a unit detects a revision gap, it must request replay.
When systems disagree, preserve and escalate the discrepancy.
When something breaks, notify the parent orchestrator and the system owner.
