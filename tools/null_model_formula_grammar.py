r"""Formula-grammar null-model test (corpus-wide look-elsewhere).

Implements the explicit null-model evaluation requested by external
peer-review criticism (cf. critique point 7 of the 2026-05-16
external review): rather than relying on a Bonferroni correction
over the ~28 top-tier closures, this script estimates the
look-elsewhere significance by enumerating the formula grammar
that the corpus actually uses, sampling random formulas from it,
and counting how often a randomly-sampled formula lands within
the EXACT band (|r| <= 1%) of a randomly-permuted observable target.

The empirical false-discovery rate p_random = N_hits / N_trials is
the relevant null model. The corpus is then said to over- or
under-perform this null: if N_corpus_hits / N_corpus_attempts >>
p_random, the corpus exceeds chance; if comparable, the corpus is
not better than chance.

Grammar of allowed formulas (corpus-derived):

  PRIMITIVES:  gamma=1/10, alpha_xi=9/10, eps_sync_sq=1/20,
               beta_pi=15/16, D_Omega=67/80, d=4, N_gen=3,
               2d+1=9, d+N_gen=7, d-1=3, N_gen+1=4, ...
  BINARY OPS:  +, -, *, /, **  (exponent in {1, 2, 3, -1, -2, 1/2})
  SMALL RATIONAL FACTORS:  1/2, 1/3, 1/4, 1/6, 1/8, ..., 2, 3, 4, ...
  COMPOSITION DEPTH:  up to 3 nested operations
  POSITIVITY FILTER:  only formulas with positive numeric value

The TARGETS are pulled from the corpus closure_index.json plus
PDG/Planck/DESI external anchors for the top-tier closures.

For each TRIAL:
  1. Pick a random observable target (real numeric value) from the
     anchor list.
  2. Generate a random formula from the grammar.
  3. Compute the relative residual |formula - target|/|target|.
  4. Count as HIT if |r| <= 0.01 (the EXACT band).

The corpus-baseline comparison:
  - corpus_hits = closures registered with status `consistent` and
    `mechanism_derived` or `mechanism_motivated` in closure_index;
  - corpus_attempts = total closures.

Output: null_model_formula_grammar_results.json
"""
from __future__ import annotations

import json
import math
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / (
    "null_model_formula_grammar_results.json")

# ---------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------
PRIMITIVES = [
    ("gamma", Fraction(1, 10)),
    ("alpha_xi", Fraction(9, 10)),
    ("eps_sync_sq", Fraction(1, 20)),
    ("beta_pi", Fraction(15, 16)),
    ("D_Omega", Fraction(67, 80)),
    ("s_face", Fraction(1, 4)),
    ("d", Fraction(4, 1)),
    ("N_gen", Fraction(3, 1)),
    ("2d+1", Fraction(9, 1)),
    ("2d-1", Fraction(7, 1)),
    ("d+N_gen", Fraction(7, 1)),
    ("d-1", Fraction(3, 1)),
    ("N_gen+1", Fraction(4, 1)),
    ("2d+N_gen", Fraction(11, 1)),
    ("d*N_gen", Fraction(12, 1)),
]

SMALL_RATIONALS = [Fraction(1, k) for k in (2, 3, 4, 5, 6, 8, 10, 16, 20)] \
    + [Fraction(k, 1) for k in (2, 3, 4, 5, 6, 8, 10)]

OPS = ["+", "-", "*", "/"]
EXPONENTS = [Fraction(1, 1), Fraction(2, 1), Fraction(3, 1),
              Fraction(-1, 1), Fraction(-2, 1), Fraction(1, 2)]


def _safe_pow(base: Fraction, exp: Fraction) -> Fraction | None:
    """Return base ** exp as a Fraction if exact, else None."""
    if base <= 0 and exp.denominator != 1:
        return None
    if exp.denominator == 1:
        n = int(exp)
        if n >= 0:
            return base ** n
        if base == 0:
            return None
        return Fraction(base.denominator, base.numerator) ** (-n)
    # Non-integer exponent: only allow sqrt of perfect squares.
    if exp == Fraction(1, 2):
        n2 = base.numerator
        d2 = base.denominator
        sn = math.isqrt(n2)
        sd = math.isqrt(d2)
        if sn * sn == n2 and sd * sd == d2:
            return Fraction(sn, sd)
        return None
    return None


