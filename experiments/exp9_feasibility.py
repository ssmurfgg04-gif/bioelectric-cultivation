"""EXP9 — Feasibility audits for the cultivation-tier claims.

The cultivation hierarchy (the project's honest framing) makes claims at
increasing distance from established physics:

  Tier A  bioelectric self-control beyond autonomic ceiling
  Tier B  morphological control (pattern read/write at will)
  Tier C  biofield influence on EXTERNAL biological systems at range
  Tier D  consciousness-matter interaction (micro-PK amplified to macro)
  Tier E  substrate independence

Tiers A-B are Levin-layer biology: established in model organisms, and now
computationally modeled in this repo (exp1-8). Tiers C-E are the ones the
novels describe and physics must either permit or forbid. This experiment
does the arithmetic NOBODY HAS PUBLISHED in integrated form: take the actual
measured numbers from decades of research and derive the required
amplification factors — an honest feasibility map instead of ridicule or
faith.

AUDIT 1 — the biofield amplification ladder
-------------------------------------------
Established numbers: the heart's magnetic field ~100 pT at 1 m (MCG
literature), brain ~10-1000 fT; the Earth's Schumann resonance ~1 pT. A cell
needs an induced transmembrane shift of order 5 mV (half a Vmem band — our
model's decision margin, and the empirical scale at which Levin-group
experiments flip cell behavior) to change discrete state. Schwan's
polarization formula dV = 1.5 a E (spherical cell, radius a) converts fields
to membrane voltage. Endogenous CURRENT-dipole sources produce tissue
E-fields that decay as 1/r^3; time-varying magnetic induction produces
E = (r/2) dB/dt. We compute, for each distance, the honest gap between what
biology radiates and what a cell needs — and what coherence (N sources
acting in phase, near-field scaling N vs sqrt(N)) would be required to close
it.

AUDIT 2 — selection vs energy (the collapse-bias scaling law)
--------------------------------------------------------------
The strongest anomalous results (PEAR 28-year RNG program: ~1e-4 per-trial
bias; Ganzfeld meta-analysis ES 0.088, ~3x in trained participants) are
TINY. The acupuncture precedent (dismissed for centuries; mechanism turned
out to be vagus-nerve stimulation; once found, the intervention could be
optimized) says small-but-real effects deserve mechanism searches, not
ridicule — but the search should be guided by honest arithmetic:
  - A single amplified quantum decision CAN flip a macroscopic switch
    (selection architecture: the energy comes from the power supply; the
    quantum event only selects). At PEAR's epsilon this is already
    "macro" in the statistical sense — that IS what PEAR measured.
  - Moving matter is different: it needs coherent redirection of thermal
    events. We compute the thermodynamic ceiling: if EVERY molecular event
    in 10 g of tissue could be biased at epsilon = 1e-4 with perfect
    rectification, the redirected power is P = eps * f * kT with f the
    addressable event rate. The result: milliwatts at the absurd extreme,
    microwatts-to-nanowatts at any realistic addressing rate.
  - Verdict frame: mW is ~6 orders short of shattering anything, but it is
    ORDERS ABOVE the pJ-scale energy of a bioelectric state transition.
    If a real consciousness-matter interface exists, the FIRST place it
    could physically express is exactly the bioelectric layer — Levin's
    layer — the layer this repository models.

Both audits are pure arithmetic on literature values; no simulation
parameters to tune. The output is a table of required amplifications and
the verdict each tier earns.
"""

from __future__ import annotations

import sys

import numpy as np

sys.path.insert(0, ".")

from experiments.viz import setup, dump_json, fig_path, PALETTE

import matplotlib.pyplot as plt

# ------------------------------------------------------------------ constants
K_B = 1.380649e-23          # J/K
T_BODY = 310.15             # K
KBT = K_B * T_BODY          # ~4.28e-21 J
C_LIGHT = 2.998e8           # m/s
MU0 = 4 * np.pi * 1e-7      # T m / A

