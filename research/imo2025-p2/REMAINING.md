# Remaining proof obligations

The full target is still the exact mathematical signature in frozen-target.txt. FullTargetAttempt.lean genuinely fails at its remaining goal. Do not label the record proved or audited.

1. Build a normalized affine isometry from the given two-dimensional torsor, taking M to (0,0), N to (d,0), with d=dist M N>0. A possible Mathlib route uses an orientation, its areaForm and inner products. FiniteDimensional.of_fact_finrank_eq_two supplies the existing dimension context; it is not a new assumption.
2. Derive the normalized circle equations and y≠0 from the two distinct common points A,B and the original affine-independence hypotheses. Generic positive radii and d<r+R are separate supporting results. Derive every denominator bound, including r,R,d,r+R-d.
3. Identify actual B as (x,-y), C as (-r,0), D as (d+R,0), respecting the original strict betweenness. No sampled Harmonic orientation or numeric nondegeneracy condition may be inserted.
4. Use circumcenter equidistance to instantiate circumcenter_coordinates for actual P.
5. Use the derived actual secondInter identities in FullTargetAttempt.lean to prove the candidate E,F formulas. Candidate polynomial memberships alone do not identify actual intersections.
6. Prove actual H has the proposed coordinates from Mathlib Triangle.orthocenter, identify its parallel line, and prove affine independence of actual B,E,F.
7. Identify the candidate polynomial zero set with the actual circumcircle. Apply normalized_unique_parameter and contact_is_reflected_A to prove incidence and uniqueness at T=(N -ᵥ A)+ᵥ M.
8. Apply tangentAt_of_unique_intersection only after its premises are proved for the actual circle/line. Close the unchanged original existential goal.

Source proofs are linked in README and provenance; do not copy unlicensed traces. Keep generation separate from verification and leave independent fidelity/trust review pending. No local execution: all next builds go through bounded remote Actions runs.
