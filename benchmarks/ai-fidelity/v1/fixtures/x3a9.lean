import Std

theorem candidate (n : Nat) (h : n < n) : n < n + 1 := by
  exact False.elim (Nat.lt_irrefl n h)

#print axioms candidate
