# First-Order Logic

This directory is the sole home for the formal reconstruction layer named **First-Order Logic**.

## Three parts — source extraction before architecture

The labels **Part 1**, **Part 2**, and **Part 3** remain primary. Their source-grounded definitions must be extracted before assigning modern logical machinery.

The words **מיוחד** and **כולל** are used only as a **relational analogy supplied for understanding Part 3**. They do **not** define Part 1 or Part 2.

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

The Chapter 8 treatment of **מקום** supplies a comparison used to clarify the intended structure. It is not the “place of logic” and it does not turn Part 3 into a spatial category.

## Extraction target

The current research task is to extract the **linguistic-logical units** from the relevant Maimonidean material before imposing an architecture.

The working unit is:

> **מופע משמעותי ביחס** — a meaningful occurrence understood together with its relation/context.

It is therefore not merely a token and not merely a sentence.

Candidate extracted layers:

```text
שם / מילה
   ↓
מונח
   ↓
מובן
   ↓
נושא / נשוא
   ↓
יחס
   ↓
הבחנה
   ↓
צירוף
   ↓
סיבה
   ├── חומר
   ├── צורה
   ├── פועל
   └── תכלית
   ↓
שינוי / העתקה / גזירה
   ↓
מדרגה
   ↓
התכנסות
```

These are **extraction targets**, not claims that Maimonides himself presents this exact taxonomy.

### Source-grounding rule

Examples such as **עין**, **אריה**, **תפלה**, and the Chapter 8 discussion of **מקום** should be represented through their source relations and contexts, not reduced to a flat list of meanings.

```text
שם
├── נאמר על → עניין א
└── נאמר על → עניין ב
```

rather than:

```text
שם = [מובן א, מובן ב]
```

## Four causes

The four causes are a separate source-grounded structure that must be preserved:

```text
חומר
צורה
פועל
תכלית
```

They are not four competing answers. In the research model they are four causal aspects through which one and the same thing may be understood. Their exact role in the surrounding Maimonidean passages must be extracted from the sources rather than assumed.

## The circular / encompassing hypothesis

`HYPOTHESIS`: The relevant second-order structure may not be adequately represented as a single chain A → B → C → D, but may involve movement among meanings, relations, causes, and contexts until relations converge back on the thing under investigation.

This is a **research hypothesis**, not a statement that Maimonides explicitly formulated a “circular logic.”

## Strict boundaries

- Part 1 remains Part 1.
- Part 2 remains Part 2.
- Part 3 remains the reserved relation layer.
- **מיוחד / כולל** are not identities for Part 1 / Part 2.
- No modern “particular/universal” equivalence is asserted.
- “מקום” is not treated as the spatial location of logic.
- No downstream inference, contradiction, transformation, or dependency machinery is assigned to Part 3 before source extraction establishes it.
- Modern notation is a **FORMAL_MODEL**, not historical Maimonidean notation.

## Repository boundary

All First-Order Logic material belongs under `first-order-logic/`. Do not place it in `milaot-hahigayon/sentences/` or unrelated directories.

Status values include `FACT`, `RELATIONAL_ANALOGY`, `FORMAL_MODEL`, `HYPOTHESIS`, and `NOT_YET_VERIFIED`.