# Axis Extraction Protocol (AEP)

**Status:** SPECIFIED / NOT_YET_VERIFIED  
**Output:** reviewed Keystone candidates and source-grounded logic fragments

## Procedure

1. **Register source.** Record source URI/ID, repository/ref, exact path and locator, version or commit, language, permission scope, and available hash.
2. **Preserve literal span.** Store the original excerpt without silent correction. Any normalization must be reversible or accompanied by an explicit mapping.
3. **Separate epistemic objects.** Record source, excerpt, claim, interpretation, hypothesis, implementation, test, and verification as distinct typed records.
4. **Map structure.** Identify terms, predicates, relations, operators, constraints, quantifiers, boundaries, and unresolved references. Unknown fields stay unknown.
5. **Formalize.** Provide an explicit first-order representation where appropriate; record second-order/meta-level assumptions separately. Do not force every source into formal logic.
6. **Check closure and contradiction.** Check variable binding, arity, type/domain, source resolution, contradiction, and applicability boundaries.
7. **Run perturbation tests.** Compare baseline, removal, substitution, negation, and boundary variants. Include at least one counter-reading where meaningful.
8. **Review.** Record reviewer independence and disagreements. A mirror/counter-reading is a test input, not automatically the correct interpretation.
9. **Assign status.** Use the narrowest supported status; attach the actual test output.
10. **Version.** Hash the normalized artifact and retain source mapping, parent IDs, rule IDs, and test versions.

## Required record fields

`id`, `source_id`, `source_locator`, `literal_excerpt`, `language`, `normalization_map`, `terms`, `relations`, `operators`, `constraints`, `boundaries`, `formalization`, `assumptions`, `counter_readings`, `tests`, `review_status`, `epistemic_status`, `version`, `artifact_hash`, `next_action`.

## Failure handling

- Missing source or permission: `BLOCKED`.
- Ambiguous interpretation: `INCONCLUSIVE`; preserve alternatives.
- Contradiction: record both sides and scope; do not silently choose one.
- Failed ablation or perturbation: retain the failure as evidence.
- Visual similarity or numeric weight without a supported relation: no relation is emitted.
- No actual execution evidence: status cannot be `TESTED` or `VERIFIED`.

## Minimum test matrix

| Test | Question |
|---|---|
| Baseline | Does the candidate produce the declared output? |
| Ablation | What changes if the candidate element is removed? |
| Substitution | Does a plausible replacement preserve the structure? |
| Negation | Which consequences change under explicit negation? |
| Boundary | Where should the rule not apply? |
| Counter-reading | Is there a source-compatible alternative interpretation? |
| Rebuild | Does the same version/configuration reproduce the same artifact? |
