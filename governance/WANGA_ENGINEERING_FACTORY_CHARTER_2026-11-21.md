# WANGA-LAB — Engineering Factory Charter

Status: PROPOSED OPERATING CHARTER — branch review required
Date: 2026-11-21

## 1. Mission

WANGA-LAB is the engineering factory for the user's logic-based software language and its AI analytical-agent runtime. It designs, implements, integrates, tests, and maintains the algorithms and software infrastructure required by the program.

WANGA-LAB is not intended to duplicate universities, public research institutes, or external scientific laboratories. It does not create a parallel institution for general-purpose scientific research.

## 2. What WANGA builds

1. **Logic language and execution semantics** — syntax, formal representations, deterministic execution rules, state transitions, and compiler/interpreter components.
2. **Advanced algorithms** — logical analysis, relation processing, projection, comparison, consistency checking, state snapshots, and other algorithms explicitly specified by the architecture owner.
3. **Analytical AI agent** — the agent runtime that applies the logic language, requests evidence, analyzes bounded inputs, explains results, and returns traceable outputs.
4. **Processor and registry interfaces** — adapters and contracts for AI231, Majorana / Thinking Machine, ENC registries, and the 231-gate interface. Names and semantics remain subject to source verification; no unresolved constants or gate meanings may be invented.
5. **Integration and reliability** — APIs, orchestration, versioning, test harnesses, reproducible builds, monitoring, security boundaries, and independent verification.
6. **Engineering documentation** — executable specifications, interface contracts, architecture decision records, test evidence, and release notes.

## 3. What WANGA does not own

- It does not operate as a university or general scientific research institute.
- It does not replace external research organizations or claim their scientific authority.
- It does not independently define the research agenda of partner institutions.
- It does not claim that proposed processors, consciousness architectures, hardware, or performance targets are implemented until demonstrated by reproducible tests.
- It does not silently redefine the architecture owner's unresolved terms, values, or invariants.

Existing evidence, provenance, drift-forensics, and verification code may be retained where it directly supports engineering quality and system integrity. Such capabilities are engineering assurance services, not a mandate to expand WANGA into a research institute.

## 4. External research and university interface

A separate Global Research Liaison / Directorate coordinates external research relationships. Its responsibilities are:

- identify relevant universities, laboratories, and research organizations;
- issue bounded technical questions and research briefs;
- agree on deliverables, owners, schedules, and acceptance criteria;
- track progress and dependencies;
- receive papers, datasets, prototypes, and experimental results;
- verify provenance and route accepted findings to WANGA engineering teams.

WANGA provides technical requirements and evaluates whether delivered results satisfy engineering acceptance criteria. It does not impersonate the research partner or treat an unverified claim as a proven result.

## 5. Work intake and delivery contract

Every engineering task must contain:
- task ID and requesting system;
- problem statement and expected output;
- source documents and version references;
- owner and reviewer;
- dependencies and access permissions;
- acceptance tests and evidence required;
- estimated effort and target date;
- rollback or containment plan where applicable.

A task is complete only when its implementation, tests, review, and evidence are recorded. A passing unit test alone is not proof of system-level readiness.

## 6. Separation of duties

- **Architecture owner:** sets intended architecture, priorities, and unresolved decisions.
- **Engineering lead:** decomposes approved requirements and coordinates implementation.
- **Specialist agents / engineers:** implement bounded components within explicit permissions.
- **Independent verifier:** checks requirements, tests, provenance, and claimed outcomes; it must not approve its own work.
- **Global Research Liaison:** manages external research partners and institutional schedules; it does not override engineering verification.
- **Release authority:** approves deployment only after acceptance evidence and required independent review.

No role may silently change another role's authority or the canonical contracts.

## 7. Initial engineering workstreams

1. Logic-language specification and executable reference semantics.
2. Analytical-agent runtime and tool/permission contracts.
3. Algorithm library and deterministic test vectors.
4. AI231 / Majorana interface and state protocol.
5. ENC-MASTER and nine-registry data contracts, after C/Q/L source definitions are recovered.
6. 231-gate interface, preserving unresolved META and 231-vs-288 decisions as blocked items until authoritative source evidence resolves them.
7. CI, regression, integration, concurrency, replay, and independent verification.

## 8. Definition of done

A component is not called implemented merely because a directory, prompt, agent identity, workflow, or configuration file exists.

Required evidence:
- implementation exists on a named branch and commit;
- declared inputs, outputs, permissions, and failure behavior are documented;
- automated tests run and their output is retained;
- independent verification is recorded;
- integration tests demonstrate the component works with its dependencies;
- deployment status is stated accurately as proposed, tested, staged, or production.

## 9. Operating principle

**External institutions research. The Directorate coordinates. WANGA engineers. Independent audit verifies. The architecture owner sets direction.**

This charter changes WANGA's intended operating scope; it does not by itself prove that the listed capabilities have been implemented or deployed.
