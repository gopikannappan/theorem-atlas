import copy
import json
import unittest
from pathlib import Path
from scripts.catalogue import validate
from source_adapters.openai_math import parse

class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path('catalog/results.json').read_text())

    def test_live_snapshot_integrity(self):
        validate(self.data)
        self.assertEqual(len(self.data['results']), 372)
        self.assertEqual(sum(len(r['manuscripts']) for r in self.data['results']), 719)

    def test_reject_duplicate_id(self):
        self.data['results'].append(copy.deepcopy(self.data['results'][0]))
        with self.assertRaises(ValueError): validate(self.data)

    def test_reject_unpinned_source(self):
        self.data['results'][0]['upstream_commit'] = 'main'
        with self.assertRaises(ValueError): validate(self.data)

    def test_reject_unsupported_verification_claim(self):
        self.data['results'][0]['status'] = 'faithful'
        with self.assertRaises(ValueError): validate(self.data)

    def test_reject_external_audit_claim(self):
        r = next(r for r in self.data['results'] if r['proofs'])
        r['proofs'][0]['audit_state'] = 'audited'
        with self.assertRaises(ValueError): validate(self.data)

    def test_reject_missing_declaration(self):
        r = next(r for r in self.data['results'] if r['proofs'])
        r['proofs'][0]['declaration'] = ''
        with self.assertRaises(ValueError): validate(self.data)

    def test_parentheses_in_manuscript_path(self):
        result = parse('**123. Fillings.**\n[CAT(0)](preprints/CAT(0)/paper.pdf)')[0]
        self.assertTrue(result['manuscripts'][0]['url'].endswith('preprints/CAT(0)/paper.pdf'))

    def test_adapter_fails_closed_on_unknown_format(self):
        with self.assertRaises(ValueError): parse('upstream format changed')

    def test_family_parsing_and_entities(self):
        result = parse('**123. A &amp; B.** ([Lean](lean/docs/123.md))\n&emsp;[Paper](preprints/example/paper.pdf)')[0]
        self.assertEqual(result['title'], 'A & B')
        self.assertEqual(result['kind'], 'result_family')
        self.assertEqual(result['status'], 'discovered')
        self.assertEqual(len(result['proofs']), 0)

if __name__ == '__main__': unittest.main()
