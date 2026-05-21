# Agent Context — mini-harness

> **This file is for AI agents** (Claude/opencode/aider/Cursor/your-own-agent) picking up this project at any point.
> It tells you what this repo is, where we are, and how to work here.
>
> **Last updated**: 2026-05-21

---

## 1. What is this repo?

**`mini-harness`**: A from-scratch evaluation harness for coding agents — built in 30 days (May 21 – Jun 19, 2026) as a job-search sprint targeting **DeepSeek Agent Harness Engineer**.

### Core philosophy
- **No frameworks**. No LangChain, no LangGraph, no AutoGen. Every layer is hand-written.
- **Systems-first**: C++ sandbox (cgroups + seccomp + namespaces), not Docker.
- **Research infra language**: We measure the *impact of harness mechanisms on agent behavior*, not "I implemented memory".

### Target roles
- **Primary**: DeepSeek Agent Harness Engineer
- **Secondary**: Moonshot/智谱/MiniMax + 字节/阿里/腾讯 AI Lab

### What you'll build (~5000-8000 LOC)
| Layer | Tech | Done? |
|---|---|---|
| Sandbox Runtime | C++ (cgroups v2 + seccomp + namespaces) + Python SDK | No |
| Tool Server | Python, MCP protocol (from spec, no SDK) | No |
| Agent Loop | Python async, 4 providers (Anthropic/OpenAI/DeepSeek/Qwen) | No |
| Memory System | Structured working state + sliding window + lightweight long-term | No |
| Context Manager | 3 trim strategies + prompt cache + token budget | No |
| Skills Framework | Pluggable skills, auto-discovery | No |
| Failure Analysis | 8-class failure taxonomy + trajectory replay | No |
| Subagent / Multi-Agent | Spawner (sequential/parallel) + planner/executor/reviewer triad | No |
| Eval Pipeline | SWE-bench Lite + 8 agent metrics | No |
| Trajectory | JSONL + OpenTelemetry-style tracing + Streamlit viewer | No |

### Hidden north-star
Every module serves one goal: **let the harness drive a model through a long-horizon task** (30-80 steps, multi-file, real project). Day 26 is the final validation — attempt a PR to vLLM or FastAPI.

---

## 2. Where are we? (Day 1 of 30, as of 2026-05-21)

### Completed
- [x] Day 1: `experiments/day01_react_from_scratch.py` — 260 LOC, 3 tools, 3 providers, ReAct from scratch
- [x] PLAN.md v3.0 — full 30-day plan with JD alignment
- [x] 30 daily briefs updated to v3.0
- [x] `docs/learning_map.md` — languages, tools, papers, source code, deny list
- [x] `docs/interview_prep.md` — 76 interview questions across 13 categories

### Next tasks (in order of priority, but any order OK)
1. **Day 1 review**: Re-reading Day 1 code, running 5-task experiment, writing `docs/notes/day01_review.md`
2. **Day 2**: Rewrite day01 as async with pydantic + httpx + structlog
3. **Day 3**: Prompt Engineering A/B/C test (3 system prompts × 5+ tasks)
4. **§零 of learning_map**: Linux containerization basics (namespaces, cgroups, seccomp) — finish before Day 8

### Environment
- **Local LLM**: vLLM Qwen3.6-27B-FP8 on `localhost:9070` (systemd service `vllm-fp8`). Manage with `vllm_fp8 {start|stop|status|report}`
- **Paper summaries**: `docs/notes/paper_summaries.md` — Chinese summaries of all referenced papers. Read this before diving into original papers.
- **API keys**: `.env` (not tracked). Copy from `.env.example` for cloud provider experiments.

---

## 3. How to work here

### Rules (from AGENTS.md)
- **All work is git-tracked**. No scratch files. Commit after each meaningful unit.
- **Push to `origin main`** at end of each working session.
- **Never commit secrets**. `.env` is gitignored.
- **No LangChain/LangGraph/LlamaIndex/vector DBs**.
- **No silent dependencies**. Every new package needs one-line justification in commit body.
- **No unprompted LLM calls** — they cost money. Show the user first.

### Commit message style
```
<scope>: <imperative summary, lowercase, <=72 chars>
```
Scopes: `init`, `chore`, `docs`, `plan`, `dayNN`, `sandbox`, `tools`, `agent`, `harness`, `experiments`

### Code conventions
- Python: 3.12, async-first, pydantic v2, structlog
- C++ (sandbox): C++20, no exceptions across C ABI
- Lint: `ruff check .` before commits touching Python
- Tests: `*/tests/`, run with `pytest -q`

