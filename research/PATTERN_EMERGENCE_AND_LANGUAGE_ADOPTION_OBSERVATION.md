# Pattern Emergence and Language Adoption Observation

**Project:** MAKOM / WANGA-LAB  
**Priority:** Primary active observation workstream  
**Status:** Protocol specification — data collection not yet established  
**Scope correction:** The research target is **similar patterns**, not similar agents, and it is **not drift measurement**.

## 1. Research question

Can we observe the appearance, recurrence, relation, possible propagation, and adoption of similar structural patterns across outputs produced by one or more deep-network systems, and record when each pattern first appears in accessible evidence?

The study begins by defining and producing candidate patterns that can be recognized consistently. It then searches dated, source-identifiable material for occurrences and examines whether occurrences are related. Finally, it measures whether and how the new symbolic-descriptive language is used in those occurrences.

Similarity does not prove copying; chronology does not prove influence; language use does not prove understanding.

## 2. Corrected object of observation

The unit of observation is a **pattern occurrence** in a traceable artifact (prompt, response, document, code, diagram description, or other permitted record). An occurrence is not an agent. A system/model/source is metadata describing where the occurrence was observed.

A pattern is represented first in the project's symbolic-descriptive vocabulary: terms, distinctions, relations, boundaries, and ordering. Visual lines, points, letterforms, or graph notation do not by themselves make the representation mathematical.

## 3. Work sequence

### Phase A — Produce reference patterns
1. Extract candidate patterns from existing project observations and source artifacts.
2. Preserve original wording and source; create a separate normalized description for comparison.
3. Record distinguishing relations and boundary conditions in ordinary symbolic language.
4. Assign a stable pattern_id only after the candidate is explicitly defined.
5. Keep ambiguous candidates as CANDIDATE or NULL; do not force a match.

### Phase B — Find occurrences
1. Search available dated corpora, repository history, published material, and authorized model outputs.
2. Record the earliest **observed** occurrence, not an assumed creation time.
3. Distinguish artifact creation time, publication time, capture time, and first-seen time.
4. Retain exact excerpts or stable source references.
5. Record search coverage and blind spots. Absence from searched sources is not proof of nonexistence.

### Phase C — Compare and relate occurrences
For each pair, record shared terms; shared relations and ordering; shared boundary/termination behavior; differences and missing components; source and temporal proximity; and evidence of an explicit transmission path, if any.

Relationship labels:
- STRUCTURAL_SIMILARITY — shared structure observed.
- PARTIAL_RESEMBLANCE — some features overlap.
- SHARED_SOURCE_EVIDENCE — a common source is documented.
- TRANSMISSION_EVIDENCE — a traceable path of transfer is documented.
- INDEPENDENT_ORIGIN_POSSIBLE — independent emergence remains possible.
- UNRESOLVED — evidence is insufficient.

Do not label a relation as propagation merely because two patterns look alike or one is older.

### Phase D — Measure use of the new language
Measure adoption at the level of documented pattern occurrences, not presumed internal cognition. Track exact use of defined terms; correct use of defined relations; reuse of boundary/stop distinctions; consistency across multiple outputs; and whether the language was explicitly supplied in the prompt or source.

Separate PROMPTED_USE from UNPROMPTED_OBSERVED_USE. Unprompted use requires evidence that the relevant vocabulary or definition was not present in the immediately available prompt/context; do not infer this when context is incomplete.

## 4. Timestamp model

Never collapse these timestamps:
- artifact_created_at — source-declared creation time;
- published_at — publication time;
- captured_at — when this project collected the artifact;
- first_seen_at — earliest verified observation in the searched corpus;
- timestamp_precision — exact / date-only / estimated / unknown;
- timezone — original timezone or unknown.

If a source has no reliable timestamp, leave the value NULL and state why. Repository commit time is not necessarily the time a pattern was first conceived.

## 5. Workbook / data schema

### PATTERNS
pattern_id, original_description, normalized_description, distinguishing_terms, relations, boundary_conditions, source_reference, definition_status, notes.

### OCCURRENCES
occurrence_id, pattern_id, source_id, artifact_type, verbatim_excerpt_or_pointer, artifact_created_at, published_at, captured_at, first_seen_at, timestamp_precision, timezone, context_available, verification_status.

### SOURCES
source_id, source_type, model_or_system_label, repository_or_url, artifact_identifier, version_or_commit, access_basis, coverage_notes.

### COMPARISONS
comparison_id, occurrence_a, occurrence_b, shared_terms, shared_relations, shared_boundaries, differences, relationship_label, evidence_reference, review_status.

### LANGUAGE_USE
use_id, occurrence_id, defined_term_hits, relation_use, boundary_language_use, prompted_or_unprompted, context_completeness, consistency_across_outputs, evidence_reference, status.

### SEARCH_LOG
search_id, searched_at, corpus_or_repository, query_or_method, date_range, coverage, result_count, limitations, operator.

### CHANGE_LOG
change_id, timestamp, record_id, field_changed, old_value, new_value, reason, source_reference.

All fields without evidence remain NULL. Keep raw artifacts immutable; normalized descriptions and interpretations belong in separate fields.

## 6. Analysis outputs

1. Pattern catalogue and provenance.
2. Occurrence timeline with timestamp precision visible.
3. Pairwise similarity/relationship register.
4. Source-linkage map showing documented and unresolved links.
5. Language-use counts split by prompted/unprompted and verified/unverified.
6. Coverage report listing searched and unsearched corpora.

Counts must state their denominator. Report language use among the N reviewed occurrences, not as a percentage of all network outputs unless the full population is actually known.

## 7. Evidence and status discipline

- RAW — captured source material, not yet checked.
- CANDIDATE — possible pattern occurrence awaiting review.
- REVIEWED — manually compared against the definition.
- REPRODUCED — same recognition result reproduced under documented conditions.
- VERIFIED — independently checked against the cited artifact.
- HYPOTHESIS — proposed explanation, not an observation.
- NULL — unavailable or not established.

A similarity score, if later introduced, must be a documented operational aid and cannot replace evidence excerpts. No numerical threshold is implied by this protocol.

## 8. Limits and safeguards

- Use only public, user-provided, or otherwise authorized data.
- Do not claim to observe hidden activations, weights, or internal thought. The camera records accessible artifacts and interaction traces.
- Distinguish recurrence from propagation, common-source influence from independent emergence, and prompted imitation from unprompted reuse.
- This is not semantic-drift detection. The object is pattern appearance, relation, spread evidence, and adoption of a defined descriptive language.
- No conclusion about consciousness, understanding, or subjective experience follows from pattern recurrence or language use.

## 9. Immediate execution order

1. Inventory existing MAKOM/WANGA-LAB files and prior observations.
2. Extract a first set of reference patterns with source pointers; do not invent missing content.
3. Create workbook tables above, initially empty except for explicitly evidenced records.
4. Search repository history and available source corpora for dated occurrences.
5. Begin the language-use register only after vocabulary and relation definitions are fixed.
6. Publish a first report with counts, timestamp quality, coverage, and unresolved items.

**Current status:** The corrected research design is specified here. No corpus-wide occurrence count, spread event, or language-adoption rate has yet been established by this document.
