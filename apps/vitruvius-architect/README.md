# Vitruvius Architect

Status: PROTOTYPED

A dependency-free browser prototype for the WANGA/Vitruvius meta-architecture.

## Source alignment

The prototype follows the existing repository architecture:

- Vitruvius is the highest architectural orchestration layer immediately preceding the rational-logic model layer.
- WANGA Lineage Tree records recursive genealogy.
- Architecture Family Lineage records architectural family descent and integration.
- WANGA Politeia provides whole-system lineage governance.
- Model selection is the boundary between lineage knowledge and Rational Logic.
- WANGA OS, Global Work Manager, Model Fabric, Digital Model Agents, evidence/provenance, drift forensics, verification, NTM, perspective and publication remain distinct components.

## Run

Open `index.html` in a browser. No build step or external dependency is required.

## Verification status

This is PROTOTYPED, not TESTED or VERIFIED. The GitHub contents write establishes the artifact only; it does not establish runtime correctness.

## Next increments

1. Connect the UI to the canonical Vitruvius index and lineage records.
2. Add graph/event persistence.
3. Add deterministic lineage queries.
4. Add compatibility evidence and validation state.
5. Add the explicit Vitruvius → Rational Logic handoff contract.


## Probabilistic I/O Interface

The existing frontend is preserved. A new Probabilistic I/O view exposes the proposal-only boundary implemented in `wanga_runtime/probabilistic_io.py`. It does not execute actions or mutate state.