def _safe_div(a: Fraction, b: Fraction) -> Fraction | None:
    if b == 0:
        return None
    return a / b


def sample_formula(rng: random.Random, max_depth: int = 3
                     ) -> tuple[Fraction | None, int]:
    """Return (value, depth_used)."""
    if max_depth == 0 or rng.random() < 0.3:
        choice = rng.choice([0, 1])
        if choice == 0:
            return rng.choice(PRIMITIVES)[1], 1
        return rng.choice(SMALL_RATIONALS), 1
    a, da = sample_formula(rng, max_depth - 1)
    if a is None:
        return None, da
    op = rng.choice(OPS + ["pow"])
    if op == "pow":
        e = rng.choice(EXPONENTS)
        return _safe_pow(a, e), da + 1
    b, db = sample_formula(rng, max_depth - 1)
    if b is None:
        return None, da + db
    if op == "+":
        return a + b, da + db + 1
    if op == "-":
        return a - b, da + db + 1
    if op == "*":
        return a * b, da + db + 1
    if op == "/":
        return _safe_div(a, b), da + db + 1
    return None, da + db


# ---------------------------------------------------------------
# Targets: real-valued external anchors from the top-tier closures
# (PDG / Planck / DESI / NuFIT 2024-2026). Values selected to span
# magnitudes from ~1e-10 to ~1e3.
# ---------------------------------------------------------------
TARGETS = [
    ("alpha_EM_inv", 137.036),
    ("alpha_s_MZ", 0.118),
    ("sin2_theta_W", 0.23129),
    ("V_us", 0.2243),
    ("V_cb", 0.0411),
    ("V_ub", 0.00382),
    ("m_e_MeV", 0.5109989),
    ("m_mu_MeV", 105.6583755),
    ("m_tau_MeV", 1776.86),
    ("m_top_GeV", 172.69),
    ("m_b_GeV", 4.183),
    ("m_c_GeV", 1.273),
    ("m_u_MeV", 2.16),
    ("m_d_MeV", 4.67),
    ("v_EW_GeV", 246.2186),
    ("Sigma_m_nu_eV", 0.0593),
    ("Y_p", 0.245),
    ("Omega_b_h2", 0.02237),
    ("Omega_DM_h2", 0.12),
    ("Omega_Lambda", 0.6889),
    ("Omega_m", 0.3111),
    ("h_dimensionless", 0.675),
    ("n_s", 0.9649),
    ("sigma_8", 0.811),
    ("S_8", 0.832),
    ("eta_B", 6e-10),
    ("S_BH_over_A", 0.25),
    ("J_CP", 2.28e-5),
    ("a_mu_anomaly", 1.16591e-3),
    ("delta_CP_rad", 1.13),
]

EXACT_BAND = 0.01     # |r| <= 1%
PRECISE_BAND = 0.025  # |r| <= 2.5%
N_TRIALS_DEFAULT = 200_000
RANDOM_SEED = 20260516


def run(n_trials: int, max_depth: int = 3) -> dict:
    rng = random.Random(RANDOM_SEED)
    hits_exact = 0
    hits_precise = 0
    n_valid = 0
    per_target_hits: dict[str, int] = {name: 0 for name, _ in TARGETS}
    t0 = time.time()
    for _ in range(n_trials):
        val, _ = sample_formula(rng, max_depth)
        if val is None or val <= 0:
            continue
        target_name, target_value = rng.choice(TARGETS)
        if target_value == 0:
            continue
        # Match magnitude windows: a 5-smooth random rational that
        # accidentally lands within 1% of a PDG measurement is what
        # we are counting. We do NOT pre-filter by magnitude --- a
        # random formula has to itself end up in the target's order
        # of magnitude.
        ratio = float(val) / float(target_value)
        if ratio < 0:
            continue
        rel = abs(float(val) - target_value) / abs(target_value)
        n_valid += 1
        if rel <= EXACT_BAND:
            hits_exact += 1
            per_target_hits[target_name] += 1
        if rel <= PRECISE_BAND:
            hits_precise += 1
    elapsed = time.time() - t0

    p_random_exact = hits_exact / n_valid if n_valid else float("nan")
    p_random_precise = hits_precise / n_valid if n_valid else float("nan")

    print(f"  Trials:           {n_trials:,}")
    print(f"  Valid samples:    {n_valid:,}")
    print(f"  EXACT hits ({EXACT_BAND*100:.1f}%):    "
          f"{hits_exact:,}  (p_random = {p_random_exact:.4e})")
    print(f"  PRECISE hits ({PRECISE_BAND*100:.1f}%):  "
          f"{hits_precise:,}  (p_random = {p_random_precise:.4e})")
    print(f"  Elapsed:           {elapsed:.1f}s")
    return {
        "n_trials": n_trials,
        "n_valid_samples": n_valid,
        "n_hits_exact": hits_exact,
        "n_hits_precise": hits_precise,
        "p_random_exact": p_random_exact,
        "p_random_precise": p_random_precise,
        "per_target_hits": per_target_hits,
        "elapsed_seconds": elapsed,
    }


