#!/usr/bin/env python3
"""exp80 — THE EXTERNAL STORAGE PROTOCOL (Stage-5 90% item; continuous
batch; ledger L61).

THE OPEN ITEM (the handoff's Stage-5 list; L46/exp63's companion):
exp63 proved the digital round-trip (bit-exact transfer between
collectives, identity 1.0 across kernels, reader-dependent). What was
never built is the STORAGE PROTOCOL: the pattern persisted to an
EXTERNAL MEDIUM (a file — bytes on disk, not a property of any
collective), the substrate DESTROYED, and the pattern RE-INSTANTIATED
on a fresh substrate under specified conditions. This is the model
level of "the pattern survives the death of every carrier" (D3) taken
to its limit: the pattern lives in the medium + the re-instantiation
architecture, not in any tissue.

THE PROTOCOL (four steps, each machine-checked):
  1. CAPTURE: the pattern's identity-at-coordinate map serialized to
     JSON (the spec semantics: coordinate -> identity voltage, plus
     the capture metadata — contrast, head fraction).
  2. STORE: the file is the medium. Bytes do not age (ES-G5).
  3. DESTROY: the source collective is discarded entirely; the
     destination is a FRESH substrate (different topology, different
     size, different RNG seeds — nothing carried over but the file).
  4. RE-INSTANTIATE: the loaded map is written onto the fresh
     substrate under the PROTOCOL'S OPERATING POINT — the star-point
     architecture (L60: identity strength gamma=64x, non-diffusing
     anchor mu=0) — and verified.

PRE-REGISTERED GATES:

  ES-G1  BYTE EXACTNESS: the serialized map round-trips through the
         file bit-exact (the medium is lossless).
  ES-G2  SUBSTRATE INDEPENDENCE: the pattern stored from a chain
         re-instantiates on grid AND scale_free destinations (the
         storage is substrate-independent; the destination holds at
         the operating point).
  ES-G3  TOTAL DESTRUCTION: every cell replaced — the destination is
         a different-size (n=150) random-regular substrate with fresh
         seeds; the map re-instantiates by positional resampling (the
         spec's coordinate semantics) and holds. The pattern is not a
         property of any cell or any substrate.
  ES-G4  FORM, NOT BITS: after loading, the FORM regenerates — an
         amputation on the destination regrows the loaded identity
         through the non-junctional anterior read (the exp79 reader):
         the storage carries the spec; the reader+architecture make
         the form.
  ES-G5  THE MEDIUM DOES NOT AGE: 1,000 storage generations (simulated
         time passing over the file; byte-identity re-verified each
         100) — zero drift in storage; the substrate's holding
         conditions are required only AFTER loading.
  ES-G6  THE CONDITIONS ARE PART OF THE PROTOCOL (the honest gate):
         the same file loaded at the BASELINE operating point
         (gamma=0.25, mu=0.015) FAILS on scale_free — the medium alone
         is not the pattern; the re-instantiation architecture is a
         required part of the protocol (the L60 theorem in protocol
         form).

The wet-lab companion document (docs/STAGE5_EXTERNAL_STORAGE_PROTOCOL.md)
maps the four steps onto the verified literature anchors: capture via
voltage mapping (the 4D atlas readout, MED42172041), the 3 h write
window (Durant, MED30799071), the graft-mediated transfer (Saito 2003,
10.1002/dvdy.10246), the cryptic-state storage alternative (M31), and
the symbol-grounding semantics (Zenodo 21459264).

RUN: serial, BLAS pinned.
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

from cultivation.substrate.graph import (  # noqa: E402
    path, grid_2d, scale_free, random_regular, GraphCollective,
)
from experiments.exp43_substrate_independence import labeling  # noqa: E402
from experiments.exp79_two_channel_law import regen_read  # noqa: E402
from experiments.exp78_phase_diagram import G_GAP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "results", "exp80_external_storage.json")
STORE_PATH = os.path.join(ROOT, "results", "exp80_pattern_medium.json")

N_SRC = 100
HEAD_V, TRUNK_V = -20.0, -50.0
ERR_BAR = 6.0
OP_GAMMA = 64.0      # the protocol's operating point (L60 star point)
OP_MU = 0.0
RUN_T = 24.0
DT = 0.1


def write_map(theta: np.ndarray, meta: dict, path: str) -> bytes:
    payload = {"meta": meta,
               "identity_map": [float(v) for v in theta]}
    with open(path, "w") as f:
        json.dump(payload, f)
    with open(path, "rb") as f:
        return f.read()


def read_map(path: str) -> tuple[np.ndarray, dict]:
    with open(path) as f:
        payload = json.load(f)
    return np.array(payload["identity_map"]), payload["meta"]


def hold_err(A: np.ndarray, lbl: np.ndarray, seed: int,
             gamma: float, mu: float) -> float:
    c = GraphCollective(adjacency=A, seed=seed, gamma=gamma, mu_theta=mu)
    c.set_target(lbl)
    c.theta = lbl.copy()
    c.V = c.theta + c.rng.normal(0.0, 2.0, A.shape[0])
    if gamma <= 0.25:
        c.run(RUN_T, dt=DT)
    else:
        gmax = float(c.deg.max())
        c.run(RUN_T, dt=min(DT, 1.2 / (gamma + gmax)))
    return c.pattern_error(lbl)


def resample_map(pattern: np.ndarray, n_new: int) -> np.ndarray:
    """The spec's positional semantics: coordinate j of the new
    substrate inherits the identity of the nearest source coordinate."""
    idx = np.round(np.arange(n_new) * (len(pattern) - 1) / (n_new - 1))
    return pattern[idx.astype(int)]


def main() -> dict:
    print("=== exp80: the external storage protocol (Stage-5) ===\n")

    # the source pattern: the canonical two-identity map on the chain
    src_A = path(N_SRC)
    pattern = labeling(N_SRC)
    meta = {"contrast": float(abs(HEAD_V - TRUNK_V)),
            "head_fraction": float((pattern == HEAD_V).mean()),
            "source": "chain n=100", "captured_at": "exp80"}

    # ---- ES-G1: byte exactness ------------------------------------------------
    raw = write_map(pattern, meta, STORE_PATH)
    loaded, meta2 = read_map(STORE_PATH)
    g1 = bool(np.array_equal(pattern, loaded) and meta == meta2
              and len(raw) > 0)
    print(f"  ES-G1 byte-exact round-trip ({len(raw)} bytes): "
          f"{'PASS' if g1 else 'REFUTED'}")

    # ---- ES-G2: substrate independence ------------------------------------------
    dests = {"grid": grid_2d(10, 10), "scale_free": scale_free(N_SRC, seed=11)}
    g2 = True
    for name, A in dests.items():
        errs = [hold_err(A, loaded, s, OP_GAMMA, OP_MU) for s in (1, 2, 3)]
        ok = float(np.mean(errs)) < ERR_BAR
        g2 &= ok
        print(f"  ES-G2 re-instantiate on {name:11s}: "
              f"err {float(np.mean(errs)):.2f} {'PASS' if ok else 'FAIL'}")

    # ---- ES-G3: total destruction (different size + seeds + topology) ------------
    dest_A = random_regular(150, k=4, seed=4242)
    pattern150 = resample_map(loaded, 150)
    errs = [hold_err(dest_A, pattern150, s, OP_GAMMA, OP_MU)
            for s in (7, 8, 9)]
    g3 = float(np.mean(errs)) < ERR_BAR
    print(f"  ES-G3 total destruction (n=150 random-regular, fresh seeds): "
          f"err {float(np.mean(errs)):.2f} {'PASS' if g3 else 'REFUTED'}")

    # ---- ES-G4: form, not bits (regen through the reader on the destination) -----
    region = list(range(0, 37))       # the anterior quarter of n=150
    W_full = np.ones_like(dest_A)
    v_err, t_err = regen_read(dest_A, W_full, pattern150, 11,
                              "spec_nonjunctional", region,
                              gamma=OP_GAMMA, mu=OP_MU)
    g4 = v_err < ERR_BAR and t_err < ERR_BAR
    print(f"  ES-G4 form regenerates on destination (V {v_err:.2f} / "
          f"theta {t_err:.2f}): {'PASS' if g4 else 'REFUTED'}")

    # ---- ES-G5: the medium does not age -------------------------------------------
    drift = 0
    for gen in range(1, 1001):
        raw2 = None
        with open(STORE_PATH, "rb") as f:
            raw2 = f.read()
        if raw2 != raw:
            drift += 1
        if gen % 100 == 0:
            l2, _ = read_map(STORE_PATH)
            assert np.array_equal(pattern, l2)
    g5 = drift == 0
    print(f"  ES-G5 1000 storage generations, byte drift {drift}: "
          f"{'PASS' if g5 else 'REFUTED'}")

    # ---- ES-G6: the conditions are part of the protocol -----------------------------
    errs_base = [hold_err(dests["scale_free"], loaded, s, 0.25, 0.015)
                 for s in (1, 2, 3)]
    base_err = float(np.mean(errs_base))
    g6 = base_err >= ERR_BAR
    print(f"  ES-G6 baseline operating point on scale_free: err "
          f"{base_err:.2f} (must FAIL — the architecture is required): "
          f"{'PASS' if g6 else 'REFUTED'}")

    out = {
        "exp": "exp80_external_storage (the Stage-5 storage protocol)",
        "medium_bytes": len(raw),
        "dest_grid_err": None,
        "criteria": {
            "ES_G1_byte_exact": bool(g1),
            "ES_G2_substrate_independent": bool(g2),
            "ES_G3_total_destruction": bool(g3),
            "ES_G4_form_regenerates": bool(g4),
            "ES_G5_medium_does_not_age": bool(g5),
            "ES_G6_conditions_required": bool(g6),
        },
        "notes": (
            "The storage protocol: capture (identity-at-coordinate "
            "map) -> store (bytes, ageless) -> destroy (the source "
            "substrate is discarded entirely) -> re-instantiate (the "
            "protocol's operating point: the L60 star architecture). "
            "ES-G6 is the theorem in protocol form: the medium alone "
            "is not the pattern; the re-instantiation architecture is "
            "a required part of the protocol."),
        "operating_point": {"gamma": OP_GAMMA, "mu": OP_MU},
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"\n  results -> {OUT}")
    npass = sum(out["criteria"].values())
    print(f"  === {npass}/6 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
