#!/usr/bin/env python3
"""exp172 — DEEP-BAND INVENTION SWEEP (the widened repertoire's frontier).

exp168's registered next (L146): "the widened floor makes deep-zone
writes FIRST-CLASS (the search's own deep voltage band down to -60 is
now fully readable — the class the old floor effectively refused at
decode is writable, so a deep-band invention sweep prices the widened
repertoire's own frontier)". CF-1 (NEURAL_SPEC_MIN -35 -> -60, L146)
made the compiler's full repertoire [-60, -15] (exp141's WIDE_LO/HI =
REPERTOIRE_LO/HI, compiler/anatomy.py) readable at decode: before,
any committed spec below -35 fell back to canon at exp136.decode's
adoption branch; now it adopts. THIS EXPERIMENT prices the newly
readable band directly.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Ladder, bars, and gates are fixed now.

THE DESIGN:
  * Target patterns: piecewise-constant zone patterns f on n=100
    engines, built by exp94's spec_target_n machinery (MULTI zones,
    labeling_bfs_n) with the zone values forced to the rung ladder —
    DEEP rungs {-40.0, -45.0, -50.0, -55.0, -60.0} (5 rungs x 10
    instances) and SHALLOW controls {-20.0, -25.0, -30.0} (3 rungs x
    10 instances); seeds (1, 2, 3) per (rung, instance) — the same
    3-seed protocol as exp168's B2/B3.
  * THE TWO ARMS (the audit IS the design, exp168's mechanism):
      PATCHED — the working tree's CF-1 floor (-60.0): decode adopts.
      PINNED  — OLD_FLOOR_PIN rebinding the ONE constant to -35.0
                (save/restore asserted) in the modules that captured
                it at import time: the pre-CF-1 engine.
  * Readout: exp136's decode VERBATIM (the consumer CF-1 targets) —
    e_decode = pattern_error(f) after the adoption walk, then the
    stability hold; errs at 2-dp precision, replay comparisons exact.

PRE-REGISTERED GATES (each evaluated exactly once):

  GATE-D1 (shallow audit) SHALLOW controls: patched errs == pinned
           errs BIT-EXACTLY per (rung, instance, seed) — 90/90
           records (float equality). The adoption branch consumed
           one normal draw on EITHER side pre-patch (adopted or
           canon), so the rng streams align; any mismatch is an
           instrument bug, not a finding.
  GATE-D2 (the deep regime is live) DEEP rungs: pinned err >
           patched err on >= 80% of (rung, instance, seed) records;
           the pinned arm's errs sit at the canon-refusal scale
           (deposited: err_pinned vs err(canon projection of f),
           the "write did not take" reference, recorded per rung).
  GATE-D3 (the frontier price) the patched err profile vs depth
           deposited per rung; the frontier rung NAMED = the deepest
           rung whose median decode err <= 6.0 AND median hold err
           <= 6.0 (the production ERR_BAR, exp150's C3 clause) on
           the 3-seed medians. PASS iff at least one deep rung
           reaches the bar (the widened repertoire's frontier is
           real); the named rung is the deposit either way.
  GATE-D4 (hygiene) zero rejections; all errs finite; the pin's
           save/restore asserted between arms; the shallow arm run
           FIRST so any pin leakage fails D1 loudly.

NO post-hoc knob tuning; the ladder is fixed above. A --smoke
instrument check (rungs -40 and -20, instance 0, seed 1) is permitted
before the credited run and discarded; the credited full run uses the
committed script unchanged.

DEPOSIT: results/exp172_deep_band_sweep.json

RUN:
  python3 -m experiments.exp172_deep_band_sweep            # full
  python3 -m experiments.exp172_deep_band_sweep --smoke    # check
  python3 -m experiments.exp172_deep_band_sweep --rung -50.0
  # jobs: shallow | d40 | d45 | d50 | d55 | d60
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

from experiments.exp136_generator_v6 import (  # noqa: E402
    decode as exp136_decode,
)
from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)

import cultivation.bioelectric.collective as core  # noqa: E402

# ---- FIXED CONSTANTS ------------------------------------------------
DEEP_RUNGS = [-40.0, -45.0, -50.0, -55.0, -60.0]
SHALLOW_RUNGS = [-20.0, -25.0, -30.0]
N_INST = 10
SEEDS = (1, 2, 3)
ERR_BAR = 6.0                   # exp150's production bar
OLD_FLOOR = -35.0
NEW_FLOOR = -60.0

OUT = os.path.join(ROOT, "results", "exp172_deep_band_sweep.json")


class OldFloorPin:
    """exp168's OLD_FLOOR_PIN mechanism, verbatim semantics."""

    def __enter__(self):
        self._saved = core.NEURAL_SPEC_MIN
        core.NEURAL_SPEC_MIN = OLD_FLOOR
        return self

    def __exit__(self, *exc):
        core.NEURAL_SPEC_MIN = self._saved
        assert core.NEURAL_SPEC_MIN == NEW_FLOOR, "pin restore failed"


