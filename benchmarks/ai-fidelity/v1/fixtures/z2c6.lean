import Std

theorem candidate (k : Nat) : Nat.succ k + 0 = Nat.succ k := by
  exact Nat.add_zero (Nat.succ k)

#print axioms candidate
