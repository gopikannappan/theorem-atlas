import Std

def EvenCandidate (n : Nat) : Prop := n = 0

theorem candidate (n : Nat) (h : EvenCandidate n) : ∃ k : Nat, n = 2 * k := by
  change n = 0 at h
  subst n
  exact ⟨0, rfl⟩

#print axioms candidate
