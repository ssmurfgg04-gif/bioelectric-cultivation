# The theory, formalized

## 1. The bioelectric sheet

Each cell $i$ holds membrane voltage $V_i$ (mV), coupled by gap junctions
$G_{ij}$, with a slow homeostatic target $\theta_i$ (the intrinsic resting
state the cell's channel expression re-converges toward — real biology:
cells adjust resting potential via ion-channel transcription over hours):

$$\frac{dV_i}{dt} = \gamma(\theta_i - V_i) + \sum_j G_{ij}(V_j - V_i) + \eta_i(t)$$

$$\frac{d\theta_i}{dt} = \varepsilon(V_i - \theta_i) + \mu \sum_j A_{ij}(\theta_j - \theta_i) + \xi_i(t) + \text{drivers}_i$$

The same $\varepsilon$ term does double duty: a 24h forced depolarization
rewrites $\theta$ (stable reprogramming, the two-headed planarian memory of
Durant et al. 2017), and unforced noise makes $\theta$ random-walk (aging
drift). Reprogramming and aging are two regimes of one mechanism.

Oncogene drivers are voltage-gated theta pulls — depolarization is
permissive for the tumoral state (Chernet & Levin 2013/2015), which is why
hyperpolarization can normalize oncogene-expressing tissue and why restoring
gap-junction connectivity lets a hyperpolarization wave erode a tumor from
its boundaries.

Regeneration is pattern extension: the blastema inherits identity from the
wound-boundary tissue as it regrows (`collective.regrow`) — whatever the
remaining tissue REMEMBERS is what gets built. This is what makes
reprogramming memory empirically testable.

## 2. Aging as control-system degradation

Three mechanisms: $G(t) = G_0 e^{-\lambda t}$ (connexin decay),
$\sigma_\eta(t) = \sigma_0 e^{\kappa t}$ (noise growth), $\theta$ diffusion.
Failure: cells whose tracking error leaves the healthy operating envelope
senesce (pin depolarized, drop out of the network). The senesced burden
grows by immigration (baseline damage, frailty-scaled) plus SYSTEMIC
self-catalysis (inflammaging):

$$\frac{ds}{dt} \approx s_0 z + h_{sys}\, s \quad\Rightarrow\quad s(t) \sim \frac{s_0 z}{h_{sys}}\left(e^{h_{sys} t} - 1\right)$$

Death is a hazard $\mu_i(t) = k \cdot s_i(t) \propto e^{h_{sys} t}$ — the
Gompertz form, emerging rather than assumed, with the saturation cap of $s$
giving late-life mortality deceleration (plateaus) for free. See
exp3 for the honest fits: Gompertz WINS the pre-saturation window; Weibull
edges it out over the full adult window; and the fitted slope does NOT
track $h_{sys}$ (documented negative — the slope is an emergent property of
the frailty mixture and saturation timing).

## 3. The information layer

$I(V; M)$: the gap-junction network is a denoiser — young tissue cleans a
noisy voltage pattern so the state still predicts the morphology it will
build; aged tissue (noise grown, junctions decayed) cannot, and the state
decouples from the morphology it is supposed to encode. Measured: 1.55 bits
young → 0.83 bits aged (exp5).

$\Phi$ (linear-Gaussian integration, in the Barrett & Seth 2011 /
Oizumi et al. family): $\Phi(P) = I_{whole} - I_{part} - I_{\bar{part}}$
minimized over bipartitions, computed exactly for small systems on the
discrete Lyapunov covariance. Peaks at intermediate coupling; ~0 for modular
systems; computed on REAL C. elegans gap-junction motifs (Cook et al. 2019
data). Honest negative: linearized fixed-point $\Phi$ cannot distinguish
coherent from incoherent drive (the Jacobian sees activation magnitude, not
coherence) — time-resolved measures are required for the meditation
question.

## 4. The coding layer (helix-codec isomorphism)

The morphological target is information stored in a noisy biological
channel. helix-codec's cascade (outer RS + inner code + consensus +
digest) maps onto: RS across spatial clusters, gap-junction belief
propagation within neighborhoods, repeated-measurement consensus, and
CRC/SHA-gated write-back. Two hard requirements imported from the helix
stress test (F3, F5): never write unverified data (silent corruption is
the worst failure mode), and intervene before the parity budget is
exhausted (zero-margin recovery is a latent failure).

Documented negative: storing RS parity AS voltage setpoints is actively
eroded by the sheet's smoothing dynamics — the viable architecture stores
parity out-of-band (the genomic archive) and uses the coupling graph as
the BP denoising layer instead.

## 5. The maintenance claim

"Cultivation" = maintaining the error-correcting capability above the
channel's noise level, indefinitely. Measured: periodic budgeted
maintenance extends median lifespan ~1.08-1.10x (exp6), and sustained
maintenance from mid-life beats one-shot correction (exp3: one-shot x1.00,
sustained x1.07) — the ongoing-practice structure the cultivation framing
predicts. Honest caveat: in this mortality model, verification does not yet
pay (death depends on senesced burden and tracking, not pattern fidelity) —
pattern-fidelity-dependent mortality is the follow-up that would test it.
