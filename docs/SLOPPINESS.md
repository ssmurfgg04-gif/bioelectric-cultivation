# SLOPPINESS LEDGER — the ensemble audit (M17)

Methodological audit of the existing stack, in the spirit of
"fix anywhere we may be sloppy before adding anything new".
Findings ranked by severity. Each row: issue -> evidence -> fix -> status.

## S1 — No uncertainty quantification anywhere (SEVERE)

**Issue.** Every headline number in exp18 (V1 rank 3/10, V4 rho 0.42-0.75)
and exp19 (+23% vs none, +1.2% vs HAND, "all ablations <= 0.01") is a
point estimate over 2-3 seeds. No standard errors, no confidence
intervals, no permutation tests. The plateau conclusion of exp19
("broad plateau, single-dimension ablations shift hold by <= 0.01")
rests on n=3 held-out seeds with no dispersion reported.

**Fix.**
- exp18: permutation p-value for the V1 rank (null = random rank among
  groups); bootstrap CI for the V4 Spearman rho (resample groups).
- exp19: report SE across held-out seeds for every arm comparison;
  declare comparisons |delta| < 1 SE as "indistinguishable" rather
  than "plateau".
- **Status: fixed in exp20+ (stats module) — backfill exp18/exp19
  numbers via the shared stats helpers.**

## S2 — CEM update is unsmoothed (MODERATE)

**Issue.** `cultivation/inverse/cem.py` jumps mu/sigma fully to elite
statistics each iteration. With noisy fitness (exp19 uses 2 CRN seeds
per candidate) unsmoothed CEM is known to oscillate and prematurely
converge (the standard fix: smoothed updates, Szita & Lorincz 2006;
de Boer et al. tutorial §5).

**Fix.** Optional smoothing `smooth=alpha` (mu <- alpha*mu_new +
(1-alpha)*mu_old; same for sigma), default ON with alpha=0.7; keeps
checkpoint format. **Status: fixed (backward-compatible flag).**

## S3 — CEM has no stagnation restart (MODERATE)

**Issue.** Single run, no detection of premature elite collapse. The
variance floor (2% of range) prevents death but not stagnation.

**Fix.** Optional `restart_after` stagnation counter: if best_f
unchanged for k iterations, re-inflate sigma to (hi-lo)/4 around
current best. **Status: fixed (opt-in flag; exp19 baseline unchanged
for reproducibility, new runs use it).**

## S4 — exp19 dead code + blank figure panel (MINOR)

**Issue.** Line 237 `state["elite_k"] = [... for u in []]` always
yields [] (leftover). The fig19 middle panel is `ax[1].axis("off")`
because search history is never stored in the results JSON.

**Fix.** Remove dead line; store CEM history (per-iteration best + mu)
in state and plot best-f trace. **Status: fixed.**

## S5 — Spearman with ties handled crudely (MINOR)

**Issue.** exp18 implements Spearman as argsort-of-argsort; ties (common
in gene-family expression sums) get arbitrary distinct ranks, biasing
rho slightly.

**Fix.** Use scipy.stats.spearmanr (average ranks for ties) in the
shared stats module; keep the old function only as a cross-check.
**Status: fixed (stats module; exp18 re-run uses it).**

## S6 — V1 rank granularity is coarse (MINOR, transparency)

**Issue.** "Neoblast rank 3/10" ranks among ~10 GROUPED cell-type
buckets, not the 51 (PSCA) / 58 (Fincher) annotated clusters. The
README states this honestly but the headline number is coarser than
the data.

**Fix.** Also report the cluster-level rank where annotations map
1:1 (neoblast clusters), and state both. **Status: fixed in exp20
(PSCA cluster-level ranks added to the report).**

## S7 — Ablations reuse the held-out seeds (MINOR)

**Issue.** exp19 ablations are evaluated on the same seeds 31-33 as
the headline comparison — mild double-dipping (ablation deltas share
noise with the baseline they are compared to).

**Fix.** Note it explicitly in the results JSON (done); new
experiments use disjoint ablation seeds. **Status: noted, exp20+
uses disjoint seeds.**

## S8 — vmem_inference permeability floors untested (MINOR)

**Issue.** GENE_WEIGHTS floors (PK 0.05, PNa 0.02, PCl 0.05) are
hardcoded; the weight jackknife covers gene weights but not the
floors.

**Fix.** Floor-sensitivity check added to the stats module (perturb
floors +-50%, re-rank). **Status: fixed (added to exp20 report).**

## S9 — Dataset-hunting discipline (PROCESS)

**Issue.** The user's directive: search-first, do not re-hunt what
exists; improvements before new rigs. This ledger exists to enforce it.

**Fix.** Every new experiment must (a) cite the exact source of every
external number, (b) pre-register criteria before results are seen,
(c) include a kills-row if it is a validation experiment.
**Status: standing rule.**
