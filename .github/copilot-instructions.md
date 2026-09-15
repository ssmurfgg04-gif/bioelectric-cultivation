# Copilot instructions — bioelectric-cultivation house rules

This repo runs falsification-first computational biology: a bioelectric
cell-collective model is validated against published planarian
experimental data (PlanformDB 2.5.0, in `data/planform/`). Non-negotiable
discipline when generating or editing code here:

## Bit-exactness discipline

- `cultivation/bioelectric/collective.py::regrow()` is the regeneration
  mechanism. New capabilities MUST be additive keyword parameters that
  are INERT at their defaults: identical RNG draw sequence, identical
  floating-point operations when the parameter is at its default.
- Before proposing any model change, run:
  `python3 scripts_dev/verify_m26_bitexact.py` — exp29's recorded
  per-seed errors must reproduce to 1e-9. Then `python3 -m tests.run_tests`.
- Never "clean up" float expressions in the step/regrow hot paths;
  `x * 1.0 + 0.0 * y` patterns are load-bearing bit-exactness guards.

## Pre-registration discipline

- Every experiment (`experiments/expNN_*.py`) writes its criteria INTO
  the docstring BEFORE the outcome query runs. Never edit a criterion
  after seeing results; re-register under a new name (see S2W3 -> S2W3b
  in README) and record the change in `docs/FALSIFICATION.md`.
- Serial execution with BLAS threads pinned:
  `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`.
- Results go to `results/expNN_*.json`, deterministic given seeds.

## Where things live

- `docs/FALSIFICATION.md` — the ledger (Level N per experiment).
- `docs/NIGHT_LOG.md` — overnight research loop log + next-night queue.
- `README.md` — milestone sections (M-numbers).
- `docs/QUEST_STAGE2_VALIDATION.md` — the Stage 2 quest spec.
- Runner wiring for DeepScientist: fork branch `zai-runner-wiring`
  (z-ai-web-dev-sdk backed runner; `ds doctor --runner zai`).
