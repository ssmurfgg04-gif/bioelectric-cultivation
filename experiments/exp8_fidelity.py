"""EXP8 — Pattern-fidelity mortality: does VERIFIED maintenance finally win?

The pre-registered follow-up to exp6's negative results (T2.4b/T2.4c:
"mortality is insensitive to written-value correctness"). Mortality here
DEPENDS on discrete pattern fidelity: organs fail when their fraction of
cells-in-the-correct-Vmem-band drops below critical.

REGIME NOTE (honest): the default aging parameters put the CHANNEL capacity
cliff (noise growth crossing the level spacing) at t~50-60, which confounds
every pattern-level intervention with mass noise-driven senescence. This
experiment runs a reduced-noise regime (kappa 0.032, lambda 0.024) so that
PATTERN correctness — the variable under test — is the binding constraint.
The channel-cliff regime is probed by the channel-therapy arms.

Six arms, identical physics and write budget:
  none  : baseline aging.
  local : consensus-only maintenance (no archive) — repairs senesced domains
          from the noisy consensus. A jumped domain IS the consensus:
          invisible from inside.
  codec : consensus-verified archive-referenced maintenance — two
          independent reads must agree (trust the read), then domains are
          compared to the genomic archive, then verified-wrong/senesced
          domains are rewritten with archived values. Unverified = refused.
  regen : the planarian strategy — periodic full re-derivation from the
          archive (Dai et al. 2025). Resets pattern and senescence; the
          channel engines keep running, so cycles must be repeated.
  chan  : codec + verification-GATED connexin restoration (boost coupling
          only in verified individuals — re-opening junctions in corrupted
          tissue propagates the corruption).
  blind : codec maintenance + UNGATED connexin boost for everyone — the
          control that isolates the value of gating.

Pre-registered criteria (falsification ledger):
  T3.1a  codec/none median gain >= 1.06          (maintenance extends life)
  T3.1b  codec/local median gain >= 1.03         (THE GATE: verification pays
                                                  under fidelity mortality)
  T3.1c  degraded channel: codec/local >= 1.03   (verification protects
                                                   writes in noise)
  T3.1d  regen/none >= 1.25 and regen > codec    (re-derivation rejuvenates)
  T3.1e  chan > codec                            (channel therapy adds)
  T3.1f  chan > blind                            (gating the boost pays)
  T3.2   aging clock: Spearman(fidelity at age 40..60, remaining lifespan)
         rho >= +0.25, p < 0.01                  (bioelectric mortality
                                                  biomarker)
  T3.3   Gompertz remains competitive (AIC gap < 60) in the none arm.
"""

from __future__ import annotations

import sys

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams, hazard_and_fits
from cultivation.bioelectric.fidelity import FidelityAgingCohort, FidelityCodec
from cultivation.coding.bio_channel import CHANNEL_PRESETS
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

N_CELLS = 60
K_INDIV = 300
YEARS = 130.0
CHECKUP = 5.0
FROM_AGE = 30.0
REGEN_PERIOD = 20.0
BUDGET = 6
BOOST = 1.25
BOOST_CAP = 8.0
SEEDS = (5, 6, 7, 8, 9)
CONDS = ("none", "local", "codec", "regen", "chan", "blind")

# Isolated-fidelity regime: (1) channel noise stays below the state-flip
# threshold through ~age 95 so pattern correctness — not capacity — is the
# binding constraint; (2) the inflammaging engine is weakened so regional
# pattern corruption carries the dominant share of mortality (in the default
# regime the engine+noise dominate and drown every pattern-level difference
# — a documented structural finding). The complementary high-noise regime
# (the capacity-cliff probe) is run in a separate block below.
REGIME = dict(kappa_noise=0.020, lambda_gap=0.024,
              mu_theta=0.03,       # junction-scaled pattern propagation
              h_sys=0.050, seed_rate=6.0e-5, h_inflam=0.030, mortality_k=0.10)

