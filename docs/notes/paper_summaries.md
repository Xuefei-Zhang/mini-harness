# Paper & Research Summaries

> 所有论文的中文摘要 + 关键概念。替代精读论文正文。
> 括号内标注"必读"的论文建议至少看 abstract + intro。其余看这份总结即可。

---

## ReAct (2022) — [arxiv 2210.03629](https://arxiv.org/abs/2210.03629)

**一句话**：让 LLM 在推理（Thought）和行动（Action）之间交替，比纯推理或纯行动都更有效。

**核心机制**：
- Thought-Action-Observation 循环。每一步先生成 Thought（自然语言推理），再选择 Action（工具调用），然后系统返回 Observation（工具输出）。
- Thought 的作用是：让模型"慢下来"，在 commit 到某个行动前显式地思考。这相当于给 autoregressive 模型加了一个外部的推理缓冲区。
- 在训练时，用人类专家轨迹（state-action pair）做 fine-tune；在推理时，zero-shot prompt 就能复现类似效果。

**关键实验结果**：
- HotpotQA（问答）：ReAct zero-shot 比 pure thought 或 pure action baseline 准确率高 4-7%
- Fever（事实核查）：推理质量提升，同时减少幻觉
- ALFWorld（交互式环境）：任务完成率从 ~5% 提升到 ~33%

**为什么有效**：
- Thought 为后续 Action 提供推理链，减少盲目试错
- Observation 为后续 Thought 提供外部信息，打破模型内部知识的局限
- 两者互相强化，形成"推理-验证-修正"的正反馈

