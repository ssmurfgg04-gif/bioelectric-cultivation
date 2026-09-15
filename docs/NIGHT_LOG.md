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
- **N3.7 exp34 M27 candidates.** M27b chain diffusion ADOPTED (ion_tail
  0.00->1.00, S2W4 artifact resolved); M27a REFUTED structurally
  (head-fragment theta carries no tail-ward trend) -> M28 dual-field
  candidate registered (theta expression + phi positional map). L17.
- **N3.8 Pushed exp34 + M27 params.**

## Night-four queue (updated)
1. M28 DUAL-FIELD: add phi (positional-coordinate layer) — fragment-
   surviving, re-anchors at wound faces; regrow identity = phi readout
   blended with theta chain (M25 coupling gating applies to BOTH
   readouts). Target: cross_a 1.00 -> ~0.5 without moving tail/head/trunk
   (they are already 0.00) and keeping restored/intact controls 0.00.
2. Channel-slice penetrance dampening: cns/diffusion mapping for
   ion_channel arms to land ~0.45 instead of 1.00 (dose-style scan).
3. S2R3c: resolve ExperimentDrug timing semantics from primary
   literature; extract the octanol/heptanol dose series.
4. QUEST task 6: novel-prediction sweep over recorded-NO cells.
5. ds quest on the bioelectric repo when `ds doctor --runner zai` is
   green (quota watcher running).
- **N3.9 exp36 M28 phi scan.** Length-gradient refutation RESOLVED
  (cross_a 1.00->0.00, zero collateral, innexin preserved); penetrance
  binary vs recorded graded — night-five candidate: stochastic
  spec-expression layer. L19. Adopted candidate mapping phi=0.75.
- **N3.10 Pushed M29 (phi layer + scan).**

## Night-five queue (updated)
1. Stochastic spec-expression layer: per-seed spec availability (fragment
   size x expression noise) on top of phi_readout — target: cross_a
   seed-splitting (~0.52), bins b/c/d graded (0.43/0.27/0.27).
2. Plane-dependent readout for innexin|head (record 0.00 vs sim 1.00):
   head-specific readout channel (exp35 L18 candidate).
3. Channel-slice dose scan (cns x diffusion grid) against ion trunk 0.46.
4. S2R3c: ExperimentDrug timing semantics from primary literature.
5. ds quest on the bioelectric repo when `ds doctor --runner zai` is
   green (quota watcher still running).
- **N3.11 DeepScientist quest registered.** Quest 001 created (runner:
  zai, default_runner switched in config.yaml), goal = night-five queue
  (stochastic spec-expression, innexin|head plane-dependent readout,
  channel dose scan) with the house discipline inline. `ds run` preflight
  correctly refuses while the z-ai backend is 429-ing. Watcher v2
  (scripts/quota_watch.sh) polls every 15 min: on first green probe it
  runs `ds doctor --runner zai`, and when green launches quest 001 and
  babysits it until the 19:00 UTC (22:00 Nairobi) cutoff.
- **N3.12 Wiring bugs fixed (fork branch).** Two wire_zai_runner anchor
  bugs shipped earlier were caught when the launcher rebuilt its venv:
  metadata.py entry landed outside the dict (IndentationError); the
  daemon import got glued onto a prefix anchor (ImportError). Both fixed
  in all trees, patcher now carries a py_compile gate; fork branch
  zai-runner-wiring force-pushed with the fix (d227b4e). `ds doctor
  --runner zai` reaches a REAL end-to-end probe — everything green
  except the externally quota-gated model call.

## Night four/five — 2026-09-15 (executed directly by the research agent; z-ai backend quota-gated all day — quest 001 executed by the primary agent per the user's standing fallback directive)

### Seeded state at nightfall
- main @ a237145; fork zai-runner-wiring @ d227b4e; quest 001 registered (runner zai), blocked on 429.