# ---- BODY (written by the run agent; gates fixed above) -------------
# Fixed BEFORE the credited run, disclosed here and in the deposit:
#   * INSTANCE mechanism (zero new RNG, zero new knobs): instance i is
#     the MULTI 3-zone program translated axially — every MULTI zone
#     boundary shifted by +i cells on the n=100 lattice (i = 0..9;
#     instance 0 = MULTI verbatim). f = spec_target_n(spec_i(rung),
#     canon, 100) with spec_i's zone VALUES forced to the rung.
#   * canon = labeling_bfs_n(exp136's A_CHAIN) — asserted bit-equal to
#     the decode engine's own canon memory (wildtype_target(100)), so
#     D1's "one normal draw on either branch" precondition holds and
#     D3 prices the deep band, not a canon mismatch.
#   * decode operating cell (gamma, mu) = (1.0, 0.0): exp150's/exp168's
#     deposited emitted rung (the production cell); seeds (1, 2, 3).
#   * THE PIN: OldFloorPin (verbatim class above) rebinds
#     core.NEURAL_SPEC_MIN; exp136_generator_v6 captured the SAME
#     constant at import time (line 149 from-import) and decode reads
#     its own module global, so the pinned arm additionally
#     saves/rebinds/restores g6.NEURAL_SPEC_MIN with asserts — the
#     docstring's "modules that captured it at import time".
#   * errs are deposited at 2-dp precision (plus exact floats for the
#     replay audit); the patched-vs-pinned comparisons are EXACT.
import time

import experiments.exp136_generator_v6 as g6
from cultivation.compiler.anatomy import AnatomySpec, Zone

GAMMA, MU = 1.0, 0.0              # the deposited production decode cell


def instance_zones(i: int) -> list:
    """Instance i: the MULTI 3-zone program shifted +i cells."""
    shift = i / 100.0
    return [(z.f0 + shift, z.f1 + shift, z.name) for z in MULTI.zones]


def target_for(rung: float, instance: int) -> tuple:
    """f, decode zone triples, canon-projection reference err."""
    zs = instance_zones(instance)
    spec = AnatomySpec(
        zones=[Zone(f0=a, f1=b, voltage=rung, name=nm)
               for (a, b, nm) in zs],
        amputate_plane=MULTI.amputate_plane,
        spec_name=f"ms-multi-deep-i{instance}",
        somatic_latch=MULTI.somatic_latch)
    canon = labeling_bfs_n(g6.A_CHAIN)
    assert np.array_equal(canon, g6.wildtype_target(g6.N)), \
        "canon mismatch: labeling_bfs_n(A_CHAIN) != engine canon"
    f = spec_target_n(spec, canon, g6.N)
    # the "write did not take" reference: f with every below-floor cell
    # replaced by the canon the pinned walk would read instead
    canon_proj = f.copy()
    below = f < OLD_FLOOR
    canon_proj[below] = canon[below]
    ref_err = float(np.sqrt(np.mean((f - canon_proj) ** 2)))
    triples = [(a, b, rung) for (a, b, _nm) in zs]
    return f, triples, ref_err


def _floors_patched() -> bool:
    return (core.NEURAL_SPEC_MIN == NEW_FLOOR
            and g6.NEURAL_SPEC_MIN == NEW_FLOOR)


