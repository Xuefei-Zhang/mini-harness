# Day 01 — Agent Loop 与 ReAct

> 参考实现：`experiments/day01_react_from_scratch.py`（260 行，3 tools, 4 providers）
> 活体标本：pi-mono `packages/agent/src/agent-loop.ts`

## Why this day matters
你已经写了 ReAct agent，但"写了"不等于"理解了"。面试时会问你：ReAct 为什么有效？Thought-Action-Observation 循环的本质是什么？你的实现和成熟产品比差距在哪？今天通过 pi-mono 源码 + 手写实验来回答。

## 学习流程

### 1. 读 pi-mono 源码（活体标本）
`~/3rd/pi-mono/`
- `packages/agent/src/agent-loop.ts` — **精读**：turn loop 结构、tool call 检测、`executeToolCalls()`、事件发射
- `packages/agent/src/agent.ts` — 浏览：Agent 类如何封装 loop

**思考题**（用自己的话回答）：
- pi-mono 的 agent-loop 是怎么组织循环的？和 ReAct 的 Thought-Action-Observation 对应吗？
- `executeToolCalls()` 里工具执行失败了怎么处理的？
- 事件系统（event emitter）在 loop 里的角色是什么？

### 2. 回答面试问题
参考 `docs/interview_prep.md`：
- **Q1**: 描述一个完整的 agent loop。从用户输入到最终输出，每一步发生了什么？
- **Q3**: 你的 agent loop 和 ReAct paper 中的描述有什么差异？为什么？
- **Q6**: tool use 的完整流程：模型返回 tool_call → 解析 → 验证 → 执行 → 结果返回。每一步可能出错吗？怎么 recover？

### 3. 读背景资料
- ReAct paper：先看 `docs/notes/paper_summaries.md` 中的 "ReAct" 节（5 分钟）。如有兴趣再读原文 [arxiv 2210.03629](https://arxiv.org/abs/2210.03629)
- Anthropic: Building Effective Agents（必读）：[链接](https://www.anthropic.com/research/building-effective-agents) — 只看 "Agents" 部分

### 4. 重读 Day 1 代码
`experiments/day01_react_from_scratch.py`：
- 梳理 Thought → Action → Observation 循环的数据流
- 对比你的实现和 pi-mono 的实现：哪些设计相同、哪些不同？

### 5. 实验：跑 5 个不同任务
用 `experiments/day01_react_from_scratch.py` 跑以下任务（`--provider vllm`），记录每次的结果：
- 简单计算："What is 17 * 23 + 5?"
- 文件读取："Read pyproject.toml and tell me the dependencies"
- 多步推理："What is the factorial of 7?"
- 边界情况："What is 1/0?"
- 模糊问题："What's the weather today?"

记录格式：
| 任务 | 成功/失败 | 步数 | 估算 token | 观察 |

### 6. 写笔记
`docs/notes/day01_review.md`：
- ReAct 机制的核心循环（3-5 句话）
- 你的实现 vs pi-mono agent-loop 的差异
- ReAct 在哪类任务上表现好/差
- 你的 regex parser 是否可靠，遇到什么边界情况

## Acceptance criteria
- [ ] 读通 pi-mono `agent-loop.ts` 的主循环
- [ ] 能回答 Q1 / Q3 / Q6（用自己的语言）
- [ ] 5 个任务的实验记录在 `docs/notes/day01_review.md`
- [ ] ReAct 优缺点分析（5-8 句）

## Commit message
`day1: agent loop study (pi-mono + handwork), ReAct review, 5-task experiment`

## If you finish early
- 对比同一个任务在 vllm vs 云端 provider 下的表现差异
- 提前看 `packages/coding-agent/src/core/tools/bash.ts`（为 Day 2-3 热身）

## If you fall behind
- 跳过补注释，只做 pi-mono 阅读 + 实验记录
