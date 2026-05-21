# Agent Harness 面试题库

> 按面试高频度排序。每天挑 1-2 题，写下你的回答 → agent 帮你修正 → 你总结。
>
> **用法**：
> 1. 每天选 1-2 个 `[ ]` 题目
> 2. 在下方对应题目下写你的回答（或直接口头回答）
> 3. 让 agent 帮你修正/补充
> 4. 答完改为 `[x]`，最终在底部"我的答案总结"区写精简版
>
> **目标**：Day 29 模拟面试前，P0 题全部 `[x]`，P1 题至少 70% `[x]`。

---

## 一、Agent Loop & 核心机制（🔴 P0，面试必问）

### 1.1 Agent Loop
- [ ] **Q1**: 描述一个完整的 agent loop。从用户输入到最终输出，每一步发生了什么？
- [ ] **Q2**: agent 卡住了（死循环同一个 tool call），你怎么检测和处理？
- [ ] **Q3**: 你的 agent loop 和 ReAct paper 中的描述有什么差异？为什么？
- [ ] **Q4**: 如果 agent 在第 47 步才完成任务，context window 早满了——你怎么处理的？
- [ ] **Q5**: 你为什么不直接用 LangGraph，要自己写 agent loop？

### 1.2 Tool Use
- [ ] **Q6**: 描述 tool use 的完整流程：模型返回 tool_call → 解析 → 验证 → 执行 → 结果返回。每一步可能出错吗？怎么 recover？
- [ ] **Q7**: 如果你的 tool 执行失败了（比如 shell 命令返回非 0），你怎么把这个信息反馈给模型？
- [ ] **Q8**: tool call 的 retry 策略是什么？什么时候重试，什么时候不重试？
- [ ] **Q9**: tool 的描述（description）对模型选择工具有多大影响？你做过实验吗？

### 1.3 MCP
- [ ] **Q10**: MCP 协议的生命周期是什么？`initialize` → `tools/list` → `tools/call`，每一步交换什么数据？
- [ ] **Q11**: MCP 的 stdio transport 和 SSE transport 有什么区别？你为什么选 stdio？
- [ ] **Q12**: MCP server 的 workspace 安全怎么做？如何防止路径逃逸（`../`、symlink）？

### 1.4 Provider 抽象
- [ ] **Q13**: 你如何设计多 provider 的抽象层？Anthropic 和 OpenAI 的 tool-use schema 有什么不同？怎么统一？
- [ ] **Q14**: 不同 provider 对同一 prompt 的响应差异大吗？你观察到什么 pattern？

---

## 二、Context Engineering（🔴 P0，面试高频）

### 2.1 Context 管理
- [ ] **Q15**: context window 满了怎么办？你实现了几种裁剪策略？各有什么 trade-off？
- [ ] **Q16**: `drop_oldest` 和 `summarize_oldest` 在什么场景下各更优？你有数据支撑吗？
- [ ] **Q17**: 你如何计算 message 的 token 数？不同 provider 的 tokenizer 不同怎么处理？
- [ ] **Q18**: tool_use / tool_result 配对在裁剪时怎么处理？能拆开吗？

### 2.2 Prompt Caching
- [ ] **Q19**: Anthropic 的 prompt caching API 怎么用？你在 harness 中怎么利用它？
- [ ] **Q20**: prompt caching 和 KV Cache 是什么关系？一个在 API 层，一个在模型层？
- [ ] **Q21**: 你的 agent loop 中哪些设计影响了 prompt cache hit rate？

### 2.3 长 Context
- [ ] **Q22**: 如果 agent 跑了 100 步，context 膨胀到 150k tokens——你的 harness 怎么处理？
- [ ] **Q23**: hierarchical 裁剪策略的核心思想是什么？为什么比 drop_oldest 好？

---

## 三、Memory & Working State（🔴 P0 / 🟡 P1）

- [ ] **Q24**: agent 的 memory 系统有哪些层次？短期 memory 和长期 memory 的区别是什么？
- [ ] **Q25**: 你为什么选择 structured working state 而不是 embedding-based memory？trade-off 是什么？
- [ ] **Q26**: working state 在长任务（50+ step）中起到了什么作用？有实验数据吗？
- [ ] **Q27**: agent 在跨 session 恢复时，working state 如何持久化和加载？

---

