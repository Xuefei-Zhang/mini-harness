# 一个月 Agent Infra / Harness 求职冲刺计划 v3.0

> 起始日期：2026-05-21（实际开始：2026-05-17，Day 1 已完成）
> 截止日期：2026-06-19（30 天滚动）
> 目标岗位：Agent Infrastructure / Harness / Coding Agent 工程师
> 核心目标：DeepSeek Agent Harness 工程师
> 并行目标：Moonshot/智谱/MiniMax/百川/阶跃/零一 + 字节/阿里/腾讯/百度 AI Lab + 幻方
> 每周投入：40+ 小时
> 投递启动：Day 28+
>
> **灵活原则**：任务可按任意顺序完成，以质量为准，学习心得（docs/notes/）为完成凭证。每周 review 时根据进度调整。
>
> **北极星**：一个真正能跑的、可观测的、可评估的、可复现的 mini-harness。不是功能堆砌。
>
> **隐藏主线**：每一行代码都在为同一个目标服务——让 harness 能驱动模型完成一项**长任务**（long-horizon task）：从零实现一个中等复杂度软件，或在 vLLM / FastAPI / SWE-bench 的大型项目中针对真实 issue 产出可 merge 的 PR。这个目标不单独列为某个 Day，而是隐含在每个模块的设计决策中（见各模块的 `→ 服务于长任务的 X` 标注）。Day 26 是最终验证。

---

## 0. 背景与定位

### 我的优势（对 Agent/Harness 岗位加分）
- 7 年系统软件 + 全栈（app→middleware→driver→fw）经验 → Harness 工程师核心素养
- 多 OS 平台经验（Windows/Linux/FreeRTOS）→ 容器化、跨平台执行环境天然契合
- C/C++ 系统级能力强 → Agent runtime、tool sandbox 底层实现
- 实际用过 opencode、多家模型 → 有 agent product sense

### 短板（需要补的）
- 缺少 Python/TypeScript 现代后端栈的工程化经验
- 没有公开的 LLM/Agent 项目作品
- 对 agent 核心概念停留在使用层面，缺实现深度
- 缺少 evaluation/harness 经验
- **研究味道不够浓** — 需要从"工程实现"升级到"理解模型行为"

### 项目本质
> 这不是聊天机器人。这是 **LLM Runtime + Evaluation Infrastructure**。
>
> 对标：SWE-bench 官方 harness 内核 + Anthropic claude-code-action 的执行层。

### DeepSeek JD 对标分析

| JD 关键词 | 优先级 | 计划覆盖 | 完成方式 |
|---|---|---|---|
| Agent Loop | 🔴 P0 | Day 14 | 完整的 async agent loop，含 stuck detection、retry |
| Tool Use | 🔴 P0 | Day 13 | MCP tool server，4 个核心工具 |
| MCP | 🔴 P0 | Day 13 | 从 spec 实现，不用 SDK |
| Context Engineering | 🔴 P0 | Day 17 | 窗口管理、缓存命中、压缩策略 + **对 tool selection accuracy 的影响** |
| Sandbox/Runtime | 🔴 P0 | Day 8-11 | C++ cgroups + seccomp + namespaces（差异化武器） |
| Evaluation | 🔴 P0 | Day 22-26 | SWE-bench Lite + **agent metrics** + **model co-evolution analysis** |
| Trajectory | 🔴 P0 | Day 27 | JSONL + viewer + **OpenTelemetry-style tracing** |
| Memory | 🟡 P1 | Day 16 | **structured working state**（主）+ 短期滑动窗口 + 轻量长期存储 |
| Reasoning | 🟡 P1 | Day 4-5 | CoT（重点）+ Reflexion（重点）+ ToT（lightweight demo） |
| Prompt Engineering | 🟡 P1 | Day 3 | A/B/C 测试，记录效果差异 |
| Skills | 🟡 P1 | Day 15 | 可插拔技能机制，agent 自动选择/加载 |
| Subagent | 🟡 P1 | Day 20 | spawn + 回收 + 错误传播 |
| Multi-Agent | 🟢 P2 | Day 19 | **planner/executor/reviewer 三角色**（lightweight demo） |
| KV Cache | 🟢 P2 | Day 21 | 原理分析 + small-scale demo |

