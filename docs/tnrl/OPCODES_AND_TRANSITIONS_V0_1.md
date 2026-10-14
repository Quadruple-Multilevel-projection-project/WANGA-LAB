# TNRL v0.1 — Opcode and State-Transition Contract

Status: **SPECIFIED — NOT YET VERIFIED**  
Scope: deterministic interface contract; not a claim of zero defects or complete runtime safety.

## Invariant

`NEURAL_PROPOSAL != FORMAL_COMMIT`

A proposal is untrusted input. JSON Schema validation is only the first gate; it does not prove semantic correctness, truth of evidence, or safety of an operation.

## Opcodes

| Opcode | Meaning | Required evidence | State mutation |
|---|---|---|---|
| `READ` | Request an observation of a named target | Source/reference for the observation | No |
| `ASSERT` | Submit a claim for formal checking | Evidence references and a checkable predicate | No, unless a separate approved transition is committed |
| `TRANSFORM` | Propose a deterministic transformation | Input identity, transformation rule, constraints | Proposal only |
| `VALIDATE` | Check types, invariants, and preconditions | Applicable rule identifiers | No |
| `PROPOSE_STATE_TRANSITION` | Request a specific state change | From/to state, transition-rule ID, evidence | No; request only |
| `HALT` | Stop processing the current proposal | Failure code and audit event | Moves execution controller to HALTED; does not imply rollback |

Unknown opcodes MUST be rejected. An opcode name alone never grants permission to execute.

## Gate order

1. Parse input; reject malformed JSON.
2. Validate against `NIR_SCHEMA_V0_1.json`.
3. Resolve every referenced rule and evidence item; reject missing references.
4. Type-check the operation and target.
5. Evaluate all preconditions against the current authoritative state.
6. Check authorization and applicable policy.
7. Validate the proposed transition against the transition table.
8. Commit atomically only if every gate passes and the transition rule explicitly permits commit.
9. Record the decision, inputs, evidence identifiers, rule versions, resulting state hash, and failure reason if rejected.

Any failure before commit MUST fail closed: no requested state mutation is applied. A process-level `sys.exit(1)` may stop a command-line process, but it is not itself a proof of rollback, containment, or system-wide safety.

## State-transition table

| Current state | Event / condition | Next state | Commit allowed? |
|---|---|---|---|
| `RECEIVED` | Input parses | `PARSED` | No |
| `RECEIVED` | Parse failure | `REJECTED` | No |
| `PARSED` | Schema and type checks pass | `VALIDATED` | No |
| `PARSED` | Schema/type check fails | `REJECTED` | No |
| `VALIDATED` | Evidence, preconditions, authorization, and transition rule all pass | `READY_TO_COMMIT` | No |
| `VALIDATED` | Any required gate fails or evidence is unresolved | `REJECTED` | No |
| `READY_TO_COMMIT` | Atomic commit succeeds | `COMMITTED` | Yes, for the explicitly authorized transition only |
| `READY_TO_COMMIT` | Commit conflict or storage error | `FAILED` | No |
| Any nonterminal state | Explicit halt or unrecoverable validation error | `HALTED` | No |
| `COMMITTED` | Audit record successfully persisted | `AUDITED` | Already committed; audit completion does not expand authority |
| `COMMITTED` | Audit persistence fails | `AUDIT_PENDING` | No further commits until reconciled |
| `REJECTED`, `HALTED`, `FAILED`, `AUDITED` | New proposal | New independent `RECEIVED` record | No inherited authorization |

Terminal statuses are not interchangeable. In particular, `REJECTED` is a validation outcome, `HALTED` is a control outcome, and `FAILED` is an execution/storage outcome.

## Required tests before claiming verification

- Reject unknown opcode and unexpected fields.
- Reject missing, unresolved, or malformed evidence references.
- Reject invalid types and false preconditions.
- Reject unauthorized transitions and stale state versions.
- Prove rejected proposals do not mutate authoritative state.
- Test atomicity under concurrent updates and storage failures.
- Verify audit records bind proposal, rules, evidence, decision, and state hashes.
- Run negative tests and publish the exact command, environment, results, and commit SHA.

## Assurance boundary

This document defines intended behavior. It does not establish `epsilon = 0`, prove that all possible failures are covered, or show that a runtime implementation already enforces these rules. Those claims require executable implementation, independent tests, and formal proof for explicitly stated properties.
