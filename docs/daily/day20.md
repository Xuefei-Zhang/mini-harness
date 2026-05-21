# Day 20 — Subagent 调度器

## Why this day matters
JD 要求"Subagent"。→ 服务于长任务：长任务中主 agent 需要 spawn 子 agent 做并行工作（如同时分析 3 个文件、并行跑测试）。

## Build tasks

### 1. Subagent 抽象
`agent/subagent/runner.py`：
```python
class SubagentConfig(BaseModel):
    task: str                      # 子任务描述
    tools: list[str] | None = None # 可用工具（默认继承父 agent）
    memory_isolated: bool = True   # 独立 working state
    max_steps: int = 15
    timeout_seconds: int = 120

class SubagentResult(BaseModel):
    answer: str
    steps: int
    cost_usd: float
    trajectory: list[dict]
    error: str | None

class SubagentSpawner:
    async def spawn(self, config: SubagentConfig) -> SubagentResult: ...
    async def spawn_many(self, configs: list[SubagentConfig],
                         mode: str = "parallel") -> list[SubagentResult]: ...
```

### 2. 调度模式
- **sequential**：按顺序执行，后一个可以看到前一个的结果
- **parallel**：同时 spawn，用 `asyncio.gather` → 长任务中并行是关键

### 3. 结果回收 + 错误传播
- 子 agent 完成后，结果注入主 agent 的 working state
- 子 agent 失败时：retry / skip / abort
- 超时处理：`asyncio.timeout`

### 4. 实验
`experiments/day20_subagent.py`：主 agent 收到任务"分析这个 repo 的代码质量和测试覆盖率"，spawn 两个子 agent（并行）：
- 子 agent A：分析代码质量（read_file + search_code）
- 子 agent B：检查测试覆盖率（run_shell: pytest --collect-only）

## Acceptance criteria
- [ ] SubagentSpawner 实现（spawn + spawn_many, sequential + parallel）
- [ ] 错误传播（timeout / error / max_steps）
- [ ] 实验跑通

## Commit message
`agent: subagent orchestrator — sequential/parallel spawning with error recovery`

## If you fall behind
- 只做 sequential，parallel 用 asyncio.gather 一行代码
