# A slow homeostatic target is necessary and sufficient for persistent bioelectric pattern memory in a minimal gap-junction model

**Draft preprint (q-bio.TO).** Author: Jack (ssmurfgg04-gif) · Code: github.com/ssmurfgg04-gif/bioelectric-cultivation

## Abstract
Planarian fragments briefly exposed to bioelectric perturbation can regenerate two heads, and they keep doing so across later amputations without further treatment. We ask what minimal dynamical ingredient makes such a rewrite persistent.

We study a 1-D chain of gap-junction-coupled cells. Each cell has a fast membrane voltage V and a slow homeostatic target θ toward which V relaxes. θ in turn adapts to V at rate ε.

Under pre-registered gates (20 seeds per arm), a 24 h posterior depolarising clamp under gap-junction block rewrites the regeneration target in 20/20 seeds. The rewrite survives two amputation–regrowth rounds. Gap-junction block alone rewrites 0/20. Setting ε = 0 abolishes persistence (0/20), so θ plasticity is necessary. The dose-response is sigmoidal, with half-effect near −28.6 mV.

In a companion aging model, sustained low-dose target correction extends median lifespan by ×1.087 (95% CI 1.081–1.093). The same total dose given once yields ×1.044 (CI 1.041–1.048). The paired difference is +0.043 (CI 0.038–0.047; permutation p = 1 × 10⁻⁴).

We also report a pre-registered negative result: the aging model yields Gompertz-shaped mortality, but no model parameter sets the Gompertz rate. The cause is the saturating burden-to-hazard link.

We derive four falsifiable wet-lab predictions. The novel one is W4: blocking slow channel re-expression during the perturbation should abolish memory.

## 1. Introduction
Bioelectric patterns carried by gap-junction-coupled tissues instruct large-scale anatomy (Levin 2021). In planaria, transient manipulation produces two-headed animals whose altered target morphology persists across rounds of amputation (Durant et al. 2017).

Models of this phenomenon use bistable circuits (Pietak & Levin 2017; Cervera et al. 2019). Here we isolate a simpler candidate: a **separation of time scales** between voltage and a slow, plastic set point. We test it under pre-registered, multi-seed, ablation-controlled gates.

## 2. Model
For cells i on a chain with adjacency A and coupling G = g·A:

dV_i/dt = γ(θ_i − V_i) + Σ_j G_ij (V_j − V_i) + η_i(t)

dθ_i/dt = ε(V_i − θ_i) + μ Σ_j A_ij (θ_j − θ_i)

The defaults are γ = 0.25 h⁻¹, g = 0.20 h⁻¹, ε = 0.04 h⁻¹, μ = 0.015 h⁻¹ and σ_η = 0.3, with N = 100 cells and dt = 0.1 h. The timescale ratio is ε/γ = 0.16.

Amputation removes cells 85–99. Regrowth extends the stored θ pattern from the wound boundary. The readout is tail head-likeness, h = clip((mean V_tail + 40)/15, 0, 1). Full units are in `docs/UNITS.md`.

## 3. Methods
**Pre-registration.** Hypotheses and pass/fail gates were committed before any run (`docs/PRIMARIES.md`, commit 6d64990). We used fresh seed ranges and Holm–Bonferroni correction across three primaries.

**P1 arms** (20 seeds):
- **A:** −20 mV clamp on the posterior quarter, GJ scale 0.05, 24 h, then 2 amputations.
- **B:** GJ block only.
- **C:** arm A with ε = 0.
- **D:** clamp voltages from −35 to −15 mV.

**P2.** Cohorts of K = 400 individuals, simulated for 130 years at dt = 0.25 yr, 20 seeds. Arms: none; sustained (10% θ pull plus clearing of up to 3 senesced cells, every 4 yr from age 48 to 96); one-shot (dose-matched single application at 48). Statistics: bootstrap CIs and a paired sign-flip permutation test.

**P3.** Engine-dominant variant (h0 × 0.1). We fit a truncation-corrected Gompertz MLE on ages 35–100 and estimated the elasticity of β with respect to h_sys.

## 4. Results
See `docs/PRIMARY_RESULTS.md`; all numbers are reproducible with `python -m experiments.exp448_p1_target_memory` and the analogous P2/P3 scripts.

- **P1 passes all four gates** (p = 9.5 × 10⁻⁷).
- **P2 passes both gates** (p = 1 × 10⁻⁴).
- **P3 fails.** β falls with h_sys (elasticity −0.16 ± 0.04). The exploratory trace shows why: hazard = k·burden is capped at k, so a faster engine saturates the burden earlier.

## 5. Discussion
A slow plastic set point turns a transient input into a durable attractor shift. This is the minimal requirement for "bioelectric memory" in this model class. It predicts that interfering with slow channel re-expression should block memory formation (W4); the published experiments do not yet test this.

**Limitations:**
- 1-D chain, Euler–Maruyama integration, phenomenological regrowth.
- The h readout saturates, and arm A is at ceiling.
- No absolute planarian mV data exist for quantitative fitting.
- The aging model is phenomenological, uses years rather than hours, and has the structural Gompertz-rate defect reported here.
- Earlier exploratory claims (cross-species ordering, human-graph transfer, Gompertz β in the human range) are withdrawn (`docs/CLAIMS_AUDIT.md`).

## 6. Predictions (W1–W4)
See `docs/DATA_CONTACT.md`.

## References
- Durant F. et al. (2017) Long-term, stochastic editing of regenerative anatomy via targeting endogenous bioelectric gradients. *Biophys J* 112:2231.
- Pietak A., Levin M. (2017) Bioelectric gene and reaction networks. *J R Soc Interface* 14:20170425.
- Cervera J. et al. (2019) Bioelectrical coupling of single-cell states in multicellular systems. *J Phys Chem Lett*.
- Levin M. (2021) Bioelectric signaling: reprogrammable circuits underlying embryogenesis, regeneration, and cancer. *Cell* 184:1971.
- Gavrilov L., Gavrilova N. (2001) The reliability theory of aging and longevity. *J Theor Biol* 213:527.