### Work log
- **N4.1 ZAI quota resolved per user directive.** Probe confirmed 429 on chat + web_search. Fallback: the primary research agent executed quest 001's goal directly (this night); Europe PMC free REST used for all literature fetches (no key, not rate-limited). The zai runner stays wired for when quota opens.
- **N4.2 exp38 M30** (ledger L20): per-cell spec-expression REFUTED — the chain RE-CARRIES the spec blend (the mechanism insight behind the sharp phi transition). Amended per-blastema re-anchoring splits seeds (q=0.55 -> 0.67) but flips the marginal innexin seed via RNG-stream shift -> NOT adopted. M31: anchor availability as stored fragment history.
- **N4.3 exp37 full sweep** (L21): 1,029/1,462 experiments mapped per-experiment (coverage 0.704, 36 arms, adopted state). Plane ordering rho +0.80 PASS; class ordering REFUTED (other_rnai 0.80 vs sim 0.00 — missing gene layer + bias); MAE 0.595 REFUTED with the SYMMETRIC signature (no-perturbation undershoots, perturbation overshoots). M32: threshold fitting.
- **N4.4 exp39 Levin comparison** (L22): 6/6 published direction claims MATCH (Beane 2011/2013, Oviedo 2007/2010, Pezzulo/Levin 2021). Absolute mV honestly scoped unpublished.
- **N4.5 exp40 dose scan** (L23): grid monotone in diffusion; ion|trunk RESOLVED at (cns=1, diff=1.0); S2R3c closed — untested not falsified, novel-prediction deposit.
- **N4.6 exp41 Stage 3 compiler** (L24): restorative + two-head compilation verified 3/3 (zero search); safety refusal PASS; coupling precondition load-bearing PASS; ectopic novel-anatomy REFUTED by 0.22 mV + latch amendment REFUTED (different signature) -> v1 hybrid latch+spec rule. Verifier substring bug caught+fixed.
- **N4.7 exp42 Stage 4 light cone** (L25): propagation + fragmentation + junction-scaled dose-response (rho=1.00) PASS; memory CONE-BOUNDED (LC-G4 refuted w/ power diagnosis) — the instrument explains the 24h rewrite requirement.
- **N4.8 exp43 Stage 5 substrate independence** (L26): mechanism transfers universally (M25 corruption 12-22 mV, regen 1.1-4.5 mV); attractor existence is substrate-conditioned (boundary-to-volume ratio of the target partition; degree normalization probed, insufficient). Compiler R5 (substrate-aware partitioning) registered.

