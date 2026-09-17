#!/usr/bin/env python3
"""exp177 — THE GRID RESIDUAL DECOMPOSITION (what R_T cannot reach).

exp169's registered next (L148 (ii)): the schedule grid classifies
ALL-DIFFUSE at T=32, so the scoped read is exp167's adopted read
everywhere on the grid and the pooled median stands at 0.68 mV —
N3's 0.60 bar is never reached by R_T there. "The temporal channel's
remaining excess is NOT flip-clock: price it." THIS EXPERIMENT
decomposes the grid's residual.

========================= PRE-REGISTRATION =========================
Committed BEFORE any decode. Channels, decomposition, and gates are
fixed now; the credited run uses this file unchanged.

THE RESIDUAL (defined once): per grid instance i (exp148's schedule
grid, 20 instances = 8 x n=100 + 2 x n=400 per class x 2 classes...
the deposited instance set of exp169's S4), residual
  r_i = scoped_err_i - N3_BAR (0.60),
where scoped_err_i = the instance's median decode err under the
scoped read (exp169's deposited per-instance records — replayed
bit-exactly first, then decomposed; NO new decodes for the replay).

THE CHANNEL CENSUS (zero knobs, pre-registered channel list): per
instance, the structural features computable from the medium ALONE:
  (c1) schedule class (per | aper) — one-hot;
  (c2) n (100 | 400);
  (c3) T (the window length, T_GRID);
  (c4) flip mass m_i = total presence transitions across the window;
  (c5) support size |sup_i| and its DENSITY (edges / n^2);
  (c6) support ASYMMETRY a_i = ||sup - sup^T||_0 / |sup|_0 (the
       oriented dimension's footprint — exp160's A-SYM class);
  (c7) the frame-diversity d_i = mean pairwise Jaccard distance
       between frame supports (temporal dimension's footprint).
  THE DECOMPOSITION: Spearman rank correlation of each feature with
  r_i across the instance set, deposited per class and pooled; the
  DOMINANT channel = the feature with the largest |rho| at
  |rho| >= 0.5 (a pre-named threshold, not a fit); if no feature
  reaches 0.5, the residual is declared UNATTRIBUTED at this census
  and the deposit says so (that is a completed answer, not a
  failure — it registers the next instrument).

CANDIDATE REPAIR (priced ONLY IF a dominant channel fires, zero
  knobs): the mapped rule from exp166's RULE_MAP for the dominant
  feature's dimension (asymmetry -> R_O one-way restore; density ->
  R_H cancellation-weighted S; frame-diversity -> R_T is already
  active, so frame-diversity dominance registers the gap instead of
  pricing a rule). The mapped rule runs on the instances in the
  dominant feature's TOP TERcile (the pre-registered slice), spot
  scale (3 seeds), and the delta median deposited. No adoption
  claim — pricing only.

INSTRUMENTS (zero new calibration):
  * exp148's module verbatim (the grid constructors, T_GRID,
    GRID_CLASSES, GRID_BASE_SEED, N_INSTANCES, N_INSTANCES_400);
  * exp169's deposit results/exp169_rt_scoping.json (the per-
    instance scoped records — the replay source);
  * the -35.0 instrument pin (exp167's mechanism) for any decode;
  * seeds (1, 2, 3) for the candidate-repair spot runs.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-R1 (replay) the grid scoped errs replay exp169's S4 records
           bit-exactly (per instance, per seed) — the decomposition
           runs on the deposited errs, zero new decodes for this
           gate.
  GATE-R2 (the census is complete) all seven features computed for
           all instances, no NaN, the Spearman table deposited per
           class and pooled (the table IS the deliverable).
  GATE-R3 (the verdict clause) a dominant channel is NAMED at
           |rho| >= 0.5, OR the residual is deposited UNATTRIBUTED
           at this census. Both branches complete the gate; the
           branch taken is the finding.
  GATE-R4 (hygiene) zero rejections in any decode performed; pin
           save/restore asserted.

NO post-hoc knob tuning; the census is fixed. A --smoke check (1
instance per class, features only) is permitted before the credited
run and discarded.

DEPOSIT: results/exp177_grid_residual.json

RUN:
  python3 -m experiments.exp177_grid_residual            # full
  python3 -m experiments.exp177_grid_residual --smoke    # check
  python3 -m experiments.exp177_grid_residual --job census
  # jobs: replay | census | repair
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from experiments.exp148_temporal_read import (  # noqa: E402
    FlipGridMedium, GRID_BASE_SEED, GRID_CLASSES, N_INSTANCES,
    N_INSTANCES_400, T_GRID,
)
from experiments.exp169_rt_scoping import (  # noqa: E402
    THRESHOLD, f_max_frames, scoped_read,
)

# ---- INSTRUMENT PIN -------------------------------------------------
import cultivation.bioelectric.collective as _core_mod   # noqa: E402
import experiments.exp142_sign_read as _m142             # noqa: E402
import experiments.exp145_phase_read as _m145            # noqa: E402
import experiments.exp148_temporal_read as _m148         # noqa: E402
import experiments.exp94_multizone_scale as _m94         # noqa: E402

DEP169_FLOOR = -35.0
PIN_MODULES = (_core_mod, _m142, _m145, _m148, _m94)
_PIN_SAVE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
             for m in PIN_MODULES}


def pin_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = DEP169_FLOOR


def restore_floor() -> None:
    for m in PIN_MODULES:
        if hasattr(m, "NEURAL_SPEC_MIN"):
            m.NEURAL_SPEC_MIN = _PIN_SAVE[m.__name__]


RHO_BAR = 0.5                   # the pre-named dominance threshold
OUT = os.path.join(ROOT, "results", "exp177_grid_residual.json")
DEP169 = os.path.join(ROOT, "results", "exp169_rt_scoping.json")


# ---- BODY (written by the run agent; the gates above are fixed) -----
#
# The docstring mandates "Spearman via scipy.stats if available else
# rank-correlation by hand" — the conditional import below IS that
# clause; the pre-registered import block above is untouched.
try:
    from scipy.stats import spearmanr as _scipy_spearmanr
    SPEARMAN_IMPL = "scipy.stats.spearmanr"
except Exception:                                       # pragma: no cover
    _scipy_spearmanr = None
    SPEARMAN_IMPL = "hand_rank_pearson(avg_ties)"

N3_BAR = 0.60       # the residual's bar (exp148's deposited N3 bar)

# THE CHANNEL CENSUS columns: family (c1-c7), the feature's dimension
# (exp166's RULE_MAP dimensions: hyper/oriented/temporal — c2's n is
# the SCALE dimension, exp94's instrument), description. c5 carries
# BOTH pre-registered columns (size and its density).
FEATURE_COLUMNS = (
    ("c1_class_per", "c1", "temporal",
     "schedule class one-hot (per=1, aper=0; with two classes the "
     "single indicator is the full one-hot rank space)"),
    ("c2_n", "c2", "scale", "n (100 | 400)"),
    ("c3_T", "c3", "temporal", "window length T (T_GRID)"),
    ("c4_flip_mass", "c4", "temporal",
     "flip mass m_i: total presence transitions across the window "
     "(exp148's TC1 flip-clock matrix, undirected total)"),
    ("c5_support_size", "c5", "density",
     "support size |sup_i| (directed nonzero entries)"),
    ("c5_support_density", "c5", "density",
     "support density: edges / n^2"),
    ("c6_support_asymmetry", "c6", "oriented",
     "||sup - sup^T||_0 / |sup|_0 (exp160's A-SYM footprint)"),
    ("c7_frame_diversity", "c7", "temporal",
     "mean pairwise Jaccard distance between frame supports"),
)

# The pre-registered repair mapping (docstring): the mapped rule from
# exp166's RULE_MAP for the dominant feature's dimension. R_T — the
# temporal dimension's rule — is ALREADY ACTIVE on every grid instance
# (all diffuse -> exp167's adopted read), so temporal dominance
# registers the gap; the scale dimension carries no rule in exp166's
# RULE_MAP, so scale dominance registers the gap too.
DIMENSION_RULE = {"density": "hyper", "oriented": "oriented",
                  "temporal": None, "scale": None}


def _grid_instances(smoke: bool) -> list[dict]:
    """The deposited instance set, built EXACTLY as exp169's S4 section
    builds it (its pass-1 loop VERBATIM): for cls_name, sched in
    GRID_CLASSES.items(), i in range(N_INSTANCES + N_INSTANCES_400),
    n = 400 if i >= N_INSTANCES else 100, FlipGridMedium(n,
    seed=GRID_BASE_SEED + i, sched=sched); the instance's f_max via
    exp169's f_max_frames on the raw frames."""
    inst_range = list(range(1)) if smoke else \
        list(range(N_INSTANCES + N_INSTANCES_400))
    out = []
    for cls_name, sched in GRID_CLASSES.items():
        for i in inst_range:
            n = 400 if i >= N_INSTANCES else 100
            med = FlipGridMedium(n, seed=GRID_BASE_SEED + i, sched=sched)
            out.append({"cls": cls_name, "i": i, "n": n,
                        "gen_seed": GRID_BASE_SEED + i, "sched": sched,
                        "med": med,
                        "f_max": f_max_frames(list(med.snapshots()))})
    return out


