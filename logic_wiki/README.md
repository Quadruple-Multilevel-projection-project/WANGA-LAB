# WANGA Logic Wiki

An original, source-linked research encyclopedia for logical primitives, relations, operators, rules, recursive compositions, proofs, counterexamples and model versions. It is not an official Wikipedia project.

## Rules
- Stable article IDs and version control.
- Each factual claim links to a source or is explicitly labelled as proposal/hypothesis.
- Source, claim, interpretation, hypothesis and implementation status are different fields.
- A fractal map is a composition candidate, not automatic proof of correctness.
- Navigation should connect source → claim → primitive → relation → composition rule → test/report.
- Edit data/articles.json, not generated HTML/Markdown.
- Conversation contributions must come from accessible excerpts or user-provided exports under research/inbox/conversations.

## Build locally

    python scripts/build_logic_wiki.py --root . --out logic_wiki/generated

The weekly workflow validates records and opens/updates a PR with generated wiki pages and a readiness report. It never auto-merges.

The first-model gate is intentionally not met by the seed glossary alone.