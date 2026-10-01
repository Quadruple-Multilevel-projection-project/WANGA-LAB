# First-Order Logic

This directory is the sole home for the formal reconstruction layer named **First-Order Logic**.

## Three parts — relation is not identity

The labels **Part 1**, **Part 2**, and **Part 3** are primary.

The words **מיוחד** and **כולל** are used only as a **relational analogy supplied for understanding Part 3**. They do **not** define Part 1 or Part 2.

Therefore the system must **not** be represented as:

```text
Part 1 = מיוחד
Part 2 = כולל
```

Instead:

```text
Part 1 ─────────────── Part 2
          │
          │  supplied relation
          ▼
       Part 3
          │
          ▼
   שם משתתף / היחס
```

The Chapter 8 treatment of **מקום** supplies the comparison used to clarify the intended structure: a name may have a special and a general mode of application, and the participating-name mechanism concerns the relation between such modes. This analogy is **not an assignment of those labels to Parts 1 and 2**.

### Strict boundary

Until the source-grounded definition is established:

- Part 1 remains Part 1.
- Part 2 remains Part 2.
- Part 3 remains the reserved relation layer.
- No modern “particular/universal” equivalence is asserted.
- No downstream inference, contradiction, transformation, or dependency machinery is assigned to Part 3.

Modern first-order notation is a **FORMAL_MODEL**, not historical Maimonidean notation.

## Repository boundary

All First-Order Logic material belongs under `first-order-logic/`. Do not place it in `milaot-hahigayon/sentences/` or unrelated directories.

Status values include `FACT`, `RELATIONAL_ANALOGY`, `FORMAL_MODEL`, `HYPOTHESIS`, and `NOT_YET_VERIFIED`.
