# 03 — Agent Orchestration

**Status: PROPOSED**

## Hierarchy

- **L0 — Supervisor:** routing policy, gate state, and kill-switch.
- **L1 — Domain agents O1–O8:** Registry, Resolver, Signal Bus, Participant Router, Parent Aggregator, Evidence, Neural Interface, Feedback.
- **L2 — Sub-agents:** per-repository and per-participant lanes (P1–P6).
- **L3 — Sub-sub-agents:** gate clusters and versioned rule packs.
- **L4 — Endpoint agents:** health probe, export worker, read-only connector, smoke runner, evidence writer.
- **L0-AUDIT:** independent read-only observer with no write rights.

This is a proposed registry, not proof that agents are running.

## Signal pipeline

`signal → schema normalization → four-step filter → schema validation → lattice/coordinate lock → evidence write → route to assigned L2 lane → aggregate at P0`

The named Ta'amei stages in the supplied design are Mahpach, Pashta, Zakef, and Siluk. Their operational meanings and acceptance semantics must be tied to the canonical Introduction and Gate 14 source before they can authorize an automated judgment. Until then they are configuration labels, not verified mathematical operators.

## Hard controls

- Agents do not read credentials.
- Only `evidence-writer` may write to the evidence store.
- Ambiguous Gate 14 interpretation returns `REQUIRES_REVIEW`.
- The declared 401 unresolved pairs remain `UNRESOLVED` until source-backed review closes them.
- L0 kill-switch must halt L2–L4 lanes within one cycle; this requires a test proving the bound.
- Provenance must be preserved during routing and aggregation.
- A neural proposal is not a formal commit; invalid type or failed precondition halts execution.

## Evaluation

Record lane violations, unauthorized writes, ambiguous-case handling, kill-switch latency, evidence completeness, and routing accuracy. Do not report scores until an evaluation set has been defined and run.
