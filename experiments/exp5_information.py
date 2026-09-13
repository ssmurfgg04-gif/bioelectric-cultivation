"""EXP5 — Information metrics: I(V;M) and integration Phi.

(a) Mutual information between the bioelectric state and the morphological
    outcome: sample initial states around three attractor basins, run the
    dynamics, classify the outcome, measure MI. Prediction: MI is high at
    low noise and DECAYS as channel noise grows (aging = information loss),
    and reprogramming RE-ROUTES the information to a new target.

(b) Integration Phi (linear-Gaussian): peaks at intermediate coupling;
    ~0 for modular systems; rises under coherent drive in a CTRNN (the
    crude computational stand-in for attention/meditation states); computed
    on REAL C. elegans gap-junction motifs.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from cultivation.bioelectric.collective import BioElectricCollective
from cultivation.bioelectric.morphospace import (
    wildtype_target, twoheaded_target, pattern_error,
)
from cultivation.information.mutual_info import estimate_mi_joint
from cultivation.information.phi import phi_integration, connectivity_family_phi
from cultivation.neural.ctrnn import CTRNN, make_small_world
from cultivation.neural.connectome import load_celegans_gap_junctions, motif_samples
from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

N = 60
TARGETS = {
    "wt": wildtype_target(N),
    "twohead": twoheaded_target(N),
    "midcorrupt": None,  # built below
}


def _midcorrupt_target():
    t = wildtype_target(N)
    t[25:35] = -20.0
    return t


TARGETS["midcorrupt"] = _midcorrupt_target()


def outcome_class(final_V: np.ndarray) -> int:
    errs = [pattern_error(final_V, TARGETS[k]) for k in ("wt", "twohead", "midcorrupt")]
    return int(np.argmin(errs))


def features(V: np.ndarray) -> np.ndarray:
    return np.array([
        V[: N // 4].mean() - V[-N // 4:].mean(),   # polarity coefficient
        (V > -32).mean(),                           # depolarized fraction
        V[N // 2 - 3: N // 2 + 3].mean(),           # mid-region level
    ])


def mi_dataset(age: float, n_samples: int = 450, seed: int = 0) -> float:
    """I(V_mid; M): how much does the CURRENT bioelectric state tell you about
    the morphology the system will build? The gap-junction network is the
    denoiser: young tissue cleans up a noisy V so V_mid still predicts the
    outcome; aged tissue (noise grown, junctions decayed) cannot — the state
    decouples from the morphology it is supposed to encode."""
    rng = np.random.default_rng(seed)
    sigma = 3.0 + 25.0 * age
    g = 0.2 * (1.0 - 0.9 * age)
    X, y = [], []
    for i in range(n_samples):
        basin = i % 3
        target = TARGETS[["wt", "twohead", "midcorrupt"][basin]]
        c = BioElectricCollective(n=N, seed=int(rng.integers(1 << 30)),
                                  noise_std=sigma, g_gap=g)
        c.set_target(target)
        c.set_state(target + rng.normal(0, sigma, N))
        c.run(2, dt=0.1)              # partial relaxation + GJ smoothing
        V_mid = c.V.copy()            # the observable state
        c.run(13, dt=0.1)             # settle to the outcome
        X.append(features(V_mid))
        y.append(outcome_class(c.V))
    X = np.array(X); y = np.array(y)
    return estimate_mi_joint(X, y, bins=4)


def ctrnn_phi_states(seed: int = 0) -> dict:
    """EXPLORATORY / HONEST NEGATIVE: linearized Phi at a fixed point cannot
    distinguish coherent from incoherent drive (the Jacobian depends on
    activation magnitude, not coherence pattern). Recorded, not asserted —
    time-resolved integration measures are future work."""
    W = make_small_world(10, k=3, p=0.3, w=0.8, seed=seed)
    out = {}
    for label, drive in [
        ("rest", None),
        ("coherent_drive", "strong"),
        ("incoherent_drive", "noise"),
    ]:
        net = CTRNN(W, tau=1.0, noise=0.02, seed=seed)
        if drive == "strong":
            I = net.coherent_drive(strength=0.6)
        elif drive == "noise":
            rng = np.random.default_rng(seed)
            I = rng.normal(0, 0.6, 10)
        else:
            I = None
        net.run(40, dt=0.05, I=I)
        J = net.jacobian()
        A = np.eye(10) + 0.5 * J
        rho = float(np.max(np.abs(np.linalg.eigvals(A))) + 1e-9)
        A = A * (0.95 / rho)  # stabilize: active but non-explosive
        res = phi_integration(A, np.eye(10) * 0.05, max_bipartitions=256)
        out[label] = {"phi": res["phi"], "I_whole": res["I_whole"]}
    return out


def main() -> dict:
    setup()
    results: dict = {}

    # ---- (a) MI vs age ---------------------------------------------------------------
    ages = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    mi_curve = []
    for a in ages:
        mi = mi_dataset(a, n_samples=360, seed=int(1000 * a + 7))
        mi_curve.append({"age": a, "MI_bits": mi})
        print(f"  age={a:.1f} -> I(V;M) = {mi:.3f} bits")
    results["mi_vs_noise"] = mi_curve
    mi_hi = mi_curve[0]["MI_bits"]
    mi_lo = mi_curve[-1]["MI_bits"]
    results["C_mi_high_when_healthy"] = mi_hi > 1.0
    results["C_mi_decays_with_noise"] = mi_lo < 0.55 * mi_hi  # >45% information loss
    print(f"  MI decays with noise: {results['C_mi_decays_with_noise']} "
          f"({mi_hi:.2f} -> {mi_lo:.2f} bits)")

    # ---- (b) Phi: connectivity family ------------------------------------------------
    fam = connectivity_family_phi(n=8, seed=0)
    results["phi_family"] = {k: v for k, v in fam.items() if not isinstance(v, list)}
    results["phi_coupling_sweep"] = fam["coupling_sweep"]
    peak_g = max(fam["coupling_sweep"], key=lambda x: x[1])[0]
    results["C_phi_peaks_intermediate"] = (
        fam["two_modules"] < 0.05 and 0.15 < peak_g < 1.2
    )
    print(f"  Phi family: modular={fam['two_modules']:.3f} chain={fam['chain']:.3f} "
          f"smallworld={fam['smallworld']:.3f} peak coupling g={peak_g}")

    # ---- (c) CTRNN drive states: exploratory, honest negative --------------------------
    st = ctrnn_phi_states(seed=3)
    results["ctrnn_states"] = st
    results["C_coherent_drive_raises_phi"] = (
        st["coherent_drive"]["phi"] > st["rest"]["phi"]
        and st["coherent_drive"]["phi"] > st["incoherent_drive"]["phi"]
    )  # recorded, NOT asserted — linearized Phi cannot see coherence (documented)
    results["ctrnn_note"] = ("Linearized fixed-point Phi depends on activation magnitude, "
                             "not coherence; time-resolved measures required. Honest negative.")
    print(f"  CTRNN Phi: rest={st['rest']['phi']:.3f} "
          f"coherent={st['coherent_drive']['phi']:.3f} "
          f"incoherent={st['incoherent_drive']['phi']:.3f}")

    # ---- (d) real C. elegans gap-junction motifs --------------------------------------
    A, names = load_celegans_gap_junctions()
    motifs = motif_samples(A, size=8, n_samples=25, seed=2)
    phis = []
    for m in motifs:
        rho = float(np.max(np.abs(np.linalg.eigvals(m))) + 1e-9)  # spectral radius
        Wn = m / max(rho, 1.0) * 0.7  # spectrally normalized, active coupling
        res = phi_integration(Wn, np.eye(8) * 0.05, max_bipartitions=256)
        phis.append(res["phi"])
    results["celegans_motif_phi"] = {
        "n_motifs": len(phis), "mean": float(np.mean(phis)),
        "std": float(np.std(phis)), "max": float(np.max(phis)),
        "n_cells_in_gap_network": int(A.shape[0]),
        "gap_edges": int((A > 0).sum() // 2),
    }
    print(f"  C. elegans gap junctions: {A.shape[0]} cells, "
          f"{int((A>0).sum()//2)} edges; motif Phi mean={np.mean(phis):.3f} "
          f"max={np.max(phis):.3f}")

    # ---- figure ---------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(9.5, 7.2), constrained_layout=True)
    ax = axes[0, 0]
    ax.plot([m["age"] for m in mi_curve], [m["MI_bits"] for m in mi_curve],
            "o-", color=PALETTE["primary"])
    ax.set_title("(a) I(V; M) vs organismal age (information loss)")
    ax.set_xlabel("age (noise grows, gap junctions decay)")
    ax.set_ylabel("mutual information (bits)")

    ax = axes[0, 1]
    keys = ["chain", "er_p0.3", "er_p0.5", "smallworld", "alltoall_w0.1", "two_modules"]
    vals = [fam[k] for k in keys]
    ax.bar(range(len(keys)), vals, color=[PALETTE["primary"]] * 4 + [PALETTE["muted"]] * 2)
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(["chain", "ER .3", "ER .5", "small-world", "all-to-all", "2 modules"],
                       fontsize=7, rotation=20)
    ax.set_title("(b) Integration Phi by connectivity family")
    ax.set_ylabel("Phi (bits)")

    ax = axes[1, 0]
    sweep = fam["coupling_sweep"]
    ax.plot([s[0] for s in sweep], [s[1] for s in sweep], "o-",
            color=PALETTE["accent"])
    ax.axhline(0, color=PALETTE["muted"], lw=0.8)
    ax.set_title("(c) Phi vs coupling strength (peak at intermediate)")
    ax.set_xlabel("coupling g")
    ax.set_ylabel("Phi (bits)")

    ax = axes[1, 1]
    ax.hist(phis, bins=10, color=PALETTE["primary"], alpha=0.85)
    ax.axvline(np.mean(phis), color=PALETTE["accent"], ls="--", lw=1.2,
               label=f"mean {np.mean(phis):.2f} bits")
    ax.set_title("(d) Phi of real C. elegans gap-junction motifs (8-cell)")
    ax.set_xlabel("Phi (bits)"); ax.set_ylabel("count")
    ax.legend(frameon=False)

    fig.savefig(fig_path("fig5_information.png"))
    plt.close(fig)

    path = dump_json("exp5_information.json", results)
    print(f"[exp5] results -> {path}")
    for k in ["C_mi_high_when_healthy", "C_mi_decays_with_noise",
              "C_phi_peaks_intermediate"]:
        print(f"  {k}: {results[k]}")
    print(f"  C_coherent_drive_raises_phi (exploratory, not asserted): "
          f"{results['C_coherent_drive_raises_phi']}")
    return results


if __name__ == "__main__":
    main()