## 四、Sandbox & Runtime（🔴 P0，差异化加分）

### 4.1 cgroups / namespaces / seccomp
- [ ] **Q28**: 描述你的 sandbox 架构。cgroups v2 限制了哪些资源？namespaces 隔离了什么？
- [ ] **Q29**: seccomp-bpf 的工作原理是什么？你过滤了哪些系统调用？为什么？
- [ ] **Q30**: 如果 agent 在 sandbox 里跑了 fork bomb / 10GB 内存分配 / `curl` 外网 / `cat /etc/shadow`，你的 sandbox 怎么拦住？
- [ ] **Q31**: 你的 sandbox cold start 延迟是多少？和 E2B / Docker exec 对比如何？
- [ ] **Q32**: clone3 和 clone 的区别？为什么选 clone3？

### 4.2 安全设计
- [ ] **Q33**: sandbox 的 threat model 是什么？你防什么？不防什么？
- [ ] **Q34**: 如果模型在 sandbox 里生成了恶意代码并执行了——你的 sandbox 能拦住吗？边界在哪？

---

## 五、Evaluation & Harness（🔴 P0）

### 5.1 SWE-bench
- [ ] **Q35**: SWE-bench Lite 的数据格式是什么？`problem_statement`, `patch`, `test_patch` 各是什么？
- [ ] **Q36**: 你的 evaluation pipeline 怎么工作的？agent → patch → test → pass/fail，每步怎么做？
- [ ] **Q37**: 你的 agent 在 SWE-bench Lite 上的 pass@1 是多少？和 baseline（直接发给模型）比提升了多少？
- [ ] **Q38**: SWE-bench 官方 harness 和你的 harness 有什么区别？

### 5.2 Agent Metrics
- [ ] **Q39**: 你定义了哪些 agent metrics？每个 metric 怎么计算？为什么重要？
- [ ] **Q40**: 如果你的 avg_tool_calls 很高（50+），是 agent 能力差还是 task 复杂？你怎么判断？
- [ ] **Q41**: token_efficiency（每步平均 token）和成功率的关系是什么？你观察到什么 trade-off？

### 5.3 Failure Analysis
- [ ] **Q42**: 你归纳了哪些 agent 失败模式？每种占多少比例？
- [ ] **Q43**: 哪些 harness 机制能减少哪些失败类型？有数据吗？
- [ ] **Q44**: 你的 trajectory replay 怎么实现的？有什么用途？

---

## 六、Model Behavior & Co-evolution（🔴 P0，研究味道）

- [ ] **Q45**: 你观察到哪些 harness 机制让 DeepSeek 模型表现更好？让 Sonnet 更好的？
- [ ] **Q46**: 特定 prompt 结构（结构化 vs 链式）对不同模型的影响有什么差异？
- [ ] **Q47**: memory 注入时机（每步 vs 仅在失败后）对模型表现有什么影响？
- [ ] **Q48**: context 策略（drop_oldest vs hierarchical）对 pass@1 的影响？
- [ ] **Q49**: 你对"模型行为"的判断力体现在哪里？能举一个你发现模型 behavior pattern 的例子吗？

---

## 七、System Design（🟡 P1）

- [ ] **Q50**: 如果让你设计一个支持 1000 个并发 agent 的 harness，架构是什么样？
- [ ] **Q51**: 如果每个 agent 平均跑 30 分钟、消耗 $0.50——如何控制 1000 并发的成本？
- [ ] **Q52**: 如何实现 agent 的 checkpoint / resume？断点续跑怎么设计？
- [ ] **Q53**: 如何实现 agent trajectory 的分布式存储和查询？
- [ ] **Q54**: 如果要在 harness 上加 rate limiting（每个 provider 每分钟 N 次请求），怎么设计？

---

## 八、Multi-Agent & Subagent（🟡 P1 / 🟢 P2）

- [ ] **Q55**: subagent 和 multi-agent 的区别是什么？什么场景用哪个？
- [ ] **Q56**: 你的 planner/executor/reviewer 三角色流水线在什么场景下比单 agent 好？代价是什么？
- [ ] **Q57**: subagent spawn 时，如何分配 tool set？子 agent 需要和主 agent 相同的工具吗？
- [ ] **Q58**: 子 agent 失败时，错误如何传播回主 agent？有几种 fallback 策略？

---