### 优先级定义
- **P0（ALL-IN）**：必须做好，代码质量在线，有数据支撑。面试必问。
- **P1（做好即可）**：实现完整，有实验数据。面试加分。
- **P2（轻量 demo）**：跑通即可，不深挖。体现广度。

### 战略选择
- All-in Agent 方向，不分散精力到推理岗
- 硬件不投入，钱花在 API 和云资源（预算 ¥3000-5000/月）
- C++ sandbox 是差异化武器（大部分 Agent 候选人不懂 seccomp/cgroups/namespace）
- **不做**：LangChain/LangGraph、RAG/向量数据库、AutoGen 套壳
- 全开源 + 中英博客双发
- **博客语言**：用 "research infra language"（见 §12）

---

## 1. 核心交付物总览（Day 30 末尾）

1. **GitHub 项目 `mini-harness`**：~5000-8000 行代码
   - C++ sandbox（cgroups + seccomp + namespaces）
   - Python agent loop（4 provider，含 Memory / Context / Skills / Failure Analysis）
   - MCP tool server
   - SWE-bench Lite evaluation pipeline + agent metrics
   - Trajectory system（JSONL + OpenTelemetry-style tracing + viewer）
2. **5 篇技术博客**（中英双语，research infra language）
   - Blog 1: 《从系统工程师视角写一个 Agent Harness：30 天从零到 SWE-bench》
   - Blog 2: 《用 C++ 实现 LLM Agent 的最小 sandbox：从 cgroups 到 seccomp》
   - Blog 3: 《Agent Working State：structured memory 对 trajectory stability 的影响》
   - Blog 4: 《Coding Agent Failure Taxonomy：从 200 次 trajectory 中归纳的 8 类失败模式》
   - Blog 5: 《Context Compression 对 tool selection accuracy 的影响 + SWE-bench Lite 成绩》
3. **更新后的简历**（含项目链接 + 量化 metric）
4. **目标公司清单 + JD skill mapping 表**（含 DeepSeek 对标）
5. **20-30 家公司的投递规划**

---

## 2. 项目架构 v3.0

### 组件矩阵（按优先级排序）

| 组件 | 优先级 | 对应 JD | 技术栈 |
|---|---|---|---|
| Sandbox Runtime | 🔴 P0 | 技术水平过硬 | C++（cgroups v2 + seccomp + namespaces）+ Python SDK |
| Agent Loop | 🔴 P0 | Agent Loop, LLM API | Python async，4 provider，stuck detection，retry |
| Tool Server | 🔴 P0 | MCP, Tool Use | Python，MCP 协议 |
| Context Manager | 🔴 P0 | Context Engineering | 裁剪 + prompt cache + 压缩 |
| Eval Pipeline | 🔴 P0 | Harness | SWE-bench Lite + agent metrics |
| Trajectory System | 🔴 P0 | Harness | JSONL + OTel-style tracing + viewer |
| Memory（Working State） | 🟡 P1 | Memory | structured state + 滑动窗口 + 轻量长期存储 |
| Skills Framework | 🟡 P1 | Skills | 可插拔技能机制 |
| Failure Analysis | 🟡 P1 | Reasoning | 失败分类 + trajectory replay |
| Reasoning Engine | 🟡 P1 | Reasoning/Planning | CoT（重点）/ Reflexion（重点）/ ToT（demo） |
| Subagent | 🟡 P1 | Subagent | spawn + 回收 |
| Multi-Agent | 🟢 P2 | Multi-Agent | planner/executor/reviewer（demo） |
| KV Cache Demo | 🟢 P2 | KV Cache | 原理 + small-scale PyTorch demo |

---

## 3. 周度规划（v3.0）

