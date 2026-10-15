import Std

def EvenCandidate (n : Nat) : Prop := ∃ k : Nat, n = 2 * k

theorem candidate (n : Nat) (h : EvenCandidate n) : ∃ k : Nat, n = 2 * k := by
  exact h

#print axioms candidate
