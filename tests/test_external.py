import copy
import json
import unittest
from pathlib import Path
from source_adapters.external import parse_inventory
from scripts.catalogue import validate

class ExternalSourceTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path('catalog/results.json').read_text())
        self.config = next(c for c in json.loads(Path('catalog/external-sources.json').read_text()) if c['adapter'] == 'inventory')

    def test_complete_external_inventory_counts(self):
        records = self.data['results']
        self.assertEqual(sum(r['kind'] == 'external_proof_artifact' for r in records), 513)
        self.assertEqual(sum(r['kind'] == 'formalization_project' for r in records), 4)
        self.assertEqual(sum(bool(r['proofs']) for r in records), 12)
        self.assertEqual(sum(len(r['proofs']) for r in records), 13)
        self.assertEqual({r['source'] for r in records}, {'OpenAI mathematics', 'Anthropic / Claude', 'Google DeepMind / AlphaProof Nexus', 'Harmonic / Aristotle', 'Math Inc. / Gauss', 'DeepSeek / Prover-V2', 'Google DeepMind / Formal Conjectures'})

    def test_truncated_inventory_fails_closed(self):
        with self.assertRaises(ValueError): parse_inventory(self.config, {'truncated': True, 'tree': []})

    def test_no_invented_manuscripts_or_declarations(self):
        tree = {'truncated': False, 'tree': [
            {'path': 'APNOutputs/OEIS/example.lean', 'type': 'blob'},
            {'path': 'README.md', 'type': 'blob'}]}
        record = parse_inventory(self.config, tree)[0]
        self.assertEqual(record['proofs'], [])
        self.assertEqual(record['manuscripts'], [])
        self.assertEqual(record['status'], 'discovered')
        self.assertEqual(record['kind'], 'external_proof_artifact')
        self.assertIn(self.config['commit'], record['artifact_url'])

    def test_missing_license_attribution_is_rejected(self):
        r = next(r for r in self.data['results'] if r['kind'] == 'formalization_project')
        del r['license']
        with self.assertRaises(ValueError): validate(self.data)

    def test_artifact_location_must_match_pinned_source(self):
        r = next(r for r in self.data['results'] if r['kind'] == 'external_proof_artifact')
        r['artifact_url'] = r['repository'] + '/blob/main/example.lean'
        with self.assertRaises(ValueError): validate(self.data)

if __name__ == '__main__': unittest.main()
