# 07 — Gates and Metrics

**Status: PROPOSED — gate implementation and results NOT_YET_VERIFIED**

## Gate register

| Gate | Required evidence | Promotion rule |
|---|---|---|
| G1 — Contract | Frozen manifest schema, export allowlist, versioned contract | Block if incomplete or mutable without version change |
| G2 — Staging deployment | Compose/Kubernetes deployment evidence and inspected render | Block if startup or render fails |
| G3 — Verifier QA | Ground-truth version, reproducible metrics, FP/FN review | Block if test set or results are missing |
| G4 — Agent boundaries | Lane-evaluation report, access tests, kill-switch test | Block on any unauthorized action or unresolved safety failure |
| G5 — Provenance/integrity | SHA256SUMS, provenance log, manifest validation | Block on mismatch or missing source trace |
| G6 — Security | SBOM, dependency scan, secret scan, security review | Block on secrets or unreviewed critical findings |
| G7 — Release targets | Canary/airgap smoke evidence as applicable | Block if target evidence is missing |
| G8 — Rollback | Timestamped redeployment and health evidence for previous bundle | Block unless rollback succeeds within the declared cycle |

The detailed gate criteria must be frozen in CI before any gate can be reported as passed.

## Required measurements

- Precision, recall, false-positive and false-negative counts.
- Latency and reviewer time.
- Dev and production-build render inspection.
- Rollback duration and outcome.
- Mean time to detect drift.
- Count of unresolved pairs.
- Agent lane violations and unauthorized evidence writes.
- Bundle size and secrets detected.

## Status discipline

A configured pipeline is not a passed gate. An HTTP 200 is not proof of correct rendering. A generated signature is not proof of a valid release unless verification succeeds. `TESTED` requires reproducible test evidence; `VERIFIED` requires evidence tied to the specific artifact and commit.
