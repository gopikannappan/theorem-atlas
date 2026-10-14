import copy
import json
import unittest
from pathlib import Path
from scripts.check_ai_review_records import validate_records

ROOT = Path(__file__).resolve().parents[1]

class AIReviewRecordsTest(unittest.TestCase):
    def setUp(self):
        self.session = json.loads((ROOT / "audits/ai-fidelity/sessions/stacks-normal-rings.json").read_text())
        self.packet = json.loads((ROOT / self.session["packet"]["path"]).read_text())
        self.read = lambda name: (ROOT / name).read_bytes()

    def test_complete_record_is_not_a_certification(self):
        result = validate_records(self.packet, self.session, self.read)
        self.assertEqual(result["reviewer_count"], 2)
        self.assertEqual(result["certification"], "none")

    def test_packet_and_report_changes_invalidate_record(self):
        for path in [self.session["packet"]["path"], self.session["reviewers"][0]["files"][0]["path"]]:
            with self.subTest(path=path), self.assertRaises(ValueError):
                validate_records(self.packet, self.session, lambda name: self.read(name) + (b"changed" if name == path else b""))

    def test_duplicate_or_self_review_and_exposed_reports_rejected(self):
        for mutation in [
            lambda s: s["reviewers"][1].update(agent_path=s["reviewers"][0]["agent_path"]),
            lambda s: s["reviewers"][1].update(id=s["reviewers"][0]["id"]),
            lambda s: s["reviewers"][0].update(generated_target=True),
            lambda s: s["reviewers"][0].update(other_review_seen_before_initial_freeze=True),
            lambda s: s["reviewers"][0].update(fresh_context=False),
        ]:
            changed = copy.deepcopy(self.session)
            mutation(changed)
            with self.assertRaises(ValueError):
                validate_records(self.packet, changed, self.read)

    def test_recommendations_cannot_be_promoted_to_certification(self):
        for value in ["faithful", "audited", "ai_fidelity_review_passed"]:
            changed = copy.deepcopy(self.session)
            changed["certification"] = value
            with self.assertRaises(ValueError):
                validate_records(self.packet, changed, self.read)

    def test_missing_provenance_remains_visible(self):
        self.session["provenance_complete"] = True
        with self.assertRaises(ValueError):
            validate_records(self.packet, self.session, self.read)

    def test_source_url_and_paths_must_match_frozen_input(self):
        changed = copy.deepcopy(self.packet)
        changed["target"]["url"] = "https://example.com/unpinned"
        with self.assertRaises(ValueError):
            validate_records(changed, self.session, self.read)
        self.session["packet"]["path"] = "audits/ai-fidelity/../../secrets"
        with self.assertRaises(ValueError):
            validate_records(self.packet, self.session, self.read)

if __name__ == "__main__":
    unittest.main()
