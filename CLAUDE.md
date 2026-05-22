# CLAUDE.md — mini-harness project instructions

> For any AI agent (Claude/other) picking up this project. Read this before starting work.

## Quick context
- **Project**: 30-day from-scratch agent harness, targeting DeepSeek Agent Harness Engineer
- **User**: 7 years system software (C/C++/Linux), new to agent harness + TypeScript
- **Single source of truth**: `docs/plan/PLAN.md` — check §10 status table for progress
- **Agent context**: `docs/AGENT_CONTEXT.md` — full project overview

## Environment
- **Local LLM**: vLLM Qwen3.6-27B-FP8 on `localhost:9070` (systemd `vllm-fp8`). Default provider.
- **Manage**: `vllm_fp8 {start|stop|status|report}`
- **API keys**: `.env` not tracked. Use cloud providers only when API-specific features are needed.

## Learning flow (IMPORTANT)
The user studies each module by reading `~/3rd/pi-mono/` source code BEFORE building in mini-harness.

```
Daily flow:
1. docs/daily/dayNN.md          → today's tasks + acceptance criteria
2. docs/notes/pi-mono-learning-map.md → pi-mono files for this module
3. ~/3rd/pi-mono/               → read the referenced source files
4. docs/interview_prep.md       → answer corresponding interview questions
5. Discuss with user            → correct understanding until user can answer independently
6. experiments/                 → hand-write Python experiments, run with --provider vllm
7. docs/notes/dayNN.md          → write summary (≤30 lines)
```

## Paper reading
- User prefers `docs/notes/paper_summaries.md` (Chinese summaries) over original papers
- Only Anthropic "Building Effective Agents" is marked as required full reading
- Never assume the user has read a paper — point to the summary first

## Daily workflow rules
- Tasks can be done in ANY order — quality + learning notes = complete
- User confirms completion → update status in PLAN.md §10
- Each day produces a note at `docs/notes/dayNN.md` (≤30 lines)
- Commit after each meaningful unit; push to `origin main` at end of session

## Code conventions
- Python 3.12, async-first, pydantic v2, structlog, `from __future__ import annotations`
- No LangChain / LangGraph / vector DBs
- Every new dependency needs one-line justification in commit body
- Lint: `ruff check .` before commits
- Tests: `*/tests/`, run with `pytest -q`

## Git / commit rules
- Push to `origin main` at end of each working session
- `.env` is gitignored; never commit secrets
- Commit style: `<scope>: <imperative summary, lowercase, <=72 chars>`
- Scopes: `init`, `chore`, `docs`, `plan`, `dayNN`, `sandbox`, `tools`, `agent`, `harness`, `experiments`
- Always Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>

## What NOT to do
- Don't run live LLM calls unprompted — use vLLM (local, free) unless user specifies
- Don't pull in LangChain / LangGraph / LlamaIndex / vector DBs
- Don't silently add new dependencies
- Don't create scratch files — everything git-tracked
- Don't take destructive git actions without confirmation
- **Don't write the experiment code for the user.** The daily experiments (e.g., Day 1 ReAct from scratch) are *hand-writing exercises* — the user learns by coding them themselves after reading the pi-mono source. Your job is to prepare the environment, explain what's needed, then wait for the user to write. If you start implementing the experiment, you're defeating the purpose. Instead, set up deps, describe the requirements, and say "you write it, ask me if stuck."
