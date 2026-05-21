# Day 13 — MCP Tool Server v0

## Why this day matters
MCP（Model Context Protocol）是 tool server 的新标准——Anthropic、OpenAI、Coze/Dify 都支持。你从 spec 实现（不用 SDK），面试时能讲透协议细节。你的工具还能直接接入 Claude Desktop、opencode、Continue。

## Reading (1)
- MCP "Tools" + "stdio transport" — https://modelcontextprotocol.io/specification/2025-06-18/server/tools
  5 分钟，协议很小。

## Build tasks

### Part A — 最小 MCP server（4 小时）
`tools/mcp_server/server.py`：单文件 Python，MCP over stdio。

JSON-RPC 方法：
- `initialize` → server name `mini-harness`, protocol version, capabilities `{tools: {}}`
- `tools/list` → 返回 4 个工具
- `tools/call` → 按名字分发

工具（每个返回 MCP `content` 数组）：
1. **`read_file`** — `{path, offset?, limit?}`，workspace 根目录约束
2. **`write_file`** — `{path, content}`，同 workspace 约束
3. **`run_shell`** — `{cmd, timeout_seconds?}`，在 sandbox 内运行
4. **`search_code`** — `{pattern, path?}`，调用 `rg --json --max-count=50`

**不用第三方 MCP 库**，自己实现 framing。~300 行。

### Part B — Workspace 安全
- `--workspace /path` CLI 参数
- 拒绝 workspace 外的路径（处理 `..`、symlink、绝对路径）
- 单元测试：`test_workspace_escape_rejected.py`

### Part C — 连接 Claude Desktop
配置 Claude Desktop → 验证 4 个工具出现 → 让 Claude 在 scratch 目录完成一个任务。

## Acceptance criteria
- [ ] `python -m tools.mcp_server.server` 响应 initialize + tools/list 正确
- [ ] Claude Desktop 看到 4 个工具并成功运行
- [ ] `run_shell` 在 sandbox 内执行（`cat /etc/shadow` → 失败）
- [ ] workspace 逃逸测试通过

## Commit message
`tools: MCP server v0 with read/write/shell/search, sandboxed`

## If you finish early
- 加 `list_directory` 工具

## If you fall behind
- 去掉 `search_code`，agent 可以通过 `run_shell` 调用 `rg`
