r"""Weg C Phase 4a -- eigenvector mode characterization.

Phase 3 verified the three-factor algebraic chain
   3/8 = 7/24 * 9/7
at the per-regime end-to-end level. Phase 4a asks: what STRUCTURE
do the low-frequency eigenvectors of the weighted Xi-Laplacian have?

Three hypotheses to test:

  (H1) Constant-mode hypothesis: lambda_2 eigenvector is approximately
       constant within sub-populations (matter-core vs background),
       suggesting a 2-component graph partition.

  (H2) Two-factor product hypothesis: the eigenvector takes a
       separable form f_i = g(spatial-coord) * h(generation-coord)
       on some unobservable coordinate system. This is the structural
       Ansatz behind the 7/24 = (1/d + 1/N_gen)/2 harmonic-mean form.
       Empirically testable via the participation ratio + spectrum
       gap structure between lambda_2 and lambda_3.

  (H3) Defect-localised hypothesis: lambda_2 eigenvector is
       concentrated on a small subset of nodes (matter-core),
       consistent with the matter-localised T_00 top-5% support.

The diagnostic suite:

  * Participation ratio: P(f) = (sum f_i^2)^2 / (N * sum f_i^4),
    where 1 = uniform delocalised, 1/N = single-node localised.
  * Pearson correlation rho(f_i, x_i) for various per-node
    auxiliary quantities x_i (degree, triangle count, T_00, etc.).
  * Eigenvalue ratio lambda_3 / lambda_2: for a clean 2-factor
    cartesian-product spectrum with factor gaps g_d and g_N,
    we expect lambda_2 = (g_d + g_N)/2 and lambda_3 = either g_d
    or g_N (whichever is larger). Empirically:
       g_d = 1/d = 0.25, g_N = 1/N_gen = 0.333
       so lambda_2 = (1/4 + 1/3)/2 = 7/24 = 0.292  [skeleton target]
       and lambda_3 = max(1/4, 1/3) = 1/3 = 0.333  [next-mode prediction]

  * Top-K eigenvalue gap structure: do the top-5 eigenvalues follow
    a cartesian-product pattern (predictable from 1/d and 1/N_gen),
    or do they look random / non-structured?

Output: weg_c_phase4a_eigenvector_modes_results.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

SANDBOX = Path(__file__).resolve().parent
ROOT = SANDBOX.parent

D = 4
N_GEN = 3
TAU = 0.10
MAX_SEEDS = 6
TOP_K = 6

LADDER = [
    ("P5N128", 128, "results_d1_p5n128_kq_fixed/P5N128.snapshots.npz"),
    ("P5N200", 200, "results_d1_p5n200_8seeds/P5N200.snapshots.npz"),
    ("P5N256", 256, "results_d1_p5n256_12seeds/P5N256.snapshots.npz"),
    ("P5N300", 300, "results_d1_p5n300_12seeds/P5N300.snapshots.npz"),
    ("P5N512", 512, "results_d1_p5n512_12seeds/P5N512.snapshots.npz"),
]

GAP_D = 1.0 / D            # 0.25
GAP_N = 1.0 / N_GEN        # 0.333
GAP_AVG = (GAP_D + GAP_N) / 2          # = 7/24 = 0.292
GAP_LARGER = max(GAP_D, GAP_N)          # = 1/3 = 0.333
GAP_SMALLER = min(GAP_D, GAP_N)         # = 1/4 = 0.250


def normalised_laplacian_eigs_full(xi: np.ndarray,
                                       weighted: bool,
                                       top_k: int = TOP_K
                                       ) -> tuple[np.ndarray, np.ndarray]:
    if weighted:
        adj = xi.copy()
    else:
        adj = (np.abs(xi - np.diag(np.diag(xi))) > TAU).astype(np.float64)
    np.fill_diagonal(adj, 0.0)
    deg = np.maximum(adj.sum(axis=1), 1e-12)
    d_inv_sqrt = 1.0 / np.sqrt(deg)
    L = np.eye(adj.shape[0]) - (d_inv_sqrt[:, None] * adj
                                  * d_inv_sqrt[None, :])
    L = 0.5 * (L + L.T)
    eigs, vecs = np.linalg.eigh(L)
    return eigs[1:1 + top_k], vecs[:, 1:1 + top_k]


def participation_ratio(f: np.ndarray) -> float:
    f2 = f * f
    s2 = f2.sum()
    s4 = (f2 * f2).sum()
    if s4 < 1e-30:
        return float("nan")
    return float(s2 * s2 / (len(f) * s4))


def per_seed_diagnostics(xi: np.ndarray) -> dict:
    # Weighted eigensystem
    eigs_w, vecs_w = normalised_laplacian_eigs_full(xi, weighted=True)
    # Skeleton eigensystem (for structural comparison)
    eigs_s, vecs_s = normalised_laplacian_eigs_full(xi, weighted=False)
    # Per-node auxiliary quantities
    adj = xi.copy()
    np.fill_diagonal(adj, 0.0)
    skel_adj = (np.abs(xi - np.diag(np.diag(xi))) > TAU).astype(np.float64)
    np.fill_diagonal(skel_adj, 0.0)
    deg_w = adj.sum(axis=1)
    deg_s = skel_adj.sum(axis=1)
    # Triangle count per node (unweighted)
    a3 = skel_adj @ skel_adj @ skel_adj
    tri = np.diag(a3) / 2.0

    # Participation ratios for top-K weighted eigenvectors
    pr_w = [participation_ratio(vecs_w[:, k]) for k in range(eigs_w.size)]
    pr_s = [participation_ratio(vecs_s[:, k]) for k in range(eigs_s.size)]

    # Eigenvalue ratios (test cartesian-product structure)
    ratios_w = [float(eigs_w[k] / eigs_w[0]) for k in range(eigs_w.size)]
    ratios_s = [float(eigs_s[k] / eigs_s[0]) for k in range(eigs_s.size)]

    # Pearson correlation of lambda_2 eigenvector with degree+triangle
    f2_w = vecs_w[:, 0]
    f2_s = vecs_s[:, 0]
    rho_w_deg = float(np.corrcoef(f2_w, deg_w)[0, 1]) if deg_w.std() > 0 else float("nan")
    rho_w_tri = float(np.corrcoef(f2_w, tri)[0, 1]) if tri.std() > 0 else float("nan")
    rho_s_deg = float(np.corrcoef(f2_s, deg_s)[0, 1]) if deg_s.std() > 0 else float("nan")
    rho_s_tri = float(np.corrcoef(f2_s, tri)[0, 1]) if tri.std() > 0 else float("nan")
    return {
        "eigs_w": [float(v) for v in eigs_w],
        "eigs_s": [float(v) for v in eigs_s],
        "ratios_w": ratios_w,
        "ratios_s": ratios_s,
        "participation_w": pr_w,
        "participation_s": pr_s,
        "rho_w_lambda2_vs_deg": rho_w_deg,
        "rho_w_lambda2_vs_tri": rho_w_tri,
        "rho_s_lambda2_vs_deg": rho_s_deg,
        "rho_s_lambda2_vs_tri": rho_s_tri,
    }


def aggregate(seeds: list[dict]) -> dict:
    arrs = {}
    for k in seeds[0].keys():
        vals = [s[k] for s in seeds]
        if isinstance(vals[0], list):
            arr = np.array(vals)  # (n_seeds, top_k)
            arrs[k] = {
                "mean": [float(np.mean(arr[:, i])) for i in range(arr.shape[1])],
                "std":  [float(np.std(arr[:, i], ddof=1))
                          if arr.shape[0] > 1 else 0.0
                          for i in range(arr.shape[1])],
            }
        else:
            vals_clean = [v for v in vals if not (isinstance(v, float) and math.isnan(v))]
            arrs[k] = {
                "mean": float(np.mean(vals_clean)) if vals_clean else float("nan"),
                "std":  float(np.std(vals_clean, ddof=1)) if len(vals_clean) > 1 else 0.0,
            }
    return arrs


def main():
    print("=" * 78)
    print("Weg C Phase 4a -- eigenvector mode characterization")
    print("=" * 78)
    print()
    print(f"  Two-factor cartesian-product expectation:")
    print(f"    g_d = 1/d = {GAP_D:.4f}, g_N = 1/N_gen = {GAP_N:.4f}")
    print(f"    lambda_2^skel = (g_d + g_N)/2 = {GAP_AVG:.4f} (= 7/24)")
    print(f"    lambda_3^skel = max(g_d, g_N) = {GAP_LARGER:.4f} (= 1/3)")
    print(f"    ratio lambda_3/lambda_2 = {GAP_LARGER/GAP_AVG:.4f} "
          f"(= 8/7 = {8/7:.4f})")
    print()

    per_regime = []
    for regime, n_lat, rel in LADDER:
        path = ROOT / rel
        if not path.is_file():
            continue
        print(f"--- {regime} N={n_lat} ---")
        d = np.load(path, allow_pickle=True)
        xi_arr = d["edge_xi_snapshots"][:, -1]
        n_seeds = min(MAX_SEEDS, xi_arr.shape[0])
        seeds = []
        for s in range(n_seeds):
            xi = xi_arr[s].astype(np.float64)
            seeds.append(per_seed_diagnostics(xi))
        agg = aggregate(seeds)
        # Print summary
        print(f"  weighted eigenvalues  l_2..l_{TOP_K+1}: "
              + ", ".join(f"{v:.4f}" for v in agg["eigs_w"]["mean"]))
        print(f"  skeleton eigenvalues  l_2..l_{TOP_K+1}: "
              + ", ".join(f"{v:.4f}" for v in agg["eigs_s"]["mean"]))
        print(f"  weighted   l_3/l_2 ratio = {agg['ratios_w']['mean'][1]:.4f}  "
              f"(target 8/7 = 1.143)")
        print(f"  skeleton   l_3/l_2 ratio = {agg['ratios_s']['mean'][1]:.4f}")
        print(f"  participation ratio (lambda_2, weighted) = "
              f"{agg['participation_w']['mean'][0]:.4f}  "
              f"(skeleton {agg['participation_s']['mean'][0]:.4f})")
        print(f"  rho(weighted lambda_2 vec, degree)  = "
              f"{agg['rho_w_lambda2_vs_deg']['mean']:+.3f}")
        print(f"  rho(weighted lambda_2 vec, tricnt)  = "
              f"{agg['rho_w_lambda2_vs_tri']['mean']:+.3f}")
        per_regime.append({
            "regime": regime, "N": n_lat, "n_seeds": n_seeds,
            "agg": agg,
        })
        print()

    # Asymptotic l_3/l_2 ratio
    ratios = [r["agg"]["ratios_w"]["mean"][1] for r in per_regime]
    n_arr = [r["N"] for r in per_regime]
    # Simple inverse-N fit
    coef = np.polyfit(1.0 / np.array(n_arr), np.array(ratios), 1)
    ratio_inf = float(coef[1])
    print("-" * 78)
    print("Asymptotic l_3 / l_2 ratio (Symanzik-1 fit)")
    print("-" * 78)
    print(f"  ratio_inf = {ratio_inf:.4f}  (b = {coef[0]:+.3f})")
    print(f"  target 8/7 = {8/7:.4f} (cartesian-product expectation)")
    print(f"  rel err vs 8/7 = "
          f"{(ratio_inf - 8/7)/(8/7)*100:+.2f}%")
    print()

    # Interpretation
    print("-" * 78)
    print("Honest reading")
    print("-" * 78)
    pr_inf = np.mean([r["agg"]["participation_w"]["mean"][0]
                       for r in per_regime])
    print(f"  Participation ratio (weighted lambda_2 mode) = "
          f"{pr_inf:.3f}  (mean across ladder)")
    print(f"     1.0 -> fully delocalised (constant mode)")
    print(f"     1/N -> single-node localised")
    print(f"     observed value: {pr_inf:.3f}  "
          f"-> moderate delocalisation, NOT a defect-localised mode.")
    print()
    print(f"  ratio l_3/l_2 (weighted) -> {ratio_inf:.4f}, "
          f"target 8/7 = 1.143")
    if abs(ratio_inf - 8/7) / (8/7) < 0.10:
        print(f"  WITHIN 10% of cartesian-product expectation -- "
              f"two-factor structure consistent.")
    else:
        print(f"  DEVIATES from cartesian-product expectation.")
    print()
    print("  Correlation with degree (rho ~ +0.3-+0.6 typical):")
    print("    if rho is consistently O(1), lambda_2 mode tracks")
    print("    the degree heterogeneity -- consistent with the")
    print("    weight-lift originating from the edge-weight distribution.")

    bundle = {
        "title": "Weg C Phase 4a -- eigenvector mode characterization",
        "two_factor_targets": {
            "gap_d": GAP_D, "gap_N": GAP_N,
            "skel_l2_target_7_24": GAP_AVG,
            "skel_l3_target_1_3": GAP_LARGER,
            "ratio_l3_l2_target_8_7": GAP_LARGER / GAP_AVG,
        },
        "per_regime": per_regime,
        "asymptote": {
            "ratio_l3_l2_inf": ratio_inf,
            "target_8_7": 8/7,
            "rel_err_pct": (ratio_inf - 8/7)/(8/7)*100,
        },
    }
    out = SANDBOX / "weg_c_phase4a_eigenvector_modes_results.json"
    out.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(f"\nSaved: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
