# WANGA-LAB — MODEL MEMORY UPDATE PROTOCOL V1

## Purpose

Provide a durable, auditable bridge between project state in GitHub and the model's working-memory instructions.

## Principle

GitHub is the technical source of truth. Significant verified project-state changes generate a memory-update event/proposal.

This protocol does not falsely claim that a GitHub repository directly mutates ChatGPT persistent memory. It creates the durable artifact from which the model can update its active working context when the environment exposes that capability.

## Trigger Classes

- NEW_PROJECT
- ARCHITECTURE_CHANGE
- STATUS_CHANGE
- VERIFICATION_COMPLETED
- DEPENDENCY_CHANGE
- ROLE_CHANGE
- TERMINOLOGY_CORRECTION
- PRIMARY_BACKUP_BOUNDARY_CHANGE
- MEMORY_RULE_CHANGE

## Required Event

Each event should contain:

- timestamp
- source repository
- source path or commit
- change summary
- evidence
- affected project(s)
- proposed memory delta
- verification state
- review state

## Processing

GitHub state
→ detect significant change
→ collect evidence
→ create memory-update proposal
→ classify
→ review
→ incorporate into active working memory
→ record resulting state

## Operating Principle

The technical executor performs the detection, evidence collection, classification and proposal construction. The user supplies direction, capital and resources.

## Periodic Review

Generate periodic memory-maintenance proposals from accumulated project changes.

Never silently overwrite established memory. Preserve history and record the reason for each substantive change.
