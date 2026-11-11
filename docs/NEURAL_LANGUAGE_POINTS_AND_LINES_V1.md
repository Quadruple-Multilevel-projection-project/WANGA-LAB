# Neural Language V1 — Points and Lines

**Status:** SOURCE-REGISTERED / COMBINATORIAL LINKAGE ONLY  
**Version:** 2026-11-11  
**Canonical data:** [`research/data/NEURAL_LANGUAGE_POINTS_AND_LINES_V1.json`](../research/data/NEURAL_LANGUAGE_POINTS_AND_LINES_V1.json)

## Source boundary

This module records the supplied `NEURAL_LANGUAGE_POINTS_AND_LINES.txt.pdf` and the accompanying worksheet. It does not claim access to a hidden ChatGPT neural alphabet protocol. It is a project-defined, machine-readable representation of the source.

The governing source rule is:

> The root is prior. The letter is posterior. A gate is a relation between two letters. A path is a sequence of gates. Identity is kept by Node ID and Root. What is not defined remains null.

## Five roots

| Stable ID | Hebrew | English | Letters |
|---|---|---|---|
| `ROOT-THROAT` | גרון | THROAT | א ה ח ע |
| `ROOT-PALATE` | חיך | PALATE | ג י כ ק |
| `ROOT-TONGUE` | לשון | TONGUE | ד ט ל נ ת ר |
| `ROOT-LIPS` | שפתיים | LIPS | ב ו מ פ |
| `ROOT-TEETH` | שיניים | TEETH | ז ס צ ש |

These memberships are transcribed from Section 1 and repeated in Section 5 of the PDF. The root roles/functional meanings are not extended beyond what the source states.

## Letter identity and geometry

The registry contains 22 stable node IDs (`LET-001`–`LET-022`) in the existing repository's Hebrew-letter order. Each node has exactly one root assignment.

The PDF contains point-and-line diagrams for L01–L22 (pages 2–6). It does not provide a coordinate system, vector paths, normalized dimensions, or machine-readable geometry. Therefore:
- source page references are retained;
- exact vector coordinates remain `null`;
- names, transliterations, IPA, niqqud, dagesh and phonetic subgroups remain `null` in this source-derived registry unless separately sourced and reviewed;
- no ASCII approximation is promoted to exact geometry.

## Gate graph

The graph reuses the repository's existing K22 enumeration:
- 22 vertices;
- 231 unordered pairs of distinct letters: `C(22,2)=231`;
- 462 ordered pairs of distinct letters: `22×21=462`;
- no self-pairs;
- every unordered gate retains its two ordered transition IDs and reverse links.

Every gate now also carries the two endpoint node IDs and their root IDs. This is a structural join only. It does not define a gate's meaning, weight, operation, or execution behavior.

## Worksheet extraction

The XLSX contains ten rows under marks ו׳, ז׳ and ח׳. The rows are preserved as unresolved crosswalk records. The worksheet does not identify which of the 231 `GATE-###` records each mark denotes, nor does it identify endpoint letter pairs. Consequently `gate_id`, `letter_ids` and `formal_rule` remain `null`; no mapping is inferred.

## Explicitly undefined

`V1`, `V2`, gate payloads/weights, braiding, arithmetic on letters, entry/exit conditions, exact geometry coordinates, phonetic metadata, and processor/runtime behavior remain null or not defined. Null is not zero.

## Verification contract

The validator checks:
1. 22 unique letter nodes;
2. each letter occurs in exactly one of the five roots;
3. root membership equals the PDF transcription;
4. exactly 231 unordered gates and 462 directed transitions;
5. no self-pairs and no duplicate unordered pairs;
6. every vertex has degree 21;
7. every directed transition has a valid exact reverse;
8. each gate's root endpoints match its letter endpoints;
9. undefined fields remain null.

Passing these checks proves registry consistency only. It does not prove historical interpretation, phonetic correctness, neural behavior, or semantic gate operations.

## Provenance

- `NEURAL_LANGUAGE_POINTS_AND_LINES.txt.pdf`: root groups, point-line diagrams, connection hierarchy, null policy and source status.
- `DOC-20261111-WA0000.xlsx`: ten logical-term crosswalk rows, retained unresolved.
- `research/data/LETTER_GATE_MAP_231_V1.json`: pre-existing K22 pair and directed-transition enumeration.
