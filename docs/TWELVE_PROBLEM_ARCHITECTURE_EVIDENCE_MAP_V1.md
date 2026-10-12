# 12-Problem Map — Bidirectional Logic Architecture (5+5)

**Status:** SPECIFIED / PROPOSED. This is a design-to-evidence map, not proof that the architecture solves all twelve problems. No benchmark result is accepted without a reproducible test set, protocol, logs, and baseline.

## Purpose
Connect the proposed ten-stage bidirectional architecture to the investor narrative and identify what each claimed response would need to demonstrate. “Forward 1–5 / return 6–10” describes functional stages, not ten already-built neural networks. The four mathematical-weight layers attached to letter interpretations are a separate research dimension and must not be conflated with the 5+5 flow.

## The twelve problem areas

| # | Problem to investigate | Proposed architectural response | Evidence needed before claiming a solution | Current status |
|---|---|---|---|---|
| 1 | Statistical generation vs explicit logical constraints | Preserve source structure and run explicit rules/constraints alongside learned components | Fixed benchmark comparing valid reasoning, unsupported outputs, abstention, and error rates against baselines | PROPOSED |
| 2 | Traceability from output back to source | Keep source IDs, extraction records, transformations, rule versions, and output links through the return path | Demonstrate trace reconstruction on held-out examples; distinguish exact text reconstruction from structural reconstruction | PARTLY DOCUMENTED extraction method; round trip NOT VERIFIED |
| 3 | Failure-state detection and recovery | Represent invalid states, constraint failures, recovery rules, and safe stopping explicitly | Inject known failures; measure detection, recovery, false alarms, and safe abstention | SPECIFIED conceptually; runtime NOT VERIFIED |
| 4 | One undifferentiated notion of weight | Separate the four proposed mathematical-logical weight layers linked to each letter interpretation from ordinary model parameters and confidence scores | Recover original definitions/formulas from source archive; define types, units, composition, and sensitivity tests | NOT YET SPECIFIED from primary evidence |
| 5 | Hard constraints mixed with soft scores | Use hard gates for non-negotiable rules and soft weights only for ranking within valid paths | Contradiction tests proving a high soft score cannot override a failed hard constraint | SPECIFIED; implementation NOT VERIFIED |
| 6 | Loss of nested sentence structure | Preserve clauses, relations, participants, order, negation, conditions, and source spans | Annotation agreement and structure-recovery evaluation on a held-out corpus | First-stage extraction documented in a 79-page working artifact; broader performance NOT VERIFIED |
| 7 | Letters treated as passive characters | Store multiple source-grounded interpretations, forms, positions, combinations, and candidate computational roles as separate records | Source citations, alternative readings, counterexamples, and ablation tests per letter/combination | RESEARCH HYPOTHESIS |
| 8 | Disconnection between macro, micro, and pico scales | Define explicit scale mappings and aggregation rules | Formal scale definitions, numerical stability tests, and cross-scale consistency evaluation | NOT YET SPECIFIED sufficiently |
| 9 | Hidden semantic/logical contradictions | Check relations and constraints across interpretations and combinations | Contradiction corpus, precision/recall, adjudicated errors, and comparison with baselines | PROPOSED |
| 10 | No unified machine-readable representation | Produce a versioned logical-mathematical record with provenance, constraints, weights, uncertainty, and reconstruction metadata | Schema validation, deterministic replay, and separate exact-text/structural round-trip tests | PROPOSED |
| 11 | Unsuitable evidence for high-stakes environments | Add audit trails, failure reporting, provenance, bounded operation, and review gates | Domain-specific risk assessment, external review, operational trials, and documented failure handling | No “zero-crash” claim; NOT VERIFIED |
| 12 | Language/logical structure not packaged as reusable engineering assets | Package bounded, task-specific logic modules with inputs, outputs, constraints, provenance, versions, tests, and integration guidance | User interviews, paid pilots, utility measurements, maintenance costs, and comparison to alternatives | Commercial hypothesis; NOT VALIDATED |

## Important corrections to the earlier twelve-point summary
1. The architecture does **not** currently prove that it deterministically eliminates hallucinations; it proposes explicit constraints that can be tested.
2. A bidirectional design does **not** automatically guarantee lossless reconstruction. Exact text and structural round-tripping require separate tests.
3. “World of Nekudim,” “breaking of vessels,” “Tikun,” “Aleph,” and “Lamed” are source concepts and proposed engineering analogies. The analogy is not itself evidence of an implemented crash/recovery mechanism.
4. “Sub-atomic,” “quantum-logical,” and “metaphysical” describe the researcher's conceptual depth unless a physical mechanism is independently specified; they must not be marketed as proven physics.
5. The values LFA 94.8%, CSR 99.2%, and EDI 0.02 appearing in the supplied draft are **not accepted as empirical results** without reproducible data, metric definitions, protocol, baseline, and run logs.
6. No claim that this is the only system capable of these functions. Neurosymbolic AI and computational text-analysis research already exist; novelty must be shown by direct comparison.
7. Do not invent the four weight-layer names or formulas. Recover them from the user's research sources and mark unresolved elements as NOT_YET_SPECIFIED.
8. Keep the three source branches separate: (a) Rambam / *Millot ha-Higayon* and systematic text extraction; (b) philosophical logic of place, identity, relations, boundaries, part/whole, and change; (c) letter logic and its source-grounded interpretations. Arizal texts form a source corpus, not a substitute name for the whole system.
9. Keep the investor story connected but bounded: the research corpus is an explanatory/evidence asset; the potential product is task-specific logic packages, paid configuration/integration, and custom logic. Demand, pricing, and competitive advantage remain unverified until customer evidence exists.

## Investor linkage
The investor-facing explanation should communicate:
- **Problem:** in some tasks, fluent output is insufficient without constraints, provenance, and replayable evidence.
- **Approach:** source-grounded extraction → alternative interpretations → explicit constraints and proposed weight layers → bounded module → tests → traceable output.
- **Potential asset:** reusable task-specific logic packages, not the page count itself.
- **Milestones:** source audit; recover the original four weight definitions; build one bounded demonstrator; evaluate exact and structural round trips separately; compare to a baseline; validate demand through customer discovery and paid pilots.
- **Risk disclosure:** the full 5+5 engine, four weight layers, 231-gate runtime, 3D/fractal coordinate system, broad performance gains, and commercial demand are not yet verified as a complete system.

## Canonical links
- Architecture review: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/FIVE_FORWARD_FIVE_RETURN_LOGIC_ARCHITECTURE_REVIEW_V1.md
- Investor explanation draft: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/INVESTOR_LOGIC_EXPLANATION_UPDATE_DRAFT_HE.md
- 257-page corpus plan: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/LETTER_LOGIC_CORPUS_257_PAGE_PLAN_V1.md
- Source audit of 79-page extraction artifact: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/SOURCE_AUDIT_79_PAGE_LOGIC_EXTRACTION_2026-10-12.md
- Publication staging by site/fractal: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/LOGIC_CORPUS_PUBLICATION_STAGING_2026-10-12.md

## Publication status
This document is a review artifact. It does not authorize publication of unverified performance claims. The Wix investor site still requires an explicit destination choice before publishing this update live.
