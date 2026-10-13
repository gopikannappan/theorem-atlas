# Integer complexity of powers of three

Candidate proof: the minimum number of ones needed to express `3^n` using addition, multiplication, and parentheses is `3*n`, for every positive natural `n`. This is a useful exact cost bound and a small foundation for verified expression optimizers. It is an existing mathematical result, not a new discovery.

## Sources and reuse

The [source formulation](https://github.com/google-deepmind/formal-conjectures/blob/72dad3524e0174dea703f267664d3bc9298803a0/FormalConjectures/Mathoverflow/75792.lean) leaves `Mathoverflow75792.complexity_three_pow` unfinished. Its manuscript reference is [Altman–Zelinsky, Integer Complexity and Well-Ordering](https://arxiv.org/abs/1207.4841).

We import the existing [expression-tree proof](https://github.com/BrettKnox/open-problems-lab/blob/04ef51fe64bbdd85a40c7105cf0ea46a3bee80af/OpenProblemsLab/IntegerComplexity.lean), rather than copying it or claiming a new proof of Selfridge's bound. The new work proves both directions between expression trees and the source's `Reachable` predicate, equality of the two minima, and the source's powers-of-three statement.

Only `Reachable`, `Reachable.self`, and the `complexity` expression are selectively extracted from Formal Conjectures, with its copyright/license notice retained. Importing its whole module would introduce unfinished declarations. Both upstream repositories use Apache-2.0; our original bridge uses the root Apache-2.0 license.

The source's executable decision procedure is omitted and classical decidability is used instead; `complexity` is consequently noncomputable here. The constructors, minimization expression, domain, and positive-exponent hypothesis are retained. Source category annotations are omitted. The [answer elaborator](https://github.com/google-deepmind/formal-conjectures/blob/72dad3524e0174dea703f267664d3bc9298803a0/FormalConjecturesUtil/Answer.lean) marks `answer(True)` as the proposition `True`; we write it explicitly to avoid importing that metaprogram. These extraction choices require independent fidelity review.

## Evidence and review

Status: **candidate, independently unreviewed**. CI compilation and printed axiom dependencies are compiler evidence, not mathematical fidelity approval. No catalogue record is promoted, and the existing verifier/validation rules are unchanged. In particular, the new workflow is candidate-build infrastructure and requires maintainer review; it is not an independent certification service.

The CI job retains the exact checked commit, candidate hash, lockfile, provenance, preparation logs, compiler diagnostics, printed declaration and axiom lists as an artifact. The lockfile pins the full dependency closure. Expected ordinary Lean foundations must be examined rather than simply counting axioms. An independent reviewer should check the source extraction, both representation maps, minima equality, imported dependency source and its axiom closure, and CI isolation.

Candidate compilation occurs only in GitHub CI in a container without network, credentials, root privileges, writable root filesystem, or Linux capabilities. Dependency preparation has network access and builds only pinned upstream code. The Lean archive checksum, Ubuntu image digest, Lean version, Mathlib commit, and external proof commit are pinned. Apt packages are not individually pinned; this is not a bit-for-bit reproducible operating-system image. Mathlib's downloaded caches are a trust surface requiring independent review.

## Reproduction (in remote CI)

```sh
docker build --platform linux/amd64 -t theorem-atlas-integer-complexity proofs/integer-complexity
timeout --kill-after=10s 120s docker run --rm \
  --network none --read-only --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 128 --memory 6g --cpus 2 \
  --user 1000:1000 --tmpfs /tmp:rw,nosuid,nodev,size=256m \
  --mount "type=bind,src=$PWD/proofs/integer-complexity/IntegerComplexity.lean,dst=/work/IntegerComplexity.lean,readonly" \
  theorem-atlas-integer-complexity
```

No local builds or tests are authorized for this contribution. Generation is separate from the CI compiler invocation. Budget: at most eight candidate revisions; 120 seconds per candidate compile, 45 minutes per dependency/build job. Every submitted revision remains in branch history. Useful diagnostics and the final outcome are checkpointed in `ATTEMPTS.md`.
