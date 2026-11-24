# AI AGENT HANDOFF NOTICE

## Mandatory first read

Before any planning, coding, data modification, or interface change, every WANGA agent MUST read and accept:

1. `WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md` — the canonical WANGA semantic definition and mandatory four-application architecture.
2. `AI-AGENT-NOTICE.md` — the sequential logic, evidence, provenance, and repository-safety gates.

The semantic truth contract is the first governing semantic contract for every agent and downstream component contract. If an agent cannot accept or understand it, the agent must stop and report:

`BLOCKED — WANGA SEMANTIC CONTRACT NOT ACCEPTED OR NOT UNDERSTOOD.`

This repository is governed by the following sequential execution gates:

L1 — FIRST-ORDER STRUCTURAL LOGIC
↓
L2 — DERIVATION LOGIC
↓
L3 — RELATION / RULE VALIDATION
↓
EVIDENCE / PROVENANCE FILTER
↓
DETERMINISTIC OUTPUT FILTER

A later gate cannot repair an earlier failure. Do not skip gates.

## Evidence discipline

Maintain:

SOURCE → EXTRACTED → FORMALIZED → DERIVED → MAPPED → TESTED → VERIFIED

Never silently convert:
- SOURCE → FACT
- INTERPRETATION → FACT
- HYPOTHESIS → FACT
- MAPPING → IDENTITY
- SEMANTIC SIMILARITY → PROVENANCE
- CODE EXISTS → VERIFIED BEHAVIOR

## Unknown

If evidence or a required logical rule is missing:

NOT_YET_VERIFIED

If a determination cannot safely be made:

I DON'T KNOW.

Do not guess or use confidence language to conceal missing evidence.

## Contradictions

Preserve conflicting source statements and their provenance. Do not silently select one or manufacture a reconciliation.

## Source-internal claims

Metaphysical, philosophical, symbolic, or other source-internal claims must remain source-internal unless independent evidence establishes an external factual claim.

## Repository safety

Before modifying this repository:
1. Inspect the existing state.
2. Inspect relevant files, branches, issues, and PRs.
3. Identify the source supporting the change.
4. Make the smallest justified change.
5. Test the change.
6. Report only what actually happened.

Do not restart existing work, invent provenance, create duplicate tasks, or claim verification that did not occur.

## Stop condition

If the protocol is not understood, or required evidence/rules are missing:

BLOCKED — [category]: [exact issue]

Stop. Do not modify the repository.

## Required reporting

ACTION
SOURCE
TRANSFORMATION
EVIDENCE
RESULT
VERIFICATION
STATUS

Permitted status values:
BUILT / SPECIFIED / PROTOTYPED / TESTED / VERIFIED / PLANNED / HYPOTHETICAL / NOT_YET_VERIFIED / OPEN / BLOCKED

This notice is a handoff boundary, not an optional suggestion.

Canonical WANGA semantic contract:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/WANGA_SEMANTIC_TRUTH_CONTRACT_V1.md

Canonical agent notice:
https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/AI-AGENT-NOTICE.md
