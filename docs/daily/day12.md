# Day 12 — MCP tool server v0

## Why this day matters
MCP (Model Context Protocol) is the emerging standard for tool servers — Anthropic, OpenAI, and the Coze/Dify ecosystems all support it. By implementing it from spec (not via SDK) you can speak fluently about it in interviews and your tools become drop-in usable in Claude Desktop, opencode, Continue, etc.

## Reading (1)
- MCP "Tools" subsection of the spec — https://modelcontextprotocol.io/specification/2025-06-18/server/tools
  Plus the **stdio transport** section (~5 minutes). That's all. The protocol is small.

## Build tasks

### Part A — Minimal MCP server (4 hours)
`tools/mcp_server/server.py` — a single file Python program speaking MCP over stdio.

Required JSON-RPC methods:
- `initialize` — return server name `mini-harness`, protocol version `2025-06-18`, capabilities `{tools: {}}`
- `tools/list` — return the four tools below
- `tools/call` — dispatch by name

Tools (each returns MCP `content` array):

1. **`read_file`** — args: `{path: str, offset?: int, limit?: int}`; reads from a configurable workspace root (no escaping it)
2. **`write_file`** — args: `{path: str, content: str}`; same workspace constraint
3. **`run_shell`** — args: `{cmd: str, timeout_seconds?: int}`; **runs inside your `Sandbox` from Day 11**, returns stdout+stderr+exit_code
4. **`search_code`** — args: `{pattern: str, path?: str}`; shells out to `rg --json --max-count=50` (also via Sandbox)

Use **stdio transport**: read JSON-RPC messages line-delimited from stdin, write to stdout, log to stderr only. No third-party MCP library — implement the framing yourself. The whole thing should be ~300 lines.

### Part B — Workspace safety
- Take `--workspace /path` CLI arg
- Reject any `read_file`/`write_file` whose resolved path is outside workspace (handle `..`, symlinks, absolute paths)
- Add a unit test: `test_workspace_escape_rejected.py`

### Part C — Connect to Claude Desktop
Add `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "mini-harness": {
      "command": "/Users/xuefeiz2/self/mini-harness/.venv/bin/python",
      "args": ["-m", "tools.mcp_server.server", "--workspace", "/Users/xuefeiz2/code/scratch"],
      "env": {}
    }
  }
}
```
Restart Claude Desktop. Verify the four tools appear in the `🔌` menu. Have Claude do: *"Read README.md from my scratch repo, suggest one improvement, write a new file CHANGES.md with the suggestion."*

### Part D — Connect to opencode
opencode also supports MCP (see opencode docs). Add equivalent config under `~/.config/opencode/`. Verify `run_shell` works in a sandbox there too. (This is your dogfooding moment — you're using your own sandbox via your own MCP server through opencode.)

## Acceptance criteria
- [ ] `python -m tools.mcp_server.server --workspace /tmp` responds correctly to a hand-written `initialize` + `tools/list` JSON-RPC over stdio (script it as a smoke test in `tools/mcp_server/tests/`)
- [ ] Claude Desktop sees all 4 tools and successfully runs an end-to-end task
- [ ] `run_shell` is sandboxed (verify by attempting `cat /etc/shadow` → fails)
- [ ] Workspace escape test passes

## Commit message
`tools: MCP server v0 with read/write/shell/search tools, sandboxed`

## If you finish early
Add a `list_directory` tool. Add a `tools/get` method showing each tool's full schema (some clients need this).

## If you fall behind
Drop `search_code` — `read_file` + `run_shell` cover the same surface area; agent can run `rg` itself via shell.
