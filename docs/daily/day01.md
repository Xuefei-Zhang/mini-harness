# Day 01 — Bootstrap & ReAct from scratch

> Already executed. This file exists for completeness; the actual log is at `../notes/day01.md`.

## Why this day matters
Establishes the project skeleton, picks the toolchain you'll live in for 30 days, and forces you to *write* a ReAct loop with no framework — so every later abstraction has a baseline to compare against.

## Reading (1)
- Anthropic, *Building effective agents* — https://www.anthropic.com/research/building-effective-agents
  Skim once for vocabulary (workflow vs agent, prompt chaining, routing, orchestrator-workers, evaluator-optimizer, reflection). You will reference these patterns all month.

## Build tasks
- Repo scaffold under `~/self/mini-harness/`
- `pyproject.toml` with anthropic / openai / httpx / pydantic / structlog / typer
- `scripts/setup.sh` — one-shot bootstrap
- `experiments/day01_react_from_scratch.py` — ReAct, 3 tools (`calc`, `read_file`, `finish`), 3 providers (Anthropic SDK, DeepSeek raw HTTP, OpenAI raw HTTP)

## Acceptance criteria
- [x] `./scripts/setup.sh` succeeds on a clean clone
- [x] `python experiments/day01_react_from_scratch.py "What is 17*23+5?"` returns `396`
- [x] At least one provider runs end-to-end with real API key

## Commit message
`day1: env setup, ReAct from scratch, README v2`