| 周 | 主题 | 核心产出 |
|---|---|---|
| W1 (Day 1-7) | Agent 基础 + Prompt/Reasoning + 源码 | 博客 1；Prompt A/B；Reasoning 对比；3 张架构图 |
| W2 (Day 8-14) | Sandbox（C++）+ MCP + Agent Loop | sandbox v0 + MCP + agent loop v0；博客 2 |
| W3 (Day 15-21) | Skills + Memory + Context + Failure Analysis + Subagent/KV | 博客 3+4；failure taxonomy；trajectory replay |
| W4 (Day 22-30) | SWE-bench + metrics + 模型共同进化 + 博客 5 + 简历 + 投递 | eval 数字 + agent metrics + 简历定稿 + 投递 |

### 每周节奏
- 周一-周二：理论 + 读源码（输入）
- 周三-周五：编码（输出）
- 周六：写博客 + 整理 commit（沉淀）
- 周日：休息 + 复盘 + 调整下周计划

---

## 4. W1（Day 1-7）：Agent 基础 + Prompt/Reasoning

**目标**：理解 agent 全谱系机制，建立对"模型行为"的直觉

### Day 1 - Agent Loop 与 ReAct
> 从零手写，参考 pi-mono `packages/agent/src/agent-loop.ts`
- [ ] 读 pi-mono agent-loop 源码，理解 turn loop + tool call 检测
- [ ] 回答面试 Q1/Q3/Q6（`docs/interview_prep.md`）
- [ ] 手写 `experiments/day01_react_from_scratch.py`：3 tools, vllm provider, ~250 行
- [ ] 跑 5 个任务，记录成功率/步数/token
- [ ] 写 `docs/notes/day01_review.md`：ReAct 在哪类任务上好/差？为什么？

### Day 2 - 现代 Python 速通
- asyncio、pydantic v2、httpx、structlog
- 把 day01 重写成 async 版本
- 产出：`experiments/day02_async_react.py`，并发跑 10 个任务

### Day 3 - Prompt Engineering 实践
- 3 套 system prompt（最小/结构化/链式），A/B/C 测试
- 记录：成功率 / token / 步数 / 质量
- 产出：`experiments/day03_prompt_ab.py` + `docs/notes/day03_prompt_results.md`

### Day 4 - Reasoning：CoT（重点）
- 实现 Chain of Thought（Thought 强制执行，≥ 2 句）
- 对比 baseline ReAct vs CoT 的成功率和 token 效率
- 产出：`experiments/day04_reasoning_modes.py`

### Day 5 - Reasoning：Reflexion（重点）+ ToT（lightweight）+ 对比总结
- **Reflexion**：失败后生成反思 → 注入下次 prompt → 观察是否改善
- **ToT**：lightweight demo（3 分支 + 投票），跑 1-2 个任务即可
- 对比表：baseline / CoT / ToT / Reflexion → `docs/notes/day04_reasoning_comparison.md`

### Day 6 - 精读 opencode 源码
- tool dispatch 序列化、permission、session 管理、context window 处理
- 架构图 → `docs/design/opencode-arch.png`
- 笔记 → `docs/notes/day06_opencode.md`

### Day 7 - 精读 aider + SWE-agent + 博客 1
- aider：repo map、edit 格式、git 集成
- SWE-agent：ACI 思想、action space 设计
- 架构图 → `docs/design/aider-arch.png`、`docs/design/swe-agent-arch.png`
- **博客 1**《从系统工程师视角写一个 Agent Harness：30 天从零到 SWE-bench》
- 中英双发：掘金 + dev.to

**W1 产出 checklist**
- [ ] ReAct 回顾 + 实验记录
- [ ] Prompt A/B 测试结果
- [ ] Reasoning 模式对比（CoT 重点 + Reflexion + ToT demo）
- [ ] 三张架构图
- [ ] 博客 1 发布

---

## 5. W2（Day 8-14）：Sandbox（C++）+ MCP + Agent Loop v0

**目标**：交付项目里最差异化的组件 + agent loop 骨架

