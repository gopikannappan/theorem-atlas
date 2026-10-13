# Repository security checkpoint — 2026-10-13

This is the configuration inspected and applied for `gopikannappan/theorem-atlas`. It is hardening evidence, not a guarantee that the repository or its external mathematics is vulnerability-free.

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
| Administrator bypass | Available (`enforce_admins=false`); owner maintenance is an exception to normal PR enforcement |
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

- A general Lean proof runner still needs an OS sandbox (container or stronger). `run_pilot.py` runs only its fixed infrastructure example in a temporary directory and is not an arbitrary-code sandbox. PR CI does not run Lean.
- Mathematical fidelity, local external-proof audits, and a separately maintained proof verifier are not delivered by these repository controls.
- The new `theorem-atlas` organization requires the owner's web signup. No transfer or site hostname/path change has been made. See ORGANIZATION_TRANSFER.md.
