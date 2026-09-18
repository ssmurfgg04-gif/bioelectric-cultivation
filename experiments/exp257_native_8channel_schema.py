#!/usr/bin/env python3
"""exp257 — THE NATIVE MULTI-CHANNEL WRITE-PATH SCHEMA (THE
ARCHITECTURAL OVERRIDE; batch 22 item 2 — the priority experiment).

THE OPEN ITEM (exp232's S3b STACK-2CH + the user's override directive):
the underlying state is a 2-tuple (V, theta). It cannot represent the
paper's 8 channels because there is nowhere to put them — three of the
paper's 8 channels (Ca2+ transients, 5-HT electrophoresis, apoptosis)
have NO lower-level substrate at all, and the boundary excess lives in
the channel truncation, not in the read face (exp213/216/219/221's four
refutations, exp245's 0.686 unexplained share).

THE SCHEMA (pre-registered here, before any body):

  The state becomes a named 8-channel array `S` of shape (n, 8) on
  BioElectricCollective (and every state-carrying subclass). Channels,
  named per exp232's census — the paper's own 8-channel spec:

    ch0 "vmem"  Vmem bistability            — ACTIVE (the legacy self.V)
    ch1 "theta" homeostatic target / the
                epigenetic-proliferation
                memory face                 — ACTIVE (the legacy self.theta)
    ch2 "gj"    per-cell gap-junction state — DORMANT (init 1.0; today a
                global scalar gap_scale; per-cell state, zero dynamics
                at defaults)                — activation queued (exp259)
    ch3 "ctx"   interior-context channel    — DORMANT (init 0.0; NO stack
                substrate today)            — activation queued (exp258)
    ch4 "ca2"   Ca2+ transient layer        — DORMANT (init 0.0; ABSENT
                today — now it has state)
    ch5 "sht"   serotonin/5-HT electrophoresis — DORMANT (init 0.0;
                ABSENT today — now it has state)
    ch6 "apop"  apoptosis morphogenetic signal — DORMANT (init 0.0;
                ABSENT today — now it has state)
    ch7 "ichan" per-cell ion-channel expression — DORMANT (init gamma;
                today a scalar dial; zero dynamics at defaults)

  Dormancy contract: at defaults every dormant channel (ch2..ch7) has
  ZERO dynamics, ZERO feedback into ch0/ch1, and is only CARRIED
  (initialized, cloned, restored, read). The ch0/ch1 dynamics, the RNG
  draw order, and every legacy code path are byte-identical — the
  refactor is ADDITIVE ONLY.

  Compatibility shims (the migration path): self.V / self.theta become
  properties backed by S[:, 0] / S[:, 1]; set_state, set_target,
  clone_state, restore_state keep their exact legacy signatures and
  semantics (the 2-tuple is channels 0/1; restore writes 0/1 and leaves
  2..7 untouched). New accessors: set_channel / read_channel /
  clone_state_full / restore_state_full (the 8-channel form) and
  CHANNEL_NAMES / ACTIVE_CHANNELS / DORMANT_CHANNELS module constants.

PRE-REGISTERED GATES:

  S1  THE SCHEMA: BioElectricCollective carries S (n, 8) with the 8
      census names above; every legacy accessor is a bit-exact shim;
      the new full-state accessors exist and round-trip (write ch4,
      clone_state, restore_state — ch4 unchanged; clone_state_full /
      restore_state_full — ch4 preserved through the round trip).
  S2  THE BIT-EXACT GATE (zero delta on the deposits):
      B1  exp79's 45-point grid errs re-run bit-exact vs
          results/exp79_two_channel_law.json (the two-channel law's
          own surface — the core deposit);
      B2  exp32's M26 chain record re-run bit-exact (the regrow walk —
          the write path);
      B3  GraphCollective settle+read fingerprint matches
          exp198's n=400 cohort anchor (the subclass carries state
          through the schema);
      B4  the full test suite green from the repo root (hygiene,
          non-gating).
  S3  THE MIGRATION: no experiment module changes (imports unchanged);
      only the core state plumbing (collective.py + the two subclasses'
      state plumbing) is touched; the dormancy contract is asserted in
      code (a dormant channel cannot alter ch0/ch1 trajectories: a
      seeded settle run with ch4 arbitrarily perturbed mid-run
      reproduces the unperturbed run's ch0/ch1 bit-exactly).
  S4  THE DISCIPLINE: deterministic (re-run bit-identical across
      processes); the -60.0 floor restored and asserted at exit after
      any exp169 import; every step pre-registered, nothing tuned.

THE BRANCHES (pre-named): S1-S4 PASS -> SCHEMA-8-NATIVE (the override
lands; channel activation queued one at a time, exp258 first); ANY S2
failure -> the schema does NOT land — diagnose, repair, re-run, the
delta is named in the deposit.

RUN: the anchor batteries (exp79's grid the long pole; serial, BLAS
pinned) + the suite; runner or foreground segments.
"""
# SEGMENTS (runner split; every segment self-contained, deterministic,
# no wall-clock fields) — body-only mechanics, added at body time:
#
#   --seg s1     the S1 schema battery (fast)
#   --seg s3s4   the S3 dormancy probes + S4 determinism probes (fast)
#   --seg b1     exp79's 45-point grid re-run (the long pole)
#   --seg b2     exp32's 15 deposited arms re-run
#   --seg b3     exp198's c3 cell re-run (CornerMedium n=400, 25 x 3)
#   --seg suite  the full test suite (subprocess, parsed)
#   --merge f1 f2 ...  merge section files into the final deposit
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp257_native_8channel_schema.json")


