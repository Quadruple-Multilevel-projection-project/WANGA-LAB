# David Jones Box / KRAKEN

## Purpose

This directory is the engineering documentation boundary for the **David Jones Box** and the **KRAKEN** heterogeneous quantum-computing orchestration concept.

The David Jones Box is the bounded enclosure / integration boundary.

KRAKEN is the orchestration and computation fabric inside that boundary. **KRAKEN is not a single processor.**

The purpose of this documentation is to make the processor configuration, interfaces, evidence requirements, and verification gates explicit before the architecture is presented to a regulated financial institution.

## Current configuration statement

The current internal requirement is:

- **36 dual-processor configurations**
- **72 quantum processing positions / QPU positions**
- heterogeneous orchestration rather than a monolithic QPU
- bounded execution and explicit interfaces
- quantum and classical control paths documented separately

These numbers are recorded as **INTERNAL REQUIREMENT / NOT_YET_VERIFIED** until an engineering source, hardware specification, simulation, or laboratory test establishes them.

## Verification boundary

No claim in this directory should be interpreted as:

- a physically constructed quantum computer;
- demonstrated quantum advantage;
- a validated 72-QPU machine;
- a production-ready financial system;
- regulatory approval or certification.

The repository must preserve the distinction between:

`REQUIREMENT → ARCHITECTURE → SIMULATION → ENGINEERING VALIDATION → PHYSICAL TEST`

## Required configuration artifacts

1. Processor/accelerator inventory.
2. Per-processor interface contract.
3. Control-plane topology.
4. Quantum-classical data path.
5. Synchronization and latency budget.
6. Error-correction / decoding boundary.
7. Resource scheduling policy.
8. Failure isolation and recovery.
9. Provenance and evidence capture.
10. Drift-test integration.
11. Reproducibility specification.
12. Verification report.

## Status vocabulary

`BUILT · SPECIFIED · PROTOTYPED · TESTED · VERIFIED · PLANNED · HYPOTHETICAL`

No **VERIFIED** status without recorded evidence.
