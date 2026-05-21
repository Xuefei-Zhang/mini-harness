# Day 16 — Memory 系统（structured working state 为主）

## Why this day matters
→ 服务于长任务：50-step 的任务中，agent 必须记住"我已经改了 3 个文件，还有 2 个没动，上次失败是因为 X"。
DeepSeek 关心的不是"agent 以前聊过什么"，而是 **"agent 当前在做什么、下一步该干嘛"**。

## Reading (1)
- Anthropic paper 中 memory 章节

## Build tasks

### 1. Structured Working State（核心）
`agent/memory/working_state.py`：
```python
class WorkingState(BaseModel):
    current_goal: str
    subtasks: list[Subtask]           # 分解后的子任务
    attempted_actions: list[ActionRecord]   # 已尝试的操作
    known_failures: list[FailureRecord]    # 已知失败及原因
    modified_files: list[str]              # 已修改的文件
    open_questions: list[str]              # 待确认的问题

class WorkingStateTracker:
    def update_from_step(self, step: ToolUseBlock, result: str) -> None: ...
    def inject_into_prompt(self) -> str: ...  # → system prompt 的 working state 段落
```
每个 step 自动更新 working state。→ 长任务中这是 agent 的"任务板"。

### 2. 短期 Memory（滑动窗口）
`agent/memory/short_term.py`：Last N messages / token budget，保持 tool 配对。

### 3. 长期 Memory（轻量，关键词检索）
`agent/memory/long_term.py`：SQLite + FTS5，存跨 session 的关键决策。→ 长任务中断后恢复。
**不做 embedding 检索**——embedding 检索是 RAG 的东西，和 coding agent 的 working memory 关系不大。

### 4. 实验
`experiments/day16_memory.py`：
- 任务：让 agent 实现一个 3 文件的小项目（app.py, models.py, test_app.py）
- 对比：same task, with/without working state → 对比 success rate / avg steps / recovery from failure
- 跨 session：让 agent 中断 → 恢复 → 检查 working state 是否正确

## Acceptance criteria
- [ ] **Structured Working State**（核心）实现，能自动更新 + 注入 prompt
- [ ] 短期 memory 滑动窗口（保持 tool 配对）
- [ ] 长期 memory（SQLite + FTS5，不用 embedding）
- [ ] 对比实验：working state 对成功率的影响

## Commit message
`agent: structured working state + short-term memory + lightweight long-term store`

## If you fall behind
- 只做 working state + 短期 memory，长期 memory 用内存 list 代替
