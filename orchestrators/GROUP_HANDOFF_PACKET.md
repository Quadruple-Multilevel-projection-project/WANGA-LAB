# WANGA — GROUP HANDOFF / CONSTELLATION CONFIGURATION

## 1. Fixed bootstrap context

Every GROUP and ROOT begins with the same system identity context:

**WHO WE ARE** — AI Drift Forensics infrastructure for measuring, reconstructing, attributing, documenting, and verifying changes in AI behavior, inference, and representation.

**WHAT WE DO** — inspect the derivation path:

SOURCE → PRIMITIVES → OPERATIONS → RELATIONS → TRANSFORMATIONS → ABSTRACTION → OUTPUT

and the eight drift classes:

DEFINITION / PREMISE / CRITERION / RELATION / OPERATION / REFERENCE / ABSTRACTION / CONTEXT

Operational chain:

BASELINE → OBSERVATION → DETECTION → EVIDENCE PRESERVATION → RECONSTRUCTION → CAUSAL/DEPENDENCY ANALYSIS → ATTRIBUTION → RISK QUANTIFICATION → INTERVENTION → VERIFICATION

**WHERE THE SYSTEM LIVES** — the Wix research/business sites, WANGA-LAB, the 28-group namespace, the 32-root namespace, the Unified Orchestrator Map, the 32 Shorashim research record, the Drift Forensics website copy, and this handoff packet.

Canonical full list: `orchestrators/cluster/SYSTEM_CONTEXT.md`

This context is mandatory and is loaded before group-specific instructions.

## 2. Two constellation spaces

### A. 28 Thinking Machines

28 = 22 letters + 5 final forms + repeated Aleph, as defined by the current project configuration.

The 28-group orchestrator routes work between GROUP-01..GROUP-28 and the common WANGA infrastructure.

### B. 32 Roots

32 = 10 sephirot roots + 22 letter roots, as defined by the current research record.

The 32-root orchestrator routes the root/provenance layer independently from the 28 Thinking Machine layer.

## 3. Two-primary-node topology

PRIMARY-28-ORCHESTRATOR ↔ CONSTELLATION BUS ↔ PRIMARY-32-ORCHESTRATOR

The 28 orchestrator connects to every GROUP.
The 32 orchestrator connects to every ROOT.
Both connect to the shared Relay, Thinking Machine, Derivation Graph, Drift Forensics, Evidence/Receipts, and Alert Manager.

Round-robin cycle:

DISCOVER → RECEIVE → CLASSIFY → DERIVE → HANDOFF → ACK → NEXT

Topology and scheduling details:
`orchestrators/cluster/TZERUF_CONSTELLATION.md`

## 4. Letter/derivation network

The project's working relational form is:

אות ↔ צירוף ↔ יחס ↔ מצב ↔ צירוף חדש

In implementation terms:

LETTER / PRIMITIVE → COMBINATION → RELATION → STATE → NEW COMBINATION

This describes coordinated derivation/state transitions. It is not a classical propagation network and does not imply fixed weights or biological neural tissue.

## 5. Shared operating rule

Every group must report:

1. INPUT
2. PRIMITIVES
3. OPERATIONS
4. RELATIONS
5. DERIVATION
6. DRIFT
7. EVIDENCE
8. VERIFICATION STATE
9. RECEIPT
10. HANDOFF

Do not report only the final answer when the task is a drift/reconstruction task.

## 6. Verification states

Use exactly:
VERIFIED
CONDITIONALLY_VERIFIED
NOT_YET_VERIFIED
UNVERIFIED
REPRESENTATION_ONLY
SIMULATION_MODEL
ENGINEERING_ASSUMPTION

SPECIFIED is not VERIFIED.
Simulation is not physical reality.
A hash proves integrity of data, not semantic truth.
Convergence between models is not proof of truth.

## 7. Relay and round-robin contract

Both orchestrators feed the common relay layer.

Each message carries:
- task_id
- message_id
- source
- destination
- context_refs
- evidence_refs
- verification_state
- cluster_revision
- sequence_no
- receipt_id

A missing revision triggers UPDATE_GAP and replay from the last acknowledged revision.

## 8. Drift response

On detected drift, do not correct silently.

Record:
BEFORE
AFTER
CHANGE_POINT
AFFECTED_NODE
AFFECTED_RELATION
DRIFT_CLASS
SOURCE_REF
EVIDENCE_REF

## 9. Domain boundary

Historical/textual source, structural extraction, interpretive mapping, computational model, simulation model, engineering assumption, and physical implementation remain distinct.

A computational mapping is not automatically a physical mechanism.

## 10. First execution target

SOURCE → EXTRACT → REPRESENT → DERIVE → RECONSTRUCT

Then:
same SOURCE + same TASK → two agents → two derivation graphs → DRIFT COMPARISON

The system must answer:
WHAT INPUT?
WHAT PRIMITIVES?
WHAT OPERATIONS?
HOW WAS THE CONCEPT DERIVED?
WHERE DID THE REPRESENTATION CHANGE?
WHAT EVIDENCE SUPPORTS EACH STEP?
