# Daily Integration Map — Logic Research, Logic Boxes, and Public Site

**Date:** 2026-10-13  
**Status:** DOCUMENTED / LINKS MAPPED / SITE NAVIGATION NOT YET VERIFIED  
**Purpose:** One entry point connecting the logic architecture discussed on 2026-10-12, the technical research archive, the first three task-specific logic products, and their public Wix explanations.

## 1. The integrated research-to-product path

Source corpus and primary texts  
→ source-linked extraction  
→ sentence roles, entities, relations, and provenance  
→ logic identification and reconstruction  
→ logic structures, preconditions, boundaries, and failure modes  
→ specification of task-specific Logic Boxes  
→ composition gate: compatibility + authorization + scope + evidence + deterministic checks  
→ test fixtures and reproducible results  
→ product/demo status with explicit evidence labels  
→ public explanation in the Wix catalog  
↔ source links and revision records in WANGA-LAB

This is a proposed workflow and information architecture. A hyperlink between two documents does not prove a runtime dependency or working software integration.

## 2. Architecture sources from the research archive

- [Five-forward / five-return architecture review](./FIVE_FORWARD_FIVE_RETURN_LOGIC_ARCHITECTURE_REVIEW_V1.md) — canonical ten-stage functional loop; status ARCHITECTURE PROPOSAL / NOT_YET_VERIFIED.
- [Twelve-problem architecture evidence map](./TWELVE_PROBLEM_ARCHITECTURE_EVIDENCE_MAP_V1.md) — problem-by-problem claims, proposed responses, evidence, and tests.
- [79-page source audit](../research/SOURCE_AUDIT_79_PAGE_LOGIC_EXTRACTION_2026-10-12.md) — scope and limits of what the source material establishes.
- [257-page letter-logic corpus plan](../research/LETTER_LOGIC_CORPUS_257_PAGE_PLAN_V1.md) — planned corpus structure; not a claim that the entire corpus is complete.
- [Logic Mine research tracks](../research/LOGIC_MINE_RESEARCH_TRACKS.md) — source mining, extraction, formalization, configuration, and future logic research.
- [Logic as Product — markets bridge](./LOGIC_AS_PRODUCT_MARKETS_BRIDGE_V1.md) — product and market hypotheses, explicitly subject to validation.
- [Logic before implementation — public-site bridge](../research/LOGIC_BEFORE_IMPLEMENTATION_SITE_BRIDGE.md) — links the technical archive and public research sites.

### Required conceptual separations

1. Ten functional stages = five forward-processing stages plus five return/integration stages.
2. Four logical-mathematical weight layers are a separate concept; original names/formulas must come from source evidence.
3. Four sentence roles (subject, predicate, internal participant, relation/connective) are an extraction schema, not weight layers.
4. Source facts, extracted structure, interpretation, and engineering hypothesis must remain separately labelled.
5. “Atomic”, “subatomic”, and “metaphysical” describe conceptual depth unless a physical mechanism is independently specified.
6. Exact-text reconstruction and structural reconstruction are different verification tasks.

## 3. First three Logic Boxes

### BOX-01 — Evidence Gatekeeper / שומר סף לראיות
**Purpose:** Separate claim, source, contradiction, missing evidence, and verification status.  
**Expected output:** claim ledger with source/provenance, conflict state, uncertainty, and VERIFIED, NOT_YET_VERIFIED, or INSUFFICIENT_EVIDENCE as appropriate.  
**Current status:** SPECIFIED through published explanation; do not represent as tested production software without a reproducible implementation and test evidence.  
**Public page:** https://beywolf5.wixsite.com/my-site-17/post/logic-box-01-evidence-gatekeeper

### BOX-02 — Task Decomposer & Scope Binder / פירוק משימה ותחימת היקף
**Purpose:** Bind an instruction to a target, allowed scope, acceptance criteria, prohibited changes, and stop conditions.  
**Expected output:** explicit task contract and a scope-violation result when an action exceeds it.  
**Current status:** SPECIFIED through published explanation; software-level execution remains unverified unless separately evidenced.  
**Public page:** https://beywolf5.wixsite.com/my-site-17/post/logic-box-02-task-scope-binder

### BOX-03 — Deterministic Action Filter / מסנן פעולות דטרמיניסטי
**Purpose:** Gate proposed actions on authorization, scope, risk, reversibility, and required verification.  
**Expected output:** allow / deny / require-review decision with a reason and evidence trail.  
**Current status:** SPECIFIED through published explanation; do not imply it controls live site changes unless the control path and tests demonstrate that fact.  
**Public page:** https://beywolf5.wixsite.com/my-site-17/post/logic-box-03-deterministic-action-filter

