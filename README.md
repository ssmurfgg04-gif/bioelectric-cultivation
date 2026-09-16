# bioelectric-cultivation

**A computational research framework for bioelectric morphogenesis, aging-as-attractor-degradation, and inverse design of bioelectric interventions.**

If the body runs software — a bioelectric control layer of membrane voltages coupled by gap junctions — then morphogenesis is what that software computes, aging is the slow corruption of the stored program, regeneration is a restore-from-backup, and cancer is a decode failure into a wrong attractor. This repository implements that framing as runnable code: coupled-ODE cell collectives with homeostatic target memory, an aging model (gap-junction decay + noise growth + target drift), an error-correcting "cultivation codec" on top, information-theoretic metrics (mutual information I(V;M), linear-Gaussian integrated information Φ), and inverse-design search for interventions.

The project follows a falsification-first methodology: every claim has an automated test that would break it.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  cultivation/bioelectric/   the physics of the control layer │
│    collective.py  N-cell gap-junction-coupled ODE sheet     │
│    aging.py       3-mechanism degradation (G, noise, target) │
│    morphospace.py targets, basins, polarity, amputation     │
│    fidelity.py    discrete-state pattern fidelity, regional  │
│                   jump corruption, organ-failure mortality,  │
│                   verification-gated channel therapy         │
├──────────────────────────────────────────────────────────────┤
│  cultivation/coding/        the error-correction isomorphism │
│    gf256.py reed_solomon.py  RS across spatial cell clusters │
│    belief_prop.py            gap-junction BP denoising       │
│    bio_channel.py            young/old channel presets       │
│    cultivation_codec.py      read → correct → write → repeat │
├──────────────────────────────────────────────────────────────┤
│  cultivation/information/   what the layer "knows"           │
│    mutual_info.py  I(V;M) estimation                        │
│    phi.py          linear-Gaussian Φ (Barrett & Seth 2011)   │
├──────────────────────────────────────────────────────────────┤
│  cultivation/neural/        the interface layer              │
│    ctrnn.py        continuous-time recurrent nets            │
│    connectome.py   real C. elegans gap-junction data         │
├──────────────────────────────────────────────────────────────┤
│  cultivation/inverse/       the engineering layer            │
│    mlp.py decoder.py   bioelectric-state → outcome model     │
│    cem.py              cross-entropy-method intervention search│
├──────────────────────────────────────────────────────────────┤
│  experiments/               the evidence                     │
│    exp1 regeneration memory   exp5 information metrics       │
│    exp2 cancer normalization  exp6 error-correction lifespan │
│    exp3 Gompertz derivation   exp7 sharded stress sweep      │
│    exp4 cross-species         exp8 pattern-fidelity gate     │
│    exp9 feasibility audits   aggregate.py                   │
├──────────────────────────────────────────────────────────────┤
│  tests/                     the falsification suite          │
│  docs/RESEARCH_MAP.md       the connected synthesis          │
└──────────────────────────────────────────────────────────────┘
```

## The isomorphism

| Neural network | Bioelectric cell collective | In this repo |
|---|---|---|
| activation $a_i$ | membrane voltage $V_i$ | `collective.V` |
| synaptic weight $w_{ij}$ | gap-junction conductance $G_{ij}$ | `collective.G` |
| activation function | ion-channel gating | intrinsic relaxation |
| plasticity $dw/dt$ | connexin remodeling | `aging` G-decay / repair |
| training target | morphological target $\theta^*$ | slow homeostatic variable `theta` |
| inference | morphogenesis | forward simulation |
| catastrophic forgetting | pattern instability / aging | `aging` target drift |
| network retraining | regeneration / reprogramming | `exp1`, `exp2` |

| DNA storage codec (helix-codec) | Bioelectric morphology |
|---|---|
| file to store | morphological target (body plan) |
| oligos | cell clusters |
| sequencing noise | ion-channel stochasticity |
| synthesis errors | wrong voltage states |
| RS across oligos | RS across spatial clusters |
| LDPC within oligo | gap-junction belief propagation |
| consensus reads | redundant cell consensus |
| channel aging | bioelectric aging |

## Core dynamics

$$\frac{dV_i}{dt} = \gamma(\theta_i - V_i) + \sum_j G_{ij}(t)\,(V_j - V_i) + \eta_i(t)$$
$$\frac{d\theta_i}{dt} = \varepsilon(V_i - \theta_i) + \mu \sum_j A_{ij}(\theta_j - \theta_i) + \xi_i(t)$$

$V_i$ is the fast bioelectric state; $\theta_i$ is the slow homeostatic "target memory" (cells genuinely re-set their resting potential via channel expression — this is the mechanism behind Levin's stable reprogramming results). The same $\varepsilon$ term that lets a 24h perturbation rewrite the target also produces aging drift under noise — reprogramming and aging are two regimes of one mechanism.

Aging: $G(t) = G_0 e^{-\lambda t}$ (gap-junction decay), $\sigma_\eta(t) = \sigma_0 e^{\kappa t}$ (noise growth), plus target diffusion and a senescence cascade (cells whose tracking error exceeds a threshold pin depolarized and drop out of the network, degrading connectivity for everyone else — compounding failure).

## Quickstart

```bash
pip install -r requirements.txt
python -m tests.run_tests                 # full falsification suite
python -m experiments.exp1_regeneration   # planarian memory repro
python -m experiments.exp3_gompertz       # Gompertz from first principles
python -m experiments.exp8_fidelity       # THE Level-3 gate experiment
python -m experiments.exp9_feasibility    # cultivation-tier physics audits
python -m experiments.exp7_stress --shard 0/4 --out results/   # sharded sweep
```

## Sharded stress sweeps on GitHub runners

`.github/workflows/sharded-sweep.yml` fans `exp7` across a 24-way matrix (max-parallel 20) and aggregates artifacts into `results/`. Trigger via Actions UI or API. `.github/workflows/helix-stress.yml` stress-tests the helix-codec repository (RS/LDPC/Viterbi under escalating error loads) on runners so no local CPU is burned.

## Results (the falsification ledger)

**Level 1 — reproducing known biology: 9/9 PASS.** Two-headed planarian reprogramming with memory across amputations + dose-response + GJ-block negative control (Durant et al. 2017 structure); the full cancer-normalization matrix including the long-range gap-junction requirement and the locked-driver boundary (Chernet & Levin 2015 structure).

**Level 2 — the aging hypothesis: 7 PASS + 5 diagnosed negatives (2 now resolved).**
- Gompertz-form mortality EMERGES and wins the pre-saturation window (all seeds); Weibull edges the full adult window; mean fitted beta across the 162-run sweep: **0.090/yr** — the empirical human range.
- Cross-species: Spearman **rho = 1.00** (mouse, rat, naked mole rat, human, bowhead; hydra negligible senescence by preset), robust to +-20% jitter. Documented limitation: Gompertz-family ratio compression (Strehler-Mildvan).
- I(V;M): **1.55 -> 0.83 bits** as the gap-junction denoiser degrades (aging = information loss, measured).
- Phi: peaks at intermediate coupling, ~0 for modular systems; **0.12 bits mean on real C. elegans gap-junction motifs** (Cook et al. 2019 connectome).
- Maintenance: error-corrected write-back extends median lifespan **x1.08-1.10** single-cohort, **x1.13 mean across the 162-run parameter sweep** (24 GitHub runners). One-shot mid-life correction gains nothing; sustained practice does.

**Level 3 — intervention discovery (pattern-fidelity mortality): THE GATE OPENED.**
- **T3.1b PASS — the gate that exp6's negative pre-registered:** under fidelity-dependent mortality, archive-verified maintenance beats consensus-only maintenance **x1.09**. Regional corruption (cluster jumps — the two-headed-worm mechanism) is invisible to consensus; only an archive-referenced decoder can detect it. The genome is biology's outer code; the bioelectric layer is the inner code that lost its archive; verification is what its absence costs.
- **Regeneration rejuvenates: x1.25** — the planarian strategy (Dai et al. 2025) reproduced; cycles must repeat because the channel engines are not reset.
- **The bioelectric aging clock: fidelity at age 30-60 predicts remaining lifespan (Spearman rho 0.39-0.45, p < 0.01)** — the model's cheapest decisive wet-lab prediction (voltage dyes + longitudinal planarian cohorts).
- **The two-bottleneck law:** pattern repair plateaus at the channel capacity cliff; connexin restoration helps when noise binds (x1.06) but is net-harmful when corruption binds (x0.94 vs codec — quarantine loss); even full regeneration is channel-limited (x0.77). Interventions must be diagnosed, not blindly applied.
- Verification pays in degraded channels (**x1.06**) via consensus-read verification + a write-precision gate that refuses reckless writes.

**Level 3F — feasibility audits (exp9): the arithmetic nobody ran.**
- Contact-range biofield effects: **real physics** (cardiac E-field at 1 cm = 10x the 333 V/m needed for a 5 mV cell-state flip) — testable with existing magnetometry.
- Organism-range passive biofields, Schumann resonance, macro telekinesis: **DEAD-AS-STATED** (10^5, 10^13, and 10^8-years-of-lifting-1-gram short, respectively).
- Selection vs energy: an amplified RNG bit is already macroscopic — the energy objection never applied to switch-flipping; the ~mW micro-PK ceiling is ~9 orders ABOVE a bioelectric state transition (1.25e-16 J). **If a consciousness-matter interface exists, the first place it could physically express is the bioelectric layer — the layer this repository models.**

Full ledger: `docs/FALSIFICATION.md` · the connected synthesis: `docs/RESEARCH_MAP.md` · dossier PDF in the release notes.

## The Tower (exp10-15): from the gate to an integrated stack

Five layers, each discovered and validated in its own phase, then composed
end-to-end on a corpus no phase ever saw:

| Layer | Phase | What it contributes | Result |
|---|---|---|---|
| L5 consciousness-body interface | exp12 | the retention physics that makes somatic memory a trusted write target: bistable, re-writable, hopping-bounded, decay-tolerant without reward | 16/16 criteria |
| L4 latching somatic memory | exp11 | written patterns persist indefinitely; novel morphologies (third eye, dual zone) engineered by discovered clamp protocols; amputation memory is local | 5/5 criteria |
| L3 CEM-discovered policy | exp10 | the intervention schedule itself, found by search under an honest procedure-risk cost model | 4/4 criteria |
| L2 verified codec | exp8 | consensus-then-archive maintenance — THE GATE | see Level 3 above |
| L1 fidelity-dependent mortality | exp8 | aging = pattern information loss | see Level 3 above |

**Phase A (exp11) — engineering new body plans.** CEM-discovered sparse voltage-clamp protocols reach a novel mid-trunk organ zone (third eye) at settled fidelity **0.96**, hold it after clamp release (decay < 0.05 over 500 free units), and carry it through partial amputation (novel identity recovers, with overshoot) but not full amputation — positional memory is local, exactly as pre-registered. Difficulty scales with novel-boundary count (Spearman rho > 0). The Levin anchor (two-headed) reproduces at 0.94.

**Phase B (exp12) — the consciousness-body interface.** A controller coupled to the collective's bioelectric state learns to hold a written target under a paired corruption stream: training transcends the reflex ceiling **x5**, coherent (structured) moves carry precision where random moves move only the mean, the incentive loop tracks a moving target, and — the Pezzulo 2021 test — **with the reward loop cut, retention plateaus above baseline rather than decaying to zero**: the somatic latch, not the learning loop, is the re-writable memory medium. Bistability confirmed by hysteresis (path-dependent terminal states), rewritability by the write-A/measure/write-B/measure/rewrite-A test, hopping bounded as Ryom 2021 predicts.

**Phase C (exp13) — the scaling laws.** The codec gate is a smooth monotone law, not a lucky parameter cell: gate value grows 1.25 -> 2.29 with regional corruption pressure (saturating quadratic, **R2 = 0.997**) and erodes 1.59 -> 1.13 with channel noise (linear, **R2 = 0.91**). Honest negatives: per-cell archive writes do NOT shift the channel-capacity cliff knee (only a small additive term); overshoot does not scale with latch strength (it is bounded by it — C4c).

**Phase D (exp14) — the integrated stack on held-out physics.** Composed on a corpus (kappa 0.017, lambda 0.026, jump 0.006, f_crit 0.655, seeds 51-53) that no phase tuned, searched, or validated on: **the gate transfers (x1.91)**, the frozen discovered policy beats no-intervention **x1.75**, the full stack runs at **x1.71** over the pre-gate baseline, and — the exp12 layer's signature — under passive policy decay (the noreward physics) the stack degrades **gracefully at exactly x1.00**: the latch carries what was written. Three honest negatives recorded: the discovered policy loses to the hand-built arm on the milder held-out regime (111 vs 124 — it was optimized under its own regime's constraints); grafting the latch onto the aging stack costs ~20% (the tower's open joint — the layers compose cleanly in the morphology domain, not yet in the aging domain); and the CEM-vs-GA benchmark (Hazan & Levin 2022's "first step" vs the next, 140 evals each, common random numbers) finds **no sample-efficiency separation** — the policy landscape has a broad attainable plateau (~94, +19% above the best hand-built policy) that uniform sampling reaches as fast as adaptive sampling. The honest claim: inverse design beats hand design; the algorithm choice barely matters on this landscape.

**Phase E (exp15) — the falsification controls.** Four controls that could have taken the tower down; 8/11 pre-registered criteria pass: (E1) **0 of 8** random policies beat the discovered one (mean 90.9 vs 111.2 — the win is searched structure); (E2) with the latch rate zeroed, the third-eye pattern relaxes **exactly to the null baseline** (0.86) while the native latch holds 0.96 — the memory, not clamp residue, carries novel morphology; (E3) with the genomic archive permuted (mortality still scored against the true pattern; the none-arm sanity check confirms default physics is untouched), verified maintenance **collapses below doing nothing** (48.3 vs 63.5) — the archive is load-bearing, and a wrong archive is worse than no archive; (E4) cross-species protocol transfer degrades without annihilating (0.69/0.79) and — the finding the pre-registered inertness criterion missed — **the intervention's sign flips**: the wrong protocol actively overwrites correct cells (-0.18 below null), the computational analog of off-target reprogramming hazard.

One-image summary: `results/figures/fig16_tower_summary.png` (policy / scaling law / novel morphology / retention). Per-phase figures: `results/figures/fig10-fig15`.

## D3 resolved (exp16): the write semantics of death

The tower's open joint — the latch layer fought the codec's writes on
senesced cells (x0.80) — is closed, and the closure turned the star question
("when a cell dies, is the pattern lost, or written somewhere?") into four
competing, tested write semantics (`cultivation/bioelectric/senescence_semantics.py`,
grounded in the 2026-09 literature sweep in `research/d3_sweep/`):

- **The matched-channel law (the engineering fix).** The v1 latch's memory
  pin ran ~100x the bandwidth of the junction channel it backed up — a
  dominant "backup" that fights the primary channel and chronically
  inflates the senescence hazard. The v2 latch forms memories fast
  (alpha ~ 20/yr) and pulls weakly (k = 0.25/yr, calibrated by the C2
  sweep: composition x1.000 at 0.25 degrading monotonically to x0.881 at
  50). **Composition with codec maintenance: x1.000**; under the
  biologically-corrected death semantics (bystander broadcast): x0.991.
  The somatic memory's job is to REMEMBER, not to ENFORCE.
- **The star question, answered in this model's currency.** Four semantics
  tested against the novel-pattern information ledger: erasure 0.535,
  transcription 0.534 (identical — the informative negative), stasis 0.560,
  broadcast 0.560. The naive hypothesis — death is a transcription event,
  the self moves cell-to-cell — fails because single-cell memory copies
  are outvoted by the collective consensus within weeks. **The pattern is
  an attractor of collective dynamics, not a property of individual
  cells**: no single death can erase it (redundancy — death IS a
  transition), and no single transcription can move it (the self is not
  cell-local). The pattern survives through three redundant carriers:
  collective state, frozen stasis anchors (+2.5% vs erasure), and the
  genomic archive.
- **The bystander effect is demographically silent.** The broadcast (the
  literature's mechanism: injury depolarization waves, gap-junction
  bystander effects, SASP spreading) shows dose-dependent excess
  senescence and a lethal interaction with junction decay (perturbations
  linger when healing coupling is gone), yet the four semantics sit within
  0.7 yr of each other in median lifespan: the death-write decides WHERE
  the pattern lives, not HOW LONG the organism lives.

Figure: `results/figures/fig17_d3_semantics.png`. Full ledger:
`docs/FALSIFICATION.md` Level 5.

## D3b (exp17): the anchored target — keeping a written body plan alive

The D3 answer left one gap: the codec is archive-referenced, so a novel
morphology (existing only in somatic memory) reads "wrong" every cycle and
gets repaired to factory default — verified maintenance actively erases
engineered morphologies (I_recoverable@60: 0.100 vs 0.584 unmaintained;
and the erasure arm's median lifespan RISES — the hazard is informational,
not mortal). The fix is the biological target-morphology semantics, built
as a THREE-TIER memory (`FidelityCodec(target_source="anchored")` +
`protect_written=True`):

1. **Protected tier** — deliberate writes (clamp protocols, codec repairs)
   mark their cells; those anchors do not track consensus: bistable
   somatic memories (Pezzulo & Levin 2021). Result: the written pattern
   holds at **0.91 recoverable at age 60, 0.90 at age 100**, with median
   lifespan +20% over no maintenance — a novel body plan survives a
   century of aging, death broadcasts, and its own maintenance cycles.
2. **Consensus tier** — never-written cells' anchors track the local
   collective (the D3 redundancy carrier).
3. **Genomic archive** — the fallback when a cluster's memory is
   internally incoherent (corrupted), preserving the exp6/exp8 verified
   semantics exactly.

Honest negatives on the way (FALSIFICATION.md D5-D8): a tracker memory
referenced by its own codec faithfully maintains DRIFT (0.126 — the
feedback-loop trap), and a coherent wrong memory is maintained with full
conviction (0.000 — memory correctness is load-bearing, E3's analog).

Figure: `results/figures/fig18_anchored_target.png`.

## The no-wetlab validation layer — EXECUTED (exp18)

`cultivation/validation/vmem_inference.py` connects the public planarian
single-cell atlases to the model: ion-transporter expression -> GHK resting
potential -> the worm's predicted bioelectric map -> four falsifiable,
literature-cited predictions. **The atlases were ingested this session**:
PSCA (21,612 cells x 28,066 genes) and Fincher (50,456 cells x 26,561
genes), joined to curated ion-transporter gene families via the planosphere
Rosetta Stone + AHRD annotations (validated 3/3 against published
Smed-TRPM gene IDs). Results (`experiments/exp18_psca_ingest.py`):
**V1 CONFIRMED on both atlases** — neoblasts rank among the most
hyperpolarized cell types (3/10 and 1/7; weight-jackknife 18-20/20) —
while V2 (muscle form) is refuted, V3 (phagocyte depolarization) is split
(the better-powered atlas supports it), and V4's atlas-proxy is falsified
with mechanism (innexin co-expression correlates with inferred Vm; the
physiological coupling claim needs spatial data). The method is
rank-robust for stemness gradients, not absolute-Vm: gating is invisible
to transcriptomes. Full ledger: `docs/FALSIFICATION.md` Level 5.

## The century-hold policy (exp19)

With the anchored stack holding novel targets (exp17), the CEM search was
re-run under a new objective: not "reach the target" but **"hold the
target over a century"** (fitness = mean over ages 30-100 of
alive-fraction x pattern-recoverability; death is ultimate pattern loss).
`experiments/exp19_anchored_cem.py`: the search beats no-maintenance by
+23% held-out, **rediscovers the matched-channel law from an uninformative
start** (k_anchor -> 0.33: the exp16 calibration emerges as a search
result), finds a hold-optimum distinct from the reach-optimum (write in
adolescence, start maintenance a decade later, dense but low-amplitude),
and honestly fails to beat the hand-built exp17 policy (+1.2%) — the
century-hold landscape is a broad plateau (all eight single-dimension
ablations shift hold by <= 0.01).

## The fidelity-clock wet-lab program (pre-registered)

`docs/FIDELITY_CLOCK.md` — the experiment series D3's resolution
unblocked: FC1 the cross-sectional clock (does spatial Vmem fidelity
decline with age), FC2 the prognosis test (does baseline fidelity predict
regeneration and survival — computational rho 0.39-0.45), FC3 the
quarantine mechanism (innexin RNAi phenocopy + bystander dye-coupling),
FC4 the protected tier in tissue (written Vmem patterns persist >= 7 days,
require junction integrity, resist injury-mimetic overwrite), FC5 the
clock reset (regeneration cycles as fidelity re-derivation). Every stage
carries an explicit kills-row. Measurement uses established methods only
(DiBAC4(3) live imaging per the published planarian protocol, WISH/smFISH,
scrape-load dye coupling).

## M17: the sloppiness audit + spatial data + the outcome corpus

Three moves, in the search-first spirit. (1) **The audit**
(`docs/SLOPPINESS.md`): no uncertainty quantification anywhere (S1),
unsmoothed CEM (S2), no stagnation restarts (S3), dead code and a blank
figure panel in exp19 (S4), tie-blind Spearman (S5), coarse V1 ranks
(S6), ablation seed reuse (S7), untested permeability floors (S8).
Fixes: `cultivation/validation/stats.py` (permutation p-values, bootstrap
CIs, mean-SE, floor sensitivity), CEM smoothing + restart flags (with
bit-exact None backdoor, unit-tested), exp19 S4 repairs. (2) **exp20 —
PRISTA4D** (Han 2026, GigaScience; 0/12/36 hpa spatial matrices, gene
bridge via the Rosetta Stone 2020): V1 PASSES in a third modality
(neoblast 3/31 spatial types); the spatial forms of V3 and V4 are
honestly REFUTED at the family-expression level — the injury transient
and junction-smoothness clauses now require measurement, sharpening
docs/FIDELITY_CLOCK.md from "preferred" to "necessary". (3) **exp21 —
PlanformDB** (Lobo 2013; 1,716 recorded experiments, penetrance-weighted):
cutting < ion < morphogen < other-RNAi abnormality ordering confirmed
(PB0), the STRONG junction-dominance claim refuted at ~3-study effective
power (PB1), bioelectric-not-above-morphogen bounded (PB2), graded
penetrance not the corpus norm (PB3). The junction claim is now
explicitly weak-form: necessary, not uniquely disruptive.

Also this session: SakanaAI's AI-Scientist installed and trialed on the
stack (OpenAI-compatible z-ai proxy; idea generation produced 18
candidate maintenance-policy experiments; the autonomous coding loop
correctly reproduced baselines and hit — and usefully exposed — the
single-zone `pattern_ledger` API limit blocking multi-pattern research;
full writeup stage rate-limited by Semantic Scholar).

## M18: exp23 — multi-pattern allocation (the AI-Scientist's best idea, cashed in)

The AI-Scientist trial's top-scored idea (multi-pattern maintenance),
unblocked by the multi-zone `pattern_ledgers` API it itself forced into
existence. Three competing novel patterns (stable / volatile /
high-turnover physics, cluster-aligned scrambled zones) + the birth
pattern share ONE anchored+protected codec budget; the budget (1/2/4/6
cells/cycle) is the scarcity dial; allocation policies (balanced,
fixed-priority, severity-weighted, critical-threshold) compete against
the status-quo cell-order allocation. K=200, 120yr, seeds 21-23, 5
pre-registered criteria, bootstrap CIs, alive-only ledgers, a bit-exact
in-session replication of exp17's anchored_protected arm (solo17:
median 73.8 yr, I_rec@60 0.907 — EXACTLY the published values).

**The honest outcome is a negative with a mechanism.** E1: the
competition cost on the volatile pattern is real but small (0.02 at
budget 1, gone by budget 6) — expression capacity is effectively
per-pattern at planarian scale. E2 REFUTED: no allocation policy beats
the status quo anywhere (policy spread 0.02). E3 PASS (the load-bearing
result): physics dominates policy by 20x — the high-turnover pattern's
deficit is a death-restoration EQUILIBRIUM set by its own hazard rate;
among living individuals its expression is fine (0.670), its all-K
deficit is mortality selection. E4: multi-pattern maintenance still
pays at every budget for every real policy (median 51.5-71.8 vs 49.0
unmaintained). **The two-layer capacity finding: the protected memory
tier stores all three written patterns for free (I_anchor = 1.000 with
zero maintenance) — storage is per-pattern and free, expression (I_V)
is the budget-bound scarce resource.** "Memory capacity" claims must
say which layer they mean. New APIs: per-cluster `jump_mult`, per-cell
`hazard_boost`, and `FidelityCodec.maintain(alloc=...)` (four policies,
unit-tested, bit-exact default path). 10 new unit tests (50 total).

## M19: the FIDELITY_CLOCK sharpened — layer-explicit, spatially honest

FC1 (and the series around it) re-registered against everything the
computational stack now actually knows, every change tagged (M17)/(M18)
inline — nothing silently edited. The sharpening, clause by clause:
**(1) the two-layer capacity law (exp23)** — the protected tier stores
written patterns for free (I_anchor = 1.000 unmaintained) while the
working state is the budget-bound decaying layer; DiBAC reads the
working state, so the fidelity clock is a claim about the EXPRESSION
layer, and the doc now says so before anyone measures the wrong thing.
**(2) FC1d (new, from exp23's equilibrium law)** — regional fidelity
deficits should ORDER BY regional turnover burden (death-restoration
equilibrium); uniform decline kills the model's aging mechanism.
**(3) FC1e + the measurement table (from exp20's V4s refutation)** —
functional dye coupling is co-measured in the SAME animals; the
coupling-to-smoothness relationship is a measured outcome, not an
imported assumption; innexin-expression maps retained only as the
expected-to-disagree correlate. **(4) A positive-control gate (from
V1s)** — neoblast-rich regions must read hyperpolarized in the same
DiBAC maps BEFORE cohort labels unblind; a pipeline that cannot see the
one spatial Vm prediction that survived screening is broken, not
negative. **(5) FC2d (from V3s)** — the fast injury transient is
explicitly out of scope for DiBAC and assigned to latency surrogates /
future GEVI collaborators, so nobody reads silence as refutation.
**(6) FC4d (new, from exp23 E1)** — two simultaneous ectopic writes
should show little interference (free storage layer); interference
would mean tissue memory capacity is shared in a way the model's
protected tier is not — the most informative possible failure. The
falsification table carries three new kill-rows; the two-week protocol
gains the positive-control gate, the coupling co-measurement pilot, and
per-region decomposition from day one.

## M20: exp24 — potentiation vs the equilibrium (the AI-Scientist's idea #2: a deep negative)

Can jump-probability reduction break the death-restoration equilibrium
that budget allocation couldn't move? The AI-Scientist's
memory-enhancement protocol #3 (reduce the jump probability of
freshly-corrected clusters) landed as a bit-exact-when-unused stack hook
(`potentiate()` / `_pot_until`, golden-tested on the active path too)
and was executed with pre-registered criteria P1-P7 across factor, window,
placement, and permanence. **The answer is no — and the no is structural:
even PERMANENT potentiation at 47% coverage moves the volatile pattern's
working state by +0.006 (bar: 0.046).** The mechanism of the failure is
legible: potentiation is correction-coupled, so it protects exactly the
clusters maintenance already keeps right, while the deficit lives in the
uncorrected tail and in mortality selection — the equilibrium now proven
immovable from BOTH the restoration side (exp23 allocation) and the
corruption side (exp24 potentiation), which is precisely FC1d's wager.
The supporting cast: random placement does nothing (gating real but
moot), the pattern dissociation confirms the two-bottleneck structure
(jump-axis help orders B > A > C), and the lifespan window effect is
NON-MONOTONE — transient windows add 1-2yr, permanent protection COSTS
5.7yr of median life (a frozen-protection mortality hazard recorded as
an open mechanistic tendril). Bit-exact regression vs exp23 held (plain
arm = exp23's default, exactly). 57 unit tests total.

## M21: exp25 — the century-hold policy vs competition (the all-pass stress test)

exp19's CEM-discovered 8-dim century-hold policy (budget 9, period 2.5,
start 31.5, k_anchor 0.326, unverified boost) transplanted into exp23's
competing-memory world, against the hand policy, both solo and in
competition, plus a budget-clamped stress arm and a bit-exact status-quo
anchor. **All five criteria PASS — and the surprise is the size: under
competition the discovered policy's hold 0.625 crushes HAND's 0.500
(+0.125, +14.4yr median) even while paying 2.3x the procedure risk,
whereas in exp19's single-pattern world the same policy had failed to
beat HAND by 1.2%.** Single-pattern benchmarks under-estimate policies
that must serve multi-pattern reality: the searched dimensions (cadence,
budget, write timing) are exactly the ones competition punishes. The
equilibrium law survived a policy it had never seen (A > B > C ordering
invariant under weak-pull + boost), and the schedule kept its edge at
the starved b2 budget (+0.067) — the advantage is the schedule, not
channel richness. A first 105yr pass was rejected for pure
survivor-censoring artifacts in death-age medians (trajectories
bit-identical, medians not) and re-run at exp23's 120yr convention —
the honest re-run is recorded in the module docstring.

## M23: exp26 — equilibrium attribution (the balance point taken apart)

The user's move after both edge attacks failed: stop attacking the
death-restoration equilibrium, take it apart. 24 arms on exp23's exact
geometry swept every primitive class — substrate, restoration, death
channels, zone coupling, channel noise, and a new architecture axis
(cluster granularity, n_clusters 4/12/20 via a bit-exact constructor
hook) — plus a four-arm flux-composite compensation protocol and a new
corruption-source instrument (per-cluster jump timestamps + per-cell
repair timestamps; every wrong cell at ledger age classified
senescence / jump / non-jump). **The verdict rewrites the story: the
equilibrium is made of SENESCENCE, not jumps** — B's 20.5% wrong cells
at 60 are 15.4% senescence / 2.0% jump / 3.0% other; C's are 17.9% /
0.3%. That is why exp23's allocation (re-slicing a budget whose binding
consumer is senesced-cluster repair, and which SATURATES at b6: the
b6->b12 elasticity is +0.04 vs +0.27 below) and exp24's potentiation
(protecting a 2% corruption channel — its +0.0056 delta is now
postdicted to the third decimal by the instrumented share x 0.75 x
0.47 coverage = +0.0072) both failed. The levers that DO move it:
**cluster granularity (the architecture answer: arch4 B 0.645 vs arch20
B 0.819, a 0.174 swing — a senesced cluster costs cluster_len budget
cells to repair, so storage granularity is the exchange rate between
senescence burden and repair capacity), channel noise (the capacity
cliff, elasticity -0.37), and the death channels (k_fail=0 lifts B
+0.036 and median +17yr).** The flux-ratio conservation law is
falsified as a complete description (EQ1a NEGATIVE) with a beautiful
dissociation: the four Phi-equal compensation arms restore ALIVE-only
fidelity above default (0.905-0.921 vs 0.876) while their all-K ledger
collapses (0.644-0.743) — the balance point is a two-term object,
alive-state balance x death-timing mixture, and death (medians 28-47 vs
71.8) freezes corruption into the ledger. Zone coupling is real and
large (EQ6 NEGATIVE: C's hazard 8x crushes B to 0.572 through shared
budget demand and organ-failure death timing — exp23's
"competition-invisible-at-b6" was an allocation statement, not a
physics one). Default arm bit-exact vs exp23 (R PASS); 7 new unit
tests (64 total, all green).

## M24: exp28 — CEM search under competition (the benchmark lesson, sealed)

The direct sequel to exp25: if the transplanted century-hold policy won
under competition, re-run the CEM SEARCH ITSELF with fitness evaluated
in the competing-memory world. Same 8-dim space, fresh search seeds, and
a held-out eval ported line-faithful from exp25 (regression anchor:
bit-exact, |delta| = 0.00e+00). **All seven criteria PASS, and the
robustness reading dies: the competitively optimal policy is a DIFFERENT
policy (write_age 20.0 vs 14.5, budget 6 vs 9) and a BETTER one — hold
0.683 vs the transplant's 0.625 (+0.058, ~3x the pre-registered bar),
median 79.7 vs 70.6yr, every seed separated.** The divergence is legible
against exp26's elasticity map: the shared budget saturates at b6, and
the blind search independently landed exactly on the saturation knee —
budget 6 — while starting maintenance earlier (25.75 vs 31.5), slowing
the cadence, and leaning 2x harder on the procedure-free unverified
boost channel. It wins with FEWER repair writes (17,139 vs 19,367,
-11.5%): the competitive optimum is a schedule, not more therapy, and
the starvation gap widens (b2 arms: 0.557 vs 0.421 — disc28 at budget 2
nearly matches disc19 at budget 9). The matched-channel weak-pull law is
rediscovered a THIRD independent time (k_anchor 0.128), interiority
survives, and exp23's stable-zone-on-top ordering holds — with the
honest sub-structure that the B/C order below A is policy-sensitive.
Benchmark discipline sealed into the ledger: evaluating policies in an
easier world than deployment under-estimates them by enough that
re-searching in the deployment world pays for itself.

## M25: exp29 + exp30 — night one: the record repairs the model, the search is certified exhausted

The first full overnight run of the DeepScientist quest
(docs/QUEST_STAGE2_VALIDATION.md), two threads, executed end-to-end.

Thread 1 — **exp29, the Stage 2 repair.** exp27's refutation became a repair
work order: PlanformDB says innexin loss must corrupt regeneration, but the
model regenerated NORMALLY with junctions blocked (2.87 mV) — regeneration
was junction-blind (cell-autonomous pattern extension, un-gated theta
diffusion). Two additive changes in `collective.py`, both bit-exact at full
coupling: M1 blastema readout through the junction network (under blockade a
committing cell falls back to the wound default plus a broad fate-axis
guess, spread 18 mV); M2 pattern propagation is junction-carried (theta
diffusion scales with gap_scale). Full test suite green before and after;
cutting arm bit-exact (3.16 == 3.16). exp27 re-run UNCHANGED: **S2P1 flips**
(innexin_sustained 2.87 -> 6.03 mV) with all controls intact — and the
repair emits two NEW testable predictions: monotone dose-response of
regeneration corruption under partial knockdown (3.28 / 3.93 / 4.54 / 6.03
mV at gap 1.0 / 0.5 / 0.25 / 0.05) and endogenous graded penetrance (1/3
seeds abnormal at full blockade) — the mixed outcomes the record actually
shows. Lesson sealed into the ledger: a refutation against published data
is a model-repair work order, not an embarrassment.

Thread 2 — **exp30, the CEM continuation.** exp28's checkpoint resumed
EXACTLY (mu/sigma/best/rng state) for 10 more iterations at protocol.
Search-world hold improved 0.7180 -> 0.7404, but held-out the continued
best is 0.6907 vs disc28's 0.6828 (+0.0079, under the +0.02 bar): **X1
REFUTED — disc28 is certified at (or within 0.02 of) the competitive
optimum**, and the search-side gain was mostly search-seed overfit. The
+0.008 and median 79.7 -> 81.6yr are kept (free, from the preserved
checkpoint); the re-search question is closed at this protocol. Harness
verified end-to-end: disc28 reproduces exp28's published 0.683 exactly
through the resumed path.

The night log starts the memory-carryover wire: per-run lessons for night
two live in docs/NIGHT_LOG.md, not in any chat.

## Research dossier

`research/` contains the verified literature (bioelectric morphogenesis, IIT, aging theory, Chinese research landscape) with DOIs verified against Crossref/PubMed responses, plus real C. elegans connectome data (OpenWorm; Cook et al. 2019).

## License

MIT.

## M26: exp31 — night two: the slice widens, the record sharpens the repair list

QUEST tasks 3-4 delivered: per-experiment amputation planes
(`experiments/planform_mining.py` — curated-name taxonomy: head/tail/trunk/
head_tail/crosspiece-with-cut-position/graft/irr/lateral/none), the
GJ-blocker drug experiments folded into the junction slice (octanol/
heptanol/hexanol -> innexin protocol; 23 drug + 9 RNAi experiments), the
AP-polarity morphogen subclass split out (wnt/beta-catenin/apc/axin, 143
experiments), and one additive bit-exact-at-default model parameter:
`regrow(direction='backward')` — a head amputation's blastema reads the
trunk boundary behind it (suite green; exp29 controls re-verified bit-exact
this session).

31 arms x 3 seeds against 1,462 outcome-bearing experiments, protocol
coverage 0.84, thresholds untouched. Scoreboard (results/
exp31_stage2_widened.json, ledger L14):

- **S2W1 PASS** — tail-plane bioelectric ordering holds on the widened
  slice: sim pooled bioelectric 0.44 vs cutting 0.00; recorded 0.535 vs
  0.367. The exp29 repair generalizes.
- **S2W7 (exploratory) PASS** — first graded per-experiment plane
  prediction: recorded abnormality rises toward anterior crosspiece cuts
  (0.520 at f<=0.25 vs 0.266 at f>0.75; rho=-0.164, p=0.043, n=153) —
  same direction as the sim, half the penetrance.
- **S2W2 REFUTED** — the model overshoots anterior crosspieces (1.00 vs
  recorded 0.52): chain inheritance has no length gradient. M26 candidate:
  distance-decaying boundary readout.
- **S2W3 REFUTED (criterion wrong-bio, model right)** — the record says
  AP-morphogen loss is plane-invariant (head 0.640 ~ tail 0.642), exactly
  the sim's posterior-re-specification behavior; the pre-registered
  specificity clause assumed tail-wound-only. Re-registered as S2W3b for
  night three — never silently swapped.
- **S2W4 REFUTED** — the model's ion-channel protocol (gamma x0.5, noise
  x3) produces ZERO regeneration corruption while junction loss produces
  0.67; the record has them comparable (0.45 vs 0.41). The junction >>
  channel asymmetry is a model artifact. M26 candidate: Vmem-gated
  blastema commitment (channel state should widen the identity guess the
  way junction state does).
- **S2W5 PASS** — restored-block and intact-baseline controls all clean.

Night-three queue: S2W3b re-registration, M26 mechanism candidates
(length-gradient readout, Vmem-gated commitment, posterior-face
regeneration), dose-resolved innexin literature check against S2R3's
monotone prediction, and the recorded-NO-data novel-prediction sweep
(QUEST task 6).

## M27: exp32 — night three: one repair adopted, two sharpened, one criterion re-registered

Night three delivered the M26 candidates as pre-registered gates
(`experiments/exp32_m26_repairs.py`, ledger L15). Model state: `regrow()`
now speaks two-face regeneration — `direction='both'` heals mid-body
removals from both wound faces (two independent blastemas), additively,
bit-exact at default (exp29 controls re-verified to 1e-9 before the run;
full suite green).

- **M26C ADOPTED** — two-face trunk regeneration: wnt_trunk@both 1.00,
  apc_trunk@both 1.00 (recorded 0.768); cutting_trunk@both 0.00 (recorded
  0.308). The recorded two-headed/two-tailed phenotypes are reachable.
- **S2W3b PASS x3** — the re-registered morphogen criterion
  (plane-INVARIANCE, not plane-gradient) passes on both sides: recorded
  spread 0.132 <= 0.15; pooled morphogen 0.724 > cutting 0.512; sim
  wnt_tail == wnt_trunk@both == 1.00.
- **M26A REFUTED as implemented** — local linear extrapolation is a no-op
  on head-only fragments (slope ~0): cross_a stays 1.00 vs recorded 0.52.
  M27 candidate: saturated extrapolation clipped to the fragment's own
  identity repertoire + graded penetrance.
- **M26B REFUTED as implemented** — i.i.d. commitment noise (cns=3)
  averages out across the segment (err 2.9 -> 4.09 mV, rate still 0.00 vs
  recorded 0.45). M27 candidate: chain-accumulating commitment diffusion
  (sd ~ sqrt(d)), matching how blastema commitment error compounds.

Process notes recorded in the ledger: a 15h post-regen protocol drift
was caught by the bit-exactness gates (innexin 0.67 -> 0.33) and
corrected before any verdict was recorded — the gates did their job.

Remaining night-three queue: dose-resolved innexin literature check
(S2R3), recorded-NO-data novel-prediction sweep (QUEST task 6), and the
DeepScientist zai-runner wiring (branch `zai-runner-wiring` on the fork;
doctor green is quota-gated on the z-ai backend).

## M27 addendum: exp33 — the dose axis the DB actually has (S2R3a unresolved, honestly)

PlanformDB 2.5.0 carries no drug concentrations — but 45 GJ-blocker rows
carry exposure timing. The M25 mechanism's per-experiment restoration
prediction (washout-before-regen recovers, S2C logic) went the WRONG way
at n=1 on the critical arm (washout 0.365/n=6 vs regen-covered 0.000/n=1)
— registered as REFUTED-as-registered, downgraded to UNRESOLVED on power
+ semantics grounds (ledger L16). The Oviedo 2010 octanol pulse ladder
(0.13–3h) is RegenPeriod=0 in the DB — no regeneration outcome recorded.
S2R3's monotone dose-response prediction remains UNTESTED (not
falsified); next step is primary-literature extraction (S2R3c).

## M28 (candidate registered): exp34 — chain commitment diffusion adopted; the length-gradient problem is structural

- **M27B ADOPTED** — chain-accumulating commitment diffusion
  (`commitment_diffusion`): identity noise random-walks along the chain
  and compounds (sd ~ diffusion*sqrt(d)). ion_channel_tail 0.00 -> 1.00;
  ion pooled 0.665 ~ junction 0.67 (record: 0.45 vs 0.41) — the S2W4
  junction>>channel artifact is resolved. Channel slice now needs
  penetrance dampening (sim 1.00 vs recorded 0.45), not mechanism.
- **M27A REFUTED (structural)** — whole-fragment secant + identity-
  repertoire clip leaves cross_a at 1.00: the head plateau dominates the
  fragment's stored theta; the tail-ward trend was amputated away. No
  stored-pattern readout can recover what the record (0.52) shows head
  fragments regenerate. Registered M28 candidate: DUAL-FIELD
  architecture — theta (expression) + phi (positional map), the model-
  level form of pattern-memory vs positional-control distinctions.
- Ledger L17; suite green; exp29/exp31 controls bit-exact throughout.

## M28 addendum: exp35 — QUEST task 6 complete (novel-prediction registry + two plane-awareness candidates)

Forward deposits for every empty runnable cell (the sharp one:
morphogen|crosspiece 0.00 — removing the re-specified territory should
fully compensate wnt loss), plus first per-plane compares the model had
never faced: innexin|head (record 0.00 vs sim 1.00 — head-specific
protection under junction loss) and ion_channel|trunk (record 0.46 vs
sim 0.00 — plane-sensitive calibration). Both feed the M28 upgrade.
research/NOVEL_PREDICTIONS.md + ledger L18.

## M29: exp36 — the dual-field layer lands: crosspiece refutation resolved, penetrance binary

M28 implemented: `phi_spec` (identity-at-coordinate, captured at pattern
set — D3's distributed memory made operational) + `regrow(phi_readout=)`
blending chain inheritance with the spec, junction-carried (M25-
consistent), bit-exact at default. Result: cutting_cross_a 1.00 -> 0.00
with ZERO collateral (tail/head/trunk/restored all 0.00 at every scan
value; innexin rate preserved) — the S2W2 overshoot is resolved at the
mechanism level, answering exp34's structural diagnosis (the map is a
separate distributed layer, not a readout of theta). Residual recorded
honestly: the model's penetrance is binary (no phi value seed-splits
cross_a), the record's is graded (0.52) — night-five candidate: a
stochastic spec-expression layer on top (mechanism untouched). Ledger
L19; adopted mapping candidate phi_readout=0.75.

## M30: exp38 — stochastic spec-expression: per-cell REFUTED (the chain re-carries the spec), regenerate-level re-anchoring splits seeds but flips a marginal innexin seed — not adopted

The L19 penetrance residual attacked with two stochastic units.
Registered per-cell Bernoulli: REFUTED at every p — the chain
RE-CARRIES the spec blend (each committed cell writes its blended
value; the next inherits it), so expression failures cannot accumulate;
one expressing cell seeds the whole regenerate. That is ALSO why the
phi transition is sharp: the chain is an amplifier, not an averager.
Amended per-blastema re-anchoring (spec_reanchor_p): seed-splitting
PASSES (q=0.55 -> cross_a 0.67, closest to recorded 0.52 at 3-seed
grain), collateral lock PASS, bins-unchanged PASS — but the anchor
draw shifts the RNG stream under blockade and flips the
threshold-marginal innexin seed (drift 1.34 mV, within tolerance, rate
off 2/3): NOT adopted — a fix that flips a previously-PASS criterion
is not a fix. M31 registered: anchor availability as STORED FRAGMENT
HISTORY (per-cell, captured at pattern set — stream-neutral by
construction). Ledger L20.

## exp37 — the full-corpus sweep (QUEST task 4 complete): 1,029/1,462 experiments mapped per-experiment

The class-level pilot became a per-experiment instrument: every
outcome-bearing PlanformDB experiment mapped to (class protocol, plane,
recorded cut fraction), 36 unique arms at the ADOPTED model state.
Coverage 0.704 PASS; plane ordering rho=+0.80 PASS; controls bit-exact
PASS. Class ordering REFUTED (other_rnai n=513: recorded 0.80 vs sim
0.00 — no gene-expression layer + class-dependent selection bias) and
absolute MAE REFUTED (0.595) with a SYMMETRIC signature: no-perturbation
classes undershoot (+0.80/+0.42), perturbation classes overshoot
(gj_block -0.52, innexin -0.56, morphogen -0.27, ion -0.19 — the
binary-penetrance residual quantified at corpus scale). M32 registered:
promote the 6.0 mV threshold to pre-registered-fitted (the exp29
watch-item). Ledger L21.

## exp39 — direct comparison to the published voltage record: 6/6 direction MATCH

Every published DIRECTION claim vs the model's fresh-extracted
quantity: depolarized head (Beane 2011), hyperpolarization->abnormal
(Beane 2013), posterior-depol ectopic head HL 0.95 (Oviedo 2010),
junction-block mixed outcomes via M25 (Oviedo 2007), wound
depolarization, stochastic identical-perturbation outcomes (Pezzulo &
Levin 2021; exp38 seed-split + exp12 latch). Zero mismatches. Honest
scope: planarian absolute mV is unpublished (dye ratios) — the model's
absolute scale is an exp1 calibration choice. Permanent record:
research/LEVIN_VOLTAGE_COMPARISON.md. Ledger L22.

## exp40 — channel dose scan: ion|trunk resolved; S2R3c closed (untested, not falsified)

The (cns x diffusion) grid is MONOTONE in diffusion (trunk 0.00 ->
0.33 -> 0.67 -> 1.00) — the model's own dose-response curve. The 1/3
cell (cns=1, diff=1.0) brackets the recorded ion|trunk 0.46 at distance
0.13 with tail/head calibrations intact: exp35's refutation candidate
RESOLVED (it was a plane-protocol artifact — exp37's two-face trunk
had already moved the gap -0.46 -> +0.21). S2R3c: no partial-dose
regeneration curve exists in the DB (L16) OR the published literature
(supramaximal doses, timing ladders only) — S2R3's monotone prediction
stands UNTESTED and is a formal novel-prediction deposit. Ledger L23.

## STAGE 3 (金丹) — the anatomical compiler v0 (exp41): compilation, not search

cultivation/compiler/anatomy.py: declarative AnatomySpec ->
InterventionProgram (regions, voltages, durations, coupling
preconditions, verification criteria) -> in-sim execution +
self-verification. The M28 phi layer IS the target representation —
write the spec, trigger a regen that reads it; zero CEM iterations.
Results: CP-G1 restorative compile PASS (3/3, ~3 mV); CP-G2 TWO-HEAD
compile PASS (the Levin anchor reached by compilation); CP-G4 safety
refusal PASS; CP-G5 coupling necessity PASS (the program fails under
blockade — the precondition is load-bearing); CP-G3 ectopic
novel-anatomy REFUTED by 0.22 mV (two-sided Laplacian erosion of
unsupported zones) with the latch amendment REFUTED under a different
signature (latch regen doesn't read phi) — compiler v1 work item: the
hybrid latch+spec rule. PROCESS: verifier substring bug caught+fixed
(execute criteria, never parse them). Ledger L24.

## STAGE 4 (元婴) — the cognitive light cone (exp42): junction-carried, dose-monotone rho=1.00

cultivation/cognitive/lightcone.py: paired-trajectory instrument (same
seed => divergence IS influence; zero averaging). Single-cell 2h pulse,
gap scan: propagation PASS, cognitive fragmentation under blockade
PASS, junction-scaled dose-response PASS (rho=1.00; horizon 5/3/2/1
cells at gap 1.0/0.5/0.25/0.05 — the third axis with the S2R3/exp40
monotone shape). LC-G4 REFUTED with a power diagnosis: the 2h pulse's
cone never reaches half-chain; the residue WITHIN the cone is 36-42 mV
— memory is CONE-BOUNDED, and the instrument now EXPLAINS the model's
own 24h sustained-forcing requirement instead of assuming it. Ledger
L25.

## STAGE 5 (飞升) — substrate independence (exp43): mechanism transfers everywhere, form is substrate-conditioned

cultivation/substrate/graph.py: GraphCollective (path / 2D lattice /
random 3-regular / scale-free) + regrow_graph (BFS regeneration,
M25-consistent). All gates REFUTED as naively registered — and the
diagnosis is the Ascension finding: identity labels are attractors
only when coherent with the substrate's connection structure (path
1.8/grid 5.6 PASS; scattered labels fail everywhere; BFS-coherent
amendment improves one notch; degree normalization probed and does
NOT rescue scale-free — the invariant is the BOUNDARY-TO-VOLUME RATIO
of the target partition). What transferred universally: the dynamics,
the M25 blind-guess corruption (12-22 mV on every topology), the regen
machinery (1.1-4.5 mV on coherent topologies). Resolved claim:
substrate-independent MECHANISM, substrate-conditioned FORM — the
compiler must become the substrate-adapter (rule R5: substrate-aware
partitioning + per-substrate calibration, night-six queue). Ledger L26.

## Night four/five (2026-09-15) — the phase inventory

All five stages now have run results on main:
Stage 1 (炼气) ~95% | Stage 2 (筑基): per-experiment instrument
delivered, corpus-scaled ordering, ion|trunk resolved, Levin 6/6,
dose-response closed; remaining: innexin|head plane-dependent readout,
M31 stored anchor availability, M32 threshold fitting | Stage 3 (金丹):
compiler v0, restorative + two-head compilation verified, novel-anatomy
frontier measured | Stage 4 (元婴): light cone measured, memory
cone-bounded | Stage 5 (飞升): mechanism universal, form
substrate-conditioned (compiler R5 registered).

## Night six (2026-09-15) — the phase inventory after completion of the night-six queue

Research directive FIRST (exp44): 14 targeted Europe PMC queries mapped
to the night-six queue; the published answers pieced together in
`research/NIGHT_SIX_SYNTHESIS.md` (Ross 2022 constitutive positional
info; Lobo 2019 axon-aligned vector transport; egal-1/microtubule notum
2025; Pezzulo/Levin 2017 cryptic-gradient + multistable-switch + regen-
window protocol; 2026 graph-wound hybrid framework). Then:

- **exp45 (L27)**: M31 registered form REFUTED (settle history is
  seed-invariant at macro scale — face drifts 4.14/4.21/4.26 mV, spread
  0.12 mV); **M31-A isolated re-anchoring ADOPTED** (all 6 gates PASS at
  q=0.50): the per-blastema coin is MINTED from the fragment's own
  stored state (blake2b of the quantized face window) — deterministic
  per fragment, zero self.rng contact, exp38's innexin seed-flip blocker
  gone (drift 0.00).
- **exp46 (L28)**: **M33 neural/muscle polarity channel — ALL 5 GATES
  PASS**. The anterior pole is a constitutive junction-INDEPENDENT
  identity source (Lobo 2019; egal-1/microtubules 2025): under blockade,
  anterior-identity cells read the spec directly (innexin_head 1.00 ->
  0.00, record 0.00); posterior identities stay junction-carried
  (innexin_tail 0.67 preserved bit-exact). The exp35 innexin|head +1.00
  gap — the LAST unexplained Stage-2 arm signature — is resolved.
  Novel prediction: gjblock_head moves toward normal.
- **exp47 (L29)**: **COMPILER v1 — ALL 6 GATES PASS; CP-G3' RESOLVED**.
  v0's latch chased the clamps halfway (window ended with the stored
  gradient HALF-WRITTEN); R1'' latch-write (latch := spec at window end,
  per the 2017 state-writable gradient semantics) fixes it: ectopic
  third-head compile verifies 3/3 (errs ~2.6 vs ~7.0). R5 substrate-
  aware partitioning (b2v <= 0.10) reproduces exp43's signature exactly
  with >=1.5x margins — the compiler IS the substrate adapter. THE
  GOLDEN CORE THRESHOLD IS FULLY CROSSED: restorative + two-head +
  ectopic novel anatomy, all zero-search.
- **exp48 (L30)**: M32 single-threshold REFUTED on the held-out class
  (train optimum 13.0 mV generalizes worse to ion_channel) — the corpus
  residual is STRUCTURAL (per-class mechanism gaps), not a threshold
  artifact; the 2017 constant-ratio finding confirms the binary
  per-animal rule. M34 candidate registered (gene-expression layer).
- **exp49 (L31)**: **LC-G4 RESOLVED** — the rewrite regime is the REGEN
  WINDOW (the 2017 protocol's own window). A 2h pulse during the
  commitment walk writes a 2.44 mV identity shift across the whole
  regenerate (intact same pulse: 0.00); persists 15h; collapses to 0.00
  under blockade; dose monotone then saturating (the chain-re-carries
  signature at the light-cone level); DIRECTIONALLY ASYMMETRIC (face
  2.44 vs 5-cells-anterior 0.00) — a novel falsifiable prediction for
  regeneration-window optogenetics.

Stage inventory after night six:
Stage 1 (炼气) complete | Stage 2 (筑基) **COMPLETE at slice + corpus
instrument level**: every arm-level signature now explained (innexin|head
via M33; penetrance via M31-A; corpus residual diagnosed structural) |
Stage 3 (金丹) **compiler v1 verified including ectopic novel anatomy**
(R5 substrate adapter in) | Stage 4 (元婴) light cone complete with the
rewrite regime named and a directional-cone prediction | Stage 5 (飞升)
mechanism universal + form substrate-conditioned, now enforced at
compile time. Night-seven queue: M34 gene-expression class layer,
M31-A fragment-size correlation scan, R5 per-substrate eps/mu
calibration, corpus re-pass with M33 (gjblock_head prediction), quest
001 via zai runner when quota opens.

## Night eight — the research-grounded wave (2026-09-15)

Research directive first, broadened past Europe PMC to six free sources
(Europe PMC + PubMed E-utilities + Crossref + arXiv + OpenAlex + Zenodo;
exp53/53b/53c): the directive's key claims were VERIFIED at abstract
level, with one citation corrected (the 3h-window paper's PMID was wrong
— the real record is MED30799071 / DOI 10.1016/j.bpj.2019.01.029). The
verified anchors: Durant 2019 3h window; Saito 2003 M-L intercalation
(10.1002/dvdy.10246); the 4D atlas (MED42172041 — ARZ, Mediator 8,
underdamped PCG, verbatim); the TAS geometric memory model
(PPRPPR1216581); both 2026 Zenodo deposits (symbol grounding 21459264,
coupling response geometry 18358611); neurobots (MED41717829) and
synthetic-construct memory (PPRPPR1219439). Synthesis with
pre-registered build gates: research/NIGHT_EIGHT_SYNTHESIS.md.

Experiments (all deterministic-gated, suite 64 green):
- exp54 pulse-timing critical window: 5/5 PASS — the decision medium is
  the FIRST COMMITMENT (3h pulse at t=0 writes 3.00 mV full-chain;
  any later start ~0.5 mV and re-absorbed; post-walk exactly 0);
  fixed-shape geometry confirmed; 3h sufficiency; 6h deadline; size
  collapse.
- exp55 graft/lateral 2D sheet: module built (two fields, midline
  source); isograft + native-axis integrity PASS; induction gates
  REFUTED with a 3-part diagnosis (D1 artifact found+fixed: the
  physiological zero-crossing must not fire; D2 pure-diffusion AP
  cannot HOLD identity — no sheet-level attractor; D3 one-sided edge
  drive cannot fill the graft). M-sheet repair registered (night nine:
  inheritance-copy fronts with the exposure gate).
- exp56 THE READER PERTURBATION TEST: 6/6 PASS — same pattern,
  different form by the reader alone; the lookup is the decoder
  (scrambled phi_spec -> MIRROR FORM: tail fully head-like at 1.000);
  destroyed carrier + reader restores the form; carrier-assistance
  precision term discovered (~6 mV).
- exp57 closing batch: TAS cryptic re-cut interval PASS (discordant
  seed: normal 5.94 -> abnormal 6.42 on re-cut; bit-exact replay 12/12
  — stable re-challenge ratios); underdamped recovery WEAK (0.296 mV,
  calibration target); M36 mis-anchored pole 3/3 PASS (egal-1
  direction: tail becomes fully head-like under blockade);
  gjblock|head_tail ledgered (model 0.67 vs recorded 0.025, n=2 —
  protocol-semantics miss).

Night-nine queue: M-sheet inheritance-copy fronts; ARZ wound-domain
readout (M35, Mediator 8 analog); compiler v2 work items; DB
head_tail re-mapping; S2R3c novel-prediction deposit; quest 001 when
quota opens.

## M26: the night-nine CONTINUOUS BATCH (exp58-exp70) — the directive changed

The unit of work stopped being "one night." Ten experiments ran back
to back, push after push, each derived from the ledger's open items
and the literature.

- exp58 M-SHEET REPAIR (7/7): Saito 2003's abstract INVERTED the
  exp55 fire rule (induction fires on SAME-SIGN medial-lateral gaps;
  L-R facing contact is SILENT). IntercalationSheet rebuilt
  additively: same-sign rule + exposure->commitment + inheritance-copy
  propagation + field maintenance. exp55's S1/S2/S4 RESOLVED.
- exp59 M35 ARZ (5/5): M35-as-first-registered REFUTED AS REDUNDANT
  (the blind-guess base already converges the wound repertoire);
  M35-A adopted — multi-lineage convergence (K=3, derived not
  fitted): tail rate 0.917 -> 0.333 vs record 0.40.
- exp60 THE GENE LAYER (M37, 3/5): the DB's 412 RNAi entries mapped
  to functional families; the morphogen class was UNDER-INCLUSIVE
  (dvl/fzd/evi/notum join at 0.815 vs 0.718); the M33 neural channel
  proven NECESSARY (substrate-gene disruption costs more than
  junction blockade); N1's deposit falsifier FIRED honestly (generic
  pooled 0.855 outside the registered band); the neoblast record is
  GRADED (M37-A registered); neoblast_depleted param added.
- exp61 COMPILER V2 (4/4): FOUR novel layouts verify zero-search in
  1.4 s; the R1'' latch-write cuts the minimum window 24 h -> 3 h
  (8x); lab-executable schedules emit (R6); 100-GENERATION
  STABILITY with ZERO anchor drift — the exp41 latch re-read path
  closed structurally.
- exp62 STAGE-4 SIGNAL-RANGE DIAL (4/5): the coupling-kernel radius
  is a REAL dial — horizon 5 -> 10 -> 16 -> 24 cells (4.8x, the
  5->20 target exceeded); the regen cone's write dilutes with k
  (5.07 -> 2.25 mV); k=4 breaks the third-head verify (the honest
  D-G4 refutation) — THE CROSS-STAGE RULE: reach is bought with
  contrast; operating envelope k<=2.
- exp63 STAGE-5 BLUEPRINT TRANSFER (4/4): the phi_spec layer
  serialized to JSON and reloaded into fresh hosts; identity 1.0
  across kernels; survives partial death; refused on non-supporting
  substrates (R5 at transfer); READER-DEPENDENT (no-readout control
  0.0). Fine voltage offset ~9.6 mV = the carrier-assistance term.
- exp64 M37-A/M37-B: M37-A ADOPTED (the neoblast coin — per-animal
  penetrance from stored state; out-of-plane prediction PASS);
  M37-B REFUTED (impairment CHANNELS are not interchangeable —
  plane signatures are channel-specific).
- exp65 M38-A CO-TUNING: geometry REFUTED (zone width nearly inert);
  the anchor itself drifts in the unclamped settle; MAINTENANCE
  CO-TUNING ADOPTED — a 3 h re-clamp schedule verifies k=4 fully.
  THE RULE: free-running envelope k<=2; beyond it the compiler
  emits a maintenance schedule. The duty cycle buys reach.
- exp66 CORPUS SEMANTICS CORRECTED (3/5): the head_tail anomaly was
  A PLANE MIS-MAP ("Head plus pre-pharyngeal crop" = one contiguous
  anterior removal); the gj_block|head 0.177 residual OWNED BY THE
  MIXTURE (pub1 octanol sustained 0.092 — M33-consistent — vs pub20
  heptanol delayed 0.345); the washout-pulse refutation registered
  M40.
- exp67 COMPILER V3 CORPUS LOOP (3/4): the full adopted stack
  generates every mapped corpus arm; MAE 0.595 -> 0.524 (the first
  corpus-level improvement since the baseline); both refuted
  signatures shrink; the plane-rho drop diagnosed as exp37's
  all-zero artifact.
- exp68 THE COHERENCE-FORMALIZATION SEARCH (star-search step 1, 2/3):
  the exp43 constraint tested against dynamics-matched formalizations
  over a 9-substrate battery — THE BOUNDARY DOES NOT MOVE (no
  substrate that b2v refuses but the dynamics supports; all five
  formalizations separate pass/fail). The floating-pattern star is
  blocked by the DYNAMICS, not the metric.
- exp69 M40 COMMITMENT-RATE COUPLING (4/4, ADOPTED): the blastema
  delays commitment under blockade (cell_period x (1 + D(1-r)));
  the constraint sweep adopts D=2 — the washout record matched
  (0.00) with the sustained signature UNCHANGED.
- exp70 ONSET-AWARE CORPUS (4/4): all gj_block experiments
  classified sustained/delayed/washout; e329 matched exactly;
  MAE 0.524 -> 0.522.

### Stage scoreboard after the continuous batch
- Stage 1 炼气 complete | Stage 2 筑基: the GENE LAYER exists (families,
  coin, channels); corpus MAE 0.595 -> 0.522 with every residual
  owned | Stage 3 金丹: compiler v2 (4 novel layouts, 3 h window,
  100-gen stability, lab schedules) + v3 corpus loop | Stage 4 元婴:
  the dial is real (4.8x reach) with the contrast trade-off RULED
  (envelope k<=2 free-running; maintenance beyond) | Stage 5 飞升:
  blueprint transfer 4/4 (digital round-trip, cross-substrate,
  partial-death survival, reader-dependent); the coherence
  constraint ROBUST across formalizations (the star stays blocked
  by the dynamics — the honest step-1 report).

### Stage scoreboard after the STAR-SEARCH ARC (exp73-exp79)
- Stage 5 飞升: **THE STAR IS CROSSED AT THE MODEL LEVEL.** The
  star-search arc ran eight steps: (1) the coherence constraint is
  formalization-robust (exp68); (2-6) every LOCAL remodeling
  mechanism fails the hub regime with a diagnosed signal pathology —
  rewiring moves the boundary for homogeneous-degree substrates
  (torus 8.47 -> 1.96) but hubs are walled (exp73); the ladder's
  prune/grow/thin rungs all stall — the local signals are
  degree-diluted, smear-corrupted, self-extinguishing, bridge-walled,
  source-blind (exp74-77); (7) the phase diagram finds the TWO-CHANNEL
  structure: the V-channel ratio g_cut/(gamma+g_total) AND the theta
  homogenization number mu*deg*T — the identity layer diffuses
  through the same junctions and hijacks itself (exp78: mu=0 takes
  scale_free 9.17 -> 0.16 mV); (8) **the star point**: (gamma=64,
  mu=0) writes ANY substrate with NO remodeling (scale_free 0.57
  verdict, 0.57 hold) and the UNIVERSAL READER — the non-junctional
  anterior read (M33) + anchor + strength — regenerates the head
  through ZERO junctions (V 0.43 / theta 0.44) (exp79).
- **The reframe is now a result**: the star was never "no substrate" —
  it is "any substrate coherent with the pattern", and the boundary is
  an ARCHITECTURE REQUIREMENT, not a wall: strong identity + a
  non-diffusing anchor + a read on a channel the coupling cannot
  hijack. The reader's domain is anterior-only (trunk regen fails at
  w=0) — the recorded posterior-biased GJ-blockade phenotypes
  reproduced as a structural theorem.
- The price is named: the anchor's cost is the RATE of organic
  repatterning (the eps channel provides redundant slower
  propagation — TC-G6's honest refutation), and the two dials'
  interaction term is the next theory task (TC-G1: Spearman 0.838).

### Stage scoreboard after the protocol/generator batch (exp80-exp83)
- Stage 2 筑基: GL-G4 CLOSED by record correction (the control hot
  bias 0.270 measured; the corrected generic target 0.585 puts the
  N1 protocol's 0.655 inside the band — the protocol was never too
  weak, the record was too hot; the N1 deposit band retired). GL-G3
  pool-closed (the M37-A coin: sim 0.695 vs record 0.701) with
  M37-A' (per-plane coin anchors) the one registered candidate left.
- Stage 3 金丹: **THE GENERATOR STAR CLOSED** — compiler v4 generates
  novel multi-zone anatomies (3 classes with no corpus counterpart,
  verified, 100-gen stable), calibrates its own admissibility
  envelope from data (test precision 100% at 40% coverage,
  no leakage), and carries the two-channel law as the
  OPERATING-POINT ESCAPE (35/35 scale_free refusals verify at the
  star point — a baseline refusal names the conditions that admit
  it). The regen-walk limitation found and owned: triggers cannot
  regenerate novel zones (the graph-native reader regen is future
  work).
- Stage 4 元婴: characterized end to end — the maintenance-duty map
  measured (chain frontier k=2→0.0, k=3→0.25, k=4→0.75, k=5/6→1.0;
  exp65's k=4@0.67 bracketed); the frontier is TISSUE-SPECIFIC
  (grid needs continuous clamping, small-world free-runs): the rule
  is universal, the envelope and the exchange rate are readout-side.
- Stage 5 飞升: the external storage protocol 6/6 (capture → store →
  destroy → re-instantiate; byte-exact, substrate-independent,
  destruction-proof, ageless medium; ES-G6: the architecture is a
  required part of the protocol) with the wet-lab companion document
  (docs/STAGE5_EXTERNAL_STORAGE_PROTOCOL.md).

### Stage scoreboard after the quantitative-law batch (exp84-exp90)
- Stage 2 筑基: **THE GENE LAYER IS CLOSED END TO END.** The record's
  plane profile is statistically FLAT (exp85: trunk-head z=0.32 — the
  profile could never refute a one-parameter coin); the coin-digest
  ARTIFACT found and repaired (the head-plane window was wound-state
  constant, u=0.212 for every seed — penetrance had saturated);
  the head-plane fragility was REGEN-layer biology (b_head=0.70 coin-
  off), repaired by the M33-gated read (0.70→0.00) — the pool
  recomposes at 0.767 vs 0.799 with NO per-plane parameters (exp86).
  The corpus re-wired to the adopted stack: MAE 0.522 → 0.365 raw /
  0.304 corrected-decoded (the stale 24h protocol window was 43% of
  the residual); the remaining gaps NAMED (the exp40 dose axis; the
  record's own series-variance floor) with the repair registered
  (exp88).
- Stage 3 金丹: **THE COMPILER IS UNIVERSAL.** v5 connects the reader
  (the R1 memory write + the exp79 reader weight + the M33 gate;
  zone errors 6-16 → 0.29 mV; five instrument findings owned) and
  emits its own operating point (R7': the star point as a
  precondition). R5' BORN: the partition refusal is a PRICE TAG, not
  a wall — at the default operating point the exp43 signature
  reproduces 7/7, at the star point EVERY substrate verifies
  (0.25-0.63 mV), and the M33 domain stays substrate-independent
  (7/7) — the two rules are orthogonal (exp89). The two-source read
  closes the multi-region novel regen UNIVERSALLY (7/7 substrates,
  0.49-0.70 mV; no backdoor; the canon source load-bearing) — the
  final rule set R1/R1'/R2/R3/R4/R5/R5'/R6/R7/R7' + two sources
  (exp90).
- Stage 5 飞升: **THE TWO-CHANNEL LAW IS QUANTITATIVELY CLOSED** —
  err = sqrt(eV² + eθ²) (Spearman 0.999, med rel 2.7%, holdout torus
  rho 1.000; the mean-field 0.838 was formula-limited, not
  dynamics-limited; the overlap correction honestly retired; the
  writability boundary 100%; the price attributed to the propagation
  panel where exp62/65 measured it) (exp84).
