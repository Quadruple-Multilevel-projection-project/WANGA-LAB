# TNRL: source story to executable kernel

The project is built as a compiler stack, not as a single prompt.

## Source model

The first three gates are treated as a source language:

1. **Gate 1 — Mishnah organization**: source classes, orders, sections, received material, derived law, decrees and customs.
2. **Gate 2 — Gemara/Talmud**: transmission, generations, teacher/student relations and the reasoning moves used to interrogate a proposition.
3. **Gate 3 — identity/aliases**: provenance and resolution of names, titles and source identities.

These source distinctions become machine data. They are not collapsed into one embedding.

## Kernel pipeline

`source -> ontology -> Talmudic operators -> typed IR -> FOL -> reasoning graph -> runtime`

The current implementation now has a textual boundary:

- `source`
- `term`
- `predicate`
- `assert` / `deny` / `unknown`
- `operator`

The compiler turns this into typed terms, predicates, propositions, FOL facts and reasoning nodes.

## Why the operator layer exists

The kernel does not treat reasoning as a flat list of true/false statements.

A question (`kushya`) can point to a proposed resolution (`terutz`); evidence (`reaya`) can support a proposition; rejection (`dehiya`) can attack a support path; contradiction (`stira`) is retained explicitly; distinction (`havdalah`) separates cases; source (`mekor`) records origin; dispute (`mahloket`) keeps alternatives; decision (`hachraa`) records a resolution.

This gives the neural model a symbolic target it can generate, validate and execute.

## Boundary to the higher language

The rational-logic language is intentionally **above** this kernel.

It is not compiled into the TNRL kernel. The Architect enforces that boundary. Later, the upper language will compile down to kernel operations in the same way a higher-level language compiles to a lower-level runtime.

## What is built now

- Typed IR and truth states
- FOL fact store with explicit contradiction
- Talmudic operator nodes
- Text parser
- Source/provenance declarations
- AST-to-IR/FOL compiler
- Reasoning graph
- Structural validator
- Architecture manifest/Architect

## Next construction layers

1. Source normalizer for the actual Halikhot Olam material.
2. Identity/provenance resolver.
3. Full grammar and typed AST.
4. Proof obligations and inference rules for each operator.
5. Runtime that executes validated reasoning graphs.
6. Neural bridge with constrained generation against the grammar/schema.
7. Upper rational-language compiler targeting this kernel.