def run_rung(rung: float, instance: int, seed: int, arm: str) -> dict:
    """One (rung, instance, seed) record. Body written by the run
    agent (gates fixed above)."""
    f, triples, ref_err = target_for(rung, instance)
    assert _floors_patched(), "floor drift before arm (expected -60.0)"
    if arm == "patched":
        dec = exp136_decode(f, triples, GAMMA, MU, seed)
    elif arm == "pinned":
        saved_core = core.NEURAL_SPEC_MIN
        saved_g6 = g6.NEURAL_SPEC_MIN
        assert saved_core == NEW_FLOOR and saved_g6 == NEW_FLOOR
        try:
            with OldFloorPin():              # pins core (verbatim class)
                g6.NEURAL_SPEC_MIN = OLD_FLOOR   # the import-time capture
                assert (core.NEURAL_SPEC_MIN == OLD_FLOOR
                        and g6.NEURAL_SPEC_MIN == OLD_FLOOR), "pin failed"
                dec = exp136_decode(f, triples, GAMMA, MU, seed)
        finally:
            g6.NEURAL_SPEC_MIN = saved_g6    # OldFloorPin restored core
        assert _floors_patched(), "pin restore failed"
    else:
        raise ValueError(f"unknown arm: {arm}")
    d_err = float(dec["decode_err"])
    h_err = float(dec["hold_err"])
    rej = list(dec.get("rejected", []))
    return {"arm": arm, "decode_err": d_err, "hold_err": h_err,
            "rejected": rej, "finite": bool(np.isfinite(d_err)
                                            and np.isfinite(h_err)),
            "canon_ref_err": ref_err}


def _record(rung: float, instance: int, seed: int) -> dict:
    pr = run_rung(rung, instance, seed, "patched")
    nr = run_rung(rung, instance, seed, "pinned")
    return {
        "rung": rung, "instance": instance, "seed": seed,
        "patched": {"decode_err": round(pr["decode_err"], 2),
                    "hold_err": round(pr["hold_err"], 2),
                    "decode_err_exact": pr["decode_err"],
                    "hold_err_exact": pr["hold_err"]},
        "pinned": {"decode_err": round(nr["decode_err"], 2),
                   "hold_err": round(nr["hold_err"], 2),
                   "decode_err_exact": nr["decode_err"],
                   "hold_err_exact": nr["hold_err"]},
        "rejected": pr["rejected"] + nr["rejected"],
        "finite": bool(pr["finite"] and nr["finite"]),
        "bit_exact": bool(pr["decode_err"] == nr["decode_err"]
                          and pr["hold_err"] == nr["hold_err"]),
        "pin_wins": bool(nr["decode_err"] > pr["decode_err"]),
        "canon_ref_err": round(pr["canon_ref_err"], 2),
        "canon_ref_err_exact": pr["canon_ref_err"],
    }


def _job_rungs(args) -> tuple:
    if args.rung is not None:
        return [float(args.rung)], f"rung{args.rung}"
    if args.job == "shallow":
        return list(SHALLOW_RUNGS), "shallow"
    if args.job == "all":
        # D4's pre-registered execution order: the shallow arm FIRST
        return list(SHALLOW_RUNGS) + list(DEEP_RUNGS), "full"
    return [-float(args.job[1:])], args.job      # d40 -> -40.0


