# 一个月 Agent Infra / Harness 求职冲刺计划 v1.0

> 起始日期：2026-05-01
> 目标岗位：Agent Infrastructure / Harness / Coding Agent 工程师
> 目标公司：国内一线大模型六小虎（Moonshot/智谱/MiniMax/百川/阶跃/零一）+ 大厂 AI Lab（字节豆包/阿里通义/腾讯混元/百度文心）+ DeepSeek/幻方
> 每周投入：40+ 小时
> 投递启动：Day 30

---

## 0. 背景与定位

### 我的优势（对 Agent/Harness 岗位非常加分）
- 7 年系统软件 + 全栈（app→middleware→driver→fw）经验 → Harness 工程师的核心素养（沙箱、进程隔离、IPC、性能优化）
- 多 OS 平台经验（Windows/Linux/FreeRTOS）→ 容器化、跨平台执行环境天然契合
- C/C++ 系统级能力强 → Agent runtime、tool sandbox 的底层实现需要
- 实际用过 opencode、多家模型 → 有 agent product sense

### 短板（需要补的）
- 缺少 Python/TypeScript 现代后端栈的工程化经验
- 没有公开的 LLM/Agent 项目作品
- 对 agent 核心概念停留在使用层面，缺实现深度
- 缺少 evaluation/harness 经验

### 战略选择（已确认）
- All-in Agent 方向，一个月内不分散精力到推理岗
- 硬件不投入（推迟到 W5+ 决策），把钱花在 API 和云资源（预算 ¥3000-5000/月）
- 主线：一个项目串三个方向（Infra + Harness + Coding Agent）
- C++ 写 sandbox 核心作为差异化武器
- 全开源 + 中英博客双发

---

## 1. 核心交付物总览（Day 30 末尾）

1. **GitHub 项目 `mini-harness`**：~3000-5000 行代码
   - C++ sandbox（cgroups + seccomp + namespaces）
   - Python agent loop（支持 4 个 LLM provider）
   - MCP tool server
   - SWE-bench Lite evaluation pipeline
2. **4 篇技术博客**（中英双语）
3. **更新后的简历**（含项目链接 + 量化 metric）
4. **目标公司清单 + JD skill mapping 表**
5. **20-30 家公司的投递规划**

---

## 2. 主线项目：mini-harness

> 一个面向 coding agent 的最小可运行 evaluation harness
> 对标：SWE-bench 官方 harness 的简化版 + Anthropic claude-code-action 内核

### 四个组件
| 组件 | 方向 | 技术栈 |
|---|---|---|
| Sandbox Runtime | Infra | C++（cgroups v2 + seccomp + namespaces）+ Python SDK |
| Tool Server | Infra | Python，MCP 协议 |
| Agent Loop | Coding Agent | Python async，多 provider 适配 |
| Eval Pipeline | Harness | Python，对接 SWE-bench Lite |

### 为什么对求职杀伤力大
- 一个项目同时证明三个方向的能力
- 国内做 SWE-bench 复现的人很少
- C++ sandbox 部分纯系统工程师才能写好，差异化优势
- 完全开源 + 4 篇博客，HR 搜名字直接命中

---

## 3. 周度规划

| 周 | 主题 | 核心产出 |
|---|---|---|
| W1 | Agent 基础 + Python 异步 + 读源码 | 1 篇博客；fork opencode；3 个架构图 |
| W2 | Sandbox（C++）+ MCP Tool Server | sandbox v0 + MCP server v0；1 篇博客 |
| W3 | Agent Loop + 多模型 + Trajectory | end-to-end demo；1 篇博客 |
| W4 | SWE-bench 接入 + 简历包装 + 投递 | SWE-bench Lite ≥10 题跑通；1 篇博客；投递启动 |

### 每周节奏
- 周一-周二：理论 + 读源码（输入）
- 周三-周五：编码（输出）
- 周六：写博客 + 整理 commit（沉淀）
- 周日：休息 + 复盘 + 调整下周计划

---

## 4. W1（Day 1-7）：Agent 概念入门 + 现代 Python + 源码精读

**目标**：从"用过 agent"升级到"理解 agent 内部如何工作"

