# Direct comparison to the published voltage record (exp39)

Status: COMPLETE — 6/6 published direction claims MATCH the model.
Instrument: `experiments/exp39_levin_voltage.py`, results
`results/exp39_levin_voltage.json`. Abstracts fetched via Europe PMC
REST (the z-ai search backend is quota-gated; free channel used).

## Honest scope

The planarian bioelectric record is published as RELATIVE quantities —
dye-ratio polarities (DiBAC4(5) etc.), depolarized-vs-hyperpolarized
contrasts, and outcome frequencies. ABSOLUTE mV values for planarian
tissues are not published. The model's absolute scale (head -20,
trunk -50) is an exp1 calibration choice, not a fit to these papers.
What the record can test — and what this comparison tests — is every
published DIRECTION/ORDERING claim against the model's corresponding
quantity, extracted fresh from the sim.

## The table

| # | Published claim | Source | Model quantity | Verdict |
|---|---|---|---|---|
| V1 | Depolarization is essential for anterior identity; "depolarization drives head formation, even at posterior-facing wounds" | Beane 2011, PMID 21276941 | WT axis: head -24.9 mV > tail -50.3 mV (depolarized head) | MATCH |
| V2 | H,K-ATPase RNAi hyperpolarizes -> shrunken heads, disproportional anatomy | Beane 2013, PMID 23250205 | ion_channel tail arm abnormal 1.00 vs cutting 0.00 | MATCH |
| V3 | GJ/neural modulation induces ectopic ANTERIOR blastemas at posterior wounds | Oviedo 2010, PMID 20026026 | posterior-quarter depolarization (wnt_ protocol) -> head-likeness at tail 0.95 >= 0.7 | MATCH |
| V4 | innexin smedinx-11 RNAi inhibits regeneration; mixed/graded outcomes; AP neoblast gradient | Oviedo 2007, PMID 17670787 | sustained gap_scale=0.05 -> M25 blind-guess readout, rate 0.67 (mixed) | MATCH |
| V5 | Wounds depolarize relative to intact tissue | wound-current literature / Beane 2011 manipulations | wound face -38.0 mV > settled body mean -43.6 mV | MATCH |
| V6 | Stochastic regenerative phenotypes under identical perturbation; bistable pattern memories | Pezzulo & Levin 2021, PMID 33550952 | exp38 amended re-anchor arm splits seeds ([16.5, 14.7, 2.8] mV); exp12 B6 latch | MATCH |

## What this buys, and what it does not

The model's polarity skeleton (depolarized head, hyperpolarized trunk,
depolarized wounds, depolarization->head identity, junction-carried
readout, stochastic penetrance) agrees with every direction claim the
published record makes. It does NOT establish absolute-value fidelity
(unpublished for planarians), organ-size scaling (Beane 2013's
blastema-amount vs identity distinction — the model extends identity,
not size; named missing layer), or the neoblast-gradient substrate
(no neoblast layer). Those remain honest gaps; exp37's L21 shift table
is the corpus-scale version of the same statement.
