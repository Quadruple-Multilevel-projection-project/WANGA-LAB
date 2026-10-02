
# Maimonides Causal / Logical Extraction

## Current source set

- chapters/guide-i-28-regel-decomposition.md
- chapters/guide-i-69-causal-formal-decomposition.md
- foundations/guide-ii-26-preliminaries-formal.md

## Method

    Source
      ↓
    Lexical unit
      ↓
    Sentence
      ↓
    Relation
      ↓
    Sentence type
      ↓
    Inferential role
      ↓
    Causal topology
      ↓
    Unified configuration

## Non-negotiable distinctions

    Reference ≠ Proposition
    Attribution ≠ Assertion
    Cause ≠ Persistence-of-Cause
    Potential ≠ Actual
    Material Cause ≠ Formal Cause
    Remote Cause ≠ Near Cause
    "Last Form" ≠ natural material form
    "Form of Forms" ≠ the Aristotelian natural form rejected in the warning
    Final Cause ≠ simple efficient cause
    P26 assumption ≠ demonstrated conclusion

## Working source-navigation premise: Qafih

Qafih's edition may be used as a **source-navigation aid only**.

Allowed:
- bibliographic references and page/location pointers;
- references to external primary or historical sources;
- pointers that may lead to an additional source worth checking;
- source leads such as Aristotle, Avicenna/Ibn Sina, al-Farabi, Geonim, Talmudic sources, or other cited works.

Required procedure:
1. Treat the reference as a lead, not as proof.
2. Open and inspect the referenced source itself.
3. Record the source independently from Qafih.
4. If the source cannot be independently checked, mark the reference as UNVERIFIED_REFERENCE.

Do **not** use Qafih as an interpretive layer for the Maimonides / Ibn Tibbon corpus.

Ignore:
- Qafih's proposed links between chapters of the Guide;
- Qafih's explanations of why one chapter corresponds to another;
- Qafih's reconstruction of the Guide's internal architecture;
- Qafih's interpretation of Ibn Tibbon's intended meaning;
- Qafih's comments about how Ibn Tibbon should be corrected or understood.

These items must not enter the source graph, sentence semantics, chapter relations, or logical classification merely because Qafih proposes them.

Core rule:

    Qafih reference → locate candidate source → verify candidate source independently
    Qafih interpretation → do not import into the source model

This is an operational research rule. It does not constitute a historical judgment about Qafih's scholarship.

## Next construction target

Build a sentence grammar carrying together:

    Category
    + CauseType
    + CausalDepth
    + Mover/Moved
    + Potential/Actual
    + CauseEnvironment
    + FinalityDepth
    + InferenceRole

Status: SPECIFIED. This is an analytic formalization, not a claim that these symbols are Maimonides' own notation.
