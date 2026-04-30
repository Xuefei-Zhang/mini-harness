# Day 02 — Async Python, pydantic, structured logging

## Why this day matters
Every modern agent framework is async because tool calls and LLM calls are I/O-bound. As a C++/systems engineer your Python is probably synchronous and dataclass-based — that ages you on sight in a Python-shop interview. Today you migrate Day 1 to the stack the rest of this project will use: **asyncio + httpx.AsyncClient + pydantic v2 + structlog**.

## Reading (1)
- Real Python, *Async IO in Python: a complete walkthrough* — https://realpython.com/async-io-python/
  Stop after the section "Using a Queue". You will not need streams, subprocess-async, or third-party libraries today.

## Build tasks

Create `experiments/day02_async_react.py` from scratch (do not edit day01). Mirror day01's behavior but:

1. **Pydantic models** for every wire-crossing structure:
   ```python
   class ToolCall(BaseModel):
       thought: str
       action: Literal["calc", "read_file", "finish"]
       args: dict[str, Any]

   class StepRecord(BaseModel):
       step: int
       prompt_tokens: int
       completion_tokens: int
       latency_ms: int
       tool_call: ToolCall | None
       observation: str | None
   ```
2. **Async LLM client** — one `httpx.AsyncClient` shared across the whole process.
   - Provider classes: `AnthropicAsync`, `DeepSeekAsync`, `OpenAIAsync` — all expose `async def complete(system, messages) -> LLMResponse`.
3. **Async tools** — even `calc` is `async def` for uniformity. (Real tools will be I/O-bound later.)
4. **Concurrent benchmark**: at the bottom add a `bench()` coroutine that runs 10 ReAct sessions concurrently with `asyncio.gather`, on tasks like:
   ```
   tasks = [
       "compute 17 * 23 + 5",
       "compute 2**16 - 1",
       "compute 999/37",
       ... 7 more arithmetic tasks ...
   ]
   ```
   Print: total wall time, per-task wall time, total tokens, $$.
5. **structlog** with JSON renderer — every step emits one log line you can grep.

## Acceptance criteria
- [ ] `python experiments/day02_async_react.py --task "17*23+5"` works
- [ ] `python experiments/day02_async_react.py --bench` runs 10 tasks; wall time ≤ 1.5× the slowest single task (proves real concurrency, not serial dressed up)
- [ ] All structured data is `BaseModel`, no raw dicts crossing function boundaries
- [ ] One JSON log line per step, captured to `runs/day02-<timestamp>.jsonl`

## Commit message
`day2: async ReAct with pydantic + httpx + structlog, 10-task concurrent bench`

## If you finish early
- Add `--provider all` that runs the same task across all 3 providers and prints a comparison table (cost, latency, success).

## If you fall behind
- Skip structlog, just `print()`. But don't skip pydantic or async — those are the point.
