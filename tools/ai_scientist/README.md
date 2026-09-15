# The AI-Scientist wiring, v2 (M22 infrastructure)

Rebuilds the M17 trial's environment (see `research/ai_scientist_trial/
README.md`) with two upgrades the trial's verdict demanded:

1. **The template exposes the CURRENT stack surface.** The M17 trial's
   coding loop lost 4 of 5 rounds to the single-zone `pattern_ledger`
   gap because its template only showed exp17-era machinery.
   `templates/bioelectric_fidelity/experiment.py` (in the AI-Scientist
   tree) is now v2: the multi-pattern stack (zones C/A/B/birth,
   `pattern_ledgers`, allocation policies, the potentiation queue),
   with exp23's mortality-timing fix (birth pattern is the target until
   the write — the born-sick trap). Idea quality tracks what the
   generator can see.
2. **Pacing + checkpointing for a 100-idea run.** The proxy
   (`zai_openai_proxy.mjs`) enforces a minimum gap between SDK calls
   and 429-specific backoff (the raw loop lost ~43% of ideas to backend
   rate limits). The driver (`ai_scientist_100ideas.py`) runs rounds of
   12 ideas, refreshes seeds from the pool's Pareto front each round,
   checkpoints after every round (crash-safe; env knobs TARGET_IDEAS /
   ROUND_IDEAS / MAX_ROUNDS for top-ups), and pre-registers the trial's
   18 idea names so only NEW ideas count toward the target.

## Rebuild recipe

```bash
git clone --depth 1 https://github.com/SakanaAI/AI-Scientist.git ~/AI-Scientist
python -m pip install openai backoff anthropic google-generativeai requests
mkdir -p ~/AI-Scientist/templates/bioelectric_fidelity
cp tools/ai_scientist/zai_openai_proxy.mjs ~/somewhere-writable/   # + node_modules
#   symlink: z-ai-web-dev-sdk from the bun global install
bun zai_openai_proxy.mjs 8787 &
cp tools/ai_scientist/run_round.py ~/AI-Scientist/
#   template: experiment.py (v2, from this session's artifacts),
#   prompt.json (frontier-grounded), seed_ideas.json (trial top-8),
#   trial_ideas.json (the M17 18)
export CULTIVATION_ROOT=/path/to/this/repo
export OPENAI_API_KEY=any OPENAI_BASE_URL=http://127.0.0.1:8787/v1
python tools/ai_scientist/ai_scientist_100ideas.py        # or nohup
```

No Semantic Scholar novelty check (the M17 rate-limit lesson): novelty
is vetted offline by `pareto_vet_ideas.py` — the Pareto front on
(Interestingness, Novelty, Feasibility), then one LLM groundedness call
per front idea against our own kill-record (classes:
frontier_advancing / already_falsified_in_stack / duplicate_of_done /
not_implementable_here — the already-falsified class is the one that
matters: "what the failures tell us").

Outputs land in `research/ai_scientist_100/` (committed with M22):
`ideas_pooled.json`, `pareto_vetted.json`, `vetting_report.json`.
