# Atlas–Palomar overlap — 2026-10-14

This is a **source-reference overlap measurement**, not a mathematical equivalence audit or a percentage of theorems verified. [Machine-readable checkpoint](../comparison-reports/palomar-2026-10-14.json).

The bounded [remote comparison](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38641690595) enumerated all **544 current Palomar entries**, representing **447 source projects**, at registry release `1377c2d090125abd17c5440988ed9494e7a4c6e1395e40e2238b179b6dc2e58d`. It read the full records and compared them with the tracked Atlas catalogue: 891 records, including 372 OpenAI result families. The catalogue SHA256 and fetched-data artifact checksum are in the JSON checkpoint. All source responses and their URL/hash manifest are retained in the linked CI artifact for 30 days.

## Results

| Denominator | Direct source identifier or exact normalized source-title candidates | Percentage |
| --- | ---: | ---: |
| OpenAI result families | 4 / 372 | 1.075% |
| Research-family or formalization-project records | 4 / 376 | 1.064% |
| All Atlas records, including benchmarks and a statement collection | 4 / 891 | 0.449% |

The last row is a poor headline metric: benchmark archive members are not research discoveries. The research/project row also mixes families and whole projects; use the OpenAI-family denominator for that release.

One family matched by source identifier; three additional families matched by exact normalized source titles. Five distinct Palomar entries produced these four family candidates. There are **no exact matches** to the curated Atlas proof's repository, commit and selected declaration simultaneously. That zero does not establish zero mathematical overlap: registered formalizations may use wrappers, new declarations or newer source versions.

## Identified connections

| Atlas family | Palomar entries | What the metadata establishes |
| --- | --- | --- |
| 107 — matrix multiplication exponent at most 9/4 | [all fields](https://palomar-registry.org/entry?id=PALOMAR-2026-10-08-000005&version=1), [all rings](https://palomar-registry.org/entry?id=PALOMAR-2026-10-11-000007&version=1) | Explicit adaptation of the family source paper; not the identical Atlas proof snapshot |
| 149 — weakly reversible mass-action systems | [permanence and recovery](https://palomar-registry.org/entry?id=PALOMAR-2026-10-11-000020&version=1) | Adaptation citing two family manuscript titles |
| 238 — Thorp shuffle | [four-row permanent inequality](https://palomar-registry.org/entry?id=PALOMAR-2026-10-08-000007&version=1) | Adaptation of a companion manuscript; does not establish that the Thorp-shuffle headline theorem is registered |
| 367 — one-phase Bernoulli problem | [flatness in dimensions at most six](https://palomar-registry.org/entry?id=PALOMAR-2026-10-14-000010&version=1) | Formalizes an explicitly identified part of the family result; does not establish full-family coverage |

Background and other citations are excluded from direct candidates. In particular, one Palomar entry citing the AlphaProof Nexus research paper does not establish coverage of all 71 Atlas proof artifacts carrying that same reference. The measurement detects 74 Atlas records with background/other references, but these are not 74 overlapping verified results.

## Method and limits

- Enumerate current registry IDs using its bounded results API, follow every cursor, require one registry release and reconcile the row count with the declared total.
- Read every current versioned entry; retain source snapshots and hashes.
- Match source identifiers or locations conservatively. For GitHub preprints, normalize only the same preprint directory and its conventional paper.pdf/paper.tex representations; different source revisions remain explicit limitations. Custom PDF filenames still require exact source-title matching.
- Count a family once even when multiple manuscripts or registrations connect to it.
- Require a mathematical-source relationship of formalizes, adapts or independently-proves for direct candidates. Do not count background citations or reused dependencies.
- Perform no fuzzy title matching, semantic-equivalence inference, proof execution or evidence-state promotion.

A full traversal does not make the matching semantically complete. Different titles, identifiers, manuscript layouts and original-result metadata may hide further connections. Conversely, a matched source may support a partial formalization, extension or different result. **Do not describe the figures as 98.9% unique mathematics, 1.1% fully verified families, or the percentage overlap of the two products' functionality.**

## Reproduction

The script is `scripts/measure_palomar_overlap.py`. Two bounded remote measurements were run: [initial strict source/title matching](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38641399724) and the cited second run after adding preprint-directory/TeX locator handling and negative tests. Both identified the same four family candidates. No local commands ran.

The live-data job is now restricted to explicit workflow dispatch; PR updates skip it to avoid repeat network reads when checkpointing results. The existing catalogue CI continues to run and tests matching helpers offline. A future measurement must retain its own source release, timestamp, catalogue hash and artifacts.
