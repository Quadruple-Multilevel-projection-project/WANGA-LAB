# Stellar Path Orchestration

## Status

**ARCHITECTURE_SPECIFIED**

This document defines a routing/orchestration model in which a fixed celestial reference frame is used as a deterministic navigation model. The celestial representation is a routing abstraction; it is not treated as a source of computational authority or physical causal force.

## Purpose

The orchestration layer gives each participating agent a reproducible path:

**Position → Path → Next Position → Boundary Check → Handoff**

The objective is to make agent movement observable, bounded, replayable, and compatible with drift forensics.

## Four-Agent Geometry

The initial routing model defines four agents, each assigned:

- a 90° operating domain;
- hard boundaries;
- a permitted path;
- one of three depth levels;
- an active address;
- defined boundary neighbors.

An agent must not cross an assigned boundary without an explicit handoff.

The four-agent geometry is represented as:

**4 × 3 CELLS**

with the depth dimension providing three routing layers.

## Path Invariant

At every observable transition, an agent must have:

1. current position
2. permitted domain
3. next permitted transition
4. boundary condition
5. transition evidence

If any required element is missing, the system must not infer that the agent remains on-path. The state is:

**NOT_YET_VERIFIED**

## Transition Model

A path is represented as a sequence:

**P₀ → P₁ → P₂ → P₃ → ...**

Each transition records the expected and actual position.

Conceptually:

**EXPECTED PATH → ACTUAL PATH → DRIFT DETECTOR**

If the actual transition remains within the permitted boundary:

**WITHIN_BOUNDARY → CONTINUE**

If it exits the permitted boundary:

**OUTSIDE_BOUNDARY → STOP / HANDOFF / AUDIT**

## Integration with Agent Relay

The Stellar Path layer does not replace the Cross-Group Agent Relay.

The separation is:

**Orchestrator** → determines task decomposition and routing intent

**Relay** → delivers messages between groups and preserves communication context

**Stellar Path** → constrains and records the permitted navigation path

**Evidence Guardian** → evaluates whether the recorded transition has sufficient evidence

A cross-group transition therefore follows:

**TASK → ROUTE → POSITION CHECK → RELAY → HANDOFF → OBSERVATION → EVIDENCE → VERIFICATION**

## Capability and Boundary Rules

Routing must remain capability-based. A celestial position does not grant an agent authority to perform a capability it does not possess.

The path model answers:

- Where is the agent?
- Which domain is active?
- Which transition is permitted?
- Which neighboring boundary may receive a handoff?
- What evidence records the transition?

It does not answer whether a professional claim is true.

## Drift Forensics

The expected path becomes a baseline.

For each transition:

**Expected Transition ≠ Actual Transition**

is an observable comparison.

A deviation is not automatically classified as a system failure. It is first recorded as a path deviation and then evaluated against:

- permitted boundary;
- task state;
- capability registry;
- message context;
- evidence state;
- handoff policy.

## Authority Boundary

The Stellar Path Orchestration layer:

- routes;
- constrains;
- records;
- detects path deviation;
- requests handoff or audit.

It does not independently:

- authorize external actions;
- declare evidence VERIFIED;
- alter ontology;
- create unrestricted capabilities;
- override human approval;
- convert symbolic structure into physical claims.

## Runtime Objects

A path transition should be representable using objects compatible with the WANGA-LAB core model:

**TASK · AGENT · POSITION · PATH · TRANSITION · BOUNDARY · HANDOFF · MESSAGE · EVIDENCE · VERIFICATION**

A transition receipt should minimally bind:

- task_id
- agent_id
- source_position
- destination_position
- permitted_domain
- boundary_result
- message_id when a relay is involved
- evidence_refs
- timestamp
- verification_state

## Implementation Sequence

Do not begin with large-scale autonomous behavior.

Recommended sequence:

1. Define position/path schema.
2. Define the 4 × 3 routing registry.
3. Define boundary rules.
4. Integrate with the Cross-Group Agent Relay.
5. Run a deterministic multi-agent path test.
6. Record transition receipts.
7. Add drift detection.
8. Connect the Evidence Guardian.
9. Expand the routing registry only after the protocol is tested.

## Design Principle

The celestial model is a **reference frame**, not an authority.

The invariant is:

**Every agent must be locatable, bounded, transition-constrained, and evidence-linked.**

That converts “not getting lost” from an informal assertion into a testable system property.
