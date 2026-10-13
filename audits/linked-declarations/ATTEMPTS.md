# Audit checkpoint — 2026-10-13

Inventory taken from catalogue commit d694d6b6c1916c81ae0fdb75afe89ea81d38fbcb: 12 linked records, 13 declarations, plus the integer-complexity pilot. Source declaration locations, upstream toolchains, Mathlib lockfile pins, and checker version pins were inspected remotely. No local commands or builds ran.

Initial CI attempt pending for eight environments. Budget and exact inputs are in inventory.json and groups/*.json. Existing verifier rules and catalogue statuses are unchanged. No independent reviewer has approved fidelity or trust.

Open review questions include the zeta title versus its linked two-thirds-minus-epsilon asymptotic bound, separate 3SUM versus APSP coverage, Harmonic's variant problem-4 statements, and the missing published digest for Lean 4.20.0-rc5. These are questions for review, not a verdict that a proof is incorrect.


Runner revision 2 is prepared after observed diagnostics: the pilot fresh replay timed out at 180 seconds, and the initial generic OpenAI setup omitted its supplied post-update patches, leaving a Catalan import missing. The next revision protects observer/probe/checker files from the workload user, runs cache configuration non-root, kills timeout process groups, prioritizes compiler observations, distinguishes module replay from fresh group replay, and gives the pilot fresh replay at most 600 seconds within the same group deadline. It applies only the patches supplied by OpenAI's exact source commit and records their hashes without changing the lockfile. No upstream theorem is edited by Atlas. Reviewer slots remain unassigned at the owner's request.


Initial run 38451927932 completed all eight environment jobs. Compiler reproduction succeeded for five external declarations plus the pilot; no fresh import replay completed. Full useful diagnostics and artifact provenance are retained in ../../audit-reports/linked-declarations-2026-10-13.json and ../../docs/AUDIT_CHECKPOINT.md. Harmonic problem 3 reports a native-computation trust dependency. Second-attempt budget increases are recorded before execution and justified by the observed target timeouts; no proof statement or verifier acceptance rule changes.
