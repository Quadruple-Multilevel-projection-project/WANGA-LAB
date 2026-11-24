# Master Connection Map — Neural Wiki Surfaces V1

**Project:** מילות ההיגיון / Logic Factory / WANGA-LAB  
**Created:** 2026-11-24  
**Status:** DOCUMENTED_LINK_MAP / RUNTIME_EDGES_NOT_VERIFIED  
**Canonical repository:** [Quadruple-Multilevel-projection-project/WANGA-LAB](https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB)

## 1. Purpose and boundary

This document establishes a source-preserving navigation and relation map across the project's three public Logic Wiki surfaces, the canonical GitHub research corpus, the three linked logic applications, the Logic Boxes, and the wider application hub.

A hyperlink is a navigation edge. It is not, by itself, proof of semantic entailment, data synchronization, API integration, or runtime execution.

The map therefore distinguishes:
- **NAVIGATION** — a human-readable link between artifacts.
- **SOURCE_OF** — a source artifact supports a record, subject to exact locator review.
- **DERIVED_FROM** — a record was transformed from a source through a recorded process.
- **ANALYTICAL_MAPPING** — an analytical invariant is compared with a candidate logical tool.
- **REVERSE_MAPPING** — the logical tool is checked back against the analytical source.
- **EDITORIAL_RELATION_CANDIDATE** — a catalog relation that is not a proof or entailment.
- **RUNTIME_CALL** — an application-to-application request; requires a successful observed round trip.
- **PUBLISHES_TO** — a GitHub-managed record is represented on a public site; requires read-back to verify publication.

## 2. Three Wiki surfaces

These are three public pages/surfaces under one Wix site, not three independent authoritative databases. The GitHub catalog remains the source-review path.

| ID | Surface | URL | Canonical source | Recorded state |
|---|---|---|---|---|
| WIKI-01 | Logic Wiki catalog | https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki.html | `logic_wiki/data/articles.json` | PUBLISHED_READ_BACK_PARTIAL |
| WIKI-02 | Logic Fractal Research | https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-fractal-research.html | `logic_wiki/data/fractal_taxonomy.json`, `logic_fractal/data/recursive_composition_contracts_v1.json` | PUBLISHED_READ_BACK_PARTIAL |
| WIKI-03 | Logic Wiki Research Status | https://headless-jhbcjnxnldu-beywolf5-1408.wix-site-host.com/logic-wiki-research-status.html | `research/reports/logic-fractal/*`, `logic_wiki/data/readiness_gate.json` | PUBLISHED_READ_BACK_PARTIAL |

The current Wix sync manifest records a partial read-back of these three files, 28 catalog cards, 10 extended topic resources, and 111 editorial relation links. It explicitly does not claim that every site file was re-audited. See [Wix sync manifest](../logic_wiki/data/wix_sync_manifest.json).

## 3. Canonical processing order

Preserve this order; do not skip or collapse stages:

`SOURCE → LINEAGE → EXTRACTION → RELATIONS → LOGIC → VERIFICATION → CONFIGURATION → WEIGHTS`

The epistemic sequence is:

`מוחש → הכרח → מושכל`

Rules:
1. Preserve the original source and its exact locator.
2. Keep literal extraction separate from normalization and interpretation.
3. Keep ANALYTICS separate from LOGIC_CONFIGURATION.
4. A mapping is a separately versioned, evidence-bearing relation; it is neither identity nor proof.
5. Reverse-check every forward analytical mapping.
6. Preserve contradictions, non-matches, scope boundaries, and unresolved items.
7. `WEIGHTS = NOT_CREATED` until the relevant logic is source-grounded and verified.
8. Do not silently normalize, translate, repair, or overwrite source wording.

## 4. Three application responsibilities

| ID | Application | Responsibility | Known URL | Runtime edge |
|---|---|---|---|---|
| APP-01 | Logic Analytics Orchestrator | Extract source-invariant analytical units; no logical-tool mapping during extraction | https://milot-hahigayon-logic-analytics-orchestrator-5hz495.v2.appdeploy.ai/ | NOT_VERIFIED |
| APP-02 | Claim & Balance Validator / מפת הקשרים | Test claims against premises, evidence, alternatives, contradictions and reverse mappings | https://app-mcuqrn.v2.appdeploy.ai/ | NOT_VERIFIED |
| APP-03 | Error Prevention & Balance Guard / שער הידיעה והוודאות | Detect source drift, unsupported assignments, missing locators, duplicate/conflicting edges and unbalanced mappings | https://app-asqobu.v2.appdeploy.ai/ | NOT_VERIFIED |

