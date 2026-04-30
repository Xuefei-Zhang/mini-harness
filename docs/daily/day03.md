# Day 03 — Read opencode source code (part 1: tool & session)

## Why this day matters
You use opencode daily. Reading its source is the highest-ROI activity of W1: you learn (a) what production agent code looks like, (b) the exact abstractions interviewers will probe, (c) the vocabulary you'll repeat in your blog post. Today focus only on **tool dispatch** and **session state** — the two areas closest to your future Sandbox + Agent Loop work.

## Reading (1)
- opencode source on GitHub — clone locally:
  ```bash
  git clone https://github.com/sst/opencode ~/code/opencode
  cd ~/code/opencode
  ```
  Read **only** these paths today (skip everything else):
  - `packages/opencode/src/tool/` — every file
  - `packages/opencode/src/session/` — every file
  - `packages/opencode/src/permission/` — every file

  Don't try to understand the TUI or the SDK. Two hours of focused reading > eight hours of skimming.

## Build tasks
No code today. Produce three artifacts in `docs/notes/opencode/`:

1. **`tool-dispatch.md`** — answer in your own words:
   - How is a tool registered? What's the schema format?
   - What happens between "model emits a tool_call" and "tool function executes"? List every function call in order.
   - How are tool errors propagated back to the model?
   - Where is the timeout enforced?

2. **`session-state.md`** — answer:
   - What exactly is in a Session? Draw the data model (use Mermaid in markdown).
   - How is conversation history persisted? When? Where on disk?
   - How does context-window management work — token counting, trimming, summarization?
   - How are concurrent sessions isolated?

3. **`permission-model.md`** — answer:
   - When does opencode ask the user for permission?
   - Per-tool, per-session, or per-pattern granularity?
   - Where is permission state stored across runs?

Each file: 200–400 words + at least one Mermaid diagram. Cite line numbers like `tool/bash.ts:45`.

## Acceptance criteria
- [ ] 3 markdown files in `docs/notes/opencode/`, total ≥ 800 words
- [ ] Each file references at least 3 specific source locations (`path:line`)
- [ ] At least 2 Mermaid diagrams across the three files
- [ ] You can verbally explain tool dispatch end-to-end without looking at notes (test on yourself)

## Commit message
`docs: opencode source notes — tool dispatch, session, permission`

## If you finish early
Start `tui-vs-engine.md`: which parts of opencode are TUI concerns and which are reusable engine logic? This is what you'd port if you ever wrote a server-mode opencode.

## If you fall behind
Drop `permission-model.md`. Tool + session are non-negotiable.
