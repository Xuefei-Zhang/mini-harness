# Day 01 — ReAct 回顾 + 实验记录

> 原始代码已完成：`experiments/day01_react_from_scratch.py`（260 行，3 tools, 3 providers）
> 今日是回顾：补齐理解和实验数据。

## Why this day matters
你已经写了 ReAct agent，但"写了"不等于"理解了"。面试时会问你：ReAct 为什么有效？Thought-Action-Observation 循环的本质是什么？和其他推理模式比优劣在哪？今天用实验数据回答这些问题。

## Build tasks

### 1. 重读 Day 1 代码
- 补完整注释：每一段代码的 WHY（不是 WHAT）
- 梳理 Thought → Action → Observation 循环的数据流

### 2. 实验：跑 5 个不同任务
用 `experiments/day01_react_from_scratch.py` 跑以下任务，记录每次的结果：
- 简单计算："What is 17 * 23 + 5?"
- 文件读取："Read pyproject.toml and tell me the dependencies"
- 多步推理："What is the factorial of 7?"
- 边界情况："What is 1/0?"
- 模糊问题："What's the weather today?"

记录格式：
| 任务 | 成功/失败 | 步数 | 估算 token | 观察 |

### 3. 写笔记
`docs/notes/day01_review.md`：
- ReAct 机制的核心循环（3-5 句话）
- 你的实现和原始 paper 的差异
- ReAct 在哪类任务上表现好/差
- 你的 regex parser 是否可靠，遇到什么边界情况

## Acceptance criteria
- [ ] Day 1 代码补了注释
- [ ] 5 个任务的实验记录在 `docs/notes/day01_review.md`
- [ ] ReAct 优缺点分析（5-8 句）

## Commit message
`day1: review ReAct implementation, 5-task experiment, analysis notes`

## If you finish early
- 对比同一个任务在 3 个 provider 下的表现差异

## If you fall behind
- 跳过补注释，只做实验记录
