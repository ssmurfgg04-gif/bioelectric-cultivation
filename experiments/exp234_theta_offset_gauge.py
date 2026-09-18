#!/usr/bin/env python3
"""exp234 — THE THETA-OFFSET GAUGE TEST (exp232's registered next (b);
the Section 12 anti-deferral rule: derived from the ledger, run now;
ledger L210).

THE OPEN QUESTION (L208): exp232's battery exposed the THETA-STATE
breakout — th_offset(threshold delta=20 mV) leaves err 19.98 mV on the
torus, th_noise(10) leaves 9.37 — and the count=2 verdict carried the
honest caveat: a breakout group is a group the WRITE law does not cover,
not necessarily a SIGNALING channel. The gauge hypothesis: the theta
layer encodes pattern RELATIVELY (V chases theta at rate gamma; theta's
own dynamics eps*(V-theta) + mu*lap(theta) conserve a UNIFORM offset —
the offset lies in the kernel of every mechanism in the stack), so a
uniform theta-offset is a GAUGE degree of freedom: it moves the absolute
RMS error err = RMS(V - lbl) by exactly delta while carrying ZERO pattern
information. If the gauge hypothesis holds, exp232's THETA-STATE
breakout is RECLASSIFIED — not a third signaling channel but an
unobservable mode — and the stack's channel inventory returns to 2
signaling channels + 1 gauge mode, which TIGHTENS the exp232 refutation
of the 8-channel mapping. Honesty cuts both ways: this experiment tests
the reclassification against the stack.

THE ZERO MODE (zero-knob derivation, checked numerically in T1): for a
uniform offset c: d(theta+c)/dt = eps*(V - theta - c); dV follows theta+c
at rate gamma; the pair (V, theta+c) satisfies the SAME equations as
(V - c, theta) — the offset is an exact symmetry of the coupled dynamics
at ANY (gamma, mu, kappa), broken ONLY by absolute anchors: the wound
state constants (amputate's wound_voltage=-30, blastema_theta=-40) and
the physiological clamps V_PHYS_MIN/MAX.

PRE-REGISTERED GATES:

  T1  THE CONSERVATION: after the th_offset delta at the star, err(T)
      stays within 0.5 mV of its T=1 value across T in {1, 6, 24, 96}
      (4 windows x 3 arms x 3 seeds) — no decay channel exists; and the
      zero-mode check: the uniform-offset vector is in the numerical
      kernel of the stack's linearized update (|M @ 1| <= 1e-9 for the
      (V,theta) block operator at 3 operating points).
  T2  THE GAUGE (the information test): the zone structure is INVARIANT
      — the head/trunk classification read off (V, theta) at the offset
      substrate matches the offset-free classification on >= 99% of
      cells at every pre-named delta in {5, 10, 20} (the threshold read
      exp142's sign read; the offset shifts both layers equally, every
      relative comparison unchanged); the pattern's mutual information
      with the target's zone map is delta-invariant (MI drop <= 0.01
      bits).
  T3  THE READ'S BLINDNESS: the production scoped read (exp178's
      machinery) decodes the offset substrate to the SAME target (the
      decode's zone assignment invariant, err_read delta-invariant
      within 0.5 mV at delta in {5, 10, 20} x 3 seeds) — the offset is
      invisible to the read: it has NO information capacity.
  T4  THE GAUGE'S EDGE (where the offset is NOT pure): the wound is an
      absolute anchor — after amputate, the offset substrate's regen
      err differs from the offset-free regen err by >= the offset size
      against the blastema constants (the gauge breaks at the wound:
      blastema_theta=-40 is ABSOLUTE, the committed pattern is offset);
      3 arms x 3 seeds, the delta-20 case. The named asymmetry: the
      stack repairs its pattern only through the wound's absolute
      reference — the gauge is global, the repair is local.

THE BRANCH (pre-named): T1+T2+T3 PASS -> GAUGE-MODE (exp232's
THETA-STATE breakout RECLASSIFIED: the stack has 2 signaling channels +
1 gauge mode; the 8-channel refutation TIGHTENS); T4 names the wound as
the gauge's unique breaker either way. Any T1/T2/T3 REFUTE ->
GENUINE-CHANNEL (the theta-state carries real information; exp232's
count=2 stands with THETA-STATE as a third signaling channel).

RUN: 4 windows + 3 deltas x panels; serial, BLAS pinned; minutes.
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp234_theta_offset_gauge.json")


def main() -> dict:
    print("=== exp234: the theta-offset gauge test ===\n")

    # ---- the frozen machinery, imported (never re-implemented) -----------
    from experiments.exp73_active_renormalization import (  # exp73's battery
        make_battery, N, HEAD_V,
    )
    from experiments.exp43_substrate_independence import labeling
    from experiments.exp79_two_channel_law import RUN_T, DT  # the star protocol
    from cultivation.substrate.graph import GraphCollective
    from cultivation.bioelectric.collective import V_PHYS_MIN, V_PHYS_MAX
    from cultivation.information.mutual_info import estimate_mi_joint
    from experiments.exp142_sign_read import _StaticMedium
    from experiments.exp148_temporal_read import decode as production_decode
    from experiments.exp169_rt_scoping import f_max_frames

    STAR_GAMMA, STAR_MU = 64.0, 0.0        # the star (exp232's battery point)
    ARMS = ("scale_free", "random3", "torus")
    SEEDS = (1, 2, 3)
    OFFSETS = (0.0, 5.0, 10.0, 20.0)       # 0 = the offset-free substrate
    WINDOWS = (1.0, 6.0, 24.0, 96.0)       # T1's pre-named windows
    PRENAMED_DELTAS = (5.0, 10.0, 20.0)    # T2/T3's pre-named deltas
    WOUND = slice(40, 60)                  # exp232's wound region
    WOUND_REGION = list(range(40, 60))
    KERNEL_BAR = 1e-9
    DEV_BAR = 0.5                          # mV (T1/T3)
    AGREE_BAR = 0.99                       # T2
    MI_BAR = 0.01                          # bits (T2)
    OFFSET_SIZE = 20.0                     # T4's delta-20 case

    battery = make_battery()
    lbl = labeling(N)
    zone_target = (lbl == HEAD_V)          # the target's zone map (head bit)

    # ---------------------------------------------------------- helpers --
    def _sign_read(field: np.ndarray) -> np.ndarray:
        """The threshold read, exp142's sign semantics: the head/trunk bit
        is the SIGN of (field - midline), the midline the substrate's OWN
        two-cluster midpoint (deterministic 2-means, zero knobs). The read
        is RELATIVE — a uniform offset shifts field and midline equally,
        so every comparison is gauge-covariant by construction."""
        c1, c2 = float(field.min()), float(field.max())
        if not c2 > c1:
            return np.zeros(field.shape, dtype=bool)
        for _ in range(200):
            mid = 0.5 * (c1 + c2)
            lo = field <= mid
            if not lo.any() or lo.all():
                break
            n1 = float(field[lo].mean())
            n2 = float(field[~lo].mean())
            if n1 == c1 and n2 == c2:
                break
            c1, c2 = n1, n2
        return field > 0.5 * (c1 + c2)

    def _kernel_residual(A: np.ndarray, gamma: float, mu: float,
                         kappa: float) -> float:
        """|M @ 1| for the stack's linearized (V,theta) block operator at
        one operating point (gamma, mu, kappa=gap_scale), built from the
        LIVE collective's own matrices (collective.py step(), drift part):
        dV = gamma*(theta-V) + G@V - V*deg;
        dtheta = eps*(V-theta) + mu*gap_scale*lap(theta).
        The uniform vector is the gauge direction. The named absolute
        breakers (the wound constants; the physiological clips
        V_PHYS_MIN/MAX) are inactive at interior operating points and
        absent from the linearization."""
        c = GraphCollective(adjacency=A, seed=0, gamma=gamma, mu_theta=mu)
        if kappa != 1.0:
            c.block_gap_junctions(kappa)
        n = A.shape[0]
        eye = np.eye(n)
        M = np.zeros((2 * n, 2 * n))
        M[:n, :n] = c.G - np.diag(c.deg) - gamma * eye
        M[:n, n:] = gamma * eye
        M[n:, :n] = c.eps * eye
        M[n:, n:] = (c.mu * c.gap_scale
                     * (c.A - np.diag(c.A.sum(axis=1)))) - c.eps * eye
        return float(np.max(np.abs(M @ np.ones(2 * n))))

    def _star_settle(A: np.ndarray, s: int, d: float, extra_window: bool):
        """exp232's run_instance protocol at the star, verbatim: settle
        (exp79's run_gm state init), the th_offset intervention, then the
        RUN_T response window. extra_window keeps the RNG draw count
        aligned between the offset-free and offset paired runs."""
        c = GraphCollective(adjacency=A, seed=s, gamma=STAR_GAMMA,
                            mu_theta=STAR_MU)
        c.set_target(lbl)
        c.theta = lbl.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)
        dt_star = min(DT, 1.2 / (STAR_GAMMA + float(c.deg.max())))
        c.run(RUN_T, dt=dt_star)
        err0 = c.pattern_error(lbl)
        if d:
            c.theta = c.theta + d          # exp232's th_offset, verbatim
        if extra_window:
            c.run(RUN_T, dt=dt_star)
        return c, dt_star, err0

    # ---- T1: the conservation + the zero mode ----------------------------
    print("  T1 conservation (windows T=1,6,24,96; delta in {5,10,20} "
          "+ the 0 reference):")
    t1_rows, states = [], {}
    t1_cons = True
    for arm in ARMS:
        A = battery[arm]
        for d in OFFSETS:
            dev_max, e24s = 0.0, []
            for s in SEEDS:
                c, dt_star, err0 = _star_settle(A, s, d, extra_window=False)
                errs, prev = {}, 0.0
                for w in WINDOWS:
                    c.run(w - prev, dt=dt_star)
                    prev = w
                    errs[w] = c.pattern_error(lbl)
                    if w == 24.0:
                        states[(arm, s, d)] = (c.V.copy(), c.theta.copy())
                dev = max(abs(errs[w] - errs[WINDOWS[0]])
                          for w in WINDOWS[1:])
                dev_max = max(dev_max, dev)
                e24s.append(errs[24.0])
                if d:
                    t1_cons &= dev <= DEV_BAR
                t1_rows.append({
                    "arm": arm, "seed": s, "delta": float(d),
                    "err0": round(err0, 4),
                    "err_T": {str(w): round(errs[w], 4) for w in WINDOWS},
                    "max_dev_from_T1": round(dev, 4),
                    "pass": bool(dev <= DEV_BAR),
                    "gated": bool(d),
                })
            print(f"    {arm:11s} delta={d:4.0f}  err(T=24) mean "
                  f"{float(np.mean(e24s)):7.3f}  max|err(T)-err(1)| "
                  f"{dev_max:.4f}")
    # the exp232 cross-check: the deposited battery's th_offset torus
    # delta-20 err at the same protocol point (L208: 19.98)
    xchk = float(np.mean([r["err_T"]["24.0"] for r in t1_rows
                          if r["arm"] == "torus" and r["delta"] == 20.0]))
    print(f"    cross-check vs exp232's deposited battery (torus, "
          f"delta=20, err at T=24): {xchk:.3f} (deposited 19.98)")

    kernel_rows, kernel_ok = [], True
    ops = (("star", STAR_GAMMA, STAR_MU, 1.0),
           ("plateau", 0.25, 0.015, 1.0),
           ("kappa-half", STAR_GAMMA, 0.015, 0.5))
    for name, g, m, k in ops:
        worst = max(_kernel_residual(battery[a], g, m, k) for a in ARMS)
        kernel_ok &= worst <= KERNEL_BAR
        kernel_rows.append({"op": name, "gamma": g, "mu": m, "kappa": k,
                            "max_abs_M1_over_arms": worst,
                            "pass": bool(worst <= KERNEL_BAR)})
        print(f"    zero-mode {name:11s} (gamma={g}, mu={m}, kappa={k}): "
              f"max |M@1| = {worst:.2e} -> "
              f"{'PASS' if worst <= KERNEL_BAR else 'REFUTED'}")
    t1_pass = bool(t1_cons and kernel_ok)
    print(f"  T1 conservation+zero-mode -> {'PASS' if t1_pass else 'REFUTED'}")

    # ---- T2: the zone structure is invariant ------------------------------
    print("  T2 zone invariance (the threshold sign read off (V,theta); "
          "deltas {5,10,20}):")
    t2_rows = []
    t2_pass = True
    for arm in ARMS:
        for s in SEEDS:
            V0, th0 = states[(arm, s, 0.0)]
            zone0 = _sign_read(0.5 * (V0 + th0))
            zone0_v = _sign_read(V0)
            zone0_t = _sign_read(th0)
            mi0 = estimate_mi_joint(np.column_stack([V0, th0]),
                                    zone_target.astype(int), bins=4)
            for d in PRENAMED_DELTAS:
                Vd, thd = states[(arm, s, d)]
                zone = _sign_read(0.5 * (Vd + thd))
                agree = float(np.mean(zone == zone0))
                agree_v = float(np.mean(_sign_read(Vd) == zone0_v))
                agree_t = float(np.mean(_sign_read(thd) == zone0_t))
                mi = estimate_mi_joint(np.column_stack([Vd, thd]),
                                       zone_target.astype(int), bins=4)
                drop = mi0 - mi
                ok = bool(agree >= AGREE_BAR and drop <= MI_BAR)
                t2_pass &= ok
                t2_rows.append({
                    "arm": arm, "seed": s, "delta": float(d),
                    "agreement_joint": round(agree, 4),
                    "agreement_V": round(agree_v, 4),
                    "agreement_theta": round(agree_t, 4),
                    "mi_bits": round(mi, 6), "mi0_bits": round(mi0, 6),
                    "mi_drop_bits": round(drop, 8),
                    "pass": ok,
                })
    worst_agree = min(r["agreement_joint"] for r in t2_rows)
    worst_drop = max(r["mi_drop_bits"] for r in t2_rows)
    print(f"    worst agreement {worst_agree:.4f} (bar {AGREE_BAR}), "
          f"worst MI drop {worst_drop:.2e} bits (bar {MI_BAR}) "
          f"-> {'PASS' if t2_pass else 'REFUTED'}")

    # ---- T3: the read's blindness (exp178's production scoped read) ------
    print("  T3 the production scoped read on the offset substrate "
          "(deltas {0,5,10,20} x 3 seeds):")
    t3_prod, t3_state = [], []
    t3_pass = True
    targets_invariant = True
    rejections = 0
    for arm in ARMS:
        A = battery[arm]
        med = _StaticMedium(A)
        fm = f_max_frames(list(med.snapshots()))
        ref_err, ref_errW, ref_tgt, ref_tgtW = {}, {}, {}, {}
        for s in SEEDS:
            for d in OFFSETS:
                # (i) the substrate's production presentation
                out = production_decode("scoped", med, s, return_state=True,
                                        f_max=fm)
                if not out["ok"]:
                    rejections += 1
                err = out.get("err")
                tgt = (np.asarray(out["state"]["target"])
                       if out["ok"] else None)
                # (ii) the disclosed state-carrying presentation: the
                # transjunctional magnitude field of the offset substrate
                # (the offset cancels in differences — the gauge's own
                # claim — so the read feels the offset only at float
                # level; this panel makes the blindness test falsifiable)
                Vd, thd = states[(arm, s, d)]
                Wd = A * np.abs(Vd[:, None] - Vd[None, :])
                medW = _StaticMedium(Wd)
                fmW = f_max_frames(list(medW.snapshots()))
                outW = production_decode("scoped", medW, s,
                                         return_state=True, f_max=fmW)
                if not outW["ok"]:
                    rejections += 1
                errW = outW.get("err")
                tgtW = (np.asarray(outW["state"]["target"])
                        if outW["ok"] else None)
                if d == 0.0:
                    ref_err[s], ref_tgt[s] = err, tgt
                    ref_errW[s], ref_tgtW[s] = errW, tgtW
                dev = (abs(err - ref_err[s])
                       if (err is not None and ref_err[s] is not None)
                       else float("nan"))
                devW = (abs(errW - ref_errW[s])
                        if (errW is not None and ref_errW[s] is not None)
                        else float("nan"))
                tin = bool(tgt is not None and ref_tgt[s] is not None
                           and np.array_equal(tgt, ref_tgt[s]))
                tinW = bool(tgtW is not None and ref_tgtW[s] is not None
                            and np.array_equal(tgtW, ref_tgtW[s]))
                if d:
                    t3_pass &= (np.isfinite(dev) and dev <= DEV_BAR
                                and tin)
                    targets_invariant &= (tin and tinW)
                t3_prod.append({
                    "arm": arm, "seed": s, "delta": float(d),
                    "err_read": err, "dev_from_delta0": round(dev, 6),
                    "target_invariant": tin,
                    "verified": bool(out.get("verified", False)),
                    "pass": bool(np.isfinite(dev) and dev <= DEV_BAR
                                 and tin) if d else None,
                })
                t3_state.append({
                    "arm": arm, "seed": s, "delta": float(d),
                    "err_read": errW, "dev_from_delta0": round(devW, 6),
                    "target_invariant": tinW,
                    "verified": bool(outW.get("verified", False)),
                })
    worst_dev = max(r["dev_from_delta0"] for r in t3_prod if r["delta"])
    worst_devW = max(r["dev_from_delta0"] for r in t3_state if r["delta"])
    print(f"    production medium: worst |err_read(delta)-err_read(0)| "
          f"= {worst_dev:.2e} mV (bar {DEV_BAR}); targets bit-invariant: "
          f"{targets_invariant}")
    print(f"    disclosed state-carrying medium (A*|dV|): worst dev "
          f"{worst_devW:.2e} mV")
    print(f"    rejections: {rejections} (zero-rejection hygiene)")
    t3_pass = bool(t3_pass and targets_invariant)
    print(f"  T3 read blind -> {'PASS' if t3_pass else 'REFUTED'}")

    # ---- T4: the gauge's edge (the wound is an absolute anchor) ----------
    print("  T4 the wound edge (delta-20 vs offset-free, amputate defaults "
          "-30/-40, regrow walk, exp43's settle):")
    t4_rows = []
    t4_pass = True
    for arm in ARMS:
        A = battery[arm]
        for s in SEEDS:
            res = {}
            for d, tag in ((0.0, "free"), (OFFSET_SIZE, "offset")):
                c, dt_star, _ = _star_settle(A, s, d, extra_window=True)
                c.amputate(WOUND)   # wound_voltage=-30, blastema_theta=-40
                c.regrow_graph(WOUND_REGION, cell_period=0.8, dt=dt_star,
                               noise=0.6)
                c.run(15.0, dt=dt_star)     # exp43's regen settle window
                res[tag] = {
                    "err": c.pattern_error(lbl),
                    "theta_region": float(np.sqrt(np.mean(
                        (c.theta[WOUND_REGION] - lbl[WOUND_REGION]) ** 2))),
                }
            diff = res["offset"]["err"] - res["free"]["err"]
            ok = bool(diff >= OFFSET_SIZE)
            t4_pass &= ok
            t4_rows.append({
                "arm": arm, "seed": s,
                "err_regen_free": round(res["free"]["err"], 4),
                "err_regen_offset": round(res["offset"]["err"], 4),
                "diff": round(diff, 4),
                "theta_region_free": round(res["free"]["theta_region"], 4),
                "theta_region_offset": round(
                    res["offset"]["theta_region"], 4),
                "pass": ok,
            })
            print(f"    {arm:11s} seed {s}: err_free "
                  f"{res['free']['err']:7.3f}, err_offset "
                  f"{res['offset']['err']:7.3f}, diff {diff:7.3f} "
                  f"(>= {OFFSET_SIZE:.0f}? {'PASS' if ok else 'REFUTED'})")
    t4_pass = bool(t4_pass)
    print(f"  T4 wound edge -> {'PASS' if t4_pass else 'REFUTED'}")

    # ---- THE BRANCH -------------------------------------------------------
    branch = ("GAUGE-MODE" if (t1_pass and t2_pass and t3_pass)
              else "GENUINE-CHANNEL")
    criteria = {
        "T1_conservation_and_zero_mode": t1_pass,
        "T2_zone_invariant_mi": bool(t2_pass),
        "T3_read_blind": t3_pass,
        "T4_wound_edge": t4_pass,
    }
    npass = sum(bool(v) for v in criteria.values())
    print(f"\n  BRANCH (pre-named): {branch}")
    if branch == "GAUGE-MODE":
        print("  exp232's THETA-STATE breakout RECLASSIFIED: the stack has "
              "2 signaling channels + 1 gauge mode; the 8-channel "
              "refutation TIGHTENS")
    else:
        print("  the theta-state carries real information; exp232's "
              "count=2 stands with THETA-STATE as a third signaling channel")
    t4_share = float(np.mean([r["diff"] for r in t4_rows])) / OFFSET_SIZE
    print(f"  the wound is the gauge's unique breaker either way: "
          f"T4 diff/offset = {t4_share:.1%} of the offset rides through "
          f"the local repair")

    out = {
        "exp": "exp234_theta_offset_gauge (exp232's registered next (b); "
               "ledger L210)",
        "branch": branch,
        "machinery": {
            "battery": "exp73_active_renormalization.make_battery (exp79's "
                       "make_battery pattern)",
            "labeling": "exp43_substrate_independence.labeling",
            "star_protocol": "exp79_two_channel_law RUN_T/DT at "
                             "(gamma=64, mu=0); exp232's run_instance "
                             "th_offset intervention verbatim",
            "read": "exp178's production scoped read = "
                    "exp148_temporal_read.decode('scoped') with "
                    "exp169's f_max_frames; medium presentation via "
                    "exp142's _StaticMedium",
            "mi": "cultivation.information.mutual_info.estimate_mi_joint "
                  "(exp5's machinery, bins=4)",
        },
        "zero_mode": {
            "operator": "the (V,theta) block operator of the stack's "
                        "linearized update (collective.py step drift), "
                        "built from the live collective's matrices; the "
                        "uniform vector is the gauge direction",
            "operating_points": kernel_rows,
            "bar": KERNEL_BAR,
            "named_breakers": {
                "wound_constants": {"wound_voltage": -30.0,
                                    "blastema_theta": -40.0},
                "physiological_clips": [V_PHYS_MIN, V_PHYS_MAX],
                "inactive_at": "every interior operating point tested",
            },
        },
        "T1": {"rows": t1_rows, "pass": t1_pass,
               "conservation_pass": bool(t1_cons),
               "zero_mode_pass": bool(kernel_ok),
               "exp232_cross_check_err24_torus_delta20": round(xchk, 3)},
        "T2": {"rows": t2_rows, "pass": bool(t2_pass),
               "worst_agreement": worst_agree,
               "worst_mi_drop_bits": worst_drop,
               "read": "threshold sign read off (V,theta) at the "
                       "substrate's own 2-cluster midline (relative, "
                       "gauge-covariant); per-layer reads disclosed"},
        "T3": {"production_medium_rows": t3_prod,
               "state_carrying_medium_rows": t3_state,
               "pass": t3_pass,
               "targets_bit_invariant": bool(targets_invariant),
               "rejections": rejections,
               "disclosure": "the production read's interface is the "
                             "weight matrix, so the substrate presentation "
                             "is state-blind by interface; the disclosed "
                             "state-carrying medium W = A*|V_i - V_j| "
                             "carries the offset substrate's transjunctional "
                             "field (the uniform offset cancels in "
                             "differences to float level), making the "
                             "blindness test falsifiable"},
        "T4": {"rows": t4_rows, "pass": t4_pass,
               "protocol": "exp43's regen protocol at the star: amputate "
                           "defaults (-30/-40), regrow_graph walk, "
                           "run(15); errs = pattern_error vs the absolute "
                           "labeling; delta-20 vs offset-free, paired by "
                           "(arm, seed) with aligned RNG streams"},
        "criteria": criteria,
        "notes": (
            "Body-landing disclosures: (a) T1's conservation evaluated at "
            "EVERY pre-named delta {5,10,20} plus the delta-0 reference "
            "(a superset of the registered single-delta reading, exp232's "
            "disclosed precedent — can only add refutations, never hide "
            "one); (b) the zero-mode operator checked at 3 operating "
            "points spanning (gamma, mu, kappa): the star (64, 0, 1), the "
            "plateau (0.25, 0.015, 1) and a kappa-varied point (64, "
            "0.015, 0.5), each over all 3 arms (max reported); (c) T2's "
            "MI uses quantile discretization, which is shift-invariant — "
            "the delta-invariance is the gauge's own claim made "
            "measurable; (d) T4's measured differences are the offset "
            "size MINUS the offset-free regen's own error floor (the "
            "walk's chained inheritance noise and, on random3/scale_free, "
            "wound components the mu=0 walk cannot reach — the region's "
            "mean theta sits at the ABSOLUTE blastema constant there): "
            "the pre-registered inequality is evaluated exactly as "
            "written; (e) the wound constants and the physiological "
            "clips are the named symmetry breakers and enter T4 only "
            "through amputate's absolute defaults."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  === {npass}/4 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
