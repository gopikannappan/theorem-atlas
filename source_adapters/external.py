"""Pinned inventories and curated declaration locations; no proof code is copied."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    return subprocess.check_output(['curl', '-fsSL', '--max-time', '60', url], text=True)


def blob(config, path):
    return f'{config["repository"]}/blob/{config["commit"]}/{path}'


def proof_reference(config, target):
    return {
        'repository': config['repository'], 'commit': config['commit'],
        'file': target['file'], 'line': target['line'], 'declaration': target['declaration'],
        'url': blob(config, target['file']) + '#L' + str(target['line']),
        'toolchain': config['toolchain'], 'mathlib_commit': config['mathlib_commit'],
        'dependencies': target['dependencies'],
        'audit_state': 'not_locally_audited', 'maintenance': 'external',
    }


def base_record(config, identifier, title, path, kind):
    return {
        'id': identifier, 'kind': kind, 'title': title, 'source': config['source'],
        'repository': config['repository'], 'upstream_commit': config['commit'],
        'source_url': blob(config, path), 'manuscripts': [],
        'status': 'discovered', 'statement': None, 'assumptions': None,
        'fidelity_review': 'unreviewed', 'proofs': [], 'scope_url': None,
        'license': config['license'], 'attribution': config['attribution'],
        'origin_note': config['origin_note'], 'model': config['model'],
        'references': [], 'reproduction_commands': config['reproduction_commands'],
    }


def parse_inventory(config, tree):
    if tree.get('truncated'):
        raise ValueError('Truncated upstream inventory; refuse partial ingestion')
    paths = sorted(x['path'] for x in tree['tree'] if x['type'] == 'blob'
                   and x['path'].startswith('APNOutputs/') and x['path'].endswith('.lean'))
    if not paths:
        raise ValueError('No AlphaProof Nexus artifacts found; inspect upstream format')
    records = []
    for path in paths:
        name = Path(path).stem
        title = name.replace('_', ' ').replace('.', ' · ')
        category = path.split('/')[1]
        r = base_record(config, 'alphaproof-nexus:' + path.removeprefix('APNOutputs/'),
                        title, path, 'external_proof_artifact')
        r['category'] = category
        r['artifact_url'] = r['source_url']
        r['metadata_note'] = 'File-level inventory; title derived from upstream filename. Theorem-level identity and coverage are unreviewed.'
        r['references'] = [{'title': 'Upstream research report', 'url': 'https://arxiv.org/abs/2605.22763'}]
        curated = config.get('curated', {}).get(path)
        if curated:
            r['title'] = curated['title']
            r['proofs'] = [proof_reference(config, dict(curated, file=path))]
            r['status'] = 'external_linked'
            if curated.get('prose'):
                r['manuscripts'] = [{'title': 'Accompanying prose proof', 'url': blob(config, curated['prose'])}]
        records.append(r)
    return records


def collect(configs):
    records = []
    for config in configs:
        if config['adapter'] == 'inventory':
            slug = config['repository'].removeprefix('https://github.com/')
            tree = json.loads(fetch(f'https://api.github.com/repos/{slug}/git/trees/{config["commit"]}?recursive=1'))
            records.extend(parse_inventory(config, tree))
        else:
            r = base_record(config, config['id'], config['title'], config['readme'], 'formalization_project')
            r['scope_url'] = r['source_url']
            r['references'] = config['references']
            r['proofs'] = [proof_reference(config, target) for target in config.get('targets', [])]
            if r['proofs']:
                r['status'] = 'external_linked'
            records.append(r)
    return records
