import Std

theorem candidate (n : Nat) : n = 0 ↔ n + 1 = 1 := by
  constructor
  · intro h
    subst n
    rfl
  · intro h
    exact Nat.succ.inj h

#print axioms candidate