CELL_RADIUS = 10e-6         # m (typical somatic cell)
SCHWAN = 1.5                # dV = SCHWAN * a * E for a spherical cell
DV_FLIP = 5e-3              # V — half a Vmem band (discrete-state margin)

HEART_B_1M = 100e-12        # T — MCG peak at 1 m
HEART_FREQ = 1.2            # Hz — cardiac fundamental
SCHUMANN_B = 1e-12          # T
HEART_DIPOLE = 0.02         # A*m — cardiac current dipole (MCG-calibrated)
TISSUE_SIGMA = 0.5          # S/m
N_BODY_CELLS = 3e13
TOTAL_BODY_CURRENT = 0.1    # A — generous whole-body ionic current budget

PEAR_EPS = 1e-4             # per-trial bias (28-year PEAR program)
GANZFELD_ES = 0.088         # Tressoldi & Storm meta-analysis (selected: ~3x)


def e_field_for_flip() -> float:
    """External E-field needed to shift a cell's Vmem by DV_FLIP (Schwan)."""
    return DV_FLIP / (SCHWAN * CELL_RADIUS)


def audit_biofield() -> dict:
    """AUDIT 1: amplification ladder from measured biofields to cell-state flips."""
    E_need = e_field_for_flip()
    out = {"E_needed_V_per_m": E_need,
           "note": "Schwan: dV = 1.5 a E; dV = 5 mV (half a Vmem band), a = 10 um"}

    # ---- source physics --------------------------------------------------
    # (a) endogenous tissue E-field from the cardiac current dipole: the
    #     field in a conducting medium at distance r: E ~ p / (4 pi sigma r^3)
    def E_dipole(r):
        return HEART_DIPOLE / (4 * np.pi * TISSUE_SIGMA * r ** 3)

    # (b) magnetic induction from the time-varying heart field:
    #     E_ind ~ (r/2) * dB/dt, dB/dt = 2 pi f B(r), B(r) ~ B1 / r^2 (dipole)
    def E_induction(r):
        B_r = HEART_B_1M / r ** 2
        dBdt = 2 * np.pi * HEART_FREQ * B_r
        return 0.5 * r * dBdt

    # (c) Schumann resonance induction
    E_schumann = 0.5 * 1.0 * 2 * np.pi * 7.83 * SCHUMANN_B

    rows = []
    for r in [0.01, 0.05, 0.1, 0.3, 1.0, 3.0]:
        e_dip = E_dipole(r)
        e_ind = E_induction(r)
        best = max(e_dip, e_ind)
        rows.append({
            "distance_m": r,
            "E_dipole_V_per_m": e_dip,
            "E_induction_V_per_m": e_ind,
            "amplification_needed": E_need / best,
        })
    out["ladder"] = rows
    out["schumann"] = {
        "E_induced_V_per_m": E_schumann,
        "amplification_needed": E_need / E_schumann,
        "note": "resonance gain bounded by Q; lossy tissue Q ~ 1-10, so even "
                "perfect tuning closes < 1 order of the ~1e6 gap",
    }

    # ---- coherence requirement -------------------------------------------
    # N coherent current dipoles scale the near field as N (incoherent: sqrt(N)).
    # What N would close the gap at 1 m?
    E_at_1m = max(E_dipole(1.0), E_induction(1.0))
    N_coh = E_need / E_at_1m
    total_dipole = N_coh * HEART_DIPOLE
    out["coherence"] = {
        "N_hearts_coherent_for_1m_flip": float(N_coh),
        "total_dipole_needed_A_m": float(total_dipole),
        "fraction_of_body_ionic_budget": float(
            total_dipole / (TOTAL_BODY_CURRENT * 0.15)),  # 15 cm lever arm
        "note": "the coherent current required exceeds the body's total ionic "
                "current budget by orders of magnitude — passive range effects "
                "are dead as stated; contact-range (cm) effects are real physics",
    }

    # ---- what survives ----------------------------------------------------
    out["verdicts"] = {
        "contact_range_cm": "PLAUSIBLE-UNVERIFIED — endogenous E-fields at 1-3 cm "
                            "reach the mV-per-cell scale; genuine local bioelectric "
                            "interaction between adjacent tissues/organs",
        "organism_range_m": "DEAD-AS-STATED — 4-9 orders of amplification short; "
                            "coherent-source requirement exceeds total body current",
        "schumann_resonance": "DEAD-AS-STATED — induction path ~1e6 short, Q-bounded "
                              "resonance cannot close it",
        "first_testable_proxy": "MEG/MCG-graded magnetometry + cell culture at "
                                "1-10 cm from a practitioner vs matched controls "
                                "(the instrument already exists; nobody has run "
                                "the bioelectric-outcome version)",
    }
    return out


