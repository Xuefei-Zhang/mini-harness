# Day 15 — Agent loop v0 + multi-provider LLM client

## Why this day matters
Day 1's ReAct was a toy. Today you build the loop you'll *actually use* for SWE-bench in W4 — async, typed, multi-provider, with proper tool-call protocol (not regex on text). This is where your project starts looking like a real agent runtime.

## Reading (1)
- Anthropic, *Tool use with Claude* — https://docs.anthropic.com/en/docs/build-with-claude/tool-use
  Read the full page once. Pay attention to the request/response shape — that becomes your canonical internal format.

## Build tasks

### Part A — Provider abstraction (2 hours)
`agent/providers/base.py`:
```python
class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str | list[ContentBlock]

class ToolDefinition(BaseModel):
    name: str
    description: str
    input_schema: dict  # JSON schema

class ToolUseBlock(BaseModel):
    id: str
    name: str
    input: dict

class ToolResultBlock(BaseModel):
    tool_use_id: str
    content: str
    is_error: bool = False

class CompletionResponse(BaseModel):
    text: str
    tool_uses: list[ToolUseBlock]
    stop_reason: Literal["end_turn", "tool_use", "max_tokens", "stop_sequence"]
    usage: Usage   # input/output tokens, cost in USD

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, messages: list[Message], tools: list[ToolDefinition]) -> CompletionResponse: ...
```

`agent/providers/anthropic.py` — wraps the Anthropic SDK, native tool-use.

`agent/providers/openai.py` — wraps OpenAI SDK, translates their `function_call` shape to your internal types.

`agent/providers/deepseek.py` — uses OpenAI-compatible API, model `deepseek-chat`.

`agent/providers/qwen.py` — uses Dashscope OpenAI-compatible endpoint.

The internal canonical format is **Anthropic-shaped** (it generalizes more cleanly than OpenAI's). Other providers translate at the boundary.

### Part B — Agent loop (2 hours)
`agent/loop/loop.py`:
```python
class Agent:
    def __init__(self, provider: LLMProvider, tools: list[Tool], system: str,
                 max_steps: int = 30):
        ...

    async def run(self, task: str) -> AgentResult:
        """Run until end_turn or max_steps. Returns final assistant text + trajectory."""
```

Loop body:
1. `complete()` with current messages
2. If response has `tool_uses`: execute each (sequentially; parallel comes Day 16), append `tool_result` blocks
3. If `stop_reason == "end_turn"` or no tool_uses: return
4. Increment step; if `step >= max_steps`: return with `truncated=True`

Tools are async callables registered as:
```python
class Tool:
    name: str
    description: str
    input_schema: dict
    handler: Callable[[dict], Awaitable[str]]
```

Reuse Day 12 tools (read_file/write_file/run_shell/search_code) — for now wire them directly without going through MCP. (MCP integration on Day 17.)

### Part C — Smoke test
`agent/tests/test_smoke.py`: with the Anthropic provider, ask the agent to *"Use read_file to read README.md and tell me how many components there are"*. Assert it ends correctly.

## Acceptance criteria
- [ ] All 4 providers implement `LLMProvider`
- [ ] Agent loop runs the smoke task with Anthropic provider successfully
- [ ] Tool-use happens via real tool_use/tool_result blocks (no regex parsing)
- [ ] `pytest agent/tests/test_smoke.py` passes (mock the provider for non-API CI)

## Commit message
`agent: provider abstraction (4 backends) + tool-use agent loop v0`

## If you finish early
Add cost tracking — every CompletionResponse has $ amount; Agent.run returns total cost.

## If you fall behind
Implement only Anthropic + DeepSeek today. OpenAI + Qwen can slot in Day 16.
