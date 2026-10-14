"""Catalogue integrity checks and static packaging; this is not a proof verifier."""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'discovered', 'statement_draft', 'statement_reviewed', 'proof_in_progress',
            'partial', 'kernel_checked', 'audited', 'faithful', 'external_linked'}
SHA = re.compile(r'[0-9a-f]{40}')

def validate(data):
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported catalogue schema')
    ids = set()
    for r in data['results']:
        if r['id'] in ids:
            raise ValueError(f'Duplicate ID: {r["id"]}')
        ids.add(r['id'])
        if not SHA.fullmatch(r['upstream_commit']) or r['status'] not in STATUSES:
            raise ValueError(f'Invalid provenance/status: {r["id"]}')
        if r['kind'] not in {'result_family', 'formalization_project', 'external_proof_artifact', 'external_artifact', 'statement_collection'} or not r['title']:
            raise ValueError(f'Invalid record kind/title: {r["id"]}')
        if r['kind'] == 'result_family' and not r['manuscripts']:
            raise ValueError(f'Missing family manuscript: {r["id"]}')
        if r['kind'] != 'result_family':
            if not r.get('license', {}).get('url', '').startswith('https://') or not r.get('attribution'):
                raise ValueError(f'Missing license attribution: {r["id"]}')
            if r['kind'] == 'external_proof_artifact' and r.get('artifact_url') != r['source_url']:
                raise ValueError('Artifact location must match pinned source')
        for reference in r.get('references', []):
            if not reference['url'].startswith('https://') or not reference['title']:
                raise ValueError('Invalid external publication reference')
        for url in [r['source_url'], *(p['url'] for p in r['manuscripts'])]:
            if not url.startswith('https://') or r['upstream_commit'] not in url:
                raise ValueError(f'Unpinned source: {r["id"]}')
        # Initial release cannot confer audit or fidelity status. Future evidence policy
        # requires independent review before these states can be enabled.
        if r['status'] in {'statement_reviewed', 'partial', 'kernel_checked', 'audited', 'faithful'} or r['fidelity_review'] != 'unreviewed':
            raise ValueError('Review and verification states are not supported in catalogue v1')
        if r['status'] == 'external_linked' and not r['proofs']:
            raise ValueError('External linked status requires a proof reference')
        for p in r['proofs']:
            if (not SHA.fullmatch(p['commit']) or p['commit'] not in p['url']
                or not p['url'].startswith(p['repository'] + '/blob/' + p['commit'] + '/')
                or not p['file'].endswith('.lean') or not p['declaration']
                or not p['url'].endswith(p['file'] + '#L' + str(p['line']))
                or p['audit_state'] != 'not_locally_audited' or p['maintenance'] != 'external'):
                raise ValueError(f'Invalid external proof: {r["id"]}')
    return data

def main():
    data = validate(json.loads((ROOT / 'catalog/results.json').read_text()))
    # Compute the report from the current data; checked-in reports are checkpoints only.
    import sys
    sys.path.insert(0, str(ROOT))
    from scripts.overlaps import annotate, report
    annotate(data['results'])
    data['overlap_report'] = report(data['results'])
    out = ROOT / 'dist'
    out.mkdir(exist_ok=True)
    for name in ['index.html', 'app.js', 'style.css', 'catalogue-state.mjs', 'evidence-state.mjs', 'evidence.json', 'attribution.html']:
        shutil.copyfile(ROOT / 'site' / name, out / name)
    shutil.copytree(ROOT / 'site/licenses', out / 'licenses', dirs_exist_ok=True)
    (out / 'results.json').write_text(json.dumps(data, ensure_ascii=False))
    (out / '.nojekyll').touch()
    print(f'Built dist/ with {len(data["results"])} validated records')

if __name__ == '__main__':
    main()