### Day 1 - 环境与认知校准
- 上午：注册 Claude/DeepSeek/Qwen/OpenRouter API；配好 opencode；初始化 GitHub repo
- 下午：精读 Anthropic [Building effective agents](https://www.anthropic.com/research/building-effective-agents)
- 晚上：精读 ReAct paper（arxiv 2210.03629），200 行 Python 手写 ReAct agent（不用框架）
- 产出：`experiments/day01_react_from_scratch.py`

### Day 2 - 现代 Python 速通
- 主题：asyncio、pydantic v2、httpx、uv 包管理、structlog
- 实操：把 day01 重写成 async 版本，加 pydantic 类型
- 产出：`experiments/day02_async_react.py`，能并发跑 10 个任务

### Day 3-4 - 精读 opencode 源码
- 重点：tool 调用序列化、permission 系统、session 管理、context window 处理
- 画一张架构图（excalidraw）
- Day 4 晚上：开博客 1《从系统工程师视角拆解 opencode 架构》

### Day 5-6 - 精读 aider + SWE-agent 源码
- aider：repo map、edit 格式、git 集成
- SWE-agent：ACI 思想、action space 设计
- Day 6 晚上：发布博客 1（掘金 + GitHub Discussions）

### Day 7 - W1 复盘 + W2 准备
- 整理笔记到 `docs/notes/`
- 阅读 MCP spec、Firecracker design 概览
- 列出 W2 sandbox + tool server v0 的接口设计

**W1 产出 checklist**
- [ ] `experiments/` 下 5+ 个学习脚本
- [ ] 1 篇博客发布
- [ ] opencode + aider + SWE-agent 三张架构图
- [ ] mini-harness 仓库初始化

---

## 5. W2（Day 8-14）：Sandbox（C++）+ MCP Tool Server

**目标**：交付项目里最差异化的两个组件

### Day 8 - Sandbox 设计与选型
- 调研 E2B / Modal sandbox / Daytona / Anthropic code-execution
- 决策：v0 Docker exec + seccomp + cgroups；v1 Firecracker（W4 选做）
- 写 `docs/design/sandbox.md`（面试谈资）

### Day 9-11 - C++ sandbox 核心
- Day 9：基于 `clone3` + namespace + cgroups v2 写 mini-runc，限制 CPU/内存/磁盘/网络
- Day 10：seccomp-bpf 系统调用过滤；超时与 OOM 处理
- Day 11：Python SDK 包装（subprocess + JSON IPC）；测试：fork bomb、内存炸弹、网络逃逸、文件系统逃逸
- 预计：800-1500 行 C++ + 300 行 Python

### Day 12 - MCP tool server v0
- 4 个工具：`read_file` / `write_file` / `run_shell`(in sandbox) / `search_code`(ripgrep)
- 严格遵守 MCP spec，能被 Claude Desktop 直接连上
- 自测：用 Claude Desktop 修一个本地 bug

### Day 13 - 集成测试 + 博客 2
- demo：agent 在 sandbox 里写一个 Python web 服务并测试
- 博客 2《用 C++ 实现一个 LLM agent 的最小 sandbox：从 cgroups 到 seccomp》
- 必带：架构图、性能数据（启动延迟、内存）、与 E2B 对比

### Day 14 - W2 复盘
- 整理代码 + README sandbox 章节
- 录 30 秒 asciinema demo

**W2 产出 checklist**
- [ ] sandbox 拦住 4 类逃逸攻击
- [ ] MCP server 能被 Claude Desktop 调用
- [ ] 博客 2 发布
- [ ] 仓库代码 ≥ 2000 行

---

## 6. W3（Day 15-21）：Agent Loop + 多模型 + Trajectory

**目标**：把 sandbox + tool server 串成能干活的 coding agent

### Day 15-16 - Agent loop v0
- 核心 loop：`while not done: complete → parse → execute → append`
- 多模型适配层：`LLMClient` 抽象，实现 Anthropic / OpenAI / DeepSeek / Qwen
- 关键设计点（面试高频）：
  - context window 超限处理（trimming / summarization）
  - tool_call 失败 retry
  - agent 卡住检测（重复 action）
  - trace 序列化

### Day 17 - Trajectory 系统
- 每次运行产出结构化 trajectory（JSON Lines）
- 字段：prompt / response / tool_call / tool_result / cost / latency
- 实现 trajectory viewer（streamlit 或纯 HTML）

### Day 18-19 - 端到端 demo
- 任务：mini Flask repo 修真实 bug 并通过测试
- 4 个 model 各跑一次，对比成功率/token/耗时
- README 放对比表

### Day 20 - 博客 3
- 《手写一个支持 4 家模型的 coding agent loop：那些 paper 不会告诉你的工程细节》
- 重点：context 管理、retry、stuck detection 等"脏活"

### Day 21 - W3 复盘
- 修 bug + 补测试 + 整理 commit history

**W3 产出 checklist**
- [ ] agent 在 sandbox 完成端到端任务
- [ ] 4 个 LLM provider 跑通
- [ ] trajectory viewer 可用
- [ ] 博客 3 发布
- [ ] 仓库代码 ≥ 3500 行

---

## 7. W4（Day 22-30）：SWE-bench 接入 + 求职启动

### Day 22-24 - SWE-bench Lite 接入
- clone SWE-bench 官方 repo，理解数据格式
- dataset loader：取 10-20 题（先选 django/sympy 简单题）
- evaluation pipeline：跑 agent → 应用 patch → 跑测试 → 输出 pass/fail
- 复用 SWE-bench 官方 docker 镜像

### Day 25-26 - 跑通 + 调优
- Claude Sonnet 4.5 跑一遍，目标 pass@1 ≥ 30%
- DeepSeek 跑一遍对比
- 针对性改 system prompt + tool 设计

### Day 27 - 博客 4 + 项目收尾
- 《一个月从零写一个 coding agent harness，并在 SWE-bench Lite 上跑出 X% 的成绩》
- 中英双发：掘金 + dev.to + Hacker News + r/LocalLLaMA

### Day 28 - 简历 + JD 反推
- 简历改造：把 IPU 系统软件经验翻译成 agent 岗语言（多 OS、IPC、driver、performance）
- mini-harness 放最前，列 3 个量化 metric
- 4 篇博客作为附录链接
- JD 反推：抓 5 家目标公司 JD，做 skill mapping 表

### Day 29 - 模拟面试
- 自出 10 道高频题：
  - sandbox 设计
  - context window 满了怎么办
  - tool call 失败怎么处理
  - 为什么不用 LangGraph
  - 与官方 SWE-bench harness 区别
  - 如何防止 agent 死循环
- 找朋友模拟面 1-2 次

### Day 30 - 投递启动
- 第一批 5-8 家：内推优先（脉脉/v2ex/即刻）
- 准备"为什么投你"30 秒 + 3 分钟版
- 后续每周 5-10 家

**W4 产出 checklist**
- [ ] SWE-bench Lite 跑出可公布数字
- [ ] 博客 4 发布
- [ ] 简历定稿
- [ ] 第一批投递发出

---

## 8. 学习资源白名单

### 必读 paper
- ReAct（arxiv 2210.03629）
- Toolformer
- SWE-agent
- Reflexion
- Anthropic "Building effective agents"

### 必读源码（按优先级）
1. opencode
2. aider
3. princeton-nlp/SWE-agent
4. claude-code（逆向 npm 包）
5. continuedev

### 必读 spec
- MCP 协议
- OpenAI tool-use schema
- Anthropic tool-use schema

### 必看视频
- Anthropic building-effective-agents 系列
- Andrej Karpathy LLM 课

### 拒绝列表（不看）
- 吴恩达 LangChain 系列课（太浅）
- 各类中文二手教程
- LangChain / LangGraph 全家桶
- RAG / 向量数据库（与本方向几乎无关）

---

## 9. 关键避坑提醒

1. 不学 LangChain/LangGraph——顶尖公司基本不用，自己手写更显功力
2. 不做 RAG/向量数据库——和 agent infra 岗几乎无关
3. C++ sandbox 别过度设计——v0 跑通 > v1 完美
4. 英文博客直接用 Claude 翻译润色，海外 remote +50% 命中率
5. API 预算控制：W1-W3 每天 ¥30-80，W4 跑 SWE-bench 一次 ¥200-500，整月 ≤ ¥3000
6. 这一个月坚决不买显卡，钱留到投递后期决定

---

## 10. 进度追踪

每天结束时在 `docs/notes/dayNN.md` 写一份 30 行内的日报：
- 今日完成
- 遇到的坑
- 明日 top 3
- 项目代码行数 / commit 数

每周末更新本文件的 checklist。
