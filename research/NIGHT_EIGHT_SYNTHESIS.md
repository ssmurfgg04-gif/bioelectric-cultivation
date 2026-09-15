# Night-eight research synthesis — the published answers, pieced together

Compiled after exp53 (6-source wave: Europe PMC, PubMed E-utilities,
Crossref, arXiv, OpenAlex, Zenodo), exp53b (targeted verification), and
exp53c (final abstract retrieval). Raw hits: `research/NIGHT_EIGHT_RESEARCH.md`,
`research/NIGHT_EIGHT_VERIFICATION.md`, `research/NIGHT_EIGHT_FINAL.md`;
JSON: `results/exp53*.json`.

## 0. Verification ledger — what is real, what was mis-cited

| Directive claim | Verdict | Verified record |
|---|---|---|
| "Durant et al. 2019, PMID 30824103" (3h window) | **CITATION WRONG, PAPER REAL** — 30824103 is a coconut-cellulose materials paper. The actual 3h-window paper is **MED30799071**, DOI 10.1016/j.bpj.2019.01.029 (Biophys J 2019) | exp53b F1 + exp53c P-3H-2019 |
| Saito 2003, DOI 10.1002/dvdy.10246 (M-L intercalation) | **VERIFIED** — Crossref: "Mediolateral intercalation in planarians revealed by grafting experiments" (Dev Dyn 2003) | exp53 V-ML-INT |
| 4D atlas: ARZ, Mediator 8, underdamped PCG recovery | **VERIFIED VERBATIM** — MED42172041 (2026): "positional control genes recover through self-organizing dynamics analogous to an underdamped control system"; "injury-induced spatial domain termed the anterior regenerative zone"; "Mediator 8 is a critical regulator" | exp53c P-ATLAS4D |
| Blattner TAS geometric memory model | **VERIFIED** — PPRPPR1216581 (2026 preprint): "Hidden regenerative state in planarians: A geometric model of bioelectric memory using Tangential Action Spaces" | exp53 V-TAS |
| Zenodo 21459264 symbol grounding | **VERIFIED** — "Developmental bioelectricity: Syntax, Semantics, and the Inspection Spaces of Bioelectric Morphogenesis" | exp53b F2 |
| Zenodo 18358611 coupling response geometry | **VERIFIED** — "Coupling response geometry in planarian polarity editing" | exp53b F2 |
| Neurobots (Levin-lab 2026) | **VERIFIED** — MED41717829 "Engineered Living Systems With Self-Organizing Neural Networks..." | exp53 V-NEURO |
| Synthetic-construct memory (Pai-line 2026) | **VERIFIED** — PPRPPR1219439 "Behavioral, Physiological, and Transcriptional Mechanisms of Memory in a Synthetic Living Construct" | exp53 V-NEURO |
| egal-1/microtubule polarity substrate (2025) | **VERIFIED** — MED41099308: egal-1 RNAi or colchicine/nocodazole → **ectopic notum at POSTERIOR-facing wounds** | exp53c P-MTUB |
| wnt1/notum 6h timing (Reddien) | **PARTIALLY VERIFIED** — the 3h paper states "earliest known elements begin demarcating differences between anterior and posterior wounds by 6 h"; egal-1 paper: notum wound-induced at anterior-facing wounds is "the earliest known asymmetric regeneration step". Primary timing papers (Felix/Aboobaker notum; Petersen/Reddien wnt1) surfaced only via secondary mentions — flagged for a deeper pull before any 6h-deadline number is treated as exact | exp53 V-WIN-6H |

## 1. The 3h write window (MED30799071) → exp54 build directive

The published mechanism, verbatim: depolarizing the injured tissue during
the **first 3 h** alters gene expression **by 6 h** and produces a
double-headed phenotype **despite confirmed washout** — resting Vmem within
the first 3 h "kick-starts" the downstream pattern. Two quantitative hooks:
(i) the window is EARLY-anchored (first 3 h, not any 3 h), (ii) the 6h mark
is when the transcriptional circuit has already demarcated the two wound
faces — the decision is committed by then.

