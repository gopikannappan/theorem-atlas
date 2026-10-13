# Agent Operating Rules

1. Never use `sorry`, `admit`, `unsafe`, fabricated axioms, or equivalent trust bypasses to claim a verified proof.
2. Never weaken a theorem, alter assumptions, or redefine concepts merely to make a proof compile. Changes to statements require explicit independent review.
3. Use pinned Lean/Mathlib versions and run proofs in a clean, isolated build.
4. Record source manuscript URL, exact upstream commit, theorem declaration, assumptions, proof dependencies, and reproduction commands.
5. Use `#print axioms` and additional checks to audit trust assumptions; interpret results carefully rather than treating this check as sufficient on its own.
6. Persist every attempt and useful compiler diagnostic. Keep bounded budgets and checkpoint before stopping.
7. Link existing Lean proofs from any source rather than copying them unless there is a justified reason and licensing permits it. OpenAI is only the initial source adapter.
8. Keep proof generation separate from verification. An agent must not modify verifier rules or approve its own statement fidelity.
9. Mark incomplete or unreviewed work honestly. Compilation alone is not mathematical fidelity.
10. Prioritize a working end-to-end vertical slice over premature multi-agent complexity.

11. Publish a static, source-agnostic theorem catalogue for GitHub Pages. Proof links must point to pinned commits and specific Lean declarations where available; never imply an external proof has passed local audits unless verified.
