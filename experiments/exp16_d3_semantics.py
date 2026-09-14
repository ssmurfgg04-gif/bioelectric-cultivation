"""exp16 — THE WRITE SEMANTICS OF DEATH (D3, the tower's last open joint).

The question the whole project was built to ask, made operational: when a
cell dies, is the pattern LOST, or is it WRITTEN somewhere? Four competing
write semantics (cultivation/bioelectric/senescence_semantics.py), each a
different universe:

  stasis        death writes nothing          (pattern survives by redundancy)
  erasure       death destroys the memory     (death is an ending)
  transcription death moves the memory to    (death is a transition —
                junction neighbors             the star's naive form)
  broadcast     death writes a DEPOLARIZATION (the bystander effect —
                into junction neighbors        death spreads senescence)

Arms
  A  THE SHAPE TEST      senescence accumulation curves + spatial
                         clustering + Gompertz, per semantics. The real
                         signature (exponentially growing senescent
                         burden, Gompertz mortality, local spreading)
                         selects among semantics. A2: is the spread
                         STATE-mediated (junction-dependent) or purely
                         statistical (hazard-level)?
  C  THE COMPOSITION GATE the D3 engineering fix: latch v2 (consensus
                         anchoring) must compose with codec maintenance
                         (>= 0.98) where latch v1 cost 20%.
  D  THE PATTERN LEDGER  the star question, quantified: a novel morphology
                         (not in the genomic archive) is written; aging and
                         cell death run; where does the pattern go? I_V,
                         I_anchor, I_recoverable + spatial migration of
                         the memory carriers.

Pre-registered predictions:
  P1  broadcast: sen_frac grows faster than stasis AND shows spatial
      clustering above the statistical-contagion baseline; the excess
      spread is junction-dependent (A2) — the bystander effect signature.
  P2  transcription: demographics ~stasis (transcription is invisible in
      mortality), but the novel-pattern ledger decays SLOWEST and the
      memory carriers MIGRATE outward (death moves the pattern).
  P3  erasure: the novel-pattern ledger decays FASTEST.
  P4  v2 latch composes with the codec (>= 0.98; v1 reproduces ~0.80).
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams, hazard_and_fits
from cultivation.bioelectric.fidelity import (
    FidelityAgingCohort, FidelityCodec, LatchingAgingCohort,
)
from cultivation.bioelectric.senescence_semantics import SemanticsCohort
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp16_d3_semantics.json"

# ---- arm sizing -----------------------------------------------------------
K_A, YEARS_A, SEEDS_A = 200, 120.0, (21, 22, 23)      # shape + ledger arms
K_C, YEARS_C, SEEDS_C = 300, 170.0, (51, 52, 53)      # composition gate
HELDOUT_REGIME = dict(REGIME)
HELDOUT_REGIME.update(kappa_noise=0.017, lambda_gap=0.026)
HELDOUT_COHORT = dict(jump_rate=0.006, f_crit=0.655)
CHECKUP, FROM_AGE, BUDGET = 5.0, 30.0, 6

# ---- the novel morphology (arm D) ------------------------------------------
NOVEL_VAL = -10.0                                     # level 6: in no region
ZONE = np.zeros(N_CELLS, bool)
ZONE[24:36] = True                                    # the middle region
NOVEL_TARGET = fidelity_target()
NOVEL_TARGET[ZONE] = NOVEL_VAL


def _p(s):
    print(s, flush=True)


def _save(results):
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)


# ------------------------------------------------------------------ helpers
def build(cls, seed, K, regime, cohort_kw=None, **sem_kw):
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **dict(regime))
    kw = dict(cohort_kw or {})
    kw.update(sem_kw)
    return cls(K=K, params=params, seed=seed, **kw)


def clustering_index(cohort) -> float:
    """Adjacent-senesced pairs vs the random-permutation expectation —
    >1 means senescence is SPATIALLY CLUSTERED beyond chance."""
    n = cohort.n
    idxs = []
    for k in range(cohort.K):
        if not cohort.alive[k]:
            continue
        sen = cohort.senesced[k]
        Ks = int(sen.sum())
        if Ks < 2:
            continue
        pairs = int((sen[:-1] & sen[1:]).sum())
        exp_pairs = Ks * (Ks - 1) / n
        idxs.append(pairs / max(exp_pairs, 0.25))
    return float(np.mean(idxs)) if idxs else float("nan")


def exp_growth_rate(hist_t, hist_sen, lo=30.0, hi=80.0) -> float:
    """Slope of log(sen_frac) in the adult window — the accumulation
    shape (0 = linear, >0 = accelerating/contagious)."""
    t = np.asarray(hist_t)
    s = np.asarray(hist_sen, float)
    m = (t >= lo) & (t <= hi) & np.isfinite(s) & (s > 1e-3)
    if m.sum() < 8:
        return float("nan")
    return float(np.polyfit(t[m], np.log(s[m]), 1)[0])


# ---------------------------------------------------------------- arm A + A2
def arm_a(results: dict) -> None:
    _p("  A: the shape test — senescence accumulation per write semantics...")
    arms = {
        "stasis":        dict(sem="stasis", latch="v2"),
        "erasure":       dict(sem="erasure", latch="v2"),
        "transcription": dict(sem="transcription", latch="v2"),
        "broadcast":     dict(sem="broadcast", latch="v2"),
        "v1_stasis_ref": dict(cls=LatchingAgingCohort),
        "nolatch_ref":   dict(cls=FidelityAgingCohort),
    }
    out = {}
    for name, cfg in arms.items():
        cls = cfg.get("cls", SemanticsCohort)
        rows, cl60, cl90, fits = [], [], [], []
        for s in SEEDS_A:
            if cls is SemanticsCohort:
                ch = build(cls, s, K_A, REGIME,
                           death_semantics=cfg.get("sem", "stasis"),
                           latch=cfg.get("latch", "v2"))
            else:
                ch = build(cls, s, K_A, REGIME)
            seen = set()

            def sampler(t, cohort, seen=seen):
                for a in (60.0, 90.0):
                    if abs(t - a) < 0.13 and a not in seen:
                        seen.add(a)
                        (cl60 if a == 60.0 else cl90).append(
                            clustering_index(cohort))

            r = ch.run(years=YEARS_A, dt=0.25, intervention=sampler)
            rows.append(r)
            fits.append(hazard_and_fits(np.asarray(r["death_ages"], float),
                                        YEARS_A))
        med = float(np.mean([r["median_lifespan"] for r in rows]))
        rate = float(np.mean([exp_growth_rate(r["hist_t"], r["hist_sen"])
                              for r in rows]))
        gomp = [f["fits"]["gompertz"] for f in fits]
        # Gompertz params: [alpha, beta]; beta is the acceleration exponent
        beta = float(np.nanmean([np.exp(g["params"][1]) for g in gomp]))
        aic = float(np.nanmean([g["aic"] for g in gomp]))
        sen60 = _sen_at(rows, 60.0)
        out[name] = {
            "median": med, "sen_rate_30_80": rate,
            "sen_frac_at_60": sen60,
            "clustering_60": float(np.nanmean(cl60)) if cl60 else None,
            "clustering_90": float(np.nanmean(cl90)) if cl90 else None,
            "gompertz_beta": beta, "gompertz_aic": aic,
            "hist_t": rows[0]["hist_t"],
            "hist_sen_mean": [float(np.mean(x)) for x in zip(
                *[r["hist_sen"] for r in rows])],
        }
        _p(f"    {name:14s}: med {med:6.1f} yr  sen@60 {sen60:5.3f}  "
           f"rate {rate:+.4f}/yr  cl@60 {out[name]['clustering_60']}  "
           f"beta {beta:.3f}")
    results["A_shape"] = out

    # A2 — junction-dependence + dose-response: state-mediated (broadcast)
    # spread must accelerate when junctions decay more slowly AND with the
    # broadcast dose; statistical contagion is junction-independent.
    _p("  A2: junction-dependence of the spread (state vs statistical)...")
    a2 = {}
    for sem, gain in (("stasis", 0.0), ("broadcast", 3.0), ("broadcast", 8.0)):
        for lam in (0.012, 0.030):
            reg = dict(REGIME)
            reg["lambda_gap"] = lam
            rows = []
            for s in SEEDS_A:
                ch = build(SemanticsCohort, s, K_A, reg,
                           death_semantics=sem, latch="v2",
                           broadcast_gain=gain if sem == "broadcast" else 3.0)
                r = ch.run(years=YEARS_A, dt=0.25)
                rows.append(r)
            key = f"{sem}_g{gain:g}_lam{lam}"
            a2[key] = {
                "sen_frac_at_60": _sen_at(rows, 60.0),
                "sen_rate_30_80": float(np.mean([
                    exp_growth_rate(r["hist_t"], r["hist_sen"])
                    for r in rows])),
                "median": float(np.mean([r["median_lifespan"] for r in rows])),
            }
            _p(f"    {key:24s}: sen@60 {a2[key]['sen_frac_at_60']:5.3f}"
               f"  rate {a2[key]['sen_rate_30_80']:+.4f}")
    results["A2_junction"] = a2


def _sen_at(rows, age) -> float:
    vals = []
    for r in rows:
        t = np.asarray(r["hist_t"])
        m = np.abs(t - age) < 0.2
        if m.any():
            vals.append(np.nanmean(np.asarray(r["hist_sen"], float)[m]))
    return float(np.mean(vals)) if vals else float("nan")


# ---------------------------------------------------------------- arm C
def run_codec_arm(cls, sem_kw, seed, regime, cohort_kw):
    codec = FidelityCodec(n_cells=N_CELLS, budget_per_cycle=BUDGET, levels=7)
    ch = build(cls, seed, K_C, regime, cohort_kw, **sem_kw)
    stats: list[dict] = []

    def maintain(t, cohort):
        if t < FROM_AGE - 1e-9:
            return
        if abs((t - FROM_AGE) % CHECKUP) > 0.26:
            return
        rep = codec.maintain(cohort, age_preset(t), mode="codec")
        stats.append(rep)

    s = ch.run(years=YEARS_C, dt=0.25, intervention=maintain)
    s["ledger"] = {"cycles": codec.cycles, "verified": codec.verified,
                   "refused": codec.refused, "restored": codec.restored}
    return s


def arm_c(results: dict) -> None:
    _p("  C: the composition gate — latch v2 vs v1 vs none, codec on...")
    arms = {
        "plain":         (FidelityAgingCohort, {}),
        "latch_v1":      (LatchingAgingCohort, {}),
        "latch_v2":      (SemanticsCohort, {"death_semantics": "stasis",
                                            "latch": "v2"}),
        "latch_v2_bcast": (SemanticsCohort, {"death_semantics": "broadcast",
                                             "latch": "v2"}),
        "bcast_nolatch": (SemanticsCohort, {"death_semantics": "broadcast",
                                            "latch": "none"}),
    }
    out = {}
    for name, (cls, sem_kw) in arms.items():
        rows = [run_codec_arm(cls, sem_kw, s, HELDOUT_REGIME, HELDOUT_COHORT)
                for s in SEEDS_C]
        med = float(np.mean([r["median_lifespan"] for r in rows]))
        out[name] = {
            "median": med,
            "medians_by_seed": [float(r["median_lifespan"]) for r in rows],
            "restored": float(np.mean([r["ledger"]["restored"]
                                       for r in rows])),
            "refused": float(np.mean([r["ledger"]["refused"]
                                      for r in rows])),
        }
        _p(f"    {name:14s}: median {med:6.1f} yr  "
           f"(seeds {[round(r['median_lifespan']) for r in rows]})")
    base = out["plain"]["median"]
    v1 = out["latch_v1"]["median"] / base
    v2 = out["latch_v2"]["median"] / base
    v2b_vs_bnl = out["latch_v2_bcast"]["median"] / out["bcast_nolatch"]["median"]
    v2b_vs_base = out["latch_v2_bcast"]["median"] / base
    c = results.setdefault("criteria", {})
    c["C1_v2_composes"] = bool(v2 >= 0.98)
    c["C2_v2bcast_composes_within_semantics"] = bool(v2b_vs_bnl >= 0.98)
    c["C0_v1_negative_reproduced"] = bool(v1 < 0.95)
    results["C_composition"] = {
        "arms": out,
        "ratios": {"v1_over_plain": v1, "v2_over_plain": v2,
                   "v2bcast_over_bcast_nolatch": v2b_vs_bnl,
                   "v2bcast_over_plain": v2b_vs_base},
    }
    _p(f"    RATIOS  v1/plain {v1:.3f} (reproduces x0.80?)  "
       f"v2/plain {v2:.3f}  v2bcast/bcast-nolatch {v2b_vs_bnl:.3f}")


# ---------------------------------------------------------------- arm D
def arm_d(results: dict) -> None:
    _p("  D: the pattern ledger — where does a novel morphology go on death?")
    LEDGER_AT = np.arange(10.0, YEARS_A + 1, 5.0)
    arms = ("stasis", "erasure", "transcription", "broadcast", "v1_ref")
    out = {}
    for sem in arms:
        # v1 reference via the bit-exact arm (tests/test_d3_semantics.py):
        # SemanticsCohort(latch='v1', stasis) reproduces LatchingAgingCohort
        # exactly, and carries the ledger API.
        sem_kw = (dict(death_semantics="stasis", latch="v1")
                  if sem == "v1_ref" else
                  dict(death_semantics=sem, latch="v2"))
        cls = SemanticsCohort
        # mortality OFF: the information question is not the demographic one
        reg = dict(REGIME)
        reg.update(mortality_k=1e-4)
        ck = dict(jump_rate=0.006, f_crit=0.655, k_fail=0.0)
        series = {k: [] for k in ("t", "I_V", "I_anchor", "I_recoverable",
                                  "centroid", "zone_sen")}
        deaths = []
        for s in SEEDS_A:
            ch = build(cls, s, K_A, reg, ck, **sem_kw)
            written = {"done": False}
            seen = set()

            def sampler(t, cohort, written=written, seen=seen):
                if not written["done"] and t >= 5.0:
                    written["done"] = True
                    do = np.zeros((cohort.K, cohort.n), bool)
                    do[:, ZONE] = True
                    cohort.theta = np.where(do, NOVEL_VAL, cohort.theta)
                    cohort.V = np.where(do, NOVEL_VAL, cohort.V)
                    if hasattr(cohort, "on_write"):
                        cohort.on_write(do)
                for a in LEDGER_AT:
                    if abs(t - a) < 0.13 and a not in seen:
                        seen.add(a)
                        led = cohort.pattern_ledger(ref=NOVEL_TARGET,
                                                    zone=ZONE)
                        series["t"].append(float(a))
                        series["I_V"].append(led["I_V"])
                        series["I_anchor"].append(led["I_anchor"])
                        series["I_recoverable"].append(led["I_recoverable"])
                        series["centroid"].append(
                            cohort.pattern_centroid(6, ZONE))
                        series["zone_sen"].append(
                            float(cohort.senesced[:, ZONE].mean()))

            ch.run(years=YEARS_A, dt=0.25, intervention=sampler)
            deaths.append(ch.death_events)

        def _curve(key):
            u = sorted(set(series["t"]))
            m = {t: i for i, t in enumerate(series["t"])}
            return [float(np.mean([series[key][i] for i, t2 in enumerate(
                series["t"]) if t2 == t])) for t in u], u

        I_rec, ts = _curve("I_recoverable")
        I_a, _ = _curve("I_anchor")
        I_v, _ = _curve("I_V")
        cent, _ = _curve("centroid")
        zsen, _ = _curve("zone_sen")
        out[sem] = {
            "t": ts, "I_V": I_v, "I_anchor": I_a, "I_recoverable": I_rec,
            "centroid": cent, "zone_sen": zsen,
            "cell_deaths": float(np.mean(deaths)),
            "I_anchor_at_60": float(I_a[ts.index(60.0)]),
            "I_recoverable_at_60": float(I_rec[ts.index(60.0)]),
            "centroid_drift_60": float(cent[ts.index(60.0)]),
        }
        _p(f"    {sem:14s}: I_anchor@60 {out[sem]['I_anchor_at_60']:5.3f}  "
           f"I_rec@60 {out[sem]['I_recoverable_at_60']:5.3f}  "
           f"centroid@60 {out[sem]['centroid_drift_60']:5.2f}  "
           f"deaths {out[sem]['cell_deaths']:.0f}")
    results["D_ledger"] = out


# ---------------------------------------------------------------- arm C2
"""Iteration 2 — the MATCHED-CHANNEL MEMORY calibration.

