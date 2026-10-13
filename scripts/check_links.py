"""Check curated declaration locations at pinned commits, without compiling proofs."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from source_adapters.network import fetch_text, source_identity, safe_path

def main():
    data = json.loads((ROOT / 'catalog/results.json').read_text())
    count = 0
    for record in data['results']:
        for proof in record['proofs']:
            repository = source_identity(proof['repository'], proof['commit'])
            url = f'https://raw.githubusercontent.com/{repository}/{proof["commit"]}/{safe_path(proof["file"])}'
            source = fetch_text(url)
            line = source.splitlines()[proof['line'] - 1]
            name = proof['declaration'].split('.')[-1]
            if not re.match(r'^\s*(?:theorem|lemma)\s+' + re.escape(name) + r'(?:\s|$|\.)', line):
                raise ValueError(f'Declaration location changed: {proof["url"]}')
            print(f'Located {proof["declaration"]} at {proof["commit"]}:{proof["line"]}')
            count += 1
    print(f'{count} declaration locations checked; no Lean compilation or audit performed')

if __name__ == '__main__': main()
