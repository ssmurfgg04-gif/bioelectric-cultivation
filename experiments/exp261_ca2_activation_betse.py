#!/usr/bin/env python3
"""exp261 — THE CA2 CHANNEL ACTIVATION, BETSE-GROUNDED (batch 23
item 2; the THIRD activation under the exp257 schema — ch4 "ca2" —
with the kinetics ported from BETSE, the user's designated reference).

THE OPEN ITEM: the paper's 8-channel census (exp232) found Ca2+
transient signaling ABSENT from the stack; the exp257 schema gave it
native state (ch4, dormant); the activation record so far: ch3 ctx
INERT (exp258), ch2 gj INERT (exp259). Ca2+ is the channel with the
richest external grounding: BETSE (the BioElectric Tissue Simulation
Engine, github.com/betsee/betse — the cell-mesh electrical dynamics,
ionic flux and voltage-gated channel machinery of the Levin-lineage
modeling program) ships voltage-gated calcium channels with
Hodgkin-Huxley kinetics and a Vmem-dependent Ca2+ ATPase pump. This
experiment ports those kinetics VERBATIM (constants + source-line
provenance, zero re-fit) and tests whether the Ca2+ channel carries a
boundary-localized signal the V/theta pair does not.

THE PORT (pre-registered, provenance-recorded in the deposit):

  K1  BETSE's Cav3.3 T-type channel (betse/science/channels/vg_ca.py,
      class Cav3p3, Traboulsie et al. 2007): m_inf(V) =
      1/(1+exp((V+45.454426)/5.073015)); m_tau(V) = 3.394938 +
      54.187616/(1+exp((V+40.040397)/4.110392)); h_inf(V) =
      1/(1+exp((V+74.031965)/8.416382)); h_tau(V) = 109.701136 +
      0.003816*exp(-V/4.781719); open probability P = m^1 * h^1;
      time unit 1e3 (ms); reversal +30 mV (recorded, not used — the
      open-probability face only).
  K2  BETSE's Ca2+ ATPase pump face (betse/science/sim_toolbox.py,
      pumpCa): the equilibrium constant Keq = exp(-(dG_ATP/(RT) -
      2 F Vm/(RT))) — the pump's Vmem dependence is exactly the
      2-charge electrophoresis term; recorded as the pump's
      steady-state reading: the Vmem -> resting-P map is monotone
      through BOTH the channel gates and the pump equilibrium.

PRE-REGISTERED GATES (two stages, the write coupling GATED on the
readout):

  C1  THE PORT: the ported gate functions reproduce BETSE's own
      curves bit-exactly — the deposit records the source sha256 of
      the two BETSE files, the ported constants, and a 401-point
      V-grid (-85..+5 mV, the stack's physiological range) where
      m_inf/h_inf/m_tau/h_tau/P are computed BOTH by the ported
      functions and by a direct import-free recomputation from the
      quoted source lines; equality asserted to 0.0 delta.
  C2  THE READOUT (does the Ca2+ field localize the boundary
      excess?): at the dormant baseline (no coupling), compute the
      per-cell open-probability field P_i = m(V_i) h(V_i) on the c6
      battery's settled states (exp226's battery x 3 seeds, the
      exp258 battery verbatim) and test the pre-named association:
      Spearman(P_i, the cell's |V_i - theta_i| mismatch) >= 0.5 AND
      the boundary cells' mean P exceeds the non-boundary cells' mean
      (the pre-named localization clause). The readout is zero-risk:
      no dynamics touched, the channel is READ only.
  C3  THE WRITE COUPLING (only if C2 passes; if C2 fails, C3 is
      skipped and recorded SKIPPED-C2-FAIL): the HH-gated ca2 pull —
      the cell's theta restoration pull multiplied by (1 + g_ca *
      (P_i - P̄)) with P̄ the battery-wide mean P (the gain form the
      exp258 grid tested; the SAME pre-named grid {0, 0.25, 0.5,
      1.0}); the gates: the best cell reduces the worst boundary-row
      err >= 10% AND the non-boundary rows' worst-err change <= +5%
      (the exp258/exp259 forms verbatim). g_ca = 0 IS the dormant
      identity (bit-exact, the migration gate's own face).
  C4  THE DISCIPLINE: the BETSE reference tree READ-ONLY (sha-record
      the two ported files); exp226's/exp229's deposits READ-ONLY
      sha-recorded byte-unchanged; collective.py untouched (the
      activation instrument lives in the experiment module via the
      public accessors); the -60.0 floor restored and asserted;
      deterministic re-run, no wall-clock fields.

THE BRANCHES (pre-named): C2 PASS + C3 PASS -> CA2-CARRIES (the
paper's third absent substrate carries a boundary-localized,
externally-grounded signal — the 8-channel correspondence gains its
first NEW active channel); C2 PASS + C3 REFUTE -> CA2-READOUT-ONLY
(the signal localizes but the write face does not close the boundary);
C2 REFUTE -> CA2-INERT (deposited honestly).

RUN: the c6 battery x the pre-named grid (4 values x 3 seeds) + the
port verification; foreground segments.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp261_ca2_activation_betse.json")

# the BETSE reference tree (the user's directive clone; READ-ONLY)
BETSE_REF = os.path.join(os.path.dirname(ROOT), "betse-reference")
BETSE_VG_CA = os.path.join(BETSE_REF, "betse", "science", "channels",
                           "vg_ca.py")
BETSE_TOOLBOX = os.path.join(BETSE_REF, "betse", "science",
                             "sim_toolbox.py")

# ==== BODY (written by the run agent under the body-only discipline;
# docstring/imports/constants above byte-unchanged — verified against
# 54fc177 by EXPECTED_HEADER_SHA256 at merge; the gates below are the
# docstring's, each evaluated exactly once) =============================
EXPECTED_HEADER_SHA256 = (
    "b9de80d8810093b75cbfccb2c37392c448175def4098ce708a29969c7585462b")
_HEADER_MARKER = '                             "sim_toolbox.py")\n'
DOCSTRING_SHA256 = (
    "86a572361e62593f5ce695565e04293c0b917e0c79a592cded203b82f75134e8")


def main() -> dict:
    # ==== imports (the exp258 machinery; the BLAS pins precede the
    #      numpy import — the pre-registered header's discipline) ========
    import argparse
    import hashlib
    import json
    import types
    from contextlib import contextmanager

    ap = argparse.ArgumentParser()
    ap.add_argument("--seg", choices=["c0", "g025", "g050", "g100"],
                    default=None)
    ap.add_argument("--merge", nargs="*", default=None)
    ap.add_argument("--pass-b", nargs="*", default=None)
    ap.add_argument("--c2-gate", default=None, metavar="C0_SEG_JSON")
    ap.add_argument("--pbar-from", default=None, metavar="C0_SEG_JSON")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out if args.out is not None else OUT

    import numpy as np

    import cultivation.bioelectric.collective as CORE
    import experiments.exp142_sign_read as M142
    import experiments.exp148_temporal_read as M148
    from cultivation.compiler.anatomy import compile_anatomy
    from cultivation.substrate.graph import GraphCollective
    from cultivation.validation.stats import spearman_ties
    from experiments.exp142_sign_read import execute_signed as _PROD_EXECUTOR
    from experiments.exp160_any_medium import config_fingerprint
    from experiments.exp166_leading_edge import CornerMedium, cell_dims
    # exp169's import BEFORE exp199's (exp213's import order): the
    # exp169-import sets the -35.0 floor across the pin modules, and
    # exp199's _PIN_SAVE snapshots THAT state so restore_floor() lands
    # exactly at the pre-run floors; the production -60.0 floor is
    # restored EXPLICITLY at the end of every process (asserted)
    from experiments.exp169_rt_scoping import THRESHOLD, f_max_frames
    import experiments.exp199_ro_n400_tail as M199
    from experiments.exp199_ro_n400_tail import (
        N400, PER_CELL, SEEDS, pin_floor, restore_floor)
    from experiments.exp90_two_source_read import star_dt
    from experiments.exp94_multizone_scale import (
        labeling_bfs_n, spec_target_n)

    def _sha(path: str) -> str:
        return hashlib.sha256(open(path, "rb").read()).hexdigest()

    def _fingerprint(obj) -> str:
        # the deterministic deposit fingerprint (no wall-clock fields
        # anywhere in the sections)
        return hashlib.sha256(
            json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()

    # ---- the READ-ONLY references (C4: sha-recorded before any work
    #      in every process; re-checked byte-unchanged at merge; the two
    #      BETSE files are the user's directive READ-ONLY clone) --------
    DEP226 = os.path.join(ROOT, "results",
                          "exp226_boundary_dynamics_test.json")
    DEP229 = os.path.join(ROOT, "results", "exp229_curvature_test.json")
    DEP199 = os.path.join(ROOT, "results", "exp199_ro_n400_tail.json")
    DEP208 = os.path.join(ROOT, "results", "exp208_c6_tail_ablation.json")
    READ_ONLY_PATHS = {"exp226": DEP226, "exp229": DEP229,
                       "exp199": DEP199, "exp208": DEP208,
                       "betse_vg_ca": BETSE_VG_CA,
                       "betse_sim_toolbox": BETSE_TOOLBOX}
    READ_ONLY_SHAS = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
    COLLECTIVE_SHA = _sha(os.path.join(
        ROOT, "cultivation", "bioelectric", "collective.py"))

    with open(DEP199) as f:
        dep199 = json.load(f)
    with open(DEP208) as f:
        dep208 = json.load(f)
    dep_by_cell = {r["j"]: r for r in dep199["cells"]["c6"]["instances"]}
    dep208_by_j = {r["j"]: r
                   for r in dep208["sections"]["c6_tail"]["instances"]}

    # ---- the read stack, asserted before any decode (exp226 verbatim) --
    fp = config_fingerprint()
    assert fp == "8e11e88c1c2f1518", \
        f"exp160 READ_CONFIG fingerprint drifted: {fp}"
    assert THRESHOLD == 32.0, "scoped threshold drifted"

    seeds = list(SEEDS)   # exp199's (1, 2, 3) — the battery's seeds

    # =====================================================================
    # THE PORT (C1; the docstring's K1/K2). The ported functions below
    # implement BETSE's Cav3p3 source lines VERBATIM (constants
    # extracted, zero re-fit); C1 recomputes every curve DIRECTLY from
    # the quoted source lines (exec of the verbatim file lines —
    # import-free: betse itself is never imported) on the pre-named
    # 401-point V-grid and asserts 0.0 delta.
    #
    # TRANSCRIPTION NOTE (disclosed; the docstring is byte-unchanged):
    # the pre-registered K1 prose form of m_inf reads
    #     m_inf(V) = 1/(1+exp((V+45.454426)/5.073015))
    # while BETSE's own line (vg_ca.py:160 and :176) is
    #     1 / (1 + np.exp((V - -45.454426) / -5.073015))
    # The FILE line is the authoritative port: C1's headline clause is
    # "the ported gate functions reproduce BETSE's own curves
    # bit-exactly" and the docstring's own port clause is "VERBATIM
    # (constants + source-line provenance, zero re-fit)". The two forms
    # are exact complements (docstring_form == 1 - file_form); the
    # numeric demonstration is carried in the port record.
    # =====================================================================
    VG_CA_LINES = {
        104: '        P = (self.m ** self._mpower) * (self.h ** self._hpower)',
        152: '        self.time_unit = 1.0e3',
        154: '        self.vrev = 30     # reversal voltage used in model [mV]',
        160: '        self.m = 1 / (1 + np.exp((V - -45.454426) / -5.073015))',
        161: '        self.h = 1 / (1 + np.exp((V - (-74.031965)) / 8.416382))',
        164: '        self._mpower = 1',
        165: '        self._hpower = 1',
        176: '        self._mInf = 1 / (1 + np.exp((V - -45.454426) / -5.073015))',
        177: '        self._mTau = 3.394938 + (54.187616 / (1 + np.exp((V - -40.040397) / 4.110392)))',
        178: '        self._hInf = 1 / (1 + np.exp((V - (-74.031965)) / 8.416382))',
        179: '        self._hTau = 109.701136 + (0.003816 * np.exp(-V / 4.781719))'}
    TOOLBOX_LINES = {
        145: '    deltaGATP_o = p.deltaGATP',
        166: '    Keq = np.exp(-(deltaGATP_o / (p.R * T) - 2*((p.F * Vm) / (p.R * T))))'}
    _vg_src = open(BETSE_VG_CA).read().split("\n")
    _tb_src = open(BETSE_TOOLBOX).read().split("\n")
    for _n, _s in VG_CA_LINES.items():
        assert _vg_src[_n - 1] == _s, f"vg_ca.py:{_n} quoted line drifted"
    for _n, _s in TOOLBOX_LINES.items():
        assert _tb_src[_n - 1] == _s, \
            f"sim_toolbox.py:{_n} quoted line drifted"

    # the ported constants (extracted from the quoted lines; zero re-fit)
    M_VHALF = -45.454426   # vg_ca.py:160/176 — the '-45.454426' of (V - -45.454426)
    M_SLOPE = -5.073015    # vg_ca.py:160/176 — the '/ -5.073015'
    MT_BASE = 3.394938     # vg_ca.py:177
    MT_NUM = 54.187616     # vg_ca.py:177
    MT_VHALF = -40.040397  # vg_ca.py:177
    MT_SLOPE = 4.110392    # vg_ca.py:177
    H_VHALF = -74.031965   # vg_ca.py:161/178
    H_SLOPE = 8.416382     # vg_ca.py:161/178
    HT_BASE = 109.701136   # vg_ca.py:179
    HT_COEF = 0.003816     # vg_ca.py:179
    HT_TAU = 4.781719      # vg_ca.py:179
    M_POWER = 1            # vg_ca.py:164 (self._mpower)
    H_POWER = 1            # vg_ca.py:165 (self._hpower)
    TIME_UNIT = 1.0e3      # vg_ca.py:152 (recorded)
    VREV = 30.0            # vg_ca.py:154 (recorded; the open-probability face only)
    # BETSE's pump constants (betse/science/parameters.py module
    # defaults; recorded for the K2 steady-state reading)
    PUMP_F = 96485.0       # parameters.py:1106 [J/V*mol]
    PUMP_R = 8.314         # parameters.py:1107 [J/K*mol]
    PUMP_DG_ATP = -37000.0  # parameters.py:1116 [J/mol]

    def ca_m_inf(V):
        return 1 / (1 + np.exp((V - M_VHALF) / M_SLOPE))

    def ca_m_tau(V):
        return MT_BASE + (MT_NUM / (1 + np.exp((V - MT_VHALF) / MT_SLOPE)))

    def ca_h_inf(V):
        return 1 / (1 + np.exp((V - H_VHALF) / H_SLOPE))

    def ca_h_tau(V):
        return HT_BASE + (HT_COEF * np.exp(-V / HT_TAU))

    def ca_open_prob(m, h):
        return (m ** M_POWER) * (h ** H_POWER)

    def _port_verification() -> dict:
        grid = np.linspace(-85.0, 5.0, 401)
        # the RECOMPUTATION: direct evaluation of the quoted source
        # lines (import-free — the only names the lines receive are np,
        # V, and the objects the lines themselves name; the exec'd form
        # is line.strip() of the byte-asserted file line)
        sn_init = types.SimpleNamespace()
        exec(VG_CA_LINES[160].strip(), {"np": np, "V": grid, "self": sn_init})
        sn_calc = types.SimpleNamespace()
        for _n in (176, 177, 178, 179):
            exec(VG_CA_LINES[_n].strip(), {"np": np, "V": grid, "self": sn_calc})
        sn_p = types.SimpleNamespace(m=sn_calc._mInf, h=sn_calc._hInf)
        exec(VG_CA_LINES[164].strip(), {"self": sn_p})
        exec(VG_CA_LINES[165].strip(), {"self": sn_p})
        ns_p = {"np": np, "self": sn_p}
        exec(VG_CA_LINES[104].strip(), ns_p)
        rec = {"m_inf": sn_calc._mInf, "m_tau": sn_calc._mTau,
               "h_inf": sn_calc._hInf, "h_tau": sn_calc._hTau,
               "P": ns_p["P"]}
        rec_m_init = sn_init.m
        port = {"m_inf": ca_m_inf(grid), "m_tau": ca_m_tau(grid),
                "h_inf": ca_h_inf(grid), "h_tau": ca_h_tau(grid),
                "P": ca_open_prob(ca_m_inf(grid), ca_h_inf(grid))}
        deltas = {k: float(np.max(np.abs(port[k] - rec[k])))
                  for k in port}
        deltas["m_inf_init_vs_calc"] = float(
            np.max(np.abs(rec_m_init - rec["m_inf"])))
        # the K1 transcription note, demonstrated numerically: the
        # docstring's prose form and the file's line are exact
        # complements (their sum is the constant 1.0)
        docstring_form = 1 / (1 + np.exp((grid + 45.454426) / 5.073015))
        note_delta = float(np.max(np.abs(
            (docstring_form + rec["m_inf"]) - 1.0)))
        # K2: the pump's steady-state reading — the quoted Keq line
        # evaluated directly at BETSE's pump constants; recorded,
        # NOT used in any dynamics (the docstring's own clause).
        # UNIT NOTE (the pump source's own docstring): pumpCaATP's Vm
        # is in VOLTS ([V] — sim_toolbox.py:133), while the vg_ca
        # channel curves are in mV — the Keq grid is the channel grid
        # converted (V = mV * 1e-3)
        pump = {}
        vm_volts = grid * 1.0e-3
        for T in (273.15, 293.15, 310.0):
            pns = types.SimpleNamespace(R=PUMP_R, T=T, F=PUMP_F,
                                        deltaGATP=PUMP_DG_ATP)
            ns_k = {"np": np, "deltaGATP_o": PUMP_DG_ATP, "p": pns,
                    "T": T, "Vm": vm_volts}
            exec(TOOLBOX_LINES[166].strip(), ns_k)
            keq = ns_k["Keq"]
            pump[f"T={T}"] = {
                "vm_unit": "V (the pump line's own unit; the channel "
                           "curves are mV)",
                "keq_at_vmin": float(keq[0]),
                "keq_at_vmax": float(keq[-1]),
                "monotone_increasing_in_Vm": bool(np.all(np.diff(keq) > 0.0))}
        c1_pass = bool(all(v == 0.0 for v in deltas.values())
                       and note_delta < 1e-12
                       and all(v["monotone_increasing_in_Vm"]
                               for v in pump.values()))
        return {"grid": {"v_min_mV": -85.0, "v_max_mV": 5.0,
                         "n_points": int(grid.size)},
                "max_abs_delta_ported_vs_recomputed": deltas,
                "zero_delta_required": True,
                "transcription_note": {
                    "docstring_K1_m_inf_form":
                        "1/(1+exp((V+45.454426)/5.073015))",
                    "file_line_vg_ca_160_and_176":
                        "1 / (1 + np.exp((V - -45.454426) / -5.073015))",
                    "relation": ("exact complements: docstring_form + "
                                 "file_form = 1 (numerically "
                                 "demonstrated on the grid); the FILE "
                                 "line is the authoritative port per "
                                 "the VERBATIM clause and C1's headline "
                                 "('reproduce BETSE's own curves "
                                 "bit-exactly'); the docstring is "
                                 "byte-unchanged and this note is the "
                                 "disclosure"),
                    "max_abs_complement_delta": note_delta},
                "pump_keq_record": pump,
                "quoted_constants": {
                    "M_VHALF": M_VHALF, "M_SLOPE": M_SLOPE,
                    "MT_BASE": MT_BASE, "MT_NUM": MT_NUM,
                    "MT_VHALF": MT_VHALF, "MT_SLOPE": MT_SLOPE,
                    "H_VHALF": H_VHALF, "H_SLOPE": H_SLOPE,
                    "HT_BASE": HT_BASE, "HT_COEF": HT_COEF,
                    "HT_TAU": HT_TAU, "M_POWER": M_POWER,
                    "H_POWER": H_POWER, "TIME_UNIT": TIME_UNIT,
                    "VREV": VREV, "PUMP_F": PUMP_F, "PUMP_R": PUMP_R,
                    "PUMP_DG_ATP": PUMP_DG_ATP},
                "pass": c1_pass}

    # C1 runs FIRST in every process (the hard rule): fail = STOP and
    # report, no tuning — before ANY battery work
    port_record = _port_verification()
    if not port_record["pass"]:
        print("=== exp261 C1 STOP: the port verification failed ===")
        print(json.dumps(port_record["max_abs_delta_ported_vs_recomputed"],
                         indent=1))
        raise SystemExit(3)
    print("=== exp261 C1 port verification PASS "
          "(0.0 delta on m_inf/m_tau/h_inf/h_tau/P) ===")

    # ---- exp208's classification + decomposition VERBATIM (carried by
    #      exp226/exp258; the row classes, precedence intact) ------------
    def classify(T: np.ndarray, W: np.ndarray) -> dict:
        n = len(T)
        Td = np.asarray(T, dtype=float)
        bnd = np.zeros(n, dtype=bool)
        for i in range(n):
            if Td[i] != Td[(i - 1) % n] or Td[i] != Td[(i + 1) % n]:
                bnd[i] = True
        support = np.abs(W) > 0
        iu = np.triu_indices(n, 1)
        deg = np.zeros(n, dtype=int)
        for a, b in zip(iu[0][support[iu]], iu[1][support[iu]]):
            deg[a] += 1
            deg[b] += 1
        pj = deg >= 2
        cls = np.zeros(n, dtype=int)          # 2 = INTERIOR
        cls[pj] = 1
        cls[bnd] = 0
        return {"boundary": bnd, "junction": pj & ~bnd,
                "interior": ~(bnd | pj), "class": cls}

    def decompose(V: np.ndarray, T: np.ndarray, cls: np.ndarray,
                  err_recomputed: float) -> dict:
        e2 = (np.asarray(V, dtype=float)
              - np.asarray(T, dtype=float)) ** 2
        total = float(e2.sum())
        n = len(e2)
        per = []
        for name, mask in (("CANON-BOUNDARY", cls == 0),
                           ("PAIR-JUNCTION", cls == 1),
                           ("INTERIOR", cls == 2)):
            ss = float(e2[mask].sum())
            per.append({"class": name, "n_cells": int(mask.sum()),
                        "sum_sq": ss,
                        "frac_of_sq": ss / total if total > 0 else 0.0,
                        "rms_contrib_mV":
                            float(np.sqrt(ss / n)) if n else 0.0})
        ident = abs(sum(p["sum_sq"] for p in per) / n
                    - err_recomputed ** 2)
        assert ident < 1e-6 * max(1.0, err_recomputed ** 2), \
            f"accounting identity violated: {ident}"
        assert abs(sum(p["frac_of_sq"] for p in per) - 1.0) < 1e-9
        return {"per_class": per, "identity_residual": ident}

    # ---- THE ACTIVATION INSTRUMENT (lives ENTIRELY here; collective.py
    #      untouched — sha-recorded) ---------------------------------------
    # _make_ca_executor returns exp142's execute_signed VERBATIM (every
    # line identical, the commit branches untouched, NEURAL_SPEC_MIN
    # resolved dynamically from exp142's module global exactly as the
    # production executor resolves it) with the ONE pre-registered
    # activation interleaved at the commit of EVERY cell of the
    # regenerated region's walk:
    #
    #   at the commit of cell i, and ONLY at g_ca > 0:
    #     P_i := m_inf(V_i) * h_inf(V_i) at the cell's LIVE Vmem (read
    #     BEFORE the commit write — the HH gate follows the running
    #     state);
    #     ca2[i] := P_i via the public accessors (c.read_channel("ca2")
    #     / c.set_channel("ca2", ...)) — the activation's channel-write
    #     face (ch4 now carries the cell's open probability);
    #     effective commit := theta_before + (1 + g_ca * (P_i - Pbar)) *
    #     (theta_new - theta_before) — the cell's theta restoration
    #     pull (the commit displacement) multiplied by the HH-gated
    #     gain; Pbar is the battery-wide mean P over the settled
    #     g_ca = 0 c6 battery rows (the c0 checkpoint's own verified
    #     states — one scalar, zero re-fit);
    #     the effective target is written to BOTH channels exactly as
    #     the verbatim commit writes theta_new to both; the rng stream
    #     is untouched (the gain multiplies the displacement AFTER
    #     theta_new is drawn — identical draws across the whole grid).
    #   DISCLOSED READING (outcome-blind, fixed before any g_ca > 0
    #   run): the docstring's "the cell's theta restoration pull"
    #   names EVERY region cell's commit (the commit loop is the only
    #   theta restoration the executor performs); the HH open
    #   probability is the gate — no class restriction — which is what
    #   makes the coupling "HH-gated". g_ca = 0.0 takes the verbatim
    #   path with ZERO deviation (no ca2 write, no gain) — the
    #   bit-exact dormant default, the migration gate's own face.
    def _make_ca_executor(medium, g_ca: float, pbar: float,
                          telemetry: dict):
        def _execute_signed_ca(spec, adjacency, seed, op,
                               return_state=False):
            n = adjacency.shape[0]
            gamma, mu = op["gamma"], op["mu"]
            absA = np.abs(adjacency)
            dt = star_dt(gamma, float(absA.sum(axis=1).max()))       # R1
            canon = labeling_bfs_n(absA)                              # R1
            target = spec_target_n(spec, canon, n)
            c = GraphCollective(adjacency=adjacency, seed=seed,
                                gamma=gamma, mu_theta=mu)             # R2
            c.set_target(canon)
            c.write_spec_layer(target)
            prog = compile_anatomy(spec, n=n)
            if prog.rejected:
                return {"program_verified": False,
                        "rejected": prog.rejected,
                        "err_vs_target": float("nan")}
            for cl in prog.clamps:
                c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
            c.run(M142.WINDOW_H, dt=dt)
            c.release_clamps()
            reg_idx: list[int] = []
            for z in spec.zones:
                i0 = int(round(z.f0 * n))
                i1 = max(int(round(z.f1 * n)), i0 + 1)
                reg_idx.extend(range(i0, i1))
            reg_idx = sorted(set(reg_idx))
            n_ca_writes = 0
            if reg_idx:
                reg_walk = list(range(reg_idx[0], reg_idx[-1] + 1))
                region_set = set(reg_walk)
                c.amputate(slice(reg_idx[0], reg_idx[-1] + 1))
                wound_center = float(np.mean(c.theta[reg_walk]))
                parent_of: dict[int, int] = {}
                frontier: list[int] = []
                # exp97's blastema frontier under R1: |A| > 0
                for i in reg_walk:
                    nbrs = [j for j in np.where(np.abs(c.A[i]) > 0)[0]
                            if j not in region_set]
                    if nbrs:
                        parent_of[i] = int(max(
                            nbrs,
                            key=lambda j: -abs(c.theta[j] - wound_center)))
                        frontier.append(i)
                if not frontier:
                    frontier = reg_idx[:1]
                    parent_of[frontier[0]] = frontier[0]
                visited = set(frontier)
                order = [(i, parent_of[i]) for i in frontier]
                queue = list(frontier)
                while queue:
                    i = queue.pop(0)
                    for j in np.where(np.abs(c.A[i]) > 0)[0]:      # R1
                        if int(j) in region_set and int(j) not in visited:
                            visited.add(int(j))
                            parent_of[int(j)] = int(i)
                            order.append((int(j), int(i)))
                            queue.append(int(j))
                for i, src in order:
                    for _ in range(M142.STEPS_PER_CELL):
                        c.step(dt)
                    canon_src = getattr(c, "phi_spec_canon", None)
                    if c.phi_spec[i] >= M142.NEURAL_SPEC_MIN:
                        theta_new = (c.phi_spec[i]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    elif canon_src is not None:
                        theta_new = (canon_src[i]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    else:
                        theta_new = (c.theta[src]
                                     + c.rng.normal(0.0, M142.COMMIT_NOISE))
                    # ---- THE exp261 ACTIVATION (the ONLY deviation;
                    #      ZERO at g_ca = 0.0) --------------------------
                    if g_ca > 0.0:
                        v_before = float(c.V[i])
                        theta_before = float(c.theta[i])
                        p_i = float(ca_open_prob(ca_m_inf(v_before),
                                                ca_h_inf(v_before)))
                        ca2_vec = c.read_channel("ca2")
                        ca2_vec[i] = p_i
                        c.set_channel("ca2", ca2_vec)
                        gain = 1.0 + g_ca * (p_i - pbar)
                        effective = (theta_before
                                     + gain * (theta_new - theta_before))
                        c.theta[i] = effective
                        c.V[i] = effective
                        n_ca_writes += 1
                    else:
                        c.theta[i] = theta_new
                        c.V[i] = theta_new
            c.run(15.0, dt=dt)
            per_zone = {}
            ok_all = True
            for z in spec.zones:
                i0 = int(round(z.f0 * n))
                i1 = max(int(round(z.f1 * n)), i0 + 1)
                zmean = float(np.mean(c.V[i0:i1]))
                ok = abs(zmean - z.voltage) <= M142.ERR_BAR
                per_zone[z.name] = {"mean": round(zmean, 1),
                                    "ok": bool(ok)}
                ok_all &= ok
            err = float(c.pattern_error(target))
            ok_all &= err < M142.ERR_BAR
            out = {"program_verified": bool(ok_all), "per_zone": per_zone,
                   "err_vs_target": round(err, 2)}
            if return_state:
                out["final_state"] = {"V": c.V.tolist(),
                                      "target": target.tolist()}
            telemetry["n_ca_writes"] = n_ca_writes
            telemetry["ca2_last_max"] = float(
                np.abs(c.read_channel("ca2")).max())
            # C2's read-only telemetry capture: the settled theta
            # (S[:, 1]) — a COPY; it does not enter the dynamics
            telemetry["theta_final"] = c.theta.tolist()
            return out

        return _execute_signed_ca

    @contextmanager
    def _ca_route(medium, g_ca: float, pbar: float, telemetry: dict):
        """Route exp148's executor resolution (read_temporal's global
        name) to the ca2 instrument for ONE decode; the production
        attribute is restored and asserted. collective.py and every
        experiment module on disk are untouched."""
        saved = M148.execute_signed
        M148.execute_signed = _make_ca_executor(medium, g_ca, pbar,
                                                telemetry)
        try:
            yield
        finally:
            M148.execute_signed = saved
            assert M148.execute_signed is saved, \
                "executor route not restored"
            assert M148.execute_signed is _PROD_EXECUTOR, \
                "production executor binding drifted"

    def run_instrumented(med, s: int, fmax: float, g_ca: float,
                         pbar: float, telemetry: dict) -> dict:
        with _ca_route(med, g_ca, pbar, telemetry):
            return M148.decode("scoped", med, s, return_state=True,
                               f_max=fmax)

    # ---- the row builder (exp226's battery construction verbatim: the
    #      c6 cell's 25 instances via exp199's gen-seed records, seeds
    #      (1,2,3), the production scoped read — the exp258 battery
    #      verbatim, as the docstring names) ------------------------------
    def build_rows(g_ca: float, pbar, with_production: bool,
                   c2_readout: bool) -> dict:
        rows: list = []
        n_rej = 0
        rejections: list = []
        pooled_P: list = [] if c2_readout else None
        pooled_mism: list = [] if c2_readout else None
        pooled_bnd: list = [] if c2_readout else None
        seed_P: dict = {s: [] for s in seeds} if c2_readout else None
        seed_mism: dict = {s: [] for s in seeds} if c2_readout else None
        for j in range(PER_CELL):
            dep_rec = dep_by_cell[j]
            gen_seed = dep_rec["gen_seed"]
            med = CornerMedium(N400, gen_seed, cell_dims(6))
            assert med.n == N400
            fmax = float(f_max_frames(list(med.snapshots())))
            for s_idx, s in enumerate(seeds):
                prod_rec = None
                if with_production:
                    prod = M148.decode("scoped", med, s, return_state=True,
                                       f_max=fmax)
                    if not prod["ok"]:
                        n_rej += 1
                        rejections.append({"j": j, "s": s, "route": "prod",
                                           "rejection": prod["rejection"]})
                    else:
                        prod_V = np.asarray(prod["state"]["V"], dtype=float)
                        prod_T = np.asarray(prod["state"]["target"],
                                            dtype=float)
                        prod_err_exact = float(np.sqrt(
                            np.mean((prod_V - prod_T) ** 2)))
                        assert round(prod_err_exact, 2) == round(
                            prod["err"], 2), \
                            "state err vs reported err drift (prod)"
                        prod_rec = {
                            "err": float(prod["err"]),
                            "verified": bool(prod["verified"]),
                            "err_exact": prod_err_exact,
                            "V": prod_V.tolist(), "T": prod_T.tolist()}
                tel: dict = {"n_ca_writes": 0, "ca2_last_max": None,
                             "theta_final": None}
                out = run_instrumented(med, s, fmax, g_ca, pbar, tel)
                if not out["ok"]:
                    n_rej += 1
                    rejections.append({"j": j, "s": s,
                                       "route": f"g{g_ca}",
                                       "rejection": out["rejection"]})
                    rows.append({"j": j, "s": s, "gen_seed": int(gen_seed),
                                 "rejected": True,
                                 "rejection": out["rejection"]})
                    continue
                V = np.asarray(out["state"]["V"], dtype=float)
                T = np.asarray(out["state"]["target"], dtype=float)
                err_exact = float(np.sqrt(np.mean((V - T) ** 2)))
                assert round(err_exact, 2) == round(out["err"], 2), \
                    "state err vs reported err drift"
                cinfo = classify(T, med.Wbase)
                cls = cinfo["class"]
                bnd = cls == 0
                interior = cls == 2
                dev = np.abs(V - T)
                row = {"j": j, "s": s, "gen_seed": int(gen_seed),
                       "rejected": False,
                       "err": float(out["err"]),
                       "err_exact": err_exact,
                       "verified": bool(out["verified"]),
                       "n_ca_writes": int(tel["n_ca_writes"]),
                       "ca2_last_max": tel["ca2_last_max"],
                       "n_bnd": int(bnd.sum()),
                       "n_int": int(interior.sum()),
                       "bnd_max": float(dev[bnd].max()) if bnd.any() else None,
                       "int_max": (float(dev[interior].max())
                                   if interior.any() else None),
                       "nonbnd_max": float(dev[~bnd].max()),
                       "nonbnd_mean": float(dev[~bnd].mean()),
                       "bnd_errs": dev[bnd].tolist()}
                # C2's readout fields (the g_ca = 0 rows only): the
                # settled-state open-probability field vs the
                # |V - theta| mismatch (theta from the read-only
                # telemetry capture)
                if c2_readout:
                    theta = np.asarray(tel["theta_final"], dtype=float)
                    assert theta is not None and theta.shape == V.shape
                    mism = np.abs(V - theta)
                    p_row = ca_open_prob(ca_m_inf(V), ca_h_inf(V))
                    assert np.all(np.isfinite(p_row))
                    row["c2"] = {
                        "rho_row": float(spearman_ties(p_row, mism)),
                        "mean_P": float(p_row.mean()),
                        "bnd_mean_P": (float(p_row[bnd].mean())
                                       if bnd.any() else None),
                        "nonbnd_mean_P": float(p_row[~bnd].mean()),
                        "mism_max": float(mism.max()),
                        "mism_mean": float(mism.mean())}
                    pooled_P.append(p_row)
                    pooled_mism.append(mism)
                    pooled_bnd.append(bnd)
                    seed_P[s].append(p_row)
                    seed_mism[s].append(mism)
                # the replay anchors (exp258's X1 verbatim): the
                # deposit's 2-dp errs + verified, and exp208's
                # decomposition rows bit-exactly
                dec = decompose(V, T, cls, err_exact)
                ref_dec = dep208_by_j[j]["decompositions"][s_idx]
                row["replay_dep199_err"] = bool(
                    round(out["err"], 2) == float(dep_rec["errs"][s_idx]))
                row["replay_dep199_verified"] = bool(
                    bool(out["verified"])
                    == bool(dep_rec["verified"][s_idx]))
                row["replay_exp208_decomposition"] = bool(all(
                    pc["sum_sq"] == rc["sum_sq"]
                    and pc["n_cells"] == rc["n_cells"]
                    for pc, rc in zip(dec["per_class"],
                                      ref_dec["per_class"])))
                if prod_rec is not None:
                    # the dormant identity (g_ca = 0) vs the production
                    # path — bit-exact state
                    row["prod"] = {
                        "err": prod_rec["err"],
                        "verified": prod_rec["verified"],
                        "err_exact": prod_rec["err_exact"],
                        "V_bit_exact": bool(np.array_equal(
                            V, np.asarray(prod_rec["V"], dtype=float))),
                        "T_bit_exact": bool(np.array_equal(
                            T, np.asarray(prod_rec["T"], dtype=float))),
                        "err_equal": bool(row["err"] == prod_rec["err"]),
                        "verified_equal": bool(
                            row["verified"] == prod_rec["verified"])}
                rows.append(row)
            print(f"  [c6 j{j:2d}] done (g_ca={g_ca})")
        readout = None
        pbar_out = None
        if c2_readout:
            P_all = np.concatenate(pooled_P)
            M_all = np.concatenate(pooled_mism)
            B_all = np.concatenate(pooled_bnd)
            rho = float(spearman_ties(P_all, M_all))
            assert np.isfinite(rho), "pooled Spearman not finite"
            bnd_mean = float(P_all[B_all].mean())
            nonbnd_mean = float(P_all[~B_all].mean())
            pbar_out = float(P_all.mean())
            per_seed_rho = {}
            for s in seeds:
                Ps = np.concatenate(seed_P[s])
                Ms = np.concatenate(seed_mism[s])
                per_seed_rho[str(s)] = float(spearman_ties(Ps, Ms))
            readout = {
                "statistic": (
                    "Spearman(P_i, |V_i - theta_i|) pooled over EVERY "
                    "cell of EVERY verified g_ca=0 battery row (the "
                    "settled c6 battery states, 25 instances x 3 "
                    "seeds x 400 cells), plus the battery-wide "
                    "boundary-vs-non-boundary mean-P comparison "
                    "(exp208's classify canon-boundary classes, "
                    "precedence intact); per-row and per-seed rho "
                    "deposited as audit"),
                "mismatch": (
                    "|V_i - theta_i| at the settled state; theta is "
                    "the instrumented executor's read-only telemetry "
                    "capture of S[:, 1] (a copy; it does not enter "
                    "the dynamics); the row's V/T are bit-exact vs "
                    "the production decode per the identity check"),
                "P_field": ("P_i = m_inf(V_i) * h_inf(V_i) (the "
                            "ported Cav3.3 steady-state gates; "
                            "C1-verified)"),
                "n_rows": int(sum(1 for r in rows
                                  if not r.get("rejected"))),
                "n_points": int(P_all.size),
                "rho_pooled": rho,
                "rho_bar": 0.5,
                "rho_pass": bool(rho >= 0.5),
                "bnd_mean_P": bnd_mean,
                "nonbnd_mean_P": nonbnd_mean,
                "localization_pass": bool(bnd_mean > nonbnd_mean),
                "pbar": pbar_out,
                "pbar_definition": (
                    "the battery-wide mean open probability over the "
                    "same settled g_ca=0 states (P_all.mean(); one "
                    "scalar, zero re-fit; the C3 gain's reference)"),
                "pooled_P_sha256": hashlib.sha256(
                    P_all.tobytes()).hexdigest(),
                "pooled_mismatch_sha256": hashlib.sha256(
                    M_all.tobytes()).hexdigest(),
                "per_seed_rho": per_seed_rho,
                "per_row": [{"j": r["j"], "s": r["s"],
                             "rho_row": r["c2"]["rho_row"],
                             "mean_P": r["c2"]["mean_P"],
                             "bnd_mean_P": r["c2"]["bnd_mean_P"],
                             "nonbnd_mean_P": r["c2"]["nonbnd_mean_P"]}
                            for r in rows if not r.get("rejected")],
            }
        return {"rows": rows, "n_rejections": n_rej,
                "rejections": rejections,
                "c2_readout": readout, "pbar": pbar_out}

    def worst_over(rows, key_fn, pick):
        vals = [key_fn(r) for r in rows
                if not r.get("rejected") and key_fn(r) is not None]
        return (max(vals) if vals else None,
                sum(1 for r in rows if not r.get("rejected")))

    # ---- the segments -----------------------------------------------------
    G_CA = {"g025": 0.25, "g050": 0.5, "g100": 1.0}

    def _seg_c0() -> dict:
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(0.0, pbar=None, with_production=True,
                               c2_readout=True)
        finally:
            restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        assert floors_post == floors_pre, "floor restore failed"
        # the exp169-import restore (the standing convention): the
        # production -60.0 floor, restored EXPLICITLY, asserted at exit
        CORE.NEURAL_SPEC_MIN = -60.0
        rows = built["rows"]
        checks = []
        for r in rows:
            if r.get("rejected"):
                checks.append(False)
                continue
            p = r["prod"]
            checks.append(bool(
                p["V_bit_exact"] and p["T_bit_exact"]
                and p["err_equal"] and p["verified_equal"]
                and r["replay_dep199_err"] and r["replay_dep199_verified"]
                and r["replay_exp208_decomposition"]))
        n_ok = sum(1 for r in rows if not r.get("rejected"))
        identity_pass = bool(
            all(checks) and len(checks) == PER_CELL * len(SEEDS)
            and built["n_rejections"] == 0
            and n_ok == PER_CELL * len(SEEDS))
        wb, _ = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, \
            "read-only reference changed (c0)"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            "collective.py changed (c0)"
        return {"g_ca": 0.0, "port": port_record, "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_checks_pass": sum(1 for c in checks if c),
                "n_checks": len(checks),
                "identity_pass": identity_pass,
                "identity_disclosure": (
                    "g_ca = 0 vs the production scoped decode: V/T "
                    "states bit-exact, errs + verified equal, "
                    "exp199's deposit replayed at its 2-dp rounding, "
                    "exp208's decomposition rows reproduced bit-exactly "
                    "(exp226's R1 verbatim) — the dormant identity is "
                    "C3's own migration-gate face and the state source "
                    "for C2's readout and Pbar"),
                "c2_readout": built["c2_readout"],
                "pbar": built["pbar"],
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": identity_pass}

    def _seg_grid(seg: str, pbar: float) -> dict:
        g_ca = G_CA[seg]
        pin_modules = list(M199.PIN_MODULES)
        floors_pre = [getattr(m, "NEURAL_SPEC_MIN", None)
                      for m in pin_modules]
        pin_floor()
        try:
            assert all(getattr(m, "NEURAL_SPEC_MIN", None)
                       == M199.DEP160_FLOOR for m in pin_modules), \
                "instrument pin failed"
            built = build_rows(g_ca, pbar=pbar, with_production=False,
                               c2_readout=False)
        finally:
            restore_floor()
        floors_post = [getattr(m, "NEURAL_SPEC_MIN", None)
                       for m in pin_modules]
        assert floors_post == floors_pre, "floor restore failed"
        CORE.NEURAL_SPEC_MIN = -60.0
        rows = built["rows"]
        wb, n_ok = worst_over(rows, lambda r: r["bnd_max"], None)
        wi, _ = worst_over(rows, lambda r: r["int_max"], None)
        wn, _ = worst_over(rows, lambda r: r["nonbnd_max"], None)
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        assert shas_now == READ_ONLY_SHAS, \
            f"read-only reference changed ({seg})"
        assert _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                 "collective.py")) == COLLECTIVE_SHA, \
            f"collective.py changed ({seg})"
        return {"g_ca": g_ca, "pbar_used": pbar, "port": port_record,
                "rows": rows,
                "n_rows": len(rows), "n_ok": n_ok,
                "n_rejections": built["n_rejections"],
                "rejections": built["rejections"],
                "n_ca_writes_total": sum(r["n_ca_writes"] for r in rows
                                         if not r.get("rejected")),
                "ca2_last_max_over_rows": max(
                    (r["ca2_last_max"] for r in rows
                     if not r.get("rejected")), default=None),
                "worst_bnd_err_mV": wb, "worst_int_err_mV": wi,
                "worst_nonbnd_err_mV": wn,
                "read_only_shas": READ_ONLY_SHAS,
                "collective_py_sha256": COLLECTIVE_SHA,
                "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                "pass": bool(built["n_rejections"] == 0
                             and n_ok == PER_CELL * len(SEEDS))}

    def _c2_gate(path: str) -> dict:
        with open(path) as f:
            sec = json.load(f)["section"]
        assert sec["g_ca"] == 0.0 and sec["identity_pass"], \
            "the C2 gate needs the verified c0 checkpoint"
        ro = sec["c2_readout"]
        c2_pass = bool(ro["rho_pass"] and ro["localization_pass"])
        return {"seg": "c2-gate",
                "c2_pass": c2_pass,
                "rho_pooled": ro["rho_pooled"],
                "rho_bar": ro["rho_bar"],
                "rho_pass": ro["rho_pass"],
                "bnd_mean_P": ro["bnd_mean_P"],
                "nonbnd_mean_P": ro["nonbnd_mean_P"],
                "localization_pass": ro["localization_pass"],
                "pbar": sec["pbar"],
                "source": os.path.abspath(path),
                "note": ("the C2 decision that conditions the grid "
                         "dispatch (the docstring: C3 runs ONLY if C2 "
                         "passes); the merge re-derives the SAME "
                         "decision from the c0 section and asserts "
                         "equality — the deposit's C2 gate record is "
                         "the merge's evaluation, exactly once")}

    # ---- the merge (the gates, each evaluated exactly once) --------------
    def _merge(paths_a: list, paths_b) -> dict:
        # the exp169-import restore applied BEFORE the record is built
        # (exp258's disclosed repair, standing practice here): the
        # merge process's own import chain leaves the -35.0 instrument
        # floor; the production -60.0 floor is restored here so the
        # deposit's merge-side floor_at_exit carries the floor the
        # discipline names (the segment sections restored -60.0
        # themselves)
        CORE.NEURAL_SPEC_MIN = -60.0
        sections: dict = {}
        for p in paths_a:
            with open(p) as f:
                d = json.load(f)
            assert d["seg"] not in sections, "duplicate segment"
            sections[d["seg"]] = d["section"]
        c0 = sections["c0"]
        grid_secs = {k: sections[k] for k in ("g025", "g050", "g100")
                     if k in sections}

        # the file-integrity gate: the pre-registered header (docstring,
        # imports, constants — 54fc177's bytes through the
        # BETSE_TOOLBOX line)
        raw_self = open(os.path.abspath(__file__), "rb").read()
        mk = raw_self.find(_HEADER_MARKER.encode())
        assert mk != -1, "header marker not found"
        header_sha = hashlib.sha256(
            raw_self[:mk + len(_HEADER_MARKER)]).hexdigest()
        header_unchanged = bool(header_sha == EXPECTED_HEADER_SHA256)
        assert header_unchanged, (
            f"the pre-registered header drifted: {header_sha}")

        # ---- C1 (the port; the merge re-derives it and asserts
        #      equality with the c0 section's record — deterministic)
        port_now = _port_verification()
        assert port_now == c0["port"], "C1 port record drifted at merge"
        c1_pass = bool(port_now["pass"])
        assert c1_pass, "C1 failed at merge — STOP"

        # ---- row-set integrity across sections (T and Wbase are
        #      g-independent, so the row sets must match 1:1) -----------
        base_rowmap = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                       for r in c0["rows"] if not r.get("rejected")}
        for k, sec in grid_secs.items():
            m = {(r["j"], r["s"]): (r["n_bnd"], r["gen_seed"])
                 for r in sec["rows"] if not r.get("rejected")}
            assert m == base_rowmap, f"row set drifted ({k})"

        # ---- C2 (the readout; the gate, evaluated exactly once, HERE)
        ro = c0["c2_readout"]
        c2_pass = bool(ro["rho_pass"] and ro["localization_pass"])

        # ---- C3 (the write coupling; ONLY if C2 passes) ----------------
        identity_ok = bool(c0["identity_pass"])
        base_bnd = c0["worst_bnd_err_mV"]
        base_wn = c0["worst_nonbnd_err_mV"]
        assert base_bnd is not None and base_bnd > 0.0, \
            "degenerate baseline worst boundary-row err"
        c3_record: dict = {"status": None, "pass": None}
        c3_reduction = None
        nonbnd_change = None
        g_star = None
        cells: dict = {}
        if not c2_pass:
            c3_record = {
                "status": "SKIPPED-C2-FAIL", "pass": None,
                "clause": ("the HH-gated ca2 pull at the pre-named "
                           "grid {0.25, 0.5, 1.0} — NOT RUN: the "
                           "docstring gates C3 on C2 (C2 REFUTE -> C3 "
                           "skipped and recorded SKIPPED-C2-FAIL); no "
                           "g_ca > 0 decode was executed anywhere in "
                           "this experiment"),
                "identity_at_g0": identity_ok,
                "n_identity_checks": c0["n_checks"],
                "n_identity_checks_pass": c0["n_checks_pass"]}
        else:
            reds = {}
            for k, sec in sorted(grid_secs.items()):
                gv = float(sec["g_ca"])
                wb = sec["worst_bnd_err_mV"]
                wn = sec["worst_nonbnd_err_mV"]
                red = float((base_bnd - wb) / base_bnd)
                reds[gv] = red
                cells[str(gv)] = {
                    "worst_bnd_err_mV": wb,
                    "worst_int_err_mV": sec["worst_int_err_mV"],
                    "worst_nonbnd_err_mV": wn,
                    "reduction_vs_dormant": red,
                    "nonbnd_change_vs_dormant":
                        float((wn - base_wn) / base_wn),
                    "n_ca_writes_total": sec["n_ca_writes_total"],
                    "ca2_last_max_over_rows":
                        sec["ca2_last_max_over_rows"],
                    "n_rows": sec["n_rows"], "n_ok": sec["n_ok"]}
            assert len(reds) == 3, "the pre-named grid is incomplete"
            g_star = max(reds, key=lambda k: reds[k])
            c3_reduction = reds[g_star]
            nonbnd_change = cells[str(g_star)]["nonbnd_change_vs_dormant"]
            c3_pass = bool(identity_ok and c3_reduction >= 0.10
                           and nonbnd_change <= 0.05)
            c3_record = {
                "status": "PASS" if c3_pass else "REFUTE",
                "pass": c3_pass,
                "clause": ("the best grid cell reduces the worst "
                           "boundary-row err >= 10% AND the "
                           "non-boundary rows' worst-err change "
                           "<= +5% at that cell (the exp258/exp259 "
                           "forms verbatim; the gate reads the best "
                           "cell, zero post-hoc selection; all three "
                           "nonzero g values reported; g_ca = 0 is "
                           "the dormant identity — bit-exact per the "
                           "identity check on the c0 rows)"),
                "identity_at_g0": identity_ok,
                "n_identity_checks": c0["n_checks"],
                "n_identity_checks_pass": c0["n_checks_pass"],
                "g_star": float(g_star),
                "reduction_at_best_cell": c3_reduction,
                "nonbnd_change_at_best_cell": nonbnd_change,
                "baseline": {"worst_bnd_err_mV": base_bnd,
                             "worst_nonbnd_err_mV": base_wn,
                             "source": ("c0's g_ca=0 rows (bit-exact "
                                        "vs production per the "
                                        "identity check)")},
                "all_cells": cells}

        # ---- C4 (the discipline) -----------------------------------------
        shas_ok = True
        for sec in sections.values():
            if sec.get("read_only_shas") != READ_ONLY_SHAS:
                shas_ok = False
        shas_now = {k: _sha(v) for k, v in READ_ONLY_PATHS.items()}
        deposits_unchanged = bool(shas_now == READ_ONLY_SHAS and shas_ok)
        coll_now = _sha(os.path.join(ROOT, "cultivation", "bioelectric",
                                     "collective.py"))
        coll_unchanged = bool(coll_now == COLLECTIVE_SHA)
        n_rej_total = sum(sec["n_rejections"] for sec in sections.values())
        det = {"pass_b_byte_identical": None, "segments": {}}
        if paths_b:
            assert len(paths_b) == len(paths_a), \
                "pass B segment count mismatch"
            for pa, pb in zip(paths_a, paths_b):
                sa = hashlib.sha256(open(pa, "rb").read()).hexdigest()
                sb = hashlib.sha256(open(pb, "rb").read()).hexdigest()
                det["segments"][os.path.basename(pb)] = {
                    "pass_a_sha256": sa, "pass_b_sha256": sb,
                    "byte_identical": bool(sa == sb)}
            det["pass_b_byte_identical"] = bool(all(
                v["byte_identical"] for v in det["segments"].values()))
        floor_ok = all(float(sec["floor_at_exit"]) == -60.0
                       for sec in sections.values())
        c4_pass = bool(deposits_unchanged and coll_unchanged
                       and floor_ok and n_rej_total == 0
                       and det["pass_b_byte_identical"]
                       and header_unchanged)

        # ---- branch + verdict --------------------------------------------
        evaluated = [c1_pass, c2_pass, c4_pass]
        if c3_record["pass"] is not None:
            evaluated.append(c3_record["pass"])
        n_pass = sum(1 for v in evaluated if v)
        if not c2_pass:
            branch = "CA2-INERT"
        elif c3_record["pass"]:
            branch = "CA2-CARRIES"
        else:
            branch = "CA2-READOUT-ONLY"
        c3_txt = c3_record["status"]
        c3_detail = ""
        if c3_reduction is not None:
            c3_detail = (f" (reduction {c3_reduction:+.4f} at "
                         f"g_ca={g_star}; non-boundary change "
                         f"{nonbnd_change:+.4f})")
        verdict = (
            f"{n_pass}/{len(evaluated)} evaluated gates | "
            f"C1 {'PASS' if c1_pass else 'FAIL'} "
            f"(port: 0.0 delta on m_inf/m_tau/h_inf/h_tau/P, "
            f"{port_now['grid']['n_points']}-pt grid) | "
            f"C2 {'PASS' if c2_pass else 'REFUTE'} "
            f"(pooled rho {ro['rho_pooled']:.4f} vs bar "
            f"{ro['rho_bar']}; boundary mean P "
            f"{ro['bnd_mean_P']:.6f} vs non-boundary "
            f"{ro['nonbnd_mean_P']:.6f}) | "
            f"C3 {c3_txt}{c3_detail} | "
            f"C4 {'PASS' if c4_pass else 'FAIL'} | {branch}")

        deposit = {
            "exp": "exp261",
            "claim": (
                "CA2 CHANNEL ACTIVATION, BETSE-GROUNDED (the THIRD "
                "channel activation under the exp257 schema): ch4 "
                "ca2 — the port of BETSE's Cav3.3 T-type HH kinetics "
                "(m_inf/h_inf/m_tau/h_tau; P = m^1 * h^1; Traboulsie "
                "et al. 2007) + the Ca-ATPase pump's Keq steady-state "
                "reading (the 2-charge term), zero re-fit; C1 "
                "verifies the port at 0.0 delta on the pre-named "
                "401-point V-grid; C2 tests whether the "
                "open-probability field P_i = m(V_i) h(V_i) on the "
                "settled c6 battery localizes the boundary excess "
                "(Spearman(P_i, |V_i - theta_i|) >= 0.5 AND boundary "
                "mean P > non-boundary mean P); C3 (ONLY if C2 "
                "passes) the HH-gated theta-restoration pull at the "
                "pre-named g_ca grid {0, 0.25, 0.5, 1.0} (C2 PASS + "
                "C3 PASS -> CA2-CARRIES / C3 REFUTE -> "
                "CA2-READOUT-ONLY / C2 REFUTE -> CA2-INERT)"),
            "pre_registered": {
                "gates_source": (
                    "module docstring, committed before any body "
                    "(pre-registration 54fc177, batch 23; gates C1-C4 "
                    "fixed there, each evaluated exactly once); the "
                    "pre-registered header (docstring + imports + "
                    "constants) sha256-verified byte-unchanged at "
                    "merge: " + EXPECTED_HEADER_SHA256),
                "docstring_sha256": DOCSTRING_SHA256,
                "mechanism": (
                    "the HH-gated ca2 pull: at EVERY commit of the "
                    "regenerated region's walk (exp142's "
                    "execute_signed commit loop, routed through the "
                    "experiment's own instrument — collective.py "
                    "untouched), the cell's theta restoration pull "
                    "(the commit displacement theta_new - "
                    "theta_before) is multiplied by (1 + g_ca * "
                    "(P_i - Pbar)); P_i = m_inf(V_i) * h_inf(V_i) at "
                    "the cell's LIVE Vmem read BEFORE the commit "
                    "write (the HH gate follows the running state); "
                    "Pbar = the battery-wide mean open probability "
                    "over the settled g_ca=0 c6 battery rows (the c0 "
                    "checkpoint's own verified states; one scalar, "
                    "zero re-fit); the ca2 channel (ch4) is WRITTEN "
                    "with the cell's open probability at the same "
                    "commit via the public accessors "
                    "(c.read_channel('ca2') / c.set_channel('ca2', "
                    "...)) — the activation's channel-write face; the "
                    "DISCLOSED READING (outcome-blind, fixed before "
                    "any g_ca > 0 run): the docstring's 'the cell's "
                    "theta restoration pull' names EVERY region "
                    "cell's commit (the commit loop is the only theta "
                    "restoration the executor performs) and the HH "
                    "open probability is the gate — no class "
                    "restriction — which is what makes the coupling "
                    "'HH-gated'; the rng stream is untouched (the "
                    "gain multiplies the displacement AFTER theta_new "
                    "is drawn — identical draws across the whole "
                    "grid); the effective commit is written to BOTH "
                    "channels exactly as the verbatim commit writes "
                    "theta_new to both; g_ca = 0.0 takes the verbatim "
                    "path with ZERO deviation (no ca2 write, no gain) "
                    "— the bit-exact dormant default, the migration "
                    "gate's own face; the settled theta for C2's "
                    "mismatch is the instrumented executor's "
                    "read-only telemetry capture of S[:, 1] (a copy; "
                    "it does not enter the dynamics)"),
                "row_conventions": (
                    "a ROW = one per-cell err |V_i - T_i| (mV) at a "
                    "cell of the exp226/exp229 canon-boundary row "
                    "class (exp208's classify, precedence intact), "
                    "pooled over exp226's c6 battery (25 instances x "
                    "3 seeds); 'worst boundary-row err' = the max "
                    "over that pooled row set; 'non-boundary rows' = "
                    "the complement under the same convention"),
                "conventions": (
                    "the executor instrument is exp142's "
                    "execute_signed copied line-for-line into this "
                    "module with the ONE activation block; bit-exact "
                    "identity at g_ca = 0 is asserted per row against "
                    "the production decode AND exp199's deposit AND "
                    "exp208's decomposition rows (exp226's R1 "
                    "machinery verbatim); T and Wbase are "
                    "g-independent so the row sets match 1:1 across "
                    "the grid (asserted at merge); the C2-gated "
                    "dispatch: the grid segments were launched only "
                    "after --c2-gate read C2 PASS from the c0 "
                    "checkpoint section file")},
            "port_record": port_now,
            "sections": {k: sections[k] for k in sorted(sections)},
            "readout": ro,
            "grid": {"g_values": [0.0, 0.25, 0.5, 1.0],
                     "g_star": (float(g_star)
                                if g_star is not None else None),
                     "c3_status": c3_record["status"],
                     "cells": cells},
            "gates": {
                "C1": {"pass": c1_pass,
                       "clause": ("the ported gate functions reproduce "
                                  "BETSE's own curves bit-exactly: "
                                  "m_inf/h_inf/m_tau/h_tau/P computed "
                                  "BOTH by the ported functions and "
                                  "by a direct import-free "
                                  "recomputation from the quoted "
                                  "source lines on the 401-point "
                                  "V-grid (-85..+5 mV); equality "
                                  "asserted to 0.0 delta"),
                       "max_abs_delta":
                           port_now["max_abs_delta_ported_vs_recomputed"],
                       "transcription_note":
                           port_now["transcription_note"],
                       "ran_first": True,
                       "fail_stop": True},
                "C2": {"pass": c2_pass,
                       "clause": ("Spearman(P_i, |V_i - theta_i|) "
                                  ">= 0.5 AND the boundary cells' "
                                  "mean P exceeds the non-boundary "
                                  "cells' mean, on the settled c6 "
                                  "battery states (zero-risk: no "
                                  "dynamics touched, the channel "
                                  "READ only)"),
                       "rho_pooled": ro["rho_pooled"],
                       "rho_bar": ro["rho_bar"],
                       "rho_pass": ro["rho_pass"],
                       "bnd_mean_P": ro["bnd_mean_P"],
                       "nonbnd_mean_P": ro["nonbnd_mean_P"],
                       "localization_pass": ro["localization_pass"],
                       "n_points": ro["n_points"],
                       "per_seed_rho": ro["per_seed_rho"]},
                "C3": c3_record,
                "C4": {"pass": c4_pass,
                       "references_read_only": {
                           k: {"sha256": READ_ONLY_SHAS[k],
                               "unchanged": bool(shas_now[k]
                                                 == READ_ONLY_SHAS[k])}
                           for k in READ_ONLY_SHAS},
                       "collective_py_sha256": coll_now,
                       "collective_py_unchanged": coll_unchanged,
                       "n_rejections_total": n_rej_total,
                       "floor_at_exit": float(CORE.NEURAL_SPEC_MIN),
                       "floor_ok": bool(
                           float(CORE.NEURAL_SPEC_MIN) == -60.0),
                       "determinism": det,
                       "header_unchanged": header_unchanged}},
            "branch": branch,
            "verdict": verdict,
            "notes": [
                "body written by the run agent under the body-only "
                "discipline; the pre-registered header (docstring, "
                "imports, constants) byte-unchanged, verified against "
                "54fc177 by sha256 at merge",
                "TRANSCRIPTION NOTE (disclosed): the pre-registered "
                "K1 prose form of m_inf "
                "(1/(1+exp((V+45.454426)/5.073015))) drops the sign "
                "of BETSE's own denominator "
                "(vg_ca.py:160/176: (V - -45.454426) / -5.073015); "
                "the two forms are exact complements (sum = 1, "
                "demonstrated on the grid); the FILE line is the "
                "authoritative port per the docstring's own VERBATIM "
                "clause and C1's headline ('reproduce BETSE's own "
                "curves bit-exactly'); the docstring is "
                "byte-unchanged and this note is the disclosure — no "
                "gate outcome depends on the prose form (C1 compares "
                "the ported functions to the FILE lines)",
                "C1 ran FIRST in every process (segments, c2-gate, "
                "merge) and fail-stops with SystemExit(3) before ANY "
                "battery work; the deposit's C1 record is the merge's "
                "own re-derivation, asserted equal to the c0 "
                "section's embedded record",
                "the C2-gated dispatch (the docstring: C3 runs ONLY "
                "if C2 passes): the c0 segment is the checkpoint; "
                "--c2-gate read the C2 decision from it BEFORE any "
                "g_ca > 0 segment was launched; on a C2 REFUTE this "
                "merge records C3 as SKIPPED-C2-FAIL and no g_ca > 0 "
                "decode exists anywhere in the experiment",
                "the activation instrument routes exp148's executor "
                "name to the experiment's own verbatim copy of "
                "exp142's execute_signed for the instrumented decodes "
                "only; the production binding is restored and "
                "asserted around every decode; no file on disk "
                "modified but this module",
                "the K2 pump face is RECORDED, not used in any "
                "dynamics (the docstring's own clause): the quoted "
                "Keq line evaluated directly at BETSE's pump "
                "constants, monotone-increasing-in-Vm asserted",
                "no wall-clock fields anywhere in this deposit; "
                "deterministic re-run recorded via pass B byte-"
                "identity (and the merge itself re-run byte-"
                "identically)"],
            "deposit_fingerprint": None,
        }
        deposit["deposit_fingerprint"] = _fingerprint(
            {k: v for k, v in deposit.items() if k != "deposit_fingerprint"})
        return deposit

    # ---- dispatch ---------------------------------------------------------
    if args.merge is not None:
        result = _merge(args.merge, args.pass_b)
    elif args.c2_gate is not None:
        result = _c2_gate(args.c2_gate)
    elif args.seg == "c0":
        result = {"seg": "c0", "section": _seg_c0()}
    elif args.seg in G_CA:
        assert args.pbar_from is not None, \
            "grid segments need --pbar-from (the c0 checkpoint)"
        with open(args.pbar_from) as f:
            _c0sec = json.load(f)["section"]
        assert _c0sec["g_ca"] == 0.0 and _c0sec["identity_pass"], \
            "the c0 checkpoint is not a verified dormant battery"
        assert _c0sec["c2_readout"]["rho_pass"] \
            and _c0sec["c2_readout"]["localization_pass"], \
            "C2 did not pass on the checkpoint — C3 must not run"
        result = {"seg": args.seg,
                  "section": _seg_grid(args.seg,
                                       float(_c0sec["pbar"]))}
    else:
        raise SystemExit("use --seg {c0,g025,g050,g100} / --c2-gate / "
                         "--merge (runner split is canonical)")

    with open(out_path, "w") as f:
        json.dump(result, f, indent=1, default=str)
    if args.merge:
        print(f"=== exp261 MERGE: branch {result['branch']} ===")
        for k, v in result["gates"].items():
            _st = ("SKIPPED" if v.get("status") == "SKIPPED-C2-FAIL"
                   else ("PASS" if v["pass"] else "REFUTE/FAIL"))
            print(f"  {k}: {_st}")
        print(f"  {result['verdict']}")
    else:
        print(f"=== exp261 seg {result['seg']} written ===")
    # the production floor at exit, asserted (the exp169-import
    # restore convention)
    CORE.NEURAL_SPEC_MIN = -60.0
    assert float(getattr(CORE, "NEURAL_SPEC_MIN", None)) == -60.0, \
        "production floor not restored at exit"
    return result


if __name__ == "__main__":
    main()
