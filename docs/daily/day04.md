# Day 04 — Reasoning：CoT（重点）

## Why this day matters
CoT（Chain of Thought）是工业界用得最多的推理增强。你不仅要实现它，还要用数据回答："CoT 在哪些场景下比 baseline 好？好多少？token 代价是多少？"——这就是 research infra language 的起点。

## Reading (1)
- CoT：先看 `docs/notes/paper_summaries.md` 中的 "Chain of Thought" 节（3 分钟）。原文 [arxiv 2201.11903](https://arxiv.org/abs/2201.11903) 只看 abstract 即可。

## Build tasks

创建 `experiments/day04_reasoning_modes.py`：

### 1. CoT（Chain of Thought）— 重点实现
每次 Action 前强制 Thought 步骤：
```
Thought: [分析当前状态，思考下一步，≥ 2 句]
Action: [执行]
Observation: [结果]
```
对比 baseline ReAct（Thought 可选）vs CoT（Thought 强制 + 必须 ≥ 2 句）。

### 2. 实验对比
选 3-5 个需要推理的任务（非简单计算）：
- "Find the bug in this Python sort function"
- "What is the 10th Fibonacci number? Show your work."
- 自己编一个 3+ 步推理任务

对每个任务跑 baseline / CoT，记录：成功、步数、tokens、latency、质量。

### 3. 分析 → `docs/notes/day04_cot.md`
- CoT 在哪些任务上好/差？为什么？
- token 代价：CoT 比 baseline 多消耗多少 token？
- **research infra language**："我在分析 explicit reasoning 对 agent step efficiency 的影响"

## Acceptance criteria
- [ ] CoT 模式实现（Thought 强制执行，≥ 2 句）
- [ ] 3-5 任务的 baseline vs CoT 对比数据
- [ ] 分析笔记

## Commit message
`day4: implement CoT reasoning mode, baseline comparison with 3+ tasks`

## If you finish early
- 尝试 CoT + tool use 的组合：Thought 不仅推理，还说明"为什么选这个 tool"
