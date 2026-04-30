# mini-harness

> A minimal, self-built evaluation harness for coding agents.
> Built in one month as a deep-dive into agent infrastructure: sandbox, tool runtime, agent loop, and SWE-bench evaluation.

## Why

Most agent frameworks (LangChain, LangGraph, AutoGen) hide the interesting parts behind abstractions. This project rebuilds the core pieces from scratch, with a system-engineering perspective:

- **Sandbox** — written in C++ on top of cgroups v2 + seccomp + Linux namespaces, not Docker-in-Docker
- **Tool server** — speaks the MCP protocol directly, no SDK
- **Agent loop** — async Python, supports Anthropic / OpenAI / DeepSeek / Qwen with no framework
- **Eval pipeline** — runs against SWE-bench Lite end-to-end

## Components

```
mini-harness/
  sandbox/        # C++ core + Python SDK: process isolation, syscall filtering
  tools/          # MCP tool server: read_file, write_file, run_shell, search_code
  agent/          # Multi-provider agent loop with trajectory recording
  harness/        # SWE-bench Lite runner and scorer
  experiments/    # Daily learning scripts (W1-W4)
  docs/
    plan/         # 30-day plan
    design/       # Component design docs
    notes/        # Daily logs
```

## Status

Day 1 / 30 — bootstrapping. See [docs/plan/PLAN.md](docs/plan/PLAN.md) for the full plan.

## Blog series

1. (W1) Reading opencode as a systems engineer
2. (W2) Building an LLM agent sandbox in C++ — from cgroups to seccomp
3. (W3) Hand-rolling a multi-provider coding agent loop
4. (W4) From zero to a working SWE-bench Lite harness in 30 days

## License

MIT
