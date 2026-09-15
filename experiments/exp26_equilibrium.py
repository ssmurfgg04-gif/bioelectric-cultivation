"""exp26 — EQUILIBRIUM ATTRIBUTION: what is the death-restoration balance
point MADE of?

THE USER'S FRAMING (after exp23 + exp24): both attacks on the edges
failed. exp23 moved the RESTORATION side (allocation re-slicing: effect
ceiling 0.023); exp24 moved the CORRUPTION side (potentiation: +0.0056
permanent, +0.0044 transient at the 5yr spec, vs the 0.046 physics-scale
bar). The equilibrium itself — the balance point — was never probed.
If it is invariant to both sides' marginal reallocation, the lever is
elsewhere: in the ARCHITECTURE (how patterns are stored), the SUBSTRATE
(the physics of jumps), or the COUPLING between patterns. This
experiment does not try to break the equilibrium; it takes it apart.

METHOD — attribution by four complementary probes, all on exp23's exact
multi-pattern geometry (zones C/A/B/birth, cluster-aligned, scrambled;
seeds 21-23, K=200, 120yr, all-K ledger convention; the default arm is
exp23's default b6 and doubles as the bit-exact regression anchor):

  1. ELASTICITY MAP (recorded, not gated): one-factor sweeps around the
     default — jump_rate x{0.25,0.5,2,4} (substrate), budget 12 (extends
     exp23's published 1/2/4/6 curve), period {1.25,2.5,10} (restoration
     frequency), C's hazard {1,4,8} (zone physics), k_fail {0,0.15,0.60}
     (fidelity-death channel), mortality_k 0.025 (senescence-death
     channel), sigma0+kappa x{0.5,2} (channel noise physics). The
     log-log slopes rank the levers.

  2. FLUX-COMPOSITE INVARIANCE (the conservation-law candidate): define
     Phi = corruption cells/yr / restoration cells/yr
         = (jump_rate * cluster_len * sum_mult) / (budget / period).
     Default Phi = 0.34. Four compensation arms hold Phi at 0.34 while
     multiplying both sides: jump4x+budget24, jump4x+period1.25 (and the
     milder 2x pair). If the balance point is a function of Phi alone,
     all compensation arms land back on the default's I_V; if they land
     elsewhere, Phi is not the invariant — something the composite
     misses (dwell? capacity? detection?) sets the point. The two
     compensation ROUTES also dissociate: budget-route pays capacity,
     period-route pays frequency (and shortens detection dwell). Route
     asymmetry localizes the binding term.

  3. ARCHITECTURE GRANULARITY (the 'how patterns are stored' lever):
     cluster_len is now a constructor axis (n_clusters 12 -> 4 or 20;
     zones stay cluster-aligned at all three). ANALYTICAL FACT (pre-
     registered): per-cell jump-corruption flux is architecture-
     INVARIANT (jump_rate * cluster_len * sum_mult with sum_mult scaling
     as 1/cluster_len at fixed zone physics) — so if I_V* is set purely
     by the flux ratio, granularity cannot move it; if granularity moves
     it, the repair-cost-per-event / dwell-per-event channel is a real
     lever the composite Phi misses. The two readings are mutually
     exclusive; the data decides.

  4. DECOMPOSITION (two instruments):
     a. MORTALITY-SELECTION SHARE: alive-only minus all-K I_V gap at 60,
        under each death-channel arm. The equilibrium's visible 'clean'
        alive-pool fidelity is partly bought by deaths; k_fail=0 and
        mortality_k/4 split the purchase between the two death channels.
     b. CORRUPTION-SOURCE LEDGER (new stack instrument): every wrong
        zone cell at ledger age is classified by SOURCE — senescence
        (pinned), jump (cluster jumped after the cell's last repair),
        or non-jump (noise/drift/repair-imprecision). This turns exp24's
        potentiation negative into arithmetic: predicted delta =
        jump_share * (1 - 0.25) * coverage. Closure within tolerance
        means the linear decomposition EXPLAINS the failed intervention;
        a miss means potentiation over/under-performed its own
        mechanism's arithmetic (a second-order effect worth chasing).

PRE-REGISTERED (fixed before the full run; bars anchored on published
numbers only — 0.046 physics bar, 0.023 policy ceiling, exp24's +0.0056):

  EQ1a (COMPENSATION): the four Phi-equal arms (comp_b, comp_p, comp4_b,
      comp4_p) land within 0.02 of EACH OTHER pairwise on B's all-K
      I_V@60, AND within 0.02 of default. Failing => Phi alone does not
      determine the balance point.
  EQ1b (STRESS): default B I_V@60 - jr_4x B I_V@60 > 0.04 — 4x
      uncompensated corruption breaks the balance materially (the
      contrast that makes EQ1a meaningful). jr_2x recorded alongside.
  EQ2 (ROUTES): |comp_b - comp_p| < 0.02 => the two compensation routes
      are equivalent (flux law). comp_p - comp_b > 0.03 => frequency
      beats capacity (dwell/detection-binding). comp_b - comp_p > 0.03
      => capacity beats frequency (budget-binding). The branch that
      fires names the binding term.
  EQ3 (SELECTION SHARE): alive60 gap on B under k_fail=0 shrinks to
      < 50% of the default gap. Failing => the alive/all-K gap is not
      primarily fidelity-death-driven (the senescence-burden channel
      carries the selection).
  EQ4 (ARCHITECTURE DISJUNCTION, mutually exclusive branches):
      (a) all pairwise |dI_V*B@60| over {arch4, default, arch20} <
          0.02 => architecture-INVARIANT: the equilibrium is a flux-
          ratio object; granularity is not a lever.
      (b) ordered by fineness AND max pairwise |d| > 0.046 =>
          architecture is a PRIMARY lever (the 'how patterns are
          stored' answer).
      Ambiguous middle (a fails, b's magnitude fails) recorded honestly.
  EQ5 (POTENTIATION CLOSURE): pred = share_jump(B)@60(default) * 0.75
      * 0.4738; |pred - 0.0056| < 0.01 — the instrumented decomposition
      postdicts exp24's permanent-potentiation delta.
  EQ6 (MODULARITY): C's hazard 2 -> 8 leaves B's all-K I_V@60 within
      0.01 (per-pattern equilibria decoupled at budget 6; exp23 E1's
      competition-invisible reading, now probed from the physics side).
      C's own dose-response recorded as the sanity check.
  R (REGRESSION): default replicates exp23's published default@b6:
      per-pattern |dI_V@60| < 0.005, |median delta| < 0.5yr, restored
      count exactly equal (bit-exact hooks claim at experiment scale).

Falsifies: EQ1a failing (with EQ1b passing) kills the flux-ratio
conservation law — the equilibrium is not a simple corruption:repair
ratio, and the field of candidate invariants narrows to whatever the
compensation arms' residuals point at. EQ4(b) firing makes cluster
granularity — not allocation, not potentiation — the first lever that
actually moves the equilibrium, and re-weights every 'memory capacity'
claim toward storage architecture. EQ5 failing means potentiation's
failure was NOT pure arithmetic — there is a second-order interaction
(uncovered potentiation's amplification or suppression) left on the
table. EQ6 failing means zone equilibria are coupled through something
other than the budget at b6 — the death channel is the obvious suspect,
and EQ3's decomposition then reads as the coupling mechanism.

Adaptation note (recorded before the run): the architecture arms change
the CODEC's cluster granularity too (read/write units) — that is the
point (architecture = how the pattern is stored and repaired), but it
means a granularity effect conflates corruption-event size with repair
granularity; the honest reading is 'the storage-repair architecture',
not 'jump event size' alone.
"""
from __future__ import annotations

