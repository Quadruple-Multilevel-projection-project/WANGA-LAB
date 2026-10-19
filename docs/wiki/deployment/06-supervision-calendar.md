# 06 — Supervision Calendar

**Status: PROPOSED PLAN; no schedule or gate result is recorded as completed.**

## Daily rhythm

| Time | Activity | Owner | Output |
|---|---|---|---|
| 09:00 | 15-minute standup | DSA | Blockers and lane status |
| 13:00 | Risk-log update | DSA + S5 | Updated risk register |
| 17:00 | Evidence commit | S4 | `provenance.jsonl` delta |
| Thursday 16:00 | Gate review | DSA | Recorded gate verdict |

## 30-day sequence

| Day(s) | Focus | Gate |
|---|---|---|
| 1 | Charter, access, branch, inventory | — |
| 2 | Export contract and four schemas | — |
| 3 | CI gates G1–G4 | — |
| 4 | Compose bring-up and dev smoke | — |
| 5 | Gate 1 review: contract frozen | G1 |
| 6–7 | Kubernetes manifests and NetworkPolicy | — |
| 8 | Signing and SBOM | G5–G6 |
| 9 | Provenance and SHA256SUMS | G5 |
| 10 | Gate 2 review: staging deployability | G2 |
| 11–12 | Verification engine and ground truth | — |
| 13 | Gate 14 rule pack v1 | — |
| 14 | Precision/recall run | — |
| 15 | Gate 3 review: verifier tested | G3 |
| 16–17 | L0–L1 agents and routing | — |
| 18 | L2 participant lanes | — |
| 19 | Agent evaluation set | — |
| 20 | Gate 4 review: bounded orchestration | G4 |
| 21–22 | L3–L4 agents and endpoint probes | — |
| 23 | Play-configuration compiler | — |
| 24 | Regenerate visual artifacts from data | — |
| 25 | Production canary rehearsal | G7 |
| 26 | Rollback drill | G8 |
| 27 | Airgap installation proof | G7 |
| 28 | Security report and limitations | G6 |
| 29 | Sign and publish bundle v1.0.0 | All required gates |
| 30 | Release review and handover | All |

## Metrics

Track gate pass rate, dev/production smoke results, rollback time, drift-detection time, unresolved-pair count, lane violations, bundle size, and secrets found (target: zero). Metrics must be populated from run evidence, not estimates.