## 九、Reasoning & Planning（🟡 P1）

- [ ] **Q59**: CoT（Chain of Thought）在你的 agent 中怎么实现？和 baseline 比提升了什么、代价是什么？
- [ ] **Q60**: Reflexion（反思学习）和简单的 retry 有什么区别？什么时候 Reflexion 更有效？
- [ ] **Q61**: 你实现了几种 reasoning 模式？哪种在 coding agent 场景下最实用？
- [ ] **Q62**: ToT（Tree of Thoughts）在工业界用得少吗？你觉得为什么？

---

## 十、Prompt Engineering（🟡 P1）

- [ ] **Q63**: 你做过哪些 prompt A/B 测试？结构化 prompt 比最小 prompt 好多少？
- [ ] **Q64**: tool description 对模型选择工具有多大影响？你做过哪些优化？
- [ ] **Q65**: system prompt 和 conversation prompt 的分工是什么？各自放什么信息？
- [ ] **Q66**: 你如何防止模型 hallucinated actions（调用不存在的 tool / 生成非法参数）？

---

## 十一、KV Cache & 底层理解（🟢 P2）

- [ ] **Q67**: KV Cache 是什么？为什么它让 LLM 推理更快？
- [ ] **Q68**: KV Cache 的内存代价是什么？sequence_length × num_layers × 2 × d_model × num_heads？
- [ ] **Q69**: KV Cache 和 prompt caching 的区别？一个在模型层，一个在 API 层？
- [ ] **Q70**: 作为 harness 开发者，你如何优化 KV Cache 利用？

---

## 十二、项目 & 行为面（🟡 P1）

- [ ] **Q71**: 介绍你的 mini-harness 项目。为什么做这个？它解决了什么问题？
- [ ] **Q72**: 你项目中最大的技术挑战是什么？怎么解决的？
- [ ] **Q73**: 你为什么不用 LangChain / AutoGen / CrewAI？
- [ ] **Q74**: 你的 7 年系统软件背景如何帮助你做 Agent Harness？
- [ ] **Q75**: 你如何证明自己"对模型行为有品味有判断力"？
- [ ] **Q76**: 如果你的 agent 在 SWE-bench 上只跑了 20% pass@1，低于 baseline——你怎么分析？

---

## 十三、每日练习计划

| 周 | 每天练什么 | 题号 | pi-mono 代码文件 |
|---|---|---|---|
| W1 (Day 1-7) | Agent Loop + Tool Use | Q1-4, Q6-8, Q59-62 | `agent-loop.ts`, `agent.ts`, `tools/bash.ts` |
| W2 (Day 8-14) | Sandbox + MCP + Provider | Q28-34, Q10-12, Q13-14 | `stream.ts`, `providers/`, `model-resolver.ts` |
| W3 (Day 15-21) | Memory + Context + Failure | Q15-27, Q39-44 | `compaction/`, `session-manager.ts`, `regressions/` |
| W4 (Day 22-28) | Eval + Model Behavior + System Design + 行为面 | Q35-38, Q45-49, Q50-54, Q55-58, Q71-76 | `harness.ts`, `faux.ts` |
| Day 29 | 模拟面试（从每题型随机选 3-5 题） | 全覆盖 | 无 |

**每日流程**：读 pi-mono 代码 → 回答对应面试问题 → 和 agent 讨论 → 做 mini-harness 实验 → 写总结
完整映射：`docs/notes/pi-mono-learning-map.md`

---

## 十四、我的答案总结

> 每答完一题（和 agent 讨论修正后），在这里写精简版答案（3-5 句话）。
> 这份总结是面试时随身携带的"脑图"。

### 格式
```
## Q[X]: 题目关键词
你的答案（3-5 句，含数据/项目经历）
```

**示例**：
```
## Q1: Agent Loop
我的 agent loop 核心是 `while not done: complete → execute tools → append → check stuck`。
每轮调用 LLMProvider.complete()，如果有 tool_uses 就执行并追加 tool_result，
如果 stop_reason 是 end_turn 或超过 max_steps 就返回。
stuck detector 监控重复 action 和 error cascade，触发后注入 recovery prompt。
在我的实验中，stuck detection 让 agent 在 15% 的失败任务中成功恢复。
```

---

### 待填写区（从上到下填写）

<!-- 在这里按题号填写你的答案 -->
