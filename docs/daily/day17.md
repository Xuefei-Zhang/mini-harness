# Day 17 — Context Engineering + 博客 3

## Why this day matters
JD 要求"Context Engineering"。今天实现 context 窗口管理的三种策略和 prompt cache 统计。这是 agent harness 和玩具 loop 的分水岭——面试高频题。

同时写博客 3《Agent Memory 系统设计：从滑动窗口到语义检索》。

## Build tasks

### Part A — Context Manager（3 小时）
`agent/context/manager.py`：
```python
class ContextManager:
    def __init__(self, max_tokens: int, reserved: int = 4096):
        ...
    def fit(self, messages: list[Message]) -> list[Message]:
        """裁剪/压缩后返回能放进窗口 messages"""
```

三种裁剪策略（config 切换）：
1. **`drop_oldest`** — 丢弃最旧的非 system message，保持 tool 配对
2. **`summarize_oldest`** — 超限时把最旧 N 轮发给模型摘要，替换为一条 assistant message
3. **`hierarchical`** — 最近 K 轮原文保留，更早的做一次滚动摘要

### Part B — Prompt Cache（1 小时）
利用 Anthropic prompt caching API：
- 在每次请求中标记 cache breakpoint（通常在 system prompt 末尾）
- 统计 cache hit rate：连续两次调用同一 session 时第二次是否命中
- 记录到 trajectory 事件

### Part C — Token 预算监控
`agent/context/token_tracker.py`：
- 实时跟踪已用 tokens（input + output）
- 显示 budget bar：`████████░░ 80% (48k/60k)`
- 超限事件：记录何时触发裁剪、丢弃了多少 tokens

### Part D — 博客 3
`docs/blog/03-agent-memory-system.md`，~2000 字：
1. 为什么 agent 需要 memory（不是 conversation history）
2. 短期 vs 长期：滑动窗口 + 持久化
3. 检索策略：关键词 vs 语义，trade-off
4. 代码片段 + 实验数据
5. Context Engineering 如何与 memory 协作

## Acceptance criteria
- [ ] 3 种 context 裁剪策略实现 + 测试
- [ ] prompt cache 统计可用
- [ ] token 预算监控
- [ ] 博客 3 发布

## Commit message
`agent: context manager (3 strategies) + prompt cache + blog 3`

## If you fall behind
- 只做 `drop_oldest` + token 监控，博客只写 memory 部分
