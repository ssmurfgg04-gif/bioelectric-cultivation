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

---

# Night two — 2026-09-15 (executed directly by the research agent; ds/opencode binaries still absent from sandbox)

## Seeded state at nightfall
- exp29 repair ON MAIN (pending push: afb7cf1 + night-two commits; old token rotated, new token needed from user).
- Quest tasks 3-4 open: widen slice to ion_channel + morphogen classes, per-experiment amputation planes.
- M25 model state: coupling-dependent blastema readout (M1) + junction-gated theta diffusion (M2).

## Work log
- **N2.1 Mining.** FK-graph mapped (RemoveAction.FromAction -> ManipulationAction linked list; *AreaPoint polygons are per-figure frames — unusable without per-image registration, curated NAMES are the ground truth). plane taxonomy pre-registered in planform_mining.py BEFORE any class-x-plane outcome query; drug->protocol map pre-registered (octanol/heptanol/hexanol -> GJ block; EGTA/nicardipine/K/PZQ/SCH-28080 -> ion channel). Corpus: 1,462 outcome-bearing experiments; coverage 0.84.
- **N2.2 Model patch.** regrow(direction='backward') for head-face regeneration — additive, bit-exact at default. Suite green; exp29 re-run: cutting 3.16 == 3.16, all four S2R criteria still PASS.
- **N2.3 exp31 run.** 31 arms x 3 seeds. Results: S2W1 PASS (widened ordering), S2W5 PASS (controls), S2W6 PASS (coverage 0.84), S2W7 exploratory PASS (recorded crosspiece gradient rho=-0.164 p=0.043 — sim direction matches, penetrance 2x overshoots), S2W2/S2W3/S2W4 REFUTED with diagnostics (length-gradient missing; criterion wrong-bio vs plane-invariant record; junction-channel asymmetry artifact). Ledger L14, README M26.
- **N2.4 Bone step retry** — see final section below.

## Night-three queue (priority order)
1. S2W3b re-registration (plane-invariant AP-morphogen criterion) + re-run — cheap, immediate.
2. M26 candidates, one at a time, each pre-registered with exp27-unchanged discipline:
   a. LENGTH-GRADIENT readout: regrow identity interpolation with distance decay (fixes cross_a overshoot; predicted signature: bin-a pred-abn drops 1.00 -> ~0.5, recorded 0.52).
   b. VMEM-GATED COMMITMENT: channel state widens blastema_readout_noise (fixes S2W4; predicted signature: ion_channel arms 0.00 -> >0.3 while cutting arms stay 0.00).
   c. POSTERIOR-FACE regrow for trunk planes (wnt_trunk recorded 0.768 unreachable by one-face topology).
3. S2R3 dose-response literature check (PlanformDB dose-resolved innexin experiments).
4. QUEST task 6: novel-prediction sweep over recorded-NO-data cells.
5. Push pending: user supplies fresh GitHub token -> push afb7cf1 + night-two commits in one go.

## Carryover notes
- Cross-bin medians used for sim arms: a 0.167, b 0.417, c 0.667, d 1.0.
- The specificity clause mistake (S2W3) is a process lesson: pre-register BIOLOGY-LEVEL alternatives (where the identity change shows up), not just thresholds.
- Recorded plane means for reference: cutting tail 0.367 / head 0.502 / trunk 0.308 / cross 0.425; morphogen trunk 0.768; intact-RNAi (none) 0.777.

# Night three — 2026-09-15 (user directive: do all remaining phases; push first; wire zai-sdk into DeepScientist; no opencode)

## Seeded state at nightfall
- main == origin/main at 1da7ca5 (M26 night two pushed FIRST — nothing at risk).
- DeepScientist zai-runner wiring: DONE (branch `zai-runner-wiring` on
  ssmurfgg04-gif/DeepScientist fork). bin/zai-agent.mjs (headless agent
  CLI -> local OpenAI-compatible proxy -> z-ai-web-dev-sdk), ZaiRunner +
  _probe_zai_runner wired via scripts/wire_zai_runner.py (idempotent,
  applied to site-packages + npm copy + source clone; 17/17 anchors).
  `ds doctor --runner zai` performs a REAL end-to-end HELLO probe; the
  z-ai backend is hard rate-limited today (34x 429, zero successes) —
  quota watcher polls every 15 min and will fire doctor on the first
  green probe (scripts/quota_watch.sh, log: zai-selftest/quota_watch.log).

## Work log
- **N3.1 Bit-exact gate.** verify_m26_bitexact.py: exp29 cutting/innexin
  per-seed errors reproduce to 1e-9 through the M26-patched collective;
  suite green (unit + fidelity + D3 semantics + vmem_inference).
- **N3.2 M26 model patch (additive, bit-exact at defaults).** regrow()
  gains length_gradient (intrinsic positional-info extrapolation),
  commitment_noise_scale (Vmem-gated commitment), direction='both'
  (two-face trunk regrowth). No RNG-sequence changes at defaults.
- **N3.3 exp32 (pre-registered gates -> run).** Protocol-drift catch: an
  added 15h post-regen run flipped innexin 0.67->0.33 and broke bit-exact
  gates — corrected to exp31's read-immediately discipline BEFORE
  verdicts. Results: M26C ADOPTED (wnt_trunk@both 1.00, apc_trunk@both
  1.00, cutting_trunk@both 0.00); S2W3b PASS x3 (plane-invariance
  re-registration holds both sides); M26A REFUTED as implemented (local
  slope no-op on head fragments; cross_a 1.00 vs 0.52); M26B REFUTED as
  implemented (i.i.d. noise averages out; err 4.09, rate 0.00 vs 0.45).
- **N3.4 Ledger L15 + README M27.**

## Night-four queue
1. M27 candidate #1: SATURATED length-gradient extrapolation clipped to
   the fragment's own identity repertoire (intrinsic fate-axis bounds) +
   graded penetrance — target: cross_a 1.00 -> ~0.5, D(g1) < D(g0).
2. M27 candidate #2: chain-accumulating commitment diffusion (sd ~
   cns*noise*sqrt(d)) — target: ion_channel_tail rate 0.00 -> ~0.45
   without moving cutting arms.
3. S2R3 dose-resolved innexin check against the exp29 monotone
   prediction (3.28 -> 3.93 -> 4.54 -> 6.03 mV).
4. QUEST task 6: novel-prediction sweep over recorded-NO data cells.
5. ds quest on the bioelectric repo once `ds doctor --runner zai` is
   green (quota-gated).

- **N3.5 exp33 S2R3a.** Timing-semantics pre-registration -> query ->
  directional miss at n=1 (washout 0.365 vs regen-covered 0.000) ->
  ledger L16: REFUTED-as-registered, downgraded UNRESOLVED; octanol
  pulse ladder RegenPeriod=0; S2R3b/c queued (literature extraction).
- **N3.6 Pushed: M27 + exp33 (main) and zai wiring (fork branch).**