### Day 8 - Sandbox 设计与选型
- 调研 E2B / Modal sandbox / Daytona
- 决策：v0 clone3 + namespace + cgroups v2 + seccomp
- 写 `docs/design/sandbox.md`（threat model + interface contract + test plan）

### Day 9-11 - C++ sandbox 核心
- Day 9：`clone3` + namespace + cgroups v2，限制 CPU/内存/磁盘/网络
- Day 10：seccomp-bpf 系统调用过滤；超时与 OOM
- Day 11：Python SDK（subprocess + JSON IPC）；4 类逃逸测试
- 预计：800-1500 行 C++ + 300 行 Python

### Day 12 - Sandbox 集成测试 + 博客 2
- demo：sandbox 内写 Flask 应用 → 安装依赖 → 启动服务 → health check
- **博客 2**《用 C++ 实现 LLM Agent 的最小 sandbox：从 cgroups 到 seccomp》
- 必带：架构图、cold-start p50/p95、与 E2B 对比

### Day 13 - MCP tool server v0
- 4 个工具：`read_file` / `write_file` / `run_shell`(sandboxed) / `search_code`
- 严格遵循 MCP spec，能被 Claude Desktop 连接
- workspace 安全测试（`..`、symlink escape）

### Day 14 - Agent loop v0 + 4 provider + W2 复盘
- 核心 loop：`while not done: complete → execute tools → append`
- `LLMProvider` 抽象：Anthropic / OpenAI / DeepSeek / Qwen
- stuck detection（重复 action / error cascade）、retry（429/5xx backoff）
- 冒烟测试
- W2 复盘笔记

**W2 产出 checklist**
- [ ] sandbox 拦住 4 类逃逸攻击
- [ ] MCP server 能被 Claude Desktop 调用
- [ ] Agent loop v0 跑通，4 provider 可用
- [ ] 博客 2 发布
- [ ] 仓库代码 ≥ 2500 行

---

## 6. W3（Day 15-21）：Skills + Memory + Context + Failure Analysis

**目标**：从"能跑"到"可观测、可分析"——研究味道在这里成型

### Day 15 - Skills 框架
- `Skill` class（name, description, trigger_patterns, handler, config）
- `SkillRegistry`：根据任务描述自动发现/加载技能
- 3 个内置技能：`file_editor`、`code_runner`、`debug_assistant`
- 产出：`agent/skills/`

### Day 16 - Memory 系统 ⬅️ v3 重大调整
> 重心从 embedding retrieval 转向 **structured working state**。
> → 服务于长任务：50-step 的任务中，agent 必须记住"我已经改了 3 个文件，还有 2 个没动，上次失败是因为 X"。

- **Structured Working State**（核心）：
  ```python
  class WorkingState(BaseModel):
      current_goal: str
      subtasks: list[Subtask]       # 分解后的子任务
      attempted_actions: list[ActionRecord]  # 已尝试的操作
      known_failures: list[FailureRecord]   # 已知失败及原因
      modified_files: list[str]           # 已修改的文件
      open_questions: list[str]          # 待确认的问题
  ```
  每个 step 自动更新，注入 system prompt。→ 长任务中这是 agent 的"任务板"。
- **短期 Memory**（滑动窗口）：Last N messages / token budget，保持 tool 配对
- **长期 Memory**（轻量）：SQLite 存储跨 session 的关键决策（不用 embedding，用 FTS5 关键词检索）→ 长任务中断后恢复
- 产出：`agent/memory/`

### Day 17 - Context Engineering + 博客 3
→ 服务于长任务：100-step 的任务中，context 会膨胀到 100k+ tokens。agent 需要知道保留什么、丢弃什么、什么时候压缩。
- Context Manager 三种策略：`drop_oldest`、`summarize_oldest`、`hierarchical`
- **Prompt Cache**：Anthropic prompt caching API，统计 cache hit rate → 长任务的成本大头
- **Token 预算监控**：实时跟踪已用 tokens，超限事件记录
- **博客 3**《Agent Working State：structured memory 对 trajectory stability 的影响》
  - 核心论点：为什么 structured state 比 conversation memory 更适合 coding agent
  - 实验数据：same task, with/without working state → 对比 success rate / avg steps / recovery from failure