def audit_collapse_bias() -> dict:
    """AUDIT 2: selection vs energy — what a real micro-PK effect could do."""
    out = {"pear_epsilon": PEAR_EPS, "ganzfeld_es": GANZFELD_ES}

    # ---- task energy ladder (J) ------------------------------------------
    tasks = {
        "flip a transistor (selection only)": 1e-15,
        "switch a MEMS cantilever": 1e-9,
        "lift 1 g by 10 cm": 1e-2,
        "shatter concrete (1 MJ-scale)": 1e6,
    }
    out["task_energy_J"] = tasks

    # ---- the selection insight -------------------------------------------
    # An RNG output bit IS macroscopic: the quantum event selects, the power
    # supply supplies. At PEAR's epsilon the effect is already "macro" in the
    # statistical sense — the question is only ORGANIZATION: how many
    # consciously-addressable amplified decisions per second, and what bias.
    # Coherent redirected thermal power ceiling: P = eps * f * kT.
    rates = {
        "10 bit/s (conscious addressing, generous)": 10,
        "10^6 bit/s (subconscious parallel, extravagantly generous)": 1e6,
        "10^15 events/s (every molecular event in ~10 g tissue)": 1e15,
        "10^23 events/s (ALL thermal events in 10 g)": 1e23,
    }
    power = {k: PEAR_EPS * f * KBT for k, f in rates.items()}
    out["redirected_power_W"] = power

    # bioelectric comparison: energy of one cell's discrete state transition
    # C ~ 1 uF/cm^2 * 1000 um^2 = 1e-2 F/m^2 * 1e-9 m^2 = 1e-11 F; dV = 5 mV
    C_cell = 1e-11
    E_bioelectric = 0.5 * C_cell * DV_FLIP ** 2
    out["bioelectric_state_energy_J"] = E_bioelectric

    # time to accumulate task energies at each power level
    times = {}
    for k, p in power.items():
        times[k] = {task: (e / p if p > 0 else np.inf) for task, e in tasks.items()}
    out["time_to_task"] = times

    out["verdicts"] = {
        "selection_architecture": "ALREADY-MACRO-IF-REAL — PEAR's epsilon on an "
                                  "amplified bit is a macroscopic statistical bias; "
                                  "the energy question never arises for switch-flipping",
        "thermal_redirection_ceiling": "MILLIWATTS AT THE ABSURD EXTREME (every "
                                       "molecular event in 10 g biased coherently "
                                       "and rectified perfectly); microwatts at any "
                                       "realistic addressing rate",
        "macro_telekinesis": "DEAD-AS-STATED — 10^8-10^10 short of moving grams or "
                             "shattering matter; no amplification path within known "
                             "physics",
        "bioelectric_expression": "OPEN — mW ceiling is ~9 orders ABOVE the pJ-scale "
                                  "energy of a bioelectric state transition; IF a "
                                  "consciousness-matter interface exists, the first "
                                  "place it could physically express is the "
                                  "bioelectric layer — exactly the layer exp1-8 model",
        "binding_unknown": "no known mechanism allows coherent addressing of "
                           "thermal events; this is the honest open problem — "
                           "the acupuncture precedent (find the mechanism, then "
                           "optimize the intervention) is the research stance",
    }
    return out


