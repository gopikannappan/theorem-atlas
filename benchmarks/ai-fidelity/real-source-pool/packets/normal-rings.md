# normal-rings: independent source-fidelity worksheet

State: public development candidate; expert review pending. No reference verdict or evaluation result is supplied.

Source obligation: The three-way equivalence under reducedness and finitely many minimal primes.

Original scope summary: Under the source hypotheses, compare normality, integral closure in the total quotient ring, and a finite product of normal domains.

Source: https://github.com/stacks/stacks-project/blob/a04446e57ec1fbc252a871afcec7752fb2807b14/algebra.tex#L8275

Source repository revision: `a04446e57ec1fbc252a871afcec7752fb2807b14`.
Source Git blob: `ff4c47a74e8a273a49e6de7272a5c1311617cfc7`.



## Lean targets

- [normalRing_characterization](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/StacksProject/NormalRings_normalRing_characterization.lean#L1029), blob `0f6cdd84840e75835cbbc2a2b35019a5ae092f88`, toolchain `leanprover/lean4:v4.27.0`, Mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`.

## Questions to resolve without author or AI verdicts

1. Trace custom NormalRing and NormalDomain, localization at every prime, IsIntegrallyClosed and the total quotient ring.
2. Show List.TFAE covers all three assertions, not just one implication.
3. Check reducedness, finiteness of minimal primes, empty product and zero-ring conventions, universe/index types.
4. Distinguish a stronger added Noetherian hypothesis from an equivalent reformulation; mathematical source provenance remains unresolved.

For each target, record exact source/definition citations, selected obligation, correspondence or mismatch, edge cases, and a scope argument. Use the blank adjudication template. Commit or otherwise seal the first pass before inspecting author intentions and AI answers. No result is implied by this worksheet.

## Explicit gaps

- Independent reference labels pending
- Exact upstream author-selected manuscript revision unknown
- Proposed wrapper fixtures not authored or compiled

Definition locators and proposed design ideas live in pool.json. Review the actual reachable definitions; a locator is not a completed definition audit. Do not inspect design rationales during an intended first pass. None of the planned variants has been generated, compiled, or approved.

Upstream source terms remain intact. Existing Lean proofs are linked rather than copied. Compiler/trust observations from earlier upstream runs do not prove source fidelity or transfer to future variants. No catalogue status changes.
