# AI231 / WANGA — Unified Execution Roadmap
Last updated: 2026-11-20
Queue owner: AI231 Unified Execution Agent
Canonical schedule: Automation 2, daily 08:00 Asia/Jerusalem
This file is the single cumulative project backlog for the unified queue. It is not a new automation or a parallel scheduler.

## Governing rules
- WIN WITHOUT DEPENDENCE: customer value, paid validation, positive contribution margin, verified delivery and reinvestment from collected cash take priority.
- Grants and investors are optional; compare full risk-adjusted net benefit with the independent baseline and preserve IP/control.
- No production Wix write, publication, external message, payment, token issuance, contract, spending or irreversible action without explicit approval.
- Agent blueprint / registry entry / orchestration graph is not a deployed agent. Runtime activation requires exact-version backend configuration, invocation logs, isolation and egress evidence, and acceptance-test results.
- Cash, cash costs, contribution margin, qualified pipeline, forecasts and internal Logic Credits are separate measures.

## Existing goal reconciliation
- GitHub issue #90 already covers Proof-of-Logic and reward ledger design before token issuance. Advance it; do not create a duplicate ledger goal.
- GitHub issue #91 already covers the logic marketplace and Execution Shield boundary. Keep it as the existing marketplace goal.
- GitHub issues #148 and #149 both cover paid Logic Auditor / Wix pilot discovery and were created eight seconds apart. They remain open and are a possible duplicate pair; no issue was created or closed.
- Notion's accessible task/project database contains other projects but no AI231-specific consolidated execution goal. The generic homepage-copy task belongs to a separate website-redesign project and was not repurposed.
- Automation 2 remains the single canonical execution queue. No additional schedule was created.

## Backlog

### AI231-AGENT-FACTORY-WIX-AUDITOR-001
- Source: PR #160; `agent_blueprints/ai231-wix-site-evidence-auditor.json`; schema/verifier/test changes.
- Priority: P1.
- Owner: Agent Factory.
- Dependencies: exact CI verification; later, isolated backend configuration and runtime invocation evidence.
- Acceptance: canonical JSON Schema validation and dedicated acceptance tests pass; the agent remains read-only; dynamic routes remain unresolved until live verification; rollback is explicit.
- Permission/risk: repository branch only; no Wix write permission.
- Status: DONE_SPECIFIED_AND_CI_VERIFIED; root-relative link normalization added and verified; runtime NOT_CONFIGURED.
- Evidence: prior commit `0731ced6d7b2b190e49e7d2c93855bb42684db58`; updated blueprint/test commit `760ac153296a41a74954e392c22c334d291990ec`; workflow run `44880076176`, job `136773215667`; exact steps `Verify agent blueprint contract`, `Validate agent blueprint JSON Schemas`, `Wix site evidence auditor tests`; seven tests passed, including root-relative normalization.
- Next action: design a sandboxed invocation adapter and test isolation/egress before any deployment.

### AI231-WIX-CORE-METADATA-001
- Source: Wix read-only audit of Logic Engine Research Lab, AI231 Global Neural Governance and The Logic Economy.
- Priority: P1.
- Owner: Site Evidence Auditor (draft).
- Dependencies: user approval for each exact site/change/publication scope; route and terminology verification.
- Acceptance: preview-only metadata/content corrections; dated historical metrics; live route, accessibility and mobile checks.
- Permission/risk: read-only plus repository draft; production writes BLOCKED without explicit approval.
- Status: DRAFT_READY / PRODUCTION_BLOCKED; metadata patch prepared for budget.html, roadmap.html and technology.html.
- Evidence: `business_brain/website-drafts/2026-11-20-CORE-SITE-AUDIT-DRAFT.md`; `business_brain/website-drafts/2026-11-21-AI231-GLOBAL-SEO-METADATA-PATCH.md`.
- Next action: prepare a non-production preview only after the specific scope is authorized.

### AI231-WIX-COVERAGE-063-001
- Source: Wix ListWixSites inventory: 69 sites total; eight unique sites deeply inspected across the 2026-11-20 and 2026-11-21 rotations.
- Priority: P1.
- Owner: Site Evidence Auditor (draft).
- Dependencies: authorized read-only site access and rotation order.
- Acceptance: inspect the remaining 61 sites with the same page/metadata/navigation/accessibility checks and record per-site status.
- Permission/risk: read-only; no production writes.
- Status: CARRIED_FORWARD.
- Evidence: two Wix inventory pages (50 + 19); prior six-site audit plus 2026-11-21 inspection of AI231 Logic Neuron Architecture (2 pages) and Neural Hebrew Letter Network (30 pages).
- Next action: select the next highest-priority batch; preserve exactly ten execution steps per run.

