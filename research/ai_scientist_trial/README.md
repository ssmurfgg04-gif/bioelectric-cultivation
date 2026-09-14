# The AI-Scientist Trial (M17)

**What was installed.** SakanaAI/AI-Scientist v1 (github.com/SakanaAI/
AI-Scientist, 14.5k stars), wired to our own LLM backend through a
custom OpenAI-compatible proxy (`scripts/zai_openai_proxy.mjs` in the
workspace, port 8787: `node scripts/zai_openai_proxy.mjs 8787`, then
`OPENAI_API_KEY=any OPENAI_BASE_URL=http://127.0.0.1:8787/v1`). No
external API keys, no cloud models — the whole loop runs on the local
backend. Dependencies: openai, backoff, anthropic, google-generativeai
(import-time), aider-chat (code editing), pymupdf4llm/pypdf/tiktoken
(writeup); pdflatex shim -> tectonic; chktex no-op shim. Two local
patches: torch import made optional, `novel` key defaulted in ideas.

**The template.** `templates/bioelectric_fidelity/` (in the AI-Scientist
tree) runs OUR stack: experiment.py imports the cultivation package and
reproduces the exp17 arms exactly (none 0.584 / archive 0.122 /
anchored_protected 0.911 at I_rec@60). Policy knobs (cadence, budget,
schedule, write timing/amplitude) are exposed for the coding agent.

**What happened.**
1. Idea generation (18 ideas) — genuinely good ones: multi-pattern
   maintenance with competing resource allocation, memory enhancement
   protocols (periodic consolidation / potentiation — directly maps to
   our protected-tier semantics), adaptive pattern evolution
   (plasticity-vs-degradation discrimination), predictive maintenance
   (EMA degradation forecasting). Full list: ideas.json.
2. Autonomous loop on multi_pattern_maintenance: 5 experiment rounds.
   Rounds 1-2 correctly identified that its multi-zone edits did not
   take effect; round 3-4 diagnosed the NaN cascade it had introduced;
   round 5 isolated the root cause: `pattern_ledger()` is single-zone —
   a REAL extensibility gap in our stack. Its run-by-run self-diagnosis
   in notes.txt is honest and accurate.
3. Writeup stage: blocked by Semantic Scholar API rate limits
   (429 on the shared IP; backoff grew past 55 min). Stopped externally;
   the paper was never compiled. Literature search is the only stage
   that requires an unrate-limited network resource.

**What we took from it.**
- The multi-zone gap is now fixed: `pattern_ledgers()` API (commit
  c2c7754) — the AI-Scientist found a real improvement target in our
  ensemble faster than we would have.
- The three strongest generated ideas (multi-pattern allocation,
  enhancement/potentiation protocols, plasticity-vs-degradation) are
  queued as exp23-25 candidates, each pre-registrable.
- Verdict on "might it help this research": YES for idea generation and
  harness-debugging (it reads the stack, proposes literature-grounded
  policies, and finds API friction); NOT YET for autonomous discovery —
  the coding loop needs the harness to expose the right abstractions
  (single-zone ledger blocked it for 4 of 5 rounds), and the paper
  stage depends on rate-limited literature APIs.

**Artifacts in this directory:** ideas.json (the 18 generated ideas),
notes.txt (its run-by-run experiment log), aider_chat.txt (the full
coding-agent transcript), final_experiment.py (its last edit),
run_summaries.json (medians per arm per round).
