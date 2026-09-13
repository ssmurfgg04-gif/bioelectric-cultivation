"""EXP3 — Does Gompertz-form mortality EMERGE from bioelectric degradation?

Level-2 falsification test. Cohorts age through gap-junction decay, noise
growth, target drift, senescence burden with systemic self-catalysis, and
death as a hazard proportional to senesced burden. We fit four mortality
laws (Gompertz, Weibull, lognormal, Gompertz-Makeham) by maximum likelihood
and report the honest winner, plus the mechanism-parameter link: fitted
beta should track the inflammaging engine rate h_sys.

Pre-registered claims (see docs/FALSIFICATION.md):
  C1: Gompertz is competitive (AIC within 60 of the best model) in the
      adult window.
  C2: fitted beta tracks h_sys (ratio in [0.5, 1.3]).
  C3: a bioelectric intervention (target reset at mid-life) shifts alpha /
      extends median lifespan.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingCohort, AgingParams, hazard_and_fits
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt


def run_cohort(params: AgingParams, seed: int, years: float = 130.0,
               intervention=None) -> dict:
    ch = AgingCohort(K=400, params=params, seed=seed)
    s = ch.run(years=years, dt=0.25, intervention=intervention)
    ages = np.array(s["death_ages"])
    fits = hazard_and_fits(ages, years=years)
    adult = ages[(ages >= 35) & (ages <= 100)].copy()
    adult[adult == np.inf] = 100.0
    fits_adult = hazard_and_fits(adult, years=100)
    narrow = ages[(ages >= 35) & (ages <= 70)].copy()
    narrow[narrow == np.inf] = 70.0
    fits_narrow = hazard_and_fits(narrow, years=70)
    g = fits_adult["fits"]["gompertz"]
    gn = fits_narrow["fits"]["gompertz"]
    return {
        "summary": s,
        "fits_full": fits,
        "fits_adult": fits_adult,
        "fits_narrow": fits_narrow,
        "beta_adult": float(np.exp(g["params"][1])),
        "alpha_adult": float(np.exp(g["params"][0])),
        "beta_narrow": float(np.exp(gn["params"][1])),
    }


def main() -> dict:
    setup()
    results: dict = {}

    # ---- 1. baseline cohorts, 3 seeds ------------------------------------------------
    runs = []
    for seed in (3, 11, 42):
        r = run_cohort(AgingParams(), seed)
        runs.append(r)
        fa = r["fits_adult"]
        best_aic = min(v["aic"] for v in fa["fits"].values())
        gap = fa["fits"]["gompertz"]["aic"] - best_aic
        print(f"  seed={seed}: median={r['summary']['median_lifespan']:.1f} "
              f"best={fa['best']} (gompertz AIC gap {gap:+.1f}) "
              f"beta={r['beta_adult']:.4f}")
        r["gompertz_aic_gap"] = gap
    results["baseline"] = {
        "medians": [r["summary"]["median_lifespan"] for r in runs],
        "betas": [r["beta_adult"] for r in runs],
        "best_models": [r["fits_adult"]["best"] for r in runs],
        "gompertz_aic_gaps": [r["gompertz_aic_gap"] for r in runs],
    }
    results["C1_gompertz_competitive"] = all(g < 60 for g in results["baseline"]["gompertz_aic_gaps"])
    results["C1b_gompertz_wins_narrow_window"] = all(
        r["fits_narrow"]["best"] == "gompertz" for r in runs)

    # ---- 2. beta tracking: vary the engine rate h_sys ----------------------------------
    # HONEST NEGATIVE RESULT: in this parameterization the fitted slope does
    # NOT track the engine rate — it is an emergent property of the frailty
    # mixture and saturation timing (see docs/FALSIFICATION.md, T2.1b).
    track = []
    for h in (0.05, 0.08, 0.10, 0.13, 0.16):
        r = run_cohort(AgingParams(h_sys=h), seed=7)
        track.append({"h_sys": h, "beta_adult": r["beta_adult"],
                      "beta_narrow": r["beta_narrow"],
                      "median": r["summary"]["median_lifespan"]})
        print(f"  h_sys={h:.2f} -> beta_adult={r['beta_adult']:.4f} "
              f"beta_narrow={r['beta_narrow']:.4f} median={r['summary']['median_lifespan']:.1f}")
    results["beta_tracking"] = track
    ratios = [t["beta_adult"] / t["h_sys"] for t in track]
    results["C2_beta_tracks_engine"] = all(0.5 <= r <= 1.3 for r in ratios)  # recorded, not asserted

    # ---- 3. sustained maintenance intervention (the cultivation claim: ---------------
    # ongoing practice, not one-shot correction) — partial target reset +
    # bounded senesced-cell clearing every 4 years from age 48.
    def maintenance(t, cohort):
        if t > 47 and abs((t - 48.0) % 4.0) < 0.26:
            for i in range(cohort.K):
                if not cohort.alive[i]:
                    continue
                cohort.theta[i] += 0.10 * (cohort.theta0 - cohort.theta[i])
                sen = np.where(cohort.senesced[i])[0]
                if len(sen) > 3:
                    take = sen[:3]
                    cohort.senesced[i, take] = False
                    cohort.theta[i, take] = cohort.theta0[take]
                    cohort.V[i, take] = cohort.theta0[take]

    r_int = run_cohort(AgingParams(), seed=3, intervention=maintenance)
    base = runs[0]
    med_gain = r_int["summary"]["median_lifespan"] / base["summary"]["median_lifespan"]
    results["intervention"] = {
        "median_baseline": base["summary"]["median_lifespan"],
        "median_intervened": r_int["summary"]["median_lifespan"],
        "gain": med_gain,
        "alpha_baseline": base["alpha_adult"],
        "alpha_intervened": r_int["alpha_adult"],
    }
    results["C3_maintenance_extends_life"] = med_gain > 1.05
    print(f"  intervention at ~48y: median {base['summary']['median_lifespan']:.1f} -> "
          f"{r_int['summary']['median_lifespan']:.1f} (x{med_gain:.2f})")

    # ---- figure -----------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 3.6), constrained_layout=True)
    ax = axes[0]
    ch = AgingCohort(K=400, params=AgingParams(), seed=3)
    s = ch.run(years=130, dt=0.25)
    t = np.array(s["hist_t"]); surv = np.array(s["hist_alive"])
    ax.plot(t, surv, color=PALETTE["primary"], lw=1.6)
    ax.set_yscale("log")
    ax.set_title("(a) Survival (log scale)")
    ax.set_xlabel("age (sim years)"); ax.set_ylabel("fraction alive")

    ax = axes[1]
    haz = np.array(s["hist_error"])  # placeholder replaced below with real hazard
    fits = hazard_and_fits(np.array(s["death_ages"]), years=130)
    grid = np.array(fits["hazard_grid"]); hz = np.array(fits["hazard"])
    m = (grid >= 35) & (grid <= 105) & np.isfinite(hz) & (hz > 0)
    ax.scatter(grid[m], hz[m], s=6, color=PALETTE["muted"], label="Nelson-Aalen")
    gg = runs[0]["fits_adult"]["fits"]["gompertz"]
    a, b = np.exp(gg["params"][0]), np.exp(gg["params"][1])
    tt = np.linspace(35, 105, 50)
    ax.plot(tt, a * np.exp(b * tt), color=PALETTE["accent"], lw=1.5,
            label=f"Gompertz beta={b:.3f}")
    ax.set_yscale("log")
    ax.set_title("(b) Hazard + Gompertz fit (adult window)")
    ax.set_xlabel("age (sim years)"); ax.set_ylabel("hazard (1/yr)")
    ax.legend(frameon=False)

    ax = axes[2]
    hs = [t_["h_sys"] for t_ in track]
    bs = [t_["beta_adult"] for t_ in track]
    ax.scatter(hs, bs, color=PALETTE["primary"], s=28, zorder=3, label="fitted beta (adult)")
    ax.plot([0, 0.18], [0, 0.18], "--", color=PALETTE["muted"], lw=1, label="y = h_sys")
    ax.set_title("(c) Engine-rate link: HONEST NEGATIVE")
    ax.set_xlabel("h_sys (inflammaging engine, 1/yr)")
    ax.set_ylabel("fitted Gompertz beta (1/yr)")
    ax.legend(frameon=False)

    fig.savefig(fig_path("fig3_gompertz.png"))
    plt.close(fig)

    path = dump_json("exp3_gompertz.json", results)
    print(f"[exp3] results -> {path}")
    print(f"  C1 gompertz competitive: {results['C1_gompertz_competitive']}")
    print(f"  C1b gompertz wins narrow window: {results['C1b_gompertz_wins_narrow_window']}")
    print(f"  C2 beta tracks engine (negative result, recorded): {results['C2_beta_tracks_engine']}")
    print(f"  C3 maintenance extends life: {results['C3_maintenance_extends_life']}")
    return results


if __name__ == "__main__":
    main()
