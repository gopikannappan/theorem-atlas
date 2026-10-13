# Repository security checkpoint — 2026-10-13

This is the configuration inspected and applied for `theorem-atlas/theorem-atlas`. It is hardening evidence, not a guarantee that the repository or its external mathematics is vulnerability-free.

## GitHub controls

| Control | Checked state |
| --- | --- |
| Secret scanning / push protection | Enabled; zero open secret-scanning alerts at inspection |
| Private vulnerability reporting | Enabled |
| Dependabot security alerts / automated fixes | Enabled; weekly GitHub Actions dependency PR configuration tracked |
| CodeQL | Default setup configured for JavaScript/TypeScript and Python, weekly schedule; initial setup succeeded, zero open alerts at inspection |
| `main` checks | Up-to-date `build` required from GitHub Actions app 15368 |
| PR reviews | One approving review, Code Owner review, stale approval dismissal, and approval after last push |
| Merge hygiene | Conversation resolution and linear history required; force pushes and deletion disabled; squash/rebase available, merged branches deleted |
| Administrator bypass | Temporarily available (`enforce_admins=false`) until a trusted second maintainer can independently review owner-authored PRs |
| Actions policy | GitHub-owned Actions only; other verified/third-party Actions not allowed; full SHA pinning required |
| Default workflow token | Read-only; cannot approve PR reviews |
| Pages environment | Deployment branch policy permits `main`; workflow also checks the branch and excludes PRs |

No extra collaborators were invited. No credentials or raw secret-alert values were read or stored. After organization transfer, these settings need rechecking against organization policy and actual maintainer membership.

## Tracked implementation

- Workflow Actions are pinned to their reviewed upstream release commits. `upload-pages-artifact`'s nested upload action is also pinned by its upstream definition.
- Checkout does not persist credentials. PR jobs build with read-only permissions and do not upload a deployment artifact or deploy. The deployment job only has Pages/OIDC permissions.
- Runner image is `ubuntu-24.04`; Python 3.11 and Node 24 are explicit. Build and deploy have 10-minute timeouts.
- Source downloads allow only HTTPS `api.github.com` / `raw.githubusercontent.com` endpoints; they do not follow redirects or read curl configuration, and have byte/time limits. Repository and commit identifiers and relative paths are validated.
- ZIPs require the pinned digest and expected member count, reject unsafe paths/encryption, and have per-member and total decompression limits. Files are read for metadata/hashes, never extracted or executed.
- HTML meta CSP and referrer policy are included in both public pages. Browser-generated catalogue content uses DOM text operations rather than HTML interpolation. GitHub Pages cannot supply a custom `frame-ancestors` response header from this repository; no complete header-based security guarantee is claimed.
- CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, Apache-2.0 LICENSE/NOTICE, Code Owners, issue forms, and PR template provide contribution/review boundaries.

## Validation

27 Python checks and 7 JavaScript checks pass, including adverse network destinations, paths, oversized downloads, archive traversal, and decompression limits. Both source adapters synchronize successfully through the hardened downloader without changing the 891-record snapshot. All 13 curated declaration locations remain reachable at their pinned lines; this is not proof compilation or auditing. Static packaging and JavaScript syntax checks pass. Browser-based CSP and modal-interaction QA were not available in this environment.

The previous hosted UI release (detail overlay) deployed successfully. The hardened workflow is validated on GitHub after this checkpoint is committed. The independent CodeQL service analyzes JavaScript/Python; it is not a mathematical proof verifier and its results do not promote catalogue evidence states.

## Deferred boundaries

- A general Lean proof runner still needs an OS sandbox (container or stronger). `run_pilot.py` runs only its fixed infrastructure example in a temporary directory and is not an arbitrary-code sandbox. The scoped integer-complexity PR job now runs candidate compilation in a read-only, non-root, offline container, with a 120-second timeout and memory/CPU/process limits; pinned upstream dependency preparation uses network access. No credentials are passed to that container. This example is not a general independent proof-verification service and requires workflow review.
- Mathematical fidelity, local external-proof audits, and a separately maintained proof verifier are not delivered by these repository controls.
- The owner created `theorem-atlas`, and the repository has been transferred with its name and `/theorem-atlas/` Pages path retained. Controls were rechecked; CodeQL was re-enabled after its configuration reset. The actual organization maintainers team is now Code Owner. See ORGANIZATION_TRANSFER.md.

## Proof candidate CI checkpoint

The integer-complexity candidate compiled successfully in [GitHub CI](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38419766281), with warnings treated as errors and recorded declaration/axiom diagnostics. Lean, Mathlib, external proof dependency, Lean archive checksum, and Ubuntu image digest are pinned; apt packages are not individually pinned. Both failed and successful attempts are recorded in proofs/integer-complexity/ATTEMPTS.md. Candidate compilation is isolated from dependency preparation. Independent source fidelity, imported-cache trust, and workflow review remain pending; no catalogue verification state or existing verifier rules changed.

## Administrator enforcement update

On 2026-10-13, administrator enforcement was enabled at the owner's request. Owner-authored PRs then could not obtain an independent Code Owner approval because the project had only one maintainer. At the owner's request, administrator bypass was restored temporarily using the dedicated API endpoint. Read-back confirmed `enforce_admins=false`; the existing required build, one approval, Code Owner review, last-push approval, and other protection settings were retained.

Contributions should still use PRs. Re-enable administrator enforcement after adding a trusted second maintainer who can review owner-authored changes. This temporary repository-administration exception does not permit an agent or author to approve their own mathematical statement fidelity.