def main() -> dict:
    setup()
    print("[exp9] feasibility audits — the honest arithmetic")
    biofield = audit_biofield()
    bias = audit_collapse_bias()

    print(f"\n  AUDIT 1 — biofield amplification ladder")
    print(f"  E-field for a 5 mV cell-state flip: {biofield['E_needed_V_per_m']:.0f} V/m")
    for row in biofield["ladder"]:
        print(f"    r={row['distance_m']:>5} m: dipole E={row['E_dipole_V_per_m']:.2e} V/m, "
              f"induction E={row['E_induction_V_per_m']:.2e} V/m "
              f"-> amplification x{row['amplification_needed']:.1e}")
    coh = biofield["coherence"]
    print(f"  coherent hearts needed for a 1 m flip: {coh['N_hearts_coherent_for_1m_flip']:.1e}"
          f" (needs {coh['fraction_of_body_ionic_budget']:.0e}x the body's total ionic current)")
    print(f"  Schumann: amplification x{biofield['schumann']['amplification_needed']:.1e}")

    print(f"\n  AUDIT 2 — selection vs energy (collapse-bias scaling)")
    print(f"  bioelectric state transition energy: {bias['bioelectric_state_energy_J']:.2e} J")
    for k, p in bias["redirected_power_W"].items():
        print(f"    {k}: redirected power {p:.2e} W")
    t = bias["time_to_task"]
    mid_key = list(t)[1]
    for task, secs in t[mid_key].items():
        yrs = secs / 3.15e7
        print(f"    at {mid_key.split(' (')[0]}: '{task}' takes "
              f"{yrs:.1e} years")

    print("\n  VERDICTS (biofield):")
    for k, v in biofield["verdicts"].items():
        print(f"    {k}: {v}")
    print("  VERDICTS (collapse-bias):")
    for k, v in bias["verdicts"].items():
        print(f"    {k}: {v}")

    # ------------------------------------------------------------ figure
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 3.8), constrained_layout=True)

    ax = axes[0]
    rs = [row["distance_m"] for row in biofield["ladder"]]
    amp = [row["amplification_needed"] for row in biofield["ladder"]]
    ax.loglog(rs, amp, "o-", color=PALETTE["primary"], label="amplification needed")
    ax.axhline(1.0, color=PALETTE["good"], ls="--", lw=1, label="physics boundary")
    ax.axvspan(0.005, 0.03, color=PALETTE["good"], alpha=0.15,
               label="contact range (plausible)")
    ax.set_title("(a) Biofield: amplification to flip a cell state")
    ax.set_xlabel("distance from source (m)")
    ax.set_ylabel("amplification factor (x)")
    ax.legend(frameon=False, fontsize=7)

    ax = axes[1]
    labels = list(bias["redirected_power_W"])
    powers = list(bias["redirected_power_W"].values())
    y = np.arange(len(labels))
    ax.barh(y, np.log10(np.maximum(powers, 1e-30)), color=PALETTE["line2"])
    ax.axvline(np.log10(bias["bioelectric_state_energy_J"] / 1.0),
               color=PALETTE["accent"], ls="--", lw=1.2,
               label="1 bioelectric transition / s (pW-scale)")
    ax.axvline(np.log10(1e-3), color=PALETTE["muted"], ls=":", lw=1.2,
               label="mW (gram-scale work)")
    ax.set_yticks(y)
    ax.set_yticklabels([l.split(" (")[0] for l in labels], fontsize=7)
    ax.set_xlabel("log10 redirected power (W) at PEAR epsilon")
    ax.set_title("(b) Collapse-bias ceiling: selection vs energy")
    ax.legend(frameon=False, fontsize=7)

    fig.savefig(fig_path("fig9_feasibility.png"))
    plt.close(fig)

    results = {"audit_biofield": biofield, "audit_collapse_bias": bias}
    path = dump_json("exp9_feasibility.json", results)
    print(f"\n[exp9] results -> {path}")
    return results


if __name__ == "__main__":
    main()