### Night-six queue (priority order)
1. M31: stored per-cell anchor availability at pattern set (stream-neutral penetrance; prediction: seed-splitting without regrow-time RNG, fragment-size correlation).
2. innexin|head plane-dependent readout (exp35's +1.00 gap — the head-specific protection channel).
3. Compiler v1: hybrid latch+spec rule (CP-G3' signature), then R5 substrate-aware partitioning + per-substrate eps/mu calibration (exp43 signature).
4. M32: pre-registered-fitted threshold (exp37's shift table is the fitting target; exp29 watch-item).
5. 24h-pulse light cone (LC-G4's power diagnosis: whole-body cone + residue).
6. ds quest 001 via zai runner when quota opens (watcher v2 still pointed at it).

## Night six — 2026-09-15 (executed directly by the research agent; research directive first per the user's standing instruction)

### Seeded state at nightfall
- main @ 51d3706 (all five stages opened night four/five); night-six queue registered.

### Work log
- **N6.1 exp44 RESEARCH WAVE** (the user's standing directive: "you could already have answers on the web — search deeply, piece them together"): 14 Europe PMC queries mapped to the queue; raw abstracts in research/NIGHT_SIX_RESEARCH.md; the pieced-together answers in research/NIGHT_SIX_SYNTHESIS.md. Four items got direct literature answers: M31 (Ross 2022 constitutive positional info + wound reset), innexin|head (Lobo 2019 neural vector transport + egal-1/microtubule 2025), compiler v1 (Pezzulo/Levin 2017 cryptic gradient — the stored gradient is what regen reads), 24h window (the same 2017 protocol perturbs DURING regeneration). Pushed 5152956.
- **N6.2 exp45 M31** (L27): registered stored-history threshold REFUTED — the settle history is seed-INVARIANT at macro scale (drifts 4.14/4.21/4.26, spread 0.12 mV). AMENDED M31-A isolated re-anchoring: the per-blastema draw is minted from the fragment's own stored state (blake2b digest of the quantized face window) — deterministic per fragment, ZERO self.rng contact — ALL 6 GATES PASS at q=0.50 (split 1.00->0.33, collaterals 0.00, innexin drift 0.00, straddle [T,F,T]). ADOPTED. collective.py: anchor_from_history + spec_reanchor_isolated (additive, bit-exact at defaults). Pushed 6ee40da.
- **N6.3 exp46 M33** (L28): non-junctional neural/muscle polarity channel — ALL 5 GATES PASS. innexin_head 1.00->0.00 (record 0.00); posterior immunity (tail 0.67 bit-exact); full-coupling inert; dose monotone; zero collateral. The exp35 innexin|head +1.00 gap — the LAST unexplained Stage-2 arm signature — RESOLVED. Novel prediction: gjblock_head toward normal. collective.py: neural_readout + NEURAL_SPEC_MIN. Pushed 3e105f9.
- **N6.4 exp47 compiler v1** (L29): CP-G3' RESOLVED — v0's latch chased the clamps halfway (window ended with the gradient HALF-WRITTEN); R1'' latch-write ends the window with latch := spec (the 2017 state-writable-gradient semantics): ectopic third-head verifies 3/3 (errs ~2.6 vs ~7.0). Registered disjunction resolved: the WRITE alone suffices (R2'' blend decorative for this class). R5 substrate-aware partitioning (b2v <= 0.10) reproduces exp43's signature exactly (path 0.0101/grid 0.0611 compilable; random-3 0.3533/scale-free 0.4873 refused; margins >=1.5x). ALL 6 GATES PASS. THE GOLDEN CORE THRESHOLD IS FULLY CROSSED. anatomy.py + morpho_engineering.py hybrid regen. Pushed f99b33f.
- **N6.5 exp48 M32** (L30): single-threshold REFUTED on the held-out class (train optimum 13.0 mV, MAE 0.313->0.154, but ion_channel generalizes worse: 0.446 vs 0.192) — the corpus residual is STRUCTURAL (per-class mechanism gaps), not a threshold artifact. G4: the M31-A split survives any threshold (straddles at 13.0). M34 (gene-expression class layer) registered. Pure re-analysis. Pushed 8e17ea3.
- **N6.6 exp49 regen-window light cone** (L31): LC-G4 RESOLVED — the rewrite regime is the REGEN WINDOW. 2h pulse during the walk writes 2.44 mV across the whole regenerate (intact: 0.00 — contrast amendment PASS); persists 15h; collapses to 0.00 under blockade (the instrument's missing guess-mix was caught via the blocked-arm profile and corrected — the model's r-mix decays the delta x0.05/commit); dose saturates (chain-re-carries at the light-cone level); DIRECTIONALLY ASYMMETRIC cone (face 2.44 vs 5-anterior 0.00) — novel optogenetics prediction. Pushed 853bb5b.
- **N6.7 Docs**: FALSIFICATION L27-L31, README night-six inventory, this log.

### Stage scoreboard after night six
- Stage 1 炼气 complete | Stage 2 筑基 COMPLETE at slice+corpus-instrument level (every arm-level signature explained) | Stage 3 金丹 compiler v1 verified incl. ectopic novel anatomy (Golden Core threshold fully crossed) | Stage 4 元婴 light cone complete (rewrite regime named; directional-cone prediction) | Stage 5 飞升 mechanism universal / form substrate-conditioned, enforced at compile time.

### Night-seven queue (priority order)
1. M34: gene-expression class layer (the structural gap exp48 pinned — cutting/other_rnai underprediction at corpus scale).
2. M31-A fragment-size correlation scan (the night-five prediction: small regenerates all-or-nothing, large concentrate near the mean — now testable with the adopted mechanism).
3. R5 per-substrate eps/mu calibration (the compiler's per-substrate operating point, exp43's registered follow-up).
4. Corpus re-pass with M33: the gjblock_head plane-resolved prediction (toward normal) against PlanformDB.
5. Directional-cone optogenetics prediction write-up (exp49 G5) as a formal novel-prediction deposit.
6. ds quest 001 via the zai runner when quota opens (watcher v2 still pointed at it).