### Composition rule

The three boxes are complementary specifications, not automatically a working pipeline. A composed execution path must test at least:
- evidence missing or contradictory;
- task target ambiguous or out of scope;
- action unauthorized or irreversible;
- all gates pass;
- downstream failure after an upstream pass;
- preservation of the decision trace and source provenance.

No earlier failure should be silently overwritten. A failed gate should return a typed state and permit only a bounded, authorized recovery or a clear stop.

## 4. Public catalog and related Wix articles

Main site: https://beywolf5.wixsite.com/my-site-17  
Blog/catalog: https://beywolf5.wixsite.com/my-site-17/blog

- [Logic in Boxes — main catalog](https://beywolf5.wixsite.com/my-site-17/post/logic-in-boxes-catalog-he)
- [BOX-01 — Evidence Gatekeeper](https://beywolf5.wixsite.com/my-site-17/post/logic-box-01-evidence-gatekeeper)
- [BOX-02 — Task Scope Binder](https://beywolf5.wixsite.com/my-site-17/post/logic-box-02-task-scope-binder)
- [BOX-03 — Deterministic Action Filter](https://beywolf5.wixsite.com/my-site-17/post/logic-box-03-deterministic-action-filter)
- [How to buy logic boxes](https://beywolf5.wixsite.com/my-site-17/post/how-to-buy-logic-boxes)
- [Request a custom logic box](https://beywolf5.wixsite.com/my-site-17/post/custom-logic-box-request)
- [Methodology](https://beywolf5.wixsite.com/my-site-17/post/logic-box-methodology)
- [Classical logic to logic engineering](https://beywolf5.wixsite.com/my-site-17/post/classical-logic-to-logic-engineering)
- [FAQ](https://beywolf5.wixsite.com/my-site-17/post/logic-boxes-faq-he)
- [About the lab](https://beywolf5.wixsite.com/my-site-17/post/about-logic-in-boxes)
- [Catalog map](https://beywolf5.wixsite.com/my-site-17/post/logic-boxes-catalog-map)

These links record intended public entry points. They do not by themselves confirm that every article is published, that the site navigation links to each one, or that the latest site-builder job edited the existing site.

## 5. Research maps that connect the wider Wix ecosystem

Use the existing [Wix cross-site logic-map audit](../research/WIX_CROSS_SITE_LOGIC_MAP_AUDIT_2026-10-12.md) as the source of truth for the six candidate maps:
- MAP-01 — controlled website change;
- MAP-02 — claim-to-source calculation;
- MAP-03 — criterion drift rather than model-output change;
- MAP-04 — continuous logic mine and feedback;
- MAP-05 — compatibility before composition;
- MAP-06 — forensic findings update the map.

The audit records a sitemap inventory of 174 unique non-category URLs across 16 public site slugs from 28 sitemap files, not a complete audit of every private, draft, unindexed, or sitemap-less page.

## 6. Status and evidence contract

Use these labels consistently:
- SPECIFIED — described as a logical or technical contract.
- PROTOTYPED — an implementation exists, but production behavior is not established.
- TESTED — named tests were run; retain the test evidence and result.
- VERIFIED — independent/reproducible evidence supports the exact claim and declared scope.
- PLANNED — future work.
- NOT_YET_VERIFIED — insufficient evidence to make a verification claim.

Do not promote a specification to a working product based on a published article, diagram, repository file, or hyperlink alone.

## 7. Integration work still required

1. Confirm the Wix creation/editing job outcome; the previously returned response only established that a job was started.
2. Confirm which site was changed and whether it is the existing My Site 17 or a separate site.
3. Add and verify a stable public navigation path from the site homepage to the catalog, each of the three boxes, methodology, FAQ, and custom request.
4. Add a reciprocal link from the public catalog/methodology to the technical archive and this integration map.
5. Run link checks against all 11 article URLs; record HTTP/page status rather than assuming availability.
6. Build executable tests for the three boxes individually and in composition; store fixtures, outputs, and test results in the repository.
7. Keep the wider 5+5 architecture, letter-logic corpus, logic mining, and the commercial catalog linked as separate layers; do not collapse research hypotheses into product claims.

## 8. Acceptance criteria for “connected”

The work is complete only when:
- every public catalog entry links to its own detail page;
- each product page links back to the catalog and states its evidence/status boundary;
- the technical archive links to the public explanation and vice versa;
- the navigation and article links are checked on the live site;
- a composed logic demo produces reproducible outputs for pass, deny, contradiction, insufficient-evidence, and scope-violation fixtures;
- implementation, tests, and publication are reported with distinct statuses.