**Model mapping.** In the model the decision medium is the commitment
chain: each committing cell reads `theta[src]`. A Vmem pulse at the wound
face therefore writes into the chain ONLY for cells committed while the
face (and its relaxing tail) is displaced. This predicts, pre-registered:

- **G1 (fixed-shape geometry)**: identity-shift vs pulse START TIME is
  monotone decreasing with an early saturation plateau (the chain
  re-carries: any pulse covering the first cells writes the whole
  regenerate), a late failure regime (~zero — ZENODO:18358611's "late
  perturbations fail to alter polarity regardless of strength"), and a
  FINITE transition width between them — the same structural form across
  pulse-duration and fragment-size axes (the fixed-shape claim, tested in
  the model).
- **G2 (3h sufficiency)**: a pulse that ends after only the first ~3 h of
  walk time already writes a large fraction of the full-window shift —
  the published "first 3 h suffice".
- **G3 (6h deadline)**: pulses starting after the majority of the walk's
  commitment horizon write ~nothing — the decision medium is gone (the
  model's version of the 6h transcriptional deadline).
- **G4 (persistence + blockade)**: the early-pulse write persists ≥15 h
  and collapses under junction blockade (exp49's established contrasts,
  re-checked at the new pulse timing).

## 2. M-L intercalation (10.1002/dvdy.10246 + graft literature) → exp55

The symmetry hypothesis: both sides carry SYMMETRIC positional values;
M-L intercalation generates L-R positional values along the new axis;
midline tissues implanted laterally induce a **complete ectopic head**.
The published representation lesson: TWO independent position fields
(A-P and M-L), with the midline acting as a SOURCE (boundary condition),
not a wall.

**Build directive** (exp55): a 2D sheet module with two independent
fields and a midline source boundary; grafts transplant stored fields;
intercalation = coupled re-relaxation. Pre-registered gates:
- **S1**: midline-tissue graft into a lateral region → complete ectopic
  head (AP pole re-established; ML field re-intercalates around it).
- **S2**: lateral tissue grafted medially → local intercalary structures
  ONLY on the side where lateral abuts medial (the asymmetry gate).
- **S3**: isograft controls → no ectopic structures (zero collateral).

## 3. Symbol grounding (ZENODO:21459264) → exp56, the reader test

Verified verbatim: the invariant is "a spatial Vmem difference across an
electrically coupled cell collective, preceding structure and read out
into gene expression"; the residual "which map means which form" is the
symbol-grounding problem; meaning sits in the READER ("a frozen lookup or
a dynamical attractor landscape"); **"to produce 'same pattern, different
form' one must perturb the reader, not the pattern"**.

**Model mapping.** The model already has a concrete reader: the M33
neural/pole channel + the M28 phi-spec read — a frozen lookup
(`phi_spec[i] → identity`) with a substrate (Egal-1/microtubule analog).
exp56 holds the CARRIER constant (clamp the entire Vmem pattern through
the walk) and perturbs the READER (disable/attenuate the pole channel and
spec lookup). Pre-registered:
- **R1 (reader is load-bearing under blockade)**: with the pattern held
  constant and junctions down, reader-intact regenerates restore head
  identities; reader-impaired regenerates do NOT — same pattern,
  different form, produced by perturbing only the reader.
- **R2 (carrier-dominated control)**: at full coupling the pattern alone
  suffices; reader perturbation is inert — the grounding asymmetry is
  coupling-conditioned (predicts the experiment needs a junction- or
  read-impaired regime to manifest, exactly like the published GJ-blockade
  phenomenology).
- **R3 (formal statement)**: the model's decoder is a frozen lookup —
  matching the paper's first solution architecture (the second, dynamical
  attractor landscape, is what exp43/exp52 already probed at the substrate
  level).

## 4. TAS (PPRPPR1216581) → exp57, the cryptic re-cut interval

Verified: regeneration stores a **hidden state** revealed on RE-CUT;
"challenge-sensitive cryptic interval **below** the immediate double-headed
threshold" — fragments that regenerate normally can still carry altered
re-challenge outcomes; "stable re-challenge ratios"; fitted re-challenge
penetrance ~15% for immediate single-headed survivors.

**Model mapping.** The model's hidden state is the M31-A anchor coin
(blake2b of the quantized face window) + the phi-spec layer. A re-cut
changes the face position → a DIFFERENT stored window → a different coin.
Pre-registered:
- **T1 (cryptic interval exists)**: among seeds whose IMMEDIATE regen is
  normal (identity error below the outcome threshold), the RE-CUT
  penetrance of abnormal outcomes is >0 — the naive-fragment re-cut
  distribution at the same plane is the control.
- **T2 (ratio stability)**: the re-challenge abnormal-rate is seed-stable
  across independent draws (the published "stable re-challenge ratios").

## 5. The 4D atlas (MED42172041) → two further tests in exp57

- **Underdamped PCG recovery** (verbatim verified): after perturbation
  release, the model's positional field should OVERSHOOT before settling.
  The V-theta loop is a relaxation oscillator pair — the damping ratio is
  a MEASURABLE. If the default parameters are overdamped, that is an
  honest refutation of the model's recovery class and a night-nine
  calibration target (register, do not tune silently).
- **ARZ / Mediator 8** (verbatim verified): the wound-proximal
  multi-lineage domain. Registered as **M35 candidate** (not built
  tonight): a wound-proximal zone readout whose identity source is the
  CONVERGENCE of the fragment's stored identity repertoire at the face.
  Its failure signature targets the record's residual `gj_block|head`
  0.177 (sim currently 0.00 — exp50's owned measurement-layer residual is
  a candidate mechanism-layer reinterpretation; must be tested WITHOUT a
  free failure knob to avoid overfitting).

## 6. Gene-direction arms (egal-1 2025 + notum/wnt1 literature) → exp57

MED41099308: egal-1 RNAi or microtubule destabilization → ectopic notum
at POSTERIOR wounds (→ posterior heads). notum RNAi → tails in place of
heads. Model scoping: the M33 pole channel IS the notum-axis readout.
Pre-registered direction checks on the neural-channel substrate:
- **N1 (pole-loss direction)**: attenuating the pole source flips
  anterior outcomes toward tail/default (notum-RNAi direction).
- **N2 (mis-anchored pole direction)**: a pole read that fires at
  POSTERIOR identities (the egal-1/microtubule-destabilization analog:
  the substrate that normally confines the pole to anterior-facing
  wounds is broken) produces posterior ectopic anterior identities —
  the two-headed direction — while leaving full-coupling arms inert.

## 7. Wet-lab anchor statement (guiding-light alignment)

MED41717829 (neurobots) + PPRPPR1219439 (synthetic-construct memory)
confirm the program anchors: memory in NON-neural contexts,
stimulus-specific, long-term, detectable physiologically and
transcriptionally — the wet-lab analog of M31-A's stored-state minting.
The model's computational arm: the anchor coin IS "memory stored in the
fragment's own state, read at challenge time" — the same architecture the
2026 synthetic-construct paper reports empirically.

## 8. Build order for night eight (this repo)

1. exp54 pulse-timing critical window (fixed-shape scan; 3h/6h semantics).
2. exp55 2D sheet graft/lateral representation (two fields, midline source).
3. exp56 reader-perturbation symbol-grounding test.
4. exp57 TAS cryptic re-cut interval + underdamped damping measurement +
   gene-direction checks + `gj_block|head_tail` n=2 anomaly scoping.
5. Ledger L35+, novel-prediction deposits, night-nine queue.

Citation-correction deposit: the directive's PMID 30824103 is wrong
(coconut cellulose); the correct record is MED30799071 /
DOI 10.1016/j.bpj.2019.01.029. Recorded here and in the ledger.
