# WANGA-X — Executable Requirement-Driven Blueprint Prototype V1

**Date:** 2026-10-12  
**Status:** BUILT AS A STRUCTURAL PROTOTYPE / NOT YET VERIFIED AS A NEURAL MODEL GENERATOR.

## Source architecture recovered

The model being reconstructed is the WANGA-X requirement-first paradigm, supported by the Neural Thinking Machine and Model Fabric:
- [WANGA-X Research Foundations](WANGA_X_RESEARCH_FOUNDATIONS.md) defines Request → Requirement → Required Neural Computation → Structure → Blueprint → Neural Computer → Execution.
- [WANGA-X Reversible Architecture](WANGA_X_REVERSIBLE_ARCHITECTURE.md) defines immutable construction frames plus pause, snapshot, inspect, rollback, edit, rebuild, verify and commit operations.
- [NTM Orchestrator V1](../wanga-research-groups/neural-thinking-machine/NTM_ORCHESTRATOR_V1.md) defines the analysis/critique/verification loop and prohibits treating inference as observation.
- [NTM Multi-Model Orchestration](../wanga-research-groups/neural-thinking-machine/ORCHESTRATION_MODEL_V1.md) defines bounded model roles, cross-review, disagreement preservation and provider-neutral adapters.
- [Model Agent Architecture](MODEL_AGENT_ARCHITECTURE_V1.md) defines model slots and the activation lifecycle.
- [WORK_MEMORY_STATE](WORK_MEMORY_STATE.json) records 5,000 allocated model slots but 0 connected and 0 verified endpoints.

This is the target architecture being prototyped, not a claim that all components are deployed.

## Implemented in this change

- A machine-readable computation and component catalogue.
- Requirement normalization and task profiles.
- Mapping from explicit requirements to required computation capabilities.
- Three deterministic candidate architecture strategies: minimum-cost, audit-first and extensibility-first.
- Candidate ranking and dependency closure.
- A Blueprint IR with ordered modules, dependency edges, provenance paths, provider configuration state and materialization contract.
- Structural verification of dependency closure and component coverage.
- SHA-256-linked construction frames.
- Append-only rollback branch operation that references a previous frame without changing historical frames.
- CLI and regression tests.

## Exact implementation boundary

The prototype generates a Blueprint artifact and checks its declared capability coverage. It does **not** synthesize or train neural weights, instantiate a trained neural network, create live model endpoints, or prove task accuracy. If the task requires actual neural runtime materialization without a verified backend, the Blueprint is retained but marked incomplete with the precise missing capability.

The 5,000 model slots remain architectural slots. The ~1,000 Perspective Nodes remain a target layer unless individually defined and loaded. The 28-mode reasoning taxonomy is mentioned in a project brief, but a validated list of 28 named mode definitions was not found in the checked architecture files; no synthetic list is generated.

## Acceptance test

The first example asks for a logic-native model-building AI. Its Blueprint must include LNL compilation, symbolic inference, contradiction detection, source provenance, goal verification, NTM critique and reversible construction. It must report neural runtime materialization as blocked when no verified backend is available.

A document/version-drift requirement must select a different module set: version comparison, structural/semantic diff, drift classification and verification.

The next scientific/engineering step is to compare requirement-derived candidates against a fixed baseline using the same task set and score correctness, coverage, cost, latency, failure and recoverability.
