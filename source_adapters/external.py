"""Pinned inventories and curated declaration locations; no proof code is copied."""
import hashlib
import io
import zipfile
import json
from source_adapters.network import fetch_text, fetch_bytes, safe_path, source_identity
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    return fetch_text(url)


def blob(config, path):
    source_identity(config['repository'], config['commit'])
    return f'{config["repository"]}/blob/{config["commit"]}/{safe_path(path)}'


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


def parse_archive(config, payload):
    digest = hashlib.sha256(payload).hexdigest()
    if digest != config['archive_sha256']:
        raise ValueError('Proof archive checksum mismatch')
    records = []
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        members = sorted(info for info in archive.namelist() if info.endswith('.lean') and not info.startswith('__MACOSX/'))
        if len(members) != len(set(members)) or len(members) != config['expected_members']:
            raise ValueError('Unexpected or duplicate archive member inventory')
        infos = [archive.getinfo(member) for member in members]
        if (len(archive.infolist()) > 5000 or sum(info.file_size for info in infos) > 64 * 1024 * 1024
            or any(info.file_size > 8 * 1024 * 1024 or info.flag_bits & 1 for info in infos)):
            raise ValueError('Archive exceeds decompression budget or contains encrypted members')
        for member in members:
            safe_path(member)
            # Read bytes only to record exact identity; never extract or execute code.
            body = archive.read(member)
            name = Path(member).stem
            r = base_record(config, config['id_prefix'] + member, name.replace('_', ' '),
                            config['archive_path'], 'external_proof_artifact')
            r.update(artifact_url=r['source_url'], archive_member=member,
                     archive_sha256=digest, source_sha256=hashlib.sha256(body).hexdigest(),
                     benchmark_id='minif2f:' + name, category='miniF2F / ' + member.split('/')[0],
                     metadata_note='Archive member indexed by filename. Download the pinned ZIP and locate this member; no individual Lean declaration URL is available. Toolchain and dependencies were not supplied in the release.')
            r['references'] = config['references']
            records.append(r)
    if len({r['benchmark_id'] for r in records}) != len(records):
        raise ValueError('Repeated miniF2F problem ID; review before indexing')
    return records


def collect(configs):
    records = []
    for config in configs:
        if config['adapter'] == 'inventory':
            slug = source_identity(config['repository'], config['commit'])
            tree = json.loads(fetch(f'https://api.github.com/repos/{slug}/git/trees/{config["commit"]}?recursive=1'))
            records.extend(parse_inventory(config, tree))
        elif config['adapter'] == 'archive_inventory':
            slug = source_identity(config['repository'], config['commit'])
            payload = fetch_bytes(f'https://raw.githubusercontent.com/{slug}/{config["commit"]}/{safe_path(config["archive_path"])}', max_bytes=64 * 1024 * 1024)
            records.extend(parse_archive(config, payload))
        elif config['adapter'] == 'project':
            kind = config.get('kind', 'formalization_project')
            r = base_record(config, config['id'], config['title'], config.get('record_path', config['readme']), kind)
            r['scope_url'] = blob(config, config['readme'])
            if kind in {'external_artifact', 'external_proof_artifact'}:
                r['artifact_url'] = r['source_url']
            for field in ['benchmark_id', 'metadata_note']:
                if field in config: r[field] = config[field]
            r['references'] = config['references']
            r['proofs'] = [proof_reference(config, target) for target in config.get('targets', [])]
            if r['proofs']:
                r['status'] = 'external_linked'
            records.append(r)
        else:
            raise ValueError('Unknown external adapter: ' + config['adapter'])
    return records
