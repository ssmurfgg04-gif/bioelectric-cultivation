# Night log — memory carryover

Per-run lessons appended after each overnight session; the next night reads
this file BEFORE starting. Knowledge lives here, not in any chat.

## Night 1 — 2026-09-15 (executed in-sandbox as the research agent; the
DeepScientist binary itself is still pending install on the user's box)

### Thread B — Stage 2 repair (exp29) — COMPLETE, all criteria PASS

- exp27's S2P1 refutation root-caused: `regrow()` was cell-autonomous and
  theta diffusion was un-gated — regeneration never touched the junction
  network, so PlanformDB's innexin record could not constrain the model.
- Repair recipe (reusable for future data-vs-model gaps): (1) find the
  pathway the record says must matter; (2) make the mechanism ADDITIVE and
  bit-exact at neutral settings — gate RNG draws so untouched paths are
  trajectory-identical; (3) run the FULL test suite (the real no-collateral
  gate); (4) re-run the falsifying experiment UNCHANGED, thresholds
  untouched; (5) pre-register the before/after criteria before the after-run.
- New predictions registered and awaiting data: S2R3 monotone dose-response
  (3.28/3.93/4.54/6.03 mV at gap 1.0/0.5/0.25/0.05); S2R4 graded penetrance
  under full blockade (1/3 seeds). PlanformDB has dose-resolved innexin
  experiments — check them next.
- Watch-item: the S2P1 flip is marginal at seed level (1/3 cross 6.0 mV).
  If the widened slice keeps landing within noise of the threshold, promote
  `blastema_readout_noise` from hand-picked to pre-registered-fitted with
  its own criterion.

### Thread A — CEM continuation (exp30) — COMPLETE, X1 REFUTED (that is the result)

- disc28 is certified at (or within 0.02 of) the competitive optimum:
  held-out +0.0079 vs the +0.02 bar. DO NOT re-search the competitive
  8-dim space at this protocol again — the frontier has moved to the
  Stage 2 quest.
- Search-side (+0.022) vs held-out (+0.008) divergence is the
  search-seed-overfit signature at pop 24 / 10 iters. Future searches:
  hold out seeds from the start, or cap at ~+2 iters with early stop on
  elite stability.
- Ops lessons, paid for in wall-clock: (a) background processes do not
  survive between tool calls in the sandbox — run long jobs in FOREGROUND
  chunks; (b) the cem checkpoint made chunking FREE (resume is exact —
  exercised for real when the first attempt was reaped); (c) Pool(2) on a
  2-core box was ~5x SLOWER than serial with BLAS threads pinned to 1
  (`OMP/OPENBLAS/MKL_NUM_THREADS=1`); (d) `exp28.decode()` omits `h_proc`
  — add it before any `_agg` call.

### Harness verification (both threads)

- disc28 held-out hold reproduces exp28's published 0.683 exactly
  (0.6828) through the resumed path — the eval contract is
  trajectory-faithful across machines and sessions.
- exp27 cutting arm bit-exact across the model repair (3.16 == 3.16).

### Night-two queue (priority order)

1. Widen the Stage 2 slice: ion_channel class (CaV/aquaporin -> voltage
   params) and morphogen class (wnt/beta-catenin -> target polarity),
   pre-registering each mapping BEFORE querying outcomes (exp27/29
   discipline).
2. Per-experiment amputation planes from PlanformDB Region/RemoveAction
   tables -> amputation slices: turns class-level validation into the
   full per-experiment validation.
3. Check S2R3's dose-response prediction against dose-resolved innexin
   experiments in the DB.
4. Novel-prediction enumeration for untested scenarios + preprint skeleton
   in `research/`.
5. When DeepScientist is installed (`ds doctor --runner opencode` green):
   hand it this file + `docs/QUEST_STAGE2_VALIDATION.md` as the quest
   repo seed; its eval contract is exp27/29's `run_arm` + criteria tuple
   for the widened slice.