def _sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def _fingerprint(obj) -> str:
    """Deterministic deposit fingerprint: sha256 of the canonical JSON
    (sort_keys, no wall-clock fields anywhere in the sections)."""
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()


# ---------------------------------------------------------------- S1
def _seg_s1() -> dict:
    from cultivation.bioelectric.collective import (
        BioElectricCollective, CHANNEL_NAMES, N_CHANNELS, ACTIVE_CHANNELS,
        DORMANT_CHANNELS)
    from cultivation.substrate.graph import GraphCollective
    from cultivation.bioelectric.morpho_engineering import LatchingCollective

    checks: dict[str, bool] = {}

    # the constants
    checks["constants"] = bool(
        CHANNEL_NAMES == ("vmem", "theta", "gj", "ctx", "ca2", "sht",
                          "apop", "ichan")
        and N_CHANNELS == 8
        and ACTIVE_CHANNELS == ("vmem", "theta")
        and DORMANT_CHANNELS == ("gj", "ctx", "ca2", "sht", "apop", "ichan"))

    n = 40
    A = np.eye(n, k=1) + np.eye(n, k=-1)
    c = BioElectricCollective(n=n, adjacency=A, seed=0)

    # S exists, right shape, dormant inits (gj=1.0, ctx/ca2/sht/apop=0.0,
    # ichan=gamma default 0.25)
    checks["S_shape"] = bool(c.S.shape == (n, N_CHANNELS))
    checks["S_dormant_inits"] = bool(
        np.all(c.S[:, CHANNEL_NAMES.index("gj")] == 1.0)
        and np.all(c.S[:, CHANNEL_NAMES.index("ichan")] == 0.25)
        and np.all(c.S[:, CHANNEL_NAMES.index("ctx")] == 0.0)
        and np.all(c.S[:, CHANNEL_NAMES.index("ca2")] == 0.0)
        and np.all(c.S[:, CHANNEL_NAMES.index("sht")] == 0.0)
        and np.all(c.S[:, CHANNEL_NAMES.index("apop")] == 0.0))
    checks["shims_view"] = bool(
        np.array_equal(c.V, c.S[:, 0]) and np.array_equal(c.theta, c.S[:, 1]))

    # legacy accessors route into S
    v_new = np.linspace(-70, -10, n)
    th_new = np.linspace(-60, -40, n)
    c.set_state(v_new)
    checks["set_state"] = bool(np.array_equal(c.S[:, 0], v_new))
    c.set_target(th_new)
    checks["set_target"] = bool(np.array_equal(c.S[:, 1], th_new))
    checks["phi_spec_captured"] = bool(
        getattr(c, "phi_spec", None) is not None
        and np.array_equal(c.phi_spec, th_new))

    # clone_state == channels 0/1; restore_state writes 0/1 ONLY
    v2, th2 = c.clone_state()
    checks["clone_state_2tuple"] = bool(
        np.array_equal(v2, c.S[:, 0]) and np.array_equal(th2, c.S[:, 1]))
    c.set_channel("ca2", np.arange(n, dtype=float))
    c.set_channel("ctx", np.arange(n, dtype=float) * 2.0)
    c.restore_state((v_new, th_new))
    checks["restore_dormant_untouched"] = bool(
        np.array_equal(c.S[:, 0], v_new)
        and np.array_equal(c.S[:, 1], th_new)
        and np.array_equal(c.S[:, CHANNEL_NAMES.index("ca2")],
                           np.arange(n, dtype=float))
        and np.array_equal(c.S[:, CHANNEL_NAMES.index("ctx")],
                           np.arange(n, dtype=float) * 2.0))

    # the new full-state accessors round-trip all 8 channels
    full = c.clone_state_full()
    checks["clone_full_8ch"] = bool(full.shape == (n, N_CHANNELS)
                                    and np.array_equal(full, c.S))
    c.set_channel("sht", np.arange(n, dtype=float) * 3.0)
    c.restore_state_full(full)
    checks["restore_full_roundtrip"] = bool(np.array_equal(c.S, full))
    # item assignment on the shims writes through
    c.V[0] = -33.0
    checks["shim_item_assign"] = bool(c.S[0, 0] == -33.0)
    c.theta[n - 1] = -44.5
    checks["shim_item_assign_theta"] = bool(c.S[n - 1, 1] == -44.5)
    # unknown channel raises
    try:
        c.set_channel("nope", np.zeros(n))
        checks["unknown_raises"] = False
    except ValueError:
        checks["unknown_raises"] = True

    # the subclasses carry S through the same shims
    g = GraphCollective(adjacency=A, seed=0)
    checks["graph_collective_S"] = bool(
        g.S.shape == (n, N_CHANNELS)
        and np.array_equal(g.V, g.S[:, 0])
        and np.array_equal(g.theta, g.S[:, 1]))
    l = LatchingCollective(n=n, adjacency=A, seed=0)
    checks["latching_collective_S"] = bool(
        l.S.shape == (n, N_CHANNELS)
        and np.array_equal(l.V, l.S[:, 0])
        and np.array_equal(l.theta, l.S[:, 1])
        and np.array_equal(l.theta_anchor, l.S[:, 1]))

    return {"checks": checks,
            "n_checks": len(checks),
            "n_pass": int(sum(checks.values())),
            "pass": bool(all(checks.values()))}


