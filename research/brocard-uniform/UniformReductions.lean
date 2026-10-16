import Mathlib.NumberTheory.Wilson
import Mathlib.Data.Nat.GCD.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

namespace BrocardUniform

/-- An exact reformulation, with no upper bound on n or m. -/
theorem consecutive_factorization_iff (n m : ℕ) (hn : 4 ≤ n) :
    n.factorial + 1 = m ^ 2 ↔
      ∃ a b : ℕ, b = a + 1 ∧ a.Coprime b ∧
        4 * a * b = n.factorial ∧ m = a + b := by
  constructor
  · intro hsol
    have htwo : 2 ∣ n.factorial := Nat.dvd_factorial (by decide) (by omega)
    have hz : n.factorial % 2 = 0 := Nat.mod_eq_zero_of_dvd htwo
    have hodd : m % 2 = 1 := by
      by_contra hnot
      have hm0 : m % 2 = 0 := by omega
      have hs0 : (n.factorial + 1) % 2 = 0 := by
        rw [hsol, Nat.pow_mod, hm0]
      omega
    have hm : m = 2 * (m / 2) + 1 := by omega
    refine ⟨m / 2, m / 2 + 1, rfl, ?_, ?_, ?_⟩
    · exact Nat.coprime_self_add_right.mpr (by simp)
    · nlinarith [hsol]
    · omega
  · rintro ⟨a, b, hb, _hcop, hprod, hm⟩
    subst b
    subst m
    nlinarith

/-- If n+1 is prime, any solution forces that prime squared to divide n!+1. -/
theorem prime_successor_square_divides (n m : ℕ)
    (hp : (n + 1).Prime) (hsol : n.factorial + 1 = m ^ 2) :
    (n + 1) ^ 2 ∣ n.factorial + 1 := by
  letI : Fact (n + 1).Prime := ⟨hp⟩
  have hw : (n.factorial : ZMod (n + 1)) = -1 := by
    simpa using ZMod.wilsons_lemma (n + 1)
  have hzero : ((n.factorial + 1 : ℕ) : ZMod (n + 1)) = 0 := by
    rw [Nat.cast_add, Nat.cast_one, hw]
    exact neg_add_cancel 1
  have hdvd : n + 1 ∣ n.factorial + 1 :=
    (ZMod.natCast_eq_zero_iff _ _).mp hzero
  rw [hsol] at hdvd
  have hm : n + 1 ∣ m := hp.dvd_of_dvd_pow hdvd
  rw [hsol]
  exact pow_dvd_pow_of_dvd hm 2

/-- The contrapositive is an obstruction valid at every prime successor. -/
theorem prime_successor_obstruction (n : ℕ) (hp : (n + 1).Prime)
    (hnot : ¬ (n + 1) ^ 2 ∣ n.factorial + 1) :
    ∀ m : ℕ, n.factorial + 1 ≠ m ^ 2 := by
  intro m hsol
  exact hnot (prime_successor_square_divides n m hp hsol)

/-- Any fixed positive modulus is eventually uninformative for this square test. -/
theorem fixed_modulus_eventually_one (q n : ℕ) (hq : 0 < q) (hn : q ≤ n) :
    (n.factorial + 1) % q = 1 % q := by
  have hz : n.factorial % q = 0 :=
    Nat.mod_eq_zero_of_dvd (Nat.dvd_factorial hq hn)
  simp [Nat.add_mod, hz]

#check consecutive_factorization_iff
#check prime_successor_square_divides
#check prime_successor_obstruction
#check fixed_modulus_eventually_one
#print axioms consecutive_factorization_iff
#print axioms prime_successor_square_divides
#print axioms prime_successor_obstruction
#print axioms fixed_modulus_eventually_one

end BrocardUniform
