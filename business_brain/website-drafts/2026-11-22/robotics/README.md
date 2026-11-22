# AI231 Robotics Collaboration — non-production website patch draft

Date: 2026-11-22
Site: AI231 Robotics Collaboration
Wix site ID: d8dcc187-d8fe-4e3c-b7a4-9e46f020349e
Published URL: https://headless-nkogaqagpcv-beywolf5-1408.wix-site-host.com/
Source access: Wix headless files.list/read (read-only)

## Verified before state
- Files inspected: index.html (14,709 bytes), about.html (22,857 bytes), agents.html (10,775 bytes).
- All three pages have a viewport meta tag and a mobile media breakpoint.
- At the mobile breakpoint, each page hides its primary navigation (.links or .navlinks) without an alternative navigation control. index.html and agents.html have no buttons; about.html has only its language buttons. This is a source-level navigation gap; browser/device behavior was not independently tested.
- agents.html described the deployed workbench and seven role definitions without stating that live invocation history, sandbox isolation and network-egress controls were not verified.
- No contact email or form is published. The source explicitly says an official contact channel has not yet been confirmed; this was preserved rather than inventing an address or collecting personal data.

## Draft changes
1. Add a keyboard-operable mobile menu button to all three pages with aria-expanded, aria-controls, and an accessible label.
2. Add an expanded mobile navigation panel, close-on-link, Escape-key close, focus return and resize reset behavior.
3. Replace the agents page status copy with a deployment/runtime distinction: the workbench deployment is ready; live invocation history, continuous autonomous operation, sandbox isolation and egress controls remain unverified.

## Before / after status wording
**Before:** “A role-based AI workbench prototype is now deployed. Seven specialized roles can execute bounded tasks, return structured outputs and record accepted contributions.”

**After:** “The AI231 Agent Foundry workbench is deployed and contains seven role definitions plus task-run workflows. Deployment readiness is verified; live invocation history, continuous autonomous operation, sandbox isolation and network-egress controls have not been verified.”

## Draft files
- index.html — source 14709 bytes; draft 16438 JavaScript string characters.
- about.html — source 22857 bytes; draft 21195 JavaScript string characters.
- agents.html — source 10775 bytes; draft 12594 JavaScript string characters.

## Draft commit identifiers
- index.html: d4fa9cf8cbdf1f143b110c01c8b1ee729ab0b5c4
- about.html: 05cb10c3aa007ddc3599d0234aea0a87c717a394
- agents.html: c8d51577fed01f7928256046af8c4a2eb8c6f7dd

## Verification boundary
- Drafts are stored only in the GitHub execution branch; no Wix file was patched, uploaded or published.
- Internal static checks: each page has one mobile-nav button, one matching primary-nav target, an aria-expanded state, an Escape handler and a mobile-open CSS rule.
- Browser-based mobile, keyboard and screen-reader tests remain NOT_YET_VERIFIED.
- External links and dynamic routes remain outside this static-file check.

## Rollback
Discard the three draft files and this README from the execution branch. No production rollback is required because the Wix site was not modified.

## Status
DRAFT_READY / PRODUCTION_WRITE_BLOCKED_PENDING_EXPLICIT_APPROVAL
