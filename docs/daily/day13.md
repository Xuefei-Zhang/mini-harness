# Day 13 — Integration demo + blog 2 draft

## Why this day matters
You have all the pieces of W2 (sandbox + MCP server). Today you prove they compose into something that *does work* and start writing the blog that will get the most engineering-credibility traction of the four.

## Reading (1)
- Skim E2B's open-source code for *one* angle — sandbox templates: https://github.com/e2b-dev/E2B/tree/main/packages/python-sdk
  Just enough to write 2 paragraphs comparing your design choice (raw cgroups+seccomp) vs theirs (Firecracker-based). 30 minutes max.

## Build tasks

### Part A — Integration demo (3 hours)
`experiments/day13_demo.py`. A minimal scripted "agent" (no LLM yet — you're testing the sandbox + MCP plumbing):

1. Spin up the MCP server as a subprocess
2. Speak MCP over stdio (use the simple wire helpers from yesterday's smoke test)
3. Sequence:
   - `tools/call read_file {path: "demo/app.py"}` — empty stub on disk
   - `tools/call write_file {path: "demo/app.py", content: "<small Flask app code>"}`
   - `tools/call run_shell {cmd: "python demo/app.py & sleep 1; curl -s localhost:5000/health"}` — should print `{"ok":true}`
   - `tools/call run_shell {cmd: "pytest demo/test_app.py"}` — should pass

Record the full transcript to `runs/day13-demo.jsonl`. This file will be reused as a "hello world" example in your README.

### Part B — Blog 2 draft (4 hours)
`docs/blog/02-cpp-llm-sandbox.md`, target 2000 words finished, today aim for ~1200 of rough draft.

Outline:
1. **Hook**: One paragraph framing — "Every coding agent demo runs untrusted code. Almost none explain how. Here's how I built a 1500-line C++ sandbox in a week."
2. **Threat model** — 200 words from your design doc
3. **Architecture diagram** — reuse from `docs/design/sandbox.md`
4. **The four primitives** — one section each:
   - cgroups v2 (memory, CPU, pids)
   - namespaces + clone3
   - seccomp-bpf (with code snippet of your CodeRunner profile)
   - pivot_root + minimal rootfs
   For each: 200 words + a short code excerpt + "what bit me" anecdote
5. **Numbers** — cold-start p50/p95 from your benchmark, max throughput in runs/sec
6. **What I'd do differently in v1** — Firecracker for stronger isolation, virtiofs for shared FS
7. **Comparison table** — your sandbox vs E2B vs Modal sandbox vs naive Docker exec (LOC, cold start, isolation strength, network policy granularity)
8. **Code is open** — link to the repo, link to MCP server post that's coming next week

## Acceptance criteria
- [ ] `python experiments/day13_demo.py` runs end-to-end clean
- [ ] Transcript in `runs/day13-demo.jsonl` committed (small, ≤ 5KB)
- [ ] Blog 2 draft ≥ 1200 words, all 8 sections at least bullet points
- [ ] Comparison table actually filled with your measured numbers

## Commit message
`day13: end-to-end sandbox+MCP demo + blog 2 draft`

## If you finish early
Record an asciinema cast of the demo (`asciinema rec`) — embed in the blog post and the README. ~1 minute is plenty.

## If you fall behind
Cut sections 6 and 7 from the blog. Skip the asciinema. Demo + draft are the must-haves.
