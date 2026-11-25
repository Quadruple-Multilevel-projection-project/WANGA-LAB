# Agent Convergence and Verification — 2026-11-21 Update
Date: 2026-11-21
Status: VERIFIED SOURCE REVIEW / ASSESSMENT — this is not a claim of WANGA deployment or external adoption.

## 1. LangGraph — durable orchestration
The current official LangGraph overview describes a low-level orchestration runtime built from shared state, nodes and edges. It supports deterministic and model-driven steps, persistence/checkpointing, resume after failures or pauses, streaming and human-in-the-loop inspection/editing. It explicitly does not prescribe prompts or a fixed agent architecture.
- Primary source: https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/overview.mdx
- Additional source: https://docs.langchain.com/oss/javascript/langgraph/durable-execution/

**Assessment:** useful for stateful orchestration and resumability; not evidence of a sandbox, network-egress denial, semantic correctness or autonomous authority.

## 2. OpenAI Agents SDK — tool governance and handoffs
Official SDK references expose agent definitions with tools, guardrails and handoffs, plus input/output guardrails and run-level tracing/guardrail controls. The Realtime guide documents tool-approval events that pause execution until a tool call is approved or rejected.
- Agent definition: https://openai.github.io/openai-agents-python/ref/agent/
- Guardrails: https://openai.github.io/openai-agents-python/ref/guardrail/
- Runner: https://openai.github.io/openai-agents-python/ref/run/
- Tool approvals: https://openai.github.io/openai-agents-python/realtime/guide/

**Assessment:** concrete developer interfaces exist for policy gates, tool approvals and traceable handoffs. They do not establish that a particular deployment has configured those controls correctly.

## 3. Hugging Face smolagents — restricted code execution
The official secure-code-execution guide documents a custom AST-based local executor with import allowlists, disabled submodule access by default, an elementary-operation cap and fail-closed handling of unsupported operations. The same documentation warns that no local Python sandbox is completely secure and recommends remote execution isolation for robust security.
- Primary source: https://huggingface.co/docs/smolagents/v1.19.0/en/tutorials/secure_code_execution

**Assessment:** an allowlisted interpreter is a useful defense-in-depth layer, not a substitute for process/container isolation, egress controls, resource limits and adversarial testing.

## 4. Website audit alternatives — scope and differentiation
- Google Lighthouse provides automated performance, accessibility, best-practice and SEO audits, runnable through Chrome DevTools, CLI or Node integration: https://developer.chrome.com/docs/lighthouse/overview
- Screaming Frog SEO Spider documents technical SEO crawling, export of titles/descriptions/headings, a free 500-URL crawl limit and a paid license for expanded functionality: https://www.screamingfrog.co.uk/seo-spider/user-guide/general/
- Semrush Site Audit documents 140+ on-page/technical checks, crawl-scope controls, JavaScript rendering options and scheduled re-audits: https://www.semrush.com/kb/31-site-audit

**Assessment:** a generic metadata/broken-link/performance audit is already well served by established tools. A defensible AI231 pilot must test a narrower wedge: evidence-linked public-claim consistency, provenance and source-version traceability, correct classification of dynamic routes, permission-gated remediation drafts and explicit unresolved states. No buyer demand or unique market advantage is verified.

## Comparative conclusion
| Layer | Demonstrated implementation | Remaining uncertainty |
|---|---|---|
| Orchestration | Stateful graph execution, checkpointing, pause/resume | No inherent sandbox or truth guarantee |
| Tool governance | Guardrails, approvals, handoffs and traces | Correct policy configuration in a specific deployment |
| Code execution | AST restrictions and allowlisted imports | Local sandbox escape/resource risk remains |
| Site auditing | Mature technical SEO/performance crawlers | Source-backed claim provenance and permission-aware remediation are not established by generic SEO checks |
| WANGA status | Draft blueprint and CI-tested contract | No configured runtime, live agent invocation or commercial validation |

## Implications for AI231/WANGA
1. Keep the Wix Evidence Auditor read-only and DRAFT / NOT_CONFIGURED.
2. Normalize root-relative static paths before classifying links; preserve dynamic routes as UNRESOLVED until a live route/API check.
3. Require exact tool approvals, audit records, sandbox isolation, egress denial and resource limits before any runtime activation.
4. Differentiate the revenue offer by evidence/provenance and claims review, not by generic SEO scoring.
5. Measure customer value and delivery cost before building a generalized platform.

## Evidence labels
- **VERIFIED:** the cited official documentation describes the stated implementation interfaces.
- **ASSESSMENT:** the five-layer comparison and implications for the WANGA design.
- **HYPOTHESIS:** the source-backed claims audit may be a differentiated service.
- **NOT_YET_VERIFIED:** external WANGA adoption, superior performance, customer demand, paid conversion and runtime isolation.
