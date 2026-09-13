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
│    exp4 cross-species          aggregate.py                  │
├──────────────────────────────────────────────────────────────┤
│  tests/                     the falsification suite          │
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
python -m experiments.exp7_stress --shard 0/4 --out results/   # sharded sweep
```

## Sharded stress sweeps on GitHub runners

`.github/workflows/sharded-sweep.yml` fans `exp7` across a 24-way matrix (max-parallel 20) and aggregates artifacts into `results/`. Trigger via Actions UI or API. `.github/workflows/helix-stress.yml` stress-tests the helix-codec repository (RS/LDPC/Viterbi under escalating error loads) on runners so no local CPU is burned.

## Falsification status

See `docs/FALSIFICATION.md` — Level 1 (model reproduces known biology: two-headed reprogramming with memory, cancer-normalization boundary), Level 2 (Gompertz-form hazard emerging from channel degradation, cross-species consistency), each with pass/fail criteria and automated tests.

## Research dossier

`research/` contains the verified literature (bioelectric morphogenesis, IIT, aging theory, Chinese research landscape) with DOIs verified against Crossref/PubMed responses, plus real C. elegans connectome data (OpenWorm; Cook et al. 2019).

## License

MIT.
