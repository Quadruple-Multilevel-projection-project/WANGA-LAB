# Logic Fractal Research Report Format V1

Each scheduled or manual research cycle produces a dated Markdown and JSON report containing:

- Run date, runner/workflow ID and status: COMPLETED / IN_PROGRESS / BLOCKED / FAILED / NO_CHANGE.
- Source coverage, exact locators, versions/hashes, duplicates, missing locators and access gaps.
- Conversation exports actually available to the run, segment counts, hashes and permission status; never imply full private-chat access.
- Extracted literal units, claims, relations, assumptions, boundaries and stable IDs.
- Fractal composition scale, parent IDs, contracts, invariants, model hash and candidate status.
- MIRROR/counter-readings, contradictions, counterexamples and failed tests.
- Semantic benchmarks actually executed, split/holdout, metrics, failure cases and adjudication; software unit tests reported separately.
- Dynamic readiness metrics and deficits, including whether contradiction inventory, holdout and independent reviews exist.
- GitHub/CI status and Wix deployment/read-back evidence, or BLOCKED if not verified.
- Previous/current model hashes, version deltas, regressions and next actions.

NO_CHANGE is valid. Missing information must be reported as unavailable rather than imputed. VERIFIED requires evidence of the actual check and result. Never publish raw private conversation exports.