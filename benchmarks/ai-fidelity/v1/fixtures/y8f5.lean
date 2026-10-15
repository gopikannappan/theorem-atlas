import Std

theorem candidate (n : Nat) : n = 0 ∨ ∃ k : Nat, n = k + 1 := by
  cases n with
  | zero => exact Or.inl rfl
  | succ k => exact Or.inr ⟨k, rfl⟩

#print axioms candidate