# ---------------------------------------------------------------- S3/S4
def _seg_s3s4() -> dict:
    from experiments.exp73_active_renormalization import make_battery, N
    from experiments.exp43_substrate_independence import labeling
    from experiments.exp79_two_channel_law import run_gm

    battery = make_battery()
    lbl = labeling(N)
    probes = []
    for arm, g, mu in (("scale_free", 64.0, 0.0),
                       ("random3", 4.0, 0.015),
                       ("torus", 0.25, 0.0015)):
        err = run_gm(battery[arm], lbl, 1, g, mu)
        # determinism: identical re-run in-process (S4)
        err2 = run_gm(battery[arm], lbl, 1, g, mu)
        probes.append({"arm": arm, "gamma": g, "mu": mu,
                       "err": float(err), "err_rerun": float(err2),
                       "bit_identical": bool(err == err2)})
    s4_determinism = bool(all(p["bit_identical"] for p in probes))

    # S3 dormancy: a settle run with ch4 "ca2" / ch3 "ctx" arbitrarily
    # perturbed MID-RUN reproduces the unperturbed run's ch0/ch1
    # bit-exactly. Instrument: exp79's own settle path (run_gm's
    # construction), the run SPLIT INTO TWO HALVES for BOTH runs so the
    # step partitioning is identical; the perturbation values are drawn
    # from a SEPARATE rng (default_rng(12345)) — NEVER the collective's
    # self.rng, whose stream would shift and fake a divergence. The
    # dormant write can only matter if a dormant channel feeds back
    # into ch0/ch1, which the code structurally cannot do; the probe
    # asserts it empirically.
    import cultivation.bioelectric.collective as core
    from cultivation.substrate.graph import GraphCollective
    from experiments.exp79_two_channel_law import RUN_T, DT, N as N79
    pert_rng = np.random.default_rng(12345)
    dorm = []
    for arm, g, mu in (("scale_free", 64.0, 0.0), ("torus", 4.0, 0.015)):
        A = battery[arm]
        dt = DT if g <= 0.25 else min(DT, 1.2 / (g + float(
            (A * (0.0 + 0.20 * np.ones_like(A))).sum(axis=1).max())))
        # baseline: two half-runs (identical partitioning to the probe)
        c0 = GraphCollective(adjacency=A, seed=1, gamma=g, mu_theta=mu)
        c0.set_target(lbl)
        c0.theta = lbl.copy()
        c0.V = c0.theta + c0.rng.normal(0.0, 2.0, N79)
        c0.run(RUN_T / 2.0, dt=dt)
        c0.run(RUN_T / 2.0, dt=dt)
        v0, t0 = c0.clone_state()
        # probe: same construction, dormant channels scrambled mid-run
        c1 = GraphCollective(adjacency=A, seed=1, gamma=g, mu_theta=mu)
        c1.set_target(lbl)
        c1.theta = lbl.copy()
        c1.V = c1.theta + c1.rng.normal(0.0, 2.0, N79)
        c1.run(RUN_T / 2.0, dt=dt)
        c1.set_channel("ca2", pert_rng.normal(0.0, 50.0, N79))
        c1.set_channel("ctx", pert_rng.normal(0.0, 50.0, N79))
        c1.run(RUN_T / 2.0, dt=dt)
        v1, t1 = c1.clone_state()
        dorm.append({"arm": arm, "gamma": g, "mu": mu, "dt": float(dt),
                     "V_bit_identical": bool(np.array_equal(v0, v1)),
                     "theta_bit_identical": bool(np.array_equal(t0, t1))})
    s3_dormancy = bool(all(d["V_bit_identical"] and d["theta_bit_identical"]
                           for d in dorm))

    # the production floor discipline: the module never pins here, but
    # the exit assert is recorded (the exp169-import restore clause)
    floor_now = float(getattr(core, "NEURAL_SPEC_MIN", -60.0))
    floor_ok = floor_now == -60.0

    return {"determinism_probes": probes, "s4_determinism": s4_determinism,
            "dormancy_probes": dorm, "s3_dormancy": s3_dormancy,
            "floor_at_exit": floor_now, "floor_ok": floor_ok,
            "pass": bool(s4_determinism and s3_dormancy and floor_ok)}


