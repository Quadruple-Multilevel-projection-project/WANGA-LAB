# First-Order Logic

This directory is the sole home for the formal reconstruction layer named **First-Order Logic**.

## Three-part structure

The three parts must **not** be read as the ordinary modern opposition “particular vs universal.” The terms **מיוחד** and **כולל** are retained as source-derived structural labels pending a fuller definition from the logic text and the Chapter 8 discussion of participating names.

```text
Part 1 → המיוחד
Part 2 → הכולל
Part 3 → השם המשתתף / היחס בין אופני ההחלה
```

The Chapter 8 reference to **מקום** is the structural anchor, but it does not by itself exhaust the meaning of the three-part system.

```text
מקום
   ↓
אופני ההחלה: מיוחד / כולל
   ↓
שם משתתף
   ↓
הקשר בוחר את העניין המתאים
```

Therefore:

- Part 1 is not simply “an individual object.”
- Part 2 is not simply “a universal class.”
- Part 3 is not yet defined as a generic inference or transformation layer.

### Boundary rule

**Do not populate Part 3 with transformations, contradiction handling, inference systems, dependency graphs, or other downstream machinery before its source-grounded relation has been explicitly defined.**

Modern first-order notation is a **FORMAL_MODEL** and is not attributed to Maimonides as historical notation.

## Repository boundary

Do not place First-Order Logic material in `milaot-hahigayon/sentences/`, the individual gates, or unrelated directories.

Source extraction remains source-bound. Formalization is stored here with provenance and status fields.

Status values include `FACT`, `FORMAL_MODEL`, `HYPOTHESIS`, and `NOT_YET_VERIFIED`.
