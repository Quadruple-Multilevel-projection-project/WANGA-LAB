# Rational Logic Linguistic Evidence Mesh V1

## Why this layer exists

The Rational Logic runtime cannot safely be built from a flat list of Hebrew logic words.

The substrate must represent:

`surface form -> lemma -> sense -> derivation -> semantic relation -> logical role -> rule candidate`

Every edge must retain its evidence source and extraction method.

## Source mesh

Initial adapters:

1. **Sefaria** — structured Jewish texts and interconnections. Its current API provides text retrieval and structured references; documented endpoints can be accessed without API keys. citeturn602792search3turn602792search5
2. **National Library of Israel** — Search API for discovery and IIIF Presentation/Image APIs for digital objects. The Search API requires an API key; digital-object access may be limited by rights. citeturn135254search1turn135254search4turn135254search7
3. **MediaWiki/Wiktionary-compatible source adapter** — for lexical discovery where the source's API and reuse conditions permit it. Wikimedia documents a standard API model for MediaWiki installations. citeturn602792search1
4. **Open Library** — bibliographic discovery and work/edition lookup. Open Library explicitly says its public APIs are not intended to act as a bulk third-party data backend; permitted bulk acquisition should use its data-dump channels instead. citeturn602792search2turn602792search6

This is a source mesh, not a claim of unrestricted access to every library.

## Specialist agents

### LEXICOGRAPHER
Finds candidate terms, definitions, variants and citations.

### MORPHOLOGIST
Builds lemma/variant and derivational edges. It must distinguish:
- inflection
- derivation
- composition
- semantic extension
- logical transformation

### SEMANTICIST
Builds sense identity and relations:
- synonymy
- opposition
- hypernymy/hyponymy
- homonymy/polysemy
- contextual sense

### LOGIC_PHILOLOGIST
Maps language to logical function, including:
- term / predicate / subject
- quantity / quality
- negation
- proposition
- premise / conclusion
- implication / opposition
- genus / species / difference
- syllogistic role

### EVIDENCE_AUDITOR
Checks source identity, extraction method, record digest, conflicting readings and evidence status.

## First corpus

The first corpus should begin with *Milot Ha-Higayon* and then expand to commentaries and dictionaries. A public transcription is available online, and the National Library of Israel catalog identifies historical printed editions and manuscripts of the work. citeturn735865search0turn735865search6

A 2021 academic publication also documents an anonymous commentary on *Milot Ha-Higayon*, demonstrating that commentary/manuscript layers are themselves research sources rather than merely translations. citeturn735865search35

## Evidence rule

The system must never convert:

`not found`

into:

`does not exist`.

Likewise:

`agent inferred relation`

is not:

`source-established relation`.

The evidence graph therefore distinguishes source fact, extracted fact, inferred edge and verified rule.

## Data flow

```
SOURCE DISCOVERY
    |
    v
RETRIEVAL + RIGHTS CHECK
    |
    v
SEGMENT / NORMALIZE
    |
    +--> LEXICOGRAPHER
    +--> MORPHOLOGIST
    +--> SEMANTICIST
    +--> LOGIC_PHILOLOGIST
    +--> EVIDENCE_AUDITOR
    |
    v
CROSS-SOURCE ALIGNMENT
    |
    v
CONFLICT GRAPH
    |
    v
LEXICAL + DERIVATIONAL + LOGICAL KNOWLEDGE GRAPH
    |
    v
RATIONAL LOGIC COMPILER
```

## Ten-day implementation target

This is a work estimate for the software/research scope, not a completion guarantee:

**Days 1–2:** source adapters, corpus registry, provenance model  
**Days 3–4:** lemma/variant and derivation graph  
**Days 5–6:** semantic relation graph + contradiction preservation  
**Days 7–8:** logical-role extraction and rule-candidate representation  
**Day 9:** deterministic cross-source reconciliation + audit hashes  
**Day 10:** test corpus, replay, verification, and interface contract to Rational Logic runtime

The first ten days build the linguistic substrate. They do not claim that the full Rational Logic engine is already implemented.

## Status

SPECIFIED -> PROTOTYPED
