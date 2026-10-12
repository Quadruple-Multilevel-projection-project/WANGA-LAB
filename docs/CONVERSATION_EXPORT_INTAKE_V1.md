# Conversation Export Intake V1

The collector can import material the user actually exports or makes available. It cannot independently retrieve all private ChatGPT conversations.

## Run

```bash
python scripts/ingest_conversation_export.py ~/Downloads/chatgpt-export.zip --out ~/wanga-private-review/conversations
python scripts/ingest_conversation_export.py ~/Downloads/chatgpt-export.zip --out ~/wanga-private-review/metadata --metadata-only
```

The tool accepts the export ZIP or `conversations.json`. It writes one JSON record per conversation and a manifest containing source hash, conversation/message IDs, parent links, dates where available, and exact text or text hashes.

Outputs default to `PRIVATE_REVIEW_ONLY`, `publishable=false` and `NOT_APPROVED`. The script refuses to write transcript records inside the repository unless `--allow-repo-write` is explicitly supplied. That flag still does not approve publication; redact and review excerpts before they enter the public repository or Wix.

Each segment is labelled `TRANSCRIPT_TEXT_NOT_FACT_VERIFIED`: the export supports that the statement was made, not that the proposition is true. The tool does not upload, commit, or publish conversation contents.