def _evaluate(records: list) -> dict:
    shallow = [r for r in records if r["rung"] in SHALLOW_RUNGS]
    deep = [r for r in records if r["rung"] in DEEP_RUNGS]

    # D1: shallow bit-exact audit (90/90 float-equality records)
    n_d1 = sum(int(r["bit_exact"]) for r in shallow)
    d1 = {"gate": "D1", "clause": "shallow patched == pinned bit-exactly "
          "per (rung, instance, seed)", "bit_exact": n_d1,
          "n_records": len(shallow),
          "pass": bool(len(shallow) == 90 and n_d1 == 90)}

    # D2: the deep regime is live (>= 80% pinned > patched) + the
    # canon-refusal scale reference per rung
    n_d2 = sum(int(r["pin_wins"]) for r in deep)
    frac = n_d2 / len(deep) if deep else 0.0
    d2 = {"gate": "D2", "clause": "pinned err > patched err on >= 80% of "
          "deep records", "pin_wins": n_d2, "n_records": len(deep),
          "frac": round(frac, 4),
          "pass": bool(len(deep) == 150 and frac >= 0.80)}

    # D3: the frontier price — deepest deep rung whose 3-seed-median
    # patched decode err AND hold err are both <= ERR_BAR
    per_rung = {}
    for rung in list(SHALLOW_RUNGS) + list(DEEP_RUNGS):
        rows = [r for r in records if r["rung"] == rung]
        if not rows:
            continue
        insts = sorted(set(r["instance"] for r in rows))
        med_dec, med_hold = [], []
        for inst in insts:
            irows = [r for r in rows if r["instance"] == inst]
            med_dec.append(float(np.median(
                [r["patched"]["decode_err_exact"] for r in irows])))
            med_hold.append(float(np.median(
                [r["patched"]["hold_err_exact"] for r in irows])))
        per_rung[rung] = {
            "n_records": len(rows),
            "patched_median_decode_3seed": float(np.median(med_dec)),
            "patched_median_hold_3seed": float(np.median(med_hold)),
            "patched_median_decode_pooled": float(np.median(
                [r["patched"]["decode_err_exact"] for r in rows])),
            "patched_median_hold_pooled": float(np.median(
                [r["patched"]["hold_err_exact"] for r in rows])),
            "pinned_median_decode_pooled": float(np.median(
                [r["pinned"]["decode_err_exact"] for r in rows])),
            "canon_ref_median": float(np.median(
                [r["canon_ref_err_exact"] for r in rows])),
            "pin_wins_frac": round(sum(int(r["pin_wins"])
                                       for r in rows) / len(rows), 4),
            "at_bar_strict": bool(np.median(med_dec) < ERR_BAR
                                  and np.median(med_hold) < ERR_BAR),
        }
    frontier = None
    for rung in sorted(DEEP_RUNGS):          # deepest first
        s = per_rung.get(rung)
        if s and s["patched_median_decode_3seed"] <= ERR_BAR \
                and s["patched_median_hold_3seed"] <= ERR_BAR:
            frontier = rung
            break
    d3 = {"gate": "D3", "clause": f"deepest deep rung with median decode "
          f"err <= {ERR_BAR} AND median hold err <= {ERR_BAR} on the "
          f"3-seed medians; PASS iff at least one deep rung reaches "
          f"the bar", "frontier_rung": frontier, "pass": frontier is not None}

    # D4: hygiene
    n_rej = sum(len(r["rejected"]) for r in records)
    all_fin = all(r["finite"] for r in records)
    shallow_first = bool(records) and all(
        r["rung"] in SHALLOW_RUNGS for r in records[:len(SHALLOW_RUNGS)
                                                  * N_INST * len(SEEDS)])
    d4 = {"gate": "D4", "clause": "zero rejections; all errs finite; pin "
          "save/restore asserted between arms; shallow arm run FIRST",
          "rejections": n_rej, "all_finite": all_fin,
          "pin_save_restore_asserted": True,   # any violation raises
          "shallow_arm_first": shallow_first,
          "canon_match_asserted": True,
          "pass": bool(n_rej == 0 and all_fin and shallow_first)}

    npass = sum(int(g["pass"]) for g in (d1, d2, d3, d4))
    return {"records_by_rung": {str(k): v for k, v in per_rung.items()},
            "D1": d1, "D2": d2, "D3": d3, "D4": d4,
            "n_pass": npass, "verdict": f"{npass}/4",
            "frontier_rung": frontier}


def _run_smoke(args) -> dict:
    """--smoke instrument check: rungs -40 and -20, instance 0, seed 1.
    Permitted before the credited run and DISCARDED (no deposit unless
    --out is given explicitly)."""
    t0 = time.time()
    rows = []
    for rung in (-40.0, -20.0):
        for arm in ("patched", "pinned"):
            rec = run_rung(rung, 0, 1, arm)
            rows.append({"rung": rung, "arm": arm,
                         "decode_err": round(rec["decode_err"], 2),
                         "hold_err": round(rec["hold_err"], 2),
                         "decode_err_exact": rec["decode_err"],
                         "hold_err_exact": rec["hold_err"],
                         "rejected": rec["rejected"],
                         "finite": rec["finite"]})
        assert _floors_patched(), "pin restore failed in smoke"
    by = {(r["rung"], r["arm"]): r for r in rows}
    checks = {
        "zero_rejections": all(not r["rejected"] for r in rows),
        "all_finite": all(r["finite"] for r in rows),
        "shallow_bit_exact": bool(
            by[(-20.0, "patched")]["decode_err_exact"]
            == by[(-20.0, "pinned")]["decode_err_exact"]
            and by[(-20.0, "patched")]["hold_err_exact"]
            == by[(-20.0, "pinned")]["hold_err_exact"]),
        "deep_regime_live": bool(
            by[(-40.0, "pinned")]["decode_err"]
            > by[(-40.0, "patched")]["decode_err"]),
        "floors_restored": _floors_patched(),
    }
    ok = all(checks.values())
    print(f"=== exp172 SMOKE (instrument check, discarded) ===")
    for r in rows:
        print(f"  rung {r['rung']:6.1f} {r['arm']:8s} decode "
              f"{r['decode_err']:6.2f} hold {r['hold_err']:6.2f} "
              f"rej {len(r['rejected'])}")
    for k, v in checks.items():
        print(f"  {k}: {'OK' if v else 'FAIL'}")
    print(f"  === smoke {'OK' if ok else 'INSTRUMENT BUG'} "
          f"({time.time() - t0:.1f}s) ===")
    dep = {"exp": "exp172_deep_band_sweep", "kind": "smoke",
           "discarded": True, "rows": rows, "checks": checks, "ok": ok}
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)),
                    exist_ok=True)
        with open(args.out, "w") as fh:
            json.dump(dep, fh, indent=1)
    return dep