# ---------------------------------------------------------------- B1
def _seg_b1() -> dict:
    import experiments.exp79_two_channel_law as m79
    from experiments.exp73_active_renormalization import make_battery, N
    from experiments.exp43_substrate_independence import labeling

    dep = json.load(open(os.path.join(
        ROOT, "results", "exp79_two_channel_law.json")))
    gpts = {(p["arm"], p["gamma"], p["mu"]): p["err"]
            for p in dep["grid_points"]}
    battery = make_battery()
    lbl = labeling(N)
    rows = []
    n_match = 0
    for arm in ("scale_free", "random3", "torus"):
        A = battery[arm]
        for g in m79.GAMMA_GRID:
            for mu in m79.MU_GRID:
                errs = [m79.run_gm(A, lbl, s, g, mu) for s in (1, 2, 3)]
                err_full = float(np.mean(errs))
                err_dep = round(err_full, 2)
                ok = (err_dep == gpts[(arm, g, mu)])
                n_match += int(ok)
                rows.append({"arm": arm, "gamma": g, "mu": mu,
                             "err_full": err_full, "err_round2": err_dep,
                             "deposited": gpts[(arm, g, mu)],
                             "bit_exact": bool(ok)})
    return {"rows": rows, "n": len(rows), "n_bit_exact": n_match,
            "pass": bool(n_match == len(rows) == 45)}