def _features(med) -> dict:
    """THE CHANNEL CENSUS — c1-c7 computed from the medium ALONE (no
    decode, no outcome feedback, zero knobs)."""
    frames = list(med.snapshots())
    n = int(med.M.shape[0])
    sup = med.native_support() > 0            # the instance's support
    size = float(np.count_nonzero(sup))
    dens = size / float(n * n)                # (c5) edges / n^2
    # (c6) support asymmetry, exp160's A-SYM formula
    asym = (float(np.count_nonzero(sup != sup.T)) / size) if size else 0.0
    # (c4) flip mass via exp148's TC1 flip_clock_matrix VERBATIM (the
    # symmetric per-edge presence-transition counts; the undirected
    # total = the strict upper triangle's sum)
    F = _m148.flip_clock_matrix(med)
    mass = float(np.triu(F, 1).sum())
    # (c7) frame diversity: mean pairwise Jaccard distance between
    # frame supports (edge sets; the masks are symmetric)
    bools = [(np.abs(W) > 0).ravel() for W in frames]
    jds = []
    for a in range(len(bools)):
        for b in range(a + 1, len(bools)):
            inter = int(np.logical_and(bools[a], bools[b]).sum())
            union = int(np.logical_or(bools[a], bools[b]).sum())
            jds.append(1.0 - inter / union)
    return {"c1_class_per": 1.0 if med.sched == "per" else 0.0,
            "c2_n": float(n),
            "c3_T": float(med.T),
            "c4_flip_mass": mass,
            "c5_support_size": size,
            "c5_support_density": dens,
            "c6_support_asymmetry": asym,
            "c7_frame_diversity": float(np.mean(jds))}


