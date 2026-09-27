# AI Forensic Lab — Research & Publication Specification v1

Status: SPECIFICATION / INTEGRATION TARGET
Repository: Quadruple-Multilevel-projection-project/WANGA-LAB

## Purpose

AI Forensic Lab is the proposed public research surface for documenting AI drift investigations as reproducible evidence work.

The lab separates:
- source material,
- observation,
- evidence,
- verification,
- finding,
- claim,
- publication.

It does not treat a published Wix page as the source of truth. GitHub remains the technical source of code, schemas, workflows, evidence registries, and architecture contracts.

## Core forensic chain

PERSON
→ INSTITUTION
→ PROJECT
→ QUESTION
→ METHOD
→ EXPERIMENT
→ DATASET
→ OBSERVATION
→ EVIDENCE
→ VERIFICATION
→ REPLICATION
→ FINDING
→ CLAIM
→ RUN
→ SNAPSHOT
→ NODE
→ PUBLICATION

## Forensic operating model

1. Define the question and boundary.
2. Identify the source and retrieval location.
3. Record the observation without silently interpreting it.
4. Preserve provenance and content hashes where applicable.
5. Separate direct evidence from inference and hypothesis.
6. Run drift/comparison checks.
7. Verify structural claims before publication.
8. Publish only validated material to the public Wix surface.

## Current architectural alignment

The repository already contains:
- AI Drift Forensics / Global Drift Network structures.
- evidence and provenance concepts.
- verification layers.
- a GitHub-to-Wix publication/integration architecture.
- runtime/authentication contracts for external services.

The repository architecture explicitly assigns Wix to publication/external integration and GitHub to technical source of truth.

## Fourth-neural-logic research track

This lab may document research into a proposed fourth/neural logic, but the label is treated as a research hypothesis/architecture term rather than an established scientific fact.

The current research axis distinguishes:
- linear relations: separation, order, inference;
- circular relations: scopes, contexts, structures returning to themselves;
- connecting relations: relations that connect separation and scope and investigate why/how they connect;
- proposed fourth/neural layer: orchestration of distinctions, relations, evidence, context, and changing system state.

No fixed single hierarchy is assumed. Relations remain situation-dependent and must be justified by source evidence.

## Source fidelity rule

Claims about Maimonides, Abraham Abulafia, Sifra de-Tzeniuta, the Ari, or other historical sources must preserve the distinction between:
- verified source text,
- direct inference,
- analytical interpretation,
- hypothesis,
- unknown.

The forensic lab must not turn an architectural analogy into a historical attribution.

## Sifra de-Tzeniuta / Lurianic research boundary

The current project question concerns the extraction of structural/heuristic rules from the source tradition.

Research must distinguish:
- Sifra de-Tzeniuta as the dense textual source,
- later Lurianic systematization as a separate historical layer,
- Abulafia's letter-combination method as a separate methodological system.

A shared structural analogy is not, by itself, evidence of historical dependence.

## Publication target

Wix surface name:
AI Forensic Lab

Proposed public sections:
- Investigations
- Evidence
- Verification
- Drift Forensics
- Research Methods
- Source Registry
- Architecture
- Research Notes

## Non-claims

This document does not claim:
- that the Wix site already implements a forensic backend;
- that a fourth logic is scientifically established;
- that Sifra de-Tzeniuta is historically derived from Abulafia;
- that the Ari's later system is identical to the original text;
- that a local or simulated computation proves physical/empirical validity.

## Integration principle

Source → Extraction → Provenance/Hash → Structural Mapping → Verification → Evidence → Publication

Publication is downstream of verification.
