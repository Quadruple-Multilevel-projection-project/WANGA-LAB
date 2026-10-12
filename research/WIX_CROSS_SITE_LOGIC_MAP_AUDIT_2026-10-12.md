# Wix Cross-Site Logic Map Audit

**Date:** 2026-10-12  
**Status:** Sitemap inventory created; selected content reviewed; six candidate maps documented.

## Scope and coverage
- Wix account inventory reports **53 sites**.
- This audit pulled **28 sitemap files** and found **174 unique non-category URLs across 16 public site slugs**.
- The inventory distinguishes sitemap-listed pages from pages that received semantic review. URL-topic labels do not prove that a page contains logic or establishes a dependency.
- These are public, sitemap-indexed URLs from the selected sites, not every private, draft, unindexed, or sitemap-less page in the account.

## Source-grounded evidence and composition
### MAP-01 — Controlled website change
Sources: [Task Decomposer & Scope Binder](https://beywolf5.wixsite.com/my-site-17/post/task-decomposer-scope-binder-he), [Evidence Gatekeeper](https://beywolf5.wixsite.com/my-site-17/post/logic-box-01-evidence-gatekeeper), [Deterministic Action Filter demo](https://beywolf5.wixsite.com/my-site-17/post/demo-deterministic-action-filter-publish-change).  
Path: requirement → scope contract → evidence gate → action gate → authorized publication → verification. Tests distinguish an allowed typo correction, an unapproved price change, and publication without permission. The live site mutation is not connected by this demonstration.

### MAP-02 — Claim-to-source calculation
Sources: [Evidence Gatekeeper synthetic demo](https://beywolf5.wixsite.com/my-site-17/post/demo-evidence-gatekeeper-bout-nails), [Evidence Gatekeeper logic box](https://beywolf5.wixsite.com/my-site-17/post/evidence-gatekeeper-logic-he).  
The fictional inputs use a price change from 180 NIS to 140 NIS: 40/180 ≈ 22.2%, not 30%. The site labels the business and inputs as fictional; this must not be reported as a real business finding.

### MAP-03 — Criterion drift rather than model-output change
Sources: [Verified Synthetic Drift Case](https://beywolf5.wixsite.com/forensic-logic-dri/post/what-a-verified-synthetic-drift-case-actually-proves), [AI Drift Forensics](https://beywolf5.wixsite.com/forensic-logic-dri/post/ai-drift-forensics-from-baseline-to-reproducible-finding).  
The synthetic score remains 0.75 while the threshold moves from 0.80 to 0.60; the decision flips. Verification remains limited to the synthetic fixture.

### MAP-04 — Continuous logic mine and feedback
Sources: [Continuous Logic Mine](https://beywolf5.wixsite.com/forensic-logic-dri/post/continuous-logic-mine-a-research-loop-not-a-static-archive), [Provenance in Logic Research](https://beywolf5.wixsite.com/forensic-logic-dri/post/from-source-to-structure-preserving-provenance-in-logic-research), [Reusable Logic Packages](https://beywolf5.wixsite.com/forensic-logic-dri/post/reusable-logic-packages-contracts-composition-and-verification).  
Path: source → extraction → reconstruction → architecture → configuration → verification → deployment → evidence → new extraction. The loop is a research model; end-to-end autonomous implementation is not thereby demonstrated.

### MAP-05 — Compatibility before composition
Sources: [Reusable Logic Packages](https://beywolf5.wixsite.com/forensic-logic-dri/post/reusable-logic-packages-contracts-composition-and-verification), [Logic Capability Layer](https://beywolf5.wixsite.com/forensic-logic-dri/post/beyond-agent-registries-the-proposed-logic-capability-layer), [Logic Boxes Catalog Map](https://beywolf5.wixsite.com/my-site-17/post/logic-boxes-catalog-map).  
Check interfaces, preconditions, permissions and failure behavior. The proposed combination needs composite tests; correctness of individual pieces is insufficient.

### MAP-06 — Forensic findings update the map
Sources: [AI Drift Forensics](https://beywolf5.wixsite.com/forensic-logic-dri/post/ai-drift-forensics-from-baseline-to-reproducible-finding), [Forensic Case Engine](https://beywolf5.wixsite.com/forensic-logic-dri/post/the-forensic-case-engine-evidence-states-attribution-and-uncertainty), [International AI Forensics Methodology](https://beywolf5.wixsite.com/international-ai-for/methodology).  
A drift signal is not a cause. Preserve artifacts, reproduce, distinguish association from causality, then update the affected mapping version based on bounded findings.

## Content-quality findings
1. **Repeated tail paragraphs:** six reviewed My Site 17 logic-box and demo pages append the same three philosophical/economic paragraphs. Verify whether this is intentional shared content or accidental body duplication before editing.
2. **Generic store products:** Computational Logic lists 12 product URLs titled “I'm a product” with template text. These are inventory records, not validated logic packages.
3. **Mixed-purpose site content:** alliance, NGO, generic FAQ, product-template and other non-logic pages remain in the inventory but are excluded from the validated logic core.

## Artifacts
- [Machine-readable page inventory and candidate maps](./data/WIX_PAGE_INVENTORY_2026-10-12.json)
- [Bridge between public site and WANGA-LAB](./LOGIC_BEFORE_IMPLEMENTATION_SITE_BRIDGE.md)
- [Continuous Logic Mine research track](./LOGIC_MINE_RESEARCH_TRACKS.md)

## Quality-control changes
- The Logic Engine landing page now emphasizes five direct research sources and no longer presents a broad mixed-purpose collection of unrelated site cards.
- The 70-article source register is explicitly a sitemap/article catalogue, not a claim that every article's content has been semantically verified.
- The 174-URL inventory is now searchable by URL, site, page kind, and focused-review status; tags are labelled as URL-derived filters.
- Misleading 'verified sources' wording was changed to 'sources reviewed'. Original source pages were not edited or deleted.

## Post-deploy QA
- Browser test confirmed that the 174-record URL inventory loaded, had no duplicate URLs, filtered to 29 `CONTENT_REVIEWED` records, and returned the correct filtered state for `my-site-17`.
- Browser tests confirmed the synthetic price calculation (about 22.22%) and threshold-drift case (score 0.75; 0.80 => REJECT; 0.60 => ACCEPT).
- The homepage's unrelated mixed-purpose cards were removed. The interactive node behavior on `cross-site-logic-map.html` remains to be tested separately.

## Evidence vocabulary
- `SITEMAP_LISTED`: URL appears in a public sitemap.
- `CONTENT_REVIEWED`: contents were inspected in this audit stream.
- `PROPOSED_COMBINATION`: source-derived design that requires composite testing.
- `VERIFIED_WITHIN_SYNTHETIC_FIXTURE`: verification is limited to the described synthetic case.
- An explicit hyperlink is not automatically a logical dependency.
