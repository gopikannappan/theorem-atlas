import hashlib
import io
import json
import unittest
import zipfile
from pathlib import Path
from scripts.overlaps import report
from source_adapters.external import parse_archive

class OverlapTests(unittest.TestCase):
    def setUp(self):
        self.records = json.loads(Path('catalog/results.json').read_text())['results']

    def test_same_catalogue_source_page_is_not_duplicate_artifact(self):
        self.assertEqual(report(self.records)['exact_artifact_groups'], [])
        self.assertEqual(report(self.records)['repeated_manuscript_groups'], [])

    def test_actual_duplicate_artifact_is_detected(self):
        original = next(r for r in self.records if r.get('artifact_url') and not r.get('archive_member'))
        duplicate = dict(original, id='test:duplicate')
        self.assertEqual(len(report([original, duplicate])['exact_artifact_groups']), 1)

    def test_archive_members_do_not_collapse_to_archive_url(self):
        archive = [r for r in self.records if r.get('archive_member')]
        self.assertEqual(len(archive), 438)
        self.assertEqual(report(archive)['exact_artifact_groups'], [])
        self.assertEqual(report(archive)['identical_source_hash_groups'], [])
        self.assertEqual(report(archive)['repeated_benchmark_groups'], [])

    def test_multiple_proofs_share_one_problem_record(self):
        matches = [r for r in self.records if r.get('benchmark_id') == 'imo:2025:p4']
        self.assertEqual(len(matches), 1)
        self.assertEqual(len(matches[0]['proofs']), 2)
        self.assertEqual(report(self.records)['alternative_proof_records'], ['harmonic:imo2025:p4'])

    def test_text_and_statements_are_not_lean_proofs(self):
        p2 = next(r for r in self.records if r['id'] == 'harmonic:imo2025:p2')
        self.assertEqual(p2['kind'], 'external_artifact')
        self.assertEqual(p2['proofs'], [])
        statements = next(r for r in self.records if r['kind'] == 'statement_collection')
        self.assertEqual(statements['proofs'], [])

    def test_archive_checksum_mismatch_fails_before_ingestion(self):
        config = next(c for c in json.loads(Path('catalog/external-sources.json').read_text()) if c['adapter'] == 'archive_inventory')
        with self.assertRaisesRegex(ValueError, 'checksum'): parse_archive(config, b'wrong archive')

    def test_archive_member_count_change_fails_closed(self):
        payload = io.BytesIO()
        with zipfile.ZipFile(payload, 'w') as archive: archive.writestr('test/example.lean', 'test')
        config = {'archive_sha256': hashlib.sha256(payload.getvalue()).hexdigest(), 'expected_members': 438}
        with self.assertRaisesRegex(ValueError, 'inventory'): parse_archive(config, payload.getvalue())

if __name__ == '__main__': unittest.main()
