# Cartography Agent Instructions

## Scope
Operate only on explicitly registered files and feeds. Do not infer unobserved events, make private transcripts public, or treat the project's conceptual vocabulary as evidence that a real-world event occurred.

## Source handling
1. Preserve source URI, exact locator, publication time if available, observation time, source version/hash when available, permission scope, and literal excerpt or authorized summary.
2. Keep source, claim, observation, interpretation, hypothesis, implementation, test, and verification distinct.
3. Missing source fields remain missing. Do not manufacture coordinates or evidence.
4. Treat each generated bundle as a candidate unless its verification procedure and evidence are present and checked.

## Boundaries
- No forecasting in the daily recorder.
- No automatic semantic repair.
- No deriving an axiom from a hard-coded placeholder.
- No promotion to VERIFIED based only on schema success or successful execution.
- No input from generated output folders; only the explicit inbox paths are inputs.
- Never commit raw private conversation exports.
- On failure, stop the affected stage, retain the log, and leave unrelated independent checks available.

## Repository writes
The parent repository workflow proposes changes through a bot branch and pull request. Never push directly to the default branch. Do not auto-merge. A green software test means only that the named software checks passed.
