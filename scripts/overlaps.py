"""Mechanical catalogue overlap checks; never infer mathematical equivalence."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def repeated(items):
    buckets = defaultdict(set)
    for key, record_id in items:
        buckets[key].add(record_id)
    return [{'key': key, 'record_ids': sorted(ids)} for key, ids in sorted(buckets.items()) if len(ids) > 1]


def report(records):
    return {
        'scope': 'Exact metadata identities only; mathematical statement equivalence has not been reviewed.',
        'exact_artifact_groups': repeated((r['artifact_url'] + '#' + r.get('archive_member', ''), r['id']) for r in records if r.get('artifact_url')),
        'repeated_proof_location_groups': repeated((p['url'], r['id']) for r in records for p in r['proofs']),
        'repeated_manuscript_groups': repeated((m['url'], r['id']) for r in records for m in r['manuscripts']),
        'repeated_benchmark_groups': repeated((r['benchmark_id'], r['id']) for r in records if r.get('benchmark_id')),
        'identical_source_hash_groups': repeated((r['source_sha256'], r['id']) for r in records if r.get('source_sha256')),
        'alternative_proof_records': [r['id'] for r in records if len(r['proofs']) > 1],
        'source_reuse': json.loads((ROOT / 'catalog/relationships.json').read_text()),
    }


def annotate(records):
    relations = json.loads((ROOT / 'catalog/relationships.json').read_text())
    for record in records:
        record['source_relationships'] = [r for r in relations if r['record_id'] == record['id']]
    return records


def main():
    records = json.loads((ROOT / 'catalog/results.json').read_text())['results']
    output = report(records)
    (ROOT / 'catalog/overlap-report.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__': main()
