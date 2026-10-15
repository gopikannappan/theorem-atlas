import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("fidelity_score", ROOT / "scripts/score_fidelity_benchmark.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class BenchmarkScoringTests(unittest.TestCase):
    def setUp(self):
        self.packet = {"benchmark_id": "test", "cases": [{"id": "control"}, {"id": "defect"}]}
        self.key = {"benchmark_id": "test", "reference_status": "author_intent_only_expert_pending",
                    "cases": [{"id": "control", "intended_label": "aligned", "intended_category": None},
                              {"id": "defect", "intended_label": "mismatch", "intended_category": "added_assumption"}]}
        self.report = {"benchmark_id": "test", "reviewer_id": "test", "source_commit": "frozen",
                       "packet_git_blob": "blob", "cases": [
                           dict(id=name, verdict=verdict, category=category,
                                source_obligation="all inputs", lean_location="fixture:1",
                                explanation="scope comparison", counterexample_or_scope_argument="additional hypothesis")
                           for name, verdict, category in [("control", "aligned", "equivalent"),
                                                           ("defect", "mismatch", "added_assumption")]]}

    def score(self):
        return module.score(self.packet, self.key, self.report, "frozen", "blob")

    def test_success_is_author_agreement_without_certification(self):
        result = self.score()
        self.assertEqual(result["counts"]["intended_defects_flagged"], 1)
        self.assertEqual(result["counts"]["aligned_agreements"], 1)
        self.assertEqual(result["counts"]["category_agreements"], 1)
        self.assertIsNone(result["expert_accuracy"])
        self.assertEqual(result["certification"], "none")

    def test_false_alarm_and_missed_defect(self):
        self.report["cases"][0]["verdict"] = "mismatch"
        self.report["cases"][1]["verdict"] = "aligned"
        counts = self.score()["counts"]
        self.assertEqual(counts["control_false_alarms"], 1)
        self.assertEqual(counts["intended_defects_missed"], 1)
        self.assertEqual(counts["intended_defects_flagged"], 0)

    def test_abstention_is_not_acceptance_or_detection(self):
        for case in self.report["cases"]:
            case["verdict"] = "inconclusive"
        counts = self.score()["counts"]
        self.assertEqual(counts["inconclusive"], 2)
        self.assertEqual(counts["aligned_agreements"] + counts["intended_defects_flagged"], 0)

    def test_missing_duplicate_extra_cases_rejected(self):
        original = copy.deepcopy(self.report)
        for rows in [original["cases"][:1], original["cases"] + [original["cases"][0]],
                     original["cases"] + [dict(original["cases"][0], id="extra")]]:
            self.report = dict(original, cases=rows)
            with self.assertRaises(ValueError):
                self.score()

    def test_input_identity_mismatch_rejected(self):
        for field in ("source_commit", "packet_git_blob", "benchmark_id"):
            changed = copy.deepcopy(self.report)
            changed[field] = "wrong"
            with self.assertRaises(ValueError):
                module.score(self.packet, self.key, changed, "frozen", "blob")

    def test_missing_diagnostic_rejected_but_correctness_not_inferred(self):
        self.report["cases"][0]["explanation"] = ""
        with self.assertRaises(ValueError):
            self.score()

    def test_frozen_reports_are_complete_and_scorable(self):
        root = ROOT / "benchmarks/ai-fidelity/v1"
        read = lambda name: json.loads((root / name).read_text())
        run = read("run.json")
        for path in run["reports"]:
            result = module.score(read("cases.json"), read("answer-key.json"), read(path),
                                  run["source_commit"], run["packet_git_blob"])
            self.assertEqual(result["total"], 12)
            self.assertEqual(result["diagnostic_correctness"], "ungraded")

    def test_frozen_inputs_and_compiler_hashes(self):
        root = ROOT / "benchmarks/ai-fidelity/v1"
        run = json.loads((root / "run.json").read_text())
        for name, expected in (("cases.json", run["packet_git_blob"]),
                               ("answer-key.json", run["key_git_blob"])):
            data = (root / name).read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            self.assertEqual(digest, expected)
        observations = json.loads((root / "compiler-observation.json").read_text())["observations"]
        packet = json.loads((root / "cases.json").read_text())
        self.assertEqual({row["id"] for row in observations}, {row["id"] for row in packet["cases"]})
        for row in observations:
            source = (root / "fixtures" / (row["id"] + ".lean")).read_bytes()
            self.assertEqual(hashlib.sha256(source).hexdigest(), row["source_sha256"])
            self.assertEqual(row["exit_code"], 0)

    def test_preserved_reports_and_results_match(self):
        root = ROOT / "benchmarks/ai-fidelity/v1"
        read = lambda name: json.loads((root / name).read_text())
        run = read("run.json")
        expected = read("results.json")
        actual = []
        for path, archive in zip(run["reports"], run["report_archives"]):
            data = (root / path).read_bytes()
            digest = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
            self.assertEqual(digest, archive["blob"])
            actual.append(module.score(read("cases.json"), read("answer-key.json"), read(path),
                                       run["source_commit"], run["packet_git_blob"]))
        self.assertEqual(actual, expected["results"])
