# Day 07 — 精读 aider + SWE-agent + 博客 1

## Why this day matters
完成 W1 最后一块。aider 和 SWE-agent 是现代 coding agent 两大基石。读完它们 + 发布博客 1，W1 才算真正结束。

## Build tasks

### 1. 读 aider 源码
重点：
- **Repo Map**：如何在 token budget 内给模型展示代码库概览？
- **Edit 格式**：search-replace 为什么比 diff 更可靠？
- **Git 集成**：怎么用 git 做 safety？

### 2. 读 SWE-agent 源码
重点：
- **ACI（Agent-Computer Interface）**：action space 怎么设计？
- **Observation 裁剪**：命令输出超长时怎么处理？
- 读 [SWE-agent paper](https://arxiv.org/abs/2405.15793) method section

### 3. 架构图
- `docs/design/aider-arch.png`
- `docs/design/swe-agent-arch.png`

### 4. 博客 1 — 《从系统工程师视角写一个 Agent Harness：30 天从零到 SWE-bench》
- 你是谁（系统工程师背景）
- 为什么做这个项目
- 项目架构总览（sandbox / tools / agent loop / eval / memory / subagent）
- 技术栈和为什么不用 LangChain
- W1 学到的东西（ReAct / Prompt / Reasoning）
- 接下来的计划

中英双发：掘金 + dev.to

## Acceptance criteria
- [ ] aider + SWE-agent 源码笔记
- [ ] 三张架构图（opencode + aider + SWE-agent）
- [ ] 博客 1 发布

## Commit message
`day7: aider + SWE-agent notes, 3 arch diagrams, blog 1 published`

## If you fall behind
- 博客先发中文版，英文后续补
