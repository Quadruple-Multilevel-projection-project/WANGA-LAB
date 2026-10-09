# Business Pivot & First Logic Product — 2026-10-09

**Record type:** Consolidated project-state update  
**Scope:** Work discussed and advanced during 2026-10-08 to 2026-10-09  
**Status vocabulary:** BUILT / PROTOTYPED / TESTED / NOT_YET_VERIFIED

## 1. Commercial priority

The near-term commercial direction is a **catalogue/marketplace of task-specific AI logic packages** extracted, formalized, configured, and tested from the research corpus. Each package should state its task, inputs, outputs, operating boundaries, evidence requirements, configuration options, and verification status.

The immediate objective is not fundraising and not to recruit people into a multi-year training program. The immediate objective is to produce clear Hebrew research and business material, demonstrate concrete logic packages, and validate whether customers will pay for configured logic and execution.

Proposed commercial model:
- reusable base logic packages;
- paid configuration for a defined customer task;
- paid integration/execution where compute, tokens, or operational work are required;
- custom logic packages for customer-specific requirements.

Pricing, demand, and conversion remain **NOT_YET_VERIFIED** until supported by customer evidence.

## 2. Productization order

1. Logic Lab / task-specific logic packages — near-term commercial focus.
2. Demonstrate packages with repeatable examples and a small product catalogue.
3. AI Drift Forensics — later institutional direction, after sufficient demonstrated capability and evidence.

This ordering does not cancel WANGA-LAB's forensic research. It separates the near-term route to a sale from the longer-term institutional offering.

## 3. First interactive sample: AI Logic Auditor

**Product name:** AI Logic Auditor Demo  
**ProductOS project ID:** `8946d3a4-4c84-4a1f-b151-ac267809b82a`  
**GitHub sync:** configured target reported by ProductOS, but repository file availability and a successful push have not yet been verified.  
**Preview:** https://69bb8cc01894754ca7570cde42f7bb57.preview.bl.run

The prototype demonstrates source-grounded checks on three business examples:
- **Bout Nails:** compare price, treatment-duration wording, and unsupported durability claims.
- Marketing claim: detect an unjustified expansion from a small customer survey to the entire market and unsupported superiority language.
- Quote consistency: check arithmetic between line items and a stated total.

The UI shows source excerpts, the claim under review, a finding category, an explanation, and a report-copy action.

### Implementation status

- **BUILT:** Hebrew-first web UI, sample selector, editable source and claim fields, local deterministic rule checks, findings display, report-copy action.
- **TESTED:** production build completed successfully; local preview returned HTTP 200 and contained the expected sample UI.
- **PROTOTYPED:** rule-based demonstration only.
- **NOT_YET_VERIFIED:** detection quality, generalization to arbitrary documents, customer usefulness, security/compliance suitability, commercial demand.
- **NOT IMPLEMENTED:** external LLM connection, comprehensive logic engine, production deployment, customer data storage, independent benchmark.

The Bout Nails business and its prices are fictional demonstration data, not a claim about a real business.

## 4. Evidence discipline

The demo's rule checks must not be described as a general-purpose AI forensic engine. It demonstrates a narrow product concept: compare a claim against a supplied source, surface a possible mismatch, and preserve the evidence trail.

The labels `NOT_YET_VERIFIED`, `PROTOTYPED`, and `TESTED` must remain distinct. A successful software build does not establish detection accuracy.

## 5. Relationship to WANGA-LAB

WANGA-LAB remains the research and engineering repository for:
- evidence integrity and provenance;
- drift forensics and reconstruction;
- logic mining and logical-structure configuration;
- verification methods and reproducible fixtures.

The marketplace is a near-term productization path built from selected logic assets. It is not a replacement for the research repository and does not disclose protected Rational Logic implementation.

## 6. Immediate validation criteria

Before presenting the demo as a reliable commercial tool:
1. Build a labeled test set of correct claims, contradictions, unsupported claims, and meaning drift.
2. Record expected findings before running the tool.
3. Measure correct detections, missed findings, and false positives.
4. Compare with manual review or a simple baseline.
5. Document limitations and retain source-linked findings.
6. Validate customer demand with actual user feedback or a paid pilot.

**Current conclusion:** an interactive sample exists and passes a build check. It is a demonstrator, not yet a verified commercial product.

---
