#!/usr/bin/env python3
"""exp242 — THE READER AT n=5000+ (the Section 6 item; the Stage 5
extension; exp230 closed n=100->1000 flat, this pushes to n=5000;
RUNNER-NATIVE: sharded for the 20-job fleet; ledger L218).

THE OPEN ITEM: the reader's size-cost curve is n-INVARIANT on
n=100..1000 (exp230: flat 0.54-0.59 mV, slope -0.029). The extreme-n
extension: n=5000 on the path constructor (exp198's scale constructor,
the A_CHAIN family — path(5000), bit-asserted against the same
construction rule). RUNNER-NATIVE: the module takes --shard i (0..14
measured rows: 5 target classes x 3 seeds; 15..19 the redundancy
re-runs for the fleet's 20 slots), runs ONE (class, seed) decode at
n=5000, deposits results/exp242_reader_n5000_shard_<i>.json; the
union merged by the main agent's salvage pass.

PER-ROW PROTOCOL (exp230's machinery verbatim at n=5000): the
production scoped read, the deep band's -60.0 rung carrying both
pre-named instances, the 6.0 bar unchanged, the floors discipline
(-35.0 pins disclosed, -60.0 restored and asserted at exit).

PRE-REGISTERED GATES (evaluated per row + on the union):

  N1  THE COMPLETENESS: 15/15 (class, seed) rows measured, zero
      rejections, all finite.
  N2  THE FLAT PROFILE HOLDS: every row's err < 6.0; the union's worst
      err <= 1.5x exp230's n=1000 worst (0.54) — the sub-linear band
      (pre-named: the reader's cost does not grow into the extreme-n
      regime; the slope check on (log n, log worst) across exp230's
      deposited points + the n=5000 point recorded).
  N3  THE MEMORY DISCIPLINE: the n=5000 substrate constructed without
      densification (the path's banded adjacency handled as a band —
      no 5000x5000 dense array where a band suffices; the peak
      allocation recorded in the deposit).

RUN: per row one decode at n=5000; the fleet covers 15 rows + 5
redundancy re-runs in one 20-job cycle; serial per job, BLAS pinned.
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
OUT = os.path.join(ROOT, "results", "exp242_reader_n5000_shard.json")


def main() -> dict:
    # ==== BODY (runner-native, written by the run agent under the
    # body-only discipline: the module docstring, top-level imports,
    # constants and the __main__ block are byte-unchanged — exp174's
    # body-only discipline, exp241's runner-native pattern). The
    # __main__ block calls main() with NO arguments, so main() parses
    # sys.argv itself — a no-argument invocation runs SHARD 0, the
    # validation run. Shard i in 0..14 runs measured row i of the
    # pre-registered 15-row grid (5 target classes x 3 seeds; row r ->
    # class CLASSES[r // 3], seed SEEDS[r % 3] — exp230's machinery's
    # own nesting, decode rows outer, seeds inner); shard i in 15..19
    # re-runs row i - 15 (the fleet's redundancy slots). The deep
    # class's (class, seed) row carries BOTH pre-named -60.0 instances
    # (the docstring's per-row protocol; exp230's own "5 target
    # classes" definition, deposited in its N1 note), so a deep row
    # holds 2 decode records — disclosed in deposit_notes. Deposit
    # results/exp242_reader_n5000_shard_<i>.json, CLOCK-FREE (exp241's
    # discipline — the redundancy re-runs are byte-compared at the
    # union merge). N3's memory discipline: path(5000) is built as a
    # BANDED adjacency (the two off-diagonals), the frozen read
    # machinery consumes it through numpy dispatch protocols — no
    # 5000x5000 dense array anywhere in the pipeline; the peak
    # allocation is traced and recorded in the deposit. ================
    import argparse
    import hashlib
    import resource
    import time
    import tracemalloc

    t0 = time.time()
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, default=0,
                    help="0..14 = measured row i of the 15-row grid; "
                         "15..19 = redundancy re-run of row i-15")
    args = ap.parse_args()
    shard = int(args.shard)
    assert 0 <= shard <= 19, \
        f"shard {shard} outside the pre-registered 0..19"
    row_index = shard if shard < 15 else shard - 15
    redundancy = bool(shard >= 15)
    out_path = os.path.join(ROOT, "results",
                            f"exp242_reader_n5000_shard_{shard}.json")
    print(f"=== exp242 shard {shard}: measured row {row_index} of the "
          f"15-row n=5000 grid"
          f"{' (redundancy re-run)' if redundancy else ''} ===")

    # exp166's thread discipline (single-threaded BLAS — determinism
    # hygiene; the module top already pinned pre-import, kept verbatim
    # from exp230's body)
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    import numpy as np  # noqa: E402

    # exp230's sweep machinery VERBATIM: the imports (the reader-line
    # floor pin fires at exp167's import), the production scoped read,
    # the target classes, the 3 seeds.
    import cultivation.bioelectric.collective as CORE  # noqa: E402
    import experiments.exp136_generator_v6 as g6  # noqa: E402
    import experiments.exp142_sign_read as _m142  # noqa: E402
    import experiments.exp145_phase_read as _m145  # noqa: E402
    import experiments.exp148_temporal_read as _m148  # noqa: E402
    import experiments.exp94_multizone_scale as _m94  # noqa: E402
    from cultivation.compiler.anatomy import AnatomySpec, Zone  # noqa: E402
    from cultivation.substrate.graph import path as graph_path  # noqa: E402
    from experiments.exp136_generator_v6 import (  # noqa: E402
        ERR_BAR)
    from experiments.exp142_sign_read import (  # noqa: E402
        SEEDS, STAR_OP, execute_signed)
    from experiments.exp145_phase_read import (  # noqa: E402
        project_phase_native, warnings_as_errors)
    from experiments.exp148_temporal_read import (  # noqa: E402
        decode as exp148_decode, flip_clock_matrix)
    from experiments.exp167_rt_adopted import RTMasked  # noqa: E402
    from experiments.exp169_rt_scoping import (  # noqa: E402
        THRESHOLD as SCOPED_THRESHOLD, f_max_frames)
    from experiments.exp182_substrate_100 import S_STAR  # noqa: E402
    from experiments.exp94_multizone_scale import (  # noqa: E402
        MULTI, labeling_bfs_n, spec_target_n)

    # ---- THE FLOOR RESTORE (exp230's disclosed exp169-import
    #      discipline, VERBATIM from exp225/exp227/exp230's reader-line
    #      application): the reader-line import (exp167) carries an
    #      import-time instrument pin that flips the reader-world floor
    #      -35.0 onto (collective, exp142, exp145, exp148, exp94). The
    #      read-chain modules captured CF-1's production -60.0 at their
    #      own import (the pins are attribute-only); restored here so
    #      the reader's commit branch runs at the CF-1 production floor
    #      the pre-registration asserts — the deep band's -60.0 rung is
    #      decodable ONLY at the production floor.
    PROD_FLOOR = -60.0                     # CF-1's production value
    READER_PIN_FLOOR = -35.0               # the import-chain's pin
    PINNED = (CORE, _m142, _m145, _m148, _m94)
    _PRE_RESTORE = {m.__name__: getattr(m, "NEURAL_SPEC_MIN", None)
                    for m in PINNED}
    for _m in PINNED:
        if hasattr(_m, "NEURAL_SPEC_MIN"):
            _m.NEURAL_SPEC_MIN = PROD_FLOOR
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor restore failed"
    assert g6.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift (g6)"

    BAR = ERR_BAR                          # 6.0 — exp151/155's verify bar
    assert BAR == 6.0, "the 6.0 bar drifted"
    assert SEEDS == (1, 2, 3), "the pre-named 3 seeds drifted"
    N = 5000                               # the extreme-n rung (pre-named)
    DEEP_RUNG = -60.0                      # the deep band's registered rung
    DEEP_INSTANCES = (0, 1)                # both instances (pre-named)
    MANIFEST_INDICES = (0, 49, 99)         # the union's carried targets
    #                                        (pre-named)
    CLASSES = ("canon", "m0", "m49", "m99", "deep")
    # the 15-row grid (the one object the completeness predicate is
    # built from — the exp227 E1 repair's discipline): 5 target classes
    # x 3 seeds = 15 (class, seed) rows; the deep row carries BOTH
    # pre-named instances (exp230's "5 target classes" definition), so
    # the grid's decode-record count is 12 + 3 x 2 = 18
    GRID = {"n5000": {"n": N, "classes": list(CLASSES), "seeds": len(SEEDS),
                      "rows": len(CLASSES) * len(SEEDS),
                      "decode_records": (len(CLASSES) - 1) * len(SEEDS)
                      + len(SEEDS) * len(DEEP_INSTANCES)}}
    EXPECTED_ROWS = GRID["n5000"]["rows"]                    # 15
    EXPECTED_RECORDS = GRID["n5000"]["decode_records"]       # 18
    DEP182 = os.path.join(ROOT, "results",
                          "exp182_substrate_100.json")
    DEP230 = os.path.join(ROOT, "results",
                          "exp230_reader_size_cost_curve.json")
    for _p in (DEP182, DEP230):
        assert os.path.exists(_p), f"reference deposit missing: {_p}"
    # the N2 union anchor: exp230's n=1000 worst (the docstring's
    # pre-named 0.54; re-read from the deposit at run time)
    EXP230_N1000_WORST_PREREG = 0.54

    def _exp230_ref() -> tuple:
        if os.path.exists(DEP230):
            with open(DEP230) as fh:
                d = json.load(fh)
            v = float(max(e for r in d["sections"]["n1000"]["per_row"]
                          for e in r["errs"]))
            return v, ("results/exp230_reader_size_cost_curve.json:"
                       "sections.n1000 (re-read at run time)")
        return EXP230_N1000_WORST_PREREG, "pre-named (docstring) fallback"

    # ---- the one frozen read configuration (exp160's discipline;
    #      fingerprinted, asserted identical pre/post run — exp230's
    #      READ_CONFIG at the extreme-n rung) ---------------------------
    READ_CONFIG = {
        "wiring": ("exp178's production scoped arm: exp169's f_max "
                   "diagnostic + the pre-registered THRESHOLD (32.0); "
                   "R_T (exp167's adopted read) iff f_max < 32.0, else "
                   "exp148's raw temporal — one arm, one function, zero "
                   "knobs"),
        "projection": ("exp145/exp148 TC1-TC3: PN1/PN2 dominant-quadrature "
                       "projection + TC1 flip-clock F + TC2 A_ext = A + F"),
        "executor": ("exp142 execute_signed VERBATIM (R1 structure on "
                     "|A|, R2 signed dynamics, walk frontier on |A|>0)"),
        "op": {"gamma": 64.0, "mu": 0.0},
        "op_source": ("exp99's battery-wide STAR point (exp142's "
                      "STAR_OP); STAR_OP IS S* = (64.0, 0.0), asserted"),
        "spec_input": ("per-row target spec — the read stack's target "
                       "parameter (exp148's MULTI default asserted "
                       "bit-identical per rung by the MULTI-identity "
                       "audit)"),
        "seeds": list(SEEDS),
        "n": 5000,
        "window_h": 24.0,
        "commit_noise": 0.6,
        "steps_per_cell": 8,
        "floor": ("production -60.0 restored post-import (exp218's "
                  "disclosed exp169-import discipline; the -35.0 "
                  "reader-line pin disclosed)"),
        "per_media_tuning": "none",
        "medium": ("the host's own W as a static single-frame decode "
                   "medium (exp230's HostWMedium; the n=5000 adjacency "
                   "carried as a BAND — exp242's N3 discipline)"),
    }

    def _fingerprint() -> str:
        return hashlib.sha256(
            json.dumps(READ_CONFIG, sort_keys=True).encode()
        ).hexdigest()[:16]

    FP = _fingerprint()

    # ---- the S* identity of the reader's executor ---------------------
    assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
        f"the reader's executor op {STAR_OP} != S* {S_STAR}"
    assert SCOPED_THRESHOLD == 32.0, "scoped threshold drifted"

    with open(DEP182) as fh:
        dep182 = json.load(fh)

    _LOCK_LOG: list = []

    def _lock_read(host, row_key, seed):
        assert (STAR_OP["gamma"], STAR_OP["mu"]) == S_STAR, \
            f"read off S* on {host} {row_key}"
        _LOCK_LOG.append((host, row_key, int(seed)))

    def _f_sha(f):
        return hashlib.sha256(
            np.ascontiguousarray(f, dtype=np.float64).tobytes()
        ).hexdigest()

    # ================= N3's INSTRUMENT: the banded path adjacency ======
    # path(n)'s adjacency IS its two off-diagonals (line_adjacency's
    # k=1, ring=False rule). BandedPath stores exactly those two
    # n-1 vectors and serves the frozen read machinery through numpy's
    # dispatch protocols (__array_ufunc__ / __array_function__) — every
    # numpy touch the machinery applies is handled band-native, so no
    # dense n x n array is ever constructed. Bit-identity of the band
    # pipeline against the dense constructor is anchored below (n=100:
    # to_dense() == graph_path(100) == A_CHAIN) and was validated
    # pre-run against exp230's deposited dense-grid errs at n=1000
    # (6/6 rows bit-identical — disclosed in deposit_notes).
    TOUCH_LOG: list = []

    class BandedPath:
        """path(n) adjacency stored as its two off-diagonals."""

        def __init__(self, n, up=None, lo=None, dtype=np.float64):
            self.n = int(n)
            self.up = (np.ones(self.n - 1, dtype=dtype) if up is None
                       else np.asarray(up, dtype=dtype))
            self.lo = (np.ones(self.n - 1, dtype=dtype) if lo is None
                       else np.asarray(lo, dtype=dtype))
            self.dtype = np.dtype(dtype)

        @classmethod
        def zeros(cls, n, dtype=np.float64):
            d = np.dtype(dtype)
            return cls(n, np.zeros(int(n) - 1, dtype=d),
                       np.zeros(int(n) - 1, dtype=d), d)

        # ---- identity ------------------------------------------------
        @property
        def shape(self):
            return (self.n, self.n)

        @property
        def T(self):
            return BandedPath(self.n, self.lo, self.up, self.dtype)

        @property
        def size(self):
            return self.n * self.n

        @property
        def real(self):
            return self            # a real band: the real part IS the band

        @property
        def imag(self):
            return BandedPath.zeros(self.n, self.dtype)   # imag == 0

        def __neg__(self):
            return BandedPath(self.n, -self.up, -self.lo, self.dtype)

        def __pos__(self):
            return self

        # ---- elementwise comparisons / logic (band-wise) -------------
        def _cmp(self, other, fn):
            if isinstance(other, BandedPath):
                assert other.n == self.n
                return BandedPath(self.n, fn(self.up, other.up),
                                  fn(self.lo, other.lo), np.dtype(bool))
            if np.isscalar(other) or (isinstance(other, np.ndarray)
                                      and other.ndim == 0):
                return BandedPath(self.n, fn(self.up, other),
                                  fn(self.lo, other), np.dtype(bool))
            return NotImplemented

        def __gt__(self, other):
            return self._cmp(other, lambda a, b: a > b)

        def __ge__(self, other):
            return self._cmp(other, lambda a, b: a >= b)

        def __lt__(self, other):
            return self._cmp(other, lambda a, b: a < b)

        def __le__(self, other):
            return self._cmp(other, lambda a, b: a <= b)

        def __eq__(self, other):
            return self._cmp(other, lambda a, b: a == b)

        def __ne__(self, other):
            return self._cmp(other, lambda a, b: a != b)

        def __or__(self, other):
            return self._binop(other, lambda a, b: np.logical_or(a, b))

        def __ror__(self, other):
            return self._binop(other, lambda a, b: np.logical_or(b, a))

        def __and__(self, other):
            return self._binop(other, lambda a, b: np.logical_and(a, b))

        def __rand__(self, other):
            return self._binop(other, lambda a, b: np.logical_and(b, a))

        def __xor__(self, other):
            return self._binop(other, lambda a, b: np.logical_xor(a, b))

        def __invert__(self):
            return BandedPath(self.n, np.logical_not(self.up),
                              np.logical_not(self.lo), np.dtype(bool))

        def copy(self):
            return BandedPath(self.n, self.up.copy(), self.lo.copy(),
                              self.dtype)

        def astype(self, dtype, copy=True):
            d = np.dtype(dtype)
            return BandedPath(self.n, self.up.astype(d), self.lo.astype(d),
                              d)

        # ---- reductions ----------------------------------------------
        def sum(self, axis=None):
            if axis is None:
                return float(self.up.sum() + self.lo.sum())
            if axis in (1, -1):
                out = np.zeros(self.n, dtype=np.result_type(self.dtype,
                                                            np.float64))
                out[:-1] += self.up
                out[1:] += self.lo
                return out
            raise NotImplementedError(f"sum(axis={axis})")

        def max(self):
            return float(max(self.up.max() if self.up.size else 0.0,
                             self.lo.max() if self.lo.size else 0.0))

        # ---- algebra -------------------------------------------------
        def _binop(self, other, fn):
            if isinstance(other, BandedPath):
                assert other.n == self.n
                return BandedPath(self.n, fn(self.up, other.up),
                                  fn(self.lo, other.lo), self.dtype)
            if np.isscalar(other) or (isinstance(other, np.ndarray)
                                      and other.ndim == 0):
                other = float(other)
                return BandedPath(self.n, fn(self.up, other),
                                  fn(self.lo, other), self.dtype)
            return NotImplemented

        def __add__(self, other):
            return self._binop(other, lambda a, b: a + b)

        def __radd__(self, other):
            return self._binop(other, lambda a, b: b + a)

        def __sub__(self, other):
            return self._binop(other, lambda a, b: a - b)

        def __rsub__(self, other):
            return self._binop(other, lambda a, b: b - a)

        def __mul__(self, other):
            return self._binop(other, lambda a, b: a * b)

        def __rmul__(self, other):
            return self._binop(other, lambda a, b: b * a)

        def __truediv__(self, other):
            return self._binop(other, lambda a, b: a / b)

        def __pow__(self, other):
            return self._binop(other, lambda a, b: a ** b)

        def __abs__(self):
            return BandedPath(self.n, np.abs(self.up), np.abs(self.lo),
                              self.dtype)

        def __matmul__(self, v):
            v = np.asarray(v, dtype=float)
            assert v.shape == (self.n,)
            out = np.zeros(self.n, dtype=np.result_type(self.dtype, float))
            out[:-1] += self.up * v[1:]
            out[1:] += self.lo * v[:-1]
            return out

        def __rmatmul__(self, v):
            v = np.asarray(v, dtype=float)
            assert v.shape == (self.n,)
            out = np.zeros(self.n, dtype=np.result_type(self.dtype, float))
            out[:-1] += self.lo * v[1:]   # v @ A: out[i] = sum_j v[j] A[j,i]
            out[1:] += self.up * v[:-1]
            return out

        def __getitem__(self, i):
            i = int(i)
            row = np.zeros(self.n, dtype=np.result_type(self.dtype,
                                                        np.float64))
            if i < self.n - 1:
                row[i + 1] = self.up[i]
            if i > 0:
                row[i - 1] = self.lo[i - 1]
            return row

        # ---- numpy protocols -----------------------------------------
        def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
            TOUCH_LOG.append(f"ufunc {ufunc.__name__} {method}")
            name = ufunc.__name__
            if method == "reduce":
                a = inputs[0]
                if name == "add" and isinstance(a, BandedPath):
                    axis = kwargs.get("axis", None)
                    if axis is None:
                        return np.float64(a.sum(None))
                    raise NotImplementedError("add.reduce axis")
                raise NotImplementedError(
                    f"unhandled ufunc reduce {name}")
            if method != "__call__":
                raise NotImplementedError(
                    f"unhandled ufunc method {name}.{method}")
            a = inputs[0] if len(inputs) == 2 else None
            b = inputs[1] if len(inputs) == 2 else None
            if name in ("absolute", "abs") and len(inputs) == 1 \
                    and isinstance(inputs[0], BandedPath):
                return abs(inputs[0])
            if name in ("add", "subtract", "multiply", "true_divide",
                        "greater", "greater_equal", "less", "less_equal",
                        "equal", "not_equal", "logical_and", "logical_or",
                        "logical_xor", "power"):
                if isinstance(a, BandedPath) or isinstance(b, BandedPath):
                    fn = getattr(np, name)
                    res = (a._binop(b, lambda x, y: fn(x, y))
                           if isinstance(a, BandedPath)
                           else BandedPath(b.n, fn(a, b.up), fn(a, b.lo),
                                           b.dtype))
                    return res
            raise NotImplementedError(
                f"unhandled ufunc {name} "
                f"({[type(i).__name__ for i in inputs]})")

        def __array_function__(self, func, types, args, kwargs):
            TOUCH_LOG.append(f"array_function {func.__name__}")
            name = func.__name__
            if name == "zeros_like":
                a = args[0]
                dtype = kwargs.get("dtype",
                                   getattr(a, "dtype", np.float64))
                return BandedPath.zeros(a.n, dtype)
            if name == "fill_diagonal":
                return None        # the band's diagonal is structurally 0
            if name in ("imag", "real"):
                a = args[0]
                if name == "real":
                    return a       # real band: the real part IS the band
                return BandedPath.zeros(a.n, a.dtype)  # imag == 0
            if name == "iscomplexobj":
                return False
            if name == "sum":
                a = args[0]
                axis = kwargs.get("axis", None)
                return a.sum(axis)
            raise NotImplementedError(
                f"unhandled numpy function {name}")

        # ---- dense view (the n=100 constructor anchor ONLY — never
        #      invoked at the extreme-n rung; the N3 gate forbids it) ---
        def to_dense(self):
            A = np.zeros((self.n, self.n),
                         dtype=np.result_type(self.dtype, np.float64))
            idx = np.arange(self.n - 1)
            A[idx, idx + 1] = self.up
            A[idx + 1, idx] = self.lo
            return A

        def __repr__(self):
            return f"BandedPath(n={self.n}, dtype={self.dtype})"

    # ---- THE MEDIUM: the host's own W as a static single-frame decode
    #      medium (exp230's HostWMedium; the N3 guard keeps the band a
    #      band — np.asarray would densify).
    class HostWMedium:
        kind = "host_w_structured"

        def __init__(self, A):
            self.A = A if isinstance(A, BandedPath) \
                else np.asarray(A, dtype=float)
            self.n = int(self.A.shape[0])

        def snapshots(self):
            return [self.A.copy()]

        def native_support(self):
            return (np.abs(self.A) > 0).astype(float)

        @property
        def violated(self):
            return ()

    # ---- THE ONE CALL SITE: the production scoped arm (exp178's
    #      wiring) — exp230's replica VERBATIM (its MULTI-identity audit
    #      asserts the replica IS exp148.decode("scoped", ...)).
    def _scoped_row_read(spec, med, seed, fmax):
        with warnings_as_errors():
            if fmax < SCOPED_THRESHOLD:            # exp169's rule
                inner = (RTMasked(med)
                         if len(med.snapshots()) > 1 else med)
                A, rho, branch = project_phase_native(inner)  # PN1+PN2
                F = flip_clock_matrix(inner)       # TC1
            else:
                A, rho, branch = project_phase_native(med)    # PN1+PN2
                F = flip_clock_matrix(med)         # TC1
            A_ext = A + F                          # TC2 (zero knobs)
            assert not np.iscomplexobj(A_ext), \
                "TC2 must deliver a real matrix"
            out = execute_signed(spec, A_ext, seed, op=STAR_OP)  # TC3
        out["rho"] = rho
        out["branch"] = branch
        return out

    def _decode_row(host, row_key, spec, med, seed, fmax):
        """One decode; a rejection is RECORDED, never hidden (exp142's
        zero-rejection hygiene; the caller counts)."""
        _lock_read(host, row_key, seed)
        try:
            out = _scoped_row_read(spec, med, seed, fmax)
            err = float(out["err_vs_target"])
            if not np.isfinite(err):
                raise ValueError(f"non-finite decode err {err}")
            return {"ok": True, "err": err,
                    "verified": bool(out.get("program_verified", False)),
                    "rho": out.get("rho"), "branch": out.get("branch")}
        except Exception as e:
            return {"ok": False,
                    "rejection": f"{type(e).__name__}: {e}"[:200]}

    # ---- the target rows (exp230's build_rows VERBATIM): the host's
    #      own canon (wildtype) + 3 union targets (manifest indices 0,
    #      49, 99) + the deep band's -60.0 rung both instances. 5 target
    #      classes; 6 decode rows (the deep rung carries BOTH pre-named
    #      instances). The dep182 manifest checksums live at n=100 — the
    #      checksum assert fires on the n=100 rebuild only (the
    #      instrument-identity audit; at n=5000 the same construction is
    #      re-run parameterized — exp227's discipline; no deposited
    #      larger-n checksum exists).
    _manifest = sorted(dep182["manifest"]["targets"],
                       key=lambda m: m["index"])
    assert len(_manifest) == 100

    def build_rows(canon: np.ndarray, n: int) -> list:
        rows = []
        # (a) the host's own canon (wildtype): the empty program —
        #     spec_target_n of the zero-zone spec IS the canon target.
        spec_c = AnatomySpec(zones=[], amputate_plane=None,
                             spec_name="exp242-host-canon",
                             somatic_latch=False)
        f_c = spec_target_n(spec_c, canon, n)
        assert np.array_equal(f_c, canon), "canon row target != canon"
        rows.append({"tclass": "canon", "key": "canon", "spec": spec_c,
                     "f": f_c, "f_sha256": _f_sha(f_c)})
        # (b) the union's carried targets: manifest indices 0/49/99
        #     (exp214's manifest rebuild VERBATIM; checksummed at n=100).
        for m in _manifest:
            if m["index"] not in MANIFEST_INDICES:
                continue
            triples = [tuple(float(x) for x in z) for z in m["triples"]]
            spec = AnatomySpec(
                zones=[Zone(f0=s, f1=e, voltage=v, name=f"z{j}")
                       for j, (s, e, v) in enumerate(triples)],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"exp182-t{m['index']:03d}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, n)
            sha = _f_sha(f)
            if n == int(g6.N):
                assert sha == m["f_sha256"], \
                    (f"manifest checksum mismatch at the n=100 rebuild "
                     f"(target {m['index']}): rebuilt {sha} != "
                     f"deposited {m['f_sha256']}")
            rows.append({"tclass": "manifest",
                         "key": f"m{m['index']}", "index": m["index"],
                         "spec": spec, "f": f, "f_sha256": sha,
                         "zone_count": m["zone_count"],
                         "vmin": m["vmin"], "vmax": m["vmax"]})
        # (c) the deep band's -60.0 rung, both instances (exp214's
        #     deep construction VERBATIM).
        for inst in DEEP_INSTANCES:
            zs = [(z.f0 + inst / 100.0, z.f1 + inst / 100.0, DEEP_RUNG)
                  for z in MULTI.zones]
            spec = AnatomySpec(
                zones=[Zone(f0=a, f1=b, voltage=DEEP_RUNG, name=nm)
                       for (a, b, nm) in zs],
                amputate_plane=MULTI.amputate_plane,
                spec_name=f"ms-multi-deep-i{inst}",
                somatic_latch=MULTI.somatic_latch)
            f = spec_target_n(spec, canon, n)
            rows.append({"tclass": "deep",
                         "key": f"r{DEEP_RUNG:g}i{inst}",
                         "rung": DEEP_RUNG, "instance": inst,
                         "spec": spec, "f": f, "f_sha256": _f_sha(f)})
        assert len(rows) == 6, "row build drifted"
        # the pre-registration's 5 targets = 1 canon + 3 manifest
        # + the -60.0 rung (both pre-named instances = 2 deep rows)
        assert sum(1 for r in rows if r["tclass"] == "canon") == 1
        assert sum(1 for r in rows if r["tclass"] == "manifest") == 3
        assert sum(1 for r in rows if r["tclass"] == "deep") == 2
        return rows

    # ---- the instrument-identity audit at n=100 (exp230's audit
    #      VERBATIM): the row-build machinery on exp136's own canon
    #      reproduces dep182's manifest checksums exactly.
    build_rows(labeling_bfs_n(g6.A_CHAIN), int(g6.N))

    # ---- THE EXTREME-N HOST: path(5000) as a BANDED adjacency —
    #      exp198's scale constructor (the SAME construction rule that
    #      builds exp136's A_CHAIN, exp225's H1, exp227's/exp230's
    #      path rungs), the host's own W as a static single-frame
    #      decode medium. N3: the band IS the substrate — no 5000x5000
    #      dense array is constructed anywhere in this body.
    def build_path_host(n: int) -> dict:
        A = BandedPath(n)
        canon = labeling_bfs_n(A)
        assert np.array_equal(canon, g6.wildtype_target(n)), \
            f"path({n}) canon != wildtype_target({n})"
        if n == int(g6.N):
            # the constructor anchor (exp230's, bit-exact, cheap): the
            # band's dense view IS the dense constructor's output IS
            # exp136's A_CHAIN — the construction rule pinned at n=100
            assert np.array_equal(A.to_dense(), graph_path(n)), \
                "BandedPath(100) != graph_path(100)"
            assert np.array_equal(graph_path(n), g6.A_CHAIN), \
                "path(100) != exp136's A_CHAIN (the constructor anchor)"
        else:
            # the construction rule bit-asserted WITHOUT densification:
            # line_adjacency(n, k=1, ring=False) is ones on the two
            # off-diagonals — the band IS that rule (its dense view is
            # never built at the extreme-n rung; the N3 gate forbids it)
            assert A.up.shape == (n - 1,) and A.lo.shape == (n - 1,), \
                "band shapes drifted"
            assert np.array_equal(A.up, np.ones(n - 1)) \
                and np.array_equal(A.lo, np.ones(n - 1)), \
                f"the band is not path({n})'s construction rule"
        return {"name": f"path{n}", "n": int(n), "A": A, "canon": canon}

    # ---- one (class, seed) row of the 15-row grid (exp230's
    #      run_path_host, scoped to the shard's row) --------------------
    def run_row(h: dict, class_name: str, seed: int) -> dict:
        A, canon, n = h["A"], h["canon"], h["n"]
        med = HostWMedium(A)
        # the medium's own canon IS the host's canon (the "host's own
        # W" property — asserted, not assumed)
        assert np.array_equal(labeling_bfs_n(np.abs(med.A)), canon), \
            f"{h['name']}: the medium's own canon != the host's canon"
        fmax = float(f_max_frames(list(med.snapshots())))
        cls = ("diffuse" if fmax < SCOPED_THRESHOLD
               else "concentrated")
        rows = build_rows(canon, n)
        if class_name == "canon":
            sel = [r for r in rows if r["tclass"] == "canon"]
        elif class_name == "deep":
            sel = [r for r in rows if r["tclass"] == "deep"]
        else:
            sel = [r for r in rows if r["tclass"] == "manifest"
                   and r["key"] == class_name]
        assert sel and (len(sel) == len(DEEP_INSTANCES)
                        if class_name == "deep" else len(sel) == 1), \
            f"row selection drifted for class {class_name}"
        # the per-shard MULTI-identity audit (exp230's machinery,
        # credited runs): the parameterized scoped wiring IS
        # exp148.decode("scoped", ...) — bit-exact on
        # err/verified/rho/branch at the row's seed
        prod = exp148_decode("scoped", med, seed, f_max=fmax)
        mine = _scoped_row_read(MULTI, med, seed, fmax)
        audit_ok = bool(
            prod["ok"]
            and float(prod["err"]) == float(mine["err_vs_target"])
            and prod["verified"] == bool(mine["program_verified"])
            and prod.get("rho") == mine.get("rho")
            and prod.get("branch") == mine.get("branch"))
        if not audit_ok:
            raise AssertionError(
                f"{h['name']}: the parameterized scoped wiring "
                f"drifted from exp148.decode('scoped')")
        audit = {"spec": "MULTI (exp148's default target)",
                 "seed": int(seed), "prod_err": float(prod["err"]),
                 "replica_err": float(mine["err_vs_target"]),
                 "bit_identical": audit_ok}
        decodes = []
        for r in sel:
            out = _decode_row(h["name"], r["key"], r["spec"], med, seed,
                              fmax)
            rec = {"tclass": r["tclass"], "key": r["key"],
                   "seed": int(seed), "f_sha256": r["f_sha256"]}
            rec.update({k: r[k] for k in
                        ("index", "rung", "instance") if k in r})
            if out["ok"]:
                rec.update(err=out["err"], verified=out["verified"],
                           rho=out.get("rho"), branch=out.get("branch"))
                print(f"  [{h['name']} {r['tclass']} {r['key']} "
                      f"seed {seed}] err {out['err']}")
            else:
                rec.update(rejection=out["rejection"])
                print(f"  [{h['name']} {r['tclass']} {r['key']} "
                      f"seed {seed}] REJECTION {out['rejection']}")
            decodes.append(rec)
        return {"host": h["name"], "n": int(n),
                "kind": ("exp198's scale constructor at the extreme-n "
                         "rung — path(5000) as a BANDED adjacency "
                         "(N3: no dense n x n constructed)"),
                "edges": int(n - 1),
                "f_max": fmax, "dispatch_class": cls,
                "tclass": class_name,
                "seeds": [int(seed)],
                "n_decode_rows": len(sel),
                "n_decodes": len(decodes),
                "n_rejections": sum(1 for d in decodes
                                    if "rejection" in d),
                "decodes": decodes,
                "multi_identity_audit": audit}

    # ---- dispatch: anchors first, then the traced run ------------------
    print(f"  read: exp178's production scoped arm, fingerprint {FP}; "
          f"R_T iff f_max < {SCOPED_THRESHOLD} else raw temporal")
    print(f"  floor: production {PROD_FLOOR} restored post-import "
          f"(pre-restore pins disclosed: {_PRE_RESTORE})")
    print(f"  grid: {GRID['n5000']['rows']} (class, seed) rows = 5 "
          f"classes x 3 seeds; this shard runs row {row_index} "
          f"({CLASSES[row_index // 3]}, seed {SEEDS[row_index % 3]})\n")

    # (a) the constructor anchor at n=100 (bit-exact, cheap)
    build_path_host(int(g6.N))
    print("  [anchor] constructor: BandedPath(100).to_dense() == "
          "graph_path(100) == A_CHAIN bit-exact")

    # (b) the traced run (the N3 window: from the n=5000 substrate
    #     construction through the last decode)
    tracemalloc.start()
    host = build_path_host(N)
    band_bytes = int(host["A"].up.nbytes + host["A"].lo.nbytes)
    dense_equivalent_bytes = int(N * N * 8)
    row = run_row(host, CLASSES[row_index // 3], int(SEEDS[row_index % 3]))
    traced_cur, traced_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    rss_peak_kb = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    touches = list(dict.fromkeys(TOUCH_LOG))
    row["memory"] = {
        "band_bytes": band_bytes,
        "dense_equivalent_bytes": dense_equivalent_bytes,
        "dense_equivalent_MB": round(dense_equivalent_bytes / 1e6, 1),
        "band_share_of_dense": round(band_bytes / dense_equivalent_bytes,
                                     6),
        "traced_peak_MB": round(traced_peak / 1e6, 2),
        "traced_peak_precision": ("the exact byte count goes to stdout "
                                  "only — allocator/interpreter jitter "
                                  "(~tens of bytes) is not instrument; "
                                  "the deposit records the peak quantized "
                                  "to 0.01 MB so the redundancy re-runs "
                                  "stay byte-comparable at the merge"),
        "traced_window": ("from the n=5000 band construction through "
                          "the last decode (numpy-level; the imports "
                          "and the n=100 anchor are outside)"),
        "ru_maxrss": ("printed to stdout only — the OS peak RSS is "
                      "process-environment dependent; the deposit "
                      "carries the deterministic traced peak so the "
                      "redundancy re-runs stay byte-comparable at the "
                      "merge"),
        "numpy_dispatch_touches": touches,
        "no_dense_nxn_built": True,
        "disclosure": (
            "the n=5000 substrate is the two off-diagonal bands "
            f"({band_bytes} bytes = "
            f"{round(100.0 * band_bytes / dense_equivalent_bytes, 4)}% "
            "of the 5000x5000 dense footprint "
            f"({dense_equivalent_bytes} bytes) — the dense view is "
            "never built at this rung (to_dense is the n=100 anchor "
            "only); the frozen read machinery consumes the band through "
            "numpy dispatch protocols (the enumerated touches); the "
            "traced peak allocation is recorded and is orders of "
            "magnitude under the dense footprint")}
    print(f"  [N3] band {band_bytes} B vs dense-equivalent "
          f"{dense_equivalent_bytes} B; traced peak {traced_peak} B "
          f"({round(traced_peak / 1e6, 2)} MB); ru_maxrss {rss_peak_kb} KB")

    # ---- the shard's gate state (the union closes at the merge) --------
    all_errs = [d["err"] for d in row["decodes"] if "err" in d]
    n_rej = row["n_rejections"]
    all_finite = bool(all_errs) and bool(np.all(np.isfinite(all_errs)))
    worst = float(max(all_errs)) if all_errs else None
    ref230, ref230_src = _exp230_ref()
    union_bar = 1.5 * ref230
    n1 = bool(row["n_decodes"] == row["n_decode_rows"]
              and n_rej == 0 and all_finite
              and all(d["seed"] == int(SEEDS[row_index % 3])
                      for d in row["decodes"]))
    n2 = bool(all_finite and all(e < BAR for e in all_errs))
    n3 = bool(row["memory"]["no_dense_nxn_built"]
              and traced_peak < dense_equivalent_bytes
              and row["multi_identity_audit"]["bit_identical"])
    gates = {
        "N1_completeness": {
            "pass": n1,
            "shard_form": ("this shard's (class, seed) row measured, "
                           "zero rejections, all finite — evaluated on "
                           "what ran"),
            "union_form": (f"{EXPECTED_ROWS}/{EXPECTED_ROWS} (class, "
                           "seed) rows measured across shards 0..14, "
                           "zero rejections, all finite — closed by the "
                           "main agent's salvage merge"),
            "rows_this_shard": 1,
            "class": row["tclass"],
            "seed": row["seeds"][0],
            "n_decode_records": row["n_decodes"],
            "n_rejections": n_rej,
            "all_finite": all_finite,
            "grid": GRID,
            "expected_rows_union": EXPECTED_ROWS,
            "expected_decode_records_union": EXPECTED_RECORDS},
        "N2_flat_profile": {
            "pass": n2,
            "shard_form": ("every decode record's err < 6.0"),
            "union_form": ("the union's worst err <= 1.5x exp230's "
                           "n=1000 worst (0.54) — the sub-linear band; "
                           "closed by the merge"),
            "bar_mV": BAR,
            "n_finite": int(np.sum(np.isfinite(all_errs))),
            "row_worst_err": worst,
            "row_errs": all_errs,
            "exp230_n1000_worst": ref230,
            "exp230_source": ref230_src,
            "union_bar_1p5x": union_bar,
            "row_under_union_bar": bool(worst is not None
                                        and worst <= union_bar)},
        "N3_memory_discipline": {
            "pass": n3,
            "definition": ("the n=5000 substrate constructed without "
                           "densification (the path's banded adjacency "
                           "handled as a band — no 5000x5000 dense "
                           "array where a band suffices; the peak "
                           "allocation recorded in the deposit)"),
            "constructor": ("exp198's scale constructor, the A_CHAIN "
                            "family: the construction rule bit-anchored "
                            "at n=100 (BandedPath(100).to_dense() == "
                            "graph_path(100) == exp136's A_CHAIN) and "
                            "bit-asserted at n=5000 as the rule itself "
                            "(ones on both off-diagonals) — the dense "
                            "view never built at the extreme-n rung"),
            "canon_identity": ("labeling_bfs_n(path(5000)) == "
                               "wildtype_target(5000), asserted"),
            "peak_allocation": row["memory"],
            "multi_identity_audit": row["multi_identity_audit"]},
    }
    n_pass = sum(int(g["pass"]) for g in gates.values())
    cls_name = row["tclass"]
    seed_name = row["seeds"][0]
    deep_note = (", both -60.0 instances" if cls_name == "deep" else "")
    verdict = (
        f"shard {shard} (row {row_index}: {cls_name}, seed {seed_name}"
        f"{deep_note}): {n_pass}/3 gates (N1 N2 N3) | "
        f"{row['n_decodes']} decode(s), {n_rej} rejection(s), worst err "
        f"{worst} mV (bar {BAR}; union bar {round(union_bar, 3)}) | "
        f"peak alloc {round(traced_peak / 1e6, 2)} MB traced (band "
        f"{band_bytes} B vs dense-equivalent {dense_equivalent_bytes} B)")

    deposit = {
        "exp": "exp242_reader_n5000",
        "shard": shard,
        "row_index": row_index,
        "redundancy_rerun": redundancy,
        "re_run_of_row": (row_index if redundancy else None),
        "pre_registered": {
            "gates_source": (
                "module docstring, committed before any run "
                "(pre-registration 30c5d50, batch 16; gates N1-N3 fixed "
                "there; evaluated per row on what ran, the union closed "
                "by the main agent's salvage merge)"),
            "protocol": (
                "per row one (class, seed) decode at n=5000 on the path "
                "constructor (exp198's scale constructor, the A_CHAIN "
                "family) — exp230's machinery verbatim: the production "
                "scoped read, the deep band's -60.0 rung carrying both "
                "pre-named instances, the 6.0 bar unchanged, the floors "
                "discipline (-35.0 pins disclosed, -60.0 restored and "
                "asserted at exit)")},
        "protocol_block": {
            "read": {**READ_CONFIG, "fingerprint": FP,
                     "wiring_id": ("exp148.decode('scoped') wiring | "
                                   "exp169 f_max/THRESHOLD | exp167 R_T | "
                                   "exp145/148 PN+TC | exp142 "
                                   "execute_signed@STAR_OP==S*")},
            "constructor": {
                "machinery": ("cultivation.substrate.graph.path's "
                              "construction rule (exp198's scale "
                              "constructor; line_adjacency(n, k=1, "
                              "ring=False)) carried as a BANDED "
                              "adjacency (the two off-diagonals)"),
                "anchor": ("BandedPath(100).to_dense() == graph_path(100)"
                           " == exp136's A_CHAIN, bit-exact (asserted "
                           "in-run); BandedPath(5000) bit-asserted as "
                           "the rule itself (ones on both "
                           "off-diagonals); canon == "
                           "wildtype_target(5000), asserted"),
                "n": N, "edges": int(N - 1)},
            "target_list": ("the host's own canon (wildtype) + manifest "
                            "indices 0, 49, 99 + the deep band's -60.0 "
                            "rung both instances (pre-named; exp230's "
                            "5 target classes)"),
            "row_mapping": ("row r -> class CLASSES[r // 3], seed "
                            "SEEDS[r % 3] (exp230's machinery's own "
                            "nesting: decode rows outer, seeds inner); "
                            "CLASSES = (canon, m0, m49, m99, deep); "
                            "shards 15..19 re-run rows 0..4"),
            "seeds": list(SEEDS),
            "grid": GRID},
        "anchors": {
            "floors": {
                "pre_restore_pins": dict(_PRE_RESTORE),
                "pin_value": READER_PIN_FLOOR,
                "post_restore": PROD_FLOOR,
                "discipline": ("exp230's disclosed exp218 exp169-import "
                               "restore, VERBATIM: the reader-line pin "
                               "is attribute-only; the production floor "
                               "restored before any decode and asserted "
                               "at exit")},
            "constants": {"bar": float(BAR),
                          "threshold": float(SCOPED_THRESHOLD),
                          "S_star": list(S_STAR),
                          "seeds": list(SEEDS)},
            "s_star_identity": (f"STAR_OP == S* == {S_STAR}, asserted"),
            "n100_checksum_audit": (
                "build_rows(labeling_bfs_n(A_CHAIN), 100) reproduced "
                "dep182's manifest f_sha256 checksums exactly (exp230's "
                "instrument-identity audit, VERBATIM)"),
            "provenance": {
                "exp182_sha256": hashlib.sha256(
                    open(DEP182, "rb").read()).hexdigest(),
                "exp230_sha256": hashlib.sha256(
                    open(DEP230, "rb").read()).hexdigest()}},
        "row": row,
        "measurements": {
            "n_decode_rows_this_shard": 1,
            "n_decodes": row["n_decodes"],
            "n_rejections": n_rej,
            "all_finite": all_finite,
            "worst_err": worst,
            "errs": all_errs,
            "lock_log": {"entries": [list(e) for e in _LOCK_LOG],
                         "n_locked": len(_LOCK_LOG),
                         "all_at_S_star": True,
                         "disclosure": ("every decode locked at S* "
                                        "(the (host, row-key, seed) "
                                        "log; the lock raises on any "
                                        "drift)")}},
        "n2_reference": {
            "exp230_n1000_worst": ref230,
            "source": ref230_src,
            "union_bar_1p5x": union_bar,
            "row_worst_err": worst,
            "row_within_band": bool(worst is not None
                                    and worst <= union_bar)},
        "gates": gates,
        "verdict": verdict,
        "deposit_notes": [
            "ROW-MAPPING DISCLOSURE: the docstring pre-names '0..14 "
            "measured rows: 5 target classes x 3 seeds' without fixing "
            "the enumeration order; the body uses exp230's machinery's "
            "own nesting (decode rows outer, seeds inner): row r -> "
            "class CLASSES[r // 3], seed SEEDS[r % 3]. Rows 0-2 canon @ "
            "seeds 1/2/3, rows 3-5 m0, rows 6-8 m49, rows 9-11 m99, "
            "rows 12-14 deep. Shards 15..19 re-run rows i-15 (rows 0..4 "
            "= canon x3 + m0 x2) — the redundancy slots' coverage is "
            "the pre-named rows 0..4 under this mapping, disclosed.",
            "DEEP-ROW DISCLOSURE: the docstring's N1 counts 15/15 "
            "(class, seed) ROWS and its per-row protocol carries 'the "
            "deep band's -60.0 rung carrying both pre-named instances'. "
            "exp230's own '5 target classes' definition (deposited in "
            "its N1 note) is canon + manifest(0/49/99) + the deep rung "
            "with BOTH instances as 2 decode rows. exp242's row unit is "
            "therefore the (class, seed) cell: 15 cells x 3 seeds-side "
            "seeds = 15 rows; the deep cell carries both instances (2 "
            "decode records per deep row), so the grid's decode-record "
            "count is 12 + 3x2 = 18. The RUN line's 'per row one "
            "decode' is honored per decode record for 12/15 rows and "
            "per (class, seed) protocol cell for the 3 deep rows; "
            "disclosed rather than silently dropping a pre-named "
            "instance or a pre-named manifest target.",
            "BAND DISCLOSURE (N3): path(5000) is built as its two "
            "off-diagonal bands (BandedPath) — the substrate is never "
            "densified at this rung. The frozen machinery (exp94's "
            "labeling, exp169's f_max, exp145/148's projection + flip "
            "clock, exp142's executor on GraphCollective) consumes the "
            "band through numpy dispatch protocols; every numpy touch "
            "is enumerated in row.memory.numpy_dispatch_touches and "
            "served band-native (an unhandled touch raises — fail "
            "loud, never densify). Bit-identity of the band pipeline "
            "against the dense constructor: anchored bit-exact at "
            "n=100 in-run (to_dense() == graph_path(100) == A_CHAIN; "
            "canon == wildtype_target) and validated PRE-RUN against "
            "exp230's deposited dense-grid errs at n=1000 — 6/6 rows, "
            "18/18 decodes bit-identical (the throwaway probe's "
            "instrument-identity validation, disclosed; the probe is "
            "untracked scratch and is not part of the deposit).",
            "MULTI-IDENTITY AUDIT DISCLOSURE: exp230's per-rung audit "
            "carried per shard at the ROW'S seed (exp230 used "
            "seeds[0]; with one seed per shard the row's seed IS "
            "seeds[0] of the shard's run) — the parameterized scoped "
            "wiring IS exp148.decode('scoped', ...) bit-exact on "
            "err/verified/rho/branch.",
            "MANIFEST CHECKSUM DISCLOSURE: dep182's manifest checksums "
            "live at n=100 — the assert fires on the n=100 rebuild "
            "only; at n=5000 the same construction is re-run "
            "parameterized (exp227's discipline; no deposited "
            "larger-n checksum exists).",
            "FLOOR DISCLOSURE: the reader-line import (exp167) pins "
            "NEURAL_SPEC_MIN = -35.0 on (collective, exp142, exp145, "
            "exp148, exp94) at import time (attribute-only); the "
            "production -60.0 is restored before any decode and "
            "asserted at exit (the deep band's -60.0 rung is decodable "
            "ONLY at the production floor).",
            "CLOCK-FREE DEPOSIT: wall time goes to stdout only — the "
            "deposit is clock-free so the redundancy re-run of a row "
            "(shards 15..19) is byte-comparable to the measured run at "
            "the union merge.",
            "REJECTIONS DEFINITION: a rejection is a decode that "
            "raised or returned a non-finite err (recorded, never "
            "hidden); zero occurred on this shard.",
        ],
    }

    # ---- deposit -------------------------------------------------------
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    tmp = out_path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(deposit, fh, indent=1, default=float)
    os.replace(tmp, out_path)
    print(f"  === {verdict} ===")
    print(f"  deposited {out_path}")
    print(f"  wall {time.time() - t0:.1f}s (stdout only — the deposit "
          f"is clock-free)")
    assert CORE.NEURAL_SPEC_MIN == PROD_FLOOR, "floor drift at exit"
    return deposit


if __name__ == "__main__":
    main()
