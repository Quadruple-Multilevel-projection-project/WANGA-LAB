import json

from engine import logic_bundle_builder


def bundle_source():
    return {
        "bundle_id": "BUNDLE-IDEMPOTENT-TEST",
        "version": "0.1.0",
        "source_refs": ["https://example.invalid/source"],
        "structure": {
            "type": "SYNTHETIC_CONTRACT",
            "required": ["source_ref", "exact_locator"],
            "release_state": "DRAFT_UNVERIFIED"
        }
    }


def test_same_bundle_input_is_idempotent(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    inbox = root / "cartography" / "inbox" / "logic_bundles"
    output = root / "cartography" / "logic_bundles"
    inbox.mkdir(parents=True)
    (inbox / "bundle.json").write_text(json.dumps(bundle_source()), encoding="utf-8")
    monkeypatch.setattr(logic_bundle_builder, "ROOT", root)
    monkeypatch.setattr(logic_bundle_builder, "INBOX", inbox)
    monkeypatch.setattr(logic_bundle_builder, "OUT", output)

    first = logic_bundle_builder.build_bundles()
    assert first["status"] == "BUILT"
    artifact_before = (output / "BUNDLE-IDEMPOTENT-TEST.json").read_text(encoding="utf-8")

    second = logic_bundle_builder.build_bundles()
    assert second["status"] == "ALREADY_CURRENT"
    assert len(second["already_present"]) == 1
    assert (output / "BUNDLE-IDEMPOTENT-TEST.json").read_text(encoding="utf-8") == artifact_before


def test_changed_source_under_existing_bundle_id_fails_closed(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    inbox = root / "cartography" / "inbox" / "logic_bundles"
    output = root / "cartography" / "logic_bundles"
    inbox.mkdir(parents=True)
    source_path = inbox / "bundle.json"
    source_path.write_text(json.dumps(bundle_source()), encoding="utf-8")
    monkeypatch.setattr(logic_bundle_builder, "ROOT", root)
    monkeypatch.setattr(logic_bundle_builder, "INBOX", inbox)
    monkeypatch.setattr(logic_bundle_builder, "OUT", output)

    assert logic_bundle_builder.build_bundles()["status"] == "BUILT"
    changed = bundle_source()
    changed["structure"]["required"].append("source_hash")
    source_path.write_text(json.dumps(changed), encoding="utf-8")

    result = logic_bundle_builder.build_bundles()
    assert result["status"] == "FAILED"
    assert "BUNDLE_ID_CONTENT_MISMATCH:BUNDLE-IDEMPOTENT-TEST" in result["rejected"][0]["reason"]
