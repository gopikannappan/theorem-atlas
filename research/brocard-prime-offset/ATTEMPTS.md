# Prime-offset-two proof checkpoint

**Checked statement:** if n+2 is prime and (n+2)mod8 is3 or5, then n!+1≠m² for every natural m. There is no upper bound on n in this theorem. It is a classical corollary, not a new solution or a global classification. No separate formal infinitude theorem is claimed.

## Attempt1: rejected

Source `1ca2929dcefc5b1679815acbc48e09dd8b20fd3e`, blob `bfebcb58d82d02ad75c4d2b8d5f0068e4b6ccdde`.
[Run39017589235](https://github.com/theorem-atlas/theorem-atlas/actions/runs/39017589235), job117352778460, artifact12095412816, digest `sha256:b775d7925e6a5d17da7af6b1f02e73c76bf6e66f6cb64ee2c3f7dcf2c0f2c294`.

Compilation exited1 because the concrete n=11 example left the goal Nat.Prime13 unsolved. The general declarations and n=5 known-pair proof printed without recovery axioms, but the file failed; reject_eleven printed a recovery placeholder/sorryAx. This attempt is rejected and is not proof evidence. Its full stdout/stderr is permanently retained in [observations/attempt-1-failed.json](observations/attempt-1-failed.json).

## Attempt2: compiled, review pending

Source `20c20e7acbd7f64fdc6ffa0e7adf02afb26d0d3c`, blob `faa326c5644139436161501cc8bec77dc79c24f8`, SHA256 `c3a6fcacc5da755b89b3fb817839682fdeda80ed0d3d1d0a4770c52b0579b651`.
[Run39017798460](https://github.com/theorem-atlas/theorem-atlas/actions/runs/39017798460), job117353363997, artifact12095965484, digest `sha256:f292ba9faf6ef8ecb267bf785523005ad753249164a6df2b0abf56cc4b5d5067`.

The sole repair replaced norm_num with ordinary kernel reduction decide for the small primality goal. No native evaluation was used, and all five theorem statement signatures stayed unchanged. The signatures and comparison identities are retained in frozen-statements.json. Two nonfatal letI style warnings remain recorded.

All five declarations compiled. Selected-module replay exited0 with imported libraries assumed. The full [successful report](observations/attempt-2-compiled.json) includes exact commands, printed types, axioms, stdout/stderr and limits. No fresh dependency replay or external checker ran. The first four declarations report propext, Classical.choice, Quot.sound; known_pair_five reports propext. No recovery axiom or native-evaluation flag was reported in these successful outputs.

Declaration URLs are pinned to the exact corrected source commit, blob and lines in provenance.json. Existing Mathlib proof bodies remain linked and reused, not copied.

## Scope and remaining gap

The proof explicitly uses an odd prime n+2 and the exact square-of-two criterion. For the final obstruction, positivity of n follows from the residue3/5 guard, so it is not silently added as an assumption. The n=11 instance confirms a nonempty excluded family; the known n=5,m=11 pair remains on the allowed prime7 branch.

Composite n+2 and primes in residues1 or7 remain uncovered. No fourth pair or uniform proof for all n>7 has been found. The theorem does not claim a new discovery, audited catalogue status, independent statement fidelity, or formal infinitude of the excluded set.

## Budget and reproduction

Two candidate compilation attempts are checkpointed. The final evidence commit may trigger one third reproducibility compilation, with unchanged Lean source, within the three-compilation budget. No further proof revisions are part of this attempt. Final validation links/outcomes go in PR13 to avoid another recursive documentation-triggered compilation.

Reproduce remotely using the Brocard prime-offset exclusion GitHub Actions workflow, with exact Docker preparation/offline runtime commands in .github/workflows/brocard-prime-offset.yml. Lean4.34.0-rc1 and Mathlib d77ef0741c6da1ff12df68fb4145ea0ae0850c54 plus transitive dependencies are pinned; candidate execution is isolated, offline and non-root. Compilation limit120seconds; module replay90seconds. Nothing ran locally.

Independent fidelity/trust reviewers remain unassigned. Existing verifier policy and catalogue acceptance are unchanged.
