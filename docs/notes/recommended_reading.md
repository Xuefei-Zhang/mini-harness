# 推荐阅读资料

> 补充阅读清单：Anthropic + OpenAI Agent Blog、Claude Code / Codex 架构文档、MCP 协议
> 与 `paper_summaries.md` 互补 — 后者是学术论文，前者是工程实践。

---

## 一、Anthropic Agent 系列博客/文档

### 必读（与计划直接相关）

| # | 标题 | URL | 对应 Day | 说明 |
|---|---|---|---|---|
| 1 | **Building Effective Agents** | https://www.anthropic.com/research/building-effective-agents | Day 1, 4, 14 | **核心必读**。Anthropic 对 Agent 设计的完整方法论：为什么 ReAct 有效、CoT vs ReAct 何时用哪个、Memory 设计原则、以及如何评估 Agent 是否"真正工作"而非巧合。第 4 节 "Agents" 直接对应你的 Day 1 ReAct 实现。第 5 节讲 Memory 策略，是 Day 16 structured working state 的理论基础。 |
| 2 | **Core Principles of LLM Security and Abuse** | https://www.anthropic.com/research/core-principles-of-llm-security-and-abuse | Day 8-13 | 理解 Agent 为什么需要 sandbox + permission model。Anthropic 定义的"LLM 特有攻击面"（privilege escalation via prompt, task injection, resource abuse），是你设计 sandbox 隔离级别的威胁模型来源。 |
| 3 | **Extending Deployment Safety to Computer Use** | https://www.anthropic.com/research/extending-deployment-safety-to-computer-use | Day 8-12 | 讲 Anthropic 如何为 Computer Use（鼠标/键盘控制）构建安全层 —— 权限门、用户确认、动作沙盒。和你用 seccomp + cgroups 做的 sandbox 思路相同但领域不同，值得对比。 |
| 4 | **Prompt Engineering: Fundamentals** | https://www.anthropic.com/guide/prompt-engineering-fundamentals | Day 3 | Anthropic 官方 Prompt Engineering 指南：system prompt 结构、few-shot 示例设计、结构化输出。直接支撑 Day 3 的 A/B/C 测试。 |
| 5 | **Prompt Engineering: Advanced Techniques** | https://www.anthropic.com/guide/prompt-engineering-advanced | Day 4, 5 | 高级技巧：Chain of Thought 引导、XML 标签结构化、让模型自我验证。与 Day 4-5 Reasoning 模式直接相关。 |

### 进阶读（研究味道）

| # | 标题 | URL | 对应 Day | 说明 |
|---|---|---|---|---|
| 6 | **Model Context Protocol (MCP)** | https://www.anthropic.com/news/model-context-protocol | Day 13 | MCP 发布公告。理解为什么 Anthropic 选择这个协议标准化 tool/server 连接。你的 Day 13 从零实现 MCP 需要读官方 spec 而非此文，但此文解释了"为什么"。 |
| 7 | **Claude Code: AI Software Engineering** | https://www.anthropic.com/claude-code | Day 14, 27 | Claude Code 产品介绍。重点看"agent loop"、"tool use"、"permissions"部分 —— 这是你最接近的对标产品。 |
| 8 | **The AI Scientist** (外部，但值得) | https://arxiv.org/abs/2502.18080 | Day 18, 25 | 讲 AI 驱动科学研究的全流程。对应你"长任务"（long-horizon）目标 —— 一个 Agent 如何独立运行数天完成论文级任务。 |

---

## 二、Claude Code 关键特性文档

### 架构与核心循环

| # | 文档 | URL | 说明 |
|---|---|---|---|
| 1 | **How Claude Code Works** | https://docs.anthropic.com/en/docs/claude-code/overview | 总览：Claude Code 如何解析用户输入 → 选择工具 → 执行 → 返回。对应你的 Day 14 Agent Loop 实现。重点看 "execution model" 和 "tool call flow"。 |
| 2 | **Tool Use** | https://docs.anthropic.com/en/docs/build-with-claude/tool-use | 官方 Tool Use 文档：schema 定义、多工具并行调用、错误传播。你的 Day 13 MCP tool server 需要完全兼容此 schema。 |
| 3 | **MCP Integration** | https://docs.anthropic.com/en/docs/agents-tools/mcp-overview | Claude Code 如何连接 MCP server。理解 stdio transport、JSON-RPC 2.0 封装、以及 tool discovery 流程。Day 13 的关键参考。 |

### Context 管理

