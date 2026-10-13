# Linked-declaration audit checkpoint — 2026-10-13

Scope: 13 declarations across 12 linked catalogue records, plus the integer-complexity pilot. Reviewer slots remain unassigned at the owner's request. **No completed independent audit is claimed.** Existing catalogue evidence policy and verifier rules are unchanged.

## Initial bounded CI pass

[Run 38451927932](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38451927932) used Atlas commit b67e3923af2bbd0d496ab7398606f26a5d30fc77. Controller commands, outcomes, artifact links/hashes, release digests, useful compiler diagnostics, and last module progress are retained in [the machine-readable checkpoint](../audit-reports/linked-declarations-2026-10-13.json). Full CI artifacts have 30-day retention.

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

## Second bounded CI pass

[Run 38456001250](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38456001250) used Atlas controller commit 84f0dba73e15b33a38e1aa79f790825dbd3bf575. All eight environment attempts have ended. Full controller commands, probe output, source hashes, pinned dependency identities, supplied patch hashes, useful diagnostics, and artifact links/checksums are checkpointed in the machine-readable report. No local execution took place.

| Declaration | Build | Type / axioms | Module replay (imports assumed) | Fresh group replay | Trust observation |
| --- | --- | --- | --- | --- | --- |
| [atlas:integer-complexity](https://github.com/theorem-atlas/theorem-atlas/blob/758e030c9ae8fc0a7ce8ed5165cec3672b81d197/proofs/integer-complexity/IntegerComplexity.lean#L103) | passed | passed | passed | passed | foundation list observed; review pending |
| [anthropic:fermat-last-theorem](https://github.com/anthropics/fermats-last-theorem/blob/6e837e75355538c7f80bab5b956861e86c4eacc2/Theorems/Thm_fermat_last_theorem.lean#L128) | not run | not run | not run | not run | axioms not observed |
| [math-inc:strongpnt](https://github.com/math-inc/strongpnt/blob/2f5835c322314f55f1026ec2f139d704b7c45c69/StrongPNT/PNT5_Strong.lean#L5911) | passed | passed | passed | timeout | foundation list observed; review pending |
| [harmonic:imo2025:p1](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P1.lean#L1387) | timeout | not run | not run | incomplete_group_build | axioms not observed |
| [harmonic:imo2025:p3](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P3.lean#L417) | passed | passed | failed | incomplete_group_build | Lean.ofReduceBool; trust review pending |
| [harmonic:imo2025:p4:1](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P4.lean#L1437) | passed | passed | failed | incomplete_group_build | Lean.ofReduceBool; trust review pending |
| [harmonic:imo2025:p4:2](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P4_solve2.lean#L934) | passed | passed | failed | incomplete_group_build | Lean.ofReduceBool; trust review pending |
| [harmonic:imo2025:p5](https://github.com/harmonic-ai/IMO2025/blob/72b62405a176a7eaeadb335a7fa6ee80b6667161/HarmonicLean/IMO2025P5.lean#L615) | passed | passed | passed | incomplete_group_build | foundation list observed; review pending |
| [anthropic:zeta23](https://github.com/anthropics/formal-math/blob/e1a4e6508154ea59f030480661590a9fe3018011/zeta23/Solution.lean#L64) | passed | passed | passed | timeout | foundation list observed; review pending |
| [alphaproof-nexus:ErdosProblems/erdos_152.lean](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/ErdosProblems/erdos_152.lean#L505) | passed | passed | passed | timeout | foundation list observed; review pending |
| [alphaproof-nexus:OEIS/oeis_51293_conjecture_0.lean](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/OEIS/oeis_51293_conjecture_0.lean#L517) | passed | passed | passed | timeout | foundation list observed; review pending |
| [alphaproof-nexus:StacksProject/NormalRings_normalRing_characterization.lean](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/APNOutputs/StacksProject/NormalRings_normalRing_characterization.lean#L1029) | passed | passed | passed | timeout | foundation list observed; review pending |
| [anthropic:3sum-apsp](https://github.com/anthropics/formal-math/blob/e1a4e6508154ea59f030480661590a9fe3018011/3sum-apsp/ThreeSumApsp/Statements/EndStatement.lean#L44) | passed | passed | passed | timeout | foundation list observed; review pending |
| [openai-math:005](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/NumberTheory/Catalan/Results/Conclusions.lean#L11) | timeout | not run | not run | no_built_modules | axioms not observed |

External coverage: **10 of 13 declarations** compiled and printed their types/axioms, spanning **9 of 12 linked records**; **7** passed module replay with imports assumed, and **0** were covered by a successful fresh group replay. The additional integer-complexity pilot passed compilation, module replay, and fresh replay. Its source hash was unchanged. This pilot is separate from the 12 catalogue records.

Across both bounded attempts, **11 of 13 external declarations**, spanning **10 of 12 linked records**, compiled and printed their types/axioms at least once. Harmonic problem 1 succeeded in the first attempt but timed out in the second under the same source pin; the report preserves both results. Catalan and FLT remain unreproduced by this workbench.

Harmonic statement reviewers should use the year-specific [official 2025 English problem sheet](https://www.imo-official.org/assets/documents/problems/2025/2025_eng.pdf), recorded as a source supplement in the report, rather than relying on the generic latest-year problem page.

Each fresh result describes replay of the group's combined import environment with the version-matched Lean checker. It is not a separately implemented external checker or an independent mathematical fidelity decision. A skipped fresh replay after an incomplete group build does not imply successfully replayed individual targets. Timeouts and infrastructure failures do not establish mathematical falsity.

### Remaining limitations

- Both source mathematical fidelity and trust reviews remain **pending, with reviewers unassigned**, at the owner's request. The catalogue still reports **0 completed independent audits**.
- Harmonic problem 3 and both problem-4 proofs report Lean.ofReduceBool. Their second-attempt module replays fail with interpreter unknown-declaration errors for nativeDecide-generated constants; the exact diagnostics are retained. This native-computation trust surface remains unapproved. Problem 5 passes module replay. The fresh group replay is skipped because problem 1 did not complete, and the first attempt's separate unknown Std core-constant failure is retained.
- FLT preparation remains blocked by the pinned project/cache toolchain mismatch. No source pin or theorem was changed to make it build; the upstream full replay's reported resource requirements exceed this hosted-runner budget.
- Catalan's exact supplied compatibility patches were applied and recorded; the missing-import setup gap was resolved, but the target build still timed out at 20 minutes. The source overlays remain subject to independent review.
- Timeout-limited builds and fresh replays remain incomplete. There are no automatic retries beyond the two recorded bounded attempts. A future attempt must use the retained diagnostics and an explicit resource plan.
- Stronger comparator and independently implemented external-checker passes were not run. A source hash comparison protects only the observed target file against accidental change; it does not certify all dependencies or the controller.

## Review handoff

Use [the workbench](../audits/linked-declarations/README.md) and its pinned per-target inputs. Independent reviewers must examine the statement and assumptions, definition correspondence, whole proof dependencies, axiom interpretation (including native computation), source overlays, cache/toolchain trust, and coverage versus each manuscript. No agent approval is recorded. Comparator and an independently implemented external checker remain stronger follow-up steps where practical.

Current completed independent audits: **0**.

## Scheduling checkpoint

The evidence-only checkpoint commit c58c0a3d8bb1010b23e95416864d0d2f8b4a805e unexpectedly queued [run 38461448185](https://github.com/theorem-atlas/theorem-atlas/actions/runs/38461448185): PR path filters evaluate the cumulative PR diff, so separate report paths alone do not prevent another run. Further observational jobs are now restricted to explicit workflow dispatch; PR-triggered observation jobs are skipped and the existing concurrency setting cancels the duplicate. This scheduling change does not alter observer/checker logic or catalogue acceptance rules. Future attempts require an explicit resource plan and their own retained checkpoint. The existing catalogue build still runs on PRs.
