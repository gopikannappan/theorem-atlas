"""Refresh only this adapter's records; preserve other sources and curated fields."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from source_adapters.openai_math import COMMIT, fetch, parse

ROOT = Path(__file__).resolve().parents[1]

def main():
    records = parse(fetch('CONTENTS.md'))
    path = ROOT / 'catalog/results.json'
    old = json.loads(path.read_text())['results'] if path.exists() else []
    prior = {r['id']: r for r in old}
    for record in records:
        previous = prior.get(record['id'])
        if previous and previous['upstream_commit'] == COMMIT:
            for field in ['status', 'statement', 'assumptions', 'fidelity_review', 'proofs']:
                record[field] = previous[field]
    records += [r for r in old if not r['id'].startswith('openai-math:')]
    path.write_text(json.dumps({'schema_version': 1, 'results': records}, indent=2, ensure_ascii=False) + '\n')
    print(f'Catalogue contains {len(records)} records after OpenAI refresh at {COMMIT}')

if __name__ == '__main__':
    main()
