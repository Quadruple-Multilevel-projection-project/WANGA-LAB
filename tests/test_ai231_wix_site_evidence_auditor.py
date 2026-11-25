import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from core.wix_link_auditor import (
    LinkStatus,
    classify_static_link,
    normalize_root_relative_path,
    PublicationStatus,
    classify_publication_state,
    NavigationStatus,
    classify_navigation_presence,
    audit_page_metadata,
)

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "agent-blueprint-v1.schema.json"
BLUEPRINT_PATH = ROOT / "agent_blueprints" / "ai231-wix-site-evidence-auditor.json"


class WixSiteEvidenceAuditorBlueprintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.blueprint = json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_blueprint_passes_canonical_schema(self):
        self.validator.validate(self.blueprint)

    def test_agent_is_draft_and_read_only(self):
        self.assertEqual(self.blueprint["status"], "draft")
        self.assertTrue(self.blueprint["runtime"]["isolation_required"])
        self.assertFalse(self.blueprint["runtime"]["network_egress"])
        self.assertEqual(self.blueprint["runtime"]["credential_refs"], [])
        permissions = set(self.blueprint["tool_permissions"])
        self.assertNotIn("publish_wix_site", permissions)
        self.assertNotIn("write_wix_site", permissions)
        self.assertNotIn("modify_production_site", permissions)
        self.assertNotIn("read_public_web_content", permissions)
        self.assertIn("analyze_supplied_data", permissions)

    def test_public_page_fetch_is_orchestrator_supplied(self):
        boundary = " ".join(self.blueprint["boundaries"]).lower()
        self.assertIn("must not fetch public urls directly", boundary)
        self.assertIn("network egress", boundary)
        test = next(item for item in self.blueprint["acceptance_tests"] if item["id"] == "AT-WIX-009")
        self.assertIn("blocked_no_network_egress", test["expected"].lower())

    def test_dynamic_routes_are_unresolved_until_verified(self):
        text = " ".join(
            test["description"] + " " + test["expected"]
            for test in self.blueprint["acceptance_tests"]
        ).lower()
        self.assertIn("unresolved_dynamic_route", text)
        self.assertIn("wix blog", text)

    def test_production_write_requests_are_blocked(self):
        text = " ".join(
            test["description"] + " " + test["expected"]
            for test in self.blueprint["acceptance_tests"]
        ).lower()
        self.assertIn("blocked", text)
        self.assertIn("production wix", text)

    def test_rollback_is_explicit(self):
        failure = self.blueprint["failure_behavior"].lower()
        self.assertIn("rollback", failure)
        self.assertIn("discard", failure)
        self.assertIn("revert", failure)

    def test_schema_rejects_network_egress(self):
        unsafe = copy.deepcopy(self.blueprint)
        unsafe["runtime"]["network_egress"] = True
        self.assertTrue(list(self.validator.iter_errors(unsafe)))

    def test_root_relative_links_are_normalized_before_missing_link_classification(self):
        self.assertEqual(normalize_root_relative_path("/roadmap.html"), "roadmap.html")
        self.assertEqual(
            classify_static_link("/roadmap.html", {"roadmap.html"}),
            LinkStatus.FOUND_STATIC,
        )

    def test_root_relative_missing_file_is_classified_missing(self):
        self.assertEqual(
            classify_static_link("/not-in-inventory.html", {"roadmap.html"}),
            LinkStatus.MISSING_STATIC,
        )

    def test_wix_dynamic_route_is_not_misclassified_as_missing(self):
        self.assertEqual(
            classify_static_link("/post/logic-and-matter", {"index.html"}),
            LinkStatus.UNRESOLVED_DYNAMIC_ROUTE,
        )

    def test_relative_link_resolves_from_current_page_directory(self):
        self.assertEqual(
            classify_static_link(
                "../roadmap.html",
                {"roadmap.html"},
                current_page="/pages/about.html",
            ),
            LinkStatus.FOUND_STATIC,
        )

    def test_query_and_fragment_do_not_change_static_file_match(self):
        self.assertEqual(
            classify_static_link("/roadmap.html?lang=he#overview", {"roadmap.html"}),
            LinkStatus.FOUND_STATIC,
        )

    def test_external_and_fragment_only_links_are_not_missing_static_files(self):
        self.assertEqual(
            classify_static_link("https://example.com/roadmap.html", set()),
            LinkStatus.EXTERNAL,
        )
        self.assertEqual(
            classify_static_link("#overview", set()),
            LinkStatus.ANCHOR,
        )

    def test_path_traversal_outside_site_root_is_rejected(self):
        self.assertEqual(
            classify_static_link("/../../secrets.txt", {"secrets.txt"}),
            LinkStatus.INVALID_LOCAL_PATH,
        )

    def test_publication_status_conflict_blocks_live_claim(self):
        self.assertEqual(
            classify_publication_state(True, False),
            PublicationStatus.STATUS_CONFLICT,
        )

    def test_publication_status_requires_both_independent_signals(self):
        self.assertEqual(
            classify_publication_state(True, None),
            PublicationStatus.UNRESOLVED_MISSING_EVIDENCE,
        )

    def test_matching_publication_signals_are_classified_consistently(self):
        self.assertEqual(
            classify_publication_state(True, True),
            PublicationStatus.CONSISTENT_PUBLISHED,
        )
        self.assertEqual(
            classify_publication_state(False, False),
            PublicationStatus.CONSISTENT_UNPUBLISHED,
        )

    def test_invalid_publication_signal_is_not_coerced_to_boolean(self):
        self.assertEqual(
            classify_publication_state("Published", False),
            PublicationStatus.UNRESOLVED_INVALID_EVIDENCE,
        )


    def test_navigation_absence_in_multi_page_site_is_candidate_not_defect(self):
        self.assertEqual(
            classify_navigation_presence(0, 26),
            NavigationStatus.ISOLATED_PAGE_CANDIDATE,
        )

    def test_navigation_present_is_classified(self):
        self.assertEqual(
            classify_navigation_presence(3, 26),
            NavigationStatus.NAVIGATION_PRESENT,
        )

    def test_single_page_site_may_have_no_navigation(self):
        self.assertEqual(
            classify_navigation_presence(0, 1),
            NavigationStatus.NO_NAVIGATION_EXPECTED,
        )

    def test_navigation_requires_site_context(self):
        self.assertEqual(
            classify_navigation_presence(None, 26),
            NavigationStatus.UNRESOLVED_INSUFFICIENT_CONTEXT,
        )

    def test_invalid_navigation_counts_fail_closed(self):
        self.assertEqual(
            classify_navigation_presence(True, 26),
            NavigationStatus.UNRESOLVED_INVALID_EVIDENCE,
        )
        self.assertEqual(
            classify_navigation_presence(-1, 26),
            NavigationStatus.UNRESOLVED_INVALID_EVIDENCE,
        )

    def test_blueprint_navigation_acceptance_requires_context(self):
        test = next(item for item in self.blueprint["acceptance_tests"] if item["id"] == "AT-WIX-010")
        expected = test["expected"].lower()
        self.assertIn("isolated_page_candidate", expected)
        self.assertIn("no_navigation_expected", expected)
        self.assertIn("unresolved_insufficient_context", expected)
        self.assertIn("do not automatically edit", expected)


