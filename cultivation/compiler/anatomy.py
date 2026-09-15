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

# R5 (substrate-aware partitioning, exp47): a target partition is
# compilable on a substrate iff its boundary-to-volume ratio (crossing
# edges / total edges) is <= R5_MAX. Calibration = exp43's measured
# attractor-existence signature (path 1.8 mV PASS, grid 5.6 mV PASS,
# random-3-regular 11.2 mV FAIL, scale-free 11.9 mV FAIL): the head|trunk
# partition's ratios are ~0.010 (path) and ~0.033 (grid) for the passing
# substrates vs ~0.38 (random-3) for the failing ones — R5_MAX=0.10 sits
# strictly between with margin on both sides (exp47 R5-G2). Literature:
# substrate-conditioned pattern support is expected (2026 hybrid framework;
# robustness as a design property, PMC38505634).
R5_MAX = 0.10


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
    somatic_latch: bool = False         # R1'': emit the latch-write step

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
    latch_write: list[dict] = field(default_factory=list)  # R1'' (v1)
    schedule: list[dict] = field(default_factory=list)  # R6 (v2): lab dosing schedule

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
        for st in self.schedule:
            lines.append(
                f"  SCHEDULE {st['step']}. {st['agent']}: {st['action']}"
                f" ({st['timing']}; {st['concentration_class']})")
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

    # R1'' (compiler v1, exp47): the LATCH-WRITE step. Per Pezzulo/Levin
    # 2017 the stored bioelectric gradient is what regeneration reads —
    # so the rewrite protocol must END with the stored gradient SET to
    # the target (the experimental 'reversal' is a deliberate state
    # write, not a wait). Emitted for every zone when the spec requests
    # the somatic latch substrate; execute_and_verify applies it after
    # the 24h window and before the trigger.
    prog.latch_write = []
    if spec.somatic_latch:
        for z in spec.zones:
            i0, i1 = int(round(z.f0 * n)), int(round(z.f1 * n))
            prog.latch_write.append({
                "zone": z.name, "i0": i0, "i1": max(i1, i0 + 1),
                "voltage": float(z.voltage),
            })
        prog.preconditions["somatic_latch"] = True
        prog.preconditions["latch_rationale"] = (
            "R1'': the stored gradient must hold the target — the "
            "window ends with the latch WRITTEN to the spec (exp47; "
            "Pezzulo/Levin 2017 cryptic-gradient semantics)")

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

    # R6 (compiler v2): the LAB-EXECUTABLE schedule — step-by-step
    # agents/timing/concentration CLASSES a real lab could translate.
    # Concentrations are emitted as CLASSES anchored to measured dose
    # axes (exp40's (cns, diffusion) grid; the record's octanol-class
    # baths), not invented numbers.
    step = 0
    if spec.somatic_latch:
        step += 1
        prog.schedule.append({
            "step": step, "agent": "Vmem clamp (ion-channel modulation)",
            "action": "hold spec zones at their target voltages",
            "timing": f"0-{WINDOW_H:.0f} h sustained",
            "concentration_class": "exp40 grid (cns,diffusion) per |delta| > 5 mV",
        })
        step += 1
        prog.schedule.append({
            "step": step, "agent": "somatic latch write (window end)",
            "action": "set stored gradient := spec in every zone",
            "timing": f"at {WINDOW_H:.0f} h, before the trigger",
            "concentration_class": "state write (no agent)",
        })
    step += 1
    prog.schedule.append({
        "step": step, "agent": "GJ health precondition",
        "action": "verify gap-junction conductance >= 1.0 (M25/M28)",
        "timing": "immediately before the trigger",
        "concentration_class": "octanol-free; heptanol-class bath ONLY if blockade arm",
    })
    step += 1
    if spec.amputate_plane:
        prog.schedule.append({
            "step": step, "agent": "trigger",
            "action": f"amputate {spec.amputate_plane} plane; regrow reads the spec",
            "timing": f"t = {WINDOW_H:.0f} h",
            "concentration_class": "none (mechanical)",
        })
    return prog


