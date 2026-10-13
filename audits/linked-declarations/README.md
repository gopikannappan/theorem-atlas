# Linked-declaration audit workbench

This workbench inventories all 13 curated declarations across the catalogue's 12 linked records, plus the integer-complexity pilot. It collects **observations**, not independent audit approvals. Existing catalogue validation and verifier rules are unchanged. No proof, statement, upstream options, or dependency pin is modified to make a build succeed.

## Scope and evidence boundaries

The workflow checks exact repository commits, toolchain files, Mathlib pins, full dependency lockfiles, and installed dependency commits. It builds the specific original module, prints the declaration type with full names and notation disabled, and prints the transitive axiom dependencies. A version-matched kernel checker replays the module and imports with `--fresh`.

This is kernel replay using Lean's own kernel, not an independently implemented external checker. Ordinary axioms, native-computation dependencies, custom axioms, and error-recovery dependencies must be interpreted by a reviewer; this workbench has no rule that approves them. Compiler/replay success does not approve the statement's meaning, manuscript fidelity, imported caches, or toolchain integrity. [Lean's validation guide](https://lean-lang.org/doc/reference/latest/ValidatingProofs/) describes stronger comparator and external-checker approaches.

Each group records source/manuscript references, exact declaration location, dependencies, toolchain, release artifact, and pending fidelity/trust review with no reviewer assigned. Source-level questions are recorded without treating them as independently reviewed findings. Paper coverage must be assessed per declaration, especially the zeta asymptotic bound and the separate 3SUM/APSP results.

## Remote execution and isolation

All execution is GitHub CI only. Docker preparation installs the pinned Lean release, clones the exact upstream project, and uses the pinned Mathlib cache. Upstream Lake configuration and the cache utility execute inside that preparation container, with network but no repository credentials. No target proof is built during preparation. The upstream lockfile must remain byte-for-byte unchanged and installed dependency commits must match it.

Original proof builds, declaration probes, and replay run in a separate non-root container with network disabled, no credentials, no Linux capabilities, no host mounts, and CPU/memory/process limits. Its filesystem is writable because Lake needs to emit proof objects. The container is destroyed after each job. It has no Docker socket and cannot write the host evidence directory; output is captured by the workflow outside the container.

The Ubuntu base image and modern Lean archives have pinned digests. The older Lean 4.20.0-rc5 release has no published GitHub asset digest; its observed SHA256 is recorded, and its archive authentication remains a review limitation. Apt packages and Mathlib binary caches are additional trust surfaces. No blanket supply-chain or mathematical certification is claimed.

## Reproduction on a remote runner

```sh
mkdir audit-context
cp audits/linked-declarations/{Dockerfile,prepare.py,observe.py} audit-context/
cp audits/linked-declarations/groups/atlas-integer-complexity.json audit-context/group.json
timeout --kill-after=20s 900s docker build --platform linux/amd64 -t atlas-declaration-observation audit-context
timeout --kill-after=20s 900s docker run --rm \
  --network none --cap-drop ALL --security-opt no-new-privileges \
  --user 1000:1000 --pids-limit 256 --memory 6g --cpus 2 \
  --tmpfs /tmp:rw,nosuid,nodev,size=256m atlas-declaration-observation
```

Change the group JSON to reproduce another pinned target. No local execution is authorized in this session.

## Bounded attempts and retained diagnostics

Initial budget: one CI attempt per environment, eight environments total, with at most four jobs at once. Each job has a 15-minute preparation limit and 15-minute observation limit, inside a 35-minute job deadline. A target build gets at most eight minutes; a fresh replay gets at most three minutes, sharing the group budget. Exhaustion/failure is incomplete evidence, not mathematical falsity. Any additional attempt must be justified by a specific new diagnostic and checkpointed.

Artifacts retain Atlas's checked commit, exact group metadata, runner scripts, archive/dependency preparation logs, compiler output, declaration/axiom output, and checker results for 30 days. No upstream proof implementation or dependency cache is redistributed. Useful findings and outcomes are checkpointed in ATTEMPTS.md and the PR body.

## Independent review handoff

For each declaration, an independent reviewer must record identity, reviewed commit, source URL, formal statement and assumptions, definition correspondence, dependencies and axiom interpretation, limitations, and signed-off conclusion. A source-correct challenge plus a suitably isolated comparator/external checker remains the stronger next step. The proof-generating agent cannot approve its own integer-complexity fidelity or alter verifier rules.

All fidelity and independent trust reviews remain pending. The catalogue's audited count stays zero until its separately reviewed evidence policy permits promotion and completed reviews supply evidence.
