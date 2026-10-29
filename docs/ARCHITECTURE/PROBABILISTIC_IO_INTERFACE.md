# Probabilistic I/O Interface

Status: PROTOTYPED

## Purpose

This is the implementation of the external **Probabilistic I/O Interface** specification.
It is a proposal boundary, not an autonomous supervisor and not an instruction to the
ChatGPT runtime itself.

## Boundary

`ProbabilisticIOInterface.propose()`:

1. accepts a structured request;
2. validates required context and boundary conditions;
3. emits a deterministic JSON envelope;
4. never executes the proposed action;
5. never mutates persistent state;
6. emits `STATUS: LOGICAL_HALT_TRIGGERED` when the request cannot be safely represented.

### Output contract

```json
{
  "supervisor_status": "PENDING_VERIFICATION",
  "logical_state_id": "AGENT_DEMOTED_TO_PROBABILISTIC_IO // AWAITING_SUPERVISOR_COMMAND",
  "payload": "<proposal-or-halt>",
  "validation": {
    "valid": true,
    "contradiction_vector": [],
    "missing_context": []
  }
}
```

The supervisor status is a field in the **built system**. It does not alter the execution
status of the ChatGPT model used to develop or inspect this repository.

## Halt rule

The implementation does not invent a justification when context is missing or a request
crosses the execution boundary. It returns the exact halt marker plus a machine-readable
contradiction vector.

## Existing frontend

The existing `apps/vitruvius-architect/` browser prototype is retained. The new interface
is an additional view inside that frontend; it does not replace the saved frontend.


## Deterministic logical-consistency gate

Before a proposal is accepted, the request must carry a `logical_consistency` object containing three distinct layers:

1. **First-order logic** — `internal`, `external`, `coordination`.
2. **Second-order logic / type-genus layer** — three distinct parts: `part_1`, `part_2`, `part_3`.
3. **Private/particular logic** — three distinct parts for the current investigation.

The private/particular layer is **not** treated as a third or higher logical order. It is the completion layer for the specific investigation.

The gate rejects:
- missing parts;
- explicit cross-level contradictions;
- treating private logic as a higher order;
- closing an investigation before private logic is complete.

A rejection uses the exact halt marker and a machine-readable contradiction/missing-context vector.

## Deterministic session continuity

The repository now contains `wanga_runtime/continuity.py`. It provides:

- `LogicalConsistencyGate` for the three-layer structural check;
- `SessionCheckpoint` for minimal sufficient session state;
- deterministic JSON serialization;
- checkpoint validation;
- a SHA-256 digest for the serialized checkpoint.

A checkpoint records objective, status, completed action, facts, decisions, evidence, repository state, changed files, blockers, open questions, remaining gap, exactly one next action, prohibited drift targets, unverified claims, and logical-consistency state.

A checkpoint is a **continuity artifact, not an authority above current evidence**. On a new session, current repository/CI evidence outranks an old checkpoint. If the checkpoint conflicts with current evidence, it is stale and must be reconstructed.

### Session transition

`SESSION → CHECKPOINT → RESTORE → VERIFY AGAINST CURRENT STATE → NEXT ACTION`

The system must not claim that a conversation-ending note is automatically written by the runtime. The deterministic mechanism is implemented; the host/agent must invoke checkpoint creation at the end of each work session.

## Verification boundary

The implementation is not `VERIFIED` merely because code exists. The required progression remains:

`SPECIFIED → PROTOTYPED → BUILT → TESTED → VERIFIED`

with evidence at each transition.
