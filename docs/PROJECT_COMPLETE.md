# PROJECT COMPLETE — bioelectric-cultivation

**Completion date:** 2026-09-21 · **Final HEAD:** `0938512` (main) ·
**Ledger:** L1–L290 + the completion entry (`docs/FALSIFICATION.md`) ·
**Deposits:** 342+ in `results/`, all git-tracked · **Tests:** 67+ green
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
  zero-substrate path: **blocked, honestly, at 8 formalizations** (see
  below).
- **The history register — the breakthrough chain (exp289–304).** The
  first non-inert channel: a self-history register (`phi_history`) that
  carries the program's own commit sequence. Characterized end-to-end:
  it carries the decode (12/12 hosts, exp289), stores everything
  write-side (exp290), reproduces the Zenodo arithmetic bit-exactly
  (exp291), is self-sourced and dose-peaked (exp292), protects
  super-additively under stress (~29×, exp293), dissolves the
  noise-carried premium (exp294), is plateau-robust and
  cell-identity-specific (exp295), generalizes across channels (exp296),
  composes (exp298–300), changes what the program writes while leaving
  its control structure untouched (exp301), and — the final session's
  headline — **makes the write-time stress decode-invisible: the
  composed carrier protects at +13.13 mV (~18× the single register's
  +0.73), the stress delta under the carrier exactly +0.0000 mV**
  (exp302, 12/12 hosts).
- **The final code review + performance pass.** 4 fixes landed (the
  O(n²)-per-step hot-loop cache, the combined deposit/safety test sweep,
  58 untracked deposits recovered from a silent-loss state, the shared
  vectorized classifier), all verified bit-exact — the exp304 deposit
  re-ran byte-identically after the core change. 6 frozen-body debts
  documented (`docs/CODE_REVIEW_FINAL.md`).

## What it proved impossible (the honest negative)

**The zero-substrate star is blocked at 8 formalizations.** A
substrate-independent pattern representation does not exist for this
dynamics, robust across: five static structural metrics (exp68), the
temporal-schedule form (exp162), the gauge quotient (exp244), and — the
final session — **the transport form** (exp303/304), which split the
question into two faces and answered both:

- the **content face: YES** — the program's commit stream alone, replayed
  into a fresh wiring-only substrate (no spec install, no clamps, no
  encode, no carried state), reconstructs the walked region's pattern to
  0.59 mV (dormant) and **0.05 mV (the composed carrier — near-exact)**;
- the **transport face: NO** — 0/130 genuine cross-substrate transports
  in either form (the mean price ~16 mV, the stress-degradation scale).

The block's final location is the sharpest result of the arc: **the
pattern lives in the wiring-keyed indexation as much as in the values.**
The write product is a complete representation *relative to its own
wiring* and transports *nowhere*. Any future unblocking attempt must make
the walk order substrate-free (a wiring-independent zone-addressing
scheme) — improving the written values is pointless; under the carrier
they are already within 0.05 mV of the spec.

## Where the work lives

- **The repo:** `github.com/ssmurfgg04-gif/bioelectric-cultivation`
  (main; the final HEAD `0938512`).
- **The ledger:** `docs/FALSIFICATION.md` — every verdict, every
  pre-registration, every gate count, L1 → the completion entry.
- **The deposits:** `results/expNNN_*.json` — deterministic,
  fingerprinted, bit-exact-reproducible; the anchors re-verified across
  sessions without a single drift.
- **The final-session deposits:** `docs/SYNTHESIS_FINAL.md` (what the
  last experiments showed), `docs/CODE_REVIEW_FINAL.md` (the review),
  `results/exp302_composed_stress_face.json`,
  `results/exp303_zero_substrate_8th.json`,
  `results/exp304_transport_rescoped.json`.
- **The theory:** `docs/THEORY.md`, `docs/RESEARCH_MAP.md`, and the
  literature anchors in `research/` (Sediqi ionic-history and
  Blattner-TAS hidden-state registers — both independently confirmed by
  exp289's landing).

## What the next researcher should do

1. **Do not re-attack the zero-substrate star through the values.** The
   transport face is closed; the binding is the indexation. A
   wiring-independent zone-addressing scheme (addressing cells by
   role/zone-fraction rather than by BFS position) is the one untried
   door, and it is a compiler change, not a dynamics change.
2. **The carrier is ready for transfer work.** The composed union at
   g=1.0 is protective (+13.13 mV), write-side real, structure-preserving,
   and plateau-robust. The wetlab companion protocol
   (`docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md`) is the entry point.
3. **The pre-registered open list** (the shelf faces on the carrier, the
   write-side stress face) is small and honest — both are extensions by
   inches, which is why they were not run in the final session.
4. **Run the suite first.** `python3 -m tests.run_tests` from the repo
   root — 67+ tests plus the deposit/safety sweep; everything else is
   downstream of that green.
