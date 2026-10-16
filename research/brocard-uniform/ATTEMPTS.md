# Bounded proof checkpoint

All four declared mathematical statements stayed unchanged. There were two candidate iterations: one failed compiler attempt and one successful corrected attempt. The final documentation/evidence commit may trigger a third compilation for reproducibility, within the total three-compilation budget. No further proof revision or budget extension is authorized by this checkpoint.

## Attempt1 — rejected

Source commit `7db1219845577ed410efe66432ad94e08419d925`, Lean Git blob `8f83149c7e728e48d92ff0b22461cad6d7b03857`.
[CI run38978245889](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38978245889), job117232747694, artifact12079972704, digest `sha256:e7d054d4db2ef24ac1f9213000e87f8683bd21a662605f051aa3bdcbbad84f86`.

Compilation exited1 with `UniformReductions.lean:23:8: error: No goals to be solved`. A rewrite already closed the goal and the following tactic was redundant. Lean's failed elaboration printed a recovery placeholder and `sorryAx` for the first theorem; this attempt is expressly **not valid proof evidence**. The full compiler report, including expanded diagnostic proof output, remains in [observations/attempt-1-failed.json](observations/attempt-1-failed.json). It is retained to document the failure, not imported or used as a proof.

## Attempt2 — compiled, independent review pending

Source commit `c465d610a89f92585c16c289d17826a1fd201a90`, Lean Git blob `9a1694d0a5a00b4b47e9b1df6f01a38a1ddaeb56`, SHA256 `74f7fb7ccdebc42d99fed89e5ef18d3f1f0682be05d1653b33128e469808c2a0`.
[CI run38978628115](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38978628115), job117233969652, artifact12080162025, digest `sha256:ae50a6549952b3cd63e36afe95c97f49d210ca17b0aeebac95036c10166612ea`.

The repair removed the redundant tactic only. Diagnostic commands now display theorem types rather than huge proof bodies. A text comparison of all four declared signatures is retained in frozen-statements.json; no assumptions, conclusions, domains, quantifiers, or definitions changed.

Compilation exited0. The module replay also exited0, with imports assumed; no fresh dependency replay or external checker ran. Full commands, stdout/stderr and outcomes are in [observations/attempt-2-compiled.json](observations/attempt-2-compiled.json).

Axiom observations:
- consecutive_factorization_iff: propext, Classical.choice, Quot.sound.
- prime_successor_square_divides: propext, Classical.choice, Quot.sound.
- prime_successor_obstruction: propext, Classical.choice, Quot.sound.
- fixed_modulus_eventually_one: propext.

No recovery axiom or native-evaluation trust flag was reported in these four successful declaration outputs. The letI style warning remains and is recorded; it is not a proof failure. These are compiler/trust observations, not independent mathematical fidelity approval.

## Exact remaining gap

For n≥4, the equivalence retains the entire equation and root m, including its converse. It translates the problem to consecutive coprime factors with4ab=n!, but gives no uniform reason such factors cannot exist for n>7.

The prime-successor condition gives a necessary Wilson-prime divisibility test, not a sufficient condition. It says nothing directly about composite n+1 and does not classify Wilson primes.

The eventual-residue result shows why finitely many fixed moduli cannot prove global nonsquareness: for every positive q, all n≥q give the square residue1. Choosing new moduli as n grows supports finite exclusions but does not establish universal coverage.

No fourth solution, new mathematical theorem, infinite-family coverage proof, or global completeness proof has been found in this bounded attempt. Independent source-fidelity and trust reviewers remain unassigned. No catalogue status changes.

## Remote reproduction

Use the Brocard uniform proof reductions workflow on this PR/branch. Dockerfile pins the Lean release archive hash, Ubuntu digest and complete Mathlib dependency manifest. Exact preparation and offline runtime commands are in .github/workflows/brocard-uniform.yml. Candidate compilation is bounded to120seconds and module replay to90seconds. All execution is remote; no local commands were run.

The final validation run will be linked in the PR description to avoid another checkpoint commit recursively triggering further compilation. Its observation must be reported separately from these original two attempts.
