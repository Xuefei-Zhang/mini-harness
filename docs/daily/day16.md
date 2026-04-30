# Day 16 — Context management, retries, stuck-detection

## Why this day matters
The interview question is never "did you write a loop?" — it's "what happens at step 47 when the context window is 90% full and the model just emitted the same wrong action three times?" Today is the day you have answers.

## Reading (1)
- Anthropic, *Long context tips* — https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips
  Skim. Then read the prompt-engineering section on "putting examples and document content earlier" — relevant to what you trim later.

## Build tasks

### Part A — Context window manager (3 hours)
`agent/loop/context.py`:
```python
class ContextManager:
    def __init__(self, max_tokens: int, reserved_for_completion: int = 4096):
        ...

    def fit(self, messages: list[Message]) -> list[Message]:
        """Return a (possibly trimmed/summarized) message list that fits."""
```
Strategy (implement all three; pick by config):
1. **`drop_oldest`** — remove oldest non-system messages until under limit. Keep tool_use/tool_result pairs together (never orphan a tool_result).
2. **`summarize_oldest`** — when over limit, take the oldest N turns, ask the model "Summarize the following in 200 tokens preserving any decisions made and files touched", replace those turns with one assistant message.
3. **`hierarchical`** — keep most-recent K turns verbatim; summarize anything older once, into a single rolling summary block.

Token counting: use the provider's `count_tokens` if available, else `tiktoken` for OpenAI-family and Anthropic's beta token-counting endpoint.

### Part B — Retry layer (1 hour)
`agent/loop/retry.py` — wrap every provider call:
- HTTP 429 / 529 / 5xx → exponential backoff with jitter, max 5 attempts
- Token budget exceeded → bubble up (don't retry)
- Tool execution exception → format as `tool_result` with `is_error=True` and let the model recover; do **not** retry from the agent loop's side
- Hard timeout per call (default 120s) using `asyncio.timeout`

### Part C — Stuck detection (1 hour)
`agent/loop/stuck.py`:
```python
class StuckDetector:
    def observe(self, tool_use: ToolUseBlock, result: str) -> StuckSignal | None:
        """Return a StuckSignal if the agent appears stuck."""
```
Heuristics:
- **Repeated identical tool_use** (same name + same input) ≥ 3 times → `RepeatedAction`
- **Same tool, alternating between 2 inputs** ≥ 4 times (ABAB) → `Oscillation`
- **N consecutive tool errors** (configurable, default 5) → `ErrorCascade`
- **No file write in last K=10 steps** when task involves coding → `NoProgress`

When a signal fires, the Agent appends a system-flavored user message:
```
"You appear to be stuck (signal: RepeatedAction). Reconsider your approach.
Possible options: try a different tool, ask for clarification, or use the finish tool with what you have."
```
Single-shot — if it fires twice in a row, abort the run with `truncated=True, reason="stuck"`.

### Part D — Tests
`agent/tests/test_context.py` — feed 100 fake messages, assert each strategy produces a valid trimmed list (no orphan tool_results, under limit).
`agent/tests/test_stuck.py` — synthetic sequences trigger each signal exactly once.

## Acceptance criteria
- [ ] All three context strategies pass their tests
- [ ] Retry layer survives a flaky mock provider that fails 50% of calls
- [ ] Stuck detector unit tests green
- [ ] Run `experiments/day15_smoke.py` again — should still pass with all the new layers active

## Commit message
`agent: context manager (3 strategies) + retry + stuck detection`

## If you finish early
Add a `replay` mode: given a saved trajectory JSONL, replay it without LLM calls (uses recorded responses) — invaluable for debugging.

## If you fall behind
Implement only the `drop_oldest` context strategy and the `RepeatedAction` stuck signal. Skip retry layer (the SDKs have basic retries built-in).
