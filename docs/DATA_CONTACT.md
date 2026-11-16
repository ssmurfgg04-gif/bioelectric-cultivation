# Phase 4: Contact with Data

## What the data allows
`research/levin_voltage_series.json` holds 119 entries. Of these, 99 are PlanformDB outcome records; two absolute mV values exist, both from adjacent models (*Xenopus*, BETSE), and **none from planarian tissue**. The planarian record is DiBAC₄(3) *relative* polarity, outcome frequencies, and timing.

A held-out **quantitative** voltage fit is therefore impossible with the data in hand. Fitting P1's mV parameters to it would be fitting noise. Earlier claims to have matched these data (exp39) are direction matches on 6 pairs that were chosen with the model in view, so they are not held out.

## What P1 predicts that a wet lab can falsify
These are model predictions, stated before any wet-lab data. Translating clamp mV into a pharmacological dose needs a calibration experiment (step 1 below).

| # | Prediction | Falsified if |
|---|---|---|
| W1 | The fraction of two-headed regenerates is a **sigmoidal** function of depolarisation dose. Model half-effect is near −28.6 mV, about 57% of the way from the trunk potential (−40 mV) to the head potential (−20 mV). | the dose curve is flat, or step-like at a single dose |
| W2 | A rewrite that survives one re-cut survives the next (P1 arm A: 20/20 after 2 rounds) | persistence decays across successive re-cuts |
| W3 | GJ block *alone* does not rewrite (arm B: 0/20) | GJ block alone yields head-likeness comparable to arm A |
| W4 | Blocking the slow re-setting of resting potential (the θ analogue, e.g. inhibiting ion-channel transcription during the exposure) **abolishes** persistence (arm C: 0/20) | persistence survives transcriptional block of channel expression |
| W5 | Two-headed probability is a steep function of exposure **duration** at a fixed dose. Slowing resting-potential re-setting shifts the duration curve right by the same factor (model: collapse at ε·T ≈ 0.65, exp456) | the duration curve is flat, or the shift is not proportional |


W4 is the one prediction the model makes that the original experiments do not already contain. It is the experiment worth proposing to a collaborator.

## Concrete next steps
1. **Calibration:** DiBAC₄(3) imaging of posterior fragments across 5 doses of a depolarising agent. This maps dose to relative depolarisation and replaces the mV axis of W1 with a measured one.
2. **Collaborator:** take `docs/STAGE5_WETLAB_COMPANION_PROTOCOL.md` plus W1–W4 to a planarian lab (e.g. the Allen Discovery Center at Tufts, or a regional zoology department with planarian husbandry).
3. **Cross-species:** retired (CLAIMS_AUDIT A4) until presets come from blind-sourced measurements.
