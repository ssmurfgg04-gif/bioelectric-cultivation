#!/usr/bin/env python3
"""exp237 — THE NCA CLONE BOUND (Hansali 2025, IEEE TMBMC — the direct
computational parallel; the Section 6 item; ledger L213).

THE OPEN QUESTION: Neural Cellular Automata (per-cell local updates with
a perception vector and a residual rule) regenerate target patterns from
local information alone — Hansali 2025's NCA is the literature's
computational parallel of the stack. The test: is the stack's
regeneration competence reproducible by a purely LOCAL rule (the NCA
claim), or does the stack's memory layer (theta — the homeostatic
target, D3's distributed property) carry information a local rule
cannot capture?

THE INSTRUMENT (zero-knob, a behavioral clone, no training loop beyond
least squares): on the torus arm (the NCA-native topology), record the
stack's own transitions (V, theta) over the regeneration window after
the standard amputation (exp73's protocol) — the dataset D = {(x_t, x_
t+1)} of per-cell states with the canonical neighborhood. The CLONE: a
linear local rule x'_t+1 = W @ phi(x_t) with the perception vector
phi = the NCA standard: (self, neighbor-mean, neighbor-std) per layer
(V and theta), fitted by ridge least squares on D. TWO clones: the
CLONE-WITH-MEMORY (phi includes theta; 9 features) and the CLONE-WITHOUT
(phi includes V only; 5 features — the pure-NCA perception). The bound
test: each clone runs ITS OWN closed-loop regeneration from the wound
state; the stack's regen is the reference.

PRE-REGISTERED GATES:

  H1  THE ONE-STEP FIDELITY: the clone-with-memory's one-step prediction
      R^2 >= 0.95 on held-out transitions (the stack's local update IS
      locally predictable); the clone-without's R^2 reported beside it
      (pre-named expectation: strictly lower — V alone does not predict
      the update because dV depends on theta).
  H2  THE CLOSED-LOOP REGEN BOUND: the clone-with-memory completes the
      regeneration (final err < 6.0, exp79's bar) on the torus at 3
      seeds; the clone-without FAILS (err >= 2x the bar) — the memory
      layer's information is NECESSARY for the regen competence: the
      stack is NOT reducible to a memoryless NCA.
  H3  THE HANSALI PARALLEL (the convergence claim): the clone-with-
      memory's closed-loop trajectory stays within the stack's own
      trajectory tube (the max per-cell deviation <= 2x the stack's
      seed-to-seed spread at every checkpoint) — the LOCAL rule
      reproduces the COMPETENCE (the NCA parallel is real: a local
      perceptron suffices WHEN the perception includes the memory).

THE BRANCH (pre-named): H2 PASS (with-memory completes, without fails)
-> MEMORY-NECESSARY (the stack's regen is NOT a memoryless-NCA
phenomenon; the theta layer is the irreducible difference — the
Hansali/Levin memory claim grounded computationally); H2 REFUTE ->
REDUCIBLE (a memoryless local rule regenerates the pattern — the
memory's information is dispensable, deposited honestly).

RUN: the transition recording + 2 ridge fits + the closed-loop panels;
serial, BLAS pinned; minutes.
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
OUT = os.path.join(ROOT, "results", "exp237_nca_clone_bound.json")


def main() -> dict:
    print("=== exp237: the NCA clone bound (the Hansali parallel) ===\n")

    # ---- the frozen machinery, imported (never re-implemented) -----------
    from experiments.exp73_active_renormalization import (  # the battery
        make_battery, N, ERR_BAR, RUN_T, DT, VERDICT_SEEDS,
    )
    from experiments.exp43_substrate_independence import (  # the labeling
        labeling, region_err,
    )
    from cultivation.substrate.graph import GraphCollective
    from cultivation.bioelectric.collective import V_PHYS_MIN, V_PHYS_MAX

    # ---- the instrument (zero-knob; every choice frozen here) ------------
    WOUND = slice(40, 60)                # exp79's TC-G6 mid wound — the
    WOUND_REGION = list(range(40, 60))   # batch-15 torus precedent (T4)
    FIT_SEEDS = (1, 2)                   # the transition-fit seeds
    HELDOUT_SEED = 3                     # the full held-out trajectory
    RIDGE_LAM = 1e-6                     # numerical conditioning only
    REGEN_WINDOW = 15.0                  # exp43's regen settle window
    CELL_PERIOD, REGEN_NOISE = 0.8, 0.6  # exp43's walk constants
    CHECK_EVERY = 10                     # checkpoint stride (steps)
    H1_BAR = 0.95
    H2_FAIL_MULT = 2.0                   # the clone-without fail bar (2x)
    TUBE_MULT = 2.0                      # H3's tube multiplier

    battery = make_battery()
    A = battery["torus"]                 # the NCA-native topology
    lbl = labeling(N)
    region_idx = np.arange(N)[WOUND]
    n_steps = len(WOUND_REGION) * int(round(CELL_PERIOD / DT)) \
        + int(round(REGEN_WINDOW / DT))

    class _Recording(GraphCollective):
        """The stack's collective with per-step (V, theta) transition
        recording switched on for the regeneration window. step() is the
        ONLY addition; the recorded pairs are clean one-step dynamics
        transitions (the walk's commitment writes land BETWEEN steps and
        never appear as transitions)."""

        def __init__(self, **kw):
            super().__init__(**kw)
            self._record = False
            self.pre_V, self.pre_th = [], []
            self.post_V, self.post_th = [], []

        def step(self, dt: float = 0.1) -> None:
            if self._record:
                self.pre_V.append(self.V.copy())
                self.pre_th.append(self.theta.copy())
            super().step(dt)
            if self._record:
                self.post_V.append(self.V.copy())
                self.post_th.append(self.theta.copy())

    def perception(V: np.ndarray, th: np.ndarray,
                   use_theta: bool) -> np.ndarray:
        """phi — the NCA standard perception on the canonical neighborhood
        (A[i] > 0): per layer (self, neighbor-mean, neighbor-std), plus
        the constant and the graph-Sobel gradient channel (neighbor-mean
        - self; the undirected regular graph's collapse of the NCA's
        directed Sobel pair). V-only: 5 features; with theta: 9 — the
        pre-named counts. V/th: (T, n) or (n,); returns (T*n, F)/(n, F)."""
        V2 = np.atleast_2d(V)
        th2 = np.atleast_2d(th)
        nbr = (A > 0).astype(float)
        deg = nbr.sum(axis=1)
        V_nbm = (nbr @ V2.T).T / deg
        V_nbs = np.sqrt(np.maximum((nbr @ (V2 ** 2).T).T / deg
                                   - V_nbm ** 2, 0.0))
        cols = [np.ones_like(V2), V2, V_nbm, V_nbs, V_nbm - V2]
        if use_theta:
            t_nbm = (nbr @ th2.T).T / deg
            t_nbs = np.sqrt(np.maximum((nbr @ (th2 ** 2).T).T / deg
                                       - t_nbm ** 2, 0.0))
            cols += [th2, t_nbm, t_nbs, t_nbm - th2]
        return np.stack(cols, axis=-1).reshape(-1, len(cols))

    # ---- the stack's regen reference + the transition recording ----------
    print("  the stack's regen reference on the torus (exp73 settle -> "
          "amputate defaults -> regrow_graph walk -> run(15)):")
    stack: dict[int, dict] = {}
    rec: dict[int, tuple] = {}
    for s in VERDICT_SEEDS:
        c = _Recording(adjacency=A, seed=s)
        c.set_target(lbl)
        c.theta = lbl.copy()
        c.V = c.theta + c.rng.normal(0.0, 2.0, N)       # exp73's settle
        c.run(RUN_T, dt=DT)
        c.amputate(WOUND)            # the absolute defaults -30/-40
        c._record = True
        wound = (c.V.copy(), c.theta.copy())
        c.regrow_graph(WOUND_REGION, cell_period=CELL_PERIOD, dt=DT,
                       noise=REGEN_NOISE)
        c.run(REGEN_WINDOW, dt=DT)
        c._record = False
        assert len(c.post_V) == n_steps, (len(c.post_V), n_steps)
        stack[s] = {
            "wound": wound,
            "traj_V": np.array(c.post_V),
            "traj_th": np.array(c.post_th),
            "region_err": region_err(c, region_idx, lbl),
            "pattern_err": c.pattern_error(lbl),
        }
        rec[s] = (np.array(c.pre_V), np.array(c.pre_th),
                  np.array(c.post_V), np.array(c.post_th))
        print(f"    seed {s}: regen region err "
              f"{stack[s]['region_err']:.3f} mV | whole-tissue "
              f"{stack[s]['pattern_err']:.3f} mV")

    # ---- the dataset D and the two ridge fits -----------------------------
    def dataset(seeds, use_theta: bool) -> tuple[np.ndarray, np.ndarray]:
        Phis, Ys = [], []
        for s in seeds:
            pre_V, pre_th, post_V, post_th = rec[s]
            Phis.append(perception(pre_V, pre_th, use_theta))
            Ys.append(np.column_stack([post_V.ravel(), post_th.ravel()]))
        return np.vstack(Phis), np.vstack(Ys)

    Phi_tr_w, Y_tr = dataset(FIT_SEEDS, True)
    Phi_tr_wo, _ = dataset(FIT_SEEDS, False)
    Phi_te_w, Y_te = dataset((HELDOUT_SEED,), True)
    Phi_te_wo, _ = dataset((HELDOUT_SEED,), False)
    assert Phi_tr_w.shape[1] == 9 and Phi_tr_wo.shape[1] == 5

    def ridge(Phi: np.ndarray, Y: np.ndarray, lam: float) -> np.ndarray:
        F = Phi.shape[1]
        return np.linalg.solve(Phi.T @ Phi + lam * np.eye(F), Phi.T @ Y)

    W_with = ridge(Phi_tr_w, Y_tr, RIDGE_LAM)      # (9, 2): V', theta'
    W_without = ridge(Phi_tr_wo, Y_tr, RIDGE_LAM)  # (5, 2)
    print(f"  D: {Phi_tr_w.shape[0]} fit transitions (seeds {FIT_SEEDS}), "
          f"{Phi_te_w.shape[0]} held out (seed {HELDOUT_SEED}); "
          f"ridge fits done (9 and 5 features)")

    # ---- H1: the one-step fidelity (held-out seed 3) ----------------------
    def r2(Phi: np.ndarray, Y: np.ndarray, W: np.ndarray) -> float:
        res = float(np.sum((Y - Phi @ W) ** 2))
        tot = float(np.sum((Y - Y.mean(axis=0)) ** 2))
        return 1.0 - res / tot

    r2_with = {"pooled": r2(Phi_te_w, Y_te, W_with),
               "V": r2(Phi_te_w, Y_te[:, :1], W_with[:, :1]),
               "theta": r2(Phi_te_w, Y_te[:, 1:], W_with[:, 1:])}
    r2_without = {"pooled": r2(Phi_te_wo, Y_te, W_without),
                  "V": r2(Phi_te_wo, Y_te[:, :1], W_without[:, :1]),
                  "theta": r2(Phi_te_wo, Y_te[:, 1:], W_without[:, 1:])}
    h1_pass = bool(r2_with["pooled"] >= H1_BAR)
    expect_held = bool(r2_without["pooled"] < r2_with["pooled"])
    print(f"  H1 one-step R^2 (held-out seed {HELDOUT_SEED}): "
          f"with-memory {r2_with['pooled']:.6f} "
          f"(V {r2_with['V']:.6f}, theta {r2_with['theta']:.6f}) | "
          f"without {r2_without['pooled']:.6f} "
          f"(V {r2_without['V']:.6f}, theta {r2_without['theta']:.6f}) "
          f"-> {'PASS' if h1_pass else 'REFUTED'} "
          f"(bar {H1_BAR}; 'strictly lower' expectation "
          f"{'held' if expect_held else 'NOT held'})")

    # ---- H2/H3: the closed-loop panels ------------------------------------
    class _Clone(GraphCollective):
        """The frozen regen machinery with the LOCAL UPDATE replaced by a
        fitted linear local rule (the behavioral clone). step() is the
        ONLY override: amputate/regrow_graph/run are the stack's own
        machinery, run verbatim on the clone's own state."""

        def __init__(self, Wfit, use_theta, **kw):
            super().__init__(**kw)
            self._Wfit = Wfit
            self._use_theta = use_theta
            self.traj_V, self.traj_th = [], []

        def step(self, dt: float = 0.1) -> None:
            assert abs(dt - DT) < 1e-12, "the clone is a dt=DT one-step map"
            phi = perception(self.V, self.theta, self._use_theta)
            x = phi @ self._Wfit                                 # (n, 2)
            self.V = np.clip(x[:, 0], V_PHYS_MIN - 5.0, V_PHYS_MAX + 5.0)
            self.theta = np.clip(x[:, 1], V_PHYS_MIN, V_PHYS_MAX)
            self.traj_V.append(self.V.copy())
            self.traj_th.append(self.theta.copy())

    clones: dict[str, dict[int, dict]] = {}
    for name, Wfit, use_th in (("with_memory", W_with, True),
                               ("without", W_without, False)):
        clones[name] = {}
        for s in VERDICT_SEEDS:
            cc = _Clone(Wfit=Wfit, use_theta=use_th, adjacency=A, seed=s)
            cc.V = stack[s]["wound"][0].copy()
            cc.theta = stack[s]["wound"][1].copy()
            cc.regrow_graph(WOUND_REGION, cell_period=CELL_PERIOD, dt=DT,
                            noise=REGEN_NOISE)
            cc.run(REGEN_WINDOW, dt=DT)
            assert len(cc.traj_V) == n_steps
            clones[name][s] = {
                "traj_V": np.array(cc.traj_V),
                "traj_th": np.array(cc.traj_th),
                "region_err": region_err(cc, region_idx, lbl),
                "pattern_err": cc.pattern_error(lbl),
                "theta_region_err": float(np.sqrt(np.mean(
                    (cc.theta[region_idx] - lbl[region_idx]) ** 2))),
            }

    print("  H2 closed-loop regen (final region err vs the label, "
          f"bar {ERR_BAR} / fail bar {H2_FAIL_MULT * ERR_BAR}):")
    h2_rows = []
    for name in ("with_memory", "without"):
        for s in VERDICT_SEEDS:
            e = clones[name][s]
            h2_rows.append({"clone": name, "seed": s,
                            "region_err": round(e["region_err"], 4),
                            "pattern_err": round(e["pattern_err"], 4),
                            "theta_region_err": round(
                                e["theta_region_err"], 4)})
            print(f"    {name:12s} seed {s}: region err "
                  f"{e['region_err']:.3f} mV | whole-tissue "
                  f"{e['pattern_err']:.3f} mV")
    mean_with = float(np.mean([clones["with_memory"][s]["region_err"]
                               for s in VERDICT_SEEDS]))
    mean_without = float(np.mean([clones["without"][s]["region_err"]
                                  for s in VERDICT_SEEDS]))
    leg1 = bool(mean_with < ERR_BAR)
    leg2 = bool(mean_without >= H2_FAIL_MULT * ERR_BAR)
    h2_pass = bool(leg1 and leg2)
    print(f"    mean: with-memory {mean_with:.3f} "
          f"({'completes' if leg1 else 'FAILS'}), without "
          f"{mean_without:.3f} "
          f"({'fails at >= 2x bar' if leg2 else 'completes — the fail leg REFUTED'}) "
          f"-> H2 {'PASS' if h2_pass else 'REFUTED'}")

    # ---- H3: the trajectory tube ------------------------------------------
    stack_V = np.stack([stack[s]["traj_V"] for s in VERDICT_SEEDS])
    stack_th = np.stack([stack[s]["traj_th"] for s in VERDICT_SEEDS])
    stack_mean = stack_V.mean(axis=0)
    stack_spread = np.maximum.reduce([
        np.abs(stack_V[0] - stack_V[1]),
        np.abs(stack_V[0] - stack_V[2]),
        np.abs(stack_V[1] - stack_V[2])])           # per-cell seed diameter
    ckpts = list(range(CHECK_EVERY - 1, n_steps, CHECK_EVERY))
    h3_rows, h3_pass = [], True
    print(f"  H3 trajectory tube ({len(ckpts)} checkpoints, every "
          f"{CHECK_EVERY} steps; max per-cell deviation vs 2x the stack's "
          "seed-to-seed spread):")
    for s in VERDICT_SEEDS:
        dev = np.abs(clones["with_memory"][s]["traj_V"] - stack_mean)
        ratios = [float(dev[t].max()
                        / (TUBE_MULT * stack_spread[t].max() + 1e-12))
                  for t in ckpts]
        worst_t = int(np.argmax(ratios))
        per_cell = dev / (TUBE_MULT * stack_spread + 1e-12)
        wi = np.unravel_index(np.argmax(per_cell), per_cell.shape)
        dev_th = np.abs(clones["with_memory"][s]["traj_th"]
                        - stack_th.mean(axis=0))
        spread_th = np.maximum.reduce([
            np.abs(stack_th[0] - stack_th[1]),
            np.abs(stack_th[0] - stack_th[2]),
            np.abs(stack_th[1] - stack_th[2])])
        th_ratio = float(np.max(dev_th
                                / (TUBE_MULT * spread_th + 1e-12)))
        ok = bool(max(ratios) <= 1.0)
        h3_pass &= ok
        h3_rows.append({
            "seed": s, "pass": ok,
            "worst_checkpoint_step": ckpts[worst_t],
            "worst_ratio": round(max(ratios), 4),
            "checkpoint_ratios": [round(r, 4) for r in ratios],
            "per_cell_worst_ratio": round(float(per_cell.max()), 4),
            "per_cell_worst_at": {"step": int(wi[0]) + 1,
                                  "cell": int(wi[1])},
            "theta_tube_worst_ratio_disclosure": round(th_ratio, 4),
        })
        print(f"    seed {s}: worst checkpoint ratio "
              f"{max(ratios):.3f} at step {ckpts[worst_t]} "
              f"(per-cell worst {float(per_cell.max()):.3f}) "
              f"-> {'within tube' if ok else 'OUT of tube'}")
    h3_pass = bool(h3_pass)

    # ---- THE BRANCH --------------------------------------------------------
    branch = "MEMORY-NECESSARY" if h2_pass else "REDUCIBLE"
    criteria = {
        "H1_one_step_fidelity": h1_pass,
        "H2_closed_loop_regen_bound": h2_pass,
        "H3_hansali_parallel_tube": h3_pass,
    }
    npass = sum(bool(v) for v in criteria.values())
    print(f"\n  BRANCH (pre-named): {branch}")
    if branch == "MEMORY-NECESSARY":
        print("  the memory layer's information is NECESSARY for the regen "
              "competence: the stack is NOT reducible to a memoryless NCA")
    else:
        print("  a memoryless local rule regenerates the pattern — the "
              "memory's information is dispensable, deposited honestly")

    out = {
        "exp": "exp237_nca_clone_bound (the Hansali 2025 parallel; "
               "ledger L213)",
        "branch": branch,
        "machinery": {
            "battery": "exp73_active_renormalization.make_battery "
                       "(the torus arm, exp68's battery verbatim)",
            "labeling": "exp43_substrate_independence.labeling",
            "region_err": "exp43_substrate_independence.region_err",
            "protocol": "exp73's settle (theta=labels, V=theta+N(0,2), "
                        "RUN_T=24, DT=0.1) -> amputate defaults (-30/-40) "
                        "-> regrow_graph walk (cell_period=0.8, "
                        "noise=0.6) -> run(15) — exp43's SI-G2 protocol "
                        "at exp73/exp79's constants",
            "physiology": "cultivation.bioelectric.collective "
                          "V_PHYS_MIN/MAX clips (the stack's own bounds)",
        },
        "instrument": {
            "arm": "torus (10x10, N=100, degree-4 canonical neighborhood)",
            "wound": "slice(40, 60) — exp79's TC-G6 mid wound, the "
                     "batch-15 torus precedent (exp234 T4's exact region)",
            "clones": {
                "with_memory": "phi = [1, V_self, V_nbm, V_nbs, V_grad, "
                               "th_self, th_nbm, th_nbs, th_grad] (9)",
                "without": "phi = [1, V_self, V_nbm, V_nbs, V_grad] (5) "
                           "— the pure-NCA perception",
                "gradient_channel": "V_grad = V_nbm - V_self: the NCA's "
                                    "directed Sobel pair collapsed on an "
                                    "undirected regular graph",
                "rule": "x'_t+1 = W @ phi(x_t), W fitted by ridge least "
                        f"squares (lambda={RIDGE_LAM}, numerical "
                        "conditioning only) on D; step() replaced, "
                        "regen machinery verbatim",
            },
            "dataset": {
                "fit_transitions": int(Phi_tr_w.shape[0]),
                "heldout_transitions": int(Phi_te_w.shape[0]),
                "fit_seeds": list(FIT_SEEDS),
                "heldout_seed": HELDOUT_SEED,
                "window_steps_per_seed": int(n_steps),
                "pairing": "clean one-step (pre, post) dynamics "
                           "transitions; commitment writes land between "
                           "steps and never appear as transitions",
            },
            "checkpoints": {"stride_steps": CHECK_EVERY,
                            "count_per_seed": len(ckpts)},
            "bars": {"H1_R2": H1_BAR, "H2_regen_err": ERR_BAR,
                     "H2_fail_mult": H2_FAIL_MULT,
                     "H3_tube_mult": TUBE_MULT},
        },
        "W_matrices": {
            "W_with_rows_V_theta_9feat": np.round(W_with.T, 6).tolist(),
            "W_without_rows_V_theta_5feat": np.round(W_without.T, 6).tolist(),
        },
        "H1": {"r2_with": {k: round(v, 6) for k, v in r2_with.items()},
               "r2_without": {k: round(v, 6)
                              for k, v in r2_without.items()},
               "bar": H1_BAR, "pass": h1_pass,
               "expectation_strictly_lower_held": expect_held},
        "H2": {"rows": h2_rows,
               "mean_region_err_with": round(mean_with, 4),
               "mean_region_err_without": round(mean_without, 4),
               "leg1_with_completes": leg1,
               "leg2_without_fails_at_2x": leg2,
               "pass": h2_pass},
        "H3": {"rows": h3_rows, "pass": h3_pass,
               "tube": "deviation from the stack's 3-seed mean vs 2x the "
                       "per-checkpoint maximal per-cell seed diameter "
                       "(V layer gated; theta-layer worst ratio "
                       "deposited per seed as disclosure)"},
        "criteria": criteria,
        "notes": (
            "Body-landing disclosures: (a) the closed loop grants BOTH "
            "clones the frozen regen machinery verbatim (amputate "
            "defaults -> regrow_graph walk -> run(15)) on the clone's "
            "own state; the clone substitutes the fitted linear rule for "
            "the LOCAL UPDATE only (step()), so the walk's inheritance "
            "reads — which read theta, the memory layer — are protocol, "
            "not rule; H2 prices the RULE's memory-needs given the "
            "protocol, and the without clone's commitments inherit "
            "theta[src] maintained by its own fitted theta-map (a "
            "function of V-features alone). (b) The wound is exp79's "
            "TC-G6 mid wound slice(40,60) — the batch-15 torus "
            "precedent (exp234 T4's exact region); exp43's tail "
            "slice(85,100) on the torus wraps against the head block "
            "and the stack's own walk commits wrapped cells to head "
            "identity (the reference would fail its own bar "
            "structurally). (c) The perception's 4th per-layer channel "
            "is the graph-Sobel gradient (neighbor-mean - self); on the "
            "regular torus it is exactly collinear with (self, "
            "neighbor-mean) — the ridge minimum-norm solution absorbs "
            "it and the pre-named 9/5 counts hold. (d) The fit/held-out "
            "split is by whole trajectory (fit seeds 1,2; held-out "
            "seed 3). (e) The clone is a deterministic mean-flow rule; "
            "its commitment-noise draws ride its own seed-s rng stream "
            "(the stack's dynamics-noise draws shift the streams; the "
            "tube is the pre-named absorber). (f) H2 gates the MEAN "
            "region error over the 3 seeds (exp73's verdict "
            "convention), per-seed errs deposited; the whole-tissue "
            "pattern error on the torus carries the plateau write-fail "
            "floor (~8.4 mV, exp73 SR-G1) — the regen bar applies to "
            "the REGENERATED REGION (exp43 SI-G2 semantics); "
            "whole-tissue errs deposited as disclosure. (g) H3's "
            "per-cell worst ratio (the strict per-cell tube reading) "
            "deposited beside the gated scalar reading."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1, default=float)
    print(f"\n  results -> {OUT}")
    print(f"  === {npass}/3 gates PASS ===")
    return out


if __name__ == "__main__":
    main()
