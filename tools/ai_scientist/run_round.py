"""One AI-Scientist idea-generation round (run as a subprocess by the driver).

Isolates crashes: generate_ideas() writes ideas.json only at round end,
so a crashed round costs at most ROUND_IDEAS worth of LLM calls.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("OPENAI_API_KEY", "any")
os.environ.setdefault("OPENAI_BASE_URL", "http://127.0.0.1:8787/v1")
os.environ.setdefault("CULTIVATION_ROOT", "/home/z/my-project/repo")
sys.path.insert(0, "/home/z/AI-Scientist")

from ai_scientist.llm import create_client          # noqa: E402
from ai_scientist.generate_ideas import generate_ideas  # noqa: E402

n = int(sys.argv[1]) if len(sys.argv) > 1 else 12

client, model = create_client("gpt-4o")
ideas = generate_ideas(
    "/home/z/AI-Scientist/templates/bioelectric_fidelity",
    client=client,
    model=model,
    max_num_generations=n,
    num_reflections=5,
)
print(f"[round] complete: {len(ideas)} ideas in ideas.json")
