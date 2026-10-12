# Conversation Intake Protocol V1

## Access scope
Only process conversation material actually accessible in the current conversation, connected tools, or an explicitly provided/exported file. Do not claim to have swept every ChatGPT conversation on the account. If archive access fails, log the gap.

## Intake envelope
A batch must contain:
- batch ID and source kind;
- conversation/export ID, source version and access date if known;
- SHA-256 of the original source;
- exact literal spans and locators;
- extracted claim type: FACT, PROJECT_SPEC, HYPOTHESIS, QUESTION or DECISION;
- candidate concepts, alternative readings, conflicts and related article IDs;
- extraction version and review state.

## Processing rules
1. Keep the original immutable and hash it.
2. Never replace a literal span with a paraphrase; store normalized text separately.
3. Distinguish project proposals from external facts.
4. Keep alternative definitions in parallel until review.
5. De-duplicate only after comparing source, context, version and span.
6. Add wiki links without upgrading epistemic status.
7. Generate a batch report: captured, candidate, duplicate, conflict, exclusion and access-gap counts.
8. Record access/processing timestamps and code/model versions.

## Privacy and publication
Exclude credentials, sensitive identifiers, unrelated personal detail and raw private conversation text from the public wiki unless its publication is explicitly authorized. A private archive does not become public just because a fragment was extracted.
