import Mathlib.NumberTheory.Wilson
import Mathlib.NumberTheory.LegendreSymbol.QuadraticReciprocity
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

namespace BrocardPrimeOffset

/-- Wilson's theorem reduces n! to one when the prime modulus is n+2. -/
theorem factorial_eq_one_mod_prime_offset (n : ℕ) (hp : (n + 2).Prime) :
    (n.factorial : ZMod (n + 2)) = 1 := by
  letI : Fact (n + 2).Prime := ⟨hp⟩
  have hw : ((n + 1).factorial : ZMod (n + 2)) = -1 := by
    simpa using ZMod.wilsons_lemma (n + 2)
  have hzero : ((n + 2 : ℕ) : ZMod (n + 2)) = 0 := by simp
  have hsum : ((n + 1 : ℕ) : ZMod (n + 2)) + 1 = 0 := by
    have heq : n + 2 = (n + 1) + 1 := by omega
    simpa only [heq, Nat.cast_add, Nat.cast_one] using hzero
  have hcoef : ((n + 1 : ℕ) : ZMod (n + 2)) = -1 := by
    simpa using congrArg (fun z : ZMod (n + 2) => z - 1) hsum
  have hmul : ((n + 1 : ℕ) : ZMod (n + 2)) *
      (n.factorial : ZMod (n + 2)) = -1 := by
    simpa only [Nat.factorial_succ, Nat.cast_mul] using hw
  rw [hcoef] at hmul
  simpa using congrArg Neg.neg hmul

/-- An actual solution at a positive n forces n+2 into residues 1 or7 modulo8. -/
theorem solution_prime_offset_residues (n m : ℕ) (hn : 0 < n)
    (hp : (n + 2).Prime) (hsol : n.factorial + 1 = m ^ 2) :
    (n + 2) % 8 = 1 ∨ (n + 2) % 8 = 7 := by
  letI : Fact (n + 2).Prime := ⟨hp⟩
  have hfac := factorial_eq_one_mod_prime_offset n hp
  have hcast := congrArg (fun k : ℕ => (k : ZMod (n + 2))) hsol
  have hm : (m : ZMod (n + 2)) ^ 2 = 2 := by
    simpa only [Nat.cast_add, Nat.cast_one, Nat.cast_pow, hfac, one_add_one_eq_two] using hcast.symm
  have hsquare : IsSquare (2 : ZMod (n + 2)) :=
    ⟨(m : ZMod (n + 2)), by simpa only [pow_two] using hm.symm⟩
  exact (ZMod.exists_sq_eq_two_iff (by omega)).mp hsquare

/-- An unbounded family rule, not an exhaustive classification of all n. -/
theorem prime_offset_two_obstruction (n : ℕ) (hp : (n + 2).Prime)
    (hbad : (n + 2) % 8 = 3 ∨ (n + 2) % 8 = 5) :
    ∀ m : ℕ, n.factorial + 1 ≠ m ^ 2 := by
  intro m hsol
  have hn : 0 < n := by omega
  have hgood := solution_prime_offset_residues n m hn hp hsol
  omega

/-- A concrete instantiation confirms that the excluded family is nonempty. -/
theorem reject_eleven : ∀ m : ℕ, Nat.factorial 11 + 1 ≠ m ^ 2 := by
  apply prime_offset_two_obstruction 11
  · norm_num
  · norm_num

/-- A known solution lies on an allowed branch (n+2=7). -/
theorem known_pair_five : Nat.factorial 5 + 1 = 11 ^ 2 := by norm_num

#check factorial_eq_one_mod_prime_offset
#check solution_prime_offset_residues
#check prime_offset_two_obstruction
#check reject_eleven
#check known_pair_five
#print axioms factorial_eq_one_mod_prime_offset
#print axioms solution_prime_offset_residues
#print axioms prime_offset_two_obstruction
#print axioms reject_eleven
#print axioms known_pair_five

end BrocardPrimeOffset
