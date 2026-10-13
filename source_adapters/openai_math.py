"""Pinned OpenAI manuscript-family ingestion. Does not assert theorem fidelity."""
import html
import re
import subprocess

REPOSITORY = 'https://github.com/openai/math'
COMMIT = '1581d4cbdd69a0faf34b2089614fe2a814316a6a'


def fetch(path):
    return subprocess.check_output([
        'curl', '--fail', '--silent', '--show-error', '--location',
        '--max-time', '60', f'https://raw.githubusercontent.com/openai/math/{COMMIT}/{path}'
    ], text=True)


def plain(text):
    return html.unescape(re.sub(r'<[^>]+>', '', text)).replace('$`', '').replace('`$', '').strip()


def parse(contents):
    headers = list(re.finditer(r'\*\*(\d{3})\. (.*?)\*\*', contents))
    records = []
    for i, match in enumerate(headers):
        block = contents[match.end():headers[i + 1].start() if i + 1 < len(headers) else len(contents)]
        manuscripts = re.findall(r'\[([^\n]*?)\]\((preprints/[^\n]+?\.pdf)\)', block)
        scope = re.search(r'\[Lean\]\((lean/docs/[^)]+)\)', block)
        records.append({
            'id': f'openai-math:{match[1]}', 'kind': 'result_family',
            'title': plain(match[2]).rstrip('.'), 'source': 'OpenAI mathematics',
            'repository': REPOSITORY, 'upstream_commit': COMMIT,
            'source_url': f'{REPOSITORY}/blob/{COMMIT}/CONTENTS.md',
            'manuscripts': [{'title': plain(title), 'url': f'{REPOSITORY}/blob/{COMMIT}/{path}'} for title, path in manuscripts],
            'status': 'discovered', 'statement': None, 'assumptions': None,
            'fidelity_review': 'unreviewed', 'proofs': [],
            'attribution': 'OpenAI mathematics collection. Family and manuscript titles indexed by Theorem Atlas; proof implementations linked upstream.',
            'license': {'code': 'Apache-2.0', 'materials': 'Apache-2.0 (repository notice)', 'url': f'{REPOSITORY}/blob/{COMMIT}/LICENSE', 'third_party_note': 'External cited publications retain their own terms.'},
            'scope_url': f'{REPOSITORY}/blob/{COMMIT}/{scope[1]}' if scope else None,
        })
    if not records or len({r['id'] for r in records}) != len(records):
        raise ValueError('Unrecognized or duplicate family catalogue; inspect upstream format')
    return records
