# Plugin Configuration Factory — Research Protocol V1

Status: METHOD SPECIFICATION / NO EMPIRICAL RESULTS CLAIMED.

## Research question
Which plugin, MCP, agent-skill, provider and nested-configuration arrangement performs a declared task most effectively under stated constraints?

There is no universal best configuration. Every comparison is task- and environment-scoped.

## Experimental unit
An experiment compares one immutable task/input snapshot, one baseline, one or more candidate configuration graphs, pinned component/provider versions, equivalent test conditions where possible, repeatable cases and a recorded execution environment.

## Metrics
| Dimension | Example measurements |
|---|---|
| Capability fit | required capabilities covered / missing |
| Task outcome | success, partial success, failure, abstention |
| Reliability | completion rate, error classes, retry rate |
| Performance | p50/p95 latency, throughput |
| Cost | API cost, compute, storage, network |
| Security | granted scopes, exposed data classes, unresolved findings |
| Portability | successful export/import and provider substitution |
| Complexity | component count, edges, setup steps, maintenance events |
| Observability | trace coverage, provenance completeness, reproducibility |
| Language traceability | source-term references resolved, unresolved mappings preserved |

Record raw values and test context. Do not combine dimensions into a weighted score unless an explicit policy is approved and weights have a traceable source.

## Comparison procedure
1. Freeze task, source snapshot and evaluation conditions.
2. Validate each configuration against the JSON schema.
3. Check unique IDs, references, interface contracts and unbounded cycles.
4. Check least privilege, secret references, data-flow boundaries and approval requirements.
5. Run baseline and candidates on the same test set.
6. Record outputs, errors, costs, latency and environment.
7. Repeat to expose variability; state sample size and limitations.
8. Compare trade-offs; retain failures and negative results.
9. Run provider substitution/exit tests where portability is claimed.
10. Have an independent verifier inspect evidence and status transitions.

## Evidence statuses
- SPECIFIED: documented but not executed.
- TESTED: identified test executed and output retained.
- VERIFIED: defined verification criteria passed with reproducible evidence.
- ASSESSMENT: reasoned interpretation of available evidence.
- HYPOTHESIS: proposed explanation or expected outcome.
- UNRESOLVED: insufficient or conflicting evidence.
- BLOCKED: prerequisite or safety gate failed.

## Minimum experiment record
Store experiment_id, timestamp, task_id, immutable input reference, baseline/candidate config IDs, component versions, environment, procedure, raw outputs, metric values, errors, evidence references, reviewer, result status and limitations.

## Prohibited shortcuts
- Do not compare candidates on different task inputs and call it a performance win.
- Do not equate a successful API connection with task effectiveness.
- Do not treat marketing claims as proof of runtime behavior.
- Do not invent costs, limits, permissions, endpoints or capabilities.
- Do not hide failed runs or select only favorable results.
- Do not promote proposed term-to-configuration relations to VERIFIED without source evidence.


## Action signature
Timestamp=2026-11-20T00:59:46.207438+00:00
Contract_Start_Time=2026-11-16T05:28:32+00:00
Action_ID=ACT-20261120-PLUGIN-CONFIGURATION-FACTORY-001
SHA256=eb3bce9a13961a119d17dab98525364f68085c7eff0f2cc0fbd8adc69f7d2cdb
