# Synthetic fidelity screening pilot v1

This pilot tests source-to-Lean statement comparison on twelve original elementary natural-number cases. It does not evaluate research mathematics, prove human-level performance, or grant catalogue audit status. The author-intent reference has no independent expert approval. Reviewer slots for expert adjudication remain unassigned.

## Frozen inputs and separation

- Source packet and fixtures: commit `5ad31c8ce250d75bec9acc65ec3bd05781dcb987`.
- Packet Git blob: `cc185fe638d76d954c3910af287b01d4660d10d4`.
- Author-intent key frozen separately before commissioning reviews: commit `c5162c020b733f2fd8734e9760757f36e6c20d82`, path `benchmarks/ai-fidelity/v1/answer-key.json`.
- Reviewer instructions: `v1/REVIEW_PROMPT.md` at the source commit. Commissioning messages and exact responses are retained with run metadata.
- No source fixture or prompt changed after reviewing began. Reviewers received no author labels, partition names, compiler outcomes, or peer responses. Isolation is an orchestration property and self-report, not an independently authenticated guarantee.
- The coordinator authored cases and reference intentions and assembled/scored results. It does not approve its own mathematical fidelity. Counts measure agreement with these intentions; expert accuracy and diagnostic correctness remain ungraded.

Two fresh-context AI reviewers inspect only the packet, frozen instructions, and listed Lean files through read-only remote GitHub access. They use the same inherited model family; exact versions may be unavailable. This is not cross-model independence. Budget: sixteen file reads and about ten minutes per reviewer. No local commands, paid API calls, proof execution, or external mathematical research are needed for review.

## Cases and predeclared measures

Cases include matching controls and intended defects in definitions, assumptions, quantifiers, domain coverage, vacuity, and omitted equivalence directions. All twelve propositions are provable in Lean. Deliberate synthetic defects are isolated from actual theorem submissions; no published theorem or verifier rule was weakened.

The original key includes development and challenge family partitions. They are planning partitions, not a genuinely hidden held-out evaluation: the author knows all cases, all cases were reviewed with one frozen prompt, and all become public after responses freeze. Shared elementary mathematics and paired cases limit effective sample size. Do not extrapolate percentages to research theorems.

Score each reviewer separately: aligned-control agreements, intended defects flagged, intended defects missed, control false alarms, inconclusive responses, and intended category agreements. Abstention is neither acceptance nor successful detection. A nonempty explanation is required for record completeness; automated scoring cannot establish its mathematical correctness. No confidence intervals or population accuracy claims are justified by this tiny dependent convenience sample.

Expert adjudication should assess both source/Lean equivalence and reviewer explanations, accept valid alternative formulations, resolve ambiguous cases, and approve/revise reference labels in a separate PR. The original key and reports must remain unchanged; amendments are additional records.

## Reproduction and compiler evidence

Compilation workflow: [run 38699847763](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38699847763), job 116305101591. Structured diagnostics retain every fixture command, source SHA256, stdout, stderr, exit code, and scope in `v1/compiler-observation.json`. All twelve compiled on the first attempt and `#print axioms candidate` reported no axiom dependencies. This establishes these selected propositions compile, not their source fidelity, fresh independent kernel replay, or completeness of the Lean/compiler trust base.

Lean 4.34.1 with its bundled Std is pinned by release archive SHA256 in the Dockerfile. No Mathlib is used. Ubuntu image digest is pinned; apt package versions and runner infrastructure are not fully pinned. The networked image-preparation step installs the pinned archive without repository credentials; fixture execution is offline, non-root, read-only, capability-restricted, and bounded. GitHub checks out the PR merge commit, while copied case content is identified by per-file hashes and the frozen packet commit. Artifact retention is thirty days; permanent structured observations are committed.

Authorized reproduction in GitHub Actions: dispatch `AI fidelity benchmark fixture compilation` on this branch after merge. Equivalent commands for a separate clean remote runner:

```sh
docker build --progress=plain -t atlas-fidelity-fixtures benchmarks/ai-fidelity
docker run --rm --init --network none --cap-drop ALL --security-opt no-new-privileges --read-only --pids-limit 128 --memory 2g --cpus 2 --tmpfs /tmp:rw,nosuid,nodev,size=128m atlas-fidelity-fixtures
python3 scripts/score_fidelity_benchmark.py
python3 -m unittest discover -s tests -v
```

No commands were run on the user's local machine. Compiler diagnostics are observations, AI answers are screening opinions, and author-reference agreement is a pilot result. Original benchmark code and source statements use the repository's Apache-2.0 license.

## What is required next

Obtain independent expert reference labels and explanation adjudication. Then preregister a new, genuinely hidden set of harder real-manuscript cases with controlled defects and faithful alternative formulations, created separately from reviewers. Compare the same frozen AI process against those labels and, if claiming human comparability, a blinded human baseline. Measure abstentions, missed subtle defects, repeatability, runtime, and cost. Keep generation, verification policy, and fidelity approval separate. This public toy set is now contaminated for future held-out claims.
