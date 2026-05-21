# Day 26 — 终极挑战：长任务验证

## Why this day matters
这是整个 30 天的最终验证。你之前写的每一个模块——working state、context manager、failure recovery、subagent、trajectory——不是为了 demo，是为了让 harness 能驱动模型完成一项**真正长任务**。

如果成功，这是简历上最重的一句话：
> "我用自己的 harness 驱动模型为 [项目名] 提交了一个可 merge 的 PR。"

## Build tasks

### Part A — 选项目/任务（1 小时）
三选一：
1. **vLLM**：GitHub 找 `good first issue` 或 `bug`
2. **FastAPI**：找一个 bug fix 或小型 feature
3. **从零实现**：给定 spec，实现一个中等复杂度项目（如 HTTP 缓存中间件：LRU + TTL + benchmark）

关键标准：任务需要 30-80 steps，跑 1-3 小时，涉及多文件修改。

### Part B — 让 harness 跑起来（全天下）
```bash
python experiments/day26_ultimate.py \
    --provider claude \
    --task "Fix vLLM issue #XXXX: [description]" \
    --workspace /path/to/vllm \
    --memory-working-state \
    --context-strategy hierarchical \
    --failure-recovery enabled \
    --trajectory trajectories/ultimate.jsonl
```

观察：
- agent 能否在 50+ steps 后仍然"知道"自己在做什么？
- context 膨胀到 80k tokens 后，裁剪策略是否保留了关键信息？
- 失败后 working state 是否帮助 agent 避免重蹈覆辙？
- subagent 是否在合适的时候被 spawn？

### Part C — 如果 agent 卡住了
这不是失败。这是最有价值的部分。

用 trajectory replay 分析卡在哪、为什么。修复 harness → 重新跑。这就是"与模型共同进化"。

### Part D — 记录一切
`docs/notes/day26_ultimate_challenge.md`：
- 选了什么项目/issue
- 跑了多少步、多少小时、多少 cost
- 失败了几次、harness 如何恢复
- 最终结果：PR 能否 merge？代码质量如何？
- **harness 的哪些机制在长任务中真正起了作用？哪些没用？**

## Acceptance criteria
- [ ] 长任务至少跑完一轮（不管成功还是失败）
- [ ] trajectory 记录完整（30+ steps）
- [ ] `day26_ultimate_challenge.md` 笔记完整
- [ ] 如果失败了：分析原因 + harness 需要改进的点

## Commit message
`day26: long-horizon task — harness drives agent through [X]-step task`

## If you finish early
- 让 DeepSeek 跑同一任务，对比结果
- 如果产出 PR：完善 PR description，提交

## If you fall behind
- 缩小任务范围：不是"实现整个 feature"，而是"修这一个 bug"
- 但不要让步到"只跑 10 steps"——失去长任务的意义

---

> **这不是 Day 26。这是 30 天来的每一个决策为什么这样做的答案。**
