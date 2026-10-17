# Prime-offset-two Brocard exclusion

This bounded attempt targets an exact family rule for n!+1=m²:

**If n+2 is prime and its remainder modulo8 is3 or5, there is no natural m with n!+1=m².**

This has no finite upper bound on n. It is a classical Wilson/quadratic-residue consequence, not a claimed discovery or a solution of the full open problem. The file does not separately prove that its set of excluded n is infinite.

## Derivation

Put p=n+2. Wilson gives (n+1)!≡-1(modp), while n+1≡-1(modp), hence n!≡1(modp). A square solution would therefore give m²≡2(modp). For an odd prime p,2 is a square modulo p exactly when p mod8 is1 or7. Thus residues3 and5 are excluded.

PrimeOffsetTwo.lean reuses Mathlib's Wilson theorem and its existing exact square-of-two criterion; neither proof is copied or reimplemented. The file also proves the n=11 instance (p=13) and checks the known pair n=5,m=11 (p=7, an allowed branch).

Declared targets:
- factorial_eq_one_mod_prime_offset: all natural n with n+2 prime; no positivity restriction needed.
- solution_prime_offset_residues: positive n, n+2 prime, and an actual square solution force residue1 or7.
- prime_offset_two_obstruction: all natural n with n+2 prime and residue3 or5 admit no solution.
- reject_eleven and known_pair_five: concrete proof instantiations, not a numerical search.

The residual gap is explicit: composite n+2 and prime n+2 in residues1 or7 remain uncovered by this rule. It says nothing sufficient about those values. The unrestricted Brocard–Ramanujan problem remains open; no new pair has been found.

## Sources and scope

- [Mathlib's Wilson proof](https://github.com/leanprover-community/mathlib4/blob/d77ef0741c6da1ff12df68fb4145ea0ae0850c54/Mathlib/NumberTheory/Wilson.lean), ZMod.wilsons_lemma.
- [Mathlib's quadratic reciprocity file](https://github.com/leanprover-community/mathlib4/blob/d77ef0741c6da1ff12df68fb4145ea0ae0850c54/Mathlib/NumberTheory/LegendreSymbol/QuadraticReciprocity.lean#L74), ZMod.exists_sq_eq_two_iff, Git blob `f097ae5217fcf7522f8b31dd3806489eda56021f`.
- [Helou–Haddad, A note on a problem of Brocard–Ramanujan (2008)](https://doi.org/10.1007/s11139-008-9139-8), [institutional abstract](https://pure.psu.edu/en/publications/a-note-on-a-problem-of-brocard-ramanujan/), for published infinite-family criteria. Only abstract/metadata was inspected; this project does not claim a theorem-number-specific reproduction of that paper.
- [Prior uniform reductions, PR12](https://github.com/theorem-atlas/theorem-atlas/pull/12); [prior bounded experiment, PR11](https://github.com/theorem-atlas/theorem-atlas/pull/11). This work does not transfer their evidence to a new statement.

## Verification and budget

Pinned Lean4.34.0-rc1 and Mathlib d77ef0741c6da1ff12df68fb4145ea0ae0850c54, with a complete transitive manifest. Candidate source is mounted read-only only after upstream dependencies are prepared. Execution is offline, non-root, resource-bounded and isolated in Docker on GitHub Actions. Ubuntu image/Lean archive digests are pinned; apt packages and runner infrastructure are not completely pinned.

The observer records source SHA256, complete compiler diagnostics, exact types and axiom dependencies, and optional selected-module replay. Module replay assumes imported libraries; it is not fresh dependency replay or independent source-fidelity approval. Workflow success means compilation succeeded, with replay status recorded separately. Original candidate code is Apache-2.0; upstream proof terms remain linked under their own terms.

Budget: at most three candidate compilations, including a possible final reproducibility compilation; dependency preparation600seconds, candidate compilation120seconds, optional module replay90seconds. Mathematical statements stay fixed across any library/API or proof-syntax repair. Preserve every failure and useful diagnostic. No trust bypass, theorem weakening or catalogue acceptance change is authorized.

Reproduce remotely with the Brocard prime-offset exclusion GitHub Actions workflow. Exact Docker preparation/runtime commands are in .github/workflows/brocard-prime-offset.yml. No local commands run. Candidate generation, module checking, independent fidelity review and catalogue acceptance remain separate. Reviewer slots remain unassigned. Both original attempts, their complete reports and the exact remaining gap are checkpointed in ATTEMPTS.md and observations/. The corrected file compiled and passed selected-module replay with imports assumed; independent review remains pending.
