# Day 21 — KV Cache 原理 + 端到端 Demo + W3 复盘

## Why this day matters
串联 W3 收尾。先补 KV Cache 原理（轻量），然后串起所有模块跑端到端 demo——验证 W3 建设的 harness 能否协同工作。

## Reading (1)
- Karpathy LLM 课，KV Cache 部分（约 30 分钟）→ [YouTube](https://www.youtube.com/watch?v=kPRA0W1kEC8)

## Build tasks

### Part A — KV Cache 原理（1-2 小时）
`docs/notes/day21_kv_cache.md`：
- KV Cache 是什么：存储每个 token 的 Key 和 Value，避免重复计算 prefix
- 内存代价：sequence_length × num_layers × 2 × d_model × num_heads
- 和 prompt caching 的区别：模型层 vs API 层
- 作为 harness 开发者，如何优化 KV Cache 利用？（system prompt 每轮发送 → 适合 caching）

可选：`experiments/day21_kv_cache.py` — 纯 PyTorch tiny transformer KV Cache demo（时间不够跳过）

### Part B — 端到端 demo（4 小时）
`experiments/day21_full_demo.py`：
```bash
python experiments/day21_full_demo.py \
    --task "Implement an HTTP todo service with tests" \
    --provider claude \
    --memory-working-state \
    --context-strategy hierarchical
```
任务流：
1. Agent 收到任务 → Skills 发现（file_editor + code_runner）
2. Agent 写代码 → 遇到 bug → Working State 记录失败
3. Agent spawn 子 agent 写测试 → 子 agent 完成后汇报
4. Agent 运行测试 → 失败 → 从 working state 检索历史 → 修复
5. 所有测试通过 → finish

记录完整 trajectory。

### Part C — W3 复盘
`docs/notes/week3-retro.md`：
- 总代码行数（`tokei agent/`）
- 总 API 花费
- W3 最大的 3 个收获
- 哪些模块需要重构
- W4 预算估算

### Part D — SWE-bench 准备
- `git clone https://github.com/SWE-bench/SWE-bench ~/code/swe-bench`
- 读 README Quickstart + Evaluation
- 预览 2-3 个 tasks 的 problem_statement

## Acceptance criteria
- [ ] KV Cache 原理笔记
- [ ] 端到端 demo 跑通（working state + context + skills + subagent 协作）
- [ ] trajectory 记录完整
- [ ] W3 复盘笔记

## Commit message
`day21: KV Cache notes + end-to-end demo with full harness + W3 retro`

## If you fall behind
- 端到端 demo 只跑 Claude provider，KV Cache 只做笔记不做 demo
