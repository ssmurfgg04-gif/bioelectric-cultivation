# DeepScientist overnight optimization — plan summary

Consolidated status + plan for running DeepScientist as the overnight optimizer for
this repository's intervention search. The install is the bone; everything else is
wiring. Nothing here is a framework.

## 1. Where things stand

| Item | Status |
|---|---|
| WSL2 Debian | done — up and running |
| Python 3.13 + Node 22 (in WSL2) | done — installed |
| opencode CLI | pending — npm came back empty, needs a retry (or skip straight to the Ubuntu box) |
| DeepScientist | not installed yet — everything above was prerequisite for exactly this |

All prerequisite work so far existed for one thing: installing DeepScientist. Nothing
built so far is the platform; it is toolchain.

## 2. The bone — the whole plan

1. **Finish the toolchain** — opencode in WSL2 (retry the install), or skip straight
   to the Ubuntu box.
2. **Install DeepScientist** — done when `ds doctor --runner opencode` is green.
3. **One quest, end to end** — eval contract, seeded baseline, pilot, overnight run.
4. **Nothing else.** The dropped items below stay dropped.

Explicitly dropped (non-goals):

- the research-engine merge repo
- the scaffold (already deleted)
- the four-layer platform
- Magg
- vendoring anything

The other 10 clones sit in `_upstream/` as reference and on-demand parts — nothing
else gets built unless DeepScientist proves insufficient somewhere.

## 3. The wiring — eight additions that make it work

None of these is a framework. Together they are the difference between
"DeepScientist installed" and "overnight optimization running."

| # | Wire | What it adds |
|---|---|---|
| 1 | **opencode runner auth** — provider + model in opencode config; `ds doctor --runner opencode` green | DeepScientist runs on the existing muse-spark setup. No new API keys, no new bills to configure. |
| 2 | **Eval contract** — one script: candidate policy in, float out, timed | Turns a generic research loop into *this repo's* optimizer. The only custom code in the whole project. |
| 3 | **Baseline + falsification seeding** — best CEM policy and ledger contents loaded as the quest's starting point | Night one starts from the policy that already beats the hand-tuned baseline, not from zero. Without this, the first overnight is wasted rediscovery. Sources: `results/exp25_cem_competition.json` (discovered vs hand arms), ledger: `docs/FALSIFICATION.md`. |
| 4 | **Simulator access** — bioelectric modules importable/callable from wherever quests execute (direct import or a tool wrapper) | The agent can actually *run* candidates instead of describing them. |
| 5 | **Overnight loop config** — step cap, per-step timeout, guaranteed termination, morning deliverable format (best snapshot, baseline delta, failure log) | You sleep, it stops, and the morning is readable in five minutes. |
| 6 | **Outside hypotheses (v1)** — Sakana-style ideation feeding quest inputs on demand | Ideas from outside the framework's blind spots, without adopting v1's templates or paper path. |
| 7 | **Skills on demand** — 2–3 K-Dense skills when a quest needs a domain method (e.g. a stats or bioinformatics procedure) | Method knowledge without vendoring 158 skills. |
| 8 | **Memory carryover** — per-run lessons appended to the quest repo; next night reads them | Compounding — night 12 is smarter than night 1, and the knowledge survives outside any chat. |

Wiring that already has a home in this repo: the eval contract scores candidate
intervention policies against the simulator (`cultivation/inverse/cem.py` is the
search whose output is the candidate stream); the seeded baseline is the discovered
policy from `results/exp25_cem_competition.json`.

## 4. Open threads (non-blocking)

- **opencode install retry** in WSL2, whenever a local validation box is wanted.
- **G1 review**, when the Ubuntu-box AI reports back.

Neither blocks the main path.

## 5. Night-one definition of done

1. `ds doctor --runner opencode` green.
2. Quest repo initialized with the eval contract script and seeded state
   (best CEM policy + falsification ledger contents).
3. Pilot run completes one full step within the per-step timeout.
4. Overnight run terminates on its own, by cap or by convergence.
5. Morning readout, readable in five minutes: best snapshot, delta vs seeded
   baseline, failure log.
