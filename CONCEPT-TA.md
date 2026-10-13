# Theorem Atlas — Autonomous Mathematical Formalization

## Vision
Build an open-source, AI-agent-driven system that indexes mathematical results from multiple public sources, links to existing Lean proofs wherever they live, and attempts Lean 4 formalizations for results that lack them. OpenAI's public mathematics repository is the first ingestion source, not the project's permanent scope.

## Goals
- Maintain a result-level catalogue with stable IDs, source manuscript URLs, upstream commit references, and formalization status.
- Do not duplicate existing proofs without reason: link to exact external files, declarations and commits, regardless of hosting organization.
- Autonomously extract theorem statements, map definitions into Lean/Mathlib, plan proofs, execute Lean, diagnose failures, and checkpoint progress.
- Publish reproducible proof artifacts with independent statement-fidelity review.
- Make results and failures visible so community members can contribute.

## Non-goals (initially)
- Claiming that a Lean-compiling statement automatically matches the manuscript.
- Re-proving every result simultaneously.
- Treating agent self-assessment as proof verification.

## Sources and provenance
- First source: OpenAI mathematics repository: https://github.com/openai/math
- Add source adapters for arXiv, journal papers, community formalization repositories, and future mathematical result releases.
- Inspect each source structure before implementing synchronization; paths and counts can change.
- Pin upstream commits for traceability. Respect upstream licenses and attribution.

## Proposed architecture
1. **Source adapters + indexer:** ingest results from multiple providers, identify individual theorem/result families, discover existing Lean formalizations, deduplicate and detect upstream changes.
2. **Statement agent:** translate mathematical claims and assumptions into Lean 4; search Mathlib for definitions.
3. **Statement reviewer:** independently compare the Lean theorem with the source, checking assumptions, quantifiers, definitions, and nontriviality.
4. **Proof agent:** plan lemmas, generate Lean proofs, compile, parse errors, revise strategy, and reuse validated lemmas.
5. **Research/retrieval:** search local Mathlib and proof history for relevant results.
6. **Verifier:** run pinned Lean toolchain in a clean environment; reject sorry/admit, unapproved axioms, and other trust bypasses; inspect `#print axioms` and dependencies.
7. **Publisher:** create auditable GitHub PRs containing source links, proof files, checks, and reproducibility commands.
8. **Static website:** generate a searchable/filterable GitHub Pages catalogue with theorem labels, provenance, proof status, and local or external proof links.

## State machine
- `discovered`: result indexed.
- `statement_draft`: proposed Lean statement.
- `statement_reviewed`: independently checked for fidelity.
- `proof_in_progress`: proof search running.
- `partial`: some lemmas verified.
- `kernel_checked`: proof accepted by Lean.
- `audited`: trust assumptions/dependencies checked.
- `faithful`: human or independent expert review confirms theorem matches source.
- `external_linked`: an existing proof is linked rather than duplicated.

Do not conflate compilation with statement fidelity. Headline verified counts require both audited kernel checking and fidelity review.

## Persistent search loop
Each attempt records: theorem ID, upstream and local commits, model/version, prompts or strategy metadata, generated Lean, compiler diagnostics, validated lemmas, elapsed time, and estimated compute cost. Failed attempts inform replanning; budgets prevent infinite loops. Agents cannot change verifier rules or mark their own submissions as independently reviewed.

## Website and catalogue
GitHub Pages is the public entry point. Each theorem record has a stable ID, title, source organization/publication, paper URL, mathematical domain, statement, formalization status, and zero or more proof references. Each proof reference records host repository, pinned commit, Lean file, declaration, toolchain, audit state, and whether it is locally maintained or external. Labels and filtering must distinguish `unformalized`, `in_progress`, `kernel_checked`, `audited`, and `faithful`; do not equate external links with independent verification. Generate static pages from validated catalogue data.

## Proposed repository layout
```text
README.md
CONCEPT.md
AGENTS.md
lean-toolchain
lakefile.toml
catalog/results.yaml
site/
source_adapters/
Formalization/
agent/
scripts/sync_upstream.py
scripts/verify.py
.github/workflows/lean-ci.yml
```

## MVP
1. Confirm current upstream catalogue format and identify a small set of missing results.
2. Pin Lean 4 and Mathlib; establish a clean `lake build` baseline.
3. Build a catalogue and upstream link checker.
4. Select 10 pilot results: 2 known formalized results as blinded regression tests, 8 unformalized candidates ranked by tractability.
5. Implement one checkpointed agent loop before adding multi-agent orchestration.
6. Achieve one new proof that passes clean kernel verification, dependency audit, and independent statement-fidelity review.
7. Publish a reproducible PR and a candid benchmark report.

## Metrics
- Result coverage and status by category.
- Statement-fidelity pass rate.
- Kernel-checked and independently reviewed proofs.
- Proof search time, attempts, token/compute cost, validated lemmas, and failure modes.
- Upstream sync lag and regression-test outcomes.

## Open questions
- Which manuscripts are easiest to formalize given Mathlib coverage?
- How should theorem-level identity survive manuscript revisions?
- Which models/tools give the best verified-proof yield per unit cost?
- What level of human review is required before calling a result faithful?
- How should community PRs and agent-produced PRs be prioritized?

## First implementation instruction
Read this document and AGENTS.md. Inspect the current OpenAI repository and Mathlib before coding. Propose the smallest executable vertical slice: index one result, generate/check one Lean statement, run one proof attempt, store diagnostics, and produce a reproducible report. Do not claim mathematical success without both proof and statement-fidelity evidence.