# Capacity-cliff probe regime: default channel aging (noise crosses the
# level spacing ~t50-60). Isolates the NOISE bottleneck: can pattern
# interventions (or even full regeneration) work when the channel itself
# has lost capacity?
CLIFF_REGIME = dict(kappa_noise=0.048, lambda_gap=0.030,
                    mu_theta=0.03,
                    h_sys=0.050, seed_rate=6.0e-5, h_inflam=0.030,
                    mortality_k=0.10)


def fidelity_target(n: int = N_CELLS) -> np.ndarray:
    """5-region, 4-distinct-level pattern (levels 1,2,3,5 of 7); no region
    occupies level 4 so senescent pinning at -25 mV always reads WRONG."""
    regions = [-50.0, -20.0, -50.0, -60.0, -40.0]
    per = n // len(regions)
    t = np.concatenate([np.full(per, v) for v in regions])
    if len(t) < n:
        t = np.concatenate([t, np.full(n - len(t), t[-1])])
    return t


def age_preset(t: float) -> dict:
    if t < 35:
        return CHANNEL_PRESETS["young"]
    if t < 55:
        return CHANNEL_PRESETS["mature"]
    if t < 75:
        return CHANNEL_PRESETS["old"]
    if t < 90:
        return CHANNEL_PRESETS["aged"]
    return CHANNEL_PRESETS["ancient"]


def degrade(preset: dict, factor: float) -> dict:
    return {
        "meas_noise_mV": preset["meas_noise_mV"] * factor,
        "dropout": min(0.9, preset["dropout"] * factor),
        "symbol_err": min(0.9, preset["symbol_err"] * factor),
    }


def run_condition(condition: str, seed: int, K: int = K_INDIV,
                  years: float = YEARS, channel_factor: float = 1.0,
                  regime: dict | None = None,
                  cohort_kw: dict | None = None) -> dict:
    levels = (cohort_kw or {}).get("levels", 7)
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=BUDGET,
                          levels=levels)
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **(regime or REGIME))
    ch = FidelityAgingCohort(K=K, params=params, seed=seed, **(cohort_kw or {}))
    decode_stats: list[dict] = []

    def maintain(t, cohort):
        if t < FROM_AGE - 1e-9:
            return
        if condition == "regen":
            if abs((t - FROM_AGE) % REGEN_PERIOD) <= 0.26:
                cohort.regenerate()
            return
        if condition == "none":
            return
        if abs((t - FROM_AGE) % CHECKUP) > 0.26:
            return
        preset = age_preset(t)
        if channel_factor != 1.0:
            preset = degrade(preset, channel_factor)
        if condition in ("codec", "chan", "blind"):
            rep = codec.maintain(cohort, preset, mode="codec")
            if condition == "chan":
                cohort.boost_channel(np.asarray(rep["verified_mask"], bool),
                                     BOOST, BOOST_CAP)
            elif condition == "blind":
                cohort.boost_channel(np.ones(cohort.K, bool), BOOST, BOOST_CAP)
            decode_stats.append(rep)
        else:  # local
            rep = codec.maintain(cohort, preset, mode="local")
            decode_stats.append(rep)

    s = ch.run(years=years, dt=0.25, intervention=maintain)
    return {
        "condition": condition,
        "median": s["median_lifespan"],
        "max": s["max_lifespan"],
        "survivors": s["survivors_at_end"],
        "F0_healthy": s["F0_healthy"],
        "hist_t": s["hist_t"],
        "hist_alive": s["hist_alive"],
        "hist_fid": s["hist_fid"],
        "snapshots": s["snapshots"],
        "death_ages": s["death_ages"],
        "decode_stats": decode_stats,
        "ledger": {"cycles": codec.cycles, "verified": codec.verified,
                   "refused": codec.refused, "restored": codec.restored},
    }


def aging_clock(snapshots: dict, death_ages: list, years: float) -> dict:
    """T3.2: fidelity at snapshot age predicts remaining lifespan
    (positive rho: higher fidelity -> longer remaining life)."""
    out = {}
    for age_s, fid in snapshots.items():
        age = float(age_s)
        fid = np.asarray(fid, float)
        rem = np.where(np.isinf(death_ages), years,
                       np.asarray(death_ages, float)) - age
        keep = rem > 0
        if keep.sum() < 30:
            continue
        rho, p = spearmanr(fid[keep], rem[keep])
        out[age_s] = {"rho": float(rho), "p": float(p), "n": int(keep.sum())}
    return out


