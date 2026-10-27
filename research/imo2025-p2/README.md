# IMO2025 Problem2 — full formalization attempt

**Objective:** complete the exact Compfiles theorem for the official IMO2025 Problem2, using the existing AI-produced geometry proof as a source. The full target is not established merely by proving coordinate identities.

## Source identities

- Harmonic/Aristotle geometry trace: [IMO2025P2.txt](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P2.txt), Git blob f74c6f95f6e8f78464eae812b2c3f706ea7bf2f5. Its sampled point coordinates, orientation and nondegeneracy checks must not become extra theorem assumptions.
- Exact interface: [Compfiles](https://github.com/dwrensha/compfiles/blob/1745e6ced3e671bd74417548494b034eb2c87da8/Compfiles/Imo2025P2.lean), blob acec73896c8d8500b01da4dc8de87202bb183c1c, author Joseph Myers. The upstream proof is incomplete. We retain every mathematical binder, hypothesis and conclusion, replacing only the extraction DSL keyword with a standard theorem declaration and selecting equivalent imports.
- Additional coordinate reconstruction source: [published OpenAI IMO proof](https://github.com/aw31/openai-imo-2025-proofs/blob/9990fe800af66bcc312cbfe2d631e6e64f5cb1f0/problem_2.txt), blob c3fa035b99db9add4adce8c829d4e2801a9e68c4. This is a second AI-produced proof of the same human-authored problem, not the Harmonic trace itself. Its coordinate method is reconstructed in original Lean code; no proof prose is copied.
- [Official IMO2025 problems](https://www.imo-official.org/assets/documents/problems/2025/2025_eng.pdf), Problem2, page1.

The copied statement retains its Apache-2.0 copyright/author notice. Existing upstream proofs remain linked; no Harmonic trace or OpenAI prose is redistributed. Original candidate code is Apache-2.0. No claim is made that the LLM originated the IMO problem.

## Two proof layers

FullTargetAttempt.lean contains the exact full affine-geometry target and an actual bounded proof attempt. No authored placeholder, invented axiom or trust bypass is inserted. It must compile completely before any full-proof claim.

CoordinateCore.lean attempts genuine supporting theorems over arbitrary real parameters: the linear two-circle relation; the quartic height identity; circumcenter equations derived from equidistance; a factorization of the candidate line/circle polynomial; and uniqueness of its zero parameter. These are algebraic components, not a redefinition of Mathlib sphere tangency.

The coordinate approach normalizes M=(0,0), N=(d,0), A=(x,y), with circle radii r<R. Put U=R-r and V=R+r. It proposes explicit formulas for P, H, E, F and the circumcircle. The current coordinate file does not establish all those formulas or their transport from the full affine setting.

Necessary remaining bridges must not be assumed:
1. Construct a valid normalized coordinate frame from the official hypotheses and derive all positivity/nonzero bounds.
2. Prove the second intersections E,F and the second common-circle point B have the proposed coordinates.
3. Prove the candidate polynomial describes the actual circumcircle of B,E,F, including affine independence.
4. Identify lineX/lineY with the line through the actual orthocenter H parallel to AP.
5. Derive Mathlib Sphere.IsTangent from the coordinate results and transport back to the exact target.

A unique polynomial root is not, by itself, the formal theorem. No sampled orientation facts, coordinate formulas, uniqueness premise or tangent conclusion may be added to the full target to force compilation. Any statement change would require independent review.

## Remote CI and bounded attempt

Lean4.35.0 and Mathlib56a005855ea17e0b0958f73ec801ae140b0a1679 match the pinned Compfiles environment. Every transitive dependency is pinned in the manifest. The Lean archive SHA256 and Ubuntu image digest are checked. Apt packages and runner infrastructure are not completely pinned.

GitHub Actions prepares only pinned upstream dependencies, then mounts both candidate files read-only and runs offline, non-root, with memory/PID/CPU limits. It records source hashes, complete compiler outputs, axiom lists and optional selected-module replay. Module replay assumes imports and is not fresh independent verification.

The full-target failure keeps the proof workflow red even if coordinate lemmas compile. Catalogue CI success must never be interpreted as completion of this theorem. No catalogue proof link or audit badge is added during an incomplete attempt.

Budget for this stage: four candidate CI iterations plus one final checkpoint build. The checkpoint fixes a misplaced documentation comment only; ATTEMPTS.md discloses the departure from the originally planned unchanged-source reproduction. Each coordinate compile is bounded to150seconds, full-target attempt60seconds, optional module replay90seconds, and dependency preparation900seconds. Persist every attempt and useful diagnostic. No local commands, unbounded searches or statement weakening.

The exact build/runtime commands are in .github/workflows/imo2025-p2.yml. All candidate declarations and assumptions are recorded in provenance.json. Independent fidelity/trust review remains unassigned; this agent does not approve its own statement fidelity.

## Checkpoint status

The full theorem remains unproved after four candidate iterations. Fourteen supporting lemmas elaborated in iteration4, but a comment-placement parser error prevented module success. The final checkpoint corrects only that comment; its result must be read from CI before claiming a successful supporting module. Full source identities and diagnostics are permanent in observations/ and provenance.json. See REMAINING.md. No independent fidelity or trust review has been performed.
