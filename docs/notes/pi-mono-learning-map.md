# pi-mono 学习路径映射

> 把 pi-mono 的源码作为"活体标本"，按招聘要点逐个解剖。
> 每个模块：读 pi-mono 代码 → 回答面试问题 → 讨论 → 手写实验。
>
> pi-mono clone: `~/3rd/pi-mono/`
> 已有架构地图: `~/3rd/pi-mono/learning-journal/notes/architecture-map.md`

---

## 使用方法

1. 选一个下面的模块（按 mini-harness Day 顺序，但跳跃/并行也可以）
2. 读 pi-mono 对应代码文件
3. 找到面试问题，用自己的话写出答案
4. 和我讨论，直到能不看资料回答清楚
5. 回到 mini-harness 做 handwork 实验 + 写总结

---

## 映射表

### Agent Loop (Day 1-2 + Day 14)

**pi-mono 核心文件**：
- `packages/agent/src/agent-loop.ts` — **最重要的文件**，turn loop + tool detection + executeToolCalls + event emit
- `packages/agent/src/agent.ts` — Agent 类，高层封装
- `packages/coding-agent/test/suite/harness.ts` — 测试框架，看怎么 mock agent 行为

**面试问题**：Q1-5, Q20, Q42-44

**你要弄清楚的**：
- `agentLoop()` 函数签名和参数是什么？
- turn loop 怎么检测 LLM 返回了 tool_call vs 纯文本？
- `executeToolCalls()` 怎么把 tool call 分发到具体 tool？错误怎么传播？
- 事件系统（event emitter）在 loop 中怎么工作？
- 流式响应时，怎么把 stream delta 组装成完整回复？

**handwork**：Day 1 ReAct 手写实现；Day 2 async 改写；Day 14 4-provider agent loop

---

### Tool System (Day 1 + Day 13)

**pi-mono 核心文件**：
- `packages/coding-agent/src/core/tools/index.ts` — 工具注册 + 标准工具列表
- `packages/coding-agent/src/core/tools/bash.ts` — Bash 工具实现
- `packages/coding-agent/src/core/tools/edit.ts` — 编辑工具
- `packages/coding-agent/src/core/bash-executor.ts` — bash spawn 管理
- `packages/agent/src/agent-loop.ts` — `executeToolCalls()` 的实现

**面试问题**：Q6-9

**你要弄清楚的**：
- tool 的定义结构（name, description, parameters schema）
- tool call 从 LLM 返回 → 解析 → 参数验证 → 执行 → 结果返回，每一步可能出错？
- error handling：tool 执行失败时，错误信息怎么格式化成 Observation 给模型？
- bash tool 的 timeout 和安全限制怎么实现？

**handwork**：Day 1 实现 calc/read_file/finish；Day 13 MCP tool server

---

### Provider 抽象 (Day 14)

**pi-mono 核心文件**：
- `packages/ai/src/stream.ts` — 统一流式入口：stream / streamSimple / complete
- `packages/ai/src/providers/register-builtins.ts` — 内置 provider 注册
- `packages/ai/src/providers/faux.ts` — 测试用 mock provider
- `packages/coding-agent/src/core/model-resolver.ts` — provider → 模型解析
- `packages/coding-agent/src/core/model-registry.ts` — 模型注册表

**面试问题**：Q13-14, Q45-49

**你要弄清楚的**：
- `stream()` 的接口定义？provider 实现的抽象方法有哪些？
- Anthropic 和 OpenAI 的 tool-use schema 差异在哪？怎么统一？
- provider 是怎么注册的？新增一个 provider 需要改哪些文件？
- faux provider 怎么实现确定性测试？

**handwork**：Day 14 agent loop + 4 provider

---

### Session & Context Management (Day 15-17)

**pi-mono 核心文件**：
- `packages/coding-agent/src/core/session-manager.ts` — JSONL 持久化 + branch/fork
- `packages/coding-agent/src/core/agent-session.ts` — session 生命周期
- `packages/coding-agent/src/core/compaction/compaction.ts` — **上下文压缩**
- `packages/coding-agent/src/core/compaction/branch-summarization.ts` — 分支摘要
- `packages/coding-agent/src/core/messages.ts` — `convertToLlm()` 消息转换

**面试问题**：Q15-23

**你要弄清楚的**：
- session 数据结构？message 怎么持久化为 JSONL？
- compaction 触发条件？token 预算怎么计算？
- compaction 时，tool_use / tool_result 配对怎么保持？
- branch/fork 操作做了什么？和 git branch 类比
- `convertToLlm()` 把内部消息格式转为什么？每种 provider 格式差异？

**handwork**：Day 16 Memory 系统；Day 17 Context Engineering

---

### Memory & Working State (Day 16)

**pi-mono 核心文件**：
- `packages/coding-agent/src/core/agent-session.ts` — session 如何维护状态
- `packages/coding-agent/src/core/compaction/compaction.ts` — 上下文压缩时保留什么信息
- pi-mono 没有显式的 "working state" 层，session 就是它的 memory — 这就是为什么你要自己实现一个

