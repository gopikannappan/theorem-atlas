/-
Copyright 2025 The Formal Conjectures Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Modified by Theorem Atlas contributors, 2026:
selective extraction of Reachable, its self witness, and complexity;
classical decidability replaces the upstream executable decision procedure;
new representation bridge and completed powers-of-three result.
See README.md for pinned sources, licenses, and pending fidelity review.
-/
import OpenProblemsLab.IntegerComplexity

set_option autoImplicit false
set_option maxHeartbeats 400000

namespace Mathoverflow75792

/-- The inductively defined predicate that m is reachable using n ones. -/
inductive Reachable : ℕ → ℕ → Prop
  | one : Reachable 1 1
  | add {m n a b} : Reachable m a → Reachable n b → Reachable (m + n) (a + b)
  | mul {m n a b} : Reachable m a → Reachable n b → Reachable (m * n) (a + b)

theorem Reachable.self (n : ℕ) (hn : 0 < n) : Reachable n n :=
  Nat.le_induction .one (fun _ _ ih ↦ .add ih .one) n hn

-- Avoid importing the upstream module's unfinished theorems.
-- This changes executability, not the predicate or minimization expression.
local instance (n : ℕ) : DecidablePred (Reachable n) :=
  fun _ => Classical.propDecidable _

noncomputable def complexity (n : ℕ) : ℕ :=
  if h : n = 0 then 0 else Nat.find ⟨n, Reachable.self n <| n.pos_of_ne_zero h⟩

open OpenProblems.IntegerComplexity (OnesExpr)

theorem reachable_to_expr {m k : ℕ} (h : Reachable m k) :
    ∃ e : OnesExpr, e.eval = m ∧ e.size = k := by
  induction h with
  | one => exact ⟨.one, rfl, rfl⟩
  | add h₁ h₂ ih₁ ih₂ =>
    obtain ⟨e, he, hs⟩ := ih₁
    obtain ⟨f, hf, ht⟩ := ih₂
    exact ⟨.add e f, by simp only [OnesExpr.eval, he, hf],
      by simp only [OnesExpr.size, hs, ht]⟩
  | mul h₁ h₂ ih₁ ih₂ =>
    obtain ⟨e, he, hs⟩ := ih₁
    obtain ⟨f, hf, ht⟩ := ih₂
    exact ⟨.mul e f, by simp only [OnesExpr.eval, he, hf],
      by simp only [OnesExpr.size, hs, ht]⟩

theorem expr_to_reachable (e : OnesExpr) : Reachable e.eval e.size := by
  induction e with
  | one => exact .one
  | add e f ihe ihf => exact .add ihe ihf
  | mul e f ihe ihf => exact .mul ihe ihf

/-- Both representations have exactly the same expressions and costs. -/
theorem reachable_iff_expr (m k : ℕ) :
    Reachable m k ↔ ∃ e : OnesExpr, e.eval = m ∧ e.size = k := by
  constructor
  · exact reachable_to_expr
  · rintro ⟨e, rfl, rfl⟩
    exact expr_to_reachable e

/-- The original Nat.find minimum equals the reused expression-tree minimum. -/
theorem complexity_eq_expression {n : ℕ} (hn : 0 < n) :
    complexity n = OpenProblems.IntegerComplexity.complexity n := by
  let witness : ∃ k, Reachable n k := ⟨n, Reachable.self n hn⟩
  have hdef : complexity n = Nat.find witness := by
    unfold complexity
    rw [dif_neg (Nat.ne_of_gt hn)]
  rw [hdef]
  apply le_antisymm
  · obtain ⟨e, he, hs⟩ :=
      OpenProblems.IntegerComplexity.exists_optimal (n := n) (by omega)
    apply Nat.find_min'
    rw [← he, ← hs]
    exact expr_to_reachable e
  · obtain ⟨e, he, hs⟩ := reachable_to_expr (Nat.find_spec witness)
    have h := OpenProblems.IntegerComplexity.complexity_le_size e
    simpa only [he, hs] using h

theorem complexity_three_pow_value (n : ℕ) (hn : 0 < n) :
    complexity (3 ^ n) = 3 * n := by
  rw [complexity_eq_expression (Nat.pow_pos (by decide))]
  exact OpenProblems.IntegerComplexity.complexity_three_pow (by omega)

/-- The source's answer(True) wrapper elaborates to True. Fidelity review pending. -/
theorem complexity_three_pow :
    True ↔ ∀ n : ℕ, 0 < n → complexity (3 ^ n) = 3 * n := by
  constructor
  · intro _ n hn
    exact complexity_three_pow_value n hn
  · intro _
    trivial

end Mathoverflow75792

#print Mathoverflow75792.complexity_three_pow
#print axioms Mathoverflow75792.reachable_iff_expr
#print axioms Mathoverflow75792.complexity_eq_expression
#print axioms Mathoverflow75792.complexity_three_pow