### Day 18 - Agent Failure Analysis ⬅️ 新增（比 Subagent 更重要）
> 分析 agent 为什么失败——这是真正做 harness 的团队最看重的。

- **Trajectory Taxonomy**：从实验数据中归纳失败分类
  ```
  | 类型              | 描述                    |
  |-------------------|------------------------|
  | ToolFailure       | tool 参数错误/调用失败     |
  | PlanningFailure   | 任务分解错误              |
  | ContextFailure    | 关键信息丢失（context 被裁剪）|
  | ExecutionFailure  | shell/runtime 出错       |
  | ReasoningFailure  | 推理偏航（hallucinated file path 等）|
  | RecoveryFailure   | retry 无效，陷入死循环     |
  | StaleState        | working state 过时导致错误决策 |
  | PrematureFinish   | 过早完成任务              |
  ```
- **Trajectory Replay**：给定 saved trajectory JSONL，重放不调用 LLM（用 recorded responses）
- **Failure Rate 分析**：每类失败占多少？哪些 harness 机制能减少哪类失败？
- 产出：`harness/failure/` + `docs/notes/day18_failure_taxonomy.md`
- **博客 4**《Coding Agent Failure Taxonomy：从 200 次 trajectory 中归纳的 8 类失败模式》

### Day 19 - Multi-Agent（lightweight：planner/executor/reviewer）
> 只做三角色分工流水线，不做辩论/投票。

- **Planner**：接收任务 → 分解子任务 → 输出 plan
- **Executor**：执行每个子任务 → 汇报结果
- **Reviewer**：检查 executor 输出 → approve / request changes
- 流水线：planner → executor → reviewer → (if changes) executor → done
- 产出：`agent/multi_agent/` + `experiments/day19_triad.py`

### Day 20 - Subagent 调度器
- `SubagentSpawner`：spawn + spawn_many（sequential / parallel）
- 子 agent 有独立 working state + context + tool set
- 结果回收 + 错误传播（timeout / error / max_steps）
- 产出：`agent/subagent/`

### Day 21 - KV Cache 原理 + 端到端 demo + W3 复盘
- KV Cache 原理笔记 → `docs/notes/day21_kv_cache.md`
- lightweight PyTorch demo（可选，时间不够跳过）
- 端到端 demo：串起 agent loop + memory + context + skills + failure analysis
- W3 复盘 + SWE-bench 准备

**W3 产出 checklist**
- [ ] Skills 框架（3 内置技能，自动发现）
- [ ] Memory 系统（structured working state 为主，短期 + 轻量长期为辅）
- [ ] Context Manager（3 策略 + prompt cache + token 监控）
- [ ] **Failure taxonomy**（8 类失败 + trajectory replay）
- [ ] Multi-Agent（planner/executor/reviewer 流水线）
- [ ] Subagent（spawn + 回收）
- [ ] KV Cache 笔记
- [ ] 博客 3 + 博客 4 发布

---

## 7. W4（Day 22-30）：SWE-bench + Metrics + 模型共同进化

### Day 22-24 - SWE-bench Lite 接入
- dataset loader：10-15 题（django/sympy 简单题）
- evaluation pipeline：agent → patch → test → pass/fail
- 复用官方 docker 镜像

### Day 25-26 - 跑通 + 调优 + 与模型共同进化 ⬅️ 新增
- Claude Sonnet 跑一遍，DeepSeek 跑一遍对比
- **与模型共同进化**：记录哪些 harness 机制让不同模型表现更好
  - 特定 prompt 结构（结构化 vs 链式）
  - tool 描述方式（简短 vs 详细 + 示例）
  - memory 注入时机（每步 vs 仅在失败后）
  - context 策略（drop_oldest vs hierarchical）对 pass@1 的影响
