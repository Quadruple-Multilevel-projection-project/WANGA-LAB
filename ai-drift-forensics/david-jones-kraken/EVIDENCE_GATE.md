# KRAKEN Evidence Gate

## Objective

Prevent the David Jones Box / KRAKEN architecture from being presented to a financial institution as physically validated before the underlying engineering claims have evidence.

## Gate sequence

`Requirement → Source → Configuration → Simulation → Test → Independent Verification`

For every configuration item record:

- source;
- exact hardware/model;
- assumptions;
- measured parameters;
- simulation parameters;
- test result;
- reproducibility information;
- reviewer;
- date;
- verification status.

## Banking presentation rule

The banking-facing package should separate three things:

### A. What exists
Documented hardware, software, repositories, measurements, and completed tests.

### B. What is configured
A concrete architecture that has an implementable engineering specification but may not yet be physically assembled.

### C. What is proposed
Future hardware, unvalidated mappings, or unresolved processor combinations.

This separation is mandatory for evidence integrity.
