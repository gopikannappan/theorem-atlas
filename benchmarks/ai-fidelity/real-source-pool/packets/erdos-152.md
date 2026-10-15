# erdos-152: independent source-fidelity worksheet

State: public development candidate; expert review pending. No reference verdict or evaluation result is supplied.

Source obligation: The divergence corollary on page1, not the full quantitative theorem or an infinite-Sidon-set variant.

Original scope summary: For finite Sidon sets of prescribed size, consider the minimum count of isolated pair sums. The selected obligation is that this minimum tends to infinity with set size.

Source: https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/NaturalLanguageProofs/ErdosProblems/erdos152.pdf

Source repository revision: `0647711a71183c1ea492ad60860776617ce1ea88`.
Source Git blob: `10cf3a8b982d128816dc66aff4bfc8cb9d260147`.
Source SHA256: `ec57666d3b8c052c560848f7bd8501f34ad0fcbc00c1be7c7a9010c0c274aa86`.

Only first180 words of page1 extracted in CI; full manuscript review pending

## Lean targets

- [Erdos152.target_theorem_0](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/ErdosProblems/erdos_152.lean#L505), blob `e09219a2220f579656757682839069d30572d28b`, toolchain `leanprover/lean4:v4.27.0`, Mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`.

## Questions to resolve without author or AI verdicts

1. Match the exact Sidon convention, finite-set cardinality, minimum/index family and existence of admissible sets for each n.
2. Check ℕ versus positive integers or ℤ, especially truncated s - 1 at s = 0. This is a question, not an established defect.
3. Expand answer(True) and Tendsto atTop atTop to the quantified eventual lower-bound obligation.
4. Do not credit this declaration with the manuscript's quantitative bound. Inspect f_lower_bound_div separately if that stronger claim is selected.

For each target, record exact source/definition citations, selected obligation, correspondence or mismatch, edge cases, and a scope argument. Use the blank adjudication template. Commit or otherwise seal the first pass before inspecting author intentions and AI answers. No result is implied by this worksheet.

## Explicit gaps

- Independent reference labels pending
- Full manuscript and imported Sidon/answer definitions require review
- Proposed wrapper fixtures not authored or compiled

Definition locators and proposed design ideas live in pool.json. Review the actual reachable definitions; a locator is not a completed definition audit. Do not inspect design rationales during an intended first pass. None of the planned variants has been generated, compiled, or approved.

Upstream source terms remain intact. Existing Lean proofs are linked rather than copied. Compiler/trust observations from earlier upstream runs do not prove source fidelity or transfer to future variants. No catalogue status changes.