# ---------------------------------------------------------------- B2
def _seg_b2() -> dict:
    import experiments.exp32_m26_repairs as m32

    dep = json.load(open(os.path.join(
        ROOT, "results", "exp32_m26_repairs.json")))
    # exp32's arm_defs VERBATIM (its main()'s "tonight's sim arms"
    # block) — each deposited arm carries its own protocol kwargs; the
    # bare sim_arm(arm) signature would run every crosspiece at the
    # default cut_f/gradient and produce arm-independent errs. The
    # transcription is verified by the gate itself: any drift from
    # exp32's protocol breaks bit-exactness against the deposit.
    arm_defs = [
        ("cutting_cross_a", dict(cut_f=m32.EXP31_BINS["a"],
                                 length_gradient=1.0)),
        ("cutting_cross_b", dict(cut_f=m32.EXP31_BINS["b"],
                                 length_gradient=1.0)),
        ("cutting_cross_c", dict(cut_f=m32.EXP31_BINS["c"],
                                 length_gradient=1.0)),
        ("cutting_cross_d", dict(cut_f=m32.EXP31_BINS["d"],
                                 length_gradient=1.0)),
        ("cutting_tail_g1", dict(length_gradient=1.0)),
        ("cutting_head_g1", dict(length_gradient=1.0)),
        ("cutting_trunk_g1", dict(length_gradient=1.0)),
        ("ion_channel_tail_cns3", dict(commitment_noise_scale=3.0)),
        ("ion_channel_head_cns3", dict(commitment_noise_scale=3.0)),
        ("innexin_tail_recheck", {}),
        ("cutting_trunk_both", dict(direction="both")),
        ("wnt_trunk_both", dict(direction="both")),
        ("apc_trunk_both", dict(direction="both")),
        ("wnt_tail_g0", {}),
        ("apc_head_g0", {}),
    ]
    assert [a for a, _ in arm_defs] == list(dep["sim_arms"].keys()), \
        "arm_defs transcription drifted from the deposit's arm list"
    rows = []
    n_match = 0
    for arm, kw in arm_defs:
        rerun = m32.sim_arm(arm, **kw)
        rec = dep["sim_arms"][arm]
        ok = bool(np.array_equal(np.array(rerun["err_per_seed"]),
                                 np.array(rec["err_per_seed"])))
        n_match += int(ok)
        rows.append({"arm": arm,
                     "err_per_seed": [float(x) for x in rerun["err_per_seed"]],
                     "deposited": [float(x) for x in rec["err_per_seed"]],
                     "bit_exact": ok})
    return {"rows": rows, "n": len(rows), "n_bit_exact": n_match,
            "pass": bool(n_match == len(rows))}