### Project layout
```
mini-harness/
├── sandbox/           ← C++ sandbox runtime (not yet created)
├── tools/             ← MCP tool server (not yet created)
├── agent/             ← Agent loop + memory + context + skills + subagent (not yet created)
├── harness/           ← Eval pipeline + failure analysis + trajectory (not yet created)
├── experiments/       ← Day-by-day experiment scripts (day01 exists)
├── docs/              ← Plan, daily briefs, notes, design docs
│   ├── plan/PLAN.md       ← 30-day plan v3.0 (SINGLE SOURCE OF TRUTH)
│   ├── daily/             ← 30 daily briefs (day01-day30)
│   ├── notes/             ← Daily logs (day01 exists)
│   ├── design/            ← Architecture diagrams (empty, coming)
│   ├── blog/              ← Blog drafts (empty, coming)
│   ├── AGENT_CONTEXT.md   ← This file
│   ├── learning_map.md    ← Languages, tools, papers, references
│   └── interview_prep.md  ← 76 interview questions + daily practice plan
└── scripts/           ← setup.sh (exists)
```

### Daily workflow
1. User picks a Day N (any order OK)
2. Read `docs/daily/dayNN.md` for today's tasks
3. Build → test → commit
4. Log to `docs/notes/dayNN.md` (≤30 lines: what was done, pitfalls, tomorrow's top 3, LOC/commit count)
5. Push to `origin main`
6. User tells me what's done → I update task status

---

## 4. Plan overview (30 days, 4 weeks)

| Week | Theme | Key deliverables |
|---|---|---|
| W1 (Day 1-7) | Agent basics + Prompt/Reasoning + source reading | Blog 1; Prompt A/B; CoT/Reflexion; 3 architecture diagrams |
| W2 (Day 8-14) | Sandbox (C++) + MCP + Agent Loop | sandbox v0 + MCP + agent loop; Blog 2 |
| W3 (Day 15-21) | Skills + Memory + Context + Failure Analysis | Working state + context manager + failure taxonomy; Blog 3+4 |
| W4 (Day 22-30) | SWE-bench + metrics + model co-evolution + resume | Eval numbers + agent metrics + Blog 5 + resume + applications |

**Priority system**: P0 = must ship (agent loop, sandbox, tool server, context, eval, trajectory); P1 = should have (memory, skills, reasoning, failure analysis); P2 = lightweight demo (multi-agent, ToT, KV cache)

---

## 5. Key decisions (why we do things this way)

| Decision | Why |
|---|---|
| No LangChain/LangGraph | Top companies don't use them; hand-written proves depth |
| C++ sandbox (not Docker) | Differentiator — most agent candidates don't know seccomp/cgroups |
| Structured working state > embedding memory | DeepSeek cares about "what is the agent doing now", not "what did it chat about" |
| Failure analysis > multi-agent debate | Real harness teams need failure taxonomy, not 5-agent roleplay |
| ToT/Multi-Agent = lightweight demo | Industry uses ReAct + Reflexion + retry, not debate simulations |
| Blog language = "research infra" | "我在研究 context compression 对 tool selection accuracy 的影响" beats "我实现了 context manager" |
| Tasks can be done in any order | Quality + learning notes = counts as complete. Weekly review adjusts plan. |

---

## 6. API budget

- **W1-W3**: ¥30-80/day for prompt/reasoning experiments
- **W4**: ¥200-500 per SWE-bench run
- **Total monthly cap**: ¥3000-5000
- **No GPU purchase** — all LLM work via API

---

## 7. Dependencies (current)

```toml
# Runtime
anthropic, openai, httpx, pydantic v2, python-dotenv, structlog, rich, typer
# Dev
pytest, pytest-asyncio, ruff, mypy
# Optional (later)
streamlit (trajectory viewer)
```

---

## 8. How to pick up work

When you (the agent) start a new session with the user:

1. Read `docs/plan/PLAN.md` → check the status table (§10) for current progress
2. Read `docs/daily/dayNN.md` → the next Day N the user wants to work on
3. Read `docs/notes/` → any existing logs from previous sessions
4. Follow the daily brief: build tasks → acceptance criteria → commit
5. Ask the user if they want to work on a specific Day or if you should pick the next one

---

## 9. Interview prep

- `docs/interview_prep.md`: 76 questions across 13 categories, P0/P1/P2 graded
- Daily practice: 1-2 questions per day, aligned with that day's build tasks
- Day 29: mock interview (random 3-5 questions per category)
- "Research infra language" table in PLAN.md §12 — use this framing in answers

---

## 10. Files that matter most

| File | Why |
|---|---|
| `docs/plan/PLAN.md` | **SINGLE SOURCE OF TRUTH** — 30-day plan, JD mapping, status table |
| `docs/daily/dayNN.md` | Today's tasks — build tasks, acceptance criteria, commit message |
| `docs/notes/dayNN.md` | What was actually done — the proof of completion |
| `docs/AGENT_CONTEXT.md` | This file — helps any agent understand the project |
| `AGENTS.md` | Working agreements — git rules, code conventions, deny list |
| `docs/learning_map.md` | What to learn, what to skip, when |
| `docs/interview_prep.md` | 76 interview questions + answers being built over time |
