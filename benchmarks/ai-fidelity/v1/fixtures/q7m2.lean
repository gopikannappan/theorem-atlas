import Std

theorem candidate (n : Nat) : n + 0 = n := by
  exact Nat.add_zero n

#print axioms candidate