if __name__ == "__main__":
    unittest.main()


class WixPageMetadataAuditorTests(unittest.TestCase):
    def test_missing_canonical_is_detected_without_network(self):
        html = '<html><head><title>About</title><meta name="description" content="About page"></head></html>'
        result = audit_page_metadata(html, expected_canonical="https://example.test/about.html")
        self.assertEqual(result["canonical_status"], "MISSING")
        self.assertEqual(result["canonical_count"], 0)

    def test_single_matching_https_canonical_is_present(self):
        expected = "https://example.test/about.html"
        html = f'<html><head><link rel="canonical" href="{expected}"></head></html>'
        result = audit_page_metadata(html, expected_canonical=expected)
        self.assertEqual(result["canonical_status"], "PRESENT")
        self.assertEqual(result["canonical_href"], expected)

    def test_non_https_canonical_is_invalid(self):
        result = audit_page_metadata('<link rel="canonical" href="http://example.test/about.html">')
        self.assertEqual(result["canonical_status"], "INVALID")

    def test_duplicate_canonical_tags_are_reported(self):
        html = (
            '<link rel="canonical" href="https://example.test/a">'
            '<link rel="canonical" href="https://example.test/b">'
        )
        result = audit_page_metadata(html)
        self.assertEqual(result["canonical_status"], "DUPLICATE")
        self.assertEqual(result["canonical_count"], 2)

    def test_canonical_must_match_orchestrator_supplied_expected_url(self):
        html = '<link rel="canonical" href="https://example.test/old.html">'
        result = audit_page_metadata(
            html,
            expected_canonical="https://example.test/new.html",
        )
        self.assertEqual(result["canonical_status"], "MISMATCH")

    def test_blueprint_declares_canonical_metadata_acceptance(self):
        blueprint = json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))
        acceptance_ids = {item["id"] for item in blueprint["acceptance_tests"]}
        self.assertIn("AT-WIX-011", acceptance_ids)
