from __future__ import annotations
import json, tempfile, unittest, zipfile
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from ingest_conversation_export import conversation_to_record, ingest, load_export, sha256_bytes

def fixture():
 return [{"id":"conv-A","title":"Logic model discussion","create_time":1791800000,"update_time":1791800100,"mapping":{
  "sys":{"message":{"id":"sys","author":{"role":"system"},"content":{"parts":["system prompt"]}}},
  "u1":{"parent":"sys","message":{"id":"u1","author":{"role":"user"},"create_time":1791800001,"content":{"parts":["The logical fractal should preserve sources."]}}},
  "a1":{"parent":"u1","message":{"id":"a1","author":{"role":"assistant"},"create_time":1791800002,"content":{"parts":["That is a design hypothesis, not a verified fact."]}}},
  "u2":{"parent":"a1","message":{"id":"u2","author":{"role":"user"},"create_time":1791800003,"content":{"parts":[{"image":"payload"}]}}}
 }}]

class ConversationIntakeTests(unittest.TestCase):
 def test_source_hash_and_private_epistemic_status(self):
  r=conversation_to_record(fixture()[0],export_locator="export.json",archive_sha256="a"*64,index=1)
  self.assertEqual(r["source_type"],"CHAT_EXPORT"); self.assertFalse(r["publishable"])
  self.assertEqual(r["publication_status"],"NOT_APPROVED"); self.assertEqual(r["permission_scope"],"PRIVATE_REVIEW_ONLY")
  self.assertEqual(r["segment_count"],2)
  self.assertTrue(all(x["status"]=="TRANSCRIPT_TEXT_NOT_FACT_VERIFIED" for x in r["segments"]))
 def test_metadata_only_keeps_hash_omits_text(self):
  r=conversation_to_record(fixture()[0],export_locator="export.json",archive_sha256="a"*64,index=1,metadata_only=True)
  self.assertTrue(all(x["text"] is None and x["text_omitted"] for x in r["segments"]))
  self.assertTrue(all(len(x["text_sha256"])==64 for x in r["segments"]))
 def test_reads_zip_export_without_extracting_it(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); zpath=root/"export.zip"
   with zipfile.ZipFile(zpath,"w") as z:z.writestr("conversations.json",json.dumps(fixture()))
   convs,raw,loc=load_export(zpath)
   self.assertEqual(len(convs),1);self.assertIn("conversations.json",loc);self.assertEqual(len(sha256_bytes(raw)),64)
 def test_refuses_private_write_inside_repository(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);repo=root/"repo";repo.mkdir();export=root/"conversations.json";export.write_text(json.dumps(fixture()),encoding="utf-8")
   with self.assertRaises(ValueError):ingest(export,repo/"research/inbox/conversations",repo_root=repo)
 def test_manifest_never_marks_export_publishable(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);export=root/"conversations.json";export.write_text(json.dumps(fixture()),encoding="utf-8");out=root/"private"
   result=ingest(export,out,repo_root=root/"repo")
   self.assertEqual(result["record_count"],1);self.assertTrue(result["private_review_only"]);self.assertEqual(result["publication_status"],"NOT_APPROVED")
   record=json.loads((out/(result["records"][0]["record_id"]+".json")).read_text(encoding="utf-8"))
   self.assertIn("source_locator",record);self.assertEqual(record["segment_count"],2)
 def test_duplicate_conversation_ids_fail_before_writing(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); export=root/"conversations.json"
   export.write_text(json.dumps(fixture()+fixture()),encoding="utf-8")
   out=root/"private"
   with self.assertRaises(ValueError):ingest(export,out,repo_root=root/"repo")
   self.assertFalse(out.exists())
 def test_text_is_preserved_exactly(self):
  r=conversation_to_record(fixture()[0],export_locator="export.json",archive_sha256="a"*64,index=1)
  self.assertEqual(r["segments"][0]["text"],"The logical fractal should preserve sources.")
  self.assertEqual(r["segments"][1]["text"],"That is a design hypothesis, not a verified fact.")
if __name__=="__main__":unittest.main()
