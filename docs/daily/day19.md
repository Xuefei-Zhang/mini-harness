# Day 19 — Multi-Agent（lightweight：planner/executor/reviewer）

## Why this day matters
JD 要求"Multi-Agent"。工业界实际大量用的是"planner → executor → reviewer"三角色流水线，不是"5 agent 辩论"。只做这个，不深挖。

## Build tasks

### 1. 三角色流水线
`agent/multi_agent/triad.py`：
```python
class PlannerAgent:
    """接收任务 → 分解子任务 → 输出 plan"""

class ExecutorAgent:
    """执行每个子任务 → 汇报结果"""

class ReviewerAgent:
    """检查 executor 输出 → approve / request changes"""

async def triad_pipeline(task: str, provider: LLMProvider) -> TriadResult:
    plan = await planner.run(task)
    for subtask in plan.subtasks:
        result = await executor.run(subtask)
        review = await reviewer.check(result)
        if review == "changes_needed":
            result = await executor.fix(subtask, review.comments)
    return TriadResult(plan, results)
```

### 2. 实验
`experiments/day19_triad.py`：
- 任务："实现一个 HTTP todo API（CRUD + 测试）"
- 对比：单 agent vs 三角色流水线的输出质量（代码行数、测试覆盖率、bug 数）

### 3. 分析
`docs/notes/day19_multi_agent.md`：
- 三角色流水线比单 agent 在哪些指标上好/差？
- token 代价：三角色 = 3× context，是否值得？
- 什么场景适合用 multi-agent，什么场景单 agent 就够了？

## Acceptance criteria
- [ ] planner/executor/reviewer 流水线实现
- [ ] 实验对比数据
- [ ] 分析笔记

## Commit message
`agent: lightweight multi-agent — planner/executor/reviewer triad pipeline`

## If you fall behind
- 只做 planner + executor，reviewer 简化为"run tests"