def substrate_partition_check(spec: AnatomySpec, adjacency: np.ndarray,
                              r5_max: float = R5_MAX) -> dict:
    """R5 (compiler v1, exp47): substrate-aware partitioning.

    The compiler is the SUBSTRATE ADAPTER (exp43): a target anatomy is
    compilable on a substrate only if the identity partition it defines
    is COHERENT with that substrate's connectivity — measured as the
    partition's boundary-to-volume ratio (crossing edges / total edges).
    exp43's measured attractor-existence signature is the calibration:
    path and 2D grid support the head|trunk partition; random-3-regular
    and scale-free do not (errors 11-12 mV vs 2-6 mV).

    Returns an audit-ready dict: ratio, counts, limit, and the compile
    decision. Called by the compiler when a substrate is declared; a
    refusal names the measured ratio and the limit (R4 discipline for
    substrates: refuse what the substrate cannot support).
    """
    n = adjacency.shape[0]
    identity = np.full(n, -1, dtype=int)   # -1 = unzoned (default identity)
    for k, z in enumerate(spec.zones):
        i0, i1 = int(round(z.f0 * n)), int(round(z.f1 * n))
        identity[i0:min(max(i1, i0 + 1), n)] = k
    total = int(np.sum(np.triu(adjacency, 1)))
    crossing = 0
    for i in range(n):
        for j in np.where(adjacency[i] > 0)[0]:
            if j > i and identity[i] != identity[j]:
                crossing += 1
    ratio = crossing / total if total else 0.0
    ok = ratio <= r5_max
    return {
        "substrate_compilable": bool(ok),
        "boundary_to_volume": round(ratio, 4),
        "crossing_edges": crossing, "total_edges": total,
        "r5_max": r5_max,
        "rationale": (
            "R5: the attractor must be coherent with the connectivity "
            "structure (exp43: mechanism universal, form "
            "substrate-conditioned)"),
    } if ok else {
        "substrate_compilable": bool(ok),
        "boundary_to_volume": round(ratio, 4),
        "crossing_edges": crossing, "total_edges": total,
        "r5_max": r5_max,
        "rationale": (
            f"R5 REFUSAL: partition b2v {ratio:.3f} > limit {r5_max} — "
            "this substrate cannot support the target partition "
            "(exp43 signature)"),
    }


def execute_and_verify(prog: InterventionProgram, spec: AnatomySpec,
                       seed: int = 1, gap_scale: float | None = None,
                       collective_cls=None,
                       latch_spec_blend: float = 1.0,
                       window_h: float | None = None) -> dict:
    """Run the program in-sim and evaluate its own verification criteria.

    latch_spec_blend (compiler v1, R2''): on the latching substrate the
    regeneration writes the blended identity into the latch,
    anchor <- (1-blend)*anchor_inherited + blend*spec[i]; blend=1.0 (the
    v1 adopted mapping) makes the regen READ the latch that R1'' has
    just written — the stored gradient carries the spec (Pezzulo/Levin
    2017). blend=0.0 reproduces the exp41 v0 latch behavior.

    window_h (compiler v2): the rewrite-window duration override for
    the MINIMUM-STEPS study; None keeps the v1 24 h window (bit-exact).
    The clamp entries state the compile-time window; the override only
    shortens how long the clamps actually hold before latch+trigger.
    """
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
    win = WINDOW_H if window_h is None else float(window_h)
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(win, dt=0.1)
    c.release_clamps()

    # R2: trigger the spec-reading regrow
    from experiments.exp32_m26_repairs import HEAD, TAILP, TRUNK
    planes = {
        "tail": [TAILP], "head": [HEAD], "trunk": [TRUNK],
        "head_tail": [TAILP, HEAD],
    }
    regen_meta = None
    latching = hasattr(c, "theta_anchor")
    if latching and prog.latch_write:
        # R1'' LATCH-WRITE: the window ends with the stored gradient SET
        # to the spec (the v0 latch only chased the clamps partway —
        # exp41's CP-G3' failure signature, zone means ~10 mV short).
        for lw in prog.latch_write:
            c.theta_anchor[lw["i0"]:lw["i1"]] = lw["voltage"]
    if spec.amputate_plane:
        phi = prog.regen["phi_readout"]
        # R1' execution semantics: on the latching substrate the regen
        # uses the substrate's own anchor-inheriting regrow; v1 (R2''):
        # the regen READS the latch that R1'' has written, blended with
        # the spec at latch_spec_blend (1.0 = the stored gradient IS the
        # spec — the 2017 cryptic-gradient semantics).
        for plane in planes[spec.amputate_plane]:
            c.amputate(plane, wound_voltage=-30.0, blastema_theta=-40.0)
            if latching:
                c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6,
                         spec=target, latch_spec_blend=latch_spec_blend)
            else:
                c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6,
                         direction="both" if plane is TRUNK else "forward",
                         phi_readout=phi, spec_reanchor_p=1.0)
            regen_meta = {"plane": str(plane), "phi": phi,
                          "substrate": "latching" if latching else "plain",
                          "latch_spec_blend": latch_spec_blend
                          if latching else None}
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


