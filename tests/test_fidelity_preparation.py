import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("prep_check", ROOT / "scripts/check_fidelity_preparation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PreparationIntegrityTests(unittest.TestCase):
    def setUp(self):
        read = lambda path: json.loads((ROOT / path).read_text())
        prefix = Path("benchmarks/ai-fidelity/real-source-pool")
        self.pool = read(prefix / "pool.json")
        self.form = read(prefix / "adjudication-template.json")
        self.pilot = read("benchmarks/ai-fidelity/v1/cases.json")
        self.targets = sum((read(Path("audits/linked-declarations/groups") / (name + ".json"))["targets"]
                            for name in ("alphaproof", "harmonic-imo")), [])
        self.observations = read(prefix / "source-observations.json")

    def validate(self):
        return module.validate(self.pool, self.form, self.pilot, self.targets, self.observations)

    def test_pending_preparation_is_not_certification(self):
        result = self.validate()
        self.assertEqual((result["families"], result["declarations"], result["pilot_slots"],
                          result["explanation_slots"]), (3, 4, 12, 24))
        self.assertEqual(result["certification"], "none")

    def test_source_commit_and_declaration_cannot_drift(self):
        original = copy.deepcopy(self.pool)
        for field in ("commit", "declaration", "source_git_blob", "mathlib_commit"):
            self.pool = copy.deepcopy(original)
            self.pool["families"][0]["targets"][0][field] = "changed"
            with self.assertRaises(ValueError):
                self.validate()

    def test_public_cases_cannot_be_promoted_to_hidden_results(self):
        self.pool["held_out"] = True
        with self.assertRaises(ValueError):
            self.validate()

    def test_missing_expert_and_explanation_slots_rejected(self):
        original = copy.deepcopy(self.form)
        self.form["first_pass"]["case_judgments"].pop()
        with self.assertRaises(ValueError):
            self.validate()
        self.form = original
        self.form["second_pass"]["diagnostic_judgments"].pop()
        with self.assertRaises(ValueError):
            self.validate()

    def test_template_cannot_supply_fabricated_grades(self):
        self.form["second_pass"]["diagnostic_judgments"][0]["explanation_correct"] = True
        with self.assertRaises(ValueError):
            self.validate()

    def test_pdf_hash_mismatch_rejected(self):
        self.observations["observations"][0]["sha256"] = "changed"
        with self.assertRaises(ValueError):
            self.validate()
