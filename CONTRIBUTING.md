# Contributing to Theorem Atlas

Contributions can improve the catalogue, add source adapters, repair the browser experience, or document proof attempts. Start with a catalogue-correction or bug issue, or open a small pull request for a clear fix. Follow [AGENTS.md](AGENTS.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## Set up and check

Use Python 3.11+ and Node.js 24 (the CI version). Catalogue builds have no third-party runtime dependencies. Source synchronization additionally uses curl and network access.

```sh
python3 -m unittest discover -s tests -v
node --test tests/catalogue-state.test.mjs
node --input-type=module --check < site/app.js
python3 scripts/catalogue.py
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Create a branch or fork, make a focused change, run the relevant checks, and open a PR against `main`. CI performs metadata checks and static packaging; it does not audit external proofs. Screenshots are useful for visual changes but do not replace interaction checks. Include observed validation limits in your PR.

## Catalogue changes

- Edit `catalog/external-sources.json` for curated external source metadata, not generated rows in `catalog/results.json`.
- Change an OpenAI pin in its adapter only after inspecting the new upstream format. Regenerate and review the catalogue diff.
- Include an exact upstream commit, source manuscript/publication link, and a precise Lean file and declaration where available. Archive members need the archive hash and member path; do not invent a direct declaration URL.
- Preserve known Lean/Mathlib pins. Mark absent pins, licensing, statements, assumptions, or fidelity review as unknown/unreviewed.
- Include attribution and a license link. Linking is preferred; inspect applicable licenses before copying code or prose. Read [source licensing](docs/LICENSES.md).
- Distinguish a family, manuscript, project, artifact, statement, and theorem. They are not interchangeable counting units.
- Group alternative proofs of a known problem, document upstream reuse in `catalog/relationships.json`, and do not merge mathematical statements from title similarity alone.

After a source change, run the relevant sync command, `python3 scripts/check_links.py`, `python3 scripts/overlaps.py`, and the checks above. Link checks use network access and only locate declarations; CI remains offline and reproducible from tracked data.

## Proof work and independent review

Proof generation and verification/review are separate responsibilities. Authors and agents must not approve their own mathematical statement fidelity or modify verification rules to accept a submission. Do not weaken statements, alter assumptions, or redefine concepts to make a proof compile. Statement changes require explicit independent review.

Persist generated sources, failed attempts, compiler diagnostics, budgets, dependencies, and reproduction instructions. Use pinned toolchains and isolated builds. No trust bypass may be used to claim a verified proof. Axioms output is one diagnostic, not a sufficient audit. The existing `run_pilot.py` only runs a fixed, reviewed infrastructure example; it is not a sandbox for arbitrary contributed Lean. Never execute unknown Lean on your host or in credential-bearing CI.

The catalogue's supported published states remain `discovered` and `external_linked` (with unreviewed drafts/in-progress work permitted by the schema). Audited or faithful status is not currently accepted. New audit policy is a separate, independently reviewed project, not part of a generated-proof PR.

## Reviews and licensing

The human maintainer reviews contributions; Code Owners review is required for protected-branch PRs. Workflow and trust/evidence-related changes need focused human scrutiny. CI success alone does not approve a theorem or a source's statement fidelity.

Original project code is Apache-2.0. By submitting original code, you license that contribution under the project's license. Existing upstream material retains its original terms; preserve source credit and do not claim ownership or blanket relicensing. No CLA is required. Do not submit material you lack permission to contribute.

Never include credentials, personal data, dependency caches, or built artifacts. For security issues, use [private reporting](SECURITY.md) instead of public issues.
