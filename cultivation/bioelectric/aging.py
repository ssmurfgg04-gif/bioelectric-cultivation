"""Aging as bioelectric control-system degradation, cohort-simulated.

Three coupled mechanisms (each literature-motivated):
  1. Gap-junction decay      G(t)    = G0 * exp(-lambda * t)     (connexin aging)
  2. Noise growth            sigma(t) = sigma0 * exp(kappa * t)  (stochastic channel opening,
                                                                 metabolic noise)
  3. Target drift            theta random-walks (homeostatic memory corrupts)

plus a *senescence cascade*: cells whose local tracking error exceeds their
healthy operating envelope pin depolarized and drop out of the network;
senesced neighbors then raise the failure hazard of nearby cells
(inflammaging-style local feedback). Death = organ failure (any segment's
senesced fraction above a critical level) or global pattern-maintenance
collapse — the redundancy-depletion logic of Gavrilov & Gavrilova's
reliability theory of aging.

The falsification question (exp3): does the hazard take the Gompertz form
mu(t) = alpha * exp(beta t), *emerging* from these mechanisms rather than
being assumed? Vectorized across K individuals x n cells.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np


@dataclass
class AgingParams:
    n_cells: int = 64
    n_organs: int = 4
    gamma: float = 0.25
    g0: float = 0.20
    eps: float = 0.04
    mu_theta: float = 0.003  # slow pattern smoothing (boundaries persist for decades)
    lambda_gap: float = 0.030  # 1/yr — gap junction decay
    kappa_noise: float = 0.048  # 1/yr — noise growth
    sigma0: float = 0.20  # mV / sqrt(yr) at t=0
    theta_drift: float = 0.045  # mV / sqrt(yr) target diffusion
    margin: float = 6.0  # mV beyond healthy envelope before hazard rises
    soft: float = 2.5  # mV hazard softness
    h0: float = 0.05  # 1/yr hazard scale at envelope edge
    h_sys: float = 0.10  # 1/yr SYSTEMIC inflammaging feedback (the Gompertz engine)
    h_inflam: float = 0.05  # 1/yr local (neighbor) senesced-burden feedback
    seed_rate: float = 1.5e-4  # 1/yr constant baseline damage per cell (sets alpha)
    mortality_k: float = 0.12  # 1/yr vital fragility: death hazard = k * senesced burden
    frailty_cv: float = 0.20  # gamma frailty on the damage seed (alpha heterogeneity)
    heterogeneity: float = 0.18  # per-individual CV on lambda/kappa
    target0: np.ndarray = field(default=None)  # wild-type pattern; built if None

    def with_updates(self, **kw) -> "AgingParams":
        return replace(self, **kw)


def _default_target(n: int) -> np.ndarray:
    t = np.full(n, -50.0)
    t[: n // 4] = -20.0
    return t


class AgingCohort:
    """K individuals of n cells each; simulate to death or `years`."""

    def __init__(self, K: int = 300, params: AgingParams | None = None, seed: int = 0):
        self.p = params or AgingParams()
        self.K = K
        self.n = self.p.n_cells
        self.rng = np.random.default_rng(seed)

        n = self.n
        A = np.zeros((n, n))
        A += np.diag(np.ones(n - 1), 1) + np.diag(np.ones(n - 1), -1)
        self.A = A
        self.degA = A.sum(axis=1)

        target0 = self.p.target0 if self.p.target0 is not None else _default_target(n)
        self.theta0 = np.asarray(target0, float)

        self.V = np.tile(self.theta0, (K, 1)) + self.rng.normal(0, 2.0, (K, n))
        self.theta = np.tile(self.theta0, (K, 1))
        self.senesced = np.zeros((K, n), dtype=bool)
        self.alive = np.ones(K, dtype=bool)
        self.death_age = np.full(K, np.inf)

        cv = self.p.heterogeneity
        self.lam = np.maximum(0.0, self.p.lambda_gap * self.rng.normal(1.0, cv, K))
        self.kap = np.maximum(0.0, self.p.kappa_noise * self.rng.normal(1.0, cv, K))
        # fixed gamma frailty on the damage seed (common beta, varying alpha —
        # the standard demographic frailty structure)
        fcv = self.p.frailty_cv
        self.frailty = self.rng.gamma(shape=1.0 / fcv**2, scale=fcv**2, size=K)
        self.t = 0.0

        # healthy operating envelope: per-cell baseline |V - theta| at t=0
        # (boundary cells legitimately sit between head and trunk levels —
        # that gradient is the healthy pattern, not a failure)
        Vb, thb, senb = self.V.copy(), self.theta.copy(), self.senesced.copy()
        errs = []
        for _ in range(24):
            self._integrate(0.25, np.full(K, self.p.g0), np.full(K, self.p.sigma0))
            errs.append(np.abs(self.V - self.theta))
        self.base_err = np.clip(np.mean(errs, axis=0), 0.5, None)
        self.V, self.theta, self.senesced = Vb, thb, senb

        # organ segments (contiguous quarters of the axis) — reported, not lethal
        self.n_org = self.p.n_organs
        self.org_len = n // self.n_org

        # history
        self.hist_t: list[float] = []
        self.hist_alive: list[float] = []
        self.hist_error: list[float] = []
        self.hist_sen: list[float] = []

    # ------------------------------------------------------------------ core
    def _integrate(self, dt: float, g: np.ndarray, sigma: np.ndarray) -> None:
        """One Euler-Maruyama step of the coupled dynamics (no mortality logic)."""
        p = self.p
        K, n = self.K, self.n

        avail = self.A[None, :, :] * (~self.senesced)[:, None, :].astype(float)
        deg = avail.sum(axis=2)
        coupling = g[:, None] * (np.einsum("kij,kj->ki", avail, self.V) - self.V * deg)

        dV = p.gamma * (self.theta - self.V) + coupling
        noise = sigma[:, None] * np.sqrt(dt) * self.rng.standard_normal((K, n))
        Vn = self.V + dt * dV + noise
        Vn[self.senesced] = -25.0  # senescent cells: moderately depolarized, disconnected

        lap = self.theta @ self.A.T - self.theta * self.degA
        dtheta = p.eps * (self.V - self.theta) + p.mu_theta * lap
        drift = p.theta_drift * np.sqrt(dt) * self.rng.standard_normal((K, n))
        self.theta = self.theta + dt * dtheta + drift
        self.V = Vn

    def step(self, dt: float, g_override: np.ndarray | None = None,
             theta_pull: np.ndarray | None = None) -> None:
        p = self.p
        t = self.t
        g = np.exp(-self.lam * t) * p.g0 if g_override is None else g_override
        sigma = p.sigma0 * np.exp(self.kap * t)

        self._integrate(dt, g, sigma)

        if theta_pull is not None:  # target-restoring intervention
            self.theta += dt * theta_pull[:, None] * (self.theta0 - self.theta)

        self.t += dt

        # senesced burden — per-cell immigration (frailty-scaled) + systemic
        # self-catalysis (inflammaging). In expectation sen_frac(t) grows as
        # (s/h)(e^{h t} - 1): exponential. Saturating logistic cap at 1 gives
        # late-life mortality deceleration for free.
        err = np.abs(self.V - self.theta)
        excess = err - self.base_err - p.margin
        local_burden = (self.senesced @ self.A.T + self.senesced) / (self.degA + 1.0)
        global_burden = self.senesced.mean(axis=1)[:, None]
        hazard = (
            p.seed_rate * self.frailty[:, None]
            + p.h_sys * np.broadcast_to(global_burden, (self.K, self.n))
            + p.h_inflam * local_burden
            + np.where(
                excess > 0,
                p.h0 * np.exp(np.clip(excess, 0.0, 60.0) / p.soft),
                0.0,
            )
        )
        draw = self.rng.random((self.K, self.n))
        newly = (~self.senesced) & (draw < dt * hazard)
        self.senesced |= newly
        # exposed for death-semantics layers (D3, senescence_semantics.py):
        # the mask of cells that senesced THIS step — the write-on-death hook
        self._newly_senesced = newly

        # death as a HAZARD proportional to senesced burden (not a threshold):
        # mu_i(t) = k * sen_frac_i(t) ~ k*(s/h)(e^{h t}-1)  =>  Gompertz with
        # beta = h_sys, alpha = k*s/h^2. Threshold-crossing timing would give
        # lognormal/Weibull shapes; the hazard formulation gives exact
        # Gompertz in the adult window and saturation-deceleration late.
        sen_frac = self.senesced.mean(axis=1)
        death_hazard = p.mortality_k * sen_frac
        dd = self.rng.random(self.K)
        died = self.alive & (dd < dt * death_hazard)
        if died.any():
            self.death_age[died] = t
            self.alive &= ~died

    # -------------------------------------------------------------------- run
    def run(self, years: float = 100.0, dt: float = 0.25,
            intervention=None, record: bool = True) -> dict:
        """Simulate; optional intervention(t, cohort) callback each step."""
        steps = int(round(years / dt))
        for _ in range(steps):
            if self.alive.sum() == 0:
                break
            self.step(dt)
            if intervention is not None:
                intervention(self.t, self)
            if record:
                self.hist_t.append(self.t)
                self.hist_alive.append(float(self.alive.mean()))
                err = np.abs(self.V - self.theta)[self.alive]
                self.hist_error.append(float(err.mean()) if err.size else np.nan)
                sen_frac = self.senesced[self.alive].mean() if self.alive.any() else np.nan
                self.hist_sen.append(float(sen_frac))
        return self.summary()

    def summary(self) -> dict:
        ages = np.where(np.isinf(self.death_age), np.nan, self.death_age)
        return {
            "K": self.K,
            "median_lifespan": float(np.nanmedian(ages)) if np.any(~np.isnan(ages)) else float("inf"),
            "max_lifespan": float(np.nanmax(ages)) if np.any(~np.isnan(ages)) else float("inf"),
            "survivors_at_end": int(self.alive.sum()),
            "death_ages": self.death_age.tolist(),
            "hist_t": self.hist_t,
            "hist_alive": self.hist_alive,
            "hist_error": self.hist_error,
            "hist_sen": self.hist_sen,
        }


# --------------------------------------------------------------------- fitting
def hazard_and_fits(death_ages: np.ndarray, years: float, dt: float = 0.25) -> dict:
    """Nelson-Aalen hazard + MLE fits (Gompertz / Weibull / lognormal / Gompertz-Makeham).

    death_ages: inf = censored (still alive at end). Lower AIC wins.
    """
    from scipy.optimize import minimize
    from scipy.stats import norm

    ages = np.asarray(death_ages, float)
    obs = ages[np.isfinite(ages)]
    n_cens = int(np.sum(np.isinf(ages)))

    def loglik_gompertz(x):
        a, b = np.exp(x[0]), np.exp(x[1])
        ll = np.sum(np.log(a) + b * obs - (a / b) * (np.exp(b * obs) - 1.0))
        ll += n_cens * (-(a / b) * (np.exp(b * years) - 1.0))
        return -ll

    def loglik_weibull(x):
        s, k = np.exp(x[0]), np.exp(x[1])
        ll = np.sum(np.log(k) - np.log(s) + (k - 1) * (np.log(obs) - np.log(s))
                    - (obs / s) ** k)
        ll += n_cens * (-(years / s) ** k)
        return -ll

    def loglik_lognormal(x):
        mu, sig = x[0], np.exp(x[1])
        z = (np.log(obs) - mu) / sig
        cens_z = (np.log(years) - mu) / sig
        ll = np.sum(-np.log(obs) - np.log(sig) + norm.logpdf(z))
        ll += n_cens * norm.logsf(cens_z).sum()
        return -ll

    def loglik_gm(x):
        a, b, c = np.exp(x[0]), np.exp(x[1]), np.exp(x[2])

        def H(tt):
            return (a / b) * (np.exp(b * tt) - 1.0) + c * tt

        ll = np.sum(np.log(a * np.exp(b * obs) + c) - H(obs))
        ll += n_cens * (-H(years))
        return -ll

    fits = {}
    specs = {
        "gompertz": (loglik_gompertz, [np.log(0.01), np.log(0.08)], 2),
        "weibull": (loglik_weibull, [np.log(30.0), np.log(2.0)], 2),
        "lognormal": (loglik_lognormal, [np.log(30.0), np.log(0.5)], 2),
        "gompertz_makeham": (loglik_gm, [np.log(0.01), np.log(0.08), np.log(1e-4)], 3),
    }
    for name, (fn, x0, k) in specs.items():
        try:
            res = minimize(fn, x0, method="Nelder-Mead",
                           options={"xatol": 1e-6, "fatol": 1e-6, "maxiter": 2000})
            ll = -res.fun
            fits[name] = {
                "loglik": float(ll),
                "aic": float(2 * k - 2 * ll),
                "params": [float(v) for v in res.x],
            }
        except Exception as e:  # pragma: no cover
            fits[name] = {"loglik": -np.inf, "aic": np.inf, "error": str(e)}

    grid = np.arange(dt, years + dt, dt)
    alive_start = np.array([np.sum(ages >= t - dt) for t in grid], dtype=float)
    deaths = np.array([np.sum((ages >= t - dt) & (ages < t)) for t in grid], dtype=float)
    haz = np.where(alive_start > 0, deaths / np.maximum(alive_start, 1) / dt, np.nan)

    best = min(fits, key=lambda k_: fits[k_]["aic"])
    return {"fits": fits, "best": best, "hazard_grid": grid.tolist(),
            "hazard": haz.tolist(), "n_deaths": int(obs.size), "n_censored": n_cens}


SPECIES_PRESETS: dict[str, dict] = {
    # Literature-motivated degradation parameter presets. HONEST FRAMING (see
    # exp4): these encode *claimed* species differences as monotone orderings
    # of the full degradation stack (connexin decay, metabolic noise, damage
    # seed, inflammaging engine, vital fragility). The model reproduces the
    # ORDERING and coarse magnitude classes, but Gompertz-family dynamics
    # compress lifespan RATIOS (the Strehler-Mildvan alpha-beta tradeoff) —
    # the full 57x mouse->bowhead span is not reachable with plausible
    # parameters, which we report as a documented structural limitation.
    "mouse":          {"lambda_gap": 0.050, "kappa_noise": 0.070, "theta_drift": 0.075,
                       "seed_rate": 5.0e-4, "h_sys": 0.120, "mortality_k": 0.150,
                       "observed_lifespan_yr": 3.5},
    "rat":            {"lambda_gap": 0.046, "kappa_noise": 0.065, "theta_drift": 0.070,
                       "seed_rate": 4.2e-4, "h_sys": 0.115, "mortality_k": 0.140,
                       "observed_lifespan_yr": 4.5},
    "naked_mole_rat": {"lambda_gap": 0.025, "kappa_noise": 0.040, "theta_drift": 0.038,
                       "seed_rate": 2.3e-4, "h_sys": 0.092, "mortality_k": 0.105,
                       "observed_lifespan_yr": 30.0},
    "human":          {"lambda_gap": 0.030, "kappa_noise": 0.048, "theta_drift": 0.045,
                       "seed_rate": 6.0e-5, "h_sys": 0.080, "mortality_k": 0.080,
                       "observed_lifespan_yr": 80.0},
    "bowhead_whale":  {"lambda_gap": 0.020, "kappa_noise": 0.032, "theta_drift": 0.032,
                       "seed_rate": 2.5e-5, "h_sys": 0.070, "mortality_k": 0.060,
                       "observed_lifespan_yr": 200.0},
    "hydra":          {"lambda_gap": 0.0, "kappa_noise": 0.0, "theta_drift": 0.0,
                       "seed_rate": 0.0, "h_sys": 0.0, "mortality_k": 0.0,
                       "observed_lifespan_yr": 1400.0},  # negligible senescence
}
