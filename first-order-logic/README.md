# First-Order Logic

This directory is the sole home for the formal reconstruction layer named **First-Order Logic**.

## Scope

This is a formal modeling layer derived from source material. Modern first-order notation is a **FORMAL_MODEL** and is not attributed to Maimonides as historical notation.

```text
First-Order Logic
├── part-1  — Logical Units
├── part-2  — Relations and Inference
└── part-3  — Transformations, Contradiction, and Dependencies
```

## Boundary

Do not place First-Order Logic material in `milaot-hahigayon/sentences/`, the individual gates, or unrelated directories.

Source extraction remains source-bound. Formalization is stored here and keeps provenance fields such as:

- source_id
- source_text
- logical_form
- relation_type
- dependency
- status
- notes

Status values must distinguish source fact from reconstruction, including `FACT`, `FORMAL_MODEL`, `HYPOTHESIS`, and `NOT_YET_VERIFIED`.
