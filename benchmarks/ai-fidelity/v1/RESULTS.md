# Pilot result: author-reference agreement only

Both fresh-context GPT-6 reviewers agreed with the author's intended labels on all twelve synthetic cases. They each flagged the six intended statement defects and accepted the six controls. Each assigned the intended category to all six defects. Neither abstained, and the reviewers did not disagree.

| Measure | Reviewer A | Reviewer B |
| --- | ---: | ---: |
| Aligned controls accepted | 6 / 6 | 6 / 6 |
| Intended defects flagged | 6 / 6 | 6 / 6 |
| Intended defects missed | 0 | 0 |
| Control false alarms | 0 | 0 |
| Inconclusive | 0 | 0 |
| Intended defect categories matched | 6 / 6 | 6 / 6 |

All twelve fixtures compiled in isolated GitHub Actions and reported no axiom dependencies, including the intentionally mismatched statements. The AI screen identified source-scope differences that compilation alone did not assess.

These counts compare with author intentions, **not expert-validated mathematical ground truth**. The same coordinator authored the key, assembled results, and wrote the scoring code; independent expert adjudication of labels and explanations remains pending. Exact reviewer versions and independent context-isolation authentication are unavailable. Both reviewers used the same family, and this is one prompt on elementary, paired examples—not twenty-four independent mathematical trials. Runtime, tokens and cost were not measured.

The result supports continuing development of fidelity screening. It does not establish human equivalence, universal sufficiency, research-level accuracy, or an audited theorem. No catalogue record has been upgraded. Read [the protocol](../README.md), [raw reports](reports/), [reference intentions](answer-key.json), [run provenance](run.json), [machine results](results.json), and [compiler diagnostics](compiler-observation.json).

Next: independent expert adjudication, then a separately authored and genuinely hidden benchmark of real manuscript/Lean pairs, including subtle defects and faithful alternative formulations. A claim of human comparability also needs a blinded human baseline. Preserve this public pilot as a regression set; do not reuse it as hidden evidence.
