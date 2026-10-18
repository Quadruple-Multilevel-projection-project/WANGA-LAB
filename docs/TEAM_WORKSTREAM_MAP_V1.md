# WANGA Team Workstream Map v1

Status: SPECIFIED

This file defines the proposed workstream/team boundaries for the WANGA organization. It does not assert that GitHub Teams or repository permissions have been created.

## Workstreams

| Team | Purpose | Primary repositories | Suggested access |
|---|---|---|---|
| LOGIC-EXTRACTION | Native logic extraction before formalization | WANGA-LAB, -logicl-neural-order, MNM | Maintain |
| DICTIONARY-TAGGING | Source Node, Reference Link, Operational Aspect, atomic tagging | WANGA-LAB, AI231.meta.io, -from-Corsican- | Maintain |
| EVIDENCE-PROVENANCE | Evidence, provenance, lineage, canonical records | WANGA-LAB, ARK-KERNEL-OVERSIGHT | Maintain |
| WEIGHTS-UNCERTAINTY | Deterministic weights/uncertainty research and evaluation | WANGA-LAB, AI231.meta.io, MNM | Maintain |
| DRIFT-FORENSICS | Baseline, observation, drift detection, reconstruction, attribution, verification | WANGA-LAB, ARK-KERNEL-OVERSIGHT | Maintain |
| VERIFICATION | Tests, reproducibility, verification gates and evidence | WANGA-LAB, ARK-KERNEL-OVERSIGHT, ai-agent-terraform | Maintain |
| AGENT-EVALUATION | Agent/model evaluation and runtime observation | WANGA-LAB, ai-agent-terraform, skills | Maintain |

## Security boundary

The repository named `GOOGLE_API_KEY` is not assigned to an operational team. It requires security review and must not be treated as a normal development repository.

## Existing WANGA-LAB evidence

- `GLOBAL_ARCHITECTURE_REGISTRY.md` is the repository-level architecture registry.
- `ai-drift-forensics/` is an existing drift/verification workstream.
- `docs/BRANCH_ARCHITECTURE_REGISTRY.md` records existing control-plane and drift branches.
- Multiple open PRs exist; new work must avoid overwriting active contributor branches.

## Access rule

Repository permissions must be granted through GitHub Teams after team membership is explicitly verified. This document is a mapping specification, not a permission change.

## Verification boundary

Team creation, membership, and repository permission assignment remain UNVERIFIED until observed directly through GitHub organization/team state.
