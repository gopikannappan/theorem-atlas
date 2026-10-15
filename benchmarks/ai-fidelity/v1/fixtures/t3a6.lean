import Std

theorem candidate (n : Nat) (h : n = 0) : n = 0 ∨ ∃ k : Nat, n = k + 1 := by
  exact Or.inl h

#print axioms candidate
