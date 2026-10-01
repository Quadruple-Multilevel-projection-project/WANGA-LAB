# First-Order Logic

This directory is the sole home for the formal reconstruction layer named **First-Order Logic**.

## Three-part structure

The three parts are not ordinary implementation phases. They are defined structurally:

```text
First-Order Logic
├── Part 1 — המיוחד
├── Part 2 — הכולל
└── Part 3 — השם המשתתף
              ↕
        המיוחד ↔ הכולל
```

The model takes the distinction established around **מקום** in Chapter 8 as the structural reference:

```text
מקום
├── כולל
└── מיוחד

Part 1 = המיוחד
Part 2 = הכולל
Part 3 = היחס/השם המשתתף המקשר את שניהם
```

### Boundary rule

**Part 3 must not be populated with transformations, contradiction handling, inference systems, or other downstream machinery until the relation of Part 3 has been explicitly defined.**

The repository therefore preserves the three parts as separate semantic layers. No material is moved from one part to another merely because it can be represented formally.

Modern first-order notation is a **FORMAL_MODEL** and is not attributed to Maimonides as historical notation.

## Repository boundary

Do not place First-Order Logic material in `milaot-hahigayon/sentences/`, the individual gates, or unrelated directories.

Source extraction remains source-bound. Formalization is stored here with provenance and status fields.

Status values include `FACT`, `FORMAL_MODEL`, `HYPOTHESIS`, and `NOT_YET_VERIFIED`.
