# Attempt checkpoint

2026-10-13: candidate 1 prepared remotely. No local compilation. Pending GitHub CI diagnostics. Source and dependency commits are recorded in provenance.json. Independent fidelity and trust review pending. Maximum eight candidate revisions; compile timeout 120 seconds, CI job limit 45 minutes.

Remote access initially rejected branch creation with HTTP 403. After the owner configured organization access, remote branch creation succeeded. No proof changes were lost; no proof build ran locally.

## CI attempt 1 — dependency preparation passed, candidate not compiled

- Candidate commit: 50e8eb8ac47e37fadc04e019ee5a6e9585f9ac30
- Checked PR merge commit: 841049947dab0d7a64b34f68daeb1f09ffcba0ec
- [CI run](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38418364605)
- [Full diagnostic artifact](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38418364605/artifacts/11826150254), SHA256 626231f78e6445e85a24e2cf83589b1195d5c94db28f0ff03752b36c4e8b4682. GitHub retention is 30 days; useful diagnostic is retained below and full run logs remain linked.
- Lean archive checksum verified; pinned imported module built successfully (1995 jobs).
- Candidate invocation failed before Lean compilation:

```text
info: OpenProblemsLab: URL has changed; deleting '/work/.lake/packages/OpenProblemsLab' and cloning again
error: read-only file system (error code: 30)
  file: /work/.lake/packages/OpenProblemsLab/.lake/build/lib/lean/OpenProblemsLab/IntegerComplexity.olean.hash
```

Diagnosis: dependencies created by root were inspected by user 1000, triggering Git ownership protection. CI attempt 2 assigns /work to the compile user during image preparation; the compile filesystem remains read-only, network disabled, and credentials absent. Cache download is limited to the four imported Mathlib modules and their transitive imports to reduce build cost. No candidate source or theorem statement changed.