def _avg_ranks(xs: list[float]) -> list[float]:
    """Average ranks (ties share the mean rank) — the hand fallback."""
    order = sorted(range(len(xs)), key=lambda k: xs[k])
    ranks = [0.0] * len(xs)
    a = 0
    while a < len(order):
        b = a
        while b + 1 < len(order) and xs[order[b + 1]] == xs[order[a]]:
            b += 1
        r = (a + b) / 2.0 + 1.0
        for k in range(a, b + 1):
            ranks[order[k]] = r
        a = b + 1
    return ranks


def _pearson(xs: list[float], ys: list[float]):
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    dx = [x - mx for x in xs]
    dy = [y - my for y in ys]
    sxx = sum(v * v for v in dx)
    syy = sum(v * v for v in dy)
    if sxx == 0.0 or syy == 0.0:
        return None
    return sum(u * v for u, v in zip(dx, dy)) / (sxx * syy) ** 0.5


def _spearman(xs: list, ys: list) -> tuple:
    """Spearman rank correlation of x with y: scipy.stats when
    available, else the identical construction (average ranks, Pearson
    of the ranks). A constant side has an UNDEFINED rho — returned as
    (None, None, constant=True); the deposit carries null, never NaN."""
    if not xs or len(xs) != len(ys):
        raise ValueError("spearman length mismatch")
    if min(xs) == max(xs) or min(ys) == max(ys):
        return None, None, True
    if _scipy_spearmanr is not None:
        out = _scipy_spearmanr(xs, ys)
        return float(out.statistic), float(out.pvalue), False
    rx, ry = _avg_ranks([float(x) for x in xs]), \
        _avg_ranks([float(y) for y in ys])
    return _pearson(rx, ry), None, False


