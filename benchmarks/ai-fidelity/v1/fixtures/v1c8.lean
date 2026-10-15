import Std

theorem candidate : ∃ n : Nat, ∃ m : Nat, n < m := by
  exact ⟨0, 1, Nat.zero_lt_succ 0⟩

#print axioms candidate
