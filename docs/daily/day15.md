# Day 15 — Skills 框架

## Why this day matters
JD 要求"熟悉 Skills"。今天设计一个可插拔的技能机制——agent 能根据任务自动发现和加载合适的技能，而不是把所有能力硬编码。这是 Claude Code 等产品的核心机制之一。

## Build tasks

### 1. Skill 抽象
`agent/skills/base.py`：
```python
class Skill(BaseModel):
    name: str                    # "file_editor", "code_runner"
    description: str             # 模型看到的技能描述
    trigger_patterns: list[str]  # 自动匹配的关键词/正则
    handler: Callable           # 执行逻辑
    config: dict = {}           # 技能特定配置

class SkillRegistry:
    def register(self, skill: Skill) -> None: ...
    def discover(self, task: str) -> list[Skill]:  # 根据任务描述匹配技能
        ...
    def load(self, skills: list[Skill]) -> list[Tool]:  # 技能 → Tool 列表
        ...
```

### 2. 内置技能（3 个）
- **`file_editor`**：read_file + write_file + search_replace 的组合技能，描述中包含"编辑代码、修改文件"
- **`code_runner`**：在 sandbox 中运行代码，自动检测语言（python/node/rust），处理依赖安装
- **`debug_assistant`**：读错误输出 → 定位源码 → 分析原因 → 建议修复

### 3. 技能发现
agent 收到任务后，先用 skill registry 的 `discover()` 匹配技能，再把匹配到的技能加载到 tool list。不需要的技能不占 context。

### 4. 测试
`agent/tests/test_skills.py`：
- "fix the bug in main.py" → 应发现 file_editor + debug_assistant
- "run the tests" → 应发现 code_runner
- "write a new feature" → 应发现 file_editor

## Acceptance criteria
- [ ] Skill 抽象 + SkillRegistry 实现
- [ ] 3 个内置技能可注册
- [ ] 技能发现测试通过（正确匹配 + 不误匹配）

## Commit message
`agent: skills framework with registry, 3 built-in skills, auto-discovery`

## If you finish early
- 第 4 个技能：`git_manager`（git diff/log/status/commit）

## If you fall behind
- 2 个内置技能（file_editor + code_runner），debug_assistant 顺延
