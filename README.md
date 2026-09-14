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

## Research dossier

`research/` contains the verified literature (bioelectric morphogenesis, IIT, aging theory, Chinese research landscape) with DOIs verified against Crossref/PubMed responses, plus real C. elegans connectome data (OpenWorm; Cook et al. 2019).

## License

MIT.
