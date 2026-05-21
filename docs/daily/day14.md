# Day 14 — Agent Loop v0 + 4 Provider + 博客 2 发布

## Why this day matters
Day 1 的 ReAct 是玩具。今天建的是 W4 跑 SWE-bench 的 agent loop——async、typed、multi-provider、proper tool-call protocol。你的项目从今天开始看起来像真正的 agent runtime。

同时发布博客 2，收尾 W2。

## Reading (1)
- Anthropic [Tool use with Claude](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — 看 request/response shape

## Build tasks

### Part A — Provider 抽象（2 小时）
`agent/providers/base.py`：
```python
class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, messages: list[Message],
                       tools: list[ToolDefinition]) -> CompletionResponse: ...
```
实现：`AnthropicProvider`, `OpenAIProvider`, `DeepSeekProvider`, `QwenProvider`。
内部格式用 Anthropic 的（比 OpenAI 的更通用），其他 provider 在边界处翻译。

### Part B — Agent Loop（2 小时）
`agent/loop/loop.py`：
```python
class Agent:
    async def run(self, task: str) -> AgentResult:
        while not done:
            response = await provider.complete(system, messages, tools)
            if response.tool_uses:
                results = await execute_tools(response.tool_uses)
                messages.extend(tool_results)
            elif response.stop_reason == "end_turn":
                return response
            if step >= max_steps:
                return truncated
```

### Part C — 冒烟测试
`agent/tests/test_smoke.py`：Anthropic provider 下让 agent 读 README.md 并回答。

### Part D — 博客 2 发布（2 小时）
- 草稿 → 2000 字定稿，Claude 润色英文
- 内联 ≥ 3 段代码 + 1 架构图 + 1 性能图
- 发布 dev.to（英文）+ 掘金（中文）

## Acceptance criteria
- [ ] 4 provider 实现 LLMProvider
- [ ] agent loop 冒烟测试通过
- [ ] tool-use 用 tool_use/tool_result blocks（不用 regex）
- [ ] 博客 2 双发

## Commit message
`day14: agent loop v0 + 4 providers + publish blog 2`

## If you fall behind
- 先实现 Anthropic + DeepSeek，OpenAI + Qwen 顺延
