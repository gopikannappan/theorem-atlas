import Mathlib.Basic.Real.Basic
import Mathlib.Geometry.Euclidean.Sphere.Tangent
import Mathlib.Geometry.Euclidean.Sphere.SecondInter
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.NormNum

set_option maxHeartbeats 2000000

namespace IMO2025P2Coordinates

/-- Coordinates of a point on both original circles give this linear relation. -/
theorem circle_difference (r R d x y : ℝ)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2) :
    2 * d * x = d ^ 2 + r ^ 2 - R ^ 2 := by
  nlinarith [hA, hB]

/-- The exact height identity; no sampled diagram is used. -/
theorem circle_height_identity (r R d x y : ℝ)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2) :
    4 * d ^ 2 * y ^ 2 =
      (d + (R + r)) * (R + r - d) * (d ^ 2 - (R - r) ^ 2) := by
  have hlin := circle_difference r R d x y hA hB
  linear_combination 4 * d ^ 2 * hA -
    (2 * d * x + d ^ 2 + r ^ 2 - R ^ 2) * hlin

/-- Circumcenter coordinates derived from equidistance, not assumed as formulas. -/
theorem circumcenter_coordinates (r R d x y p q : ℝ)
    (hr : 0 < r) (hR : 0 < R) (hd : 0 < d) (hy : y ≠ 0)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2)
    (hPA : (p - x) ^ 2 + (q - y) ^ 2 = (p + r) ^ 2 + q ^ 2)
    (hCD : (p + r) ^ 2 + q ^ 2 = (p - d - R) ^ 2 + q ^ 2) :
    2 * p = d + R - r ∧ (R + r - d) * q = -d * y := by
  have hsum : d + R + r ≠ 0 := ne_of_gt (by linarith)
  have hfactor : (d + R + r) * (2 * p - d - R + r) = 0 := by
    nlinarith [hCD]
  have hp : 2 * p = d + R - r := by
    rcases mul_eq_zero.mp hfactor with h | h
    · exact (hsum h).elim
    · linarith
  have hlin := circle_difference r R d x y hA hB
  have hkp : (R + r - d) * p = d * (r - x) := by
    linear_combination ((R + r - d) / 2) * hp + (1 / 2 : ℝ) * hlin
  have hqy : q * y = -p * (x + r) := by nlinarith [hPA, hA]
  have hkp2 : (R + r - d) * p * (x + r) = d * y ^ 2 := by
    linear_combination (x + r) * hkp - d * hA
  have hzero : ((R + r - d) * q + d * y) * y = 0 := by
    linear_combination (R + r - d) * hqy - hkp2
  refine ⟨hp, ?_⟩
  rcases mul_eq_zero.mp hzero with h | h
  · linarith
  · exact (hy h).elim

/-- A polynomial intended for the normalized circumcircle. Identifying it with the
actual circumcircle of B,E,F is a separate, currently unproved geometry step. -/
def circlePolynomial (d U V y X Y : ℝ) : ℝ :=
  X ^ 2 + Y ^ 2 - d * X + ((V ^ 2 - d ^ 2) / (2 * y)) * Y +
    (V ^ 2 - U ^ 2) / 4

def lineX (d U V t : ℝ) : ℝ :=
  (d + U) / 2 + (U * (d + V) / (2 * d)) * t

def lineY (d V y t : ℝ) : ℝ :=
  -d * y / (d + V) - (V * y / (V - d)) * t

/-- The main analytic factorization. This is not yet the full affine-geometry theorem. -/
theorem normalized_line_factorization (d U V y t : ℝ)
    (hd : d ≠ 0) (hy : y ≠ 0) (hS : d + V ≠ 0) (hK : V - d ≠ 0)
    (hheight : 4 * d ^ 2 * y ^ 2 = (d + V) * (V - d) * (d ^ 2 - U ^ 2)) :
    circlePolynomial d U V y (lineX d U V t) (lineY d V y t) =
      ((V ^ 2 - U ^ 2) / 4) * (d + V) / (V - d) *
        (t - (V - d) / (d + V)) ^ 2 := by
  have herror :
      circlePolynomial d U V y (lineX d U V t) (lineY d V y t) -
        (((V ^ 2 - U ^ 2) / 4) * (d + V) / (V - d) *
          (t - (V - d) / (d + V)) ^ 2) =
      (4 * d ^ 2 * y ^ 2 - (d + V) * (V - d) * (d ^ 2 - U ^ 2)) *
        (d * (V - d) + V * (d + V) * t) ^ 2 /
        (4 * d ^ 2 * (d + V) ^ 2 * (V - d) ^ 2) := by
    unfold circlePolynomial lineX lineY
    field_simp [hd, hy, hS, hK]
    <;> ring
  apply sub_eq_zero.mp
  simpa only [hheight, sub_self, zero_mul, zero_div] using herror

