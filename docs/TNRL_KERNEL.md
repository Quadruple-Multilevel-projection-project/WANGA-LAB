# TNRL Kernel v0.1

The kernel is the executable/compiler boundary for the Talmudic neuro-symbolic language. It is deliberately below the higher rational-logic language.

## Layer order

Source -> Ontology -> Talmudic Operators -> Typed IR -> FOL -> Runtime.

The Talmudic layer supplies direction-of-thought operators: קושיא, תירוץ, ראיה, דחייה, סתירה, הבחנה, מקור, מחלוקת, הכרעה. These are represented as typed graph operations, not unconstrained prose.

## Separation rule

rational_logic is an external upper layer. The kernel architect rejects it when compiling the kernel contract so that the boundary remains explicit.

## Provenance

Every proposition may carry provenance identifiers. Contradictory assertions are retained as contradicted rather than silently discarded.

## Status discipline

BUILT / SPECIFIED / TESTED / VERIFIED remain distinct engineering states.
