# Linked-declaration audit checkpoint — 2026-10-13

Scope: 13 declarations across 12 linked catalogue records, plus the integer-complexity pilot. Reviewer slots remain unassigned at the owner's request. **No completed independent audit is claimed.** Existing catalogue evidence policy and verifier rules are unchanged.

## Initial bounded CI pass

[Run 38451927932](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38451927932) used Atlas commit b67e3923af2bbd0d496ab7398606f26a5d30fc77. Exact commands, outcomes, artifact links/hashes, release digests, useful compiler diagnostics, and last module progress are retained in [the machine-readable checkpoint](../audit-reports/linked-declarations-2026-10-13.json). Full CI artifacts have 30-day retention.

| Environment | Observed result |
| --- | --- |
| Integer-complexity pilot | Compiled, declaration/axioms printed; fresh replay timed out at 180 seconds |
| AlphaProof — three curated declarations | All three compiled and printed ordinary foundational axiom lists; all three fresh replays timed out |
| Harmonic problem 1 | Compiled and printed ordinary foundations; fresh checker failed on an unknown Std core constant |
| Harmonic problem 3 | Compiled; final axioms also include Lean.ofReduceBool; fresh checker failed on the same Std core constant |
| Harmonic problem 4, first proof | Group-budget build timeout |
| Harmonic problem 4, second proof; problem 5 | Not reached before group budget exhaustion |
| FLT | Cache preparation rejected project Lean 4.33.1 versus Mathlib Lean 4.33.0 |
| Zeta, 3SUM, Gauss strong PNT | Target builds exceeded their eight-minute limits |
| Catalan | Missing imported PNT module during build, followed by timeout; investigation found a required supplied upstream patch step omitted by the first generic runner |

The initial pass reproduced five external declarations, plus the pilot, at the compiler/type/axiom-output level. It completed no fresh whole-import replay. A timeout or checker infrastructure error is not mathematical falsity.

Harmonic's fresh checker exception was:

```text
(kernel) unknown constant 'Std.DHashMap.Internal.Raw₀.expand.go._unary.induct'
```

Problem 3's native-computation axiom increases the trusted computation surface and requires explicit review. It is not silently counted as a foundational axiom or approved by this workbench.

## Reproduction setup findings

Catalan's bare [locked dependency](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd/tree/c39a751132c88b6e8080b74c74023fd95b3d8be0) lacks the imported Catalan modules. The pinned OpenAI [lakefile](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/lakefile.lean) supplies a post-update patch step. Its [PNT patch](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/patches/PrimeNumberTheoremAnd-lean4341.patch), Git blob 924c5f6ec6fe88ba7788b420af4e3c3c7ac00abc, adds Catalan/Consequences.lean and related modules. The missing import was therefore a setup gap in the initial runner, not a finding that the published proof is false. The second attempt applies only supplied upstream patches, preserves dependency commits/lockfile, and records each patch's identity and SHA256. Those overlays require independent source review.

FLT's [upstream comparator script](https://github.com/anthropics/fermats-last-theorem/blob/6e837e75355538c7f80bab5b956861e86c4eacc2/verification/comparator/run.sh) reports approximately 15 hours and 230 GB peak memory for its full replay. This is upstream-reported resource evidence, not an Atlas measurement. The current hosted-runner budget does not reproduce that stronger check.

Lean 4.20.0-rc5's official release metadata lacks a published asset digest. First CI download observed SHA256 e4544c44170377ef33d6ae1ebe7eea10383f7fe20a84d56c1fdc18d16fccb575; the second attempt pins that value, with its observed provenance explicitly distinguished from publisher authentication.

## Justified second runner revision

The pilot timeout, omitted OpenAI setup step, and runner inspection justify a second bounded attempt. The revised runner:

- protects observer/probe/checker files from the workload user and runs upstream cache configuration non-root;
- kills timeout process groups and reaps children;
- completes compiler probes before replay, records module replay with imports assumed separately, and performs one fresh replay of the combined group;
- records target source hashes before/after observation;
- applies the exact supplied OpenAI patches without resolving moving dependency refs;
- retains all proof statements, source commits, Mathlib pins, and checker implementations;
- provides unreviewed assumption drafts and direct import provenance for every target.

The second attempt's group budgets are explicit in the JSON inputs: 15 minutes preparation; 15 minutes observation for pilot/AlphaProof, 30 for the large single-target environments, and 45 for Harmonic's five targets. Large single-target builds may use 20 minutes; the pilot fresh replay may use 10. At most four jobs run at once, and no automatic unbounded retry is configured.

## Review handoff

Use [the workbench](../audits/linked-declarations/README.md) and its pinned per-target inputs. Independent reviewers must examine the statement and assumptions, definition correspondence, whole proof dependencies, axiom interpretation (including native computation), source overlays, cache/toolchain trust, and coverage versus each manuscript. No agent approval is recorded. Comparator and an independently implemented external checker remain stronger follow-up steps where practical.

Current completed independent audits: **0**.
