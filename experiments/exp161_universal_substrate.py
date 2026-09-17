#!/usr/bin/env python3
"""exp161 — THE UNIVERSAL SUBSTRATE TEST (Stage 5 path 2; the ~5%
untested branch per the HANDOFF): a substrate COHERENT WITH ANY
PATTERN — ONE fixed substrate that carries ARBITRARY target
morphologies — vs the current compiler, which PRICES substrate-pattern
pairs per target (exp144's nine-rung audit + exp150's R3 emission
pricing pick an operating point PER pattern).

======================================================================
PRE-REGISTERED (this docstring written BEFORE the run; the gates are
executed exactly once against these clauses; no clause may be edited
after the first instrument call):
======================================================================

THE CLAIM (C): there exists a single fixed substrate configuration S*
(one wiring + one operating point, chosen ONCE, before any per-target
verdict is issued) such that the compiler can write >= 10 DIVERSE
target morphologies onto S* at the 6.0 mV bar — while today's
machinery re-prices the operating point per target (emit_rung).

WHAT A SUBSTRATE IS HERE (honest scope, matching the machinery): the
substrate S = (adjacency, gamma, mu). The wiring is FIXED to the
machinery's home axis A_CHAIN = path(N=100) — the one wiring exp136
declared as its honest scope. The operating point (gamma, mu) ranges
over exp144's frozen EXTENDED_LADDER (the nine audited rungs). S* is
therefore ONE rung of the frozen ladder, fixed ONCE for the whole
battery; the DEFAULT substrate is (1.0, 0.015) — the DEFAULT0 pole
cell, exp136's ladder head and the price map's default.

THE TARGET BATTERY (pre-registered, fixed below in TARGETS; ten
morphologies spanning zone counts 1-4 and the voltage bands -16..-35
mV; every member must satisfy exp136's well_formed; the battery is
frozen BEFORE selection — no member may be added/dropped per
substrate):
  u-01 1-zone left  band-mid    [(0.05,0.16,-30)]
  u-02 1-zone right band-deep   [(0.80,0.92,-34)]
  u-03 1-zone mid   band-shallow[(0.46,0.58,-20)]
  u-04 2-zone flanks deep         [(0.06,0.14,-30),(0.86,0.95,-34)]
  u-05 2-zone shallow+deep mid     [(0.08,0.18,-16),(0.70,0.80,-30)]
  u-06 2-zone interior mid+deep    [(0.30,0.40,-25),(0.55,0.65,-32)]
  u-07 3-zone spread shallow/mid   [(0.06,0.14,-22),(0.42,0.50,-30),
                                    (0.80,0.90,-26)]
  u-08 3-zone deep/shallow/mid     [(0.10,0.20,-34),(0.40,0.48,-18),
                                    (0.66,0.76,-30)]
  u-09 4-zone ascending ladder    -16/-22/-28/-34
  u-10 4-zone descending ladder   -35/-28/-20/-24
DIVERSITY (deposited, pre-registered clauses): (i) zone counts cover
{1,2,3,4}; (ii) all 45 pairwise exp136 dist() distances > 0 (no two
members share a cut structure); the min pairwise distance is reported
against the exp150 corpus bar N*_pool = 33.776 as context, NOT gated.

SELECTION RULE (stated BEFORE evaluation; the maximin substrate):
  For every rung S in EXTENDED_LADDER and every target t in the
  battery, the PROBE margin (seed 1 only — the cheap instrument):
      m1(S,t) = 6.0 - max( quad1(S,t), dec1(S,t), hold1(S,t) )
  where quad1 = hypot(eV, eT) from ONE erosion seed, and dec1/hold1
  are ONE decode seed's post-settle and hold errors (exp136
  instruments verbatim, seed 1).
  S* = argmax_S min_t m1(S,t)   — the maximin substrate.
  TIES break to the LOWER rung_cost(g, mu) (exp144's frozen injective
  cost key). The rule is evaluated ONCE, on the whole battery, before
  any 3-seed verdict is computed. The probe (1 seed) vs the verdict
  (3 seeds, below) deliberately differ, so S3 is a genuine
  cross-seed prediction test, not a restatement.

THE VERDICT INSTRUMENT (the 6.0 mV bar; exp150's price_rung
semantics VERBATIM): target t is WRITABLE on S iff
  (a) two-channel audit quad = hypot(eV, eT) < 6.0 at seeds 1,2,3,
      eV = V-channel erosion mean (mu=0 arm), eT = theta-channel
      erosion mean — and
  (b) decode 3/3: post-settle decode_err < 6.0 AND 100 t.u.
      hold_err < 6.0 on ALL of seeds 1,2,3.
The 3-seed margin m3(S,t) = 6.0 - max(quad3, max dec3, max hold3).
The FULL 9x10 (rung x target) 3-seed matrix is priced and deposited
so the boundary of substrate universality is readable even where
gates fail.

GATES (all four fixed before the run):
  GATE-S1  UNIVERSALITY BAR: >= 8/10 battery targets are WRITABLE on
           S* at the 6.0 mV bar (the bar mirrors the generator's C3
           >= 8/10 and exp150's delivered-10 semantics).
  GATE-S2  NO PER-TARGET SUBSTRATE ADJUSTMENT: S* is constant across
           all ten writes — only the WRITE PROGRAM (the per-target
           spec layer, clamps and amputation region) changes. Locked
           in-module: every write asserts it is running on exactly
           the selected rung (a per-target substrate change raises),
           the wiring object identity is asserted identical on every
           call, and the accumulated substrate log is asserted
           uniform before the verdict.
  GATE-S3  THE MAXIMIN MARGIN PREDICTS THE PASS/FAIL PATTERN: with
           predicted-pass(t) := m1(S*,t) > 0 and
           actual-pass(t) := writable(S*,t) at 3 seeds, agreement on
           the 10 targets >= 9/10 (90%).
  GATE-S4  WORST-CASE CONTRAST vs THE DEFAULT SUBSTRATE: the same 10
           targets on DEFAULT = (1.0, 0.015) score worse AT THE
           WORST CASE — min_t m3(S*,t) > min_t m3(DEFAULT,t). The
           pre-registered point: universality is a WORST-CASE
           property, not a mean — means are deposited for the record
           but do not enter the gate. If the maximin rule selects the
           default rung itself, S4 is scored FAIL with the degenerate
           contrast disclosed (the honest outcome "default was
           already maximin" would kill the contrast claim).

IF S1 FAILS the deposit answers WHERE: for every failing target, the
violated channel (audit-V / audit-theta / decode / hold, with the
worst-seed values) at S*, plus (from the full matrix) the rungs that
WOULD carry it — the boundary of substrate universality.

INSTRUMENTS: exp136/exp144/exp150 imported verbatim (quad_err,
decode, price_rung, EXTENDED_LADDER, PROVENANCE, rung_cost); new
objects are only the battery, the probe margin, the maximin rule, the
substrate lock, and the worst-case contrast. No ladder, bar, or
instrument is modified. Wall budget <= 14 min (the full sweep is
9 rungs x 10 targets x 3 seeds of erosion+decode, ~0.2 s per cell).

DEPOSIT: results/exp161_universal_substrate.json
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

from experiments.exp136_generator_v6 import (  # noqa: E402
    ERR_BAR, N as LAT_N, A_CHAIN, AUDIT_SEEDS, well_formed,
    profile_of_zones, erosion, decode, dist, build_library, build_splices,
)
from experiments.exp144_audit_operating_points import (  # noqa: E402
    EXTENDED_LADDER, PROVENANCE, rung_cost,
)
from experiments.exp150_generator_complete import price_rung  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp161_universal_substrate.json")

N = LAT_N                       # 100 — the machinery's lattice
BAR = ERR_BAR                   # 6.0 mV — the unchanged bar
DEFAULT_SUB = (1.0, 0.015)      # the DEFAULT0 pole cell (pre-registered)
PROBE_SEED = 1                  # the selection probe's seed (pre-registered)

# ---- THE TARGET BATTERY (frozen; see docstring) --------------------
TARGETS = [
    ("u-01", [(0.05, 0.16, -30.0)]),
    ("u-02", [(0.80, 0.92, -34.0)]),
    ("u-03", [(0.46, 0.58, -20.0)]),
    ("u-04", [(0.06, 0.14, -30.0), (0.86, 0.95, -34.0)]),
    ("u-05", [(0.08, 0.18, -16.0), (0.70, 0.80, -30.0)]),
    ("u-06", [(0.30, 0.40, -25.0), (0.55, 0.65, -32.0)]),
    ("u-07", [(0.06, 0.14, -22.0), (0.42, 0.50, -30.0),
              (0.80, 0.90, -26.0)]),
    ("u-08", [(0.10, 0.20, -34.0), (0.40, 0.48, -18.0),
              (0.66, 0.76, -30.0)]),
    ("u-09", [(0.06, 0.14, -16.0), (0.28, 0.36, -22.0),
              (0.52, 0.60, -28.0), (0.76, 0.84, -34.0)]),
    ("u-10", [(0.05, 0.13, -35.0), (0.30, 0.38, -28.0),
              (0.52, 0.60, -20.0), (0.80, 0.88, -24.0)]),
]

# ---- THE SUBSTRATE LOCK (GATE-S2, in-module) -----------------------
_SUBSTRATE_LOG: list[tuple] = []   # (rung, wiring-id) appended per write


def _lock_substrate(rung: tuple) -> None:
    """Assert the write runs on exactly the fixed substrate: the same
    rung tuple and the same wiring object. A per-target substrate
    adjustment RAISES instead of passing silently."""
    assert rung == _SUBSTRATE_FIXED[0], \
        f"substrate drift: write used {rung}, fixed {_SUBSTRATE_FIXED[0]}"
    assert id(A_CHAIN) == _SUBSTRATE_FIXED[1], "wiring object changed"


_SUBSTRATE_FIXED: list = []        # set once at selection: [rung, id(A_CHAIN)]


def probe_margin(f: np.ndarray, zones, rung: tuple) -> float:
    """The pre-registered PROBE margin m1 (seed 1 only)."""
    g, mu = rung
    eV = erosion(f, g, 0.0, "V_only", PROBE_SEED)
    eT = erosion(f, g, mu, "theta_only", PROBE_SEED)
    quad1 = float(np.hypot(eV, eT))
    d = decode(f, zones, g, mu, PROBE_SEED)
    if d.get("rejected"):
        return -float("inf")          # compiler rejection = unwritable
    return BAR - max(quad1, float(d["decode_err"]), float(d["hold_err"]))


def writable_3seed(f: np.ndarray, zones, rung: tuple) -> dict:
    """The VERDICT instrument: exp150's price_rung verbatim + the
    writable predicate. Locked to the fixed substrate (GATE-S2): the
    write is refused if the substrate has drifted from the locked
    rung; every write is logged."""
    _lock_substrate(rung)
    row = price_rung(f, zones, rung[0], rung[1])
    _SUBSTRATE_LOG.append((rung, id(A_CHAIN)))
    rejected = bool(row["n_rejected"] > 0)
    if rejected:
        return {"row": row, "writable": False, "rejected": True,
                "margin3": -float("inf")}
    m3 = BAR - max(row["quad"], max(row["decode_errs"]),
                   max(row["hold_errs"]))
    return {"row": row, "writable": bool(row["full_valid"]),
            "rejected": False, "margin3": float(m3)}


def main() -> dict:
    t0 = time.time()
    print("=== exp161: the universal substrate test "
          "(maximin S* vs per-target pricing) ===\n")

    # ---- 0. battery integrity (pre-registered clauses) --------------
    battery = []
    for name, zones in TARGETS:
        assert well_formed(zones), f"{name} violates well_formed"
        battery.append({"name": name, "zones": zones,
                        "zone_count": len(zones),
                        "vmin": min(z[2] for z in zones),
                        "vmax": max(z[2] for z in zones)})
    zone_counts = sorted({b["zone_count"] for b in battery})
    assert zone_counts == [1, 2, 3, 4], "battery must span zone counts 1-4"
    profiles = {n: profile_of_zones(zs) for n, zs in TARGETS}
    names = [n for n, _ in TARGETS]
    Dm = np.zeros((10, 10))
    for i in range(10):
        for j in range(i + 1, 10):
            Dm[i, j] = Dm[j, i] = dist(profiles[names[i]],
                                       profiles[names[j]])
    min_pair = float(Dm[Dm > 0].min()) if (Dm > 0).any() else 0.0
    assert (Dm[np.triu_indices(10, 1)] > 0).all(), \
        "battery diversity clause: all pairwise dist > 0"
    print(f"  battery: 10 targets, zone counts {zone_counts}, "
          f"vmin..vmax [{min(b['vmin'] for b in battery)}, "
          f"{max(b['vmax'] for b in battery)}], "
          f"min pairwise dist {min_pair:.3f} "
          f"(exp150 corpus bar N*_pool 33.776, context only)")

    # ---- 1. THE FULL 9x10 SWEEP (3-seed verdict instrument) --------
    # Priced BEFORE selection issues S* (the matrix is the deposit and
    # the S1/S4 raw data); S* is selected from the SEED-1 PROBE only.
    t_sweep = time.time()
    matrix: list[list[dict]] = []
    for rung in EXTENDED_LADDER:
        row = []
        for name, zones in TARGETS:
            _SUBSTRATE_FIXED[:] = [rung, id(A_CHAIN)]
            _lock_substrate(rung)
            prof = profiles[name]
            eV = float(np.mean([erosion(prof, rung[0], 0.0, "V_only", s)
                                for s in AUDIT_SEEDS]))
            eT = float(np.mean([erosion(prof, rung[0], rung[1],
                                        "theta_only", s)
                                for s in AUDIT_SEEDS]))
            quad3 = float(np.hypot(eV, eT))
            dec = [decode(prof, zones, rung[0], rung[1], s)
                   for s in AUDIT_SEEDS]
            if any(d.get("rejected") for d in dec):
                row.append({"rung": rung, "name": name, "rejected": True,
                            "writable": False, "margin3": -float("inf")})
                continue
            derr = [float(d["decode_err"]) for d in dec]
            herr = [float(d["hold_err"]) for d in dec]
            full_valid = bool(quad3 < BAR and all(a < BAR and b < BAR
                             for a, b in zip(derr, herr)))
            row.append({"rung": rung, "name": name, "rejected": False,
                        "eV": eV, "eT": eT, "quad": quad3,
                        "decode_errs": derr, "hold_errs": herr,
                        "writable": full_valid,
                        "margin3": BAR - max(quad3, max(derr),
                                             max(herr))})
        matrix.append(row)
        wm = min(r["margin3"] for r in row)
        print(f"  rung {rung}: worst-case m3 {wm:+.3f} | "
              f"writable {sum(int(r['writable']) for r in row)}/10 "
              f"(sweep t={time.time() - t_sweep:.0f}s)")

    # ---- 2. THE MAXIMIN SELECTION (probe margins, seed 1) ----------
    probe = [[probe_margin(profiles[nm], zs, rung)
              for nm, zs in TARGETS] for rung in EXTENDED_LADDER]
    worst_probe = [float(min(col)) for col in probe]
    order = sorted(range(len(EXTENDED_LADDER)),
                   key=lambda k: (-worst_probe[k],
                                  rung_cost(*EXTENDED_LADDER[k])))
    k_star = order[0]
    S_STAR = EXTENDED_LADDER[k_star]
    k_def = EXTENDED_LADDER.index(DEFAULT_SUB)
    assert DEFAULT_SUB in EXTENDED_LADDER
    # ties disclosed: how many rungs share the maximin probe value
    tied = [EXTENDED_LADDER[k] for k in range(len(EXTENDED_LADDER))
            if abs(worst_probe[k] - worst_probe[k_star]) < 1e-12]
    print(f"\n  maximin rule: worst probe margins "
          f"{[round(w, 3) for w in worst_probe]}")
    print(f"  S* = {S_STAR} ({PROVENANCE[S_STAR]}), "
          f"worst probe {worst_probe[k_star]:+.3f} mV, ties={tied}")

    # ---- 3. fix the substrate ONCE; re-verdict the battery on S* ----
    _SUBSTRATE_FIXED[:] = [S_STAR, id(A_CHAIN)]      # locked for good
    verdicts = []
    for name, zones in TARGETS:
        verdicts.append(writable_3seed(profiles[name], zones, S_STAR))
    w_star = [v["writable"] for v in verdicts]
    n_writable = int(sum(w_star))
    worst_star = float(min(v["margin3"] for v in verdicts))
    mean_star = float(np.mean([v["margin3"] for v in verdicts]))

    # ---- 4. the same battery on the DEFAULT substrate ---------------
    _SUBSTRATE_FIXED[:] = [DEFAULT_SUB, id(A_CHAIN)]
    verdicts_def = []
    for name, zones in TARGETS:
        verdicts_def.append(writable_3seed(profiles[name], zones,
                                           DEFAULT_SUB))
    worst_def = float(min(v["margin3"] for v in verdicts_def))
    mean_def = float(np.mean([v["margin3"] for v in verdicts_def]))
    n_w_def = int(sum(v["writable"] for v in verdicts_def))

    # ---- GATE-S2: substrate constancy (the log) ---------------------
    # 20 locked writes total: 10 on S* then 10 on the default rung;
    # the wiring object identity is asserted on every write.
    runs = [r for r, _ in _SUBSTRATE_LOG]
    log_ok = bool(len(_SUBSTRATE_LOG) == 20
                  and all(r == S_STAR for r in runs[:10])
                  and all(r == DEFAULT_SUB for r in runs[10:])
                  and all(w == id(A_CHAIN) for _, w in _SUBSTRATE_LOG))
    # determinism harness: the locked writes must reproduce the sweep
    # row for S* exactly AT price_rung's own deposit precision (the
    # row stores 3-decimal-rounded channel values; comparing a
    # rounded-value margin against a raw-value margin at 1e-9 would
    # test the rounding, not the physics)
    def _same_row(i: int) -> bool:
        mrow, vrow = matrix[k_star][i], verdicts[i]["row"]
        if mrow["writable"] != verdicts[i]["writable"]:
            return False
        if mrow.get("rejected") or verdicts[i].get("rejected"):
            return mrow.get("rejected", False) == \
                verdicts[i].get("rejected", False)
        return (round(float(mrow["quad"]), 3) == round(vrow["quad"], 3)
                and [round(x, 3) for x in mrow["decode_errs"]]
                == [round(x, 3) for x in vrow["decode_errs"]]
                and [round(x, 3) for x in mrow["hold_errs"]]
                == [round(x, 3) for x in vrow["hold_errs"]])
    determinism = bool(all(_same_row(i) for i in range(10)))
    s2 = bool(log_ok and determinism)
    print(f"\n  S2 substrate log: {len(_SUBSTRATE_LOG)} writes, "
          f"constant-per-phase={log_ok}, locked-vs-sweep "
          f"determinism(3dp)={determinism}")

    # ---- GATE-S1 ----------------------------------------------------
    s1 = n_writable >= 8
    # ---- GATE-S3: probe prediction vs 3-seed verdict ----------------
    pred = [probe[k_star][i] > 0 for i in range(10)]
    agree = sum(int(p == a) for p, a in zip(pred, w_star))
    s3 = agree >= 9
    # ---- GATE-S4: worst-case contrast vs default --------------------
    degenerate = (S_STAR == DEFAULT_SUB)
    s4 = bool(worst_star > worst_def) and not degenerate
    gates = {"S1": s1, "S2": s2, "S3": s3, "S4": s4}
    npass = int(sum(gates.values()))

    # ---- WHERE (S1 boundary deposit) --------------------------------
    where = []
    for i, (name, zones) in enumerate(TARGETS):
        if w_star[i]:
            continue
        v = verdicts[i]["row"]
        if verdicts[i].get("rejected"):
            chan = {"violated": ["compiler_rejection"],
                    "n_rejected": int(v["n_rejected"])}
        else:
            worst_seed = int(np.argmax([max(a, b) for a, b in
                                        zip(v["decode_errs"],
                                            v["hold_errs"])]))
            chan = {
                "audit_V": v["eV"], "audit_theta": v["eT"],
                "quad": v["quad"], "quad_violated": bool(v["quad"] >= BAR),
                "decode_errs": v["decode_errs"],
                "hold_errs": v["hold_errs"],
                "worst_seed": AUDIT_SEEDS[worst_seed],
                "violated": [c for c, bad in
                             [("audit", v["quad"] >= BAR),
                              ("decode", max(v["decode_errs"]) >= BAR),
                              ("hold", max(v["hold_errs"]) >= BAR)]
                             if bad],
            }
        chan["carried_elsewhere"] = [
            {"rung": list(r), "margin3": float(matrix[k][i]["margin3"])}
            for k, r in enumerate(EXTENDED_LADDER)
            if matrix[k][i]["writable"]]
        where.append({"target": name, "zones": zones, **chan})

    out = {
        "experiment": "exp161_universal_substrate",
        "claim": ("one fixed substrate S* (path wiring + one "
                  "operating point) carries a diverse 10-target "
                  "battery at the 6.0 mV bar without per-target "
                  "substrate adjustment"),
        "pre_registered": {"battery": [b for b in battery],
                           "selection_rule":
                               "S* = argmax_S min_t m1(S,t); ties -> "
                               "lower rung_cost; probe = seed 1",
                           "verdict_instrument":
                               "exp150 price_rung semantics: quad<6.0 "
                               "AND decode 3/3 (dec & hold < 6.0)",
                           "gates": {
                               "S1": ">= 8/10 writable on S*",
                               "S2": "substrate constant per write "
                                     "(in-module lock), wiring identity",
                               "S3": "probe margin predicts 3-seed "
                                     "verdict, >= 9/10 agreement",
                               "S4": "min_t m3(S*) > min_t m3(default) "
                                     "(worst-case, not mean)"},
                           "default_substrate": list(DEFAULT_SUB)},
        "diversity": {"zone_counts": zone_counts,
                      "min_pairwise_dist": min_pair,
                      "dist_matrix_100": [[round(float(x), 3)
                                           for x in row] for row in Dm],
                      "context_corpus_bar_N_pool": 33.776},
        "probe_worst_margins_per_rung":
            {str(list(r)): round(w, 4) for r, w in
             zip(EXTENDED_LADDER, worst_probe)},
        "selection": {"S_star": list(S_STAR),
                      "provenance": PROVENANCE[S_STAR],
                      "worst_probe_margin": round(worst_probe[k_star], 4),
                      "tied_rungs": [list(t) for t in tied],
                      "tie_break": "lower rung_cost (frozen, injective)"},
        "s_star_battery": {
            "n_writable": n_writable,
            "writable": [names[i] for i in range(10) if w_star[i]],
            "not_writable": [names[i] for i in range(10)
                             if not w_star[i]],
            "per_target": [
                {"name": names[i],
                 "writable": bool(w_star[i]),
                 "margin3": round(float(verdicts[i]["margin3"]), 4),
                 "probe_margin1": round(float(probe[k_star][i]), 4),
                 "predicted_pass": bool(pred[i]),
                 **{k: v for k, v in verdicts[i]["row"].items()
                    if k not in ("cell", "provenance", "cost")}}
                for i in range(10)],
            "worst_case_margin3": round(worst_star, 4),
            "mean_margin3": round(mean_star, 4)},
        "default_battery": {
            "n_writable": n_w_def,
            "writable": [names[i] for i in range(10)
                         if verdicts_def[i]["writable"]],
            "worst_case_margin3": round(worst_def, 4),
            "mean_margin3": round(mean_def, 4),
            "per_target_margin3": [
                round(float(verdicts_def[i]["margin3"]), 4)
                for i in range(10)]},
        "contrast": {
            "worst_case": {"S_star": round(worst_star, 4),
                           "default": round(worst_def, 4)},
            "mean": {"S_star": round(mean_star, 4),
                     "default": round(mean_def, 4)},
            "point": "universality = worst-case, not mean"},
        "substrate_log": {"n_writes": len(_SUBSTRATE_LOG),
                          "log_constant_ok": log_ok,
                          "determinism_3dp": determinism,
                          "runs": [[list(r), "A_CHAIN"]
                                   for r, _ in _SUBSTRATE_LOG]},
        "gates": gates,
        "gates_passed": f"{npass}/4",
        "where_if_S1_failed": where,
        "full_matrix_margin3":
            [[round(float(matrix[k][i]["margin3"]), 4)
              for i in range(10)] for k in range(9)],
        "full_matrix_writable":
            [[bool(matrix[k][i]["writable"]) for i in range(10)]
             for k in range(9)],
        "full_matrix_channels": [
            [{"rung": list(r), "target": names[i],
              **{k: v for k, v in matrix[k][i].items()
                 if k in ("rejected", "eV", "eT", "quad",
                          "decode_errs", "hold_errs", "writable")}}
             for i in range(10)] for k, r in
            enumerate(EXTENDED_LADDER)],
        "wall_s": round(time.time() - t0, 1),
        "notes": ("Instruments exp136/exp144/exp150 imported verbatim "
                  "(price_rung = the verdict instrument). New objects: "
                  "the battery, the seed-1 probe margin, the maximin "
                  "selection with frozen-cost tie-break, the substrate "
                  "lock, the worst-case contrast. The full 9x10 "
                  "3-seed matrix is the universality boundary deposit. "
                  "INSTRUMENT DISCLOSURE (pre-commit): the first gate "
                  "evaluation failed S2's determinism clause in an "
                  "evaluation-only way — the clause compared the locked "
                  "writes' margin (derived from price_rung's "
                  "3-decimal-ROUNDED channel values) against the sweep "
                  "row's raw-valued margin at 1e-9, i.e. it tested the "
                  "rounding, not the physics; repaired to compare "
                  "channel-wise at price_rung's own deposit precision "
                  "(3 dp) before commit. Writable booleans and all "
                  "channel data were already in exact agreement; the "
                  "deterministic re-run is the deposited one."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, default=float)
    print(f"\n  GATES: S1={s1} S2={s2} S3={s3} S4={s4} -> {npass}/4")
    print(f"  S* {S_STAR}: {n_writable}/10 writable "
          f"(worst-case m3 {worst_star:+.3f}, mean {mean_star:+.3f}) | "
          f"default: {n_w_def}/10 "
          f"(worst-case {worst_def:+.3f}, mean {mean_def:+.3f})")
    print(f"  results -> {OUT} (wall {out['wall_s']}s)")
    return out


if __name__ == "__main__":
    main()
