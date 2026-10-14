# Limbo Cartography Core

**Deployment status:** INITIAL PACKAGE · VERIFY THROUGH CI  
**Epistemic status:** SPECIFIED / IMPLEMENTATION CANDIDATE  
**Scope:** Record source-backed structural failure points, run explicit structural checks, and preserve logic-bundle candidates with provenance.

## Operating contract

Limbo Cartography Core is a workspace for mapping structural collapse as a project-defined phenomenon, preserving the source record, and tracking candidate expanded structures. It does not infer that a system is in terminal collapse merely because a record exists. It does not promote a candidate Keystone to a verified axiom through a placeholder test.

The package keeps source material, observations, interpretations, hypotheses, implementations, tests and verification outcomes separate. Missing inputs produce explicit empty/no-input states rather than fabricated coordinates.

## Execution

From this directory, using Python 3.12 or later:

```bash
python -m pip install pytest jsonschema
python engine/deterministic_executor.py
python engine/drift_validator.py
python -m pytest -q tests
python engine/seismic_detector.py
python engine/axiomatic_stress_tester.py
python engine/logic_bundle_builder.py
python engine/drift_validator.py
```

The daily workflow for this package is activated at the parent repository's `.github/workflows/daily-limbo-cartography-agent.yml`, because GitHub Actions only discovers workflow files under the repository-root `.github/workflows/` directory. The copy under this package documents the portable standalone layout.

## Input boundaries

- Add source-grounded candidate records only under `cartography/inbox/limbo_points/`.
- Add candidate Keystone test cases only under `cartography/inbox/keystone_cases/`.
- Add candidate logic bundles only under `cartography/inbox/logic_bundles/`.
- Never use the generated output directories as input. This prevents output-to-input feedback loops.
- Raw private conversation exports must not be placed in this public repository.
- A passing schema or unit test is not proof of source truth or semantic validity.

## Status vocabulary

- `OBSERVED`: a sourced event was recorded.
- `STRUCTURALLY_TESTED`: declared structural checks ran and their result was captured.
- `VERIFIED`: accepted only with explicit verification procedure and evidence refs.
- `DRAFT_UNVERIFIED`: a bundle was preserved without a verification claim.
- `NO_INPUTS`: no candidate records were available to inspect.
- `FAILED`: a declared validation failed.

The initial reality matrix is empty. No real-world collapse event, Keystone, or clean logic bundle is asserted by the scaffold itself.
