# Roadmap (post-review, 2026-11-16)

Goal: **one credible preprint plus one installable library**, not more experiment numbers.

## Done on branch `review-fixes`
- [x] Gompertz MLE handles left truncation (`hazard_and_fits(entry=)`), with a test
- [x] exp447: Gompertz-slope sensitivity, pre-registered. Verdict: no parameter controls β
- [x] Claims audit (`docs/CLAIMS_AUDIT.md`); README status banner rewritten
- [x] Stale "β = h_sys" comments corrected; exp443 and the human substrate annotated
- [x] `pyproject.toml` (installable), `requirements-lock.txt`, `.gitignore` for checkpoints and zips

## Phase 1: choose the primaries (≤ 5, frozen in `docs/PRIMARIES.md` before any run)
Candidates, strongest first:
1. **P1, planarian target memory:** a transient depolarisation rewrites θ and persists across amputation. The dose-response is monotone, and gap-junction block abolishes it.
2. **P2, sustained vs one-shot maintenance:** periodic correction extends median lifespan; a single mid-life correction does not.
3. **P3, aging as information loss:** I(V;M) falls with gap-junction decay *beyond* what a noise-matched null with intact coupling predicts.

## Phase 2: robustness for each primary
- Sobol/Morris global sensitivity over all ~15 parameters
- ≥ 20 seeds, 95% bootstrap CIs
- Null models: shuffled graph; θ frozen (no slow memory); coupling removed
- Ablations: each mechanism removed must break the claim
- Holm–Bonferroni across the primaries

## Phase 3: model repairs the audit asks for
- A mechanism whose time constant sets the Gompertz rate (target: |e(h_sys)| ≥ 0.5 in exp447)
- A units table, and non-dimensionalised dynamics (state what one step is in hours)
- Remove the six dormant channels from the core class, or give each one dynamics and a test

## Phase 4: contact with data
- Fit P1 to held-out Levin-lab voltage data (`research/levin_voltage_series.json`), split before fitting
- Retire or redo cross-species with blind-sourced parameters
- If the human angle is kept, use structural (DWI) connectivity and frame it as a hypothesis generator
- Find a wet-lab collaborator for `docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md`

## Phase 5: ship
- Preprint on P1 + P2 (q-bio.TO), code tagged and archived on Zenodo
- Move `results/` and `research/data` to a Zenodo record; keep only summary JSONs in git
- `experiments/archive/` for everything that isn't a primary
