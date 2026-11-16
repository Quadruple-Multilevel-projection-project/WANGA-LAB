# AI231 × Agency Agents — Autonomous Company Build Integration v1.0

Timestamp: 2026-11-16T15:27:30+02:00  
Contract_Start_Time: 2026-11-16T15:27:30+02:00  
Action_ID: ACT-20261116-AI231-AGENCY-AGENTS-INTEGRATION-001  
Action_SHA256: ac8a965377fee3fd1b8802034a37775bbaf00445ee5f171741edd81983dc7ab3

Status: **INTEGRATION PLAN COMMITTED — no agents imported, installed, activated, or benchmarked by this document.**

## 1. Purpose

Use [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) as an upstream catalog of specialist-agent definitions to accelerate the construction of an AI-operated company inside AI231/WANGA.

The upstream README describes a growing catalog of specialist agents, installation/conversion paths for multiple coding-agent environments, and an MIT license badge. The repository is pinned for this integration review at commit `8ae6164602c95ca78828b148b9052460ee426885`. Recheck the license file and every file's provenance before copying or redistributing content.

The user supplied the figures **232 agents / 16 divisions / 168,000+ stars**. At the pinned source commit, the upstream `divisions.json` directly lists **18 divisions**, so the supplied division count of 16 does not match that source file. The exact agent count and current star count have not yet been independently measured. The agent count must be generated from the pinned tree and recorded with the reproducible inventory command before adoption.

## 2. What the upstream project provides — and what it does not

It provides reusable specialist role definitions, workflows, expected deliverables, division organization, installation/conversion scripts, and scenario runbooks.

It does not by itself provide:
- a legally formed company;
- a complete business operating system or verified end-to-end autonomy;
- a global algorithmic-governance or economic-diffusion engine;
- verified production security, sandboxing, credentials, observability, or disaster recovery for this project;
- authority to spend money, enter contracts, publish externally, hire, or make binding decisions.

Therefore AI231 must treat it as a **specialist-agent source catalog**, not as the company runtime or governance layer.

## 3. Target architecture

```text
AI231 / WANGA CONTROL PLANE
  ├── Constitutional & Governance Core
  │     ├── equal human standing; no assumed superior authority
  │     ├── authority/provenance register; no authority inferred from wealth
  │     ├── public-interest, rights, due-process and appeal constraints
  │     └── prevention / risk / conflict-of-interest controls
  ├── Global Diffusion & Coordination Engine
  │     ├── map resource, capability, access and dependency bottlenecks
  │     ├── model distribution options and externalities
  │     ├── coordinate voluntary participation and local decision processes
  │     └── measure whether concentration and exclusion actually decrease
  ├── Company Operating System
  │     ├── strategy, product, research, engineering, security, QA
  │     ├── finance, legal/compliance, operations, customer support
  │     ├── sales, marketing, partnerships and documentation
  │     └── project portfolio, budgets, service levels and reporting
  ├── Specialist Agent Registry (adapted upstream Agency Agents)
  ├── LangGraph orchestration + provider-neutral model adapters
  ├── isolated worker execution / secrets boundary / audit trail
  └── human authorization gates for consequential external actions
```

The governance and diffusion engine is not a department inside the company and is not subordinate to company revenue targets. It is a separate control plane with its own public-interest objectives, evidence, constraints and review.

## 4. Integration rules

1. Pin upstream source to an immutable commit; never track an unpinned moving branch in production.
2. Inventory every agent file, division, frontmatter/schema, tool assumptions, model assumptions, and license/provenance.
3. Map upstream specialist roles to AI231 work units; do not assume a one-to-one mapping between upstream divisions and AI231 departments.
4. Deduplicate roles and identify missing roles, especially governance, public-interest economics, diffusion analysis, rights impact, independent verification, and incident response.
5. Convert selected roles into AI231 canonical blueprints; preserve source URL, commit, path, original content hash, adaptation diff, version and license.
6. Validate every blueprint with the existing AI231 schema and `core/verify_contract.py`.
7. Run agents only in isolated runtimes. A Python virtual environment is not a sandbox. Deny network egress by default; grant least-privilege tools.
8. Use read-only and simulation modes first. External publication, payments, contracts, account changes, recruitment, and irreversible actions require explicit human authorization.
9. Benchmark on real project tasks against a fixed baseline. Record task success, evidence precision, schema compliance, boundary violations, latency, compute cost and recovery.
10. Do not describe the company as autonomous or production-ready until deployment, security, acceptance, recovery and operational evidence exist.

## 5. Initial company departments to instantiate

