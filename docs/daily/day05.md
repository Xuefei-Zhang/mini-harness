# Day 05 — Reasoning：Reflexion（重点）+ ToT（lightweight）+ 对比总结

## Why this day matters
Reflexion 是工业界实际在生产中用的推理增强——"失败后反思 → 下次避免"。ToT 只是 lightweight demo 体现广度。最终产出三种模式的对比分析。

## Reading (1)
- [Reflexion](https://arxiv.org/abs/2303.11366) — abstract + method

## Build tasks

延续 `experiments/day04_reasoning_modes.py`：

### 1. Reflexion（反思记忆）— 重点
- 每次失败后让模型生成反思："为什么失败？下次怎么避免？"
- 反思存入 memory（list 即可）
- 下次运行时将历史反思注入 prompt
- 观察同一任务第 1/2/3 次尝试是否改善
- **核心问题**：reflection 需要几次迭代才能从失败到成功？token 代价是否值得？

### 2. ToT（Tree of Thoughts）— lightweight demo
- 对 1-2 个任务做 ToT：每个决策点生成 3 分支 → 投票选最佳
- 不用追求完美实现，证明"你理解这个模式"即可

### 3. 三种模式对比
选 1-2 个任务，跑 baseline / CoT / Reflexion / ToT：

| 模式 | 成功 | 步数 | tokens | latency | 质量 |

### 4. 对比总结 → `docs/notes/day05_reasoning_comparison.md`
- 每种模式核心机制（2-3 句）
- 对比表
- 你的结论：工业界场景下推荐用哪种？代价是什么？
- **research infra language**："我在分析 reasoning strategies 对 task completion rate 的影响"

## Acceptance criteria
- [ ] Reflexion 实现（反思 → memory → 注入 → 观察改善）
- [ ] ToT lightweight demo（1-2 任务）
- [ ] 对比表 + 分析

## Commit message
`day5: Reflexion (重点) + ToT demo, 3-mode reasoning comparison`

## If you fall behind
- 只做 Reflexion，ToT 一行笔记带过
