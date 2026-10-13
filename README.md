# Theorem Atlas

An open, source-agnostic catalogue of mathematical results and pinned Lean proof references. Sources include OpenAI mathematics, Anthropic / Claude, and Google DeepMind / AlphaProof Nexus, Harmonic / Aristotle, Math Inc. / Gauss, DeepSeek / Prover-V2, and Formal Conjectures. See [the concept](CONCEPT-TA.md) and [operating rules](AGENTS.md).

The catalogue contains **891 records**:

| Source | Indexed units |
| --- | --- |
| OpenAI mathematics | 372 families / 719 manuscripts |
| Anthropic / Claude | 3 formalization projects |
| AlphaProof Nexus | 71 Lean artifacts |
| Harmonic / Aristotle | 4 Lean problem records and 1 text artifact; problem 4 has two proof links |
| Math Inc. / Gauss | 1 formalization project |
| DeepSeek / Prover-V2 | 438 Lean archive members: 217 test and 221 validation |
| Formal Conjectures | 1 statement-collection entry; individual conjectures are not ingested |

Twelve records have 13 curated Lean declaration links. All external proofs remain locally unaudited. These units are not a count of distinct mathematical theorems or discoveries.

Each source is pinned to an exact commit. Anthropic entries cover FLT, zeta zeros, and 3SUM/APSP. AlphaProof Nexus entries inventory every released `.lean` file under `APNOutputs/`; the inventory does not independently endorse completeness or manuscript fidelity. Original mathematical authors and formalizing model are distinguished in provenance notes.

Public catalogue: <https://theorem-atlas.github.io/theorem-atlas/>.

Contributions are welcome: see [CONTRIBUTING.md](CONTRIBUTING.md), [community conduct](CODE_OF_CONDUCT.md), and [private security reporting](SECURITY.md). Original project code is [Apache-2.0](LICENSE); upstream materials retain their own terms.

## Run locally

Python 3.11+ and curl are sufficient for catalogue builds; Node.js 24 matches CI and runs the browser-state tests; there are no Python packages to install.

```sh
python3 -m unittest discover -s tests -v
node --test tests/catalogue-state.test.mjs
python3 scripts/catalogue.py
python3 -m http.server 8000 --directory dist
```

Open <http://localhost:8000>. Tiles are the default; switch to List and paginate with 12, 24, or 48 results per page. View, page, and page size are reflected in shareable URLs. Search titles, manuscripts, declaration names, and family IDs; filter sources and evidence. Filters are reflected in the URL. Click a tile or row to open its detail overlay with pinned manuscript and proof provenance. Escape, Close, or a backdrop click returns to the catalogue; browser Back closes a panel opened from the catalogue. Record links preserve filters, view, and page and can be shared or opened in a new tab. Download the catalogue as JSON.

## Synchronize

```sh
python3 scripts/sync_upstream.py
python3 scripts/sync_external.py
python3 scripts/check_links.py
python3 scripts/overlaps.py
python3 scripts/catalogue.py
```

The adapters fetch exact commits, not moving branches. External source pins, curated targets, reproduction commands, and license metadata are in `catalog/external-sources.json`. Refreshing an external source regenerates its catalogue records from this manifest; edit that manifest for curated metadata. To adopt a new upstream version, inspect its format, change the adapter pin, run synchronization and review the diff. Curated fields survive same-commit refreshes. A new commit resets this adapter's statement/proof fields for review. Other adapters' records are retained. Do not edit generated title/manuscript fields manually.

## Lean experiment

```sh
elan toolchain install leanprover/lean4:v4.34.1
python3 scripts/run_pilot.py
```

The bounded pilot tries a generated natural-number denominator lemma relevant to Catalan's series, using Lean core. Each invocation creates a fresh temporary compilation directory and persists both failed and successful sources, diagnostics, strategy, budgets, timing, provenance, and source hashes in `attempts/`. It uses at most two attempts and 30 seconds per attempt. It does not approve its own statement fidelity or confer catalogue verification status.

The initial attempt fails; Lean's error recovery prints `sorryAx` for that failed declaration. It is rejected. The second attempt compiles and reports `propext`. This is compiler evidence for a small supporting statement only. The main Catalan proof has **not** been compiled or audited locally; Mathlib has **not** been built locally. Its upstream Lean/Mathlib pins are recorded in `catalog/sources.json` and the proof reference, not installed as a local project dependency.

## CI proof candidate

[Integer complexity of powers of three](proofs/integer-complexity/README.md) completes an unfinished source formulation by proving a bridge to an existing pinned Lean proof. The candidate compiles in [remote CI](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38419766281) with pinned Lean/Mathlib and retained axiom diagnostics. It remains independently unreviewed; the catalogue is not promoted. All builds for this contribution run in GitHub CI, with candidate compilation inside a read-only, offline container. See its [attempt log](proofs/integer-complexity/ATTEMPTS.md) and provenance.

## Publish

The workflow validates and builds the static catalogue on pull requests. On `main`, it deploys `dist/` to GitHub Pages. The repository uses **GitHub Actions** as its Pages source. The public catalogue is served at <https://theorem-atlas.github.io/theorem-atlas/>.

## Evidence boundaries

`discovered` means indexed. `external_linked` means a pinned declaration has been located, not checked locally. The schema reserves the concept's later states, but v1 rejects audit, kernel-check, or fidelity claims until an independently reviewed evidence policy exists. The catalogue validator is a metadata integrity check, **not a proof verifier**. The experiment runner records compiler results and does not audit arbitrary Lean code.

See [development checkpoint](docs/CHECKPOINT.md) for remaining work. Source material belongs to its upstream authors; the OpenAI repository identifies its license as Apache-2.0. Catalogue proof implementations are linked rather than copied. The CI proof candidate selectively extracts licensed definitions and a witness helper; the full reused proof is imported at a pinned commit.

## Source licensing

Licenses and attribution are visible in each record and on the deployed [Sources & licenses page](https://theorem-atlas.github.io/theorem-atlas/attribution.html). See [license review](docs/LICENSES.md). Anthropic code is Apache-2.0; AlphaProof Nexus code is Apache-2.0 and its other materials are CC BY 4.0, subject to third-party terms. Implementations and manuscripts are linked, not copied.

## Overlap handling

Harmonic’s two IMO 2025 problem-4 proofs are grouped in one record. Source reuse is recorded separately: OpenAI’s pinned dependency manifest already includes the exact Gauss StrongPNT commit, and AlphaProof Nexus depends on an older Formal Conjectures snapshot. These are reuse relationships, not independently reviewed mathematical equivalences.

`python3 scripts/overlaps.py` checks exact artifact identities, declaration URLs, manuscript URLs, benchmark IDs, and source hashes where available. ZIP-member identity includes the member path, so 438 files sharing one archive URL do not collapse into one record. Shared catalogue README/map URLs are not treated as duplicate artifacts. No automatic title-based merging occurs. The generated report is visible in the catalogue and stored in `catalog/overlap-report.json`.

DeepSeek’s ZIP has no release toolchain or Mathlib manifest; these are left unknown rather than fabricated. Harmonic and Math Inc. have no repository-wide LICENSE file at the inspected commits; DeepSeek’s proof-archive rights are not explicitly established by its model agreement. These sources remain metadata/link entries. See Sources & licenses before copying any material.

Repository administration and organization-transfer preparation are recorded in [security checkpoint](docs/REPOSITORY_SECURITY.md) and [organization transfer guide](docs/ORGANIZATION_TRANSFER.md).