- 写入 `docs/notes/day25_model_co_evolution.md`
- 目标：pass@1 ≥ 30%

### Day 26 — 终极挑战：长任务验证 ⬅️ 隐藏主线揭晓
> 这是整个 30 天的最终验证。让 harness 驱动模型完成一项真正长任务。

- **选一个真实项目**（三选一）：
  1. **vLLM**：找一个 `good first issue` 或 `bug`，让 agent 独立完成 → 产出 PR
  2. **FastAPI**：类似，找一个 issue，agent 提交 fix
  3. **从零实现**：给定 spec，让 agent 从零实现一个中等复杂度项目（如：实现一个 HTTP 缓存中间件，含 LRU + TTL + 基准测试）
- harness 全开：working state + context manager + failure recovery + subagent + trajectory recording
- 记录：任务跑了多少步、多少小时、多少 cost、失败了几次、harness 如何自动恢复
- **如果能产出可 merge 的 PR → 这是简历上最重的一句话**
- 写入 `docs/notes/day26_ultimate_challenge.md`

### Day 27 — Agent Metrics + Trajectory + 可视化
→ 服务于长任务：metrics 不是跑 SWE-bench 10 题的平均值，而是长任务的完整 observability。

### Day 27 - Agent Metrics + Trajectory 系统 + 可视化
- **Agent Metrics**（每次运行自动产出）：
  ```
  | metric               | 含义                    |
  |----------------------|------------------------|
  | avg_tool_calls       | 平均每轮工具调用数        |
  | context_growth_rate  | context 增长速度（tokens/step）|
  | retry_rate           | tool call 重试比例       |
  | hallucinated_actions | 幻觉动作数（tool 不存在/参数非法）|
  | recovery_rate        | 失败后 retry 成功率      |
  | token_efficiency     | 成功任务每步平均 token     |
  | stuck_interventions  | stuck detector 触发次数   |
  | working_state_accuracy | working state 与实际情况的一致性（抽样）|
  ```
- **Trajectory System**：JSONL + OpenTelemetry-style tracing（span-based）
- **Trajectory Viewer**：Streamlit app
  - timeline view（按时间线展开 events）
  - tool tree（tool call 的层级关系）
  - retry chain（某 tool call 的多次重试）
  - token cost graph（每步 token 消耗）
  - failure highlight（红色标注失败事件）

### Day 28 - 博客 5 + 简历 + JD mapping
- **博客 5**《Context Compression 对 tool selection accuracy 的影响 + SWE-bench Lite 上跑出 X%》
  - 核心论点：context 策略如何影响 agent 的工具选择准确率
  - 数据：3 种 context 策略 × 4 个 provider 的 tool selection accuracy
  - SWE-bench 结果 + agent metrics 表
- 简历改造：IPU 系统软件 → agent harness 语言
- JD 反推：DeepSeek + 5 家目标公司 skill mapping

### Day 29 - 模拟面试
- 15 道高频题（sandbox / context / memory / failure / metrics / KV / 为什么不用 LangGraph）
- 重点练习"research infra language"表达（见 §12）
- 模拟面 1-2 次

### Day 30 - 投递启动
- 第一批 5-8 家：DeepSeek 优先，内推优先
- "为什么投你"30 秒 + 3 分钟版

**W4 产出 checklist**
- [ ] SWE-bench Lite 跑出可公布数字
- [ ] Agent metrics 表（每个 task 一行）
- [ ] `day25_model_co_evolution.md` 记录
- [ ] Trajectory viewer 可用（timeline + tool tree + retry chain + cost graph）
- [ ] 博客 5 发布
- [ ] 简历定稿
- [ ] 第一批投递发出
- [ ] 仓库代码 ≥ 5000 行

---

## 8. 学习资源白名单

### 必读 paper
- Anthropic "Building effective agents"（最优先）
- ReAct（arxiv 2210.03629）
- Reflexion（arxiv 2303.11366）
- SWE-agent（arxiv 2405.15793）— method section only
- Chain of Thought（arxiv 2201.11903）— abstract + intro

