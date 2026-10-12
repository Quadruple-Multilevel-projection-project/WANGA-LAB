#!/usr/bin/env python3
"""Privately ingest a ChatGPT export without publishing transcripts."""
from __future__ import annotations
import argparse, datetime as dt, hashlib, json, re, zipfile
from pathlib import Path
from typing import Any, Mapping, Sequence

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def canonical_sha(value: Any) -> str:
    return sha256_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))

def safe_id(value: Any, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value or "").strip()).strip("-._")
    return cleaned[:90] if cleaned else fallback

def _parts_to_text(content: Any) -> tuple[str, int]:
    if not isinstance(content, Mapping): return "", 0
    parts = content.get("parts")
    if parts is None and isinstance(content.get("text"), str): return content["text"], 0
    if not isinstance(parts, list): return "", 0
    texts, non_text = [], 0
    for part in parts:
        if isinstance(part, str): texts.append(part)
        elif isinstance(part, Mapping) and isinstance(part.get("text"), str): texts.append(part["text"])
        else: non_text += 1
    return "\n".join(texts), non_text

def _iso_time(value: Any) -> str | None:
    if value is None: return None
    try:
        number = float(value)
        if number < 0: return None
        return dt.datetime.fromtimestamp(number, tz=dt.timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError, OSError):
        if isinstance(value, str):
            try:
                parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None: parsed = parsed.replace(tzinfo=dt.timezone.utc)
                return parsed.astimezone(dt.timezone.utc).isoformat()
            except ValueError: return None
        return None