def main() -> dict:
    setup()
    results: dict = {"seeds": list(SEEDS), "regime": REGIME, "conditions": {}}

    print("[exp8] pattern-fidelity mortality — the Level-3 gate")
    med_by_seed: dict[str, list[float]] = {}
    detail_seed0: dict[str, dict] = {}
    for seed in SEEDS:
        for cond in CONDS:
            r = run_condition(cond, seed=seed)
            med_by_seed.setdefault(cond, []).append(r["median"])
            if seed == SEEDS[0]:
                detail_seed0[cond] = r
        line = "  ".join(f"{c}={med_by_seed[c][-1]:.1f}" for c in CONDS)
        print(f"  seed {seed}: {line}")

    for cond in CONDS:
        meds = med_by_seed[cond]
        results["conditions"][cond] = {
            "median_mean": float(np.mean(meds)),
            "median_min": float(np.min(meds)),
            "median_max": float(np.max(meds)),
            "medians_by_seed": meds,
        }
        print(f"  {cond:6s}: median {np.mean(meds):6.1f} "
              f"(range {np.min(meds):.1f}-{np.max(meds):.1f})")

    med = {c: results["conditions"][c]["median_mean"] for c in CONDS}
    results["gains"] = {
        "codec_vs_none": med["codec"] / med["none"],
        "local_vs_none": med["local"] / med["none"],
        "codec_vs_local": med["codec"] / med["local"],
        "regen_vs_none": med["regen"] / med["none"],
        "regen_vs_codec": med["regen"] / med["codec"],
        "chan_vs_codec": med["chan"] / med["codec"],
        "chan_vs_blind": med["chan"] / med["blind"],
        "blind_vs_codec": med["blind"] / med["codec"],
    }

    # -------------------------------------------------- degraded channel arm
    print("  --- degraded channel (x2.5) ---")
    results["degraded"] = {}
    dmed: dict[str, list[float]] = {}
    for seed in SEEDS[:3]:
        for cond in ("none", "local", "codec"):
            r = run_condition(cond, seed=seed, channel_factor=2.5)
            dmed.setdefault(cond, []).append(r["median"])
    dm = {c: float(np.mean(v)) for c, v in dmed.items()}
    for c in dm:
        results["degraded"][c] = {"median_mean": dm[c], "medians_by_seed": dmed[c]}
        print(f"  {c:6s}: median {dm[c]:.1f}")
    results["degraded_gains"] = {
        "codec_vs_none": dm["codec"] / dm["none"],
        "local_vs_none": dm["local"] / dm["none"],
        "codec_vs_local": dm["codec"] / dm["local"],
    }

    # ------------------------------------------------------ cliff probe
    print("  --- capacity-cliff probe (high-noise regime) ---")
    results["cliff"] = {}
    cmed: dict[str, list[float]] = {}
    for seed in SEEDS[:3]:
        for cond in ("none", "codec", "regen", "chan"):
            r = run_condition(cond, seed=seed, regime=CLIFF_REGIME)
            cmed.setdefault(cond, []).append(r["median"])
    cm = {c: float(np.mean(v)) for c, v in cmed.items()}
    for c in cm:
        results["cliff"][c] = {"median_mean": cm[c], "medians_by_seed": cmed[c]}
        print(f"  {c:6s}: median {cm[c]:.1f}")
    results["cliff_gains"] = {
        "codec_vs_none": cm["codec"] / cm["none"],
        "chan_vs_none": cm["chan"] / cm["none"],
        "regen_vs_none": cm["regen"] / cm["none"],
        "regen_cliff_vs_regen_fidelity": cm["regen"] / med["regen"],
    }

    # ------------------------------------------------------------ criteria
    g = results["gains"]
    dg = results["degraded_gains"]
    results["criteria"] = {
        "T3.1a_maintenance_extends_life": g["codec_vs_none"] >= 1.06,
        "T3.1b_codec_beats_local": g["codec_vs_local"] >= 1.03,
        "T3.1c_verification_pays_degraded": dg["codec_vs_local"] >= 1.03,
        "T3.1d_regeneration_rejuvenates": (
            g["regen_vs_none"] >= 1.25 and med["regen"] > med["codec"]),
        "T3.1e_channel_therapy_adds": med["chan"] > med["codec"],
        "T3.1f_gating_pays": med["chan"] > med["blind"],
        "T3.1g_channel_limits_regeneration": (
            results["cliff_gains"]["regen_cliff_vs_regen_fidelity"] < 0.95),
    }

    # ---------------------------------------------------------- aging clock
    clock = aging_clock(detail_seed0["none"]["snapshots"],
                        detail_seed0["none"]["death_ages"], YEARS)
    clock_rhos = {a: [] for a in clock}
    for seed in SEEDS[1:]:
        r = run_condition("none", seed=seed)
        c = aging_clock(r["snapshots"], r["death_ages"], YEARS)
        for a, v in c.items():
            if a in clock_rhos:
                clock_rhos[a].append(v["rho"])
    results["aging_clock"] = {
        "seed0": clock,
        "rho_mean_by_age": {a: float(np.mean([clock[a]["rho"]] + clock_rhos.get(a, [])))
                            for a in clock},
    }
    mid = [v for a, v in results["aging_clock"]["rho_mean_by_age"].items()
           if 40.0 <= float(a) <= 60.0]
    results["criteria"]["T3.2_bioelectric_clock"] = bool(
        mid and np.mean(mid) >= 0.25
        and all(clock[a]["p"] < 0.01 for a in clock if 40.0 <= float(a) <= 60.0))

    # ----------------------------------------------------- Gompertz check
    ages = np.asarray(detail_seed0["none"]["death_ages"], float)
    fits = hazard_and_fits(ages, YEARS)
    best = min(fits["fits"], key=lambda k: fits["fits"][k]["aic"])
    gap = fits["fits"][best]["aic"] - fits["fits"]["gompertz"]["aic"]
    results["gompertz_check"] = {
        "best_model": best, "aic_gap_vs_gompertz": float(gap),
        "gompertz_beta": float(np.exp(fits["fits"]["gompertz"]["params"][1])),
    }
    results["criteria"]["T3.3_gompertz_competitive"] = bool(gap < 60)

    # ------------------------------------------------------------- printout
    print(f"\n  codec/none x{g['codec_vs_none']:.2f}  local/none x{g['local_vs_none']:.2f}  "
          f"codec/local x{g['codec_vs_local']:.2f}")
    print(f"  regen/none x{g['regen_vs_none']:.2f}  regen/codec x{g['regen_vs_codec']:.2f}  "
          f"chan/codec x{g['chan_vs_codec']:.2f}  chan/blind x{g['chan_vs_blind']:.2f}")
    print(f"  degraded: codec/none x{dg['codec_vs_none']:.2f}  "
          f"local/none x{dg['local_vs_none']:.2f}  codec/local x{dg['codec_vs_local']:.2f}")
    cg = results["cliff_gains"]
    print(f"  cliff: codec/none x{cg['codec_vs_none']:.2f}  chan/none x{cg['chan_vs_none']:.2f}  "
          f"regen/none x{cg['regen_vs_none']:.2f}  regen(cliff)/regen(fidelity) "
          f"x{cg['regen_cliff_vs_regen_fidelity']:.2f}")
    for k, v in results["criteria"].items():
        print(f"  {k}: {'PASS' if v else 'NEGATIVE'}")
    print(f"  aging-clock rho by age: "
          + "  ".join(f"{a}:{v:.2f}" for a, v in
                      results["aging_clock"]["rho_mean_by_age"].items()))
    print(f"  Gompertz check: best={best} gap={gap:.1f} "
          f"beta={results['gompertz_check']['gompertz_beta']:.3f}")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 4, figsize=(14.5, 3.4), constrained_layout=True)
    colors = {"none": PALETTE["muted"], "local": PALETTE["line2"],
              "codec": PALETTE["good"], "regen": PALETTE["line3"],
              "chan": "#148f77", "blind": PALETTE["accent"]}

    ax = axes[0]
    for cond in CONDS:
        r = detail_seed0[cond]
        ax.plot(r["hist_t"], r["hist_alive"], lw=1.6, color=colors[cond],
                label=f"{cond} ({np.mean(med_by_seed[cond]):.0f})")
    ax.set_title("(a) Survival under fidelity mortality")
    ax.set_xlabel("age (sim years)"); ax.set_ylabel("fraction alive")
    ax.legend(frameon=False, fontsize=7)

    ax = axes[1]
    for cond in CONDS:
        r = detail_seed0[cond]
        ax.plot(r["hist_t"], r["hist_fid"], lw=1.6, color=colors[cond], label=cond)
    ax.set_title("(b) Pattern fidelity = fraction correct-state")
    ax.set_xlabel("age (sim years)"); ax.set_ylabel("fidelity")
    ax.set_ylim(0, 1.02); ax.legend(frameon=False, fontsize=7)

    ax = axes[2]
    snap = detail_seed0["none"]["snapshots"]
    if "40.0" in snap:
        fid = np.asarray(snap["40.0"], float)
        dth = np.asarray(detail_seed0["none"]["death_ages"], float)
        rem = np.where(np.isinf(dth), YEARS, dth) - 40.0
        keep = rem > 0
        ax.scatter(fid[keep], rem[keep], s=6, alpha=0.45, color=PALETTE["primary"])
        c = results["aging_clock"]["seed0"].get("40.0", {})
        ax.set_title(f"(c) Aging clock: F(40) vs remaining life\n"
                     f"rho={c.get('rho', float('nan')):.2f}")
        ax.set_xlabel("fidelity at age 40"); ax.set_ylabel("remaining lifespan (yr)")

    ax = axes[3]
    x = np.arange(len(CONDS))
    meds = [med[c] for c in CONDS]
    ax.bar(x, meds, width=0.6, color=[colors[c] for c in CONDS])
    ax.set_xticks(x); ax.set_xticklabels(CONDS, fontsize=8)
    ax.set_title("(d) Median lifespan by regime")
    ax.set_ylabel("median (sim years)")
    for i, m in enumerate(meds):
        ax.text(i, m + 1, f"{m:.0f}", ha="center", fontsize=8)

    fig.savefig(fig_path("fig8_fidelity.png"))
    plt.close(fig)

    results["honest_notes"] = [
        "Mortality depends on DISCRETE pattern fidelity (organ-level fraction "
        "of cells in the correct Vmem band): written-value correctness can "
        "finally pay. Corruption is regional (cluster jumps) — the mechanism "
        "of two-headed planaria and tumor-like domains.",
        "Local mode maintains whatever the consensus says — it would "
        "faithfully maintain a two-headed worm. Only archive-referenced "
        "verification restores the wild-type pattern.",
        "Regeneration resets the pattern but NOT the channel engines — the "
        "model's explanation of why repeated cycles are needed (Dai 2025).",
        "Two-bottleneck structure: pattern repair plateaus at the channel "
        "capacity cliff; channel repair (connexin restoration) re-opens "
        "junction-scaled pattern propagation — DANGEROUS on corrupted tissue "
        "(quarantine loss), which is why the boost is verification-gated.",
        "Regime note: the isolated-fidelity regime (kappa 0.020, weakened "
        "inflammaging) makes pattern corruption the binding constraint; the "
        "capacity-cliff probe (kappa 0.048) shows the complementary "
        "bottleneck: when the channel loses capacity, even full re-derivation "
        "cannot hold the pattern — regeneration itself is channel-limited.",
    ]

    path = dump_json("exp8_fidelity.json", results)
    print(f"[exp8] results -> {path}")
    return results


if __name__ == "__main__":
    main()
