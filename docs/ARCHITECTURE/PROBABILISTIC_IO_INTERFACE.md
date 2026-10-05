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
