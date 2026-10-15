import Std

theorem candidate : ∀ n : Nat, ∃ m : Nat, n < m := by
  intro n
  exact ⟨n + 1, Nat.lt_succ_self n⟩

#print axioms candidate
