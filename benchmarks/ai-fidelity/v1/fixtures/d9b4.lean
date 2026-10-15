import Std

theorem candidate (n : Nat) : n = 0 → n + 1 = 1 := by
  intro h
  subst n
  rfl

#print axioms candidate