| # | 文档 | URL | 说明 |
|---|---|---|---|
| 4 | **Prompt Caching** | https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching | **必读**。Anthropic prompt caching API：如何通过 `cache_control` 标记让重复 system prompt 不被重复计费。你的 Day 17 Context Manager 需要实现类似的 cache hit 统计。 |
| 5 | **Context Window** | https://docs.anthropic.com/en/docs/about-claude/context-windows | 各模型的 context 长度和分块策略。Claude 4 系列已支持 200K-1M tokens。你的 Day 17 需要处理超长 context 的裁剪策略。 |
| 6 | **Extended Thinking** | https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking | 让模型在返回工具调用前先生成大量内部推理（最多 200K tokens）。与 Day 4 CoT 相关 —— Anthropic 的 CoT 实现方式。 |

### 安全和沙盒

| # | 文档 | URL | 说明 |
|---|---|---|---|
| 7 | **Permissions** | https://docs.anthropic.com/en/docs/claude-code/permissions | Claude Code 的权限系统：autoapprove / approve / disabled。每种工具调用在執行前需要用户确认。你的 sandbox 的 permission model 应参考此设计。 |
| 8 | **Approval Settings** | https://docs.anthropic.com/en/docs/claude-code/approval-settings | 如何配置哪些命令自动放行。这对应你的 Day 13 workspace 安全测试 —— `..` escape、symlink escape 等。 |

### 高级特性

| # | 文档 | URL | 说明 |
|---|---|---|---|
| 9 | **Managed Agents** | https://docs.anthropic.com/en/docs/claude-code/agents | Claude Code 如何 spawn 子 agent。与 Day 20 Subagent 调度器直接相关。看其如何传递 context、回收结果、传播错误。 |
| 10 | **Hooks** | https://docs.anthropic.com/en/docs/claude-code/hooks | 事件驱动钩子：tool call 前后、commit 前后执行自定义脚本。这是 harness 的 observability 入口，与 Day 27 Trajectory 系统思路一致。 |
| 11 | **Settings** | https://docs.anthropic.com/en/docs/claude-code/settings | settings.json 配置：模型选择、hook、权限、env。你的 harness 配置系统可以参考此结构。 |
| 12 | **SSH & Remote** | https://docs.anthropic.com/en/docs/claude-code/remote-ssh | Claude Code 通过 SSH 连接远程机器。你的 sandbox 如果需要远程执行（Day 12），参考此模式的连接管理。 |

---

## 三、OpenAI Agent / Coding 系列博客/文档

### 必读（与计划直接相关）

| # | 标题 | URL | 对应 Day | 说明 |
|---|---|---|---|---|
| 1 | **OpenAI Agents SDK** | https://github.com/openai/openai-agents-python | Day 14, 20 | OpenAI 开源的 Agent SDK（Python）。**不看 API 用法，看架构设计**：tracing 系统（从 Day 1 就有）、handoff 模式（planner↔executor 交接）、guardrails（前置/后置检查）。你的 Day 14 Agent Loop 和 Day 20 Subagent 调度器可以直接对比其 handoff 实现。虽然你不用 SDK，但其 tracing + handoff 设计思路值得学习。 |
| 2 | **OpenAI Codex CLI** | https://github.com/openai/codex | Day 14, 27 | OpenAI 的 CLI coding agent。重点看 TUI 模式下的 agent loop、session 管理和 approval workflow。与 Claude Code 是**直接竞品**——对比两者的 tool dispatch 和权限模型设计能帮你回答面试问题："Claude Code vs Codex CLI 的架构差异"。 |
| 3 | **OpenAI Codex Blog** | https://openai.com/index/introducing-codex/ | Day 14 | Codex CLI 发布公告。看 OpenAI 如何定义 "agentic coding"——他们的 agent loop 是思考→规划→分块执行→验证，与 Claude Code 的思考→执行→反思不同。理解两种设计哲学。 |
| 4 | **Structured Outputs** | https://platform.openai.com/docs/guides/structured-outputs | Day 13 | OpenAI 的结构化输出 API（JSON Schema 约束）。对比 Anthropic tool-use schema，两者思路相同但实现细节不同（OpenAI 用 JSON Schema，Anthropic 用自定义 tool_call 格式）。Day 13 实现 MCP 时需要理解两边的差异。 |
| 5 | **OpenAI Evals** | https://github.com/openai/evals | Day 22-24 | OpenAI 开源的 eval harness 框架。看他们如何定义 task → run → grade 的 pipeline。你的 SWE-bench Lite 接入（Day 22-24）需要设计类似的 eval pipeline。重点看 prompt_delivery 模块的模板引擎和结果聚合。 |

### 进阶读（研究味道）