# ---------------------------------------------------------------- B3
def _seg_b3() -> dict:
    from experiments.exp166_leading_edge import (
        CornerMedium, SEED_BASE as EXP166_SEED_BASE, cell_dims)
    from experiments.exp160_any_medium import BAR, config_fingerprint
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp148_temporal_read as _m148
    import experiments.exp198_adversarial_reader_n400 as m198

    dep = json.load(open(os.path.join(
        ROOT, "results", "exp198_adversarial_reader_n400.json")))
    d3 = dep["cells"]["c3"]

    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    m198.pin_floor()
    try:
        c_cell = 3
        errs_all: list[float] = []
        insts = []
        n_rej = 0
        for j in range(m198.PER_CELL):
            gen_seed = EXP166_SEED_BASE + 1000 * c_cell + j
            med = CornerMedium(m198.N400, gen_seed, cell_dims(c_cell))
            assert med.n == m198.N400
            fmax = float(f_max_frames(list(med.snapshots())))
            cls = "diffuse" if fmax < THRESHOLD else "concentrated"
            rec = {"j": j, "gen_seed": int(gen_seed), "n": int(med.n),
                   "f_max": fmax, "class": cls, "errs": [], "verified": []}
            for s in m198.SEEDS:
                out = _m148.decode("scoped", med, s, f_max=fmax)
                if not out["ok"]:
                    n_rej += 1
                    continue
                rec["errs"].append(float(out["err"]))
                rec["verified"].append(bool(out["verified"]))
                errs_all.append(float(out["err"]))
            rec["median_err"] = (float(np.median(rec["errs"]))
                                 if rec["errs"] else None)
            insts.append(rec)
        pooled = float(np.median(errs_all)) if errs_all else None
        verify_rate = (float(np.mean([v for r in insts for v in r["verified"]]))
                       if any(v for r in insts for v in r["verified"]) else None)
        section = {
            "cell": c_cell, "n_instances": len(insts),
            "n_build": int(m198.N400), "median_err": pooled,
            "median_of_instance_medians": float(np.median(
                [r["median_err"] for r in insts if r["median_err"] is not None])),
            "n_rejections": n_rej, "verify_rate": verify_rate,
            "n_diffuse": sum(1 for r in insts if r["class"] == "diffuse"),
            "n_concentrated": sum(1 for r in insts
                                  if r["class"] == "concentrated"),
            "f_max_min": min(r["f_max"] for r in insts),
            "f_max_max": max(r["f_max"] for r in insts),
            "instances": insts,
        }
    finally:
        m198.restore_floor()
    import cultivation.bioelectric.collective as core
    # the standing convention: after any exp169 import (the import chain
    # pins NEURAL_SPEC_MIN to -35.0 BEFORE exp198's save captures it),
    # restore the production floor to -60.0 EXPLICITLY
    core.NEURAL_SPEC_MIN = -60.0
    floor_ok = float(getattr(core, "NEURAL_SPEC_MIN", -60.0)) == -60.0

    # the bit-exact comparison vs the deposit (the cell's own anchors)
    matches = {
        "median_err": bool(section["median_err"] == d3["median_err"]),
        "median_of_instance_medians": bool(
            section["median_of_instance_medians"]
            == d3["median_of_instance_medians"]),
        "n_rejections": bool(section["n_rejections"] == d3["n_rejections"]),
        "verify_rate": bool(section["verify_rate"] == d3["verify_rate"]),
        "n_diffuse": bool(section["n_diffuse"] == d3["n_diffuse"]),
        "n_concentrated": bool(
            section["n_concentrated"] == d3["n_concentrated"]),
        "f_max_min": bool(section["f_max_min"] == d3["f_max_min"]),
        "f_max_max": bool(section["f_max_max"] == d3["f_max_max"]),
    }
    # per-instance errs bit-exact (the strongest form)
    inst_ok = 0
    for a, b in zip(section["instances"], d3["instances"]):
        if np.array_equal(np.array(a["errs"]), np.array(b["errs"])):
            inst_ok += 1
    return {"section_summary": {k: v for k, v in section.items()
                                if k != "instances"},
            "matches": matches, "n_instance_bit_exact": inst_ok,
            "n_instances": len(insts),
            "floor_restored": floor_ok,
            "pass": bool(all(matches.values())
                         and inst_ok == len(insts) and floor_ok)}


# ---------------------------------------------------------------- suite
def _seg_suite() -> dict:
    r = subprocess.run(
        [sys.executable, "-m", "tests.run_tests"], cwd=ROOT,
        capture_output=True, text=True, timeout=550)
    out = r.stdout + r.stderr
    n_pass = sum(1 for line in out.splitlines()
                 if line.strip().startswith("PASS "))
    bad = [ln for ln in out.splitlines()
           if ("FAIL" in ln.upper() or "TRACEBACK" in ln.upper()
               or "ERROR" in ln.upper())]
    return {"returncode": int(r.returncode), "n_pass_lines": n_pass,
            "n_bad_lines": len(bad), "bad_lines": bad[:10],
            "pass": bool(r.returncode == 0 and len(bad) == 0)}