# ------------------------------------------------------------ sections
def _section_replay() -> tuple[dict, dict]:
    """GATE-R1: the grid scoped errs replay exp169's S4 records
    bit-exactly (per instance, per seed). The instance set is rebuilt
    exactly as S4 builds it; the identity table (cls, i, n, gen_seed,
    f_max, scoping class) is asserted against the deposit; the
    per-seed scoped errs ARE the deposited records (zero new decodes);
    the pooled median must reproduce the deposited pooled median
    bit-exactly."""
    with open(DEP169) as f:
        dep = json.load(f)
    s4 = dep["sections"]["grid"]
    recs = s4["instances"]
    built = _grid_instances(False)
    assert len(recs) == len(GRID_CLASSES) * (N_INSTANCES + N_INSTANCES_400)
    assert len(built) == len(recs), "instance set shape mismatch"
    rows, ok = [], True
    for b, r in zip(built, recs):
        ident = (b["cls"] == r["cls"] and b["i"] == r["i"]
                 and b["n"] == r["n"]
                 and b["gen_seed"] == r["gen_seed"]
                 and b["f_max"] == r["f_max"]
                 and ("diffuse" if b["f_max"] < THRESHOLD
                      else "concentrated") == r["class"])
        errs = r.get("errs_scoped")
        errs_ok = (isinstance(errs, list)
                   and all(e is not None and np.isfinite(e) for e in errs))
        ok = ok and ident and errs_ok
        rows.append({"cls": b["cls"], "i": b["i"], "n": b["n"],
                     "gen_seed": b["gen_seed"], "f_max": b["f_max"],
                     "identity_bit_exact": bool(ident),
                     "errs_ok": bool(errs_ok),
                     "errs_scoped_replayed": [float(e) for e in errs],
                     "scoped_median": float(np.median(errs))})
    errs_all = [e for row in rows for e in row["errs_scoped_replayed"]]
    pooled = float(np.median(errs_all))
    gate = {"pass": bool(ok and pooled == s4["pooled_scoped_median"]
                         and len(errs_all) == len(recs) * 3),
            "identity_all_bit_exact": bool(ok),
            "pooled_median_replayed": pooled,
            "pooled_median_deposited": s4["pooled_scoped_median"],
            "pooled_median_bit_exact":
                bool(pooled == s4["pooled_scoped_median"]),
            "n_instances": len(rows), "n_errs": len(errs_all),
            "decodes_performed": 0,
            "zero_rejections": True, "rejections": 0}
    section = {"instances": rows,
               "pooled_scoped_median_replayed": pooled,
               "decodes_performed": 0, "rejections": 0, "runtime_s": 0.0}
    return section, gate


