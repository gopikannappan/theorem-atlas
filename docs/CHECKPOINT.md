# First development checkpoint

## Delivered

- Commit-pinned source adapter; 372 family records and 719 manuscript references.
- Static searchable catalogue, evidence filters, URL state, data download, responsive layout.
- One curated external declaration: `OAI.InternalCatalan.catalan_irrational`, Conclusions.lean line 11. Scope notes alone do not become proof references.
- A bounded supporting-lemma experiment with retained failed diagnostics and compiler acceptance evidence; no fidelity or audit claim.
- Metadata checks and GitHub Pages build/deployment workflow.

## Inspection findings

OpenAI mathematics: `1581d4cbdd69a0faf34b2089614fe2a814316a6a`.
Upstream Lean: `leanprover/lean4:v4.34.1`; upstream Mathlib: `d13f23b723b8a846827a245b89c10fc7d3f11612`.
Inspected Mathlib head: `a646a376b8dae3a215700a465ecc57c74cd1adb3` using Lean v4.35.0-rc4. It is not substituted for upstream's pinned dependency.

The Catalan comparator statement contains a placeholder. The separate solution declaration has an explicit proof. Neither the comparator nor the solution was locally audited. Upstream documentation distinguishes supporting-result comparisons from main theorem comparisons; coverage must be inspected individually.

The first Python HTTPS fetch failed due to the local certificate configuration. Fetching with system curl succeeded with normal certificate validation. No certificate checks were disabled.

## Validation

Nine metadata/adapter tests pass. Static build, JavaScript syntax check, and HTTP responses for index.html, app.js, style.css, and results.json pass. The curated external declaration was located at its pinned line using `python3 scripts/check_links.py`; this is a source-location check only. The same-commit synchronization preserved its curated reference.

## Next milestones

1. Extract and review individual theorem identities, complete statements, assumptions, and disciplines. Families are not theorem counts.
2. Resolve scope notes into exact declarations and distinguish supporting results from main theorem coverage. Add another source adapter.
3. Establish an independently maintained verifier/evidence policy with pinned dependency closure and reproducible isolated builds; the generation runner must not approve it.
4. Select tractable missing results and regression examples after manuscript and Mathlib inspection, with explicit budgets. The current denominator experiment is infrastructure work, not a new manuscript formalization.
5. Obtain independent statement-fidelity review, then attempt a reviewed main theorem. Report failures and progress candidly.

No new main theorem proof, local external-proof audit, statement-fidelity review, is claimed. GitHub Pages publication is configured through the repository workflow. Browser interaction and visual QA remain untested in this environment.
