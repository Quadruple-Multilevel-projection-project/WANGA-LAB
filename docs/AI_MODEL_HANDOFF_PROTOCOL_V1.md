# AI Model Handoff Protocol v1

## Purpose
Enable multiple AI models and agents to work on AI Logic Factory without duplicating work, silently changing definitions or creating contradictory diagrams.

## 1. Shared source of truth
The GitHub repository is the shared artifact store. A model must fetch the current file before editing it. Conversation memory, pasted summaries and another model's report are not authoritative substitutes for the source.

Start at `AI_LOGIC_FACTORY_DIAGRAM_INDEX.md`.

## 2. Work assignment
Every task must specify:
- task ID;
- assigned model/agent;
- one primary layer (L1–L4);
- allowed files and paths;
- explicit exclusions;
- expected artifact;
- acceptance test;
- status and deadline, if relevant.

Avoid assigning two agents to edit the same file concurrently. If overlap is unavoidable, one agent is editor and the other reviewer.

## 3. Four-layer boundaries
- L1 Language & Contract owns definitions, Place, semantic relations and truth/evidence rules.
- L2 Analytics & Visualization owns visual inputs, transformations, pattern extraction and analyst review.
- L3 KRAKEN owns bounded composition, state transitions, workload admission and compute orchestration.
- L4 Orchestration & Product owns apps, agents, APIs, knowledge registries, workflow and telemetry presentation.

Cross-layer changes require an interface proposal and review by the owners of both layers. No layer may silently redefine another layer's vocabulary.

## 4. Evidence and status
Use only these labels:
- `EXPLICIT`: directly stated in a source.
- `INFERRED`: follows from structure but is not directly stated.
- `PROPOSED`: new design suggestion.
- `EXISTING`: artifact or implementation is present.
- `SPECIFIED`: design is documented.
- `NOT_YET_VERIFIED`: no adequate independent test evidence.
- `VERIFIED`: reproducible test evidence is linked.
- `SIMULATED`: result came from simulation/emulation.
- `ABSTAIN` / `HALT`: missing evidence, unresolved conflict or failed safety gate.

Never convert INFERRED or PROPOSED into VERIFIED without evidence.

## 5. Immutable distinctions
- 14 logic gates and 175 logic terms are not the 231 letter-pair gates.
- Visual resemblance is not semantic identity.
- Simulated compute is not physical QPU execution.
- A software frequency-domain transform is not proof of physical optical processing.
- A diagram edge is not proof of a live API or deployed integration.
- A KPI target is not a measured result.

## 6. Required handoff report

```text
TASK_ID:
MODEL / AGENT:
LAYER:
SCOPE:
FILES_OPENED:
FINDINGS:
  - [EXPLICIT / INFERRED / PROPOSED] statement — source path
STATUS:
CHANGES_MADE:
TESTS_RUN:
TEST_RESULTS:
UNRESOLVED_GAPS:
CONFLICTS:
NEXT_OWNER:
NEXT_ACTION:
ACCEPTANCE_CRITERION:
```

## 7. Change control
1. Fetch latest branch and target file.
2. Check for an existing artifact before creating a new one.
3. Edit only assigned paths.
4. Update diagrams and registry when their linked sources change.
5. Validate Markdown links and Mermaid syntax.
6. Commit with a descriptive message.
7. Report commit SHA and exact URLs.
8. Do not claim a change succeeded unless GitHub returns a successful commit result and the new file can be fetched.

## 8. Review policy
The author and verifier should be different agents for critical contracts, security boundaries, semantic validation and performance claims. If no independent verifier is available, report `NOT_YET_VERIFIED`.

## 9. Cooperation rule
Models should share findings and cite source paths, avoid status competition, avoid duplicating completed work and leave clear handoffs. The goal is cumulative, inspectable progress — not competing interpretations.