import json
import sys
import time

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.aging import AgingParams
from cultivation.bioelectric.fidelity import FidelityCodec, quantize
from experiments.exp8_fidelity import (
    N_CELLS, REGIME, age_preset, fidelity_target,
)
from experiments.exp23_multi_pattern import (
    ZONES, MULTI_TARGET, ZONE_MASK, GROUPS, _zone_write,
)
from experiments.viz import setup, fig_path, PALETTE

import matplotlib.pyplot as plt

OUT = "results/exp26_equilibrium.json"
EXP23 = "results/exp23_multi_pattern.json"
EXP24 = "results/exp24_potentiation.json"

K, YEARS, SEEDS = 200, 120.0, (21, 22, 23)
FROM_AGE = 5.0            # deliberate write age (exp23 convention)
MAINT_FROM = 30.0
LEDGER_AT = np.arange(10.0, YEARS + 1, 10.0)
BUDGET = 6                # the default-arm budget (exp23's b6)

# exp24's published permanent-potentiation numbers (EQ5 closure targets)
POT_PERM_DELTA_B = 0.0056          # I_V(B)@60, b6, pot_perm - plain
POT_PERM_COVERAGE = 0.4738         # mean potentiated (animal, cluster) frac
POT_FACTOR = 0.25                  # jump-rate multiplier while potentiated