def corpus_comparison(p_random_exact: float,
                         p_random_precise: float) -> dict:
    """Compare against corpus closure_index.json EXACT-tier rate."""
    idx_path = (Path(__file__).resolve().parent
                / "closure_index.json")
    if not idx_path.is_file():
        return {"available": False}
    data = json.loads(idx_path.read_text(encoding="utf-8"))
    closures = data.get("closures", [])
    if not closures:
        return {"available": False}
    n_total = len(closures)
    n_consistent = sum(1 for c in closures
                          if c.get("status") == "consistent")
    # Count those whose tier is EXACT-band.
    n_exact = sum(1 for c in closures
                     if (c.get("tier", "") or "").lower() == "exact")
    p_corpus_exact = n_exact / n_total if n_total else float("nan")
    p_corpus_consistent = n_consistent / n_total if n_total else float("nan")
    enrichment_exact = (p_corpus_exact / p_random_exact
                          if p_random_exact > 0 else float("nan"))
    return {
        "available": True,
        "n_closures_total": n_total,
        "n_consistent": n_consistent,
        "n_exact": n_exact,
        "p_corpus_exact": p_corpus_exact,
        "p_corpus_consistent": p_corpus_consistent,
        "p_random_exact": p_random_exact,
        "p_random_precise": p_random_precise,
        "exact_enrichment_factor": enrichment_exact,
    }


def main():
    n_trials = N_TRIALS_DEFAULT
    if len(sys.argv) > 1:
        try:
            n_trials = int(sys.argv[1])
        except ValueError:
            pass
    print("=" * 78)
    print("Corpus-wide formula-grammar null model")
    print("=" * 78)
    print(f"  primitives:     {len(PRIMITIVES)}")
    print(f"  small rationals:{len(SMALL_RATIONALS)}")
    print(f"  ops:            {OPS} + pow ({len(EXPONENTS)} exps)")
    print(f"  max depth:      3")
    print(f"  targets:        {len(TARGETS)}")
    print(f"  EXACT band:     |r| <= {EXACT_BAND*100:.2f}%")
    print(f"  PRECISE band:   |r| <= {PRECISE_BAND*100:.2f}%")
    print()
    null = run(n_trials)
    print()
    print("-" * 78)
    print("Corpus comparison")
    print("-" * 78)
    comp = corpus_comparison(null["p_random_exact"],
                                null["p_random_precise"])
    if comp["available"]:
        print(f"  Corpus closures (closure_index.json):   "
              f"{comp['n_closures_total']}")
        print(f"  Of which EXACT-tier:                    "
              f"{comp['n_exact']}  "
              f"(p_corpus = {comp['p_corpus_exact']:.4e})")
        print(f"  Random null EXACT rate:                  "
              f"p_random = {comp['p_random_exact']:.4e}")
        ef = comp['exact_enrichment_factor']
        print(f"  Enrichment (corpus / random) EXACT:      "
              f"{ef:.1f}x" if not math.isnan(ef) else
              f"  Enrichment: nan")
    else:
        print("  closure_index.json not found.")
    bundle = {
        "title": "Corpus-wide formula-grammar null model",
        "grammar": {
            "n_primitives": len(PRIMITIVES),
            "n_small_rationals": len(SMALL_RATIONALS),
            "ops": OPS + ["pow"],
            "n_exponents": len(EXPONENTS),
            "max_depth": 3,
        },
        "targets": [{"name": n, "value": v} for n, v in TARGETS],
        "exact_band": EXACT_BAND,
        "precise_band": PRECISE_BAND,
        "null": null,
        "corpus_comparison": comp,
    }
    OUT.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
    print(f"\nSaved: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
