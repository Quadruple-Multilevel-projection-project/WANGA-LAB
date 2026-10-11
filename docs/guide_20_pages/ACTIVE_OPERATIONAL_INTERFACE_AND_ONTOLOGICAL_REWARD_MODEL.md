# Active Operational Interface & Ontological Reward Model

**Status: SPECIFIED / PLANNED — not a production implementation.**

## 1. Objective
Build an active environment where engineers submit, test, review, version and use logic packages; inspect contribution evidence; and, only after the reward mechanism is approved and implemented, view reward eligibility. Repository merge, package verification, marketplace listing and token reward are separate transitions.

## 2. Workbench modules

### Logic & Filter Workbench
1. **Submission portal:** stable package ID/version, provenance, license, task domain, inputs/outputs, constraints, dependencies, test vectors and limitations.
2. **Automated preflight:** schema and metadata validation, license declarations, lint/type/security checks and deterministic tests.
3. **Review queue:** reason-coded failures; human review for quality, protected IP, security and reward eligibility.
4. **Evidence bundle:** commit SHA, package hash, test run/results, reviewer decision, timestamp and status transition.
5. **Version view:** compatibility, defects, dependencies, deprecation and rollback.

The first version should use GitHub pull requests and CI as the submission portal before building a dedicated web app.

### Drift & Defense Dashboard
Display baseline and observation window, drift category, evidence references, ALLOW/DENY/DEFER/ESCALATE verdict, model/provider/runtime version, latency, false positives/negatives, limitations and incident timeline. A dashboard alone does not block actions; enforcement must occur in a tested service/API.

### Logic Marketplace
Publish task, version, compatibility, scope, evidence status, license, limitations, publisher, support status and price/usage model. Clearly distinguish demo, beta and production-approved packages. Do not invent customers, transactions or demand indicators.

## 3. Proposed contribution state machine
DRAFT → SUBMITTED → SCHEMA_VALIDATED → LICENSE_REVIEWED → TESTED → INDEPENDENTLY_REVIEWED → ACCEPTED/MERGED → REWARD_ELIGIBLE → REWARDED.

Alternate states: REJECTED, NEEDS_CHANGES, BLOCKED, REVOKED_OR_SUPERSEDED. Preserve history on rejection/revocation. Passing CI alone must not promote a package to VERIFIED; the evidence scope must say what was and was not tested.

## 4. Proof-of-Logic reward concept
Reward accepted, attributable and useful logic—not hours, commit count or unreviewed claims.

Required controls:
- Rules and maximum bounty published before work begins.
- Contributor attribution with privacy protection.
- Provenance, license and protected-IP review.
- Duplicate/dependency checks and deterministic tests.
- Independent review when correctness is not reducible to tests.
- Transparent score rubric: novelty, utility, correctness, reuse, maintainability, coverage, security and documented limits.
- Separate accounting for contribution reward and usage revenue.
- Appeal, conflict-of-interest, correction/reversal and audit trail.
- No self-approval and no reward for failed, unlicensed, malicious or unmerged submissions.

A test pass proves only declared cases, not universal logical truth.

## 5. Token decisions still open
The repository currently has no verified token-launch mechanism. Before implementation, the project owner must decide:
1. Is the unit an internal score, non-transferable credit, redeemable service credit or transferable digital asset?
2. What rights/obligations attach to earning or holding it?
3. Which service or use requires it, and why?
4. How are supply, distribution, treasury and funding controlled?
5. Who may change reward rules, and how are changes versioned?
6. How are disputes, lost keys, disputed authorship and post-merge defects handled?
7. Which legal, tax, consumer-protection and regulatory reviews apply?

Until the decisions and independent reviews are complete, issuance, demand and appreciation are a proposed design—not a live or guaranteed outcome.

## 6. Conceptual data contracts (not existing schemas)
**LogicPackageRecord:** package_id, version, source_commit, content_hash, purpose, domain, inputs, outputs, constraints, dependencies, compatibility, license, IP classification, test vectors/results, limitations, implementation/verification status, maintainer.

**ContributionRecord:** contribution_id, contributor reference, package/version, PR, commit, reviewers, decision, provenance, test evidence, license result, contribution score, reward-rule version, eligibility, ledger event, appeal status and timestamp.

**ExecutionDecision:** request ID, candidate action, policy version, context reference, verdict, reason codes, evidence, runtime version and audit record.

## 7. Milestones
- **M0:** choose canonical paths, IP/license policy and package contract.
- **M1:** one sample package, schema validator and reproducible runner.
- **M2:** PR/CI/review loop with provenance.
- **M3:** public contribution/status registry.
- **M4:** off-chain reward simulation with synthetic contributors, duplicates, failures, appeals and issuance caps.
- **M5:** one catalogued package configured and run in a sandbox.
- **M6:** legal/security gates before any transferable asset or public token issuance.

## 8. Connected issues
- [#88 — Canonical Logic Package schema](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)
- [#89 — Logic & Filter Workbench](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)
- [#90 — Proof-of-Logic and reward ledger](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/90)
- [#91 — Logic Marketplace and Execution Shields](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/91)
- [#92 — Development and contribution tracking](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)

## 9. Threat model
Assess Sybil accounts, collusion, spam, duplicate submissions, manipulated tests, malicious packages, dependency compromise, unsafe execution, IP/secret leakage, reward-key compromise, supply inflation, reviewer capture, disputed authorship, license conflicts, customer-data exposure, outages and stale registries. Fail closed on missing license, provenance, authorization or mandatory tests; use DEFER when judgment or more evidence is required.