### 必读源码（按优先级）
1. opencode（tool dispatch + session）
2. SWE-agent（ACI + action space）
3. aider（repo map + edit format）
4. claude-code（npm 包逆向）

### 必读 spec
- MCP 协议（Tools + stdio transport）
- Anthropic tool-use schema + prompt caching docs

### 必看视频
- Andrej Karpathy LLM 课（KV Cache / Attention 部分）

### 拒绝列表
- 吴恩达 LangChain 系列课
- 各类中文二手教程
- LangChain / LangGraph 全家桶
- RAG / 向量数据库
- AutoGen / CrewAI 套壳

---

## 9. 关键避坑提醒

1. **不学 LangChain/LangGraph**——自己手写 loop 更显功力
2. **不做 RAG/向量数据库**——Memory 重点是 working state，不是 embedding retrieval
3. **C++ sandbox 别过度设计**——v0 跑通 > v1 完美
4. **ToT / Multi-Agent 轻量 demo 即可**——工业界主要用 ReAct + Reflexion + retry
5. **API 预算控制**：W1-W3 每天 ¥30-80，W4 跑 SWE-bench 一次 ¥200-500，整月 ≤ ¥3000
6. **不买显卡**，钱留到投递后期
7. **任务可跳序完成**——质量 + 心得 = 算完成
8. **每周 review 调整计划**——卡住就重新分配，超预期的模块压缩时间
9. **博客用 research infra language**（见 §12）——这是打动研究团队的关键

---

## 10. 进度追踪

### 完成状态

| Day | 主题 | 优先级 | 状态 |
|---|---|---|---|
| 1 | ReAct 回顾 | 🟡 P1 | ✅ 代码完成，待回顾 |
| 2 | 现代 Python 速通 | 🟡 P1 | ⬜ |
| 3 | Prompt Engineering | 🟡 P1 | ⬜ |
| 4 | Reasoning: CoT | 🟡 P1 | ⬜ |
| 5 | Reasoning: Reflexion + ToT | 🟡 P1 | ⬜ |
| 6 | opencode 源码 | 🟡 P1 | ⬜ |
| 7 | aider + SWE-agent + 博客 1 | 🟡 P1 | ⬜ |
| 8 | Sandbox 设计 | 🔴 P0 | ⬜ |
| 9-11 | C++ sandbox 核心 | 🔴 P0 | ⬜ |
| 12 | Sandbox 集成 + 博客 2 | 🔴 P0 | ⬜ |
| 13 | MCP tool server | 🔴 P0 | ⬜ |
| 14 | Agent loop v0 | 🔴 P0 | ⬜ |
| 15 | Skills 框架 | 🟡 P1 | ⬜ |
| 16 | Memory（working state） | 🟡 P1 | ⬜ |
| 17 | Context Engineering + 博客 3 | 🔴 P0 | ⬜ |
| 18 | Failure Analysis + 博客 4 | 🟡 P1 | ⬜ |
| 19 | Multi-Agent（lightweight） | 🟢 P2 | ⬜ |
| 20 | Subagent | 🟡 P1 | ⬜ |
| 21 | KV Cache + 端到端 + 复盘 | 🟢 P2 | ⬜ |
| 22-24 | SWE-bench Lite | 🔴 P0 | ⬜ |
| 25-26 | 调优 + 模型共同进化 | 🔴 P0 | ⬜ |
| 26 | 终极挑战：长任务验证 | 🔴 P0 | ⬜ |
| 27 | Agent Metrics + Trajectory | 🔴 P0 | ⬜ |
| 28 | 博客 5 + 简历 | 🟡 P1 | ⬜ |
| 29 | 模拟面试 | 🟡 P1 | ⬜ |
| 30 | 投递启动 | 🟡 P1 | ⬜ |

### 追踪方式