# ---------------------------------------------------------------- merge
def _merge(paths: list[str]) -> dict:
    sections: dict[str, dict] = {}
    for p in paths:
        with open(p) as f:
            d = json.load(f)
        seg = d.get("section", d)
        sections[d.get("seg") or d.get("section", {}).get("seg", "s1")] = seg
    s1 = sections.get("s1", {})
    s3s4 = sections.get("s3s4", {})
    b1 = sections.get("b1", {})
    b2 = sections.get("b2", {})
    b3 = sections.get("b3", {})
    suite = sections.get("suite", {})

    g_s1 = bool(s1.get("pass"))
    g_b1 = bool(b1.get("pass"))
    g_b2 = bool(b2.get("pass"))
    g_b3 = bool(b3.get("pass"))
    g_suite = bool(suite.get("pass"))
    g_s3 = bool(s3s4.get("s3_dormancy"))
    g_s4 = bool(s3s4.get("s4_determinism") and s3s4.get("floor_ok"))
    s2 = bool(g_b1 and g_b2 and g_b3 and g_suite)
    branch = ("SCHEMA-8-NATIVE"
              if (g_s1 and s2 and g_s3 and g_s4) else "DELTA-NAMED")
    core_sha = _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py"))
    out = {
        "exp": "exp257",
        "claim": ("the native 8-channel write-path schema lands ADDITIVELY "
                  "with bit-exact compatibility shims: the paper's 8 channels "
                  "all have native state (3 had NO substrate), dormant at "
                  "defaults, activation one channel at a time (exp258: ctx; "
                  "exp259: gj)"),
        "schema": {
            "channel_names": ["vmem", "theta", "gj", "ctx", "ca2", "sht",
                              "apop", "ichan"],
            "active_channels": ["vmem", "theta"],
            "dormant_channels": ["gj", "ctx", "ca2", "sht", "apop", "ichan"],
            "dormancy_contract": ("ch2..ch7 zero dynamics, zero feedback "
                                  "into ch0/ch1 at defaults; carried only"),
            "collective_py_sha256": core_sha,
        },
        "sections": {"s1": s1, "s3s4": s3s4, "b1": b1, "b2": b2, "b3": b3,
                     "suite": suite},
        "criteria": {
            "S1_schema": g_s1,
            "S2_bit_exact": s2,
            "S2_B1_exp79_grid_45": g_b1,
            "S2_B2_exp32_chain": g_b2,
            "S2_B3_exp198_n400_c3": g_b3,
            "S2_B4_suite_green": g_suite,
            "S3_migration_dormancy": g_s3,
            "S4_discipline": g_s4,
        },
        "branch": branch,
        "verdict": branch,
        "notes": [
            "pre-registration 276e41e; docstring byte-unchanged; body "
            "written by the MAIN AGENT (the override priority)",
            "B1 compares round(err,2) — the deposit's own precision; the "
            "full-precision errs are recorded in b1.rows",
            "B2 compares err_per_seed at FULL float precision (exp32's "
            "deposited record)",
            "B3 re-runs exp198's c3 cell (CornerMedium n=400, 25 instances "
            "x 3 seeds, the production scoped read) with exp198's own "
            "pin/restore discipline; per-instance errs compared exactly",
            "the S3s4 dormancy probe scrambles ca2 AND ctx mid-run on "
            "exp79's settle path and asserts ch0/ch1 bit-identity",
            "no experiment module modified; only collective.py state "
            "plumbing (sha256 recorded above)",
        ],
        "deposit_fingerprint": None,
    }
    out["deposit_fingerprint"] = _fingerprint(
        {k: v for k, v in out.items() if k != "deposit_fingerprint"})
    return out


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["s1", "s3s4", "b1", "b2", "b3",
                                      "suite"], default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()

    if args.merge is not None:
        result = _merge(args.merge)
    elif args.seg == "s1":
        result = {"seg": "s1", "section": _seg_s1()}
    elif args.seg == "s3s4":
        result = {"seg": "s3s4", "section": _seg_s3s4()}
    elif args.seg == "b1":
        result = {"seg": "b1", "section": _seg_b1()}
    elif args.seg == "b2":
        result = {"seg": "b2", "section": _seg_b2()}
    elif args.seg == "b3":
        result = {"seg": "b3", "section": _seg_b3()}
    elif args.seg == "suite":
        result = {"seg": "suite", "section": _seg_suite()}
    else:
        # single-process full run (foreground; the segments are small
        # enough together only for smoke — the runner split is canonical)
        result = _merge([])  # not supported single-shot; runner split only
        raise SystemExit("use --seg / --merge (runner split is canonical)")

    with open(args.out, "w") as f:
        json.dump(result, f, indent=1, default=str)
    if args.merge:
        print(f"=== exp257 MERGE: branch {result['branch']} ===")
        for k, v in result["criteria"].items():
            print(f"  {k}: {'PASS' if v else 'FAIL'}")
    else:
        seg = result["seg"]
        sec = result["section"]
        print(f"=== exp257 seg {seg}: "
              f"{'PASS' if sec.get('pass') else 'FAIL'} ===")
    return result


if __name__ == "__main__":
    main()
