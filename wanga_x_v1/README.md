# WANGA-X Requirement-Driven Blueprint Engine V1

**Status: BUILT AS AN EXPERIMENTAL BLUEPRINT GENERATOR; actual neural-network materialization is not yet implemented.**

This package makes the first executable part of the WANGA-X architecture thesis:

`REQUEST → REQUIREMENT → REQUIRED NEURAL COMPUTATION → NTM CANDIDATE ARCHITECTURE SEARCH → BLUEPRINT / IR → MATERIALIZATION PLAN → VERIFICATION`

It combines the existing WANGA-X requirement-first architecture, Neural Thinking Machine, Rational Logic, Model Fabric inventory and verification contracts. It is not a general LLM, is not trained from scratch, and does not fabricate live endpoints or neural weights.

## Quick start

Requires Python 3.11+; standard library only.

```bash
python -m wanga_x_v1.cli demo
python -m wanga_x_v1.cli demo --out /tmp/wanga-x-blueprint.json
python -m wanga_x_v1.cli build wanga_x_v1/examples/logic_model_builder_requirement.json --out /tmp/wanga-x-blueprint.json
python -m wanga_x_v1.cli verify /tmp/wanga-x-blueprint.json
python -m wanga_x_v1.cli rollback /tmp/wanga-x-blueprint.json --frame F2 --note "Rebuild from the derived-computation frame" --out /tmp/wanga-x-rollback.json
python -m unittest discover -s wanga_x_v1/tests -v
```

## What the prototype does

1. Normalizes explicit task requirements.
2. Derives required computation capabilities from task profiles plus the declared requirements.
3. Generates and scores three architecture candidates: minimum-cost, audit-first and extensibility-first.
4. Selects a candidate, resolves dependencies and reports unsatisfied capabilities.
5. Emits a Blueprint with module nodes, dependency edges, provenance paths, provider state and materialization contract.
6. Records SHA-256-linked construction frames for intake, normalized requirement, required computation, candidate ranking, Blueprint and structural verification.
7. Supports append-only rollback branches referring to earlier frames without rewriting history.
8. Reads the existing work-memory/model-fabric counts so a target of 5,000 slots is not confused with live model endpoints.

## Blueprint versus neural computer

The current engine generates and verifies a **Blueprint artifact**. It does not train or instantiate neural weights, create provider endpoints or verify a trained model's accuracy. If a requirement demands actual neural runtime materialization and no verified backend exists, the build is explicitly marked incomplete and names the missing capability.

A configured language-model endpoint is marked `CONFIGURED_NOT_PROBED`, not healthy or verified. A neural backend adapter is not enabled merely because an environment variable names it.

## Requirement-driven architecture

The catalogue includes requirement normalization, Rational Logic, source provenance, NTM candidate critique/ranking, the LNL compiler, the symbolic kernel, drift analysis, reversible build management, Model Fabric registry, Blueprint materializer, optional LLM proposer and a future neural runtime materializer. Only components needed by a task plus their dependencies are selected.

The logic-model-builder fixture selects the LNL compiler and symbolic inference. The document-drift profile instead selects version comparison, structural/semantic diff and drift forensics. A full neural-runtime request is intentionally blocked until a verified backend is available.

## Existing system inventory

The repository's `docs/WORK_MEMORY_STATE.json` currently records 5,000 allocated model slots, with 0 connected and 0 verified endpoints. It records a target Perspective Layer around 1,000 nodes. The 28-mode reasoning taxonomy is mentioned in an investor brief, but a validated enumeration of the 28 named modes was not found in the inspected architecture files; this engine does not invent such a list.

## References

- [WANGA-X research foundations](../docs/WANGA_X_RESEARCH_FOUNDATIONS.md)
- [WANGA-X reversible architecture](../docs/WANGA_X_REVERSIBLE_ARCHITECTURE.md)
- [NTM Orchestrator](../wanga-research-groups/neural-thinking-machine/NTM_ORCHESTRATOR_V1.md)
- [NTM Multi-Model Orchestration](../wanga-research-groups/neural-thinking-machine/ORCHESTRATION_MODEL_V1.md)
- [Model Agent Architecture](../docs/MODEL_AGENT_ARCHITECTURE_V1.md)
- [Model Family Registry](../docs/MODEL_FAMILY_REGISTRY.yml)
- [WANGA symbolic kernel](../logic_engine_v1/README.md)

The next empirical question is whether requirement-derived architecture selection improves quality, cost, reliability or recoverability against a fixed baseline on the same tasks. This engine makes that comparison testable; it does not assume the result.
