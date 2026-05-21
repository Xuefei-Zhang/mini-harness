# Day 06 — 精读 opencode 源码

## Why this day matters
你用 opencode 日常编程。读它的源码是 W1 最高 ROI 活动：学习 (a) 生产级 agent 代码长什么样，(b) 面试官会问的抽象，(c) 博客中会用的词汇。今天只看 **tool dispatch** 和 **session state**。

## Build tasks

### 1. 读 opencode 源码
重点追踪：
- **Tool 调用序列化**：模型返回的 tool_call 如何解析、验证、执行？
- **Permission 系统**：哪些 tool 需要用户确认？permission 怎么设计？
- **Session 管理**：session 的 state 怎么维护？messages 怎么存储？
- **Context Window 处理**：context 快满了怎么裁剪？

### 2. 画架构图
excalidraw → `docs/design/opencode-arch.png`：
- 核心模块及其关系
- tool dispatch 数据流
- session state 存储方式

### 3. 笔记 → `docs/notes/day06_opencode.md`
- 3-5 个设计最巧妙的地方
- 2-3 个可以改进的地方
- 1 个可以直接用到 mini-harness 的想法

## Acceptance criteria
- [ ] opencode 的 tool dispatch + session state 源码读通
- [ ] `docs/design/opencode-arch.png` 架构图
- [ ] `docs/notes/day06_opencode.md` 笔记

## Commit message
`day6: opencode source analysis, architecture diagram, notes`

## If you finish early
- 开始看 claude-code 源码（逆向 npm 包），对比 opencode 差异

## If you fall behind
- 只看 tool dispatch，跳过 permission
