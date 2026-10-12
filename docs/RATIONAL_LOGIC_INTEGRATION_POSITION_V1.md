# Rational Logic Integration Position V1

Status: ARCHITECTURAL RESERVATION / NEXT-MONTH PRIMARY WORK
Version: 1.0.0

## 1. Purpose

The published WANGA research architecture contains a Rational Logic research direction that is not yet formalized as a machine-readable runtime layer. This document therefore does not claim that the Rational Logic engine already exists.

It reserves a first-class architectural position for it and defines how it will complement, constrain, and learn from the existing operational architecture.

## 2. Current position

Rational Logic is not another agent framework and not another global orchestrator.

Its future role is a formal reasoning layer that can:
- represent premises, rules, relations, constraints, contradictions, and conclusions;
- distinguish observation from inference;
- test whether an inference follows from declared premises;
- expose invalid or underspecified reasoning;
- provide machine-checkable acceptance conditions to agents and managers;
- receive verified evidence from WANGA and return formal reasoning results.

## 3. Bidirectional relationship

The relationship is intentionally two-way.

WANGA -> Rational Logic:
- verified evidence;
- provenance;
- observations;
- task context;
- model outputs;
- detected conflicts;
- drift findings.

Rational Logic -> WANGA:
- formal constraints;
- inference results;
- contradiction findings;
- missing-premise findings;
- rule/acceptance checks;
- reasoning status;
- verification requirements.

Neither side silently becomes the authority of the other.

Repository evidence remains the source of implementation truth. Rational Logic becomes a formal reasoning authority only over propositions that are represented inside its declared logic.

## 4. Proposed integrated flow

INTAKE
 -> NORMALIZE
 -> EVIDENCE
 -> RATIONAL REPRESENTATION
 -> RULE / RELATION EVALUATION
 -> MODEL / AGENT WORK
 -> RATIONAL CHECK
 -> VERIFICATION
 -> NTM ESCALATION
 -> WORK MEMORY
 -> FOLLOW-UP

For tasks that do not require formal reasoning, the Rational Logic stage may be bypassed explicitly and recorded as NOT_REQUIRED.

## 5. Interaction with the external agent patterns

The OpenAI Agents SDK, Google ADK, AutoGen and LangGraph patterns integrated into WANGA remain execution/orchestration patterns.

Rational Logic supplies a different function:

agent frameworks = coordination and execution patterns
Rational Logic = formal reasoning and consistency layer
WANGA Global Work Manager = global work coordination
Evidence/Drift = empirical verification layer
NTM = high-level cognitive escalation and synthesis layer
Work Memory = durable state/history

This separation prevents framework features from being mistaken for reasoning correctness.

## 6. Critical design rule

A model response is not a logical proof merely because an agent framework successfully executed it.

The future Rational Logic layer must be able to say:
- SUPPORTED
- NOT_SUPPORTED
- CONTRADICTED
- INSUFFICIENT_PREMISES
- UNDEFINED
- OUT_OF_LOGIC_SCOPE

These are proposed statuses and must be formally specified before runtime use.

## 7. Next-month work boundary

The primary next-month work is to formalize the Rational Logic layer itself:
1. define the logical language;
2. define syntax and semantics;
3. define proposition/rule/relation objects;
4. define inference and contradiction semantics;
5. define proof/evidence references;
6. define uncertainty and incomplete-premise handling;
7. define interfaces to DMA, Global Work Manager, Evidence, NTM and Work Memory;
8. create executable tests and counterexamples;
9. determine which parts are deterministic and which require bounded model assistance.

Until these are completed, no production claim is made for Rational Logic.

## 8. Architectural consequence

The integrated system should be treated as a coupled architecture rather than a linear stack:

Operational plane:
WANGA OS -> Global Work Manager -> Model Fabric -> DMA -> Runtime

Epistemic/verification plane:
Evidence -> Drift Forensics -> Verification -> Rational Logic

Cognitive plane:
Rational Logic <-> NTM

Memory plane:
Work Memory + provenance + bridge events

Publication plane:
Wix -> public research/architecture surface

The planes influence each other through explicit contracts rather than hidden state.

## 9. Core research hypothesis

The important research question is not whether Rational Logic can replace agents.

The question is whether a formal reasoning layer can make a heterogeneous multi-model system more auditable, contradiction-aware, reproducible, and controllable by placing explicit logical constraints around model-generated work.

This remains a hypothesis until experimentally validated.


## 2026-10-12 — Boundary to the letter-weight mathematical layer

A 79-page source-extraction document has been reviewed. It provides structured first-order extraction of selected passages from *Etz Chaim* and 28 units (`S-08-001…S-08-028`) for *Guide for the Perplexed* I:8. In the I:8 extraction, the document explicitly defers the second logic until the first extraction is closed.

This is useful as a source-grounded input format for a future formal-reasoning interface, but it does not define the four mathematical-weight layers or their formulas, an invertible text/math representation, the 231-gate runtime, or verified empirical results.

**Integration boundary:** Rational Logic must not silently infer the weight-layer definitions from sentence-role fields. The following are distinct:
- four roles used to extract a sentence (subject, predicate, internal participant, logical connective/relationship);
- three proposed computational layers in the separate architecture draft;
- four logical-mathematical weight layers associated with letter interpretations;
- the provenance distinctions source / extraction / interpretation / engineering hypothesis.

Until the four weight-layer definitions are recovered from research sources and given explicit contracts, Rational Logic may accept only source-linked structured propositions and relations from the extraction layer. The weight-engine interface remains **NOT_SPECIFIED / NOT_YET_VERIFIED**.

Source audit: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/research/SOURCE_AUDIT_79_PAGE_LOGIC_EXTRACTION_2026-10-12.md

## 2026-10-12 — Five-forward / five-return interface boundary

The proposed architecture is specified as five forward-processing layers and five return stages. Until implementation contracts exist, these are functional stages rather than assumed separate neural networks. The return path should expose traceability, constraint results, decoding/reconstruction results, and explicit failure states.

The four logical-mathematical weight layers associated with letter interpretations are a distinct mechanism. Rational Logic must not infer their missing formulas from the five processing layers or from the four sentence-role fields. It should receive typed, source-linked records only after the weight-layer schema is defined.

Canonical review: https://github.com/Quadruple-Multilevel-projection-project/WANGA-LAB/blob/main/docs/FIVE_FORWARD_FIVE_RETURN_LOGIC_ARCHITECTURE_REVIEW_V1.md
