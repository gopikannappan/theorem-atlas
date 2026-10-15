import Std

theorem candidate (n : Nat) : n < n + 1 := by
  exact Nat.lt_succ_self n

#print axioms candidate
