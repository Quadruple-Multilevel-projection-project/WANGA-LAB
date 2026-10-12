# Conversation Research Inbox

This directory is the explicit intake boundary for conversation material. Repository workflows cannot directly read every private ChatGPT chat. Place user-authorized exports or excerpts here; the daily WANGA research loop may also use conversation and Library material actually exposed to its runtime.

## Record format
One JSON file per conversation/export batch. Required fields: record_id, source_type (CHAT_EXPORT / USER_PASTED_EXCERPT / LIBRARY_FILE), source_locator, captured_at or null, language, content_sha256 where bytes are available, permission_scope, and segments with stable IDs, exact text, locator and epistemic status.

Never publish private or sensitive conversation text on Wix without review. Public wiki articles should link to approved derived summaries, not expose raw private transcripts by default. A conversation segment is evidence of what was said, not proof that the proposition is true.

Processing states: REGISTERED → EXTRACTED → STRUCTURED → REVIEW_REQUIRED → ACCEPTED/REJECTED. Missing chat access is BLOCKED_SOURCE_UNAVAILABLE, not an empty corpus.