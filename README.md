# Theorem Atlas

An open, source-agnostic catalogue of mathematical results and pinned Lean proof references. The first source adapter is OpenAI's public mathematics collection. See [the concept](CONCEPT-TA.md) and [operating rules](AGENTS.md).

The first slice indexes **372 result families and 719 manuscripts** at upstream commit `1581d4cbdd69a0faf34b2089614fe2a814316a6a`. These are upstream claims, not independently endorsed mathematical results. One external Catalan proof has a curated declaration link. Other families may have upstream scope notes; absence of a curated proof link does not mean no proof exists.

Public catalogue: <https://gopikannappan.github.io/theorem-atlas/>.

## Run locally

Python 3.11+ and curl are sufficient for catalogue builds; Node.js 18+ runs the pagination tests; there are no Python packages to install.

```sh
python3 -m unittest discover -s tests -v
node --test tests/catalogue-state.test.mjs
python3 scripts/catalogue.py
python3 -m http.server 8000 --directory dist
```

Open <http://localhost:8000>. Tiles are the default; switch to List and paginate with 12, 24, or 48 results per page. View, page, and page size are reflected in shareable URLs. Search titles, manuscripts, declaration names, and family IDs; filter sources and evidence. Filters are reflected in the URL. Expand a record for pinned manuscript and proof provenance. Download the catalogue as JSON.

## Synchronize

```sh
python3 scripts/sync_upstream.py
python3 scripts/check_links.py
python3 scripts/catalogue.py
```

The adapter fetches an exact commit, not a moving branch. To adopt a new upstream version, inspect its format, change the adapter pin, run synchronization and review the diff. Curated fields survive same-commit refreshes. A new commit resets this adapter's statement/proof fields for review. Other adapters' records are retained. Do not edit generated title/manuscript fields manually.

## Lean experiment

```sh
elan toolchain install leanprover/lean4:v4.34.1
python3 scripts/run_pilot.py
```

The bounded pilot tries a generated natural-number denominator lemma relevant to Catalan's series, using Lean core. Each invocation creates a fresh temporary compilation directory and persists both failed and successful sources, diagnostics, strategy, budgets, timing, provenance, and source hashes in `attempts/`. It uses at most two attempts and 30 seconds per attempt. It does not approve its own statement fidelity or confer catalogue verification status.

The initial attempt fails; Lean's error recovery prints `sorryAx` for that failed declaration. It is rejected. The second attempt compiles and reports `propext`. This is compiler evidence for a small supporting statement only. The main Catalan proof has **not** been compiled or audited locally; Mathlib has **not** been built locally. Its upstream Lean/Mathlib pins are recorded in `catalog/sources.json` and the proof reference, not installed as a local project dependency.

## Publish

The workflow validates and builds the static catalogue on pull requests. On `main`, it deploys `dist/` to GitHub Pages. The repository uses **GitHub Actions** as its Pages source. The public catalogue is served at <https://gopikannappan.github.io/theorem-atlas/>.

## Evidence boundaries

`discovered` means indexed. `external_linked` means a pinned declaration has been located, not checked locally. The schema reserves the concept's later states, but v1 rejects audit, kernel-check, or fidelity claims until an independently reviewed evidence policy exists. The catalogue validator is a metadata integrity check, **not a proof verifier**. The experiment runner records compiler results and does not audit arbitrary Lean code.

See [development checkpoint](docs/CHECKPOINT.md) for remaining work. Source material belongs to its upstream authors; the OpenAI repository identifies its license as Apache-2.0. Proof implementations are linked rather than copied.