These application roles are distinct from the three Wiki surfaces. A page link between an app and a Wiki does not prove API-to-API integration.

## 5. Logic Boxes — related specifications, not Wiki instances

| ID | Logic Box | Public specification |
|---|---|---|
| BOX-01 | Evidence Gatekeeper | https://beywolf5.wixsite.com/my-site-17/post/logic-box-01-evidence-gatekeeper |
| BOX-02 | Task Decomposer & Scope Binder | https://beywolf5.wixsite.com/my-site-17/post/logic-box-02-task-scope-binder |
| BOX-03 | Deterministic Action Filter | https://beywolf5.wixsite.com/my-site-17/post/logic-box-03-deterministic-action-filter |

The three boxes are complementary specifications. They are not assumed to form a working pipeline until individual and composed tests demonstrate the pass, deny, contradiction, insufficient-evidence, scope-violation, and downstream-failure cases.

Catalog and methodology entry points:
- Main site: https://beywolf5.wixsite.com/my-site-17
- Blog/catalog: https://beywolf5.wixsite.com/my-site-17/blog
- Logic in Boxes catalog: https://beywolf5.wixsite.com/my-site-17/post/logic-in-boxes-catalog-he
- Methodology: https://beywolf5.wixsite.com/my-site-17/post/logic-box-methodology
- FAQ: https://beywolf5.wixsite.com/my-site-17/post/logic-boxes-faq-he
- Custom Logic Box request: https://beywolf5.wixsite.com/my-site-17/post/custom-logic-box-request

## 6. Application hub and supporting deployments

| ID | Application | URL | Responsibility | Recorded boundary |
|---|---|---|---|---|
| HUB-01 | Logic Factory Hub | https://logic-factory-hub-9jj4jw.v2.appdeploy.ai/ | Orchestration, task planning, health checks, gate control, receipts | Deployed; backend routes inspected in operating map |
| APP-04 | AI231 Logic Registry | https://ai231-logic-registry-1y5kvl.v2.appdeploy.ai/ | Source, term, map, workbook-cell and relation registry | Writes require owner authentication and configured secret |
| APP-05 | AI231 Agent Foundry | https://ai231-agent-foundry-35gumn.v2.appdeploy.ai/ | Agent blueprints and bounded dispatch | End-to-end runtime/permission verification separate |
| APP-06 | Logical Configuration Orchestrator | https://logical-configuration-orchestrator-5fvr64.v2.appdeploy.ai/ | Configuration contracts, prerequisites, acceptance gates | Direct relay from Hub not verified |

Do not create duplicate apps for these processor families. Extend the existing owner application only after inspecting its contract and permissions.

## 7. GitHub source and research repositories

| ID | Repository | URL | Use in this map |
|---|---|---|---|
| REPO-01 | WANGA-LAB | https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB | Canonical research, logic wiki catalog, provenance and architecture |
| REPO-02 | WANGA-LAB.-01 | https://github.com/AmbassadorOv/WANGA-LAB.-01 | Related project repository; exact shared-file lineage must be established per artifact |
| REPO-03 | AmbassadorOv | https://github.com/AmbassadorOv/AmbassadorOv | Personal project/research index |
| REPO-04 | -logicl-neural-order | https://github.com/tribal-archery/-logicl-neural-order | Experimental neural-order repository; do not treat README claims as verified runtime |
| REPO-05 | AI231.meta.io | https://github.com/tribal-archery/AI231.meta.io | AI231 repository; inspect exact branch and content before assigning a role |
| REPO-06 | MAM-parsed | https://github.com/tribal-archery/MAM-parsed | Parsed corpus candidate; format stability and ingestion require separate review |

Repository ownership or visibility does not establish that every repository is part of one runtime system. Each asserted cross-repository lineage edge needs an exact source file, commit/ref, and locator.

## 8. Core GitHub artifacts

- [Logic Wiki schema and rules](../logic_wiki/README.md)
- [Article catalog](../logic_wiki/data/articles.json)
- [Fractal taxonomy](../logic_wiki/data/fractal_taxonomy.json)
- [Bounded agent registry](../logic_wiki/data/agent_registry.json)
- [Wix synchronization manifest](../logic_wiki/data/wix_sync_manifest.json)
- [Logic Mine research tracks](../research/LOGIC_MINE_RESEARCH_TRACKS.md)
- [Daily integration map: Logic Research, Logic Boxes, Public Site](./DAILY_INTEGRATION_MAP_2026-10-13.md)
- [Daily Processor Operating Map](./architecture/WANGA_DAILY_PROCESSOR_OPERATING_MAP.md)
- [Logic architecture correction and traceability](./LOGIC_ARCHITECTURE_CORRECTION_AND_TRACEABILITY_V1.md)

