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

## Catalogue browsing update

Tiles are the default with an accessible List toggle. Pagination supports 12/24/48 results, previous/next controls, and direct page selection. Search and filter changes reset pagination. URL parameters preserve view, page, filters, and page size. Four Node tests cover pagination bounds, empty results, and evidence filters. The UI distinguishes the 242 upstream scope notes from the single curated proof declaration.

## Validation

Nine metadata/adapter tests pass. Static build, JavaScript syntax check, and HTTP responses for index.html, app.js, style.css, and results.json pass. The curated external declaration was located at its pinned line using `python3 scripts/check_links.py`; this is a source-location check only. The same-commit synchronization preserved its curated reference.

## Next milestones

1. Extract and review individual theorem identities, complete statements, assumptions, and disciplines. Families are not theorem counts.
2. Resolve scope notes into exact declarations and distinguish supporting results from main theorem coverage. Add another source adapter.
3. Establish an independently maintained verifier/evidence policy with pinned dependency closure and reproducible isolated builds; the generation runner must not approve it.
4. Select tractable missing results and regression examples after manuscript and Mathlib inspection, with explicit budgets. The current denominator experiment is infrastructure work, not a new manuscript formalization.
5. Obtain independent statement-fidelity review, then attempt a reviewed main theorem. Report failures and progress candidly.

No new main theorem proof, local external-proof audit, or statement-fidelity review is claimed. GitHub Pages publication is configured through the repository workflow. Browser interaction and visual QA remain untested in this environment.

## Additional source checkpoint

Added three Anthropic projects and all 71 AlphaProof Nexus `APNOutputs/` Lean files, with source-specific kinds, pinned commits, toolchains/Mathlib revisions, original-source references, reproduction commands, and license attribution. Seven catalogue records now have curated declaration links. Source-location checking succeeded for all seven; this does not audit the proofs. No upstream proof source or manuscript content is copied. See LICENSES.md and catalog/external-sources.json for review evidence and exact pins.

The FLT recursive GitHub tree response was truncated; it was not used for ingestion. The adapter indexes that project's curated headline metadata directly. The complete AlphaProof Nexus tree was not truncated and its adapter rejects truncated inventories. Some exploratory candidate paths returned HTTP 404; declaration locations were resolved in the actual solution library rather than using comparator statement files.

## Remaining sources and overlaps checkpoint

Added Harmonic (four Lean problem records, one text artifact), Gauss StrongPNT, 438 DeepSeek miniF2F archive members, and a collection-level Formal Conjectures entry. Total: 891 catalogue records. DeepSeek archive SHA-256 is aa40d80045b6c9b4da34476aa8142fa5979c290970e50fc148077aa78a4ed6ce. No source was executed or copied into repository proof files; the archive was read only for filenames and identity hashes. Toolchain/dependency pins absent from that archive remain unknown.

Two alternative Harmonic problem-4 proofs are grouped under one record. OpenAI’s exact StrongPNT dependency and AlphaProof Nexus’s older Formal Conjectures dependency are documented from pinned manifests. Mechanical checks found no repeated artifact identities, declaration URLs, manuscript links, benchmark IDs, or available source hashes across separate records. This does not establish absence of equivalent mathematical statements.

The first overlap implementation mistakenly grouped records sharing the OpenAI manuscript-map URL; it was corrected before publication to compare artifact identities only. Regression tests distinguish shared source pages from repeated artifacts and distinguish ZIP members sharing one URL.

## Record detail interaction

Replaced inline card expansion with clickable card/row links and a native modal dialog, full-screen on narrow displays. Sources, manuscripts, proofs, provenance, licensing and overlap notes are rendered in the panel on demand. The fragment `#record=<encoded-id>` provides direct record links while keeping the catalogue query parameters. Normal clicks add a history entry, so Back dismisses the panel; direct record-link dismissal removes its fragment without leaving the site. Native dialog handles keyboard focus containment and restoration, and Escape/backdrop/Close dismiss the panel. Modified link clicks retain native new-tab behavior. Record-ID encoding tests cover archive member paths and invalid fragments.
