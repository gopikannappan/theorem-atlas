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
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.FieldSimp
import Aesop

open scoped Real
open Affine EuclideanGeometry Module

namespace Imo2025P2
variable {V Pt : Type*} [NormedAddCommGroup V] [InnerProductSpace ℝ V] [MetricSpace Pt]
variable [NormedAddTorsor V Pt] [Fact (finrank ℝ V = 2)]

set_option maxHeartbeats 2000000 in
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


  have hcoords_ext {u v : V}
      (hx : inner ℝ n u / d = inner ℝ n v / d)
      (hy : o.areaForm n u / d = o.areaForm n v / d) : u = v := by
    have hx0 : inner ℝ n (u - v) / d = 0 := by
      rw [inner_sub_right, sub_div]
      exact sub_eq_zero.mpr hx
    have hy0 : o.areaForm n (u - v) / d = 0 := by
      rw [map_sub, sub_div]
      exact sub_eq_zero.mpr hy
    have hid := hframe (u - v)
    rw [hx0, hy0] at hid
    have hnorm : ‖u - v‖ ^ 2 = 0 := by nlinarith only [hid]
    exact sub_eq_zero.mp (norm_eq_zero.mp (sq_eq_zero_iff.mp hnorm))
  let w : V := B -ᵥ M
  let xb : ℝ := inner ℝ n w / d
  let yb : ℝ := o.areaForm n w / d
  have hw : ‖w‖ = Ω.radius := by
    simpa only [w, dist_eq_norm_vsub V, Ω_center_eq_M] using
      (mem_sphere.mp B_mem_inter.1)
  have hwN : ‖w - n‖ = Γ.radius := by
    simpa only [w, n, vsub_sub_vsub_cancel_right, dist_eq_norm_vsub V,
      Γ_center_eq_N] using (mem_sphere.mp B_mem_inter.2)
  have hxwsub : inner ℝ n (w - n) / d = xb - d := by
    rw [inner_sub_right, sub_div, hxn]
  have hywsub : o.areaForm n (w - n) / d = yb := by
    simp only [map_sub, o.areaForm_apply_self, sub_zero]
    rfl
  have hcircleBΩ : xb ^ 2 + yb ^ 2 = Ω.radius ^ 2 := by
    simpa only [xb, yb, hw] using hframe w
  have hcircleBΓ : (xb - d) ^ 2 + yb ^ 2 = Γ.radius ^ 2 := by
    simpa only [hxwsub, hywsub, hwN] using hframe (w - n)
  have hdistinctcoords : x ≠ xb ∨ y ≠ yb := by
    by_cases hx : x = xb
    · right
      intro hy
      have hzw : z = w := hcoords_ext hx hy
      exact A_ne_B (vsub_left_cancel hzw)
    · exact Or.inl hx
  have hLA : 2 * d * x = d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2 := by
    nlinarith only [hcircleΩ, hcircleΓ]
  have hLB : 2 * d * xb = d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2 := by
    nlinarith only [hcircleBΩ, hcircleBΓ]
  have hxb : xb = x := by
    apply mul_left_cancel₀ (mul_ne_zero two_ne_zero hd)
    exact hLB.trans hLA.symm
  have hyfactor : (yb - y) * (yb + y) = 0 := by
    rw [hxb] at hcircleBΩ
    nlinarith only [hcircleΩ, hcircleBΩ]
  have hyb : yb = -y := by
    rcases mul_eq_zero.mp hyfactor with h | h
    · have heq : yb = y := sub_eq_zero.mp h
      rcases hdistinctcoords with hx | hy
      · exact (hx hxb.symm).elim
      · exact (hy heq.symm).elim
    · linarith
  have hy_nonzero : y ≠ 0 := by
    intro hy0
    rcases hdistinctcoords with hx | hy
    · exact hx hxb.symm
    · exact hy (by rw [hyb, hy0]; ring)


  have hshiftframe (v : V) :
      (inner ℝ n v / d - d) ^ 2 + (o.areaForm n v / d) ^ 2 = ‖v - n‖ ^ 2 := by
    simpa only [inner_sub_right, map_sub, sub_div, hxn,
      o.areaForm_apply_self, zero_div, sub_zero] using hframe (v - n)
  have hMN : dist M N = d := dist_eq_norm_vsub' V M N
  have hCM : dist C M = Ω.radius := by
    simpa only [Ω_center_eq_M] using (mem_sphere.mp C_mem_inter.2)
  have hDN : dist D N = Γ.radius := by
    simpa only [Γ_center_eq_N] using (mem_sphere.mp D_mem_inter.2)
  have hCMN : Sbtw ℝ C M N := (List.sbtw_four.mp sbtw_C_M_N_D).1
  have hMND : Sbtw ℝ M N D := (List.sbtw_four.mp sbtw_C_M_N_D).2.2.2
  have hCN : dist C N = Ω.radius + d := by
    have heq := dist_add_dist_eq_iff.mpr hCMN.wbtw
    rw [hCM, hMN] at heq
    exact heq.symm
  have hMD : dist M D = d + Γ.radius := by
    have heq := dist_add_dist_eq_iff.mpr hMND.wbtw
    rw [hMN, dist_comm N D, hDN] at heq
    exact heq.symm
  let c : V := C -ᵥ M
  let xc : ℝ := inner ℝ n c / d
  let yc : ℝ := o.areaForm n c / d
  have hc : ‖c‖ = Ω.radius := by
    simpa only [c, dist_eq_norm_vsub V] using hCM
  have hcn : ‖c - n‖ = Ω.radius + d := by
    simpa only [c, n, vsub_sub_vsub_cancel_right, dist_eq_norm_vsub V] using hCN
  have hc0 : xc ^ 2 + yc ^ 2 = Ω.radius ^ 2 := by
    simpa only [xc, yc, hc] using hframe c
  have hc1 : (xc - d) ^ 2 + yc ^ 2 = (Ω.radius + d) ^ 2 := by
    simpa only [xc, yc, hcn] using hshiftframe c
  have hxc : xc = -Ω.radius := by
    have hm : (2 * d) * (xc + Ω.radius) = 0 := by nlinarith only [hc0, hc1]
    have hz := (mul_eq_zero.mp hm).resolve_left (mul_ne_zero two_ne_zero hd)
    linarith
  have hyc : yc = 0 := by
    rw [hxc] at hc0
    nlinarith only [hc0]
  let dv : V := D -ᵥ M
  let xd : ℝ := inner ℝ n dv / d
  let yd : ℝ := o.areaForm n dv / d
  have hdv : ‖dv‖ = d + Γ.radius := by
    simpa only [dv, dist_eq_norm_vsub' V] using hMD
  have hdvn : ‖dv - n‖ = Γ.radius := by
    simpa only [dv, n, vsub_sub_vsub_cancel_right, dist_eq_norm_vsub V] using hDN
  have hdv0 : xd ^ 2 + yd ^ 2 = (d + Γ.radius) ^ 2 := by
    simpa only [xd, yd, hdv] using hframe dv
  have hdv1 : (xd - d) ^ 2 + yd ^ 2 = Γ.radius ^ 2 := by
    simpa only [xd, yd, hdvn] using hshiftframe dv
  have hxd : xd = d + Γ.radius := by
    have hm : (2 * d) * (xd - d - Γ.radius) = 0 := by nlinarith only [hdv0, hdv1]
    have hz := (mul_eq_zero.mp hm).resolve_left (mul_ne_zero two_ne_zero hd)
    linarith
  have hyd : yd = 0 := by
    rw [hxd] at hdv0
    nlinarith only [hdv0]


  have hdistframe (u v : Pt) :
      (inner ℝ n (u -ᵥ M) / d - inner ℝ n (v -ᵥ M) / d) ^ 2 +
        (o.areaForm n (u -ᵥ M) / d - o.areaForm n (v -ᵥ M) / d) ^ 2 =
      dist u v ^ 2 := by
    have hid := hframe ((u -ᵥ M) - (v -ᵥ M))
    rw [inner_sub_right, map_sub, sub_div, sub_div] at hid
    rw [vsub_sub_vsub_cancel_right] at hid
    simpa only [dist_eq_norm_vsub V] using hid
  let pvec : V := P -ᵥ M
  let px : ℝ := inner ℝ n pvec / d
  let py : ℝ := o.areaForm n pvec / d
  have hACdist : dist A P = dist C P := by
    have ha := (⟨_, affineIndependent_ACD⟩ : Triangle ℝ Pt).dist_circumcenter_eq_circumradius 0
    have hc' := (⟨_, affineIndependent_ACD⟩ : Triangle ℝ Pt).dist_circumcenter_eq_circumradius 1
    simpa [P_eq_circumcenter] using ha.trans hc'.symm
  have hCDdist : dist C P = dist D P := by
    have hc' := (⟨_, affineIndependent_ACD⟩ : Triangle ℝ Pt).dist_circumcenter_eq_circumradius 1
    have hd' := (⟨_, affineIndependent_ACD⟩ : Triangle ℝ Pt).dist_circumcenter_eq_circumradius 2
    simpa [P_eq_circumcenter] using hc'.trans hd'.symm
  have hPAcoord :
      (px - x) ^ 2 + (py - y) ^ 2 = (px + Ω.radius) ^ 2 + py ^ 2 := by
    have ha := hdistframe A P
    have hc' := hdistframe C P
    change (x - px) ^ 2 + (y - py) ^ 2 = dist A P ^ 2 at ha
    change (xc - px) ^ 2 + (yc - py) ^ 2 = dist C P ^ 2 at hc'
    rw [hxc, hyc] at hc'
    rw [hACdist] at ha
    nlinarith only [ha, hc']
  have hCDcoord :
      (px + Ω.radius) ^ 2 + py ^ 2 = (px - d - Γ.radius) ^ 2 + py ^ 2 := by
    have hc' := hdistframe C P
    have hd' := hdistframe D P
    change (xc - px) ^ 2 + (yc - py) ^ 2 = dist C P ^ 2 at hc'
    change (xd - px) ^ 2 + (yd - py) ^ 2 = dist D P ^ 2 at hd'
    rw [hxc, hyc] at hc'
    rw [hxd, hyd] at hd'
    rw [hCDdist] at hc'
    nlinarith only [hc', hd']
  have hdpositive : 0 < d := norm_pos_iff.mpr hn
  have hsum : d + Γ.radius + Ω.radius ≠ 0 := ne_of_gt (by linarith only [hdpositive, hΓpos, hΩpos])
  have hfactor : (d + Γ.radius + Ω.radius) *
      (2 * px - d - Γ.radius + Ω.radius) = 0 := by nlinarith only [hCDcoord]
  have hpx : 2 * px = d + Γ.radius - Ω.radius := by
    rcases mul_eq_zero.mp hfactor with h | h
    · exact (hsum h).elim
    · linarith only [h]
  have hkp : (Γ.radius + Ω.radius - d) * px = d * (Ω.radius - x) := by
    linear_combination ((Γ.radius + Ω.radius - d) / 2) * hpx + (1 / 2 : ℝ) * hLA
  have hqy : py * y = -px * (x + Ω.radius) := by nlinarith only [hPAcoord, hcircleΩ]
  have hkp2 : (Γ.radius + Ω.radius - d) * px * (x + Ω.radius) = d * y ^ 2 := by
    linear_combination (x + Ω.radius) * hkp - d * hcircleΩ
  have hpy : (Γ.radius + Ω.radius - d) * py = -d * y := by
    have hzero : ((Γ.radius + Ω.radius - d) * py + d * y) * y = 0 := by
      linear_combination (Γ.radius + Ω.radius - d) * hqy - hkp2
    rcases mul_eq_zero.mp hzero with h | h
    · linarith only [h]
    · exact (hy_nonzero h).elim


  let tPMN : Triangle ℝ Pt := ⟨_, affineIndependent_PMN⟩
  have haltitude (i j k : Fin 3) (hji : j ≠ i) (hki : k ≠ i) :
      inner ℝ (tPMN.points j -ᵥ tPMN.points k) (H -ᵥ tPMN.points i) = 0 := by
    have hj : tPMN.points j ∈ tPMN.points '' ({i}ᶜ) := ⟨j, by simpa using hji, rfl⟩
    have hk : tPMN.points k ∈ tPMN.points '' ({i}ᶜ) := ⟨k, by simpa using hki, rfl⟩
    have hside := vsub_mem_vectorSpan ℝ hj hk
    have hH : H ∈ tPMN.altitude i := by
      rw [H_eq_orthocenter]
      exact tPMN.orthocenter_mem_altitude
    have hdir := AffineSubspace.vsub_mem_direction hH (tPMN.mem_altitude i)
    exact (tPMN.vectorSpan_isOrtho_altitude_direction i).inner_eq hside hdir
  have hperp0 : inner ℝ n (H -ᵥ P) = 0 := by
    simpa [tPMN, n] using haltitude 0 2 1 (by decide) (by decide)
  have hperp1 : inner ℝ (P -ᵥ N) (H -ᵥ M) = 0 := by
    simpa [tPMN] using haltitude 1 0 2 (by decide) (by decide)
  let hvec : V := H -ᵥ M
  let hx : ℝ := inner ℝ n hvec / d
  let hy : ℝ := o.areaForm n hvec / d
  have hxP : hx = px := by
    have heq : inner ℝ n (hvec - pvec) / d = 0 := by
      simp only [hvec, pvec, vsub_sub_vsub_cancel_right, hperp0, zero_div]
    rw [inner_sub_right, sub_div] at heq
    exact sub_eq_zero.mp heq
  have hdotframe (u v : V) :
      (inner ℝ n u / d) * (inner ℝ n v / d) +
        (o.areaForm n u / d) * (o.areaForm n v / d) = inner ℝ u v := by
    have hid := o.inner_mul_inner_add_areaForm_mul_areaForm n u v
    change inner ℝ n u * inner ℝ n v + o.areaForm n u * o.areaForm n v =
      d ^ 2 * inner ℝ u v at hid
    field_simp [hd]
    nlinarith only [hid]
  have hdotP : px * (px - d) + py * hy = 0 := by
    have hrhs : inner ℝ (pvec - n) hvec = 0 := by
      simpa only [pvec, n, hvec, vsub_sub_vsub_cancel_right] using hperp1
    have heq := hdotframe (pvec - n) hvec
    rw [hrhs] at heq
    simp only [inner_sub_right, map_sub, sub_div, hxn, o.areaForm_apply_self,
      zero_div, sub_zero] at heq
    change (px - d) * hx + py * hy = 0 at heq
    rw [hxP] at heq
    nlinarith only [heq]
  have hheight :
      4 * d ^ 2 * y ^ 2 = (d + (Γ.radius + Ω.radius)) *
        (Γ.radius + Ω.radius - d) * (d ^ 2 - (Γ.radius - Ω.radius) ^ 2) := by
    linear_combination 4 * d ^ 2 * hcircleΩ -
      (2 * d * x + d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2) * hLA
  have hpq : 4 * py * hy = d ^ 2 - (Γ.radius - Ω.radius) ^ 2 := by
    have hid : 4 * px * (px - d) =
        (Γ.radius - Ω.radius) ^ 2 - d ^ 2 := by
      linear_combination (2 * px - d + (Γ.radius - Ω.radius)) * hpx
    linear_combination 4 * hdotP - hid
  have hHcoord : (d + (Γ.radius + Ω.radius)) * hy = -d * y := by
    have hm : ((d + (Γ.radius + Ω.radius)) * hy + d * y) * (d * y) = 0 := by
      linear_combination (1 / 4 : ℝ) * hheight +
        - ((d + (Γ.radius + Ω.radius)) * (Γ.radius + Ω.radius - d) / 4) * hpq +
        (d + (Γ.radius + Ω.radius)) * hy * hpy
    have hh := (mul_eq_zero.mp hm).resolve_right (mul_ne_zero hd hy_nonzero)
    linarith only [hh]


  have hlinecoords (t : ℝ) :
      inner ℝ n (((t • (P -ᵥ A)) +ᵥ A) -ᵥ M) / d = x + t * (px - x) ∧
      o.areaForm n (((t • (P -ᵥ A)) +ᵥ A) -ᵥ M) / d = y + t * (py - y) := by
    have hv : (((t • (P -ᵥ A)) +ᵥ A) -ᵥ M : V) = t • (pvec - z) + z := by
      simp only [vadd_vsub_assoc, pvec, z, vsub_sub_vsub_cancel_right]
    constructor
    · dsimp only [x, px]
      simp only [hv, inner_add_right, inner_smul_right, inner_sub_right, add_div, sub_div]
      ring
    · dsimp only [y, py]
      simp only [hv, map_add, map_smul, map_sub, smul_eq_mul, add_div, sub_div]
      ring
  have hRne : Γ.radius ≠ 0 := ne_of_gt hΓpos
  have hrne : Ω.radius ≠ 0 := ne_of_gt hΩpos
  let Estar : Pt := ((Γ.radius + Ω.radius - d) / Γ.radius) • (P -ᵥ A) +ᵥ A
  let Fstar : Pt := ((Γ.radius + Ω.radius - d) / Ω.radius) • (P -ᵥ A) +ᵥ A
  have hEco :
      inner ℝ n (Estar -ᵥ M) / d = Ω.radius / Γ.radius * (d - x) ∧
      o.areaForm n (Estar -ᵥ M) / d = -Ω.radius / Γ.radius * y := by
    obtain ⟨he1, he2⟩ := hlinecoords ((Γ.radius + Ω.radius - d) / Γ.radius)
    constructor
    · change inner ℝ n (Estar -ᵥ M) / d = _
      rw [he1]
      field_simp [hRne]
      nlinarith only [hkp]
    · change o.areaForm n (Estar -ᵥ M) / d = _
      rw [he2]
      field_simp [hRne]
      nlinarith only [hpy]
  have hFco :
      inner ℝ n (Fstar -ᵥ M) / d = d - Γ.radius / Ω.radius * x ∧
      o.areaForm n (Fstar -ᵥ M) / d = -Γ.radius / Ω.radius * y := by
    obtain ⟨hf1, hf2⟩ := hlinecoords ((Γ.radius + Ω.radius - d) / Ω.radius)
    constructor
    · change inner ℝ n (Fstar -ᵥ M) / d = _
      rw [hf1]
      field_simp [hrne]
      nlinarith only [hkp]
    · change o.areaForm n (Fstar -ᵥ M) / d = _
      rw [hf2]
      field_simp [hrne]
      nlinarith only [hpy]
  have hEstarSphere : Estar ∈ Ω := by
    have hf := hframe (Estar -ᵥ M)
    rw [hEco.1, hEco.2] at hf
    have heq : (Ω.radius / Γ.radius * (d - x)) ^ 2 +
        (-Ω.radius / Γ.radius * y) ^ 2 = Ω.radius ^ 2 := by
      calc
        (Ω.radius / Γ.radius * (d - x)) ^ 2 + (-Ω.radius / Γ.radius * y) ^ 2 =
            (Ω.radius / Γ.radius) ^ 2 * ((d - x) ^ 2 + y ^ 2) := by ring
        _ = (Ω.radius / Γ.radius) ^ 2 * Γ.radius ^ 2 := by
          rw [show (d - x) ^ 2 + y ^ 2 = Γ.radius ^ 2 by nlinarith only [hcircleΓ]]
        _ = Ω.radius ^ 2 := by field_simp [hRne] <;> ring
    rw [heq] at hf
    have hnE : ‖Estar -ᵥ M‖ = Ω.radius := by
      have hn0 := norm_nonneg (Estar -ᵥ M : V)
      nlinarith only [hf, hn0, hΩpos]
    apply mem_sphere.mpr
    simpa only [Ω_center_eq_M, dist_eq_norm_vsub V] using hnE
  have hFstarSphere : Fstar ∈ Γ := by
    have hf := hframe ((Fstar -ᵥ M) - n)
    have hxF : inner ℝ n ((Fstar -ᵥ M) - n) / d = -Γ.radius / Ω.radius * x := by
      rw [inner_sub_right, sub_div, hFco.1, hxn]
      ring
    have hyF : o.areaForm n ((Fstar -ᵥ M) - n) / d = -Γ.radius / Ω.radius * y := by
      simp only [map_sub, o.areaForm_apply_self, sub_zero, hFco.2]
    rw [hxF, hyF] at hf
    have heq : (-Γ.radius / Ω.radius * x) ^ 2 +
        (-Γ.radius / Ω.radius * y) ^ 2 = Γ.radius ^ 2 := by
      calc
        (-Γ.radius / Ω.radius * x) ^ 2 + (-Γ.radius / Ω.radius * y) ^ 2 =
            (Γ.radius / Ω.radius) ^ 2 * (x ^ 2 + y ^ 2) := by ring
        _ = (Γ.radius / Ω.radius) ^ 2 * Ω.radius ^ 2 := by rw [hcircleΩ]
        _ = Γ.radius ^ 2 := by field_simp [hrne] <;> ring
    rw [heq] at hf
    have hnF : ‖Fstar -ᵥ N‖ = Γ.radius := by
      rw [show ((Fstar -ᵥ M) - n : V) = Fstar -ᵥ N by
        simp only [n, vsub_sub_vsub_cancel_right]] at hf
      have hn0 := norm_nonneg (Fstar -ᵥ N : V)
      nlinarith only [hf, hn0, hΓpos]
    apply mem_sphere.mpr
    simpa only [Γ_center_eq_N, dist_eq_norm_vsub V] using hnF
  have hEstarNe : Estar ≠ A := by
    intro he
    have hyE : -Ω.radius / Γ.radius * y = y := by
      calc
        -Ω.radius / Γ.radius * y = o.areaForm n (Estar -ᵥ M) / d := hEco.2.symm
        _ = o.areaForm n (A -ᵥ M) / d := by rw [he]
        _ = y := rfl
    have hfactorE : -Ω.radius / Γ.radius = 1 := by
      apply mul_right_cancel₀ hy_nonzero
      simpa only [one_mul] using hyE
    have hcontr := (div_eq_iff hRne).mp hfactorE
    linarith only [hcontr, hΩpos, hΓpos]
  have hFstarNe : Fstar ≠ A := by
    intro he
    have hyF : -Γ.radius / Ω.radius * y = y := by
      calc
        -Γ.radius / Ω.radius * y = o.areaForm n (Fstar -ᵥ M) / d := hFco.2.symm
        _ = o.areaForm n (A -ᵥ M) / d := by rw [he]
        _ = y := rfl
    have hfactorF : -Γ.radius / Ω.radius = 1 := by
      apply mul_right_cancel₀ hy_nonzero
      simpa only [one_mul] using hyF
    have hcontr := (div_eq_iff hrne).mp hfactorF
    linarith only [hcontr, hΩpos, hΓpos]
  have hlineA : A ∈ line[ℝ, A, P] := left_mem_affineSpan_pair ℝ A P
  have hlineP : P ∈ line[ℝ, A, P] := right_mem_affineSpan_pair ℝ A P
  have hlineStar (t : ℝ) : (t • (P -ᵥ A)) +ᵥ A ∈ line[ℝ, A, P] :=
    AffineSubspace.vadd_mem_of_mem_direction
      ((line[ℝ, A, P]).direction.smul_mem _ (AffineSubspace.vsub_mem_direction hlineP hlineA)) hlineA
  have hEstarE : Estar = E := by
    have hsecond := ((Sphere.eq_or_eq_secondInter_iff_mem_of_mem_affineSpan_pair
      A_mem_inter.1 (hlineStar ((Γ.radius + Ω.radius - d) / Γ.radius))).mpr hEstarSphere).resolve_left hEstarNe
    exact hsecond.trans hEsecond.symm
  have hFstarF : Fstar = F := by
    have hsecond := ((Sphere.eq_or_eq_secondInter_iff_mem_of_mem_affineSpan_pair
      A_mem_inter.2 (hlineStar ((Γ.radius + Ω.radius - d) / Ω.radius))).mpr hFstarSphere).resolve_left hFstarNe
    exact hsecond.trans hFsecond.symm
  have hEcoordinates :
      inner ℝ n (E -ᵥ M) / d = Ω.radius / Γ.radius * (d - x) ∧
      o.areaForm n (E -ᵥ M) / d = -Ω.radius / Γ.radius * y := by
    simpa only [hEstarE] using hEco
  have hFcoordinates :
      inner ℝ n (F -ᵥ M) / d = d - Γ.radius / Ω.radius * x ∧
      o.areaForm n (F -ᵥ M) / d = -Γ.radius / Ω.radius * y := by
    simpa only [hFstarF] using hFco


  let circleCoeff : ℝ := ((Γ.radius + Ω.radius) ^ 2 - d ^ 2) / (2 * y)
  let circlePoly : ℝ → ℝ → ℝ := fun X Y =>
    X ^ 2 + Y ^ 2 - d * X + circleCoeff * Y + Γ.radius * Ω.radius
  let centerVector : V :=
    ((d / 2) / d) • n + ((-circleCoeff / 2) / d) • o.rightAngleRotation n
  let circleCenter : Pt := centerVector +ᵥ M
  have hcenter :
      inner ℝ n (circleCenter -ᵥ M) / d = d / 2 ∧
      o.areaForm n (circleCenter -ᵥ M) / d = -circleCoeff / 2 := by
    constructor
    · simp only [circleCenter, vadd_vsub, centerVector, inner_add_right,
        inner_smul_right, o.inner_rightAngleRotation_right, o.areaForm_apply_self,
        neg_zero, mul_zero, add_zero, real_inner_self_eq_norm_sq]
      change ((d / 2 / d) * d ^ 2) / d = d / 2
      field_simp [hd] <;> ring
    · simp only [circleCenter, vadd_vsub, centerVector, map_add, map_smul,
        smul_eq_mul, o.areaForm_apply_self, mul_zero, zero_add,
        o.areaForm_rightAngleRotation_right, real_inner_self_eq_norm_sq]
      change ((-circleCoeff / 2 / d) * d ^ 2) / d = -circleCoeff / 2
      field_simp [hd] <;> ring
  have hBpoly : circlePoly x (-y) = 0 := by
    have hid : circlePoly x (-y) =
        (x ^ 2 + y ^ 2 - Ω.radius ^ 2) -
          (2 * d * x - (d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2)) / 2 := by
      dsimp only [circlePoly, circleCoeff]
      field_simp [hy_nonzero]
      <;> ring
    simpa only [hcircleΩ, hLA, sub_self, zero_div] using hid
  have hEpoly : circlePoly (Ω.radius / Γ.radius * (d - x)) (-Ω.radius / Γ.radius * y) = 0 := by
    have hid : circlePoly (Ω.radius / Γ.radius * (d - x)) (-Ω.radius / Γ.radius * y) =
        (Ω.radius / Γ.radius) ^ 2 * ((x - d) ^ 2 + y ^ 2 - Γ.radius ^ 2) +
          (Ω.radius / (2 * Γ.radius)) *
            (2 * d * x - (d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2)) := by
      dsimp only [circlePoly, circleCoeff]
      field_simp [hRne, hy_nonzero]
      <;> ring
    simpa only [hcircleΓ, hLA, sub_self, mul_zero, add_zero] using hid
  have hFpoly : circlePoly (d - Γ.radius / Ω.radius * x) (-Γ.radius / Ω.radius * y) = 0 := by
    have hid : circlePoly (d - Γ.radius / Ω.radius * x) (-Γ.radius / Ω.radius * y) =
        (Γ.radius / Ω.radius) ^ 2 * (x ^ 2 + y ^ 2 - Ω.radius ^ 2) -
          (Γ.radius / (2 * Ω.radius)) *
            (2 * d * x - (d ^ 2 + Ω.radius ^ 2 - Γ.radius ^ 2)) := by
      dsimp only [circlePoly, circleCoeff]
      field_simp [hrne, hy_nonzero]
      <;> ring
    simpa only [hcircleΩ, hLA, sub_self, mul_zero, sub_zero] using hid
  have hpolydist (q : Pt) :
      dist q circleCenter ^ 2 - dist B circleCenter ^ 2 =
        circlePoly (inner ℝ n (q -ᵥ M) / d) (o.areaForm n (q -ᵥ M) / d) := by
    let qx : ℝ := inner ℝ n (q -ᵥ M) / d
    let qy : ℝ := o.areaForm n (q -ᵥ M) / d
    have hq := hdistframe q circleCenter
    have hb := hdistframe B circleCenter
    change (qx - inner ℝ n (circleCenter -ᵥ M) / d) ^ 2 +
      (qy - o.areaForm n (circleCenter -ᵥ M) / d) ^ 2 = dist q circleCenter ^ 2 at hq
    change (xb - inner ℝ n (circleCenter -ᵥ M) / d) ^ 2 +
      (yb - o.areaForm n (circleCenter -ᵥ M) / d) ^ 2 = dist B circleCenter ^ 2 at hb
    rw [hcenter.1, hcenter.2] at hq hb
    rw [hxb, hyb] at hb
    change dist q circleCenter ^ 2 - dist B circleCenter ^ 2 = circlePoly qx qy
    have hp := hBpoly
    dsimp only [circlePoly] at hp ⊢
    linear_combination -hq + hb - hp
  have hEpolyActual :
      circlePoly (inner ℝ n (E -ᵥ M) / d) (o.areaForm n (E -ᵥ M) / d) = 0 := by
    simpa only [hEcoordinates.1, hEcoordinates.2] using hEpoly
  have hFpolyActual :
      circlePoly (inner ℝ n (F -ᵥ M) / d) (o.areaForm n (F -ᵥ M) / d) = 0 := by
    simpa only [hFcoordinates.1, hFcoordinates.2] using hFpoly
  have hEdist : dist E circleCenter = dist B circleCenter := by
    have hq := hpolydist E
    rw [hEpolyActual] at hq
    apply (mul_self_inj_of_nonneg dist_nonneg dist_nonneg).mp
    nlinarith only [hq]
  have hFdist : dist F circleCenter = dist B circleCenter := by
    have hq := hpolydist F
    rw [hFpolyActual] at hq
    apply (mul_self_inj_of_nonneg dist_nonneg dist_nonneg).mp
    nlinarith only [hq]
  have hBE : B ≠ E := by
    intro he
    have hv : yb = o.areaForm n (E -ᵥ M) / d :=
      congrArg (fun q : Pt => o.areaForm n (q -ᵥ M) / d) he
    rw [hyb, hEcoordinates.2] at hv
    have hs : (-1 : ℝ) = -Ω.radius / Γ.radius := by
      apply mul_right_cancel₀ hy_nonzero
      simpa only [neg_one_mul] using hv
    have hr := (eq_div_iff hRne).mp hs
    have heq : Ω.radius = Γ.radius := by nlinarith only [hr]
    exact (ne_of_lt Ω_radius_lt_Γ_radius) heq
  have hBF : B ≠ F := by
    intro he
    have hv : yb = o.areaForm n (F -ᵥ M) / d :=
      congrArg (fun q : Pt => o.areaForm n (q -ᵥ M) / d) he
    rw [hyb, hFcoordinates.2] at hv
    have hs : (-1 : ℝ) = -Γ.radius / Ω.radius := by
      apply mul_right_cancel₀ hy_nonzero
      simpa only [neg_one_mul] using hv
    have hr := (eq_div_iff hrne).mp hs
    have heq : Ω.radius = Γ.radius := by nlinarith only [hr]
    exact (ne_of_lt Ω_radius_lt_Γ_radius) heq
  have hEF : E ≠ F := by
    intro he
    have hv : o.areaForm n (E -ᵥ M) / d = o.areaForm n (F -ᵥ M) / d :=
      congrArg (fun q : Pt => o.areaForm n (q -ᵥ M) / d) he
    rw [hEcoordinates.2, hFcoordinates.2] at hv
    have hs : -Ω.radius / Γ.radius = -Γ.radius / Ω.radius := by
      apply mul_right_cancel₀ hy_nonzero
      exact hv
    field_simp [hRne, hrne] at hs
    have hprod : 0 < (Γ.radius - Ω.radius) * (Γ.radius + Ω.radius) :=
      mul_pos (sub_pos.mpr Ω_radius_lt_Γ_radius) (by linarith only [hΓpos, hΩpos])
    nlinarith only [hs, hprod]
  have hcospherical : Cospherical ({B, E, F} : Set Pt) := by
    refine ⟨circleCenter, dist B circleCenter, ?_⟩
    intro q hq
    simp only [Set.mem_insert_iff, Set.mem_singleton_iff] at hq
    rcases hq with rfl | rfl | rfl
    · rfl
    · exact hEdist
    · exact hFdist
  have hBEF : AffineIndependent ℝ ![B, E, F] :=
    hcospherical.affineIndependent_of_ne hBE hBF hEF

  let T : Pt := (N -ᵥ A) +ᵥ M
  suffices h :
      ∃ affineIndependent_BEF : AffineIndependent ℝ ![B, E, F],
        (⟨_, affineIndependent_BEF⟩ : Triangle ℝ Pt).circumsphere.IsTangentAt T
          (AffineSubspace.mk' H line[ℝ, A, P].direction) by
    rcases h with ⟨hBEF, hT⟩
    exact ⟨hBEF, hT.isTangent⟩
  refine ⟨hBEF, ?_⟩
  trace_state

end Imo2025P2
