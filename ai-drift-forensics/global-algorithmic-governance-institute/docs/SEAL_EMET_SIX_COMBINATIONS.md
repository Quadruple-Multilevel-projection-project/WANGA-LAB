# חותם אמת — Six Seals / Six Combinations

Status: **EXTRACTED / NOT_YET_VERIFIED AS ENGINEERING WEIGHTS**

## Source extraction

Sefer Yetzirah, Gra version, 1:13 states that three letters are selected "in the mystery of the three mothers אמש" and are used to seal six extremities. It then assigns one permutation of the three letters to each of the six directions.

The six directions and combinations in this version are:

| Source index | Direction | Hebrew direction | Combination |
|---:|---|---|---|
| 5 | Above | רום / למעלה | יהו |
| 6 | Below | תחת / למטה | היו |
| 7 | East | מזרח / לפניו | ויה |
| 8 | West | מערב / לאחריו | והי |
| 9 | South | דרום / לימינו | יוה |
| 10 | North | צפון / לשמאלו | הוי |

Source: Sefer Yetzirah, Gra version 1:13 (Sefaria).

## Exact combinatorial structure

Base symbols:

`J = י`, `H = ה`, `V = ו`

Number of distinct permutations:

[
|S_3| = 3! = 6
]

The six permutations are exactly:

`יהו, יוה, היו, הוי, ויה, והי`

No repeated symbol occurs inside a seal. Each seal therefore corresponds to one element of the permutation group `S3`.

## Positional encoding

The source labels the six seals with the ordinal sequence:

`5, 6, 7, 8, 9, 10`

These are **source indices / positional labels**, not source-defined probability weights.

For engineering use, maintain two separate fields:

- `source_index` = 5..10
- `weight` = NOT_DEFINED_BY_THIS_SOURCE

Do **not** convert 5..10 into probability weights without an explicit derivation and a separate status label.

## Emet / אמת

The phrase "חותמו של הקב"ה אמת" is cited in later Jewish literature, including the Shelah, which then connects the seal of אמת to the six extremities and the six permutations of יהו.

Arithmetic identity:

[
גימטריה(אמת)=1+40+400=441=21^2
]

This equation is a direct arithmetic derivation; it is not being asserted here as the textual derivation of Sefer Yetzirah itself.

## The "מקום אתי" layer

Sefer Yetzirah 1:8 says that when speech/thought "runs", it should return "למקום". The Gra commentary on the Wikisource page explains this as returning to the known/appropriate place, including the reading "הנה מקום אתי".

For the engineering model this can be represented as a **return-to-reference operator**:

`RETURN(x) → REFERENCE`

This is an engineering abstraction, not a claim that the source itself defines a software operator.

The important structural distinction is:

`SIX_SEALS = directional/permutation state`

`RETURN_TO_PLACE = reference/reset behavior`

They must not be merged into a single weight until further source extraction establishes the relation.

## Next extraction gate

Before generating the first-order logic layer, extract the additional requested source families and compare:

1. exact seal permutations;
2. direction assignments;
3. source indices;
4. letter identities;
5. ordering differences between textual versions;
6. any explicitly stated numerical relations;
7. any additional constraints associated with "מקום אתי".

Only after that comparison should the first-order predicates be generated.


## Variant-control requirement

The six permutations are invariant as a set, but secondary sources can present them in different textual orders or pair them to directions differently.

Examples:

- Gra version 1:13 (Sefaria): `יהו, היו, ויה, והי, יוה, הוי` mapped to above, below, east, west, south, north respectively.
- *Otzar Eden HaGanuz* lists the six seals in the sequence `יהו, יוה, הוי, היו, ויה, והי` without using that same directional sequence.

Therefore the canonical machine record must contain:

`source_version + source_index + direction + combination`

and must never silently merge different textual orders.

## Weight-slot mathematics

Define the six source positions as a six-dimensional weight vector:

[
W = (w_5,w_6,w_7,w_8,w_9,w_{10})
]

At this extraction stage:

[
w_5,ldots,w_{10} ;=; 	ext{UNASSIGNED}
]

The source supplies the six positional slots, not numeric resonance/probability values.

Each seal can be encoded as a basis vector:

[
e_i in mathbb{R}^6,qquad iin{5,ldots,10}
]

and the weighted state can later be represented as:

[
X = sum_{i=5}^{10} w_i e_i
]

No normalization constraint such as (sum_i w_i=1) is imposed yet; that would be an engineering choice requiring a later specification.

## Permutation-matrix representation

For the ordered symbols ((י,ה,ו)), each seal is also a (3	imes3) permutation matrix (P_pi), where (piin S_3).

Thus the minimal structural object is:

[
Seal_i = (source_index_i, direction_i, pi_i, P_{pi_i}, w_i)
]

with `w_i` unassigned at this stage.

This representation is the handoff boundary for the next First-Order Logic layer.