def _section_census() -> tuple[dict, dict, dict]:
    """GATE-R2 (census complete) + GATE-R3 (the verdict clause): all
    seven feature families computed for all instances from the media
    alone; the Spearman table deposited per class and pooled; the
    DOMINANT channel = the pooled feature with the largest |rho| at
    |rho| >= RHO_BAR, else UNATTRIBUTED (both branches complete R3)."""
    with open(DEP169) as f:
        dep = json.load(f)
    recs = {(r["cls"], r["i"]): r
            for r in dep["sections"]["grid"]["instances"]}
    built = _grid_instances(False)
    rows, finite_ok = [], True
    for b in built:
        errs = recs[(b["cls"], b["i"])]["errs_scoped"]
        scoped_median = float(np.median(errs))
        feats = _features(b["med"])
        finite_ok = finite_ok and all(bool(np.isfinite(v))
                                      for v in feats.values())
        rows.append({"cls": b["cls"], "i": b["i"], "n": b["n"],
                     "gen_seed": b["gen_seed"], "f_max": b["f_max"],
                     "errs_scoped_replayed": [float(e) for e in errs],
                     "scoped_median": scoped_median,
                     "residual": scoped_median - N3_BAR,
                     "features": feats})
    # the schedule channel is structurally silent under the scoped read
    # if the paired classes replay bit-identical errs (deposit detail)
    per_rows = [r for r in rows if r["cls"] == "flip_per"]
    aper_rows = [r for r in rows if r["cls"] == "flip_aper"]
    paired_identical = all(
        p["errs_scoped_replayed"] == q["errs_scoped_replayed"]
        for p, q in zip(per_rows, aper_rows))

    scopes = {}
    for scope, sel in (("flip_per", per_rows), ("flip_aper", aper_rows),
                       ("pooled", rows)):
        table = []
        for name, fam, dim, desc in FEATURE_COLUMNS:
            xs = [r["features"][name] for r in sel]
            ys = [r["residual"] for r in sel]
            rho, p, const = _spearman(xs, ys)
            table.append({"feature": name, "family": fam,
                          "dimension": dim, "description": desc,
                          "rho": rho, "p": p, "constant": bool(const),
                          "n": len(sel)})
        scopes[scope] = table

    cand = [t for t in scopes["pooled"] if t["rho"] is not None]
    ranked = sorted(cand, key=lambda t: -abs(t["rho"]))
    dominant = ranked[0] if ranked and abs(ranked[0]["rho"]) >= RHO_BAR \
        else None
    runner_up = ranked[1] if len(ranked) > 1 else None

    table_ok = (len(scopes) == 3
                and all(len(t) == len(FEATURE_COLUMNS)
                        for t in scopes.values())
                and all(t["rho"] is None or np.isfinite(t["rho"])
                        for t in scopes["pooled"]))
    gate_r2 = {"pass": bool(finite_ok and table_ok),
               "features_finite_all_instances": bool(finite_ok),
               "n_instances": len(rows),
               "n_feature_columns": len(FEATURE_COLUMNS),
               "n_feature_families": 7,
               "tables_deposited": ["flip_per", "flip_aper", "pooled"],
               "table_complete": bool(table_ok),
               "spearman_impl": SPEARMAN_IMPL,
               "no_nan_deposited": True}
    if dominant is not None:
        branch = {"named": True, "unattributed": False,
                  "feature": dominant["feature"],
                  "family": dominant["family"],
                  "dimension": dominant["dimension"],
                  "rho": dominant["rho"], "p": dominant["p"],
                  "abs_rho": abs(dominant["rho"]),
                  "threshold": RHO_BAR,
                  "runner_up": (None if runner_up is None else
                                {"feature": runner_up["feature"],
                                 "rho": runner_up["rho"]})}
    else:
        branch = {"named": False, "unattributed": True,
                  "threshold": RHO_BAR,
                  "max_abs_rho_pooled":
                      (abs(ranked[0]["rho"]) if ranked else None),
                  "best_feature_pooled":
                      (ranked[0]["feature"] if ranked else None)}
    gate_r3 = {"pass": True, "branch": branch,
               "clause": ("a dominant channel is NAMED at |rho| >= 0.5, "
                          "OR the residual is deposited UNATTRIBUTED; "
                          "both branches complete the gate; the branch "
                          "taken is the finding"),
               "paired_outcomes_bit_identical": bool(paired_identical)}
    section = {"instances": rows, "tables": scopes, "dominant": dominant,
               "runner_up": runner_up, "unattributed": dominant is None,
               "paired_outcomes_bit_identical": bool(paired_identical),
               "spearman_impl": SPEARMAN_IMPL, "runtime_s": 0.0}
    return section, gate_r2, gate_r3


class _GridAdapter:
    """Exposes what exp166's repair machinery needs from a
    FlipGridMedium (which carries no .n/.hyperedges/.violated): n,
    snapshots(), hyperedges = [] (grid media carry NO hyperedges ->
    R_H's S = 0, the bit-exact identity) and violated (absent -> ())."""

    def __init__(self, med):
        self.med = med
        self.n = int(med.M.shape[0])
        self.hyperedges = []

    @property
    def violated(self):
        return getattr(self.med, "violated", ())

    def snapshots(self):
        return self.med.snapshots()


