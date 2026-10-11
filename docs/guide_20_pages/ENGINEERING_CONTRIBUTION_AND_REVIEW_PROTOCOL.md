# Engineering Contribution, Review & Verification Protocol

**Status: SPECIFIED in documentation; complete operational workflow remains PLANNED.**

## 1. Before a pull request
- Read the repository README and relevant architecture/research docs.
- Choose one bounded issue and define expected behavior.
- Search existing paths to avoid duplicate packages.
- Record sources, provenance and license restrictions.
- Do not submit secrets, customer data or protected Rational Logic implementation.
- Separate evidence, inference, hypotheses and implementation status.

## 2. Minimum Logic Package submission
State the task/domain, stable ID/version, input/output contract, preconditions, constraints, forbidden operations, unknown/failure handling, provenance, dependencies, license/IP classification, tests, expected results, limitations and reproducible command. Canonical schema is an open task: [Issue #88](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88).

## 3. Review gates
1. Scope and intended behavior.
2. Provenance and derivation.
3. License and IP.
4. Schema validity.
5. Reproducible tests.
6. Adversarial cases and unknown-state handling.
7. Security, side effects, privilege escalation and data leakage.
8. Compatibility/conflicts with existing rules.
9. Maintenance, versioning, owner and deprecation.
10. Accuracy of public and investor-facing claims.

A green test suite does not replace license, security or quality review.

## 4. Status rules
- PLANNED: proposed work, no implementation evidence.
- SPECIFIED: contract documented.
- PROTOTYPED: narrow demo exists.
- BUILT: artifact exists in the stated path.
- TESTED: named checks ran and result is recorded.
- VERIFIED: defined evidence gates passed for explicit scope.
- HYPOTHETICAL: future scenario or concept.
- BLOCKED: decision, dependency or access blocks progress.

Never silently upgrade a status after a commit or omit a failed result.

## 5. Contribution provenance
The planned registry should connect:
contribution → PR → commit → package version → test run → reviewer decision → verification scope → future reward eligibility → ledger event.

Reward eligibility must not be inferred from commit count or lines of code. If rewards are approved later, the rubric must be published before work begins and include appeals.

## 6. Useful contributions now
- Add cited research to the Logic Mine tracks.
- Add reproducible fixtures and tests to evidence/forensics components.
- Review the 20 pages for factual accuracy and link correctness.
- Specify the canonical package schema and conformance suite.
- Build an off-chain reward simulation without issuing an asset.
- Propose bounded specs with explicit acceptance criteria.

## 7. Open work
- [#88 — Package schema and submission contract](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/88)
- [#89 — Workbench, CLI/SDK and review loop](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/89)
- [#90 — Proof-of-Logic and reward ledger](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/90)
- [#91 — Marketplace and Execution Shield boundary](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/91)
- [#92 — Public progress and contribution tracking](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/issues/92)
