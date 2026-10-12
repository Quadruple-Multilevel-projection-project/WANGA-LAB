# Logical AI Kernel V1 — Implementation Specification

## Scope
This is the first executable symbolic subsystem for WANGA-LAB. It gives the project an actual deterministic rule engine now, while deliberately not claiming a general autonomous AI.

## Interface contract
Input JSON:
- `evidence[]`: unique ID, URI, version, location and evidence state.
- `claims[]`: unique ID, atom, epistemic state and evidence IDs.
- `rules[]`: unique ID, active/disabled status, antecedent atom patterns, consequent and source references.

Output JSON:
- claim-level input eligibility and rejection reason;
- input and derived facts with epistemic status;
- rule firings, premise IDs and source references;
- contradiction set;
- round/fixed-point status;
- machine-readable limitations.

## The four gates
1. Evidence ID and epistemic-status gate.
2. Explicit deterministic rule evaluation.
3. Contradiction detection and fail-closed inference.
4. Scope/permission/publication gate.

## Why this is a logical AI kernel, not a full AI
It reasons over structured symbols and rules but does not parse arbitrary language, acquire rules autonomously, learn semantics from the 231-gate table, or generate natural-language answers. To connect it to an LLM, add an adapter that converts language to candidate structured input, then routes all conclusions through this kernel and returns the trace. The adapter must not turn unverified inferences into facts.

## Required next increments
1. Establish a source-backed ontology of atoms and relation types.
2. Recover original four mathematical/logical weight-layer definitions from the repository/source archive.
3. Define and test the five-forward/five-return stage contracts as separate interfaces.
4. Add rule coverage, contradiction, precision/recall and false-positive test sets.
5. Add an LLM adapter only after bounded structured I/O tests exist.
6. Add a controlled GitHub/Wix write executor requiring approval; no live publication API is called by this kernel.
7. Compare results against a simple baseline and retain failing fixtures.

## Test matrix
Unit tests cover exact combinatorics; evidence gate; missing references; hypotheses not seeding rules; contradictions; disabled rules; scoped actions; publication permission; threshold drift; real repository corpus invariants; and CLI JSON validity.