/-- A unique line parameter for the normalized polynomial zero set. This does not
identify that zero set or line with the official geometric constructions. -/
theorem normalized_unique_parameter (d U V y t : ℝ)
    (hd : d ≠ 0) (hy : y ≠ 0) (hS : d + V ≠ 0) (hK : V - d ≠ 0)
    (hc : V ^ 2 - U ^ 2 ≠ 0)
    (hheight : 4 * d ^ 2 * y ^ 2 = (d + V) * (V - d) * (d ^ 2 - U ^ 2)) :
    circlePolynomial d U V y (lineX d U V t) (lineY d V y t) = 0 ↔
      t = (V - d) / (d + V) := by
  rw [normalized_line_factorization d U V y t hd hy hS hK hheight]
  have hcoef : ((V ^ 2 - U ^ 2) / 4) * (d + V) / (V - d) ≠ 0 :=
    div_ne_zero (mul_ne_zero (div_ne_zero hc (by norm_num)) hS) hK
  constructor
  · intro h
    have hs : (t - (V - d) / (d + V)) ^ 2 = 0 :=
      (mul_eq_zero.mp h).resolve_left hcoef
    exact sub_eq_zero.mp (sq_eq_zero_iff.mp hs)
  · intro h
    rw [h]
    simp

#check circle_difference
#check circle_height_identity
#check circumcenter_coordinates
#check normalized_line_factorization
#check normalized_unique_parameter
#print axioms circle_difference
#print axioms circle_height_identity
#print axioms circumcenter_coordinates
#print axioms normalized_line_factorization
#print axioms normalized_unique_parameter


/-- The candidate polynomial contains the reflected common-circle point. -/
theorem candidate_B_on_polynomial (r R d x y : ℝ) (hy : y ≠ 0)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2) :
    circlePolynomial d (R - r) (R + r) y x (-y) = 0 := by
  have hlin := circle_difference r R d x y hA hB
  have hid :
      circlePolynomial d (R - r) (R + r) y x (-y) =
        (x ^ 2 + y ^ 2 - r ^ 2) -
          (2 * d * x - (d ^ 2 + r ^ 2 - R ^ 2)) / 2 := by
    unfold circlePolynomial
    field_simp [hy]
    <;> ring
  simpa [hA, hlin] using hid

/-- Conditional membership for the proposed E coordinates; the full geometry
still has to establish that the actual second intersection has these coordinates. -/
theorem candidate_E_on_polynomial (r R d x y : ℝ)
    (hR : R ≠ 0) (hy : y ≠ 0)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2) :
    circlePolynomial d (R - r) (R + r) y (r / R * (d - x)) (-r / R * y) = 0 := by
  have hlin := circle_difference r R d x y hA hB
  have hid :
      circlePolynomial d (R - r) (R + r) y (r / R * (d - x)) (-r / R * y) =
        (r / R) ^ 2 * ((x - d) ^ 2 + y ^ 2 - R ^ 2) +
          (r / (2 * R)) * (2 * d * x - (d ^ 2 + r ^ 2 - R ^ 2)) := by
    unfold circlePolynomial
    field_simp [hR, hy]
    <;> ring
  simpa [hB, hlin] using hid

/-- Conditional membership for the proposed F coordinates. -/
theorem candidate_F_on_polynomial (r R d x y : ℝ)
    (hr : r ≠ 0) (hy : y ≠ 0)
    (hA : x ^ 2 + y ^ 2 = r ^ 2)
    (hB : (x - d) ^ 2 + y ^ 2 = R ^ 2) :
    circlePolynomial d (R - r) (R + r) y (d - R / r * x) (-R / r * y) = 0 := by
  have hlin := circle_difference r R d x y hA hB
  have hid :
      circlePolynomial d (R - r) (R + r) y (d - R / r * x) (-R / r * y) =
        (R / r) ^ 2 * (x ^ 2 + y ^ 2 - r ^ 2) -
          (R / (2 * r)) * (2 * d * x - (d ^ 2 + r ^ 2 - R ^ 2)) := by
    unfold circlePolynomial
    field_simp [hr, hy]
    <;> ring
  simpa [hA, hlin] using hid

#print axioms candidate_B_on_polynomial
#print axioms candidate_E_on_polynomial
#print axioms candidate_F_on_polynomial

end IMO2025P2Coordinates

namespace IMO2025P2Bridge

open EuclideanGeometry
variable {V P : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V]
  [MetricSpace P] [NormedAddTorsor V P]

/-- A unique intersection with an affine subspace implies actual Mathlib
sphere tangency at that point. This is a generic bridge, not the IMO proof. -/
theorem tangentAt_of_unique_intersection (s : Sphere P) (a : AffineSubspace ℝ P) (p : P)
    (hpS : p ∈ s) (hpA : p ∈ a)
    (hunique : ∀ q : P, q ∈ s → q ∈ a → q = p) :
    s.IsTangentAt p a := by
  refine ⟨hpS, hpA, ?_⟩
  intro x hx
  apply Sphere.mem_orthRadius_iff_inner_left.mpr
  apply Sphere.secondInter_eq_self_iff.mp
  apply hunique
  · exact (Sphere.secondInter_mem (x -ᵥ p)).mpr hpS
  · unfold Sphere.secondInter
    exact AffineSubspace.vadd_mem_of_mem_direction
      (a.direction.smul_mem _ (AffineSubspace.vsub_mem_direction hx hpA)) hpA

theorem tangent_of_unique_intersection (s : Sphere P) (a : AffineSubspace ℝ P) (p : P)
    (hpS : p ∈ s) (hpA : p ∈ a)
    (hunique : ∀ q : P, q ∈ s → q ∈ a → q = p) :
    s.IsTangent a :=
  (tangentAt_of_unique_intersection s a p hpS hpA hunique).isTangent

#print axioms tangentAt_of_unique_intersection
#print axioms tangent_of_unique_intersection

end IMO2025P2Bridge