## 9. Link-record syntax

Every edge added to a machine-readable registry must contain:

```json
{
  "edge_id": "EDGE-<stable-id>",
  "from_id": "<stable-node-id>",
  "to_id": "<stable-node-id>",
  "relation_type": "NAVIGATION | SOURCE_OF | DERIVED_FROM | ANALYTICAL_MAPPING | REVERSE_MAPPING | EDITORIAL_RELATION_CANDIDATE | RUNTIME_CALL | PUBLISHES_TO",
  "direction": "FORWARD | REVERSE | BIDIRECTIONAL",
  "source_ref": "<repository/path@commit-or-version>",
  "evidence_locator": "<exact section, line, record ID, or URL fragment>",
  "transformation": "<NONE or reproducible transformation>",
  "claim_status": "DOCUMENTED | CANDIDATE | VERIFIED | UNRESOLVED | BLOCKED",
  "verification_method": "<what was actually checked>",
  "verified_at": "<ISO-8601 timestamp or null>",
  "reverse_check_required": true
}
```

Validation invariants:
- `from_id` and `to_id` must resolve to registered nodes.
- `RUNTIME_CALL` requires observed request and response evidence, not a hyperlink.
- `ANALYTICAL_MAPPING` requires exact quotes and locators from both source domains.
- `REVERSE_MAPPING` must test the candidate logic tool back against the analytical source.
- `EDITORIAL_RELATION_CANDIDATE` must never be rendered as entailment or proof.
- `VERIFIED` requires reproducible evidence and an exact locator.
- Missing evidence stays `UNRESOLVED` or `BLOCKED`; it is not filled by inference.
- Original source records are immutable; revisions create new versions.

## 10. Existing catalog relation rule

The catalog currently declares that each edge generated from an article's `relations` field is an `EDITORIAL_RELATION_CANDIDATE` unless an explicit formal rule with cited premises and tests establishes a stronger relation.

Do not convert the catalog's 111 editorial links into 111 verified logical relations. Retain their current type until individually validated.

## 11. Uploaded Kraken workspace — separate artifact

The uploaded `grok-workspace.zip` contains a React/TanStack application branded **שער 231 / Kraken 36**, a catalog of architecture topics, and an attached `Kraken_Full_Architecture_For_Ilan.zip` with ten spreadsheet workbooks. This is an imported workspace artifact, not proof that it is the canonical Logic Wiki or that it is wired to the WANGA-LAB applications.

Its records should be registered as a separate source package with file hashes, workbook/sheet/cell locators, and a comparison against the canonical sources before any merge. Preserve its terminology and original data; do not silently replace the canonical catalog.

## 12. Acceptance gates for real connection

A link map is documented when all nodes and navigation URLs are recorded. A system is connected only after each relevant integration passes its own acceptance test:

1. Source record resolves to an exact immutable source locator.
2. Extracted record preserves exact text and source span.
3. Forward mapping stores both exact source quotations and the mapping basis.
4. Reverse mapping checks the candidate logic tool against the analytical source.
5. Contradictions, non-matches, and boundary failures remain visible.
6. Registry write returns a receipt and read-back matches the submitted record.
7. Wix publication is checked by reading back the exact page and checking the reciprocal navigation.
8. Application-to-application calls are tested with a bounded request/response and permission check.
9. Status is promoted only to the strongest state supported by the evidence.

Until these gates pass, report **DOCUMENTED_LINK_MAP / RUNTIME_EDGES_NOT_VERIFIED**.

## 13. Immediate next work

1. Audit the exact contents and schema of the three Wiki surfaces against the current GitHub catalog.
2. Compare the uploaded Kraken workbooks and app catalog with canonical WANGA records, preserving conflicts.
3. Build a machine-readable node/edge registry using the link-record syntax above.
4. Add reciprocal navigation only through the existing Wix/GitHub publication workflow and verify read-back.
5. Test one end-to-end path: source → extraction → analytics → forward mapping → reverse mapping → claim/balance validation → Registry receipt.
6. Do not create or activate weights, neural parameters, or new agent runtimes as part of link discovery.
