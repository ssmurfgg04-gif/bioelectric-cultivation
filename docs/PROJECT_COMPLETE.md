# PROJECT COMPLETE — bioelectric-cultivation

**Completion date:** 2026-09-21 · **Final HEAD:** `e38b34b` (main) ·
**Ledger:** L1–L293 + the re-close entry (`docs/FALSIFICATION.md`) ·
**Deposits:** 345+ in `results/`, all git-tracked · **Tests:** 67+ green
+ the 5-test combined deposit/safety sweep.

---

## What the project set out to do

Decode the bioelectric code, in the Michael Levin roadmap's sense: treat
the body's bioelectric layer as software (membrane voltages coupled by
gap junctions storing a morphogenetic target pattern), and ask — with
falsification-first, pre-registered, bit-exact experiments — whether that
software's pattern can be **read** from any substrate, **written** onto
any substrate, and — the hardest star — whether it can be carried with
**no substrate at all**.

## What it achieved

- **Stage 1 — Map (~95%, complete).** The bioelectric control layer,
  its aging model, and its compiler mapped across the anatomical,
  temporal, and channel axes.
- **Stage 2 — Validate (~90%, complete).** The reader validated under
  adversarial, substituted, and stressed media; the premium's structure
  decomposed to its mechanism (the noise-carried fraction).
- **Stage 3 — Engineer (~95%, 101% PASSED).** 10/10 novel anatomies;
  101% of the target set reached; the spec layer proven class-blind
  (exp288) — the frontier is not geometric.
- **Stage 4 — Expand (~90%, closed).** Cross-organism CLOSED;
  autocatalytic CLOSED (100/100 hosts).
- **Stage 5 — Transfer (~90%, 2 of 3 paths CLOSED).** The universal
  reader: CLOSED across media and sizes (n = 100 → 5000, sub-linear,
  n-invariant cost). The universal substrate: CLOSED (100 hosts). The
  zero-substrate path: **blocked, honestly, at 9 formalizations** (see
  below).
