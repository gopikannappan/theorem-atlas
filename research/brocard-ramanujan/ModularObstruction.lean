import Std

namespace BrocardResearch

/-- A modular non-square certificate rules out an integer square.
This generic lemma does not instantiate a factorial, primality, Wilson's theorem,
or any particular research search result. -/
theorem nonsquare_of_modular_obstruction (N q : Nat) (hq : 0 < q)
    (obstruction : ∀ r : Nat, r < q → (r * r) % q ≠ N % q) :
    ∀ m : Nat, N ≠ m * m := by
  intro m heq
  have hmod : ((m % q) * (m % q)) % q = N % q := by
    calc
      ((m % q) * (m % q)) % q = (m * m) % q := (Nat.mul_mod m m q).symm
      _ = N % q := congrArg (fun t : Nat => t % q) heq.symm
  exact obstruction (m % q) (Nat.mod_lt m hq) hmod

#print axioms nonsquare_of_modular_obstruction

end BrocardResearch