**面试问题**：Q24-27

**你要弄清楚的**：
- pi-mono 用什么机制让 agent 在长任务中记住当前状态？
- compaction 后，哪些信息被保留、哪些被丢弃？
- 如果 pi-mono 的 compaction 丢失了重要上下文，会导致什么问题？

**handwork**：Day 16 Working State 实现 + 对比实验

---

### Skills / Extensions (Day 15)

**pi-mono 核心文件**：
- `packages/coding-agent/src/core/extensions/loader.ts` — 插件加载
- `packages/coding-agent/src/core/extensions/runner.ts` — 插件运行
- `packages/coding-agent/examples/extensions/` — 示例插件

**面试问题**：Q63-66

**你要弄清楚的**：
- extension 的注册和发现机制？
- extension 如何注入 tool 或修改 prompt？
- 安全边界：extension 能做什么、不能做什么？

**handwork**：Day 15 Skills 框架

---

### Subagent / Multi-Agent (Day 18-19)

**pi-mono 核心文件**：
- 搜索 `packages/coding-agent/src/` 中涉及 subagent/child-agent 的代码
- `packages/agent/src/agent-loop.ts` — agent loop 是否可以被嵌套调用？

**面试问题**：Q55-58

**你要弄清楚的**：
- pi-mono 是否支持 subagent？如果支持，spawn 机制是什么？
- 子 agent 的 tool set 如何配置？
- 子 agent 的 output 如何回传到主 agent？

**handwork**：Day 18 Failure Analysis + Subagent；Day 19 planner/executor/reviewer

---

### Reasoning & Planning (Day 4-5)

**pi-mono 核心文件**：
- `packages/agent/src/agent-loop.ts` — 看是否有 reasoning mode 切换
- pi-mono 的 system prompt 配置 — 看怎么注入 "think step by step"

**面试问题**：Q59-62

**你要弄清楚的**：
- pi-mono 的 agent loop 是否有 CoT / Reflexion 模式？
- 如果没有，它靠什么实现多步推理？
- system prompt 里有没有强制 Thought 步骤？

**handwork**：Day 4 CoT 实现；Day 5 Reflexion + ToT

---

### Failure Analysis & Recovery (Day 18)

**pi-mono 核心文件**：
- `packages/agent/src/agent-loop.ts` — 错误处理路径
- `packages/coding-agent/test/suite/regressions/` — **真实 bug 复现测试**
- `packages/coding-agent/test/suite/harness.ts` — 怎么构造失败场景

**面试问题**：Q42-44, Q20

**你要弄清楚的**：
- agent-loop 的 error 处理：哪里 catch？怎么 recovery？
- regressions/ 目录下的测试，每个测试复现了什么 bug？
- harness.ts 怎么用 faux provider 构造可复现的失败？

**handwork**：Day 18 Failure taxonomy + trajectory replay

---

### Evaluation & Harness (Day 22-24)

**pi-mono 核心文件**：
- `packages/coding-agent/test/suite/harness.ts` — **主学习对象**
- `packages/coding-agent/test/suite/README.md` — 测试规则
- `packages/coding-agent/test/suite/regressions/` — 回归测试
- `packages/ai/src/providers/faux.ts` — 确定性 mock

**面试问题**：Q35-41, Q42-44

**你要弄清楚的**：
- harness.ts 如何构造一个完整的测试环境？
- faux provider 怎么让测试不依赖真实 API？
- regression test 的写法：给定输入 → 预期 tool call → 断言
- 怎么测试 agent 的错误恢复行为？

**handwork**：Day 22-24 SWE-bench Lite 接入

---

## 按招聘要点排序（按优先级）

招聘要求的核心能力 → 对应模块的学习顺序：

1. **Agent Loop + Tool Use** → 先学（Day 1-2 + 14）
2. **Context Engineering + Memory** → 第二天（Day 15-17）
3. **Failure Analysis + Recovery** → 第三天（Day 18）
4. **Evaluation + Test Harness** → 第四天（Day 22-24）
5. **Provider 抽象 + 多模型** → 第五天（Day 14）
6. **Skills + Extensions** → 第六天（Day 15）
7. **Reasoning + Planning** → 穿插 W1（Day 4-5）
8. **Subagent + Multi-Agent** → 第七天（Day 18-19）
9. **Sandbox** → 单独学（Day 8-11，pi-mono 没有 sandbox，用学习_map §零）

---

## 每日学习流程模板

```
┌─────────────────────────────────────────────┐
│ 1. 读 mini-harness docs/daily/dayNN.md      │  ← 今日任务
│ 2. 看上表 → 打开 pi-mono 对应代码文件       │  ← 活体标本
│ 3. 看上表 → 找 interview_prep 对应问题      │  ← 面试准备
│ 4. 写答案 → 讨论 → 修正                     │  ← 内化
│ 5. 看 paper_summaries.md（如需要）          │  ← 背景知识
│ 6. 做 mini-harness handwork 实验            │  ← 手写验证
│ 7. 写 docs/notes/dayNN.md 总结              │  ← 验收
└─────────────────────────────────────────────┘
```
