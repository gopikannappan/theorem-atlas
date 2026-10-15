# Plan for a future hidden fidelity evaluation

Status: prospective preparation plan, not a frozen hidden dataset or completed preregistered experiment. Freeze a final revision before generating reference labels, commissioning reviewers, or observing evaluation outcomes. This plan creates no new verification acceptance rule.

## Claim and task

Primary task: detect source-to-Lean statement mismatches on a specified distribution of mathematical theorem families while accepting justified alternative formulations. Formal proof validity, mathematical fidelity, source provenance, and originality are separate dimensions. A claim about human comparability needs a matched human baseline and independently validated references; toy-pilot agreement cannot substitute.

## Separation and concealment

An independent case custodian chooses new families not used in public development or prompt tuning, records source licenses and exact revisions, and freezes statements, full definition closure, variants, compiler observations, and expert references before AI review. The author of a candidate cannot approve its own fidelity. Keep labels, generation rationales, class balance and compiler results separate from review packets. Seal commitments before responses; reveal only after all responses are frozen. A public dangling Git object is not a secure secret store. Custodian storage and access controls are not provisioned here.

Split at the mathematical-family and shared-definition level. Report common dependencies and near duplicates; a new filename is not a new independent example. Published sources may have been in model training, so report contamination risk rather than asserting absence. All current pilot/pool cases are excluded from held-out claims.

## Candidate construction and reference

Include unchanged source claims, genuinely equivalent alternate encodings with explicit bridges, and subtle defects in definitions, quantifiers, assumptions, boundary cases and conclusion directions. Compile every variant in a clean, pinned environment; record failures and do not leak them as answer hints. Never use placeholders or trust bypasses as verified proofs. Deliberate weakened synthetic variants must remain isolated from theorem submissions and labeled as adversarial artifacts.

At least two independently working domain-qualified reference reviewers should compare source and Lean before seeing intended mutation labels or AI answers. A separate adjudicator resolves disagreement and scope ambiguities. Preserve inconclusive/reference-ambiguous cases rather than removing them after looking at AI performance. Grade explanation correctness and evidence locations, not only classifications.

Before any outcome, fix the case counts per family, source scopes, severity categories, inclusion/exclusion criteria, reference process, abstention handling, review budgets, models/versions, prompt, allowed tools, repeats, baseline expertise and statistical analysis. Those quantities remain TBD here; this plan does not authorize a populated experiment with unspecified choices.

## Measures and analysis

Report a full aligned/mismatch/inconclusive table per reviewer; severe intended/reference-confirmed defects missed; false alarms on valid alternatives; abstention/coverage; category and explanation correctness; family-level breakdowns; reviewer disagreements; actual token/runtime/cost evidence. Unknown measurements stay null.

Use reference-confirmed labels only for expert accuracy claims. Keep author-intention agreement separately named. Evaluate all frozen cases with the same process and budgets; preserve retries and do not select the best run. Repeated responses and paired variants are dependent observations, not extra independent theorems.

If comparing AI and humans, use the same packets and matched tool/time conditions, blind both groups to references and each other's answers, distinguish reference experts from baseline participants, and preregister a scientifically justified comparison margin and uncertainty analysis. Cluster analysis by mathematical family; do not advertise an unsupported confidence bound from a small dependent convenience sample.

## Stopping and release

Checkpoint every attempt and diagnostic. A severe confirmed miss should trigger investigation and a bounded revised development cycle; any tuning consumes that evaluation set and requires new hidden cases. Publicly report failures and limits along with successes. Preserve original cases and model outputs unchanged, adding amendments instead of rewriting history.

Release source identities, complete prompts, raw responses, reference judgments, compiler/trust observations, scripts and budget accounting after the freeze-and-reveal protocol permits it and licensing allows. Catalogue audit status remains unchanged unless its separate review requirements are met. No universal sufficiency or human replacement claim follows automatically from a benchmark score.
