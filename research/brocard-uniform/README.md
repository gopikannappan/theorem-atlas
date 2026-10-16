# Uniform Brocard–Ramanujan proof reductions

Goal: develop exact symbolic restrictions for n!+1=m², rather than extrapolating a finite search. This is bounded development work. No fourth solution or global exclusion for n>7 has been found.

## Frozen mathematical targets

UniformReductions.lean contains four declarations:

1. consecutive_factorization_iff: for every natural n,m with n≥4, n!+1=m² if and only if there are natural a,b with b=a+1, gcd(a,b)=1,4ab=n!, and m=a+b. Both directions and the value of m are retained; no bounded search or special residue class replaces the original problem.
2. prime_successor_square_divides: for every natural n,m, if n+1 is prime and n!+1=m², then (n+1)² divides n!+1. In conventional terms, a prime p=n+1 must be a Wilson prime. This is necessary only and does not cover composite n+1.
3. prime_successor_obstruction: the direct contrapositive, ruling out solutions whenever n+1 is prime and that prime-square divisibility fails.
4. fixed_modulus_eventually_one: for any positive modulus q and every n≥q, (n!+1)modq equals1modq. Thus any fixed finite set of modular square tests eventually becomes uninformative.

These are standard elementary reductions and no novelty is claimed. The contribution is an explicit, reproducible Lean development using pinned library results. Candidate generation and this observation run do not constitute independent approval of statement fidelity.

## Mathematical arguments

For the equivalence,2 divides n! when n≥4, so any square solution has odd m. Write m=2a+1 and b=a+1. Adjacent naturals are coprime, and m²-1=4a(a+1)=4ab. Conversely, with b=a+1 and m=a+b, expansion gives m²=4ab+1=n!+1. The formal statement uses4ab=n! directly, avoiding any ambiguity from truncated division in the informal n!/4 expression.

For the prime-successor condition, put p=n+1. Wilson's theorem gives n!≡-1(modp), so p divides m². Primality implies p divides m, hence p² divides m²=n!+1. This neither asserts that a Wilson prime yields a solution nor proves that no further Wilson primes exist.

For eventual residue1, q≤n and q>0 imply q divides n!; reduction of n!+1 moduloq is therefore the residue of1. No uniform exclusion of the remaining coprime factor allocations has been established.

## Literature and reuse

- [Helou and Haddad, A note on a problem of Brocard–Ramanujan, Ramanujan Journal17 (2008),155–161](https://doi.org/10.1007/s11139-008-9139-8), [author-institution record](https://pure.psu.edu/en/publications/a-note-on-a-problem-of-brocard-ramanujan/): published infinite-family exclusions and nonsquare criteria. Only the institutional abstract/metadata was inspected; no claim here identifies a theorem number or reproduces their proof.
- [Costa, Harvey and Harvey, A search for Wilson primes](https://arxiv.org/abs/1209.3436): background on the distinct Wilson-prime problem. A necessary Wilson-prime condition does not solve either open classification.
- [Existing bounded Atlas attempt, PR11](https://github.com/theorem-atlas/theorem-atlas/pull/11): finite computational observations, separate from these universal symbolic statements.
- Reuse Mathlib's [Wilson proof](https://github.com/leanprover-community/mathlib4/blob/d77ef0741c6da1ff12df68fb4145ea0ae0850c54/Mathlib/NumberTheory/Wilson.lean), [factorial divisibility](https://github.com/leanprover-community/mathlib4/blob/d77ef0741c6da1ff12df68fb4145ea0ae0850c54/Mathlib/Data/Nat/Factorial/Basic.lean), and [coprimality API](https://github.com/leanprover-community/mathlib4/blob/d77ef0741c6da1ff12df68fb4145ea0ae0850c54/Mathlib/Data/Nat/GCD/Basic.lean). Existing upstream proof bodies are linked, not copied. Original candidate code is Apache-2.0; Mathlib retains its upstream terms.

These proofs are small original derivations over existing library lemmas, justified as transparent glue for the research reductions; no competing implementation of Wilson's theorem is introduced.

## Evidence and scope

Lean4.34.0-rc1 and Mathlib d77ef0741c6da1ff12df68fb4145ea0ae0850c54 are pinned. The manifest pins every transitive package. The compiler imports only pinned dependencies prepared in an isolated Docker build; the candidate is mounted afterwards, offline, non-root and read-only. Ubuntu image and Lean archive hashes are pinned. Runner and apt packages are not fully pinned.

The observer records source SHA256, exact compiler command/stdout/stderr/exit/timeout, full printed declarations and axiom dependencies. It also attempts a bounded module replay with imports assumed; this is not fresh dependency replay or an external independent checker. Its optional result is explicit in the report. Workflow success means compilation succeeded; it does not mean optional replay succeeded, fidelity was independently approved, or the conjecture was solved.

No catalogue status or existing proof acceptance policy changes. Independent reviewers remain unassigned. No human review, new-solution claim, or audit badge is supplied by this work.

## Bound and reproduction

At most three compilation attempts, with the same declared theorem statements. Proof-syntax/library-API repairs may occur, but no statement weakening or altered mathematical definitions. Preserve useful diagnostics and previous source commits before each revision. Dependency preparation is bounded to600seconds; candidate compilation120seconds; module observation90seconds. Stop and checkpoint if the budget is exhausted.

Use the Brocard uniform proof reductions GitHub Actions workflow. It records the checked commit, source hash, toolchain and manifest. The exact Docker preparation and offline commands are in .github/workflows/brocard-uniform.yml. No local commands are run. Results will be checkpointed in ATTEMPTS.md after the remote observation.

The remaining research target is a genuinely new uniform obstruction on all possible consecutive coprime factors, or a separately scoped family with a justified proof. Formalizing these reductions makes that gap precise; it does not fill it.
