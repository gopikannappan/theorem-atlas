/-
Copyright (c) 2025 The Compfiles Contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Joseph Myers
Statement adapted from Compfiles commit1745e6ced3e671bd74417548494b034eb2c87da8.
Adaptation: problem-extraction DSL replaced by a standard theorem declaration.
No mathematical hypotheses or conclusion changed.
The attempted proof below is not certified if compilation fails.
-/
import Mathlib.Geometry.Euclidean.Sphere.Tangent
import Mathlib.Geometry.Euclidean.MongePoint
import Mathlib.Analysis.Convex.BetweenList
import Mathlib.Geometry.Euclidean.Sphere.SecondInter
import Mathlib.Analysis.InnerProductSpace.TwoDim
import Mathlib.Tactic.Ring
import Aesop

open scoped Real
open Affine EuclideanGeometry Module

namespace Imo2025P2
variable {V Pt : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [MetricSpace Pt]
variable [NormedAddTorsor V Pt] [Fact (finrank ℝ V = 2)]

set_option maxHeartbeats 200000 in
theorem imo2025_p2 {M N A B C D P E F H : Pt} {Ω Γ : Sphere Pt}
    (Ω_center_eq_M : Ω.center = M) (Γ_center_eq_N : Γ.center = N)
    (Ω_radius_lt_Γ_radius : Ω.radius < Γ.radius)
    (A_mem_inter : A ∈ (Ω ∩ Γ : Set Pt)) (B_mem_inter : B ∈ (Ω ∩ Γ : Set Pt))
    (A_ne_B : A ≠ B) (M_ne_N : M ≠ N)
    (C_mem_inter : C ∈ (line[ℝ, M, N] ∩ Ω : Set Pt))
    (D_mem_inter : D ∈ (line[ℝ, M, N] ∩ Γ : Set Pt))
    (sbtw_C_M_N_D : [C, M, N, D].Sbtw ℝ)
    (affineIndependent_ACD : AffineIndependent ℝ ![A, C, D])
    (P_eq_circumcenter :
      P = (⟨_, affineIndependent_ACD⟩ : Triangle ℝ Pt).circumcenter)
    (E_mem_inter : E ∈ (line[ℝ, A, P] ∩ Ω : Set Pt)) (E_ne_A : E ≠ A)
    (F_mem_inter : F ∈ (line[ℝ, A, P] ∩ Γ : Set Pt)) (F_ne_A : F ≠ A)
    (affineIndependent_PMN : AffineIndependent ℝ ![P, M, N])
    (H_eq_orthocenter :
      H = Triangle.orthocenter (⟨_, affineIndependent_PMN⟩ : Triangle ℝ Pt)) :
    ∃ affineIndependent_BEF : AffineIndependent ℝ ![B, E, F],
      (⟨_, affineIndependent_BEF⟩ : Triangle ℝ Pt).circumsphere.IsTangent
        (AffineSubspace.mk' H line[ℝ, A, P].direction) := by
  classical
  have hΩpos : 0 < Ω.radius := by
    rw [← mem_sphere.mp A_mem_inter.1]
    exact dist_pos.mpr
      (Sphere.ne_center_of_mem_of_mem_of_ne A_mem_inter.1 B_mem_inter.1 A_ne_B)
  have hΓpos : 0 < Γ.radius := by
    rw [← mem_sphere.mp A_mem_inter.2]
    exact dist_pos.mpr
      (Sphere.ne_center_of_mem_of_mem_of_ne A_mem_inter.2 B_mem_inter.2 A_ne_B)
  have hdpos : 0 < dist M N := dist_pos.mpr M_ne_N
  have hEsecond : E = Ω.secondInter A (P -ᵥ A) :=
    ((Sphere.eq_or_eq_secondInter_iff_mem_of_mem_affineSpan_pair
      A_mem_inter.1 E_mem_inter.1).mpr E_mem_inter.2).resolve_left E_ne_A
  have hFsecond : F = Γ.secondInter A (P -ᵥ A) :=
    ((Sphere.eq_or_eq_secondInter_iff_mem_of_mem_affineSpan_pair
      A_mem_inter.2 F_mem_inter.1).mpr F_mem_inter.2).resolve_left F_ne_A

  letI : FiniteDimensional ℝ V := FiniteDimensional.of_fact_finrank_eq_two
  let o : Orientation ℝ V (Fin 2) :=
    ((stdOrthonormalBasis ℝ V).reindex
      (finCongr (Fact.out : finrank ℝ V = 2))).toBasis.orientation
  let n : V := N -ᵥ M
  let z : V := A -ᵥ M
  let d : ℝ := ‖n‖
  let x : ℝ := inner ℝ n z / d
  let y : ℝ := o.areaForm n z / d
  have hn : n ≠ 0 := by simpa only [n, ne_eq, vsub_eq_zero_iff_eq] using M_ne_N.symm
  have hd : d ≠ 0 := norm_ne_zero_iff.mpr hn
  have hframe (v : V) :
      (inner ℝ n v / d) ^ 2 + (o.areaForm n v / d) ^ 2 = ‖v‖ ^ 2 := by
    rw [div_pow, div_pow, ← add_div]
    apply (div_eq_iff (pow_ne_zero 2 hd)).mpr
    simpa only [d, mul_comm] using o.inner_sq_add_areaForm_sq n v
  have hz : ‖z‖ = Ω.radius := by
    simpa only [z, dist_eq_norm_vsub V, Ω_center_eq_M] using
      (mem_sphere.mp A_mem_inter.1)
  have hzN : ‖z - n‖ = Γ.radius := by
    simpa only [z, n, vsub_sub_vsub_cancel_right, dist_eq_norm_vsub V,
      Γ_center_eq_N] using (mem_sphere.mp A_mem_inter.2)
  have hxn : inner ℝ n n / d = d := by
    rw [real_inner_self_eq_norm_sq]
    change d ^ 2 / d = d
    apply (div_eq_iff hd).mpr
    ring
  have hxsub : inner ℝ n (z - n) / d = x - d := by
    rw [inner_sub_right, sub_div, hxn]
  have hysub : o.areaForm n (z - n) / d = y := by
    simp only [map_sub, o.areaForm_apply_self, sub_zero]
    rfl
  have hcircleΩ : x ^ 2 + y ^ 2 = Ω.radius ^ 2 := by
    simpa only [x, y, hz] using hframe z
  have hcircleΓ : (x - d) ^ 2 + y ^ 2 = Γ.radius ^ 2 := by
    simpa only [hxsub, hysub, hzN] using hframe (z - n)

  let T : Pt := (N -ᵥ A) +ᵥ M
  suffices h :
      ∃ affineIndependent_BEF : AffineIndependent ℝ ![B, E, F],
        (⟨_, affineIndependent_BEF⟩ : Triangle ℝ Pt).circumsphere.IsTangentAt T
          (AffineSubspace.mk' H line[ℝ, A, P].direction) by
    rcases h with ⟨hBEF, hT⟩
    exact ⟨hBEF, hT.isTangent⟩
  aesop

end Imo2025P2