| AI231 workstream | Required agent capabilities | First concrete output |
|---|---|---|
| Executive operations | orchestration, planning, decision log | company operating plan and weekly queue |
| Product & research | product discovery, research synthesis | evidence-backed product backlog |
| Software engineering | architecture, frontend, backend, DevOps | tested application increments |
| AI/runtime engineering | model adapters, agent runtime, evaluation | provider-neutral agent runtime |
| Security & reliability | threat modeling, incident response, SRE | threat model and operational controls |
| Governance & rights | rights impact, authority provenance, appeals | governance rulebook and review workflow |
| Diffusion & economic systems | resource mapping, allocation simulation, market structure | baseline concentration/diffusion report |
| Finance & administration | bookkeeping workflows, budgets, cost controls | auditable budget and cost ledger |
| Legal & compliance | jurisdictional issue spotting, document tracking | issue register for qualified counsel |
| Sales & customer success | customer research, support, account workflows | customer pipeline and support playbook |
| Marketing & communications | content, research, analytics | evidence-based communications plan |
| Quality & verification | test design, evidence collection, independent review | acceptance suite and release report |

This is an AI231 workstream map, not a claim that the upstream project's divisions have already been mapped or imported.

## 6. First execution sequence

### Phase A — source inventory
- Clone or fetch the pinned upstream tree read-only.
- Count agent definitions and divisions from files, not marketing text.
- Parse metadata, role, tools, outputs, dependencies and licensing.
- Produce `agency_agents_inventory.json` and a human-readable report.
- Check duplicates, conflicting instructions, unsafe tool grants and missing governance roles.

### Phase B — adapter and blueprint conversion
- Implement a deterministic parser for upstream agent files.
- Convert one representative agent from each selected division into the AI231 blueprint schema.
- Preserve original text and hash; keep adaptation separate.
- Run schema validation and negative permission tests.

### Phase C — controlled company pilot
- Activate a small cross-functional team in a sandbox.
- Execute one bounded internal objective: research → specification → implementation → tests → review → report.
- Compare cost, time, quality, evidence precision and policy violations with a non-agent baseline.
- Do not authorize external side effects in the pilot.

### Phase D — governance/diffusion pilot
- Build a separate simulation using declared, sourced variables.
- Test whether alternative allocation/coordination rules reduce measured bottlenecks or concentration without violating rights or local choice.
- Publish assumptions, uncertainty, failure cases and reproducible results.
- Do not claim global authority or universal deployment.

### Phase E — deployment
- Only after security, legal review, user consent, independent verification, rollback and operational support are ready.
- Keep company operations and public-interest governance structurally separate.
- Publish APIs, audit records and portable data formats so the system cannot become a new proprietary gatekeeper.

## 7. Acceptance criteria

The integration is not accepted until all of the following have evidence:

- [ ] Pinned upstream commit and license audit.
- [ ] Reproducible inventory of all agent files and divisions.
- [ ] Source-to-blueprint provenance for every adopted agent.
- [ ] AI231 schema verifier passes.
- [ ] Permission-denial and prompt-injection tests pass.
- [ ] Runtime isolation and network-denial tests pass.
- [ ] Representative cross-department workflow completes end to end.
- [ ] Independent QA reproduces the results.
- [ ] Cost, latency, task quality and recovery metrics are recorded from actual runs.
- [ ] Governance/diffusion pilot has published assumptions and measured results.
- [ ] Rollback, operator ownership, data export and incident procedures are tested.

## 8. Current status and next action

**Verified in this integration session:** the upstream README and the existing AI231 factory/runtime integration specifications were read. The existing AI231 documents already define a blueprint factory, permission allowlist, runtime verification sequence and provider-portability requirement.

**Not yet done:** upstream clone, complete inventory, license audit, conversion, installation, agent activation, runtime tests, company deployment, diffusion simulation, or public rollout.

**Next action:** create the read-only inventory tool and report from the pinned upstream repository, then convert a small representative set into AI231 blueprints. Do not import all agents blindly.

## 9. References

- Upstream: https://github.com/msitarzewski/agency-agents
- Upstream README at pinned commit: https://github.com/msitarzewski/agency-agents/blob/8ae6164602c95ca78828b148b9052460ee426885/README.md
- AI231 factory contract: `docs/AI231_META_AGENT_FACTORY_V1.md`
- AI231 runtime integration: `docs/AI231_UPSTREAM_AGENT_RUNTIME_INTEGRATION_V1.md`
- AI231 blueprint verifier: `core/verify_contract.py`
