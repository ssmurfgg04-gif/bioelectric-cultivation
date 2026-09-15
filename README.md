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
