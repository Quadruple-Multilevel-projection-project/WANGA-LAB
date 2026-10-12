# Research ↔ Public Site Bridge

**Status:** DOCUMENTED / LINKS ESTABLISHED  
**Purpose:** Connect the public-facing Forensic Logic Drift site with the technical research archive in WANGA-LAB. This page records the research direction discussed on 2026-10-12 without claiming that the proposed architecture has been implemented or validated.

## Public research site

- [Forensic Logic Drift — Wix site](https://beywolf5.wixsite.com/forensic-logic-dri)

## Technical research archive

- [WANGA-LAB repository](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB)
- [Logic Mine research tracks](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/LOGIC_MINE_RESEARCH_TRACKS.md)
- [Daily integration map — Logic Research, Logic Boxes, and Public Site](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/DAILY_INTEGRATION_MAP_2026-10-13.md) — connects the 5+5 architecture review, corpus/source audits, first three logic products, and the public Hebrew catalog.

## Shared research thread: Logic before implementation

The research strategy is to investigate and document logical structures now, while technical implementation capabilities continue to evolve. The working hypothesis is that increasingly capable AI systems may eventually reduce the engineering effort required to translate formal logical specifications into executable systems.

The proposed architecture explores:
- foundational logical components and their relations;
- multi-level logical mapping and reconstruction;
- traceability of transitions between states;
- revisiting the initial mapping in light of later results;
- future machine-assisted implementation and testing.

These are research aims, not claims of a completed or verified system. The exact architecture, including its ten layers, requires formal specification and comparison against existing work.

## Cross-linking convention

When the public site publishes an article on this research thread, add its exact article URL here. When the public article is available, it should link back to this repository page so readers can move between the public explanation and the technical archive.

**Public article URL:** PENDING PUBLICATION  
**Technical record:** This file in WANGA-LAB

## Cross-site inventory and logic-map audit

- [Wix cross-site logic-map audit](./WIX_CROSS_SITE_LOGIC_MAP_AUDIT_2026-10-12.md) — six candidate solution maps, source evidence, page-quality findings and scope limits.
- [Machine-readable Wix inventory](./data/WIX_PAGE_INVENTORY_2026-10-12.json) — 174 unique public sitemap URLs across 16 site slugs, grouped by site and page type.
- [Interactive Logic Engine Research Lab](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com) — visual demo of logic maps and solution paths.
- [Logic boxes and demos](https://beywolf5.wixsite.com/my-site-17/blog) — scope binder, evidence gatekeeper, deterministic action filter and worked examples.

### Map integrity rule
A published hyperlink is recorded as a link, not automatically as a logical dependency. A proposed composition stays `PROPOSED_COMBINATION` until the combined behavior is tested. The criterion-drift example remains verified only within its declared synthetic fixture.

### Audit snapshot — 2026-10-12
- Wix account listing: 53 sites.
- This pass: 28 public sitemap files, 174 unique non-category URLs across 16 site slugs.
- This is a sitemap-based inventory, not proof that every private, draft, unindexed, or sitemap-less page in all sites was inspected.
- Observed: repeated philosophical/economic tail paragraphs on reviewed My Site 17 logic-box posts; generic “I'm a product” placeholders on 12 Computational Logic product URLs. Both are flagged for review, not automatically edited.

## Quality-control snapshot — 2026-10-12

- [Quality-control report](./QUALITY_CONTROL_2026-10-12.md) documents scope, cleanup decisions, and remaining issues.
- [Searchable Wix inventory](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/source-audit.html) now includes all 174 sitemap-listed URLs from this inventory and explicitly distinguishes 29 focused content reviews from 145 inventory-only records.
- The public landing page was reduced to five direct research sources; the off-topic mixed-purpose card set was removed.
- The label 'verified public sources' was changed to 'public sources reviewed'; the 70-post list is labelled as a sitemap register.
- Original source Wix content was not deleted or rewritten. Six repeated-tail observations and twelve generic store placeholders remain flagged for manual source-page review.
- Inventory check: 174 records, 174 unique URLs, 16 site slugs, zero duplicate URLs.

## Extended Logic Corpus — live atlas

- [Interactive corpus atlas](https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-corpus-atlas.html) — searchable 1,000-page blueprint and SVG exploration of 22 letter nodes, 231 unordered pairs, 462 directed transitions, and 1,540 unordered triple sets.
- [Page-definition plan](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/EXTENDED_LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.md).
- [Machine-readable index](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/data/LOGIC_CORPUS_1000_PAGE_BLUEPRINT_V1.json).
- [231/462 gate map](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/data/LETTER_GATE_MAP_231_V1.json) and [1,540 triple-set map](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/data/LETTER_TRIPLE_MAP_1540_V1.json).
- [Mathematical integrity register](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/LOGIC_231_MATHEMATICAL_INTEGRITY_REGISTER_V1.md).

**Atlas QA (2026-10-12):** browser test passed for loading all 1,000 page definitions, exploring undirected/directed/triple map modes, and finding `GATE-001`. Page definitions remain SPECIFIED / NOT_YET_VERIFIED; this does not verify the semantic role of all gates or a production runtime.

## Logic-native model builder and language

- [Live Wix documentation]( https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-native-model-builder.html ) documents the LNL/0.1 language, candidate–critic–refine loop, reviewed GitHub references and remaining research gaps.
- [Logic Model Builder package](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/tree/main/logic_model_builder_v1) adds a parser/compiler, a structured baseline provider, an optional model-endpoint adapter and execution through the WANGA symbolic kernel.
- [Architecture record](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/LOGIC_NATIVE_LANGUAGE_MODEL_BUILDER_V1.md).
- [Merged PR #96](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/pull/96); CI checks passed for model-builder tests, repository integrity and CodeQL.
- Status boundary: BUILT as an experimental prototype; not a new foundation model; LLM calls require explicit endpoint configuration; semantic validity and full natural-language formalization remain NOT_YET_VERIFIED.

## WANGA-X executable Blueprint engine

- [Implementation record](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/WANGA_X_EXECUTABLE_BLUEPRINT_ENGINE_V1.md).
- [Blueprint generator](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/tree/main/wanga_x_v1).
- [Merged PR #97](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/pull/97); merge commit `638d97a3e201c60a48fbf51ab30ba013837886c2`.
- CI passed for WANGA-X Blueprint tests, Repository Integrity and CodeQL Advanced.
- Capability boundary: executable requirement-to-computation mapping and Blueprint generation are built; neural weights, runtime materialization and live endpoint creation are not.
