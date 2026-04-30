# AGENTS.md

Working agreements for any AI coding agent operating inside this repo.

## Source control

- **All work in this folder MUST be tracked by git.** No file is "scratch" — if it's worth creating, it's worth committing.
- **Remote of record:** https://github.com/Xuefei-Zhang/mini-harness
  - All future work syncs to this repo. Do not create parallel/forked tracking elsewhere.
  - `origin` is configured to this URL. Do not change it without asking.
- After any meaningful unit of work (one script, one design doc, one fix), commit immediately with a clear message. Do not batch unrelated changes.
- Push to `origin main` at the end of each working session, and at minimum at the end of each "Day N" of the plan.
- **Never commit secrets.** `.env` is gitignored; only `.env.example` is tracked.

## Commit message style

```
<scope>: <imperative summary, lowercase, <=72 chars>

<optional body, wrap at 80, explain *why* not *what*>
```

Scopes used in this repo: `init`, `chore`, `docs`, `plan`, `dayNN`, `sandbox`, `tools`, `agent`, `harness`, `experiments`.

Examples:
- `day1: env setup, ReAct from scratch, README v2`
- `sandbox: add cgroups v2 memory limit`
- `chore: gitignore allow .env.example`

## Project layout (do not invent new top-level folders without updating PLAN.md)

```
sandbox/   tools/   agent/   harness/   experiments/   docs/   scripts/
```

## Plan adherence

- The single source of truth for what to do next is `docs/plan/PLAN.md`.
- Each day produces a log at `docs/notes/dayNN.md` (≤ 30 lines).
- If the plan changes, update `PLAN.md` in the same commit and explain why in the commit body.

## Code conventions

- Python: 3.12, async-first where it matters, pydantic v2 for any structured data crossing a boundary, `structlog` for logs.
- C++ (sandbox): C++20, no exceptions across the C ABI, all syscalls checked.
- Lint: `ruff check .` clean before any commit that touches Python.
- Tests live next to the code they test (`*/tests/`); run with `pytest -q`.

## What this agent should NOT do

- Do not pull in LangChain / LangGraph / LlamaIndex / vector DBs. The whole point is to build the layers underneath.
- Do not silently add new dependencies. Every new package goes through `pyproject.toml` with a one-line justification in the commit body.
- Do not run live LLM calls unprompted — they cost money. Always show the user what would be sent first when running for the first time in a session.
