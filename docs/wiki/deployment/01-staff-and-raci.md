# 01 — Staff and RACI

## Core staffing plan

| ID | Role | FTE | Hard deliverable |
|---|---|---:|---|
| S1 | Platform Engineer | 1.0 | Compose, Kubernetes, and airgap deployment tree runs on three targets |
| S2 | CI/CD Release Engineer | 1.0 | CI, export, deploy pipelines; signed bundles |
| S3 | Verification/QA Engineer | 1.0 | Test report with precision/recall on a ground-truth set |
| S4 | Data & Provenance Engineer | 1.0 | Four schemas and append-only evidence log |
| S5 | Security Engineer | 0.4 | Threat model, SBOM, secret scan, signing review |
| S6 | Visualization Engineer | 0.5 | Four generated artifacts under `artifacts/visuals/` |
| S7 | Ontology Editor / Technical Writer | 0.5 | Versioned Introduction + Gate 14 rule packs with citations |
| S8 | AgentOps Engineer | 1.0 | L0–L4 registry, routing policy, evaluation scores |

FTE values are proposed staffing targets, not evidence that these roles are staffed.

## RACI

R = Responsible; A = Accountable; C = Consulted; — = no assigned role in this condensed matrix.

| Deliverable | DSA | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---|---|---|---|---|---|---|---|---|---|
| Export bundle contract | A | C | R | C | R | C | — | — | — |
| Compose/K8s/airgap | A | R | C | C | — | C | — | — | — |
| CI/CD + signing | A | C | R | C | C | R | — | — | — |
| Verification schema + harness | A | — | — | R | R | C | — | C | — |
| Provenance/evidence | A | — | C | C | R | C | — | — | — |
| Visual artifacts | A | — | — | C | — | — | R | — | — |
| Rule packs (Gate 14) | A | — | — | C | — | — | — | R | C |
| Agent orchestration | A | C | C | C | C | C | — | C | R |

## Role instructions

- **S1:** create `deploy/compose/`, `deploy/k8s/`, and `deploy/airgap/`; make startup idempotent; document network exposure and prove offline installation.
- **S2:** implement G1–G8; sign bundles; attach provenance and checksums; rehearse canary promotion and rollback.
- **S3:** build a source-grounded test set; measure precision, recall, false positives/negatives, latency, and reviewer time; inspect dev and production-build screenshots.
- **S4:** author verification, signal, participant, and export-manifest schemas; preserve append-only provenance.
- **S5:** threat-model identities, data flows, keys, and audit storage; run dependency and secret scans; document limitations.
- **S6:** generate visual artifacts from data, not hand-edited coordinates; keep renderers read-only.
- **S7:** extract rules only from inspected canonical source sentences; version rules and retain citations.
- **S8:** register agent lanes and evaluate whether each agent remains inside its assigned lane.

These are assigned responsibilities in the proposed plan; completion remains unverified until evidence is recorded.