# ---- arms: name -> build overrides (all else = exp23 default b6) --------
ARMS = {
    # regression anchor
    "default":  {},
    # substrate: jump-rate sweep
    "jr_025x":  {"jump_rate": 0.0015},
    "jr_05x":   {"jump_rate": 0.003},
    "jr_2x":    {"jump_rate": 0.012},
    "jr_4x":    {"jump_rate": 0.024},
    # restoration: budget + period (budget curve 1/2/4/6 from exp23)
    "b12":      {"budget": 12},
    "p_1_25":   {"period": 1.25},
    "p_2_5":    {"period": 2.5},
    "p_10":     {"period": 10.0},
    # flux composite: Phi = 0.34 preserved, both sides multiplied
    "comp_b":   {"jump_rate": 0.012, "budget": 12},     # 2x / 2x
    "comp_p":   {"jump_rate": 0.012, "period": 2.5},    # 2x / 2x
    "comp4_b":  {"jump_rate": 0.024, "budget": 24},     # 4x / 4x
    "comp4_p":  {"jump_rate": 0.024, "period": 1.25},   # 4x / 4x
    # architecture: cluster granularity (zones stay aligned)
    "arch20":   {"n_clusters": 20},
    "arch4":    {"n_clusters": 4},
    # death channels
    "kfail_0":  {"k_fail": 0.0},
    "kfail_lo": {"k_fail": 0.15},
    "kfail_hi": {"k_fail": 0.60},
    "mk_lo":    {"mk": 0.025},      # mortality_k 0.10 -> 0.025
    # zone coupling: C's hazard (default 2.0)
    "hazC_1":   {"hazC": 1.0},
    "hazC_4":   {"hazC": 4.0},
    "hazC_8":   {"hazC": 8.0},
    # channel noise physics
    "noise_lo": {"regime_ovr": {"sigma0": 0.10, "kappa_noise": 0.010}},
    "noise_hi": {"regime_ovr": {"sigma0": 0.40, "kappa_noise": 0.040}},
}


def _p(s):
    print(s, flush=True)


