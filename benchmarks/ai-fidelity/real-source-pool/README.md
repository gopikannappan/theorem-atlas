# Real-source fidelity review preparation

This is a **public development candidate pool**, not a hidden test and not an executed harder benchmark. It contains three mathematical source families and four existing Lean declarations: normal rings, Erdős152, and two formalizations of IMO2025 problem4. These are LLM-produced formal proof artifacts of human-origin mathematical problems/results; membership does not assert an LLM originated the theorem.

The frozen synthetic pilot is now merged. Its author-reference agreement is useful regression evidence, but its reference labels and AI explanations still lack expert adjudication. No human baseline, independent mathematical audit, or research-level accuracy result is available.

## Review packets

Start with [pool.json](pool.json) for exact upstream commits, Lean blobs, toolchain/Mathlib pins, source scope, definition locators, questions, and readiness gaps. Individual worksheets in [packets](packets/) are navigation aids; they do not prescribe verdicts.

Existing proofs remain linked at pinned commits. No upstream proof was copied or changed. Nine proposed designs describe original controls, valid alternative presentations, and possible controlled defects. They are **designs only**: no generated Lean variant fixture exists, and no variant has compiled or been reviewed. Original upstream compilation observations do not transfer to future variants.

The normal-ring packet scopes the Stacks equivalence. The Erdős packet explicitly selects the divergence corollary, not the manuscript's stronger quantitative result. The IMO packet tests a full classification; its two existing statements must be compared without treating every syntactic difference as a defect.

## Independent reference adjudication

Use [the review instructions](EXPERT_REVIEW.md) and [adjudication-template.json](adjudication-template.json). The blank form covers all twelve pilot cases, four real-source declarations, and twenty-four AI explanation assessments. Reviewer slots are unassigned. All actual decisions, identities, independence declarations, and explanation grades are blank.

A reviewer should first inspect source statements, reachable definitions, and Lean scope, then seal that judgment before looking at the author's key and AI reports. These materials are already public, so any claimed blindness must be disclosed as self-reported. A second pass evaluates AI reasoning and reference ambiguities. A separate adjudicator should resolve disputes before labels become a reference standard.

This coordinator authored the preparation materials and cannot approve its own statement fidelity. The preparation validator checks pins, coverage, and honest pending states only. It is not a proof verifier, expert-identity verifier, or mathematical judge.

## Source observations and licensing

[Source observations](source-observations.json) retain hashes and a bounded page-one excerpt from the pinned Erdős companion PDF, collected in remote GitHub Actions run38738078353, job116432384298. The official IMO2025 English PDF is pinned by observed SHA256, not by a Git repository revision. Its problem4 was inspected on page2. The byte observer verifies the expected Git blob for the Erdős PDF and the observed SHA256 for the official PDF on subsequent runs. A changed official document must produce a new separately reviewed source record.

These observations are not a full manuscript review. Stacks source is linked to an exact Git revision and label; the revision selected by the original Lean author remains unknown. The original Erdős problem website returned403 during preparation; this packet uses the pinned companion prose and explicitly records that scope.

The original packet/protocol code uses Atlas's Apache-2.0 license. Stacks manuscript terms remain GFDL. AlphaProof source files carry Apache-2.0 notices. No explicit license file was found in the pinned Harmonic tree; its proofs are linked rather than copied. Official IMO source terms have not been determined, so only source links, hashes, and an original scope summary are included. No blanket relicensing of upstream materials is claimed.

## Conditions for a future hidden evaluation

See [the preregistration plan](HIDDEN_EVALUATION_PLAN.md). No test cases are secretly held by this public repository. A separate custodian must author and freeze new cases, validated references, and reveal rules without showing them to reviewers or prompt developers. This pool is permanently ineligible for held-out claims.

Keep exact family/dependency overlap visible. The IMO family is an olympiad stress test and cannot support a research-theorem generalization claim. Human comparability requires a blinded human baseline on the same tasks, with expertise and exposure reported. Stop short of certification if reference adjudication, trust review, or evidence identity remains incomplete.

## Reproduction and checkpoint

All execution takes place in GitHub Actions; nothing ran locally. `python3 scripts/check_fidelity_preparation.py` checks preparation record consistency, and normal catalogue CI runs its tests. The source observation workflow is bounded to six minutes, fixed URLs, at most4MB per PDF, thirty-second network waits, and a twenty-second PDF extraction timeout. It runs no downloaded proof code and uses no credentials for source fetching. Runner/apt/PDF parser versions are not fully pinned; this is a byte/excerpt observation, not a hermetic proof build.

No new AI reviewers were commissioned, no humans were contacted, and no catalogue audit labels changed. The useful completed deliverable is the expert-ready source and adjudication material. The actual human review and independently hidden evaluation remain outstanding.