def load_export(path: Path) -> tuple[list[dict[str, Any]], bytes, str]:
    raw = path.read_bytes()
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            matches = [n for n in archive.namelist() if Path(n).name == "conversations.json"]
            if not matches: raise ValueError("ZIP contains no conversations.json member.")
            member = sorted(matches, key=lambda x: (x.count("/"), len(x)))[0]
            data_bytes, locator = archive.read(member), path.name + "!/" + member
    else: data_bytes, locator = raw, path.name
    try: payload = json.loads(data_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc: raise ValueError(f"Could not parse UTF-8 conversation export: {exc}") from exc
    if not isinstance(payload, list) or any(not isinstance(x, Mapping) for x in payload):
        raise ValueError("ChatGPT export root must be an array of conversation objects.")
    return list(payload), raw, locator

def conversation_to_record(conversation: Mapping[str, Any], *, export_locator: str, archive_sha256: str, index: int, metadata_only: bool = False) -> dict[str, Any]:
    conv_id = str(conversation.get("id") or f"conversation-{index:06d}")
    record_id = "CHAT-" + safe_id(conv_id, f"{index:06d}")
    mapping = conversation.get("mapping")
    if not isinstance(mapping, Mapping): mapping = {}
    messages, excluded, attachment_only = [], 0, 0
    for node_id, node in mapping.items():
        if not isinstance(node, Mapping): continue
        message = node.get("message")
        if not isinstance(message, Mapping): continue
        author = message.get("author") if isinstance(message.get("author"), Mapping) else {}
        role = str(author.get("role") or "unknown")
        if role not in {"user", "assistant"}: excluded += 1; continue
        text, non_text = _parts_to_text(message.get("content"))
        if not text.strip():
            if non_text: attachment_only += 1
            excluded += 1
            continue
        message_id = str(message.get("id") or node_id or "")
        messages.append({
            "_sort_time": float(message.get("create_time") or 0.0) if isinstance(message.get("create_time"), (int,float)) else 0.0,
            "message_id": message_id, "parent_message_id": node.get("parent"), "role": role,
            "timestamp_utc": _iso_time(message.get("create_time")),
            "text": None if metadata_only else text, "text_sha256": sha256_bytes(text.encode("utf-8")),
            "message_record_sha256": canonical_sha({"role": role, "text": text, "message_id": message_id}),
            "text_omitted": metadata_only, "non_text_part_count": non_text,
            "status": "TRANSCRIPT_TEXT_NOT_FACT_VERIFIED", "publication_status": "NOT_APPROVED"
        })
    messages.sort(key=lambda m: (m["_sort_time"], m["message_id"]))
    segments=[]
    for order,msg in enumerate(messages,1):
        msg.pop("_sort_time",None)
        msg["segment_id"]=f"{record_id}-MSG-{order:06d}"
        msg["order_by_timestamp"]=order
        segments.append(msg)
    return {
        "schema_version":"conversation-intake/1.0","record_id":record_id,"source_type":"CHAT_EXPORT",
        "source_locator":f"{export_locator}#conversation={conv_id}","conversation_id":conv_id,
        "title":str(conversation.get("title") or "Untitled conversation"),
        "captured_at":dt.datetime.now(dt.timezone.utc).isoformat(),
        "conversation_created_at":_iso_time(conversation.get("create_time")),
        "conversation_updated_at":_iso_time(conversation.get("update_time")),
        "language":"und","archive_sha256":archive_sha256,
        "conversation_record_sha256":canonical_sha({"conversation_id":conv_id,"segments":[{k:v for k,v in s.items() if k!="text"} for s in segments]}),
        "permission_scope":"PRIVATE_REVIEW_ONLY","publication_status":"NOT_APPROVED","publishable":False,
        "metadata_only":metadata_only,"segment_count":len(segments),
        "excluded_non_user_assistant_message_count":excluded,"attachment_only_message_count":attachment_only,
        "segments":segments,"processing_status":"REGISTERED_REVIEW_REQUIRED",
        "epistemic_boundary":"This record preserves what a transcript says; it does not establish the truth of its claims."
    }

def is_within(path: Path, root: Path) -> bool:
    try: path.resolve().relative_to(root.resolve()); return True
    except ValueError: return False

def ingest(export_path: Path, output_dir: Path, *, repo_root: Path, metadata_only: bool=False, allow_repo_write: bool=False, max_conversations: int|None=None) -> dict[str, Any]:
    if is_within(output_dir, repo_root) and not allow_repo_write:
        raise ValueError("Refusing to write private transcript records inside the repository; choose a private output directory or explicitly pass --allow-repo-write after review.")
    convs,raw,locator=load_export(export_path)
    if max_conversations is not None:
        if max_conversations<1: raise ValueError("--max-conversations must be positive.")
        convs=convs[:max_conversations]
    archive_hash=sha256_bytes(raw)
    record_payloads=[
        conversation_to_record(conv,export_locator=locator,archive_sha256=archive_hash,index=i,metadata_only=metadata_only)
        for i,conv in enumerate(convs,1)
    ]
    record_ids=[record["record_id"] for record in record_payloads]
    if len(record_ids)!=len(set(record_ids)):
        raise ValueError("Duplicate conversation record IDs detected; no output files were written.")
    output_dir.mkdir(parents=True,exist_ok=True); records=[]
    for record in record_payloads:
        out=output_dir/(record["record_id"]+".json")
        out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        records.append({"record_id":record["record_id"],"output_file":out.name,"segment_count":record["segment_count"],"conversation_record_sha256":record["conversation_record_sha256"],"permission_scope":record["permission_scope"],"publication_status":record["publication_status"]})
    manifest={"schema_version":"conversation-intake-manifest/1.0","source_locator":locator,"archive_sha256":archive_hash,"captured_at":dt.datetime.now(dt.timezone.utc).isoformat(),"metadata_only":metadata_only,"record_count":len(records),"records":records,"private_review_only":True,"publication_status":"NOT_APPROVED","limits":["Only the provided export file was read; this tool cannot fetch all ChatGPT account conversations.","No transcript text was published, uploaded to Wix, or committed to GitHub by this tool.","Review/redact content before placing approved excerpts in the public repository."]}
    (output_dir/"ingest_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def main(argv: Sequence[str]|None=None) -> int:
    p=argparse.ArgumentParser(description="Ingest a user-provided ChatGPT export into a private review-only corpus.")
    p.add_argument("export",type=Path,help="ChatGPT conversations.json or export ZIP")
    p.add_argument("--out",type=Path,required=True,help="Output directory outside repository by default")
    p.add_argument("--repo-root",type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument("--metadata-only",action="store_true",help="Store message hashes/metadata, omit text")
    p.add_argument("--allow-repo-write",action="store_true",help="Allow output inside repo after explicit privacy review")
    p.add_argument("--max-conversations",type=int)
    a=p.parse_args(argv)
    try: report=ingest(a.export,a.out,repo_root=a.repo_root,metadata_only=a.metadata_only,allow_repo_write=a.allow_repo_write,max_conversations=a.max_conversations)
    except (OSError,ValueError) as exc:
        print(json.dumps({"status":"REJECTED","error":str(exc)},ensure_ascii=False)); return 2
    print(json.dumps({"status":"COMPLETED_PRIVATE_REVIEW_ONLY","records":report["record_count"],"segments":sum(x["segment_count"] for x in report["records"]),"archive_sha256":report["archive_sha256"],"output_dir":str(a.out.resolve()),"publishable":False},ensure_ascii=False))
    return 0

if __name__=="__main__": raise SystemExit(main())
