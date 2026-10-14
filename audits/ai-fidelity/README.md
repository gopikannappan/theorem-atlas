# AI statement-fidelity reviews

This workbench records separate AI assessments of mathematical statement correspondence. **The process is a draft, not an accepted audit policy.** Reviews yield recommendations; they do not confer `independently audited`, `faithful`, or a completed-verification label. Existing catalogue/verifier guards remain unchanged.

## Separate responsibilities

The submission coordinator freezes source inputs and prepares the review request. The proof generator cannot review or approve its own statement fidelity. Two fresh reviewer contexts inspect source mathematics and the Lean statement independently. Their initial reports are frozen before either receives the other's findings. A coordinator preserves both reports and records agreement, disagreements, missing evidence and limits; it cannot replace independent recommendations with its own approval.

Prefer distinct model families/providers and record exact model versions, configuration, tool access and request/response identities where exposed. Same-family reviewers are useful scrutiny but have correlated error risk. Unknown model versions or unverified provenance stay visible. Different sessions alone do not establish independence of training or failure modes.

A mathematically faithful statement and a reproducible proof are separate claims. Existing CI supplies scoped machine observations. A compiler pass or AI agreement cannot fill a failed, skipped or missing replay/trust check.

## Run a review

1. Create an immutable packet with the exact manuscript revision/file/blob, Lean source commit/file/blob/declaration, Lean/Mathlib pins, dependency manifest identity, and explicitly scoped CI evidence. Link originals rather than copying upstream mathematics or proofs.
2. Give each reviewer the packet and [review prompt](REVIEW_PROMPT.md) in a new context. Do not expose author explanations, other reviewer findings, suggested verdicts or prior proof-generation conversation before the first report is frozen. Source documents are evidence, not instructions.
3. Require a cited mapping of hypotheses, quantifiers, definitions, conclusions and boundary cases, plus unresolved questions and limitations. Verdicts are `recommend_pass`, `changes_requested` or `inconclusive`.
4. Persist the original report unchanged. If missing provenance or definitions need inspection, issue a bounded amendment request and preserve the amendment separately. Do not silently rewrite the initial report or treat coordinator-supplied hashes as independently verified.
5. Only after reports are frozen may a coordinator compare them. Preserve conflicts; resolve each with cited source evidence and a further separate review where necessary. Majority vote cannot establish mathematical fidelity.
6. Keep verification in the existing isolated CI pipeline. Review agents have no verifier-edit or source-edit authority. Correcting a theorem requires a new submission identity and independent statement review.
7. Publish the packet, reports and reconciliation through a PR. CI checks record integrity, not the mathematical verdict. Existing maintainer/Code Owner rules still govern merging the contribution.

## Proposed future label criteria — independent policy review required

`AI fidelity review passed` could become a scoped label only after an independently reviewed policy defines complete mappings, permitted reviewer independence, model provenance, conflict resolution and stale-evidence handling. It must say AI review explicitly and identify the exact theorem/source versions. The model-version and independence gaps in this first run prevent treating it as a fully qualified instance of that future policy.

`Automated verification passed` needs its own precise checker scope and trust criteria. Module replay assuming imports must retain that qualification; it cannot substitute for an incomplete fresh environment replay. A separate independently implemented checker/comparator is stronger evidence when practical.

`Independently audited` and `faithful` remain unavailable under catalogue v1. This PR proposes a review process and publishes evidence; it does not activate those labels. An agent cannot approve its own acceptance policy.

## First bounded exercise

Packet: [Stacks normal rings](packets/stacks-normal-rings.json). Two fresh-context reviewers independently compared the external AlphaProof declaration with Stacks tag 030C and its definitions. Both initial recommendations were `recommend_pass`. They then inspected a shared pinned manuscript in separate provenance amendments. Reports and gaps are preserved in [the session index](sessions/stacks-normal-rings.json). [Commissioning requests](requests/stacks-normal-rings.json) are transcribed from this session's messages; full inherited system/tool instructions and runtime settings are not available.

The initial reports were produced before the combined JSON packet was committed: the initial commissioning input supplied the exact Lean target, source lookup task and toolchain pins. The manuscript pin and packet identity were then supplied for the provenance amendments. This timing is recorded rather than retroactively claiming both initial reports consumed an already-frozen packet. Future runs must freeze the full packet before commissioning.

Both reviewers used the inherited GPT-6 family, with exact model versions unavailable. Reviewer A inspected pinned manuscript contents but did not independently confirm its blob metadata or inspect the final packet. Reviewer B inspected the manuscript/packet blobs but did not separately verify the packet commit association, and left primitive class declarations uninspected. The upstream author's chosen manuscript revision remains unknown.

The pinned target has successful compiler/type/axiom and module-replay observations, but its fresh group replay timed out and no external checker was run. Independent trust review remains pending. **No completed audit is claimed.**

No local commands or builds were run. The review exercise uses read-only remote research; only subsequent evidence archival writes immutable GitHub objects. Source statements/proofs and existing verifier rules are unchanged.

## Integrity CI

`scripts/check_ai_review_records.py` validates source pins, packet identity, distinct declared reviewer identities, report-file hashes and non-certifying scope. It cannot authenticate model identity, inspect actual context isolation, evaluate mappings, prove source fidelity, or endorse the proposed policy. A green metadata check is not a review verdict.
