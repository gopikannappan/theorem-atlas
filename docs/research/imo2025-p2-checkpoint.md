# IMO 2025 Problem 2 checkpoint

**The full theorem remains unproved.** Draft [PR15](https://github.com/theorem-atlas/theorem-atlas/pull/15) contains partial formalization, not an audited catalogue proof.

At [source 121374f632877697c7939b3264b0569ac407be90](https://github.com/theorem-atlas/theorem-atlas/tree/121374f632877697c7939b3264b0569ac407be90/research/imo2025-p2), [run40520995382](https://github.com/theorem-atlas/theorem-atlas/actions/runs/40520995382) compiled eighteen supporting lemmas and passed selected-module leanchecker replay. The reported axioms are propext, Classical.choice and Quot.sound. Replay assumes imports; it is not independent dependency verification or mathematical fidelity approval.

The full-target file retains the frozen original mathematical signature. Its local proof derives ambient coordinates, both circle equations, B=(x,-y), nonzero height, and C=(-r,0), D=(d+R,0) from the original hypotheses. Lean then reports only the remaining unsolved original geometric goal. These local derivations are not separately certified theorem declarations. The failed full theorem is not imported into the successful supporting module.

Next work must identify actual P and H, derive the actual E/F formulas, prove affine independence of B,E,F, identify their actual circumcircle, and conclude tangency. No sampled diagram hypotheses or coordinate formulas may be added to the target.

[Machine-readable checkpoint and complete latest compiler output](imo2025-p2-checkpoint.json) records source hashes, checked declarations, artifact identity/digest, commands and remaining obligations. Earlier reports 1–7 remain under [research/imo2025-p2/observations](https://github.com/theorem-atlas/theorem-atlas/tree/121374f632877697c7939b3264b0569ac407be90/research/imo2025-p2/observations). Source manuscripts, exact upstream commits, statement attribution and licensing are in the pinned README/provenance files.

All execution was remote in GitHub Actions with Lean4.35.0 and pinned Mathlib56a005855ea17e0b0958f73ec801ae140b0a1679. Apt/runner infrastructure is not fully pinned. Independent fidelity and trust review remain unassigned. No full-proof or audit badge, catalogue-count change, merge or protection-setting change was made.

This documentation-only checkpoint preserves the last report outside the proof-workflow path; it changes no candidate, dependency, workflow or verifier source and requests no additional Lean run. The initial bounded stage and its disclosed comment-only correction were followed by three continuation candidates authorized by the user's continue request.
