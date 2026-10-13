# Security policy

## Private reporting

Report vulnerabilities using this repository's **Security → Report a vulnerability** feature: [private report](https://github.com/theorem-atlas/theorem-atlas/security/advisories/new). Do not include exploit details or secrets in public issues. Include the affected commit, minimal reproduction, impact, and relevant environment. The project has no promised response-time SLA; reports are handled by the maintainer.

The supported version is the current `main` branch. Pinned external Lean sources are third-party artifacts and have not been audited locally; report upstream vulnerabilities to their maintainers too, and notify this project when its catalogue links or local tooling are affected.

## Trust boundaries

- The published app is a static catalogue. It has no login, server-side data storage, or API credentials. Source metadata is untrusted input; the browser renders it as text and accepts only HTTPS outbound URLs.
- Source adapters inspect pinned public files and inventories. They must not execute upstream code, extract archive members to disk, interpolate source values into shell commands, or follow downloads to non-HTTPS/local destinations.
- Compressed archive checksums, member counts, decompression limits, and safe member paths are enforced before member data is read. A digest establishes byte identity, not proof correctness.
- PR checks run with read-only tokens and do not deploy. Checkout credentials are not persisted. Only `main` can deploy through the Pages environment; deployment gets Pages/OIDC permissions rather than repository write access.
- Actions are pinned to commit SHAs, updated through reviewed Dependabot PRs, and restricted in repository settings. Private vulnerability reporting and existing secret scanning/push protection are enabled.
- Browser CSP is supplied through HTML metadata because GitHub Pages does not provide arbitrary response-header configuration. It restricts scripts, connections, forms, and embedded objects. This is not a complete header-based security policy; meta CSP cannot enforce `frame-ancestors`.

## Lean execution

`run_pilot.py` executes only the fixed, tracked experiment. Its temporary working directory is build isolation, not an OS security sandbox. The catalogue CI never runs Lean. Do not feed arbitrary upstream or PR-generated Lean into this runner: elaboration can execute host code. A disposable container or stronger isolation with no credentials/network and bounded resources is required for a future general proof runner. That runner and independent proof verification are not delivered by the static catalogue.

## Repository administration

See [repository security checkpoint](docs/REPOSITORY_SECURITY.md) for actual checked settings and any limits. Branch protection applies to administrators too. All changes to `main` require a PR, Code Owner approval, and a passing up-to-date build. Administrators retain the ability to change repository settings, so this is an enforced branch policy, not removal of administrative control. After an organization transfer, recheck security controls and update CODEOWNERS to real maintainer teams rather than guessed team names.