每天结束时在 `docs/notes/dayNN.md` 写一份 30 行内的日报：
- 今日完成
- 遇到的坑
- 明日 top 3
- 项目代码行数 / commit 数

每周末 review：更新本文件的状态表，根据实际进度调整后续时间安排。

---

## 11. 你能达到什么水平

完成 70%+ 且代码质量在线后，你在面试中能说的话：

### 工程能力
- "我手写了一个 async agent loop，支持 4 个 LLM provider，含 stuck detection 和 retry"
- "我用 C++ 实现了 cgroups v2 + seccomp + namespaces 的 sandbox，拦住 fork bomb / 内存炸弹 / 网络逃逸"
- "我从 MCP spec 实现了 tool server，能被 Claude Desktop 直接连接"

### 研究味道
- "我在研究 structured working state 对 trajectory stability 的影响——实验表明它比 pure conversation memory 减少 30% 的 PlanningFailure"
- "我在研究 context compression 对 tool selection accuracy 的影响——hierarchical 策略比 drop_oldest 在 40+ step 的长任务上准确率高 15%"
- "我在研究 failure recovery policy 对 pass@1 的提升——从 200 次 trajectory 中归纳了 8 类失败模式，其中 ToolFailure 占 35%，通过 improved tool descriptions 减少了 20%"
- "我在研究不同 harness 机制对不同模型的适配性——DeepSeek 对 structured prompt 更敏感，而 Sonnet 对 working state 注入的响应更好"

### 差异化
- 国内同时懂 seccomp/cgroups + agent harness + SWE-bench 的人不多
- 7 年系统软件背景 + 这个项目 = "LLM Runtime Engineer" 定位
- **如果 Day 26 产出了真实 PR**："我用自己的 harness 驱动模型为 vLLM 提交了一个可 merge 的 PR"——这句话比任何 certificate 都有说服力

### 长任务能力（隐藏主线）
完成 Day 26 后，你在面试中能说的：
- "我的 harness 能驱动模型完成 50-100 step 的长任务——context 不溢出、失败能恢复、memory 不混乱"
- "working state 让 agent 在 80-step 的任务中仍然知道'我已经改了哪些文件、还差什么没做'"
- "failure recovery policy 让 agent 在 5 次连续工具调用失败后自动切换策略，而不是死循环"

---

## 12. Research Infra Language ⬅️ 新增

博客、简历、面试中用以下表达替换对应描述：

| 不要说 | 而要说 |
|---|---|
| "我实现了 memory" | "我在研究 agent state persistence 对 trajectory stability 的影响" |
| "我实现了 context manager" | "我在研究 context compression 对 tool selection accuracy 的影响" |
| "我实现了 retry" | "我在研究 failure recovery policy 对 pass@k 的提升" |
| "我写了 prompt A/B 测试" | "我在分析 system prompt structure 对 agent step efficiency 的影响" |
| "我做了 sandbox" | "我实现了 agent execution runtime，提供 cgroups/seccomp/namespace 三级隔离" |
| "我接了 SWE-bench" | "我搭建了 reproducible evaluation pipeline，产出 pass@1 + 8 项 agent metrics" |
| "我分析了失败" | "我从 N 次 trajectory 中归纳了 coding agent 的 failure taxonomy" |
| "我对比了不同模型" | "我在分析 harness mechanisms × model capabilities 的交互效应" |

---

## 13. v3.0 变更日志

| 版本 | 日期 | 变更 |
|---|---|---|
| v3.0 | 2026-05-21 | **研究味道强化**：Memory 重心→structured working state；新增 Failure Analysis（Day 18）+ trajectory replay；ToT/Multi-Agent 降级为 lightweight；新增 agent metrics + model co-evolution（Day 25-26）；trajectory 加强（OTel-style tracing, tool tree, retry chain）；博客语言→research infra language；新增优先级（P0/P1/P2）和"你能达到什么水平"章节 |
| v2.0 | 2026-05-21 | 对齐 DeepSeek JD，新增 9 个模块 |
| v1.0 | 2026-05-01 | 初始计划 |