### AI231-LEDGER-STATE-SEPARATION-001
- Source: existing issue #90; PR #150 event schema and verifier.
- Priority: P1.
- Owner: Ledger Verifier.
- Dependencies: aggregate state schema, distinct internal issuance semantics, authorization and transition tests.
- Acceptance: planned, approved and issued-internal quantities are separate; external-token quantity remains zero; cash and contribution margin are independent.
- Permission/risk: repository design and test work only; no token or payment operation.
- Status: PARTIAL — aggregate-state schema, validator and fail-closed proposal/approval transition helper committed to PR #150; exact CI run pending at roadmap update.
- Evidence: `docs/LOGIC_CURRENCY_LEDGER_STATE_MODEL_V1.md`; PR #150 base implementation `774252990d53bc7f7a2687f942a2230db5031619`; schema `schemas/logic-currency-ledger-state-v1.schema.json`; validator `scripts/validate_logic_currency_ledger_state.py`; tests `tests/test_logic_currency_ledger_state.py`; final PR #150 commit `a471226e8763f9326613abdd5bbc1a01501ea619`.
- Next action: add the aggregate state schema and tests in a separate reviewable branch.

### AI231-LOGICAL-ISLANDS-ECONOMY-001
- Source: `docs/LOGIC_ECONOMY_BUSINESS_PLAN_V1.md`, `research/FUTURE_MARKET_ASSUMPTIONS_LEDGER.md`, Logic Economy site context.
- Priority: P1.
- Owner: Economic Agent.
- Dependencies: buyer evidence, actual cash records, attributable direct costs and partner terms.
- Acceptance: actual cash collected, cash costs, contribution margin, qualified pipeline, forecasts and internal Logic Credits reported separately.
- Permission/risk: analysis only; no funding request, payment flow or partner commitment.
- Status: PARTIAL — economic model reviewed; actual transaction/cost evidence unavailable.
- Evidence: `business_brain/economy/2026-11-20-LOGICAL-ISLANDS-REVENUE-FIRST-REVIEW.md` (updated 2026-11-21 with official Lighthouse, Screaming Frog and Semrush alternatives).
- Next action: instrument cash and delivery-cost capture before claiming unit economics.

### AI231-REVENUE-PILOT-VALIDATION-001
- Source: existing issues #148 and #149.
- Priority: P1.
- Owner: Commercialization Agent.
- Dependencies: explicit user authorization for outreach; buyer budget authority and paid-pilot acceptance.
- Acceptance: 10–15 discovery conversations, 3 qualified opportunities and at least 1 paid pilot; record actual collected cash and direct delivery cost.
- Permission/risk: internal offer draft only; no outreach or customer contact in this run.
- Status: DRAFT_ONLY / WILLINGNESS_TO_PAY_NOT_VERIFIED.
- Evidence: `business_brain/revenue/LOGIC_AUDITOR_PAID_PILOT_DRAFT_2026-11-20.md` (updated 2026-11-21 with differentiation and timed cost-measurement protocol); issues #148/#149.
- Next action: obtain outreach authorization, then test the €290 ex-VAT pricing hypothesis.

### AI231-AUTOMATION2-WIX-COVERAGE-CONFLICT-001
- Source: `business_brain/logs/2026-11-20-AI231-SUPERVISOR-RUN-005.md` and Automation 3 latest handoff.
- Priority: P1.
- Owner: Automation 3 Governance.
- Dependencies: read back the exact current Automation 2 prompt and reconcile the per-site quota with rotating coverage.
- Acceptance: Step 3 is the only website slot; inspect a priority batch, carry overflow forward, do not require one change per every site in every run, retain exactly ten steps and preserve the 08:00 schedule.
- Permission/risk: automation configuration change requires explicit governance authorization; no schedule change.
- Status: CARRIED_FORWARD to Automation 3.
- Evidence: Supervisor Run 005; latest Automation 3 handoff dated 2026-11-18.
- Next action: Automation 3 to verify the exact prompt text and prepare a narrow correction for review.

### AI231-PROCESSOR-TERMINOLOGY-MAJORANA-001
- Source: `AI231 Global Neural Governance/technology.html` and `roadmap.html`.
- Priority: P1.
- Owner: Architecture Curator.
- Dependencies: authoritative confirmation of the exact canonical processor name and version.
- Acceptance: replace legacy terminology only after source confirmation; preserve historical provenance.
- Permission/risk: content draft only; no public write.
- Status: BLOCKED — site contains “MIOMA-1”; canonical replacement is not independently verified from the inspected site source.
- Evidence: Wix read-only page snapshots; `business_brain/website-drafts/2026-11-20-CORE-SITE-AUDIT-DRAFT.md`.
- Next action: resolve against the canonical source document before editing public copy.

