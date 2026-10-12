# Conversation Inbox V1

Status: EMPTY / BLOCKED WAITING FOR AN EXPLICIT EXPORT

This protocol applies to exported conversation files that are actually provided or accessible through an authorized connector. It does not imply access to every ChatGPT conversation on an account. The intended intake directory is research/inbox/conversations/.

## Intake record required

For every export, record the stable source ID, export ID when supplied, export/access dates, original file name and byte size, SHA-256 of original bytes, exact message/page/span locator, original ordering, language, verification status, and usage/publication permissions. Record the normalization tool/version and link to the immutable original.

## Processing rules

1. Preserve the original export unchanged and read-only.
2. Store normalized text separately; normalize only technical/reversible details.
3. Keep source text, quotation, source claim, interpretation, hypothesis and implementation separate.
4. Preserve message order, timestamps, speaker labels and locators when present.
5. Do not infer missing messages or reconstruct an inaccessible conversation from summaries.
6. Do not publish raw private conversation text or unrelated personal information.
7. If original bytes are unavailable, record hash status as BLOCKED; do not substitute a hash of partial extracted text.
8. A successful parse is not verification of claims inside a conversation.

## Current access audit

On 2026-10-12 the current conversation file list contained zero uploaded files. Library searches did not locate an explicit ChatGPT transcript export. This is an access gap, not evidence that no export exists elsewhere. No transcript was fabricated or added by this run.

When an export is supplied, place it under an immutable batch directory, update the source registry and dated run report, and keep public wiki publication separate from private intake.
