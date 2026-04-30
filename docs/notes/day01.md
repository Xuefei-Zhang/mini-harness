# Day 1 — 2026-05-01

## Plan (hourly)
- 09:00–12:00  Register API keys (Anthropic / DeepSeek / Qwen / OpenRouter); `scripts/setup.sh`; verify `.env`
- 13:00–15:00  Read Anthropic *Building effective agents*; take notes (3 key takeaways)
- 15:00–17:00  Read ReAct paper (arxiv 2210.03629); summarize the loop in 5 sentences
- 17:00–21:00  Implement `experiments/day01_react_from_scratch.py` (no framework)
- 21:00–22:00  Run 3 sample tasks; commit; write this log

## What I built
- Repo scaffold + 30-day plan in `docs/plan/PLAN.md`
- `.env.example` + `pyproject.toml` (anthropic, openai, httpx, pydantic, structlog)
- `scripts/setup.sh` — one-shot bootstrap (uv venv, sync deps, smoke import test)
- `experiments/day01_react_from_scratch.py` — minimal ReAct agent in ~220 lines
  - 3 tools: `calc` (safe AST eval), `read_file`, `finish`
  - 3 providers: Anthropic SDK, DeepSeek (raw HTTP), OpenAI (raw HTTP)
  - regex-based step parser; alternating user/assistant message protocol

## Pitfalls hit
- uv's default index (PyPI direct) timed out from CN; switched to Tsinghua mirror via `~/.config/uv/uv.toml`. Saved ~20 min next time.
- Multiple stale `uv` processes from earlier killed runs held the cache lock; needed `pkill -9 uv` before re-syncing.

## Tomorrow top 3
1. asyncio + httpx async port of day01 → `day02_async_react.py` (run 10 tasks concurrently, measure speedup)
2. Replace dataclass-based response with pydantic models; add structured logging
3. Start reading opencode source — focus on `tool/` + `session/` packages

## Stats
- Code lines (project total): ~280 Python + setup script
- Commits: 1
- API spend: $0 (no live runs yet — keys to be filled tomorrow)