### AI231-ISSUE-148-149-DUPLICATE-REVIEW-001
- Source: GitHub issues #148 and #149.
- Priority: P2.
- Owner: Queue Curator.
- Dependencies: maintainer review; compare acceptance criteria and source history.
- Acceptance: determine whether one issue is a duplicate; do not close or overwrite without authorization.
- Permission/risk: read-only assessment.
- Status: ASSESSMENT — plausible overlap, not proven duplicate.
- Evidence: issue creation times differ by eight seconds; both have no comments/assignees at inspection.
- Next action: preserve both until the maintainer resolves the duplicate question.

### AI231-EXTERNAL-CONVERGENCE-TRACK-001
- Source: primary-source review dated 2026-11-20.
- Priority: P2.
- Owner: Research Agent.
- Dependencies: primary sources and implementation evidence.
- Acceptance: compare implemented controls and standards; separate released implementation, protocol specification, research and vendor claims.
- Permission/risk: public-source research only.
- Status: ONGOING — refreshed 2026-11-21 with primary-source implementation details for LangGraph, OpenAI Agents SDK, smolagents, Lighthouse, Screaming Frog and Semrush.
- Evidence: `research/2026-11-20-AGENT-CONVERGENCE-AND-VERIFICATION.md`; `research/2026-11-21-AGENT-CONVERGENCE-UPDATE.md`.
- Next action: track material changes in agent identity, task protocols, isolation and evaluation; no external WANGA adoption is claimed.

## Staleness and priority flags
- Searches for open issues labeled P0 and P1 returned no results. No separate priority field was exposed; do not infer labels.
- The open-issue query for `updated:<2026-11-13` returned 25 stale issues, consistent with Supervisor Run 005. Preserve them; do not silently displace them.
- Issue #126 (source verification, 18-versus-17 mismatch) is among the stale items and remains open. No source-level resolution was performed in this run.
- P0/P1 staleness cannot be classified by label because no P0/P1 labels or priority field were found. The newly created P1 queue entries above retain their evidence and next acceptance conditions.

## Latest run state
- Run ID: `094538d9-f674-8325-b270-b969c1376500`.
- Scheduled for: `2026-11-20T08:00:00+02:00`.
- Started: `2026-11-20T09:18:14.991525+02:00` (late start; 78 minutes after scheduled time).
- Automation 2 remains enabled daily at 08:00 Asia/Jerusalem.
- Automation 3 remains enabled daily at 07:30; its latest completed run and handoff are dated 2026-11-18. No newer Automation 3 handoff was found.
- No new automation or schedule was created.


### AI231-PUBLIC-SITE-PAGES-CONFIG-001
- Source: open PR #164, branch website/ai-logical-atlas-public-site, GitHub Pages build run 44857352444.
- Priority: P2.
- Owner: Site/Deployment Agent.
- Dependencies: repository owner must explicitly enable/configure GitHub Pages with GitHub Actions; exact public publication scope must be approved.
- Acceptance: exact PR head workflow succeeds through build/deploy and the resulting public URL is verified without exposing credentials or changing unrelated repository settings.
- Permission/risk: repository Pages settings and public deployment; BLOCKED without explicit approval.
- Status: BLOCKED — job 136702550348, step Run actions/configure-pages@v5 failed with Get Pages site failed; GitHub reports Pages is not enabled/configured. No setting or publication action was performed.
- Evidence: PR #164 head 63fb5c572a5a26485e5e65ac76aaeea61c0c376c; failed run 44857352444; checked-out workflow commit bbac8635b1bc07ca68d2c34a4b45ab47e34f19e0.
- Next action: request explicit authorization for the exact repository Pages setting and public deployment, then rerun the workflow on the current PR head.

## Run 2026-11-21 evidence delta
- Existing goals advanced: issue #90 (ledger), issue #91 (marketplace boundary), issue #148 (paid pilot discovery), and the existing agent/site coverage tasks.
- Possible duplicate pair #148/#149 remains unresolved; no issue was closed or created.
- New subtask: root-relative static-link normalization added to the existing Wix Site Evidence Auditor acceptance contract; no separate goal created.
- New website draft: metadata-only patch for three AI231 Global Neural Governance pages; production remains blocked.
- New ledger implementation: separate aggregate state schema and transition tests on the existing PR #150; no internal issuance or external token issuance.
- Two additional Wix sites inspected; 61 of 69 sites remain in the rotation.
- Current open-issue search: 27 open issues; 25 match the stale updated-before-2026-11-14 query. No open issues labeled P0 or P1 were returned. Do not infer priority from title.
- Latest Automation 3 handoff accessible in the repository remains dated 2026-11-18; no newer Automation 3 to Automation 2 handoff was found.
- Actual cash collected, actual cash costs and contribution margin remain NOT_YET_VERIFIED / NOT_COMPUTABLE from connected records; internal Logic Credits remain non-cash.