# ------------------------------------------------------------- cohort
def _jump_mult_for(n_clusters: int) -> np.ndarray:
    """Zone physics (C 1.0 / A 0.5 / B 2.0 / birth 1.0) at any granularity."""
    cl = N_CELLS // n_clusters
    jm = np.ones(n_clusters)
    for s, e, m in ((0, 15, 1.0), (15, 30, 0.5), (30, 45, 2.0), (45, 60, 1.0)):
        jm[s // cl: e // cl] = m
    return jm


def _hazard_boost_for(hazC: float) -> np.ndarray:
    hb = np.ones(N_CELLS)
    hb[0:15] = hazC
    return hb


def build26(seed: int, *, jump_rate: float = 0.006, k_fail: float = 0.30,
            n_clusters: int = 12, hazC: float = 2.0,
            regime_ovr: dict | None = None, mk: float | None = None):
    from experiments.exp23_multi_pattern import MultiPatternCohort

    class EquilibriumCohort(MultiPatternCohort):
        """MultiPatternCohort + per-cell repair bookkeeping (the
        corruption-source instrument's other half; no RNG consumption)."""

        def on_write(self, do: np.ndarray) -> None:
            if getattr(self, "_jump_audit_on", False):
                rows, cols = np.nonzero(do)
                self._last_repair_cells[rows, cols] = self.t
            super().on_write(do)

    params_kw = dict(REGIME)
    params_kw.update(regime_ovr or {})
    if mk is not None:
        params_kw["mortality_k"] = mk
    params = AgingParams(n_cells=N_CELLS, target0=fidelity_target(),
                         **params_kw)
    ch = EquilibriumCohort(K=K, params=params, seed=seed,
                           death_semantics="broadcast", latch="v2",
                           protect_written=True, jump_rate=jump_rate,
                           f_crit=0.655, k_fail=k_fail,
                           n_clusters=n_clusters)
    ch._tgt = fidelity_target()
    ch.jump_mult = _jump_mult_for(n_clusters)
    ch.hazard_boost = _hazard_boost_for(hazC)
    ch._audit_groups = GROUPS
    ch._write_audit = np.zeros(4, int)
    ch._audit_on = False
    # corruption-source instrument
    ch._jump_audit_on = True
    ch._last_jump = np.full((K, n_clusters), -np.inf)
    ch._last_repair_cells = np.full((K, N_CELLS), -np.inf)
    return ch


def _source_shares(ch, zone_mask: np.ndarray, ref: np.ndarray) -> dict:
    """Classify every zone cell at the CURRENT state by correctness and
    (if wrong) corruption source: senescence / jump / non-jump."""
    zidx = np.nonzero(zone_mask)[0]
    r = np.broadcast_to(np.asarray(ref, float), (ch.K, ch.n))
    ok = (quantize(ch.V[:, zidx], ch.levels)
          == quantize(r[:, zidx], ch.levels))                # (K, z)
    sen = ch.senesced[:, zidx]                               # (K, z)
    cl_of = zidx // ch.cluster_len                           # (z,)
    jumped_since = ch._last_jump[:, cl_of] > ch._last_repair_cells[:, zidx]
    wrong = ~ok
    src = np.where(wrong,
                   np.where(sen, 1, np.where(jumped_since, 2, 3)),
                   0)
    n = src.size
    return {
        "wrong": float((src != 0).sum() / n),
        "senescence": float((src == 1).sum() / n),
        "jump": float((src == 2).sum() / n),
        "non_jump": float((src == 3).sum() / n),
    }


# ------------------------------------------------------------- run arm
def run_arm(arm: str, seed: int) -> dict:
    spec = ARMS[arm]
    ch = build26(seed, **{k: v for k, v in spec.items()
                          if k in ("jump_rate", "k_fail", "n_clusters",
                                   "hazC", "regime_ovr", "mk")})
    budget = spec.get("budget", BUDGET)
    period = spec.get("period", 5.0)
    codec = FidelityCodec(n_cells=N_CELLS,
                          n_clusters=spec.get("n_clusters", 12),
                          budget_per_cycle=budget, levels=7,
                          target_source="anchored")
    written = {"done": False}
    seen = set()
    series = {m: {p: [] for p in ("A", "B", "C")}
              for m in ("I_V", "I_anchor", "I_recoverable")}
    src = {p: [] for p in ("A", "B", "C")}
    alive60, iv60_boot = {}, {}

    def maintain(t, cohort):
        if not written["done"] and t >= FROM_AGE - 1e-9:
            written["done"] = True
            for name in ("A", "B", "C"):
                _zone_write(cohort, name)
            cohort._tgt = MULTI_TARGET
            cohort._audit_on = True
        if t >= MAINT_FROM - 1e-9 \
                and abs((t - MAINT_FROM) % period) <= 0.26:
            codec.maintain(cohort, age_preset(t), mode="codec")
        for a in LEDGER_AT:
            if abs(t - a) < 0.13 and a not in seen:
                seen.add(a)
                specs = [(nm, MULTI_TARGET,
                          ZONE_MASK[(ZONES[nm][0], ZONES[nm][1])])
                         for nm in ("A", "B", "C")]
                led = cohort.pattern_ledgers(specs)
                for nm in ("A", "B", "C"):
                    for m in series:
                        series[m][nm].append(led[nm][m])
                    src[nm].append(_source_shares(
                        cohort, specs[("A", "B", "C").index(nm)][2],
                        MULTI_TARGET))
                if abs(a - 60.0) < 0.13:
                    for nm, _, zone in specs:
                        r = np.broadcast_to(MULTI_TARGET, (cohort.K, cohort.n))
                        okV = (quantize(cohort.V[:, zone], cohort.levels)
                               == quantize(r[:, zone], cohort.levels))
                        iv60_boot[nm] = okV.mean(axis=1).tolist()
                        alive60[nm] = (float(okV[cohort.alive].mean())
                                       if cohort.alive.any() else float("nan"))

    s = ch.run(years=YEARS, dt=0.25, intervention=maintain)
    i60 = int(np.argmin(np.abs(LEDGER_AT - 60.0)))

    def _at60(m, nm):
        arr = np.asarray(series[m][nm], float)
        return float(arr[i60]) if len(arr) > i60 else float("nan")

    def _src60(nm):
        arr = src[nm]
        return arr[i60] if len(arr) > i60 else {}

    out = {
        "budget": budget, "period": period,
        "n_clusters": spec.get("n_clusters", 12),
        "median": float(s["median_lifespan"]),
        "restored": int(codec.restored),
        "I_V_at_60": {nm: _at60("I_V", nm) for nm in ("A", "B", "C")},
        "I_anchor_at_60": {nm: _at60("I_anchor", nm)
                           for nm in ("A", "B", "C")},
        "alive60_IV": alive60,
        "gap60": {nm: (alive60.get(nm, float("nan"))
                       - _at60("I_V", nm)) for nm in ("A", "B", "C")},
        "src60": {nm: _src60(nm) for nm in ("A", "B", "C")},
        "src_series": {nm: list(v) for nm, v in src.items()},
        "series": {m: {nm: list(v) for nm, v in d.items()}
                   for m, d in series.items()},
        "by_group": ch._write_audit.tolist(),
    }
    ht = np.asarray(s["hist_t"], float)
    ha = np.asarray(s["hist_alive"], float)
    out["alive_frac_60"] = float(ha[np.argmin(np.abs(ht - 60.0))])
    return out


def _agg(rows: list) -> dict:
    def mm(f):
        return float(np.nanmean([f(r) for r in rows]))

    return {
        "median": mm(lambda r: r["median"]),
        "restored": mm(lambda r: r["restored"]),
        "I_V_at_60": {nm: mm(lambda r: r["I_V_at_60"][nm])
                      for nm in ("A", "B", "C")},
        "I_anchor_at_60": {nm: mm(lambda r: r["I_anchor_at_60"][nm])
                           for nm in ("A", "B", "C")},
        "alive60_IV": {nm: mm(lambda r: r["alive60_IV"][nm])
                       for nm in ("A", "B", "C")},
        "gap60": {nm: mm(lambda r: r["gap60"][nm]) for nm in ("A", "B", "C")},
        "src60": {nm: {k: mm(lambda r: r["src60"][nm].get(k, float("nan")))
                       for k in ("wrong", "senescence", "jump", "non_jump")}
                  for nm in ("A", "B", "C")},
        "alive_frac_60": mm(lambda r: r["alive_frac_60"]),
        "by_group": [float(np.mean([r["by_group"][g] for r in rows]))
                     for g in range(4)],
        "budget": rows[0]["budget"], "period": rows[0]["period"],
        "n_clusters": rows[0]["n_clusters"],
        "median_by_seed": [r["median"] for r in rows],
    }


# ------------------------------------------------------------ analysis
def _elasticities(agg: dict) -> dict:
    """Log-log elasticity of B's all-K I_V@60 per single-factor pair."""
    out = {}

    def el(lo, hi, flo, fhi):
        try:
            dv = np.log(hi) - np.log(lo)
            if dv == 0:
                return float("nan")
            return float((np.log(fhi) - np.log(flo)) / dv)
        except (ValueError, FloatingPointError):
            return float("nan")

    b = agg["default"]["I_V_at_60"]["B"]
    out["jump_rate"] = el(0.003, 0.012, agg["jr_05x"]["I_V_at_60"]["B"],
                          agg["jr_2x"]["I_V_at_60"]["B"])
    out["period"] = el(2.5, 10.0, agg["p_2_5"]["I_V_at_60"]["B"],
                       agg["p_10"]["I_V_at_60"]["B"])
    out["hazC"] = el(1.0, 4.0, agg["hazC_1"]["I_V_at_60"]["B"],
                     agg["hazC_4"]["I_V_at_60"]["B"])
    out["k_fail"] = el(0.15, 0.60, agg["kfail_lo"]["I_V_at_60"]["B"],
                       agg["kfail_hi"]["I_V_at_60"]["B"])
    out["noise"] = el(0.5, 2.0, agg["noise_lo"]["I_V_at_60"]["B"],
                      agg["noise_hi"]["I_V_at_60"]["B"])
    # budget: exp23's published curve extended by our b12 (B is the dial)
    try:
        with open(EXP23) as f:
            e23 = json.load(f)["arms"]["default"]
        bb = [e23["1"]["I_V_at_60"]["B"], e23["2"]["I_V_at_60"]["B"],
              e23["4"]["I_V_at_60"]["B"], e23["6"]["I_V_at_60"]["B"],
              agg["b12"]["I_V_at_60"]["B"]]
        out["budget"] = el(2.0, 6.0, bb[1], bb[3])
        out["budget_b6_b12"] = el(6.0, 12.0, bb[3], bb[4])
        out["budget_curve_B"] = [float(x) for x in bb]
    except (OSError, KeyError):
        pass
    return out


def main() -> dict:
    setup()
    t0 = time.time()
    _p("exp26 — EQUILIBRIUM ATTRIBUTION (what sets the death-restoration "
       "balance point)")
    _p(f"    K={K}, {YEARS:.0f}yr, seeds {SEEDS}, {len(ARMS)} arms "
       f"(exp23 geometry; default = exp23 default b6, the R anchor)")
    agg = {}
    for arm in ARMS:
        rows = [run_arm(arm, sd) for sd in SEEDS]
        agg[arm] = _agg(rows)
        e = agg[arm]
        iv = "  ".join(f"{nm} {e['I_V_at_60'][nm]:5.3f}"
                       for nm in ("A", "B", "C"))
        _p(f"    {arm:9s}: {iv}   median {e['median']:6.1f}  "
           f"restored {e['restored']:6.0f}")

    d = agg["default"]
    ivb = lambda a: agg[a]["I_V_at_60"]["B"]          # noqa: E731

    # ---- criteria --------------------------------------------------
    comp = [ivb(a) for a in ("comp_b", "comp_p", "comp4_b", "comp4_p")]
    eq1a = bool(max(comp) - min(comp) < 0.02
                and all(abs(c - ivb("default")) < 0.02 for c in comp))
    eq1b = bool(ivb("default") - ivb("jr_4x") > 0.04)
    dcp, dcb = ivb("comp_p"), ivb("comp_b")
    if abs(dcp - dcb) < 0.02:
        eq2, eq2_branch = True, "flux_equivalent"
    elif dcp - dcb > 0.03:
        eq2, eq2_branch = True, "dwell_binding (frequency beats capacity)"
    elif dcb - dcp > 0.03:
        eq2, eq2_branch = True, "capacity_binding (budget beats frequency)"
    else:
        eq2, eq2_branch = False, "ambiguous middle zone"
    gap_def = d["gap60"]["B"]
    gap_k0 = agg["kfail_0"]["gap60"]["B"]
    eq3 = bool(gap_k0 < 0.5 * gap_def)
    arch = {a: ivb(a) for a in ("arch4", "default", "arch20")}
    arch_d = [abs(arch["arch4"] - arch["default"]),
              abs(arch["arch20"] - arch["default"]),
              abs(arch["arch20"] - arch["arch4"])]
    arch_ordered = bool(arch["arch20"] > arch["default"] > arch["arch4"]
                        or arch["arch20"] < arch["default"] < arch["arch4"])
    if max(arch_d) < 0.02:
        eq4, eq4_branch = True, "(a) architecture-INVARIANT (flux-ratio object)"
    elif arch_ordered and max(arch_d) > 0.046:
        eq4, eq4_branch = True, "(b) architecture is a PRIMARY lever"
    else:
        eq4, eq4_branch = False, "ambiguous middle zone"
    share_jump = d["src60"]["B"]["jump"]
    pred = share_jump * (1.0 - POT_FACTOR) * POT_PERM_COVERAGE
    eq5 = bool(abs(pred - POT_PERM_DELTA_B) < 0.01)
    eq6 = bool(abs(ivb("hazC_8") - ivb("default")) < 0.01)
    with open(EXP23) as f:
        e23 = json.load(f)["arms"]["default"]["6"]
    r_ok = all(abs(d["I_V_at_60"][nm] - e23["I_V_at_60"][nm]) < 0.005
               for nm in ("A", "B", "C")) \
        and abs(d["median"] - e23["median"]) < 0.5 \
        and d["restored"] == e23["restored"]

    crit = {
        "EQ1a_compensation": eq1a,
        "EQ1b_stress": eq1b,
        "EQ2_routes": eq2,
        "EQ2_branch": eq2_branch,
        "EQ3_selection_share": eq3,
        "EQ4_architecture": eq4,
        "EQ4_branch": eq4_branch,
        "EQ5_potentiation_closure": eq5,
        "EQ6_modularity": eq6,
        "R_regression_vs_exp23": bool(r_ok),
    }
    results = {
        "exp": "exp26_equilibrium",
        "arms": agg,
        "criteria": crit,
        "elasticities": _elasticities(agg),
        "phi_note": "Phi = jump_rate*cluster_len*sum_mult / (budget/period); "
                    "default 0.34; comp arms hold it at 0.34",
        "potentiation_closure": {
            "share_jump_B": share_jump,
            "predicted_delta": float(pred),
            "observed_delta": POT_PERM_DELTA_B,
            "coverage": POT_PERM_COVERAGE,
        },
        "architecture_note": "n_clusters 4/12/20 -> cluster_len 15/5/3; "
                             "per-cell jump flux is analytically invariant "
                             "across the three (see module docstring)",
        "src60_default": d["src60"],
        "gap60_note": {"default_B": gap_def, "kfail0_B": gap_k0,
                       "mk_lo_B": agg["mk_lo"]["gap60"]["B"]},
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=1)
    for k, v in crit.items():
        if isinstance(v, bool):
            _p(f"    {k}: {'PASS' if v else 'NEGATIVE'}")
        else:
            _p(f"    {k}: {v}")
    _p(f"    potentiation closure: share_jump(B)={share_jump:.4f} -> "
       f"pred {pred:+.4f} vs observed {POT_PERM_DELTA_B:+.4f}")
    _p(f"    elasticities: "
       + "  ".join(f"{k}={v:+.2f}" if np.isfinite(v) else f"{k}=n/a"
                   for k, v in results["elasticities"].items()
                   if not isinstance(v, list)))
    _figure(results)
    _p(f"exp26 complete in {time.time()-t0:.0f}s")
    return results


# --------------------------------------------------------------- figure
def _figure(results: dict) -> None:
    setup()
    agg = results["arms"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6),
                           constrained_layout=True)

    # (a) the lever table: B's I_V@60 across single-factor arms
    order = ["jr_025x", "jr_05x", "default", "jr_2x", "jr_4x",
             "b12", "p_2_5", "p_10", "hazC_1", "hazC_4", "hazC_8",
             "kfail_0", "kfail_hi", "mk_lo", "noise_lo", "noise_hi",
             "arch4", "arch20"]
    vals = [agg[a]["I_V_at_60"]["B"] for a in order]
    colors = [PALETTE["accent"] if a != "default" else PALETTE["good"]
              for a in order]
    ax[0].bar(range(len(order)), vals, color=colors)
    ax[0].axhline(agg["default"]["I_V_at_60"]["B"], color="0.3", lw=1,
                  ls=":", zorder=0)
    ax[0].set_xticks(range(len(order)))
    ax[0].set_xticklabels(order, rotation=60, fontsize=7, ha="right")
    ax[0].set(ylabel="B I_V@60 (all-K)", ylim=(0, 1.02),
              title="the lever table — what moves the volatile pattern")

    # (b) Phi compensation: default vs the four Phi-equal arms
    names = ["default", "jr_2x", "jr_4x", "comp_b", "comp_p",
             "comp4_b", "comp4_p"]
    bs = [agg[a]["I_V_at_60"]["B"] for a in names]
    cols = [PALETTE["good"], "0.7", "0.5", PALETTE["accent"],
            PALETTE["accent"], "#b58900", "#b58900"]
    ax[1].bar(range(len(names)), bs, color=cols)
    ax[1].axhline(agg["default"]["I_V_at_60"]["B"], color="0.3", lw=1,
                  ls=":")
    ax[1].set_xticks(range(len(names)))
    ax[1].set_xticklabels(names, rotation=45, fontsize=8, ha="right")
    ax[1].set(ylabel="B I_V@60", ylim=(0, 1.02),
              title="Phi-equal compensation (dotted = default balance point)")

    # (c) corruption-source decomposition at 60, per zone
    zones = ("A", "B", "C")
    keys = ("senescence", "jump", "non_jump")
    labels = ("senescence", "jump", "non-jump")
    colr = (PALETTE["accent"], "#d33682", "0.6")
    bottom = np.zeros(3)
    for k, lb, c in zip(keys, labels, colr):
        v = np.array([results["src60_default"][z][k] for z in zones])
        ax[2].bar(range(3), v, bottom=bottom, color=c, label=lb)
        bottom += v
    ax[2].bar(range(3), 1.0 - bottom, color=PALETTE["good"],
              label="correct")
    ax[2].set_xticks(range(3))
    ax[2].set_xticklabels([f"{z}\n(gap {agg['default']['gap60'][z]:+.3f})"
                           for z in zones])
    ax[2].set(ylabel="fraction of zone cells", ylim=(0, 1.0),
              title="corruption sources @60 + selection gap (alive-allK)")
    ax[2].legend(fontsize=8, loc="lower right")
    fig.savefig(fig_path("fig26_equilibrium"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    main()