def main(args=None) -> dict:
    if args is None:
        import argparse as _ap
        args = _ap.ArgumentParser().parse_args([])  # pragma: no cover
    if args.smoke:
        return _run_smoke(args)
    t0 = time.time()
    rungs, scope = _job_rungs(args)
    records = []
    for rung in rungs:            # SHALLOW FIRST (pre-registered D4 order)
        for inst in range(N_INST):
            for seed in SEEDS:
                rec = _record(rung, inst, seed)
                records.append(rec)
            print(f"  rung {rung:6.1f} instance {inst:2d} done "
                  f"({time.time() - t0:.0f}s)", flush=True)
    full = scope == "full"
    gates = _evaluate(records) if full else None
    dep = {
        "exp": "exp172_deep_band_sweep",
        "claim": "the widened repertoire's own frontier: deep-band "
                 "invention sweep pricing the newly readable [-60, -35) "
                 "band at decode (exp168's registered next, L146)",
        "pre_registered": {
            "deep_rungs": DEEP_RUNGS, "shallow_rungs": SHALLOW_RUNGS,
            "n_instances": N_INST, "seeds": list(SEEDS),
            "err_bar": ERR_BAR, "old_floor": OLD_FLOOR,
            "new_floor": NEW_FLOOR,
            "instance_mechanism": "the MULTI 3-zone program translated "
                                  "+i cells on the n=100 lattice "
                                  "(i = 0..9; instance 0 = MULTI "
                                  "verbatim); zero new RNG",
            "instances": {str(i): instance_zones(i)
                          for i in range(N_INST)},
            "canon": "labeling_bfs_n(exp136.A_CHAIN), asserted == "
                     "wildtype_target(100) (the engine's own canon)",
            "operating_cell": [GAMMA, MU],
            "decode": "exp136_generator_v6.decode VERBATIM",
            "pin_disclosure": "OldFloorPin (verbatim class) pins "
                              "core.NEURAL_SPEC_MIN; g6.NEURAL_SPEC_MIN "
                              "(exp136's import-time capture, line 149) "
                              "saved/rebound/restored with asserts",
            "execution_order": "shallow rungs first (gate D4)",
        },
        "scope": scope, "n_records": len(records),
        "records": records,
        "gates": gates,
        "smoke_disclosure": "a --smoke instrument check (rungs -40 and "
                            "-20, instance 0, seed 1) ran before the "
                            "credited run and was discarded (no file)",
        "wall_s": round(time.time() - t0, 1),
    }
    if gates:
        for g in ("D1", "D2", "D3", "D4"):
            gg = gates[g]
            extra = ""
            if g == "D1":
                extra = f" ({gg['bit_exact']}/{gg['n_records']})"
            elif g == "D2":
                extra = f" ({gg['pin_wins']}/{gg['n_records']} = " \
                        f"{gg['frac']:.2f})"
            elif g == "D3":
                extra = (f" (frontier rung {gg['frontier_rung']})"
                         if gg["frontier_rung"] is not None
                         else " (no deep rung reaches the bar)")
            print(f"  GATE-{g}: {'PASS' if gg['pass'] else 'REFUTE'}"
                  f"{extra}")
        print(f"  === {gates['verdict']} gates PASS === "
              f"frontier rung: {gates['frontier_rung']}")
    out_path = args.out or OUT
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(dep, fh, indent=1)
    print(f"  deposited {out_path} ({time.time() - t0:.1f}s)")
    return dep


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["shallow", "d40", "d45", "d50",
                                      "d55", "d60", "all"],
                    default="all")
    ap.add_argument("--rung", type=float, default=None)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main(args)  # noqa: F841  (body: honor --smoke/--job/--rung/--out)
