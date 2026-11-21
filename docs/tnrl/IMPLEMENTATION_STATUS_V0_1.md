# TNRL v0.1 — Implementation Status

**Repository:** `Quadruple-Multilevel-projection-project/WANGA-LAB`  
**Branch:** `tnrl-nir-v0-1`  
**Status:** SPECIFIED; NOT YET VERIFIED

## Present in this branch

- `NIR_SCHEMA_V0_1.json`: proposal data shape.
- `OPCODES_AND_TRANSITIONS_V0_1.md`: opcode meanings, fail-closed gate order, state-transition contract.
- This file: explicit implementation and assurance boundary.

## Not yet established

- A working TNRL runtime that enforces this contract.
- Graph/FOL execution and a concrete rule registry.
- A persistent authoritative state machine with atomic commit.
- Automated unit, integration, concurrency, and adversarial tests.
- A formal proof of soundness, completeness, or zero error.
- A standalone repository or merged pull request.

## Acceptance criteria

Do not label this implementation BUILT, TESTED, or VERIFIED until the corresponding artifact exists and its evidence is recorded. Schema validation alone is not runtime verification. A successful commit is not proof that the committed design is correct.