| # | 标题 | URL | 对应 Day | 说明 |
|---|---|---|---|---|
| 6 | **Workbench: Agent Harness for Frontier Models** | https://openai.com/index/workbench/ | Day 18, 25 | OpenAI 的 agent harness 研究平台。重点看他们如何做 **agent × model co-evaluation**——不同 agent harness 在不同模型上的表现差异。直接对应你 Day 25 "模型共同进化"分析。 |
| 7 | **Swarm Pattern** | https://github.com/openai/openai-agents-python/tree/main/src/agents/swarm | Day 19, 20 | 轻量级 multi-agent 模式（handoff-based）。agent 之间通过 handoff 而非消息传递。你的 Day 19 planner/executor/reviewer 流水线和 Day 20 subagent 调度器可以直接参考此模式。 |
| 8 | **OpenAI Tracing** | https://platform.openai.com/docs/tracing | Day 27 | OpenAI 的 tracing API（基于 W3C Trace Context / OpenTelemetry）。你的 Day 27 Trajectory 系统需要集成 tracing——看 OpenAI 如何定义 span、event、metadata。与 Anthropic 的 hooks 对比能帮你回答 "harness observability 方案选型"。 |
| 9 | **GPT-4o System Card** | https://openai.com/index/gpt-4o-system-card-v2/ | Day 17, 18 | 模型系统卡——展示 OpenAI 如何做 red-teaming eval、failure mode 分析。你的 Day 18 Failure Taxonomy 方法论上可参考此格式。 |

---

## 四、Anthropic vs OpenAI 架构对比（面试用）

| 维度 | Anthropic (Claude Code) | OpenAI (Codex CLI / Agents SDK) | 面试答案 |
|---|---|---|---|
| **Agent Loop** | 思考→工具调用→执行→反思（单轮内完成） | 思考→规划→分块执行→验证（多轮拆分） | "Claude Code 偏重单轮完整执行，Codex 偏重视觉化验证" |
| **Tool Protocol** | MCP（行业标准，stdio + SSE） | 自定义 tool_call schema | "MCP 是开放的，OpenAI 走 API-native 路线" |
| **Memory** | 项目级 memory 文件（.claude/CLAUDE.md） | 结构化 agent state + threads API | "Anthropic 偏向 persistent files，OpenAI 偏向 API-managed state" |
| **Observability** | Hooks（事件驱动） | Tracing（OpenTelemetry） | "Hooks 适合本地开发，Tracing 适合分布式" |
| **Sandbox** | Permission gates（用户确认） | Approval modes（auto/total/user） | "两者都依赖人类 in-the-loop，但粒度不同" |

---

## 五、MCP 协议（Day 13 专用）

| # | 资源 | URL | 说明 |
|---|---|---|---|
| 1 | **MCP Spec (GitHub)** | https://github.com/modelcontextprotocol/specification | MCP 协议的正式 spec。Day 13 从零实现的唯一权威参考。重点：JSON-RPC 2.0 transport、Tool 定义、Resource 语义。 |
| 2 | **MCP Python SDK** | https://github.com/modelcontextprotocol/python-sdk | 参考实现。你的目标是**不用 SDK 手写**，但完成后用 SDK 验证你的实现是否符合 spec。 |
| 3 | **MCP Server Tutorial** | https://modelcontextprotocol.io/docs/quickstart | 官方快速入门。理解 client↔server 握手、tool listing、call 流程。 |

---

## 六、阅读优先级（按计划 Day 排序）

```
Day 3  → Anthropic Prompt Engineering Fundamentals (#4 of §一)
Day 4  → Building Effective Agents §4 (CoT) + Prompt Engineering Advanced (#5 of §一)
Day 5  → Building Effective Agents §5 (Memory, Reflexion) (#1 of §一)
Day 13 → MCP Spec (#1 of §五) + Structured Outputs (#4 of §三) + Tool Use docs (#2 of §二)
Day 14 → How Claude Code Works (#1 of §二) + Codex Blog (#3 of §三) + Agents SDK (#1 of §三)
Day 16 → Building Effective Agents §5 (Memory strategies) (#1 of §一)
Day 17 → Prompt Caching (#4 of §二) + Context Window (#5 of §二) + GPT-4o System Card (#9 of §三)
Day 18 → Building Effective Agents §6 (Evaluation) + Evals (#5 of §三) + Workbench (#6 of §三)
Day 19 → Swarm Pattern (#7 of §三)
Day 20 → Managed Agents (#9 of §二) + Swarm (#7 of §三)
Day 22 → Evals (#5 of §三)
Day 25 → Workbench (#6 of §三)
Day 27 → Hooks (#10 of §二) + OpenAI Tracing (#8 of §三) + Extended Thinking (#6 of §二)
```