**对你的项目的意义**：
- Day 1 的 ReAct 实现就是从这个 paper 来的
- 面试时能回答："ReAct 的本质是给 autoregressive 模型加一个外部的推理循环，让每一步行动都有推理支撑，每一步推理都有数据反馈"
- **Blog 替代**：[Anthropic 对 ReAct 的解读](https://www.anthropic.com/research/building-effective-agents) — 第 4 节 "Agents" 部分

---

## Chain of Thought — [arxiv 2201.11903](https://arxiv.org/abs/2201.11903)

**一句话**：在 prompt 中给几个包含逐步推理的示例，就能让模型学会"一步步想"。

**核心机制**：
- Few-shot prompt 中，每个示例不只是 Q→A，而是 Q→步骤1→步骤2→...→A
- 模型在 autoregressive 生成时，中间步骤成为了"隐式的工作内存"，让它能处理多步推理
- 不需要 fine-tune，zero-shot CoT 甚至可以通过追加 "Let's think step by step" 触发

**关键发现**：
- 在 GSM8K（小学数学题）上，8-shot CoT 把准确率从 ~18% 提升到 ~78%（13B 模型）
- 模型越大，CoT 效果越显著（规模超越 — "emergent ability"）
- 对不需要多步推理的任务，CoT 几乎不帮助，反而浪费 token

**CoT vs ReAct 的区别**：
- CoT = 纯推理链，没有工具调用。适合"模型内部知识够"的任务
- ReAct = 推理 + 工具调用。适合"需要外部信息或精确计算"的任务

**对你的项目的意义**：
- Day 4 实现 CoT 模式：强制 Thought ≥ 2 句，对比 baseline
- token 代价是核心衡量指标：CoT 生成更多 token，但可能减少重试次数

---

## Reflexion (2023) — [arxiv 2303.11366](https://arxiv.org/abs/2303.11366)

**一句话**：让模型在每次失败后生成自然语言的"反思"，下次重试时把反思注入 prompt，模型就能从错误中学习。

**核心机制**：
- 第 1 轮：模型尝试解决问题 → 环境返回成功/失败信号
- 如果失败：模型生成反思："我错了，因为 X。下次应该做 Y。"
- 第 2 轮：prompt 中追加反思作为上下文，模型重新尝试
- 重复直到成功或达到最大轮数

**关键实验结果**：
- HotpotQA：1 次重试就比 baseline 提升 ~10%；3 次重试提升 ~20%
- ALFWorld：5 次重试后完成率从 ~30% 提升到 ~50%+
- 不需要 fine-tune，纯 prompt-based

**工业界的实际形态**：
- OpenAI 的 "analysis mode" 内置了类似机制
- 很多 agent framework 的 "retry with feedback" 是 Reflexion 的简化版
- 关键区别：Reflexion 让**模型自己生成**反思，而不是人工写 feedback

**实现要点**：
- 需要一个判断"成功/失败"的机制（可以是规则、测试用例、或模型自评）
- 反思 prompt 模板："Based on the following feedback: {feedback}, what would you do differently next time?"
- 反思需要存入一个 list，每次重试时全部注入（自指注意力让模型关注最近的反思）

**对你的项目的意义**：
- Day 5 重点实现。这是工业界最可能实际部署的 reasoning 增强
- 实验设计：同一任务跑 1/2/3 轮 Reflexion，记录何时从失败翻盘、token 代价

---

## Anthropic: Building Effective Agents (必读) — [链接](https://www.anthropic.com/research/building-effective-agents)

**一句话**：99% 的 agent 任务不需要复杂的 agent 架构，prompt chaining 就够了；用 agent 的 1% 场景，要正确设计。

**核心观点**：

**Workflow vs Agent**：
- Workflow = 预定义的 LLM 调用序列（prompt chaining / routing / orchestrator-workers / majority vote）
- Agent = LLM 作为控制节点，维护状态、做长期规划、使用工具
- 99% 的应用用 workflow 就够了，只有复杂、动态、长期的任务需要 agent

**4 种 Agent 模式**：
1. **Agent with LLM-powered subtask tools**：workflow 中的某个节点用 agent 代替。最简单，最实用。
0. **Prompt chaining**：线性管道。每个 LLM 调用处理一个节点。适合大多数用例。
2. **Workflow**：非线性管道。路由、并行、orchestrator-workers、majority vote。
3. **Agent with task-specific loop**：知道有限步骤数，循环直到完成。例：SQL 查询、软件调试。
4. **General agents**：开放任务、长期运行。例：SWE-bench、研究助手。

**对 Agent 的忠告**：
- 让模型做规划（planning），不要让外部代码做规划
- 让模型自己维护状态（working state），而不是用外部数据库
- 给模型工具，但要清晰的 tool description
- 添加 "reflection" 步骤能显著提升长期任务表现

**为什么这篇必读**：
- 这是目前最系统的 agent 架构指南
- 面试时引用这篇论文的观点，说明你有架构判断力
- 你的项目设计（structured working state、failure analysis、lightweight multi-agent）完全遵循这篇的指导

---

## SWE-agent — [arxiv 2405.15793](https://arxiv.org/abs/2405.15793)

**一句话**：LLM + 终端 = 能修真实 bug 的 agent。关键是设计好 "Agent-Computer Interface"（ACI）。

**核心机制**：
- **ACI（Agent-Computer Interface）**：agent 不直接编辑文件，而是通过"终端命令"与系统交互。这包括 Bash 命令、文件读取、光标操作。
- **FileReader 工具**：不返回完整文件，而是返回行号标注的内容（`1: import os\n2: def foo():\n...`），让模型能精确引用行号。
- **Observation 裁剪**：命令输出超长时，截断到首尾各 100 行，中间用 `<truncated> `标注。
- **Lint error 解析**：执行命令后，如果出错，解析错误信息并注入下一次 prompt。

**关键实验结果**：
- SWE-bench Verified：Cosine 70B + SWE-agent = ~15% resolve rate（当时 SOTA）
- 关键发现：模型能力比 agent 架构更重要。同样的 ACI，换更强的模型就直接提升

**对你的项目的意义**：
- Day 7 读 SWE-agent 源码。重点关注 ACI 的 action space 设计
- 你的 tool server 可以借鉴 SWE-agent 的 ACI：行号标注的文件操作、输出截断、错误解析
- 面试考点："SWE-agent 的 ACI 设计为什么比直接给模型一个代码编辑器更好？" 答案：终端命令是更细粒度的 action space，模型可以组合出更灵活的操作

---

## Tree of Thoughts (ToT) — [arxiv 2305.10601](https://arxiv.org/abs/2305.10601)

**一句话**：把 CoT 的线性推理扩展为树状搜索——每个决策点生成多个分支，用投票选择最佳路径。

**核心机制**：
- 把问题分解为 K 个推理步骤（不再是隐式的，而是显式的状态）
- 每一步生成 c 个候选 Thought（而不是 1 个）
- 用投票函数（模型自评或外部评估器）筛选最好的候选
- 用 BFS 或 DFS 搜索整个树

**关键实验结果**：
- Game of 24（数学谜题）：CoT 准确率 ~4%，ToT 达到 ~55%
- Creative Writing：ToT 生成的文本被人类评为更有创意
- ARBITRAGE（商业决策）：ToT 显著优于 CoT

**为什么不重在项目中实现**：
- 实际工业场景中，ToT 的 token 代价极高（每步 c 倍膨胀）
- ReAct + Reflexion 在实践中覆盖率更广
- 作为 demo 证明理解即可，不建议在生产 harness 中重度使用

---

## ReWeigh (重加权) — 简注

**一句话**：在 agent 的上下文窗口中，不是所有 token 都同等重要。ReWeigh 通过调整 attention 权重，让关键的 system prompt 和最近的工具输出获得更高的注意力。

**对你的项目**：Day 5 的 Day 17（Context Engineering）相关。实际实现时，更多是在 prompt 层面做"信息密度"优化，而不是改模型权重。

---

## SWE-bench — [GitHub](https://github.com/SWE-bench/SWE-bench)

**一句话**：用真实的 GitHub issue + PR 作为测试集，评估 agent 能否真正修复 bug。

**数据格式**：
- `problem_statement`：GitHub issue 内容
- `base_commit`：需要打补丁的 commit
- `patch`：真实 PR 的 diff（金标准答案）
- `test_patch`：与该 bug 相关的测试用例

**评估流程**：
1. 从 issue 生成 Docker 镜像（安装依赖、checkout base_commit）
2. Agent 在容器内工作，生成补丁
3. 运行 test_patch 中的测试，比较 pass rate
4. `pass@1` = 单轮尝试就修复的比例

**SWE-bench Lite**：191 个任务（完整版是 2294），适合快速迭代

**对你的项目的意义**：
- W4 核心评估。Day 22-24 接入
- 你的 harness 最终需要在 SWE-bench Lite 上跑出数字
- 面试时能说："我的 harness 在 SWE-bench Lite 上达到了 X% pass@1"

---

## 官方文档/Blog 替代阅读

### Anthropic
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — **最重要的一篇文章**，agent 架构指南
- [Long Context Window Tips](https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips) — context engineering 实践
- [Tool Use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — tool calling 协议
- [Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) — 如何降低 token 成本

### OpenAI
- [Assistant API](https://platform.openai.com/docs/assistants/overview) — code interpreter + file search + function calling
- [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs) — 强制 JSON Schema 输出
- [Evaluating Model Performance](https://platform.openai.com/docs/guides/evals) — eval 方法论

### Qwen (通义千问)
- [Qwen Blog](https://qwenlm.github.io/) — 模型架构、训练数据、多模态
- [Qwen Code](https://qwenlm.github.io/blog/qwen-code/) — 编码能力专篇
- Qwen3 技术报告关注：长上下文、tool use 改进、多轮对话

### DeepSeek
- [DeepSeek V3 Technical Report](https://github.com/deepseek-ai/DeepSeek-V3) — MoE 架构、MLLaMA
- [DeepSeek-Coder](https://github.com/deepseek-ai/DeepSeek-Coder) — 代码模型、多阶段训练
- 重点关注：他们如何训练 coding 能力、SWE-bench 成绩

### Google (Gemini)
- [Gemini 1.5 Technical Report](https://ai.google.dev/gemini-api/docs) — 1M context window
- [Agent Toolkit](https://github.com/google-adk/python) — Agent Development Kit
- 重点关注：长上下文处理、tool use 设计

---

## 按 Day 的阅读映射

| Day | 原文献 | 看这份总结的哪一节 | 看原文？ |
|---|---|---|---|
| Day 1 (ReAct 回顾) | ReAct paper | ReAct 节 | 可选，看 Anthropic 文章代替 |
| Day 3 (Prompt Eng) | 无特定论文 | Anthropic Tool Use / Long Context | 不看论文 |
| Day 4 (CoT) | CoT paper | Chain of Thought 节 | 只看 abstract |
| Day 5 (Reflexion+ToT) | Reflexion + ToT | Reflexion + ToT 两节 | Reflexion 看 method |
| Day 6 (opencode) | 无 | 源码阅读 | 不看论文 |
| Day 7 (aider+SWE-agent) | SWE-agent paper | SWE-agent + Anthropic Agents 两节 | **Anthropic 必读** |
| Day 16 (Memory) | Anthropic memory | Anthropic Agents 节 "reflection" 部分 | 可选 |
| Day 22 (SWE-bench) | SWE-bench | SWE-bench 节 | 看 GitHub README |

**Milestone 级别（建议看原文）**：
1. Anthropic: Building Effective Agents — 架构判断力的基石
2. ReAct — 你整个项目的起点，看 abstract + intro + 方法（~30 分钟）

其余看这份总结 + 对应的官方 blog/doc 即可。
