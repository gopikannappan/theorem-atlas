# Targeted reproduction follow-ups — 2026-10-14

The two bounded attempts are checkpointed in [AUDIT_CHECKPOINT.md](AUDIT_CHECKPOINT.md). Mathematical fidelity and trust reviewers remain unassigned. This plan does not approve any statement, change theorem assumptions, or allocate additional infrastructure.

## Catalan: one targeted source build

The upstream compatibility patches fixed the original missing-import setup gap. The second run built through Catalan energy estimates and fixed modular matrix modules before its 20-minute target-build limit. Preserve the exact OpenAI commit, supplied patch blobs, Lean release, Mathlib lockfile and observer inputs from that attempt.

Proposed next attempt: one Catalan environment, 15-minute preparation, at most 60 minutes of offline target compilation on the same 6 GB / 2 CPU container budget, followed by at most 90 seconds for the immutable type/axiom probe, 60 seconds for module replay, and 10 minutes for fresh replay if compilation finishes. A dedicated job must allow 90 minutes overall. Run once by explicit workflow dispatch after the resource plan and scheduling change have been reviewed. Retain all progress, source hashes and failure diagnostics.

No dependency update or target statement edit is justified by a timeout. Stop on the first budget limit or compiler failure and checkpoint. Any cache reuse needs exact source, patch, toolchain and dependency identities; compilation alone cannot certify cache/source correspondence.

## FLT: resolve reproduction infrastructure first

The pinned project uses Lean 4.33.1 while its pinned Mathlib cache expects 4.33.0. Do not copy a different toolchain into the project or change dependency pins to obtain a green run.

First inspect the pinned upstream reproduction instructions for a supported build without that cache. If a clean source build at the recorded pins is supported, it needs its own bounded preparation plan and isolated resource profile. The published full comparator script reports roughly 15 hours and 230 GB peak memory; those are upstream estimates, not Atlas measurements. The current hosted-runner profile cannot reproduce that check.

Do not start repeated hosted-runner retries or allocate a paid runner from this plan. Record a concrete infrastructure choice and cost/resource bounds before launching a larger run. Any resulting compiler evidence still needs separate mathematical fidelity and trust review.

## Review before expansion

Prioritize an independently reviewed end-to-end audit of one manageable external declaration before expanding expensive reproduction. Candidate reviewers should check the source manuscript, exact Lean proposition, definitions, assumptions and trust dependencies. The Stacks target's custom normal-ring definitions and Harmonic native-computation dependencies need explicit attention. Reviewer slots remain unassigned; an agent cannot approve its own statement fidelity.