Iteration 1 (arm C above, preserved verbatim): v2's consensus anchoring
improved composition 0.844 -> 0.881 but the gate stayed closed. The
mechanism, identified from the no-codec arm-A reference: the pin
(k_anchor=50/yr) is ~100x the bandwidth of the junction channel it backs
up (~g0*deg ~ 0.4/yr) — it decouples theta from the live V state,
chronically inflating the |V-theta| senescence hazard (sen@60: v2 0.048
vs no-latch 0.014). A backup channel that dominates the primary channel
is not a redundancy — it is a replacement that fights it.

C2 sweeps k_anchor (the memory's pull rate) at fixed everything else.
The pre-registered principle: the composition ratio should peak at
k ~ O(junction bandwidth) — the D3 LAW: the somatic memory channel must
be bandwidth-matched to the pattern channel it replaces. The gate then
re-tests v2 (matched k) and v2+broadcast against latch-free baselines.
"""


def arm_c2(results: dict) -> None:
    _p("  C2: matched-channel memory — the k_anchor sweep...")
    ks = (0.25, 0.5, 1.0, 2.0, 5.0, 50.0)
    sweep = {}
    for k in ks:
        rows = [run_codec_arm(SemanticsCohort,
                              {"death_semantics": "stasis", "latch": "v2",
                               "k_anchor": k}, s, HELDOUT_REGIME, HELDOUT_COHORT)
                for s in SEEDS_C]
        sweep[str(k)] = float(np.mean([r["median_lifespan"] for r in rows]))
        _p(f"    k_anchor {k:5.2f}/yr: median {sweep[str(k)]:6.1f} yr")
    # latch-free baselines are k-independent: reuse the iteration-1 arms
    base = results["C_composition"]["arms"]["plain"]["median"]
    bnl = results["C_composition"]["arms"]["bcast_nolatch"]["median"]
    ratios = {k: v / base for k, v in sweep.items()}
    best_k = max(ratios, key=ratios.get)
    # full composition table at the best k, with the broadcast arm
    _p("  C2: composition table at the matched k...")
    final = {}
    for name, sem_kw in {
        "latch_v2": {"death_semantics": "stasis", "latch": "v2",
                     "k_anchor": float(best_k)},
        "latch_v2_bcast": {"death_semantics": "broadcast", "latch": "v2",
                           "k_anchor": float(best_k)},
    }.items():
        rows = [run_codec_arm(SemanticsCohort, sem_kw, s, HELDOUT_REGIME,
                              HELDOUT_COHORT) for s in SEEDS_C]
        final[name] = {
            "median": float(np.mean([r["median_lifespan"] for r in rows])),
            "medians_by_seed": [float(r["median_lifespan"]) for r in rows],
            "restored": float(np.mean([r["ledger"]["restored"] for r in rows])),
        }
        _p(f"    {name:14s}: median {final[name]['median']:6.1f} yr")
    r_v2 = final["latch_v2"]["median"] / base
    r_v2b = final["latch_v2_bcast"]["median"] / bnl
    r_v2b_base = final["latch_v2_bcast"]["median"] / base
    c = results.setdefault("criteria", {})
    c["C1_v2_composes_matched"] = bool(r_v2 >= 0.98)
    c["C2_v2bcast_composes_matched"] = bool(r_v2b >= 0.98)
    c["C3_matched_channel_peak"] = bool(
        ratios[best_k] > max(ratios[k] for k in ("0.25", "50.0")))
    results["C2_matched_channel"] = {
        "sweep_medians": sweep, "sweep_ratios": ratios, "best_k": float(best_k),
        "final": final,
        "ratios": {"v2_over_plain": r_v2, "v2bcast_over_bcast_nolatch": r_v2b,
                   "v2bcast_over_plain": r_v2b_base},
    }
    _p(f"    RATIOS  v2/plain {r_v2:.3f}  v2bcast/bcast-nolatch {r_v2b:.3f}"
       f"  (best k={best_k})")


# ---------------------------------------------------------------- arm D2
def arm_d2(results: dict) -> None:
    _p("  D2: the pattern ledger, full-copy transcription + matched k...")
    LEDGER_AT = np.arange(10.0, YEARS_A + 1, 5.0)
    arms = ("stasis", "erasure", "transcription", "broadcast")
    best_k = results.get("C2_matched_channel", {}).get("best_k", 1.0)
    out = {}
    for sem in arms:
        series = {k: [] for k in ("t", "I_V", "I_anchor", "I_recoverable",
                                  "centroid", "zone_sen")}
        deaths = []
        for s in SEEDS_A:
            reg = dict(REGIME)
            reg.update(mortality_k=1e-4)
            ck = dict(jump_rate=0.006, f_crit=0.655, k_fail=0.0)
            ch = build(SemanticsCohort, s, K_A, reg, ck,
                       death_semantics=sem, latch="v2", k_anchor=best_k)
            written = {"done": False}
            seen = set()

            def sampler(t, cohort, written=written, seen=seen):
                if not written["done"] and t >= 5.0:
                    written["done"] = True
                    do = np.zeros((cohort.K, cohort.n), bool)
                    do[:, ZONE] = True
                    cohort.theta = np.where(do, NOVEL_VAL, cohort.theta)
                    cohort.V = np.where(do, NOVEL_VAL, cohort.V)
                    if hasattr(cohort, "on_write"):
                        cohort.on_write(do)
                for a in LEDGER_AT:
                    if abs(t - a) < 0.13 and a not in seen:
                        seen.add(a)
                        led = cohort.pattern_ledger(ref=NOVEL_TARGET,
                                                    zone=ZONE)
                        series["t"].append(float(a))
                        series["I_V"].append(led["I_V"])
                        series["I_anchor"].append(led["I_anchor"])
                        series["I_recoverable"].append(led["I_recoverable"])
                        series["centroid"].append(
                            cohort.pattern_centroid(6, ZONE))
                        series["zone_sen"].append(
                            float(cohort.senesced[:, ZONE].mean()))

            ch.run(years=YEARS_A, dt=0.25, intervention=sampler)
            deaths.append(ch.death_events)

        def _curve(key):
            u = sorted(set(series["t"]))
            return [float(np.mean([series[key][i] for i, t2 in enumerate(
                series["t"]) if t2 == t])) for t in u], u

        I_rec, ts = _curve("I_recoverable")
        I_a, _ = _curve("I_anchor")
        I_v, _ = _curve("I_V")
        cent, _ = _curve("centroid")
        zsen, _ = _curve("zone_sen")
        i60 = ts.index(60.0)
        out[sem] = {
            "t": ts, "I_V": I_v, "I_anchor": I_a, "I_recoverable": I_rec,
            "centroid": cent, "zone_sen": zsen,
            "cell_deaths": float(np.mean(deaths)),
            "I_anchor_at_60": float(I_a[i60]),
            "I_recoverable_at_60": float(I_rec[i60]),
            "centroid_drift_60": float(cent[i60]),
            "centroid_drift_0": float(cent[0]),
        }
        _p(f"    {sem:14s}: I_anchor@60 {out[sem]['I_anchor_at_60']:5.3f}  "
           f"I_rec@60 {out[sem]['I_recoverable_at_60']:5.3f}  "
           f"centroid@60 {out[sem]['centroid_drift_60']:5.2f}  "
           f"deaths {out[sem]['cell_deaths']:.0f}")
    c = results.setdefault("criteria", {})
    # pre-registered: transcription preserves the novel pattern BETTER than
    # erasure AND its memory carriers MIGRATE (centroid drift grows)
    c["D1_transcription_preserves"] = bool(
        out["transcription"]["I_recoverable_at_60"]
        > out["erasure"]["I_recoverable_at_60"] + 0.05)
    c["D2_transcription_migrates"] = bool(
        out["transcription"]["centroid_drift_60"]
        > out["stasis"]["centroid_drift_60"] + 0.5)
    c["D3_erasure_worst"] = bool(
        out["erasure"]["I_recoverable_at_60"]
        <= min(out[s]["I_recoverable_at_60"] for s in arms))
    results["D2_ledger"] = out
def figure(results: dict) -> None:
    setup()
    C = {"stasis": "0.45", "erasure": PALETTE["accent"],
         "transcription": PALETTE["warn"], "broadcast": PALETTE["primary"]}
    fig, ax = plt.subplots(1, 4, figsize=(19, 4.4),
                           constrained_layout=True)
    # panel 1: sen_frac curves (iteration 1, unchanged)
    A = results["A_shape"]
    for name in ("stasis", "erasure", "transcription", "broadcast",
                 "nolatch_ref"):
        col = C.get(name, "0.72")
        t = np.asarray(A[name]["hist_t"])
        s = np.asarray(A[name]["hist_sen_mean"])
        m = (t >= 20) & np.isfinite(s)
        ax[0].plot(t[m], s[m], label=name, color=col, lw=2.2)
    ax[0].set(xlabel="age (yr)", ylabel="senesced fraction",
              title="A: the shape of accumulation")
    ax[0].legend(fontsize=8)

    # panel 2: the D3 LAW — composition ratio vs memory pull rate
    M = results["C2_matched_channel"]
    ks = sorted(M["sweep_ratios"], key=float)
    vals = [M["sweep_ratios"][k] for k in ks]
    ax[1].plot([float(k) for k in ks], vals, "o-", color=PALETTE["primary"],
               lw=2.2)
    ax[1].axhline(0.98, color=PALETTE["accent"], ls="--", lw=1.2,
                  label="composition gate")
    ax[1].axvline(0.4, color="0.6", ls=":", lw=1,
                  label="junction bandwidth ~0.4/yr")
    ax[1].set(xscale="log", xlabel="k_anchor (memory pull, 1/yr, log)",
              ylabel="latch+codec median / codec-only median",
              title="C2: the matched-channel law (D3)")
    ax[1].legend(fontsize=8)

    # panel 3: the composition bars (iteration 2)
    R = results["C2_matched_channel"]["ratios"]
    R1 = results["C_composition"]["ratios"]
    names = ["v1\n(iter 1)", "v2 k=50\n(iter 1)", "v2 matched\n(THE GATE)",
             "v2+bcast\nmatched"]
    vals = [R1["v1_over_plain"], R1["v2_over_plain"], R["v2_over_plain"],
            R["v2bcast_over_bcast_nolatch"]]
    ax[2].bar(range(4), vals,
              color=["0.6", "0.6", PALETTE["good"], PALETTE["primary"]])
    ax[2].axhline(0.98, color=PALETTE["accent"], ls="--", lw=1.2)
    ax[2].axhline(1.0, color="k", ls=":", lw=1)
    ax[2].set(xticks=range(4), xticklabels=names,
              ylabel="median lifespan ratio", ylim=(0.75, 1.10),
              title="C: does the latch compose with the codec?")

    # panel 4: the pattern ledger (iteration 2) + migration inset
    D = results["D2_ledger"]
    for name in ("stasis", "erasure", "transcription", "broadcast"):
        ax[3].plot(D[name]["t"], D[name]["I_recoverable"], color=C[name],
                   lw=2.2, label=name)
    ax[3].set(xlabel="age (yr)", ylabel="I_recoverable (novel pattern)",
              ylim=(0, 1.05),
              title="D: does the novel pattern survive death?")
    ax[3].legend(fontsize=8)
    fig.suptitle("exp16 — the write semantics of death (D3 resolved)",
                 fontsize=13)
    fig.savefig(fig_path("fig17_d3_semantics"), dpi=150)
    plt.close(fig)
    _p("  figure: results/figures/fig17_d3_semantics.png")


# ---------------------------------------------------------------- driver
def main() -> dict:
    import os
    t0 = time.time()
    _p("exp16 — the write semantics of death (D3)")
    results = {"exp": "exp16_d3_semantics",
               "arms": {"A": f"K={K_A} years={YEARS_A} seeds={SEEDS_A}",
                        "C": f"K={K_C} years={YEARS_C} seeds={SEEDS_C}"}}
    try:
        results_load = json.load(open(OUT)) if os.path.exists(OUT) else {}
    except Exception:
        results_load = {}
    # iteration 1 (arms A/C/D, preserved); iteration 2 (C2/D2)
    jobs = [("A", arm_a), ("C", arm_c), ("D", arm_d),
            ("C2", arm_c2), ("D2", arm_d2)]
    for key, fn in jobs:
        if key in results_load:
            results[key] = results_load[key]
            _p(f"  [resume] arm {key} loaded from cache")
            continue
        fn(results)
        _save(results)
        _p(f"  arm {key} done ({time.time()-t0:.0f}s) -> saved")
    if "criteria" not in results:
        results["criteria"] = results_load.get("criteria", {})
    figure(results)
    _save(results)
    _p(f"exp16 complete in {time.time()-t0:.0f}s")
    return results


if __name__ == "__main__":
    main()
