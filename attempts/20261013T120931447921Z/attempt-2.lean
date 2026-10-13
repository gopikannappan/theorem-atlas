namespace TheoremAtlas.Pilot
theorem odd_denominator_ne_zero (n : Nat) : 2 * n + 1 ≠ 0 := by
  exact Nat.succ_ne_zero (2 * n)
end TheoremAtlas.Pilot
#print axioms TheoremAtlas.Pilot.odd_denominator_ne_zero
