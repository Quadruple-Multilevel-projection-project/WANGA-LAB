# Agent Orchestration Contract — L0–L4

**Status:** SPECIFIED, not yet runtime-verified.

1. **L0 — Orchestrator:** owns stop/continue, scope, and rollback decisions.
2. **L1 — Verification boundary:** validates `verification_result`, required source references, schemas, preconditions, and evidence status.
3. **L2–L4 — Execution and routing:** execute only approved, typed tasks; return outputs and evidence. No semantic interpretation of canonical source text.
4. **Source Editor (S7):** manually extracts exact source terms/relations and assigns source references under the canonical-source policy.

## Mandatory transition
`NEURAL_PROPOSAL → SOURCE_REFERENCE_CHECK → FORMAL_GATE → EVIDENCE_GATE → DETERMINISTIC_RESULT`

- A missing or unresolved sentence ID returns `REQUIRES_REVIEW` and halts the task.
- A neural proposal cannot change a formal decision.
- Contradictory or absent evidence remains unresolved; it is not silently normalized.
- Chapter 13 is an isolated node. No derived edge to Gate 14 is allowed until S7 approves exact extracted terms/relations and source references.
- Gate 14 definitions must be extracted from the canonical source; this document does not invent those definitions.

The named Ta'amei sequence (Mahpach → Pashta → Zakef → Siluk) is recorded as a requested conceptual filter. Its operational semantics remain `NOT_YET_VERIFIED` until a source-backed specification and tests define each transition.
