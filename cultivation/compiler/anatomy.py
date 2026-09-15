"""Stage 3 (Golden Core) — the anatomical compiler.

THE CLAIM
---------
Stage 2 established the FORWARD map (mechanisms -> recorded anatomy) and
the M28 dual-field gave the model a POSITIONAL layer: `phi_spec`, the
identity-at-coordinate map captured at pattern set. This module is the
INVERSE, deterministic step:

    AnatomySpec (declarative target morphology)
        -> compile() -> InterventionProgram (bioelectric prescription)
        -> verify()  -> in-sim confirmation the program reaches the spec

This is COMPILATION, not search: Phase A (morpho_engineering) discovered
clamp protocols by CEM; the adopted Stage-2 mechanisms (M25
junction-carried readout, M28 phi spec readout, M26c two-face regrow)
make the inverse map ANALYTIC. The phi layer IS the target
representation — writing the spec and triggering a regeneration that
reads it is the whole program.

THE COMPILATION RULES (each adopted mechanism becomes one rule)
--------------------------------------------------------------
  R1  IDENTITY ZONES: every spec zone (coordinate fraction range,
      identity voltage) compiles to a sustained voltage CLAMP over that
      region for the rewrite window (the latch/rewrite requirement: 24h
      sustained forcing — exp1 T1.3, morpho_engineering's anchor).
  R2  TRIGGER: the plane to regenerate compiles to amputate + regrow
      with phi_readout=0.75 (the exp36 adopted mapping) — the regen
      READS the spec layer written by R1.
  R3  COUPLING PRECONDITION: the spec read is junction-carried, so the
      program emits a GJ-health precondition (gap_scale >= 1.0 during
      regen). The compiler does not trust the biology to be healthy —
      it states the requirement and verification checks necessity.
  R4  REPERTOIRE CHECK: identity voltages must lie inside the fate axis
      the model actually stores (physiological bounds + the WT
      repertoire); out-of-repertoire specs are REJECTED at compile time
      (safety/well-formedness — the compiler refuses to prescribe what
      the substrate cannot express).

The prescription is a plain data structure (serializable, audit-ready):
the deliverable a real lab would execute — regions, voltages, durations,
coupling preconditions, and the verification criteria.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# fate-axis repertoire (the identity range the model can express: WT
# head -20 .. WT trunk -50, wound/blastema -40; bounds padded to the
# physiological window the dynamics can hold)
REPERTOIRE_LO = -60.0
REPERTOIRE_HI = -15.0
WINDOW_H = 24.0            # sustained-forcing window (R1)
PHI_ADOPTED = 0.75         # exp36 adopted mapping (R2)
GJ_PRECONDITION = 1.0      # exp36/exp39 coupling requirement (R3)


@dataclass
class Zone:
    """A target identity zone: coordinate fractions [f0, f1) at voltage."""
    f0: float
    f1: float
    voltage: float
    name: str = "zone"


@dataclass
class AnatomySpec:
    """Declarative target morphology: identity zones + trigger plane."""
    zones: list[Zone]
    amputate_plane: str | None = None   # tail|head|trunk|head_tail|None
    cut_f: float = 0.5                  # for crosspiece-style planes
    spec_name: str = "unnamed"

    def validate(self) -> list[str]:
        errs = []
        for z in self.zones:
            if not (0.0 <= z.f0 < z.f1 <= 1.0):
                errs.append(f"zone {z.name}: coordinates must be 0<=f0<f1<=1")
            if not (REPERTOIRE_LO <= z.voltage <= REPERTOIRE_HI):
                errs.append(
                    f"zone {z.name}: voltage {z.voltage} outside the "
                    f"identity repertoire [{REPERTOIRE_LO}, {REPERTOIRE_HI}]")
        if self.amputate_plane not in (None, "tail", "head", "trunk",
                                       "head_tail", "crosspiece"):
            errs.append(f"unknown plane {self.amputate_plane}")
        return errs


@dataclass
class InterventionProgram:
    """The compiled bioelectric prescription (serializable, audit-ready)."""
    spec_name: str
    clamps: list[dict] = field(default_factory=list)   # R1
    regen: dict | None = None                          # R2
    preconditions: dict = field(default_factory=dict)  # R3
    rejected: list[str] = field(default_factory=list)  # R4
    checks: list[dict] = field(default_factory=list)   # verification criteria

    def describe(self) -> str:
        if self.rejected:
            return (f"REJECTED [{self.spec_name}]: " + "; ".join(self.rejected))
        lines = [f"PRESCRIPTION [{self.spec_name}]"]
        for c in self.clamps:
            lines.append(
                f"  1. CLAMP cells {c['i0']}..{c['i1']} at {c['voltage']:+.1f} mV"
                f" for {c['hours']:.0f} h  ({c['zone']})")
        if self.regen:
            lines.append(
                f"  2. AMPUTATE {self.regen['plane']} plane, regrow with "
                f"spec readout phi={self.regen['phi_readout']}")
        lines.append(
            f"  3. PRECONDITION: gap junctions >= {self.preconditions.get('gap_scale')} "
            f"(junction-carried spec read)")
        for k in self.checks:
            lines.append(f"  VERIFY: {k['what']} ({k['criterion']})")
        return "\n".join(lines)


def compile_anatomy(spec: AnatomySpec, n: int = 100) -> InterventionProgram:
    """Deterministic compilation: AnatomySpec -> InterventionProgram."""
    prog = InterventionProgram(spec_name=spec.spec_name)
    errs = spec.validate()
    if errs:
        prog.rejected = errs
        return prog

    # R1: identity zones -> sustained clamps over the rewrite window
    for z in spec.zones:
        i0, i1 = int(round(z.f0 * n)), int(round(z.f1 * n))
        prog.clamps.append({
            "zone": z.name, "i0": i0, "i1": max(i1, i0 + 1),
            "voltage": float(z.voltage), "hours": WINDOW_H,
        })

    # R2: trigger plane -> amputate + spec-reading regrow
    if spec.amputate_plane:
        prog.regen = {"plane": spec.amputate_plane, "cut_f": spec.cut_f,
                      "phi_readout": PHI_ADOPTED, "window_h": WINDOW_H}

    # R3: coupling precondition (the spec read is junction-carried)
    prog.preconditions = {"gap_scale": GJ_PRECONDITION,
                          "rationale": "M25/M28: the positional spec read "
                                       "runs through the junction network"}

    # verification criteria (what verify() will test)
    for z in spec.zones:
        prog.checks.append({
            "what": f"zone {z.name} holds {z.voltage:+.1f} mV",
            "criterion": f"|zone mean - {z.voltage}| <= 6.0 mV",
            "zone": (z.f0, z.f1), "voltage": z.voltage,
        })
    if spec.amputate_plane:
        prog.checks.append({
            "what": "regenerated tissue matches the spec (pattern error)",
            "criterion": "wt_pattern_error vs spec-derived target < 6.0 mV",
        })
    return prog


def execute_and_verify(prog: InterventionProgram, spec: AnatomySpec,
                       seed: int = 1, gap_scale: float | None = None,
                       collective_cls=None) -> dict:
    """Run the program in-sim and evaluate its own verification criteria."""
    from cultivation.bioelectric.collective import BioElectricCollective
    from cultivation.bioelectric.morphospace import (
        wildtype_target, head_likeness,
    )
    cls = collective_cls or BioElectricCollective
    gs = prog.preconditions.get("gap_scale", 1.0) \
        if gap_scale is None else gap_scale
    c = cls(n=100, seed=seed)
    c.gap_scale = float(gs)
    c.G = c.G0 * float(gs)
    c.deg = c.G.sum(axis=1)

    target = wildtype_target(100)
    for z in spec.zones:
        i0 = int(round(z.f0 * 100))
        i1 = max(int(round(z.f1 * 100)), i0 + 1)
        target[i0:i1] = z.voltage

    # R1: sustained clamps through the rewrite window
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=0.1)
    c.release_clamps()

    # R2: trigger the spec-reading regrow
    from experiments.exp32_m26_repairs import HEAD, TAILP, TRUNK
    planes = {
        "tail": [TAILP], "head": [HEAD], "trunk": [TRUNK],
        "head_tail": [TAILP, HEAD],
    }
    regen_meta = None
    if spec.amputate_plane:
        phi = prog.regen["phi_readout"]
        # R1' execution semantics: on the latching substrate the regen
        # uses the substrate's own anchor-inheriting regrow (the latch
        # carries positional memory; the phi readout is the plain-
        # substrate path).
        latching = hasattr(c, "theta_anchor")
        for plane in planes[spec.amputate_plane]:
            c.amputate(plane, wound_voltage=-30.0, blastema_theta=-40.0)
            if latching:
                c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6)
            else:
                c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6,
                         direction="both" if plane is TRUNK else "forward",
                         phi_readout=phi, spec_reanchor_p=1.0)
            regen_meta = {"plane": str(plane), "phi": phi,
                          "substrate": "latching" if latching else "plain"}
    c.run(15, dt=0.1)   # settle after regen (exp29 protocol tail)

    results = {"err_vs_spec_target": c.pattern_error(target),
               "final_mean_vmem": float(np.mean(c.V))}
    ok_all = True
    for k in prog.checks:
        if "zone" in k:
            i0 = int(round(k["zone"][0] * 100))
            i1 = max(int(round(k["zone"][1] * 100)), i0 + 1)
            zmean = float(np.mean(c.V[i0:i1]))
            ok = abs(zmean - k["voltage"]) <= 6.0
            results[k["what"]] = {"zone_mean": zmean, "ok": ok}
            ok_all &= ok
        elif "pattern_error" in k["criterion"]:
            ok = results["err_vs_spec_target"] < 6.0
            results[k["what"]] = {"err": results["err_vs_spec_target"],
                                  "ok": ok}
            ok_all &= ok
    results["program_verified"] = bool(ok_all and not prog.rejected)
    results["regen"] = regen_meta
    return results
