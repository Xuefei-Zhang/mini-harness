# Day 17 — Trajectory recording + viewer

## Why this day matters
Trajectories are the **product** of a harness. Eval scores are aggregates over them; debugging is reading them; future RL/SFT data is sampling from them. A good trajectory format pays back compounding interest. A bad one means re-running expensive evals every time you want to look at something.

## Reading (1)
- SWE-agent's trajectory format — https://github.com/princeton-nlp/SWE-agent/tree/main/trajectories
  Look at one `*.traj.json` file. Note what they record vs what they don't.

## Build tasks

### Part A — Trajectory schema (1 hour)
`harness/trajectory/schema.py` — pydantic models:
```python
class StepEvent(BaseModel):
    step: int
    timestamp: datetime
    kind: Literal["llm_call", "tool_call", "stuck_signal", "context_trim"]

class LLMCallEvent(StepEvent):
    kind: Literal["llm_call"] = "llm_call"
    provider: str
    model: str
    request_messages: list[Message]    # full input
    response: CompletionResponse
    latency_ms: int
    cost_usd: float

class ToolCallEvent(StepEvent):
    kind: Literal["tool_call"] = "tool_call"
    tool_name: str
    args: dict
    result: str
    is_error: bool
    duration_ms: int

class Trajectory(BaseModel):
    run_id: str          # uuid
    task: str
    started_at: datetime
    finished_at: datetime | None
    config: dict          # provider, model, tool list, limits
    events: list[StepEvent]   # union via discriminator
    final_answer: str | None
    truncated: bool
    truncation_reason: str | None
    total_cost_usd: float
    total_input_tokens: int
    total_output_tokens: int
```

Persistence: write **JSON Lines** (one event per line) to `trajectories/<run_id>.jsonl`, with a header line containing the run-level metadata (no `events` field). Streaming-friendly, append-only.

### Part B — Recorder integration (1 hour)
Modify `agent/loop/loop.py` to take an optional `Recorder`:
```python
class Recorder:
    def __init__(self, dir: Path = Path("trajectories")):
        ...
    def open(self, run_id: str, task: str, config: dict) -> RecorderHandle: ...

class RecorderHandle:
    def emit(self, event: StepEvent) -> None: ...
    def close(self, final_answer, truncated, truncation_reason) -> None: ...
```
Every LLM call, every tool call, every stuck signal → one event. Synchronously write before the next step (so a crash doesn't lose data).

### Part C — Viewer (3 hours)
`harness/trajectory/viewer.py` — Streamlit app:
```bash
streamlit run harness/trajectory/viewer.py -- --dir trajectories/
```
Features:
- Sidebar: list of trajectories (run_id, task snippet, cost, status)
- Main pane: timeline view, one collapsible card per event
  - LLM calls: show messages, response, token counts, cost, latency
  - Tool calls: show args (pretty JSON), result (with syntax highlighting if code), duration
  - Stuck signals: red banner
- Top of pane: summary stats (steps, cost, success/fail, total time)
- Filter: hide certain event kinds
- Compare mode: pick 2 trajectories side-by-side

Don't over-design — Streamlit is for *you* to debug, not a product.

### Part D — Use it
Re-run yesterday's smoke test with recorder enabled. Open the viewer. Make sure each event renders sensibly.

## Acceptance criteria
- [ ] Schema covers everything the agent loop emits
- [ ] One full trajectory written and replayable
- [ ] Viewer shows it readably; you can navigate and find any specific tool call in < 5 seconds
- [ ] File size: a 30-step trajectory is < 200KB

## Commit message
`harness: trajectory schema (JSONL) + Streamlit viewer`

## If you finish early
Add a `harness.trajectory.export` CLI that converts trajectories to OpenAI fine-tuning format (messages with tool_calls). Future-proofs you for SFT.

## If you fall behind
Skip the Streamlit viewer; cat the JSONL and read by hand. The schema and recorder are the must-haves.