def _section_repair(census: dict) -> tuple[dict, int, int]:
    """CANDIDATE REPAIR — priced ONLY IF a dominant channel fired
    (zero knobs): the mapped rule from exp166's RULE_MAP for the
    dominant feature's dimension, on the dominant feature's TOP-TERCILE
    slice, spot scale (seeds 1, 2, 3), delta median deposited. No
    adoption claim — pricing only. Returns (section, rejections,
    n_decodes)."""
    dom = census.get("dominant")
    if dom is None:
        return ({"priced": False, "gap_registered": False,
                 "reason": ("UNATTRIBUTED at this census (no pooled "
                            "|rho| >= 0.5): the candidate repair is "
                            "not priced — the pre-registered clause "
                            "prices only on a named dominant channel")},
                0, 0)
    dim = dom["dimension"]
    rule = DIMENSION_RULE[dim]
    if rule is None:
        if dim == "temporal":
            reason = ("R_T (exp166's RULE_MAP temporal rule) is already "
                      "active on every grid instance (all diffuse -> "
                      "exp167's adopted read): the gap is registered "
                      "instead of pricing a rule")
        else:
            reason = ("no rule in exp166's RULE_MAP maps the scale "
                      "dimension (n): the mapped-rule clause prices "
                      "only asymmetry->R_O and density->R_H; the gap "
                      "is registered")
        return ({"priced": False, "gap_registered": True,
                 "dominant_feature": dom["feature"],
                 "dimension": dim, "reason": reason}, 0, 0)

    from experiments.exp166_leading_edge import (   # noqa: E402
        RepairedMedium, RULE_MAP_DOC, pooled_F, rule_hyper_S,
        rule_oriented_restore)

    built = _grid_instances(False)
    with open(DEP169) as f:
        dep = json.load(f)
    recs = {(r["cls"], r["i"]): r
            for r in dep["sections"]["grid"]["instances"]}
    key = dom["feature"]
    feats = [_features(b["med"]) for b in built]
    order = sorted(range(len(built)),
                   key=lambda k: (-feats[k][key], k))
    k_top = -(-len(order) // 3)                  # ceil tercile (7 of 20)
    slice_idx = order[:k_top]
    adapters = [(k, _GridAdapter(built[k]["med"])) for k in slice_idx]
    # the rule's single statistic, computed BEFORE any decode (exp166's
    # zero-knob F: pooled median nonzero |W| over the slice's frames)
    F = pooled_F([ad for _, ad in adapters]) if rule == "hyper" else None

    rows, rejections, decodes = [], 0, 0
    for k, ad in adapters:
        b = built[k]
        frames = list(b["med"].snapshots())
        if rule == "hyper":
            # grid media carry no hyperedges -> S = 0 -> the bit-exact
            # identity on this medium class (exp166's rule VERBATIM)
            fixed = rule_hyper_S(ad, frames, F)
        else:
            fixed = rule_oriented_restore(ad, frames)
        wrapped = RepairedMedium(ad, fixed, rule)
        errs_b, vs_b = [], []
        for s in (1, 2, 3):
            out = scoped_read(wrapped, s, b["f_max"])
            decodes += 1
            if not out["ok"]:
                rejections += 1
            errs_b.append(out.get("err"))
            vs_b.append(bool(out.get("verified", False)))
        errs_scoped = [float(e) for e in recs[(b["cls"], b["i"])]
                       ["errs_scoped"]]
        med_b = float(np.median(errs_b))
        rows.append({"cls": b["cls"], "i": b["i"], "n": b["n"],
                     "gen_seed": b["gen_seed"],
                     "feature_value": feats[k][key],
                     "errs_scoped": errs_scoped,
                     "errs_armB": [float(e) for e in errs_b],
                     "verified_armB": vs_b,
                     "median_armB": med_b,
                     "scoped_median": float(np.median(errs_scoped)),
                     "delta": med_b - float(np.median(errs_scoped)),
                     "bit_identical_to_scoped":
                         bool(errs_b == errs_scoped)})
    deltas = [r["delta"] for r in rows]
    section = {"priced": True, "gap_registered": False,
               "rule": rule, "rule_description": RULE_MAP_DOC[rule],
               "dominant_feature": key, "dimension": dim,
               "tercile_rule": ("top ceil(N/3) instances by the "
                                "dominant feature's value (ties by "
                                "deposit order)"),
               "slice_size": k_top, "seeds": [1, 2, 3],
               "read": ("exp169's scoped_read (the active read) on the "
                        "mapped-rule-wrapped medium"),
               "F_pooled_median_nonzero_absW": F,
               "S_note": ("grid media carry no hyperedges -> S = 0 -> "
                          "R_H is the bit-exact identity on this "
                          "medium class") if rule == "hyper" else None,
               "slice": rows,
               "delta_median": float(np.median(deltas)),
               "delta_definition": ("median_armB - scoped_median "
                                    "(negative = the repair improves)"),
               "n_decodes": decodes, "rejections": rejections}
    return section, rejections, decodes


# ---------------------------------------------------------------- main
def main() -> dict:
    # the pre-registered __main__ block parses --smoke/--job/--out into
    # the module-level `args`; honor it (defaults for direct calls)
    a = globals().get("args")
    smoke = bool(getattr(a, "smoke", False))
    job = getattr(a, "job", "all") or "all"
    out_path = getattr(a, "out", None) or OUT
    t0 = os.times()[4]
    assert _m148.N3_BAR == N3_BAR, "N3 bar drifted from exp148's deposit"
    jobs = ["replay", "census", "repair"] if job == "all" else [job]
    mode = ("SMOKE instrument check (1 instance per class, features "
            "only) - discarded" if smoke else
            "FULL jobs=" + ",".join(jobs))
    print(f"=== exp177: THE GRID RESIDUAL DECOMPOSITION ({mode}) ===\n")

    # ---- instrument pin (restored-world semantics, save/restore) ----
    _saved = dict(_PIN_SAVE)
    pin_floor()
    assert all(getattr(m, "NEURAL_SPEC_MIN", None) == DEP169_FLOOR
               for m in PIN_MODULES), "instrument pin to -35.0 failed"
    print(f"  pin: NEURAL_SPEC_MIN = {DEP169_FLOOR} on "
          f"{[m.__name__ for m in PIN_MODULES]}\n")

    if smoke:
        for b in _grid_instances(True):
            f = _features(b["med"])
            assert all(np.isfinite(v) for v in f.values()), \
                f"non-finite feature in smoke: {f}"
            print(f"  [{b['cls']} i={b['i']} n={b['n']} "
                  f"f_max={b['f_max']}] "
                  + " ".join(f"{k}={v:.6g}" for k, v in f.items()))
        restore_floor()
        assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                   == _saved[m.__name__] for m in PIN_MODULES), \
            "smoke pin restore failed"
        print("\n  SMOKE check OK (features only) — discarded, no "
              "deposit, no gates.")
        return {"smoke": True, "discarded": True}

    # merged deposit: split runs accumulate sections across invocations
    result: dict = {}
    if job != "all" and os.path.exists(out_path):
        with open(out_path) as f:
            result = json.load(f)
    result.setdefault("sections", {})
    result.setdefault("gates", {})

    rejections = decodes = 0
    if "replay" in jobs:
        ts = os.times()[4]
        section, gate = _section_replay()
        section["runtime_s"] = round(os.times()[4] - ts, 1)
        result["sections"]["replay"] = section
        result["gates"]["R1_replay"] = gate
        print(f"  [replay] R1_replay pass={gate['pass']} "
              f"({section['runtime_s']} s, decodes 0)")
    if "census" in jobs:
        ts = os.times()[4]
        section, gate_r2, gate_r3 = _section_census()
        section["runtime_s"] = round(os.times()[4] - ts, 1)
        result["sections"]["census"] = section
        result["gates"]["R2_census_complete"] = gate_r2
        result["gates"]["R3_verdict"] = gate_r3
        br = gate_r3["branch"]
        name = br["feature"] if br["named"] else "UNATTRIBUTED"
        rho = br.get("rho") if br["named"] else br.get("max_abs_rho_pooled")
        print(f"  [census] R2 pass={gate_r2['pass']} "
              f"R3 branch={'dominant' if br['named'] else 'unattributed'}"
              f" ({section['runtime_s']} s)")
        print(f"    verdict: dominant channel = {name}"
              + (f" (pooled rho={rho:+.4f})" if rho is not None else ""))
    if "repair" in jobs:
        ts = os.times()[4]
        section, rej, dec = _section_repair(result["sections"]["census"])
        section["runtime_s"] = round(os.times()[4] - ts, 1)
        rejections += rej
        decodes += dec
        result["sections"]["repair"] = section
        print(f"  [repair] priced={section['priced']} "
              f"gap_registered={section['gap_registered']} "
              f"({section['runtime_s']} s, decodes {dec})")

    # ---- pin restore + GATE-R4 (hygiene) -----------------------------
    restore_floor()
    pin_ok = all(getattr(m, "NEURAL_SPEC_MIN", None)
                 == _saved[m.__name__] for m in PIN_MODULES)
    assert pin_ok, "pin save/restore failed"
    result["gates"]["R4_hygiene"] = {
        "pass": bool(rejections == 0 and pin_ok),
        "rejections": rejections, "decodes_performed": decodes,
        "zero_rejections": bool(rejections == 0),
        "pin": {"floor": DEP169_FLOOR, "save_restore_asserted": bool(pin_ok),
                "modules": [m.__name__ for m in PIN_MODULES]}}
    print(f"  [hygiene] R4 pass={result['gates']['R4_hygiene']['pass']} "
          f"(rejections {rejections}, pin save/restore asserted)")

    n_pass = sum(int(g["pass"]) for g in result["gates"].values())
    census = result["sections"].get("census", {})
    br = result["gates"].get("R3_verdict", {}).get("branch", {})
    rep = result["sections"].get("repair", {})
    if br.get("named"):
        head = (f"dominant channel {br['feature']} "
                f"({br['dimension']} dimension, pooled rho="
                f"{br['rho']:+.4f} >= {RHO_BAR})")
    else:
        head = "UNATTRIBUTED at this census"
    tail = ("the gap is registered (no candidate repair priced)"
            if not rep.get("priced") else
            f"mapped rule {rep['rule']} priced on the top tercile, "
            f"delta median {rep['delta_median']:+.4f}")
    one_line = f"the grid residual (r_i = scoped_err_i - {N3_BAR}): " \
               f"{head}; {tail}."
    print(f"\n  GATES: {n_pass}/{len(result['gates'])}  "
          + " ".join(f"{k.split('_')[0]}={int(g['pass'])}"
                     for k, g in result["gates"].items()))
    print(f"  VERDICT: {one_line}")

    result.update({
        "exp": "exp177_grid_residual",
        "claim": (
            "exp169's registered next (L148 (ii)): the schedule grid "
            "classifies ALL-DIFFUSE at T=32, so the scoped read is "
            "exp167's adopted read everywhere on the grid and the "
            "pooled median stands at 0.68 mV - N3's 0.60 bar is never "
            "reached by R_T there. THIS EXPERIMENT decomposes the "
            "grid's residual r_i = scoped_err_i - 0.60 over the "
            "pre-registered seven-feature channel census (media alone, "
            "zero knobs): Spearman per class and pooled; the dominant "
            "channel named at |rho| >= 0.5 OR UNATTRIBUTED; the "
            "candidate repair priced only on a named dominant "
            "channel's top tercile (no adoption claim). The errs are "
            "exp169's deposited S4 records replayed bit-exactly "
            "(GATE-R1, zero new decodes)."),
        "pre_registration": {
            "rho_bar": RHO_BAR, "n3_bar": N3_BAR,
            "residual": "r_i = scoped_err_i - 0.60 (scoped_err_i = the "
                        "instance's median decode err under the scoped "
                        "read, exp169's deposited S4 records)",
            "features": [c[0] for c in FEATURE_COLUMNS],
            "repair_map": DIMENSION_RULE,
            "gates": ["R1_replay", "R2_census_complete", "R3_verdict",
                      "R4_hygiene"]},
        "config": {
            "instances": N_INSTANCES + N_INSTANCES_400,
            "n_instances": N_INSTANCES, "n_instances_400": N_INSTANCES_400,
            "grid_classes": dict(GRID_CLASSES),
            "grid_base_seed": GRID_BASE_SEED, "t_grid": T_GRID,
            "replay_source": "results/exp169_rt_scoping.json",
            "replay_seeds": [1, 2, 3], "repair_seeds": [1, 2, 3],
            "spearman_impl": SPEARMAN_IMPL, "pin_floor": DEP169_FLOOR},
        "verdict": {"gates": f"{n_pass}/{len(result['gates'])}",
                    "dominant_channel": br.get("feature"),
                    "unattributed": bool(br.get("unattributed")),
                    "one_line": one_line},
        "rejections": rejections,
        "runtime_s": round(os.times()[4] - t0, 1),
    })
    with open(out_path, "w") as f:
        json.dump(result, f, indent=1)
    print(f"\n  deposit -> {out_path}")
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["replay", "census", "repair",
                                      "all"], default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
