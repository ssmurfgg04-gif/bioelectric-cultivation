#!/usr/bin/env python3
"""exp182 — UNIVERSAL SUBSTRATE: 100 MORE TARGETS (path 2's scale-up).

Stage 5 path 2 (the handoff ledger's LANDED status): S* = (64.0, 0.0)
carries the 10 deposited diverse targets at worst-case margin +5.391
(exp161). The registered scale-up: 100 FRESH targets. With CF-1 the
writable repertoire runs to -60, and exp172 priced the deep band
writable at the production cell — so the fresh targets span the FULL
widened repertoire, including the deep band S* has never been asked
to carry.

========================= PRE-REGISTRATION =========================
Committed BEFORE any run. Targets, protocol, and gates are fixed now.

THE TARGET SET (100 fresh programs, zero fitting):
  built by ONE pre-registered generator: rng = default_rng(182182);
  for t = 0..99: zone count k ~ {1: 3, 2: 4, 3: 2, 4: 1} (the
  exp161 diversity ladder, 1-4 zones); each zone a triple
  (start, end, value): start ~ U(0.02, 0.80), width ~ U(0.08, 0.16),
  value ~ U(-60.0, -15.0) — the FULL repertoire, deep band included,
  rounded to 1 dp; non-overlap enforced by construction (sorted
  starts, regenerated on collision — the generator is deterministic
  at the seed); values below -35 are EXPLICITLY WELCOME (that is the
  scale-up's point: S* vs the deep band). Target f built by exp94's
  spec_target_n on the MULTI 3-zone program's labeling (canon ==
  wildtype asserted per target, exp172's construction discipline).
  The 100 triples + f_sha256 deposited FIRST (the target manifest is
  the pre-registration artifact).

THE PROTOCOL (exp161's, verbatim): probe_margin and writable_3seed
at the locked substrate rung S* = (64.0, 0.0), seeds (1, 2, 3), the
substrate lock asserted per write (exp161's _lock_substrate).

GATES (each evaluated exactly once):

  GATE-V1 (the substrate lock) exp161's _lock_substrate fires on
           every write; the log carries 100 (rung, wiring-id) pairs
           all at S*.
  GATE-V2 (the scale-up bar) >= 90/100 targets writable at S*
           (writable_3seed: decode < 6.0 AND hold < 6.0 on 3/3
           seeds); the miss list deposited with per-target margins;
           zero rejections.
  GATE-V3 (the margin profile — the deliverable) worst-case margin
           over the 100 deposited; the margin-vs-depth profile
           (values binned at [-60,-50), [-50,-40), [-40,-30),
           [-30,-15]) deposited; the deposited 10-target margin
           (+5.391 worst) recorded as the reference line.
  GATE-V4 (hygiene) all errs finite; the canon == wildtype assert
           holds per target; no per-target tuning anywhere.

NO post-hoc tuning. A --smoke check (targets 0-2) is permitted
before the credited run and discarded.

DEPOSIT: results/exp182_substrate_100.json

RUN:
  python3 -m experiments.exp182_substrate_100            # full
  python3 -m experiments.exp182_substrate_100 --smoke    # check
  python3 -m experiments.exp182_substrate_100 --job V2
  # jobs: manifest | battery
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

from experiments.exp94_multizone_scale import (  # noqa: E402
    MULTI, labeling_bfs_n, spec_target_n,
)
from experiments.exp161_universal_substrate import (  # noqa: E402
    probe_margin, writable_3seed, _lock_substrate, _SUBSTRATE_LOG,
)

# ---- FIXED CONSTANTS ------------------------------------------------
S_STAR = (64.0, 0.0)
TARGET_SEED = 182182
N_TARGETS = 100
ZONE_COUNT_LADDER = {1: 3, 2: 4, 3: 2, 4: 1}
WIDE_LO = -60.0
WIDE_HI = -15.0
SCALEUP_BAR = 90                 # of 100

OUT = os.path.join(ROOT, "results", "exp182_substrate_100.json")
DEP161 = os.path.join(ROOT, "results", "exp161_universal_substrate.json")


def main() -> dict:
    # ---- BODY (written by the run agent; docstring/imports/constants
    # ---- byte-unchanged). The __main__ block calls main() with no
    # ---- arguments, so the body re-parses sys.argv with the SAME
    # ---- flags to honor --smoke/--job/--out.
    import hashlib
    import time

    import experiments.exp136_generator_v6 as g6
    from experiments.exp161_universal_substrate import _SUBSTRATE_FIXED
    from cultivation.compiler.anatomy import AnatomySpec, Zone

    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["manifest", "battery", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    t0 = time.time()

    # ---- THE TARGET GENERATOR (pre-registered; zero instrument calls)
    # Fixed RNG consumption order per target t (disclosed in deposit):
    #   1. one uniform -> zone count k against the cumulative ladder
    #      [0.30, 0.70, 0.90, 1.00] over k = 1..4 (weights {1:3, 2:4,
    #      3:2, 4:1});
    #   2. k starts ~ U(0.02, 0.80); 3. k widths ~ U(0.08, 0.16);
    #   4. k values ~ U(-60.0, -15.0);
    #   all three arrays rounded to 1 dp; zones sorted by start
    #   (stable); COLLISION = strict overlap after rounding
    #   (start[i+1] < end[i]); on collision the target's whole draw
    #   set (k + all triples) is REGENERATED from the same stream.
    def _gen(n_targets: int) -> list[dict]:
        rng = np.random.default_rng(TARGET_SEED)
        made: list[dict] = []
        for t in range(n_targets):
            canon = labeling_bfs_n(g6.A_CHAIN)
            # canon == wildtype asserted PER TARGET (exp172 discipline)
            assert np.array_equal(canon, g6.wildtype_target(g6.N)), \
                f"t{t}: canon mismatch vs the engine's wildtype"
            while True:
                u = rng.random()
                if u < 0.30:
                    k = 1
                elif u < 0.70:
                    k = 2
                elif u < 0.90:
                    k = 3
                else:
                    k = 4
                starts = np.round(rng.uniform(0.02, 0.80, size=k), 1)
                widths = np.round(rng.uniform(0.08, 0.16, size=k), 1)
                values = np.round(rng.uniform(WIDE_LO, WIDE_HI, size=k), 1)
                ends = np.round(starts + widths, 1)
                order = np.argsort(starts, kind="stable")
                triples = [(float(starts[i]), float(ends[i]),
                            float(values[i])) for i in order]
                if all(triples[j + 1][0] >= triples[j][1]
                       for j in range(k - 1)):
                    break                   # non-overlap by construction
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{j}")
                       for j, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp182-t{t:03d}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, g6.N)
            f_sha = hashlib.sha256(
                np.ascontiguousarray(f, dtype=np.float64).tobytes()
            ).hexdigest()
            made.append({"index": t, "zone_count": k, "triples": triples,
                         "vmin": min(v for _, _, v in triples),
                         "vmax": max(v for _, _, v in triples),
                         "f_sha256": f_sha, "f": f})
        return made

    def _triples(m: dict) -> list[tuple]:
        return [tuple(z) for z in m["triples"]]

    def _write(payload: dict) -> str:
        p = args.out or OUT
        os.makedirs(os.path.dirname(os.path.abspath(p)), exist_ok=True)
        with open(p, "w") as fh:
            json.dump(payload, fh, indent=1, default=float)
        return p

    # =========== --smoke: targets 0-2, permitted and DISCARDED =========
    if args.smoke:
        ms = _gen(3)
        _SUBSTRATE_FIXED[:] = [S_STAR, id(g6.A_CHAIN)]
        rows = []
        for m in ms:
            pm = probe_margin(m["f"], _triples(m), S_STAR)
            v = writable_3seed(m["f"], _triples(m), S_STAR)
            rows.append({"index": m["index"], "triples": m["triples"],
                         "probe_margin1": float(pm),
                         "writable": bool(v["writable"]),
                         "rejected": bool(v["rejected"]),
                         "margin3": float(v["margin3"])})
            print(f"  t{m['index']:3d} {m['triples']} probe {pm:+.3f} "
                  f"writable {v['writable']} margin3 {v['margin3']:+.3f}")
        checks = {
            "zero_rejections": all(not r["rejected"] for r in rows),
            "all_finite": all(np.isfinite(r["probe_margin1"])
                              and np.isfinite(r["margin3"]) for r in rows),
            "lock_log_3_all_S_star": bool(
                len(_SUBSTRATE_LOG) == 3
                and all(r == S_STAR for r, _ in _SUBSTRATE_LOG)),
        }
        ok = all(checks.values())
        print(f"=== exp182 SMOKE (targets 0-2, DISCARDED) === "
              f"{checks} -> {'OK' if ok else 'INSTRUMENT BUG'} "
              f"({time.time() - t0:.1f}s)")
        dep = {"exp": "exp182_substrate_100", "kind": "smoke",
               "discarded": True, "rows": rows, "checks": checks,
               "ok": ok}
        if args.out:
            _write(dep)
        return dep

    # ===================== the credited run ============================
    print(f"=== exp182: the universal substrate — {N_TARGETS} fresh "
          f"targets at S* = {list(S_STAR)} ===\n")

    # 0. the reference line (exp161's deposited 10-target battery)
    with open(DEP161) as fh:
        dep161 = json.load(fh)
    ref_worst = float(dep161["s_star_battery"]["worst_case_margin3"])
    ref_sstar = [float(x) for x in dep161["selection"]["S_star"]]
    assert ref_sstar == [S_STAR[0], S_STAR[1]], \
        "exp161's deposited S* != this module's S*"
    print(f"  reference line (exp161, 10 targets): worst-case m3 "
          f"{ref_worst:+.3f} at S* {ref_sstar}")

    # 1. the target manifest — generated BEFORE any instrument call
    manifest = _gen(N_TARGETS)
    realized_k: dict = {}
    for m in manifest:
        realized_k[m["zone_count"]] = realized_k.get(m["zone_count"], 0) + 1
    n_zone_vals = sum(m["zone_count"] for m in manifest)
    n_deep = sum(1 for m in manifest if m["vmin"] < -35.0)
    print(f"  manifest: {N_TARGETS} targets, {n_zone_vals} zones, "
          f"realized k {dict(sorted(realized_k.items()))} "
          f"(ladder {ZONE_COUNT_LADDER}), {n_deep} targets touch the "
          f"deep band (< -35)")
    manifest_block = [{k: v for k, v in m.items() if k != "f"}
                      for m in manifest]

    # 2. the manifest deposited FIRST (the pre-registration artifact)
    if args.job in ("manifest", "all"):
        p = _write({"experiment": "exp182_substrate_100",
                    "kind": "manifest", "deposited_first": True,
                    "target_seed": TARGET_SEED,
                    "n_targets": N_TARGETS,
                    "manifest": manifest_block})
        print(f"  manifest deposited FIRST -> {p}")
    if args.job == "manifest":
        return {"experiment": "exp182_substrate_100", "kind": "manifest",
                "manifest": manifest_block}

    # 3. the battery at the LOCKED substrate (exp161's protocol verbatim)
    _SUBSTRATE_FIXED[:] = [S_STAR, id(g6.A_CHAIN)]  # set ONCE, BEFORE any
    # verdict; _lock_substrate now RAISES on any per-target drift
    per = []
    for m in manifest:
        tr = _triples(m)
        pm = probe_margin(m["f"], tr, S_STAR)
        v = writable_3seed(m["f"], tr, S_STAR)
        row = v["row"]
        per.append({
            "index": m["index"], "zone_count": m["zone_count"],
            "triples": m["triples"], "vmin": m["vmin"], "vmax": m["vmax"],
            "f_sha256": m["f_sha256"],
            "probe_margin1": float(pm),
            "writable": bool(v["writable"]),
            "rejected": bool(v["rejected"]),
            "n_rejected": int(row["n_rejected"]),
            "margin3": float(v["margin3"]),
            "eV": row["eV"], "eT": row["eT"], "quad": row["quad"],
            "decode_errs": row["decode_errs"],
            "hold_errs": row["hold_errs"],
            "decode_err_mean": row["decode_err_mean"],
            "hold_err_mean": row["hold_err_mean"],
        })
        if (m["index"] + 1) % 10 == 0:
            print(f"  ... {m['index'] + 1}/{N_TARGETS} targets priced "
                  f"({time.time() - t0:.0f}s)", flush=True)

    # ---- GATE-V1 (the substrate lock): the log carries 100 (rung,
    # wiring-id) pairs ALL at S*; _lock_substrate fired on every write
    # (any drift would have raised inside writable_3seed)
    runs = [r for r, _ in _SUBSTRATE_LOG]
    v1 = bool(len(_SUBSTRATE_LOG) == N_TARGETS
              and all(r == S_STAR for r in runs)
              and all(w == id(g6.A_CHAIN) for _, w in _SUBSTRATE_LOG))

    # ---- GATE-V2 (the scale-up bar) --------------------------------
    n_writable = sum(int(p["writable"]) for p in per)
    n_rej_seeds = sum(int(p["n_rejected"]) for p in per)
    misses = [{"index": p["index"], "triples": p["triples"],
               "margin3": round(p["margin3"], 4),
               "probe_margin1": round(p["probe_margin1"], 4),
               "rejected": p["rejected"],
               "violated": [c for c, bad in [
                   ("audit", p["quad"] >= 6.0),
                   ("decode", max(p["decode_errs"]) >= 6.0),
                   ("hold", max(p["hold_errs"]) >= 6.0)] if bad]}
              for p in per if not p["writable"]]
    v2 = bool(n_writable >= SCALEUP_BAR and n_rej_seeds == 0)

    # ---- GATE-V3 (the margin profile — the deliverable) -------------
    margins = [p["margin3"] for p in per]
    worst = float(min(margins))
    mean_m = float(np.mean(margins))
    bins = [(-60.0, -50.0), (-50.0, -40.0), (-40.0, -30.0), (-30.0, -15.0)]
    profile = []
    for lo, hi in bins:
        tv: list = []
        nv = 0
        for p in per:
            inb = [v for (_s, _e, v) in p["triples"]
                   if lo <= v < hi or (hi == -15.0 and v == hi)]
            if inb:
                nv += len(inb)
                tv.append(p["margin3"])
        profile.append({
            "bin": f"[{lo:g},{hi:g}]" if hi == -15.0
                   else f"[{lo:g},{hi:g})",
            "n_zone_values": nv, "n_targets": len(tv),
            "worst_margin3": round(float(min(tv)), 4) if tv else None,
            "mean_margin3": round(float(np.mean(tv)), 4) if tv else None})
    v3 = bool(len(profile) == 4 and len(per) == N_TARGETS
              and np.isfinite(worst))

    # ---- GATE-V4 (hygiene) ------------------------------------------
    all_fin = bool(
        all(np.isfinite(p["probe_margin1"]) for p in per)
        and all(np.isfinite(p["quad"]) and np.isfinite(p["eV"])
                and np.isfinite(p["eT"])
                and all(np.isfinite(x) for x in p["decode_errs"])
                and all(np.isfinite(x) for x in p["hold_errs"])
                for p in per))
    canon_asserts = N_TARGETS      # _gen raised otherwise, per target
    no_tuning = True               # structural: S* fixed once BEFORE any
    # verdict; the generator ran before ANY instrument call; zero
    # per-target knobs (the log's constancy is V1's evidence)
    v4 = bool(all_fin and canon_asserts == N_TARGETS and no_tuning)

    gates = {"V1": v1, "V2": v2, "V3": v3, "V4": v4}
    npass = int(sum(gates.values()))

    out = {
        "experiment": "exp182_substrate_100",
        "claim": ("Stage 5 path 2's scale-up: the locked universal "
                  "substrate S* = (64.0, 0.0) carries 100 FRESH targets "
                  "spanning the FULL widened repertoire [-60, -15] at "
                  "the 6.0 mV bar (>= 90/100), the margin-vs-depth "
                  "profile as the deliverable"),
        "pre_registered": {
            "target_generator": {
                "rng": f"np.random.default_rng({TARGET_SEED})",
                "zone_count_ladder": ZONE_COUNT_LADDER,
                "zone_draws": "start ~ U(0.02, 0.80), width ~ "
                              "U(0.08, 0.16), value ~ U(-60.0, -15.0)",
                "rounding": "1 dp on start/width/value",
                "non_overlap": "sorted starts; collision = strict "
                               "overlap after rounding; the target's "
                               "full draw set regenerated on collision",
                "rng_order_disclosure": "per target: one uniform for k "
                                        "vs cumulative [0.30, 0.70, "
                                        "0.90, 1.00]; then k starts; "
                                        "then k widths; then k values",
                "f_construction": "exp94 spec_target_n on the MULTI "
                                  "program's labeling "
                                  "(labeling_bfs_n(A_CHAIN)); canon == "
                                  "wildtype_target(100) asserted PER "
                                  "TARGET (exp172 discipline)",
            },
            "protocol": "exp161's probe_margin + writable_3seed "
                        "VERBATIM at the locked rung S* = (64.0, 0.0), "
                        "seeds (1, 2, 3), _lock_substrate per write",
            "scaleup_bar": SCALEUP_BAR,
            "gates": {
                "V1": "_lock_substrate fires on every write; the log "
                      "carries 100 (rung, wiring-id) pairs all at S*",
                "V2": ">= 90/100 writable at S* (decode < 6.0 AND hold "
                      "< 6.0 on 3/3 seeds); miss list deposited with "
                      "per-target margins; zero rejections",
                "V3": "worst-case margin over the 100 deposited; "
                      "margin-vs-depth profile binned [-60,-50) "
                      "[-50,-40) [-40,-30) [-30,-15]; exp161's "
                      "10-target worst margin (+5.391) as the "
                      "reference line",
                "V4": "all errs finite; canon == wildtype asserted per "
                      "target; no per-target tuning anywhere",
            },
        },
        "reference_line": {
            "source": "results/exp161_universal_substrate.json",
            "S_star": ref_sstar, "n_targets": 10,
            "worst_case_margin3": round(ref_worst, 4)},
        "manifest": {"target_seed": TARGET_SEED,
                     "n_targets": N_TARGETS,
                     "n_zone_values": n_zone_vals,
                     "realized_zone_counts": {str(k): realized_k[k]
                                              for k in sorted(realized_k)},
                     "n_targets_touching_deep_band": n_deep,
                     "targets": manifest_block},
        "battery": {
            "S_star": list(S_STAR),
            "seeds": [1, 2, 3],
            "n_writable": n_writable,
            "writable_indices": [p["index"] for p in per
                                 if p["writable"]],
            "miss_list": misses,
            "n_rejected_seeds": n_rej_seeds,
            "worst_case_margin3": round(worst, 4),
            "mean_margin3": round(mean_m, 4),
            "per_target": [{**p,
                            "probe_margin1": round(p["probe_margin1"], 4),
                            "margin3": round(p["margin3"], 4)}
                           for p in per],
        },
        "margin_profile": {"bins": [b["bin"] for b in profile],
                           "per_bin": profile,
                           "note": "a target's margin enters every bin "
                                   "containing >= 1 of its zone values"},
        "substrate_log": {"n_writes": len(_SUBSTRATE_LOG),
                          "all_at_S_star": v1,
                          "runs_unique": sorted({str(list(r))
                                                 for r in runs})},
        "gates": gates,
        "gates_passed": f"{npass}/4",
        "smoke_disclosure": ("a --smoke check (targets 0-2) ran before "
                             "the credited run and was discarded (no "
                             "file; separate process)"),
        "wall_s": round(time.time() - t0, 1),
    }
    p = _write(out)
    for g in ("V1", "V2", "V3", "V4"):
        extra = ""
        if g == "V1":
            extra = f" ({len(_SUBSTRATE_LOG)} writes, all at S*)"
        elif g == "V2":
            extra = f" ({n_writable}/{N_TARGETS}, rejections {n_rej_seeds})"
        elif g == "V3":
            extra = (f" (worst {worst:+.3f} vs exp161 reference "
                     f"{ref_worst:+.3f})")
        elif g == "V4":
            extra = (f" (all finite, canon asserted {canon_asserts}/"
                     f"{N_TARGETS})")
        print(f"  GATE-{g}: {'PASS' if gates[g] else 'REFUTE'}{extra}")
    print(f"  === {npass}/4 gates PASS === S* {list(S_STAR)}: "
          f"{n_writable}/{N_TARGETS} writable, worst-case margin "
          f"{worst:+.3f} (mean {mean_m:+.3f})")
    print(f"  deposited {p} ({out['wall_s']}s)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--job", choices=["manifest", "battery", "all"],
                    default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    _res = main()  # noqa: F841  (body: honor --smoke/--job/--out)