- **The history register — the breakthrough chain (exp289–307).** The
  first non-inert channel: a self-history register (`phi_history`) that
  carries the program's own commit sequence. Characterized end-to-end:
  it carries the decode (12/12 hosts, exp289), stores everything
  write-side (exp290), reproduces the Zenodo arithmetic bit-exactly
  (exp291), is self-sourced and dose-peaked (exp292), protects
  super-additively under stress (~29×, exp293), dissolves the
  noise-carried premium (exp294), is plateau-robust and
  cell-identity-specific (exp295), generalizes across channels (exp296),
  composes (exp298–300), changes what the program writes while leaving
  its control structure untouched (exp301), makes the write-time stress
  decode-invisible: the composed carrier protects at +13.13 mV (~18× the
  single register's +0.73), the stress delta under the carrier exactly
  +0.0000 mV (exp302, 12/12 hosts) — and, in the completion-gap session:
  **unblocks the last dormant channel (exp305: ca2 carries at −0.3550 mV
  via the house blend form — the channel sweep closes 4/4; the dormancy
  was form-specific, never structural), closes the spec-layer premium at
  the limit (exp306: the composed union's commit layer is IDENTICALLY the
  target — rho 0.0/0.0 by degeneracy, cvt_rms 0.0 exactly 72/72 — the
  premium was the un-asserted spec's noise structure all the way down),**
  and its write product formalized through the 9th formalization
  (exp307).
- **The final code review + performance pass.** 4 fixes landed (the
  O(n²)-per-step hot-loop cache, the combined deposit/safety test sweep,
  58 untracked deposits recovered from a silent-loss state, the shared
  vectorized classifier), all verified bit-exact — the exp304 deposit
  re-ran byte-identically after the core change. 6 frozen-body debts
  documented (`docs/CODE_REVIEW_FINAL.md`).

## What it proved impossible (the honest negative)

**The zero-substrate star is blocked at 9 formalizations.** A
substrate-independent pattern representation does not exist for this
dynamics, robust across: five static structural metrics (exp68), the
temporal-schedule form (exp162), the gauge quotient (exp244), the
transport form (exp303/304), and — the completion-gap session — **the
zone-indexed form (exp307)**, which tried the project's own pre-named
untried door: the commit stream annotated with the source's per-position
structural classes, re-addressed through the destination's own classes.
The annotated stream transports nowhere (0/130 genuine pairs, the price
+16.23 mV — unchanged from the plain form's +16.28): the structural
classes are 2 nearly-degenerate bins and the within-class zone-phase is
the real carrier of the wiring dependence. The block's final location:
**the pattern lives in the wiring-keyed indexation as much as in the
values; a representation exists only relative to its own wiring — and the
binding is finer than the structural roles.**

The two faces the transport arc did establish:

- the **content face: YES** — the program's commit stream alone, replayed
  into a fresh wiring-only substrate (no spec install, no clamps, no
  encode, no carried state), reconstructs the walked region's pattern to
  0.59 mV (dormant) and **0.05 mV (the composed carrier — near-exact;
  the committed values are the target values identically)**;
- the **transport face: NO** — 0/130 genuine cross-substrate transports
  in every form tried (the bare stream, the carrier's stream, the
  class-annotated stream; the mean price ~16 mV, the stress-degradation
  scale).

## Where the work lives

- **The repo:** `github.com/ssmurfgg04-gif/bioelectric-cultivation`
  (main; the final HEAD `e38b34b`).
- **The ledger:** `docs/FALSIFICATION.md` — every verdict, every
  pre-registration, every gate count, L1 → the re-close entry; **the
  experiment search is documented** (L290c: the full 14-candidate pool,
  3 promoted + 8 rejected with reasons, the cap at 6 of 10).
- **The deposits:** `results/expNNN_*.json` — deterministic,
  fingerprinted, bit-exact-reproducible; the anchors re-verified across
  every session without a single drift.
- **The synthesis deposits:** `docs/SYNTHESIS_FINAL.md` (what the last
  six experiments showed), `docs/CODE_REVIEW_FINAL.md` (the review),
  `results/exp305_ca2_unblock.json`,
  `results/exp306_premium_under_union.json`,
  `results/exp307_zone_indexed_transport.json`.
- **The theory:** `docs/THEORY.md`, `docs/RESEARCH_MAP.md`, and the
  literature anchors in `research/` (Sediqi ionic-history and
  Blattner-TAS hidden-state registers — both independently confirmed by
  exp289's landing).

## What the next researcher should do

1. **Do not re-attack the zero-substrate star through the values or the
   structural roles.** The transport face is closed (0/130 in three
   forms: the bare stream, the carrier's stream, the class-annotated
   stream); the value layer is exhausted (the commits ARE the spec,
   cvt 0.0); the class annotation is nearly vacuous (2 almost-degenerate
   bins). The ONE remaining door is **zone-phase addressing** — a
   wiring-independent within-zone coordinate (addressing cells by their
   position within their zone's span, not by BFS position or structural
   role) — and it is a compiler change, not a dynamics change.
2. **The carrier is ready for transfer work.** The composed union at
   g=1.0 is protective (+13.13 mV), write-side real (the commit layer
   identically the target), structure-preserving, plateau-robust, and
   channel-general (4/4 channels carry). The wetlab companion protocol
   (`docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md`) is the entry point.
3. **The search is documented.** The ledger's L290c records the full
   candidate pool and why the cap closed at 6 of 10 — the rejected
   candidates (the shelf faces, the dose ladders, the wider batteries)
   are polish by the pre-registration bar; do not reopen them without a
   new mechanism hypothesis.
4. **Run the suite first.** `python3 -m tests.run_tests` from the repo
   root — 67+ tests plus the deposit/safety sweep; everything else is
   downstream of that green.