# ------------------------------------------------------------------ v2
def recut_stability(prog: InterventionProgram, spec: AnatomySpec,
                    seed: int = 1, generations: int = 100,
                    settle_h: float = 15.0) -> dict:
    """CP2 (compiler v2) — THE LATCH RE-READ PATH ACROSS GENERATIONS.

    After a verified program, repeatedly re-amputate the SAME plane and
    regrow with the latch-spec read (the v1 R2'' semantics). Each
    generation's regen REWRITES the latch inside the regen zone from the
    boundary anchor — the exp41-failure-structure question is whether
    that re-written latch HOLDS the spec (the stored gradient survives
    its own re-reads) or compounds drift.

    Returns the per-generation pattern error vs the spec target, the
    anchor drift in the regen zone, and the cycles-to-failure (err
    crossing 6.0 mV; None if the full horizon holds).
    """
    from cultivation.bioelectric.morpho_engineering import (
        LatchingCollective,
    )
    from experiments.exp32_m26_repairs import HEAD, TAILP, TRUNK
    from cultivation.bioelectric.morphospace import wildtype_target

    c = LatchingCollective(n=100, seed=seed)
    c.gap_scale = float(prog.preconditions.get("gap_scale", 1.0))
    c.G = c.G0 * c.gap_scale
    c.deg = c.G.sum(axis=1)

    target = wildtype_target(100)
    for z in spec.zones:
        i0 = int(round(z.f0 * 100))
        i1 = max(int(round(z.f1 * 100)), i0 + 1)
        target[i0:i1] = z.voltage

    # run the program once (verify semantics)
    for cl in prog.clamps:
        c.clamp(slice(cl["i0"], cl["i1"]), cl["voltage"])
    c.run(WINDOW_H, dt=0.1)
    c.release_clamps()
    if prog.latch_write:
        for lw in prog.latch_write:
            c.theta_anchor[lw["i0"]:lw["i1"]] = lw["voltage"]
    planes = {"tail": [TAILP], "head": [HEAD], "trunk": [TRUNK],
              "head_tail": [TAILP, HEAD]}
    if spec.amputate_plane:
        for plane in planes[spec.amputate_plane]:
            c.amputate(plane, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6,
                     spec=target, latch_spec_blend=1.0)
    c.run(settle_h, dt=0.1)

    errs, anchor_drift = [float(c.pattern_error(target))], []
    regen_zone = planes[spec.amputate_plane or "tail"][0]
    cycles_to_failure = None
    for gen in range(1, generations + 1):
        for plane in planes[spec.amputate_plane or "tail"]:
            c.amputate(plane, wound_voltage=-30.0, blastema_theta=-40.0)
            c.regrow(plane, cell_period=0.8, dt=0.1, noise=0.6,
                     spec=target, latch_spec_blend=1.0)
        c.run(settle_h, dt=0.1)
        e = float(c.pattern_error(target))
        ad = float(np.mean(np.abs(
            c.theta_anchor[regen_zone] - target[regen_zone])))
        errs.append(e)
        anchor_drift.append(ad)
        if cycles_to_failure is None and e >= 6.0:
            cycles_to_failure = gen
    return {
        "seed": seed,
        "err_generation_0": errs[0],
        "err_final": errs[-1],
        "max_err": max(errs),
        "anchor_drift_final": anchor_drift[-1] if anchor_drift else None,
        "anchor_drift_slope": (float(np.polyfit(
            np.arange(1, len(anchor_drift) + 1), anchor_drift, 1)[0])
            if len(anchor_drift) > 2 else None),
        "cycles_to_failure": cycles_to_failure,
        "errs_head": [round(e, 3) for e in errs[:10]],
        "errs_tail": [round(e, 3) for e in errs[-5:]],
    }
