# IMO 2025 Problem 2 — Lean formalization

The complete [Imo2025P2.imo2025_p2](https://github.com/theorem-atlas/theorem-atlas/blob/a97c547c0164d8967207be72ca6c17ce8c111f7c/research/imo2025-p2/FullTargetAttempt.lean#L30) declaration compiled in [GitHub Actions run 40537281937](https://github.com/theorem-atlas/theorem-atlas/actions/runs/40537281937). It uses the Compfiles mathematical signature without additional hypotheses. Independent review of the signature's fidelity to the official problem and of trust assumptions is **pending and unassigned**.

The source retains the historical filename FullTargetAttempt.lean; the proof in the pinned commit is complete. The formalized statement is a human-authored IMO problem with published AI-produced proofs. The Lean proof reconstructs a coordinate method informed by the OpenAI proof below; it is not a line-by-line translation of the Harmonic trace.

## Sources and attribution

- [Official 2025 IMO problems](https://www.imo-official.org/assets/documents/problems/2025/2025_eng.pdf), Problem 2, page 1.
- [Compfiles statement](https://github.com/dwrensha/compfiles/blob/1745e6ced3e671bd74417548494b034eb2c87da8/Compfiles/Imo2025P2.lean), commit 1745e6ced3e671bd74417548494b034eb2c87da8, blob acec73896c8d8500b01da4dc8de87202bb183c1c, Joseph Myers / Compfiles contributors, Apache-2.0. The upstream proof was incomplete; the copied statement retains its notice. The extraction DSL was replaced by a theorem declaration with the same mathematical signature.
- [Harmonic/Aristotle trace](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P2.txt), blob f74c6f95f6e8f78464eae812b2c3f706ea7bf2f5. Linked, not copied; numerical diagram constraints were not added to the target.
- [OpenAI IMO proof artifact](https://github.com/aw31/openai-imo-2025-proofs/blob/9990fe800af66bcc312cbfe2d631e6e64f5cb1f0/problem_2.txt), blob c3fa035b99db9add4adce8c829d4e2801a9e68c4. Linked, not copied; the coordinate route is reconstructed in original Lean code.

## What was checked

The frozen signature, full source and declaration are recorded in [provenance.json](provenance.json). The proof derives an orthogonal coordinate frame, identifies the geometric points and circumcircle, and proves Mathlib sphere tangency at `(N -ᵥ A) +ᵥ M`. No authored placeholder, extra axiom or sampled numerical hypothesis is used.

In the pinned remote container, `lake env lean /work/FullTargetAttempt.lean` exited 0. `#print axioms Imo2025P2.imo2025_p2` reported `propext`, `Classical.choice`, and `Quot.sound`. This is an axiom report, not a complete trust or source-fidelity review. The full theorem was not separately replayed by leanchecker.

The separate CoordinateCore.lean compiled 25 supporting lemmas and its module passed leanchecker replay with imports assumed. Cached imported dependencies were not freshly replayed. Lean 4.35.0, Mathlib commit 56a005855ea17e0b0958f73ec801ae140b0a1679, all manifest revisions, the Lean archive hash and Ubuntu image digest are pinned; apt packages and runner infrastructure are not fully pinned.

The exact container preparation and runtime commands are in [.github/workflows/imo2025-p2.yml](https://github.com/theorem-atlas/theorem-atlas/blob/a97c547c0164d8967207be72ca6c17ce8c111f7c/.github/workflows/imo2025-p2.yml). Candidate files are mounted read-only and checked offline. No local commands were run. The [successful observation](observations/attempt-17.json), earlier attempts and their diagnostics are retained. Artifact 12747369434 has digest `sha256:95d8e42591251ac48cb960b2b58f0692ac2541108a24d328a58953109ff03e89`; the permanent observation records the compiler output and source hashes.

## Review status

The declaration is Lean checked for the pinned formal statement. A reviewer must independently compare its types, assumptions and definitions with both the Compfiles statement and the official problem, and review the trust boundary. Compilation alone does not establish that fidelity. No audited or faithful catalogue status is claimed; the PR remains draft.
