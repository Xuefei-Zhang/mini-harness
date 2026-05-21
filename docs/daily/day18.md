# Day 18 — Agent Failure Analysis + Trajectory Replay + 博客 4

## Why this day matters
比 Subagent 更重要。真正做 harness 的团队最看重"理解 agent 为什么失败"。今天从实验数据中归纳失败分类、实现 trajectory replay。面试时这是"研究味道"的集中体现。

## Build tasks

### 1. Trajectory Taxonomy（失败分类）
从 Day 14-17 的实验中收集 50+ 次失败，归纳为 8 类：
```
| 类型              | 描述                                    |
|-------------------|----------------------------------------|
| ToolFailure       | tool 参数错误/调用失败                     |
| PlanningFailure   | 任务分解错误                              |
| ContextFailure    | 关键信息丢失（context 被裁剪导致）            |
| ExecutionFailure  | shell/runtime 出错                        |
| ReasoningFailure  | 推理偏航（hallucinated file path 等）       |
| RecoveryFailure   | retry 无效，陷入死循环                     |
| StaleState        | working state 过时导致错误决策              |
| PrematureFinish   | 过早完成任务                              |
```
→ `docs/notes/day18_failure_taxonomy.md`

### 2. Failure Rate 分析
`harness/failure/analyzer.py`：
```python
class FailureAnalyzer:
    def classify(self, trajectory: Trajectory) -> list[FailureEvent]: ...
    def summary(self, trajectories: list[Trajectory]) -> FailureSummary: ...
```
- 自动扫描 trajectory JSONL → 标注每类失败的次数和比例
- 分析：哪些 harness 机制能减少哪类失败（working state → PlanningFailure↓, context manager → ContextFailure↓）

### 3. Trajectory Replay
`harness/failure/replay.py`：
```python
async def replay(trajectory_path: Path) -> None:
    """重放 saved trajectory，不调用 LLM（用 recorded responses）"""
    # 用途：debug harness、复现某次失败、对比不同 context 策略的效果
    ...
```

### 4. 博客 4 — 《Coding Agent Failure Taxonomy：从 N 次 trajectory 中归纳的 8 类失败模式》
- 核心论点：coding agent 的失败可以分类、可以分析、可以通过 harness 机制缓解
- 数据：你的 failure rate 表
- 每种失败类型的代码片段（trajectory 中的真实例子）
- 哪些 harness 机制对哪类失败有效
- **research infra language**："我在分析 failure recovery policy 对 pass@k 的提升"

## Acceptance criteria
- [ ] 8 类失败分类 + 分析笔记
- [ ] FailureAnalyzer 能自动扫描 trajectory
- [ ] Trajectory Replay 可用
- [ ] 博客 4 发布

## Commit message
`harness: failure taxonomy (8 classes) + trajectory analyzer + replay + blog 4`

## If you fall behind
- 5 类失败分类 + analyzer，replay 简化为"读取 JSONL 重放"
