# mini-harness

> A from-scratch evaluation harness for coding agents — built in 30 days as a deep-dive into agent infrastructure.

[![status](https://img.shields.io/badge/status-bootstrapping-orange)]()
[![day](https://img.shields.io/badge/day-1%2F30-blue)]()
[![license](https://img.shields.io/badge/license-MIT-green)]()
[![python](https://img.shields.io/badge/python-3.12-blue)]()

## Why this exists

Most agent frameworks (LangChain, LangGraph, AutoGen) hide the interesting parts behind abstractions. This project rebuilds the core pieces from scratch with a system-engineering lens — every layer is small enough to read in one sitting.

| Layer | What | Why hand-rolled |
|---|---|---|
| **Sandbox** | C++ on cgroups v2 + seccomp + Linux namespaces | To prove I can build a real isolation primitive, not wrap Docker |
| **Tool server** | MCP protocol, no SDK | To understand the wire format, not just the client API |
| **Agent loop** | async Python, multi-provider (vLLM local + Anthropic / OpenAI / DeepSeek) | To own context-window, retry, and stuck-detection logic |
| **Eval pipeline** | SWE-bench Lite end-to-end | To produce a number, not a demo |

## Roadmap

```
W1  Agent basics + Python async + reading source code   [▓░░░░░░] Day 1/7
W2  Sandbox (C++) + MCP tool server                     [░░░░░░░]
W3  Agent loop + multi-provider + trajectories          [░░░░░░░]
W4  SWE-bench Lite + résumé + first applications        [░░░░░░░]
```

Full day-by-day plan: [`docs/plan/PLAN.md`](docs/plan/PLAN.md)
Daily logs: [`docs/notes/`](docs/notes/)

## Quick start

```bash
git clone <this-repo>
cd mini-harness
./scripts/setup.sh           # creates .venv, installs deps, copies .env.example -> .env
$EDITOR .env                 # add API keys for cloud providers (optional if using vLLM)

source .venv/bin/activate

# Local vLLM (default, zero cost) — requires vllm_fp8 start
python experiments/day01_react_from_scratch.py "What is 17 * 23 + 5?"

# Cloud providers (for API-specific feature work)
python experiments/day01_react_from_scratch.py --provider deepseek \
    "Read README.md and tell me how many components there are."
```

## Layout

```
mini-harness/
├── sandbox/        # C++ core + Python SDK    (W2)
├── tools/          # MCP tool server          (W2)
├── agent/          # multi-provider agent loop (W3)
├── harness/        # SWE-bench runner         (W4)
├── experiments/    # daily learning scripts   (W1-W4)
├── docs/
│   ├── plan/       # the 30-day plan
│   ├── design/     # component design docs
│   └── notes/      # daily logs
└── scripts/        # setup, helpers
```

## Blog series (companion writeups)

| # | Week | Title | Status |
|---|---|---|---|
| 1 | W1 | Reading opencode as a systems engineer | planned |
| 2 | W2 | Building an LLM agent sandbox in C++ — from cgroups to seccomp | planned |
| 3 | W3 | Hand-rolling a multi-provider coding agent loop | planned |
| 4 | W4 | From zero to a working SWE-bench Lite harness in 30 days | planned |

## Non-goals

- Not a production framework — pedagogical, opinionated, single-author
- No RAG, no vector DB, no fine-tuning — focus is **agent infra**, not retrieval or training
- No LangChain compatibility shim — the whole point is to understand the layers underneath

## License

MIT
