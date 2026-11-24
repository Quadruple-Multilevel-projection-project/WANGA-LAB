# 00 — Role Charter

## Role

**Title:** DEPLOYMENT_SYSTEMS_ARCHITECT (DSA)  
**Reports to:** System Owner / Principal

**Owns:** the path from committed source to a running, signed, reversible deployment, including supervised agent orchestration.

**Does not own:** product semantics, interpretation of Gate 14, or commercial claims.

## Mission

Convert the NLIL verifier, Metr GitHub Orchestrator, Willow/Plaza kernel, and visual artifacts into reproducible export bundles and supervised agent orchestration. Each capability must progress through PROPOSED → SPECIFIED → PROTOTYPED → TESTED → VERIFIED, with evidence at each transition.

## Authority

- Freeze and unfreeze exports.
- Block promotion at any gate.
- Reject bundles missing a manifest, hashes, SBOM, or provenance.
- Assign and revoke agent lanes L1–L4.

## Accountability

- `npm run build` and `npm run typecheck` pass.
- Development and production render are inspected; HTTP 200 alone is insufficient.
- Rollback is demonstrated within one release cycle.
- No secrets are included in an export bundle.
- No VERIFIED claim is made without recorded evidence.

## Interfaces

- **Upstream:** Principal (semantics and Gate 14 rulings), ontology editor (rule packs), security engineer (sign-off).
- **Downstream:** staging/production operators, pilot-customer security reviewer, AgentOps (agent health).

## Evidence discipline

The charter records target responsibilities and acceptance criteria. It does not assert that any deliverable is already implemented, tested, signed, deployed, or verified.
