"""Refresh pinned external inventories, retaining the other sources."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from source_adapters.external import collect
from scripts.catalogue import validate
ROOT = Path(__file__).resolve().parents[1]


def main():
    configs = json.loads((ROOT / 'catalog/external-sources.json').read_text())
    records = collect(configs)
    path = ROOT / 'catalog/results.json'
    data = json.loads(path.read_text())
    data['results'] = [r for r in data['results'] if not r['id'].startswith(('anthropic:', 'alphaproof-nexus:'))] + records
    validate(data)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    print(f'Indexed {len(records)} external projects/artifacts; {len(data["results"])} total records')

if __name__ == '__main__': main()
