# Day 19 — Hardening, system-prompt iteration, cost optimization

## Why this day matters
Day 18 produced a baseline. Today you make it good. The single highest-leverage thing you can change is the system prompt + tool descriptions — better than any code change. You'll also fix the rough edges that will hurt you on SWE-bench next week.

## Reading (1)
- Anthropic, *Claude code system prompt* (community-extracted) — search "claude-code system prompt site:github.com"; or read this widely-shared distillation: https://github.com/anthropics/claude-code (their docs, look for "system prompt" or "tool descriptions" sections)
  Goal: see how a state-of-the-art coding agent describes its tools and constrains the model's behavior.

## Build tasks

### Part A — System prompt v2 (2 hours)
Today's prompt is probably 10 lines. SOTA agents have ~1500-token system prompts. Write yours in `agent/prompts/system.md`. Include:
- Identity and capability statement
- The exact format expected for finishing a task
- Anti-patterns: "Do not assume; verify by reading the file. Do not edit code you have not read. Do not invent test commands; discover them from the repo (Makefile, pyproject, package.json)."
- Tool-use discipline: "Prefer narrow `read_file` ranges; do not load whole files into context if you can search."
- Stopping condition: "When all tests pass, run them once more, report the result, and call finish."

Iterate empirically: re-run Day 18 task with prompt v2; compare metrics.

### Part B — Tool description tuning (1 hour)
Each tool's `description` field is what the model actually reads when deciding which tool to use. Today's are probably 1 line. Expand each to 3–5 sentences with:
- When to use this tool
- When NOT to use this tool (point at the better alternative)
- A concrete example call
- Common pitfall

Example for `run_shell`:
> Execute a shell command in the sandboxed workspace. Use this for: running tests, listing files, applying patches, installing dependencies. Do NOT use this for editing files (use `write_file`) or for inspecting file contents > 200 lines (use `read_file` with offset/limit). Network is denied. Working directory is the workspace root. Example: `{"cmd": "pytest -x tests/test_app.py"}`. Common pitfall: long-running processes will hit the 60s timeout — for servers, append `& sleep 1; ...` so the command returns.

Re-run Day 18; compare.

### Part C — Cost optimization (2 hours)
Inspect your Day 18 trajectories. Find the three biggest cost contributors. For each, fix:
- **Repeated full-file reads** → switch to ranged reads + caching at the tool level
- **System prompt sent every turn** → it already is by API design; just make sure it's not duplicated in `messages`
- **Reading test output 5 times** → tool layer should remember the last 2 outputs and detect repeated reads

Add `agent/tools/file_cache.py`: an LRU of file path → (mtime, content). On `read_file`, if mtime hasn't changed since last read, return cached. Saves both time and tokens.

### Part D — Re-bench
Re-run Day 18 matrix with v2 prompt + tuned descriptions + caching. Update the results table. **Target: 2× cost reduction or 1.5× pass-rate improvement, whichever comes first.**

## Acceptance criteria
- [ ] System prompt v2 in `agent/prompts/system.md`, ≥ 800 tokens
- [ ] All 4 tool descriptions rewritten
- [ ] File cache implemented and tested
- [ ] New benchmark numbers show measurable improvement; both old and new tables in `docs/notes/day19-iteration.md`

## Commit message
`agent: system prompt v2, expanded tool descriptions, file cache (X% cost cut)`

## If you finish early
Add a `--budget` flag to the agent: aborts when projected cost exceeds USD limit. Important for SWE-bench (200 tasks at $0.50 each is $100/run).

## If you fall behind
Skip cost optimization; just do prompt + tool descriptions. The biggest wins come from those two anyway.
