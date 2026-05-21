# Day 03 — Prompt Engineering 实践

## Why this day matters
DeepSeek JD 要求"对模型行为有品味有判断力"。你不能只说"好的 prompt 效果更好"，你得能用数据证明。今天为 agent 写 3 套不同风格的 system prompt，A/B/C 测试，用数据说话。面试时的硬通货。

## Reading (1)
- Anthropic [Prompt Engineering guides](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering) — 只看 "System prompts" 和 "XML tags" 两节

## Build tasks

创建 `experiments/day03_prompt_ab.py`：

### 1. 3 套 System Prompt
- **A（最小指令）**：`"You are a coding assistant that uses tools to answer questions."`
- **B（结构化指令）**：角色定义 + 任务说明 + 输出格式约束 + few-shot 示例
- **C（链式指令）**：要求 agent 先分析 → 再计划 → 再执行 → 最后验证

### 2. 测试集（5-8 个任务）
- 纯计算（1-2 题）
- 文件操作（2-3 题）
- 多步推理（2-3 题）

### 3. 运行：每个任务 × 3 prompts = 15-24 次
记录：成功/失败、步数、prompt tokens / completion tokens、latency、输出质量（1-5）

### 4. 对比表 → `docs/notes/day03_prompt_results.md`
| 任务 | Prompt | 成功 | 步数 | tokens | latency | 质量 |
|---|---|---|---|---|---|---|

分析：哪套 prompt 在哪些任务上最好？token 消耗差异？生产环境会选哪套？

## Acceptance criteria
- [ ] 3 套 system prompt 定义清晰
- [ ] 5+ 任务 × 3 prompts 的实验数据
- [ ] `docs/notes/day03_prompt_results.md` 有对比表 + 分析

## Commit message
`day3: prompt engineering A/B/C test with 3 prompts, analysis`

## If you finish early
- 第 4 套 prompt：用 XML tags 结构化（Anthropic 推荐）
- 对比 Sonnet vs DeepSeek 对同一 prompt 的响应差异

## If you fall behind
- 3 个任务 × 3 prompts = 9 次运行，够用
