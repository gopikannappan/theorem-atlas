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

## CI attempt 2 — first candidate compilation failed

- Candidate source unchanged from attempt 1; infrastructure commit: 290cb5ae478a803d15b0357f51ecc6cf351cd16e
- [CI run](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38418978548)
- [Full diagnostic artifact](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38418978548/artifacts/11826715604), SHA256 824d2f44b8dea0408e9bd32890553a65d61e0381ffe6bda0bb6b042ae08d9ecb.
- Dependency preparation succeeded. Read-only, non-root, offline candidate compilation reached Lean and failed on three diagnostics:

```text
IntegerComplexity.lean:40:6: error(lean.dependsOnNoncomputable): failed to compile definition, consider marking it as 'noncomputable' because it depends on 'Classical.propDecidable', which is 'noncomputable'
IntegerComplexity.lean:83:8: error: `dif_neg` has been deprecated: Use `dite_eq_right` instead
IntegerComplexity.lean:89:14: error: Tactic `rewrite` failed: Did not find an occurrence of the pattern
  OpenProblems.IntegerComplexity.complexity n
in the target expression
  Reachable e.eval (OpenProblems.IntegerComplexity.complexity e.eval)

case a
n : ℕ
hn : 0 < n
witness : ∃ k, Reachable n k := Exists.intro n (Reachable.self n hn)
hdef : complexity n = Nat.find witness
e : OnesExpr
he : e.eval = n
hs : e.size = OpenProblems.IntegerComplexity.complexity n
⊢ Reachable e.eval (OpenProblems.IntegerComplexity.complexity e.eval)
theorem Mathoverflow75792.complexity_three_pow : True ↔
  ∀ (n : ℕ), 0 < n → Mathoverflow75792.complexity (3 ^ n) = 3 * n :=
{ mp := fun a n hn => Mathoverflow75792.complexity_three_pow_value n hn, mpr := fun a => True.intro }
'Mathoverflow75792.reachable_iff_expr' depends on axioms: [propext]
'Mathoverflow75792.complexity_eq_expression' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'Mathoverflow75792.complexity_three_pow' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
```

The error-recovery axiom in this failed run is not an accepted proof and is not manually introduced by the candidate. No verification is claimed for this revision. Candidate revision 2 adds a noncomputable section for the classical instance, uses the pinned version's non-deprecated `dite_eq_right` lemma, and rewrites expression cost before its value so the cost equality still matches. The predicate, minimum, theorem declaration, and assumptions are unchanged.

## CI attempt 3 — candidate revision 2 compiled successfully

- Candidate commit: 4650242990e3030621c0c3535bfe1891964142f3
- Checked PR merge commit begins `c4660a9`; the full SHA is in the artifact's checked-commit.txt.
- [Successful CI run](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38419766281)
- [Evidence artifact](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38419766281/artifacts/11825767438), SHA256 9be9e4dfe15582730967f5a36a6c260813f1f9d8fc92d0d3bbd6f9813a386bb4.
- Dependency preparation passed, candidate compiler exited successfully with warnings treated as errors, and diagnostics uploaded.
- Candidate compiled in approximately four seconds, within the 120-second budget. The build downloaded 1979 transitive Mathlib cache entries and built the reused module.
- Catalogue CI passed for the same candidate commit.
- No local build, test, or command was run for this contribution after the owner's explicit restriction.

Retained compiler output:

```text
theorem Mathoverflow75792.complexity_three_pow : True ↔
  ∀ (n : ℕ), 0 < n → Mathoverflow75792.complexity (3 ^ n) = 3 * n :=
{ mp := fun a n hn => Mathoverflow75792.complexity_three_pow_value n hn, mpr := fun a => True.intro }
'Mathoverflow75792.reachable_iff_expr' depends on axioms: [propext]
'Mathoverflow75792.complexity_eq_expression' depends on axioms: [propext, Classical.choice, Quot.sound]
'Mathoverflow75792.complexity_three_pow' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Only ordinary Lean foundational dependencies appear in these lists; no error-recovery axiom appears. This is compiler evidence, not independent trust or mathematical fidelity approval. Source definitions use classical decidability and the explicit True answer wrapper; those extraction choices, the representation bridge, imported proof, cache trust surface, and workflow still require independent review. No catalogue state has been promoted and no existing verifier rule was changed. PR remains draft and unmerged.

Budget checkpoint: three CI attempts, two candidate source revisions. Both failures are recorded above; every source revision is retained in branch history. This final documentation checkpoint does not change the successfully compiled candidate source or build inputs.
