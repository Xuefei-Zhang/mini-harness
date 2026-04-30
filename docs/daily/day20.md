# Day 20 — Blog 3 (write + publish)

## Why this day matters
You've shipped two infra-flavored blogs (opencode reading, sandbox internals). Blog 3 is the *application* blog — "I built a working coding agent and here's what surprised me". This is the one that lands well on Hacker News and Twitter, because it has numbers and a war-story tone.

## Reading (1)
- Re-read your Day 18 results table and Day 19 iteration notes. That's all the source material you need.

## Build tasks

### Part A — Outline (30 min)
`docs/blog/03-coding-agent-loop.md`. Outline:
1. **Hook**: a screenshot/asciinema of the agent fixing all 3 Flask bugs in 22 steps for $0.18
2. **What's NOT in this post**: no LangChain, no AutoGen, no vector DB. ~200 LOC of Python is the agent. Here's why that's enough.
3. **The provider abstraction** — show your `LLMProvider` interface, why Anthropic's tool-use shape is the canonical one, how OpenAI translates
4. **The loop in 30 lines** — show `Agent.run()` literally
5. **The non-obvious parts** that took most of the time:
   - Context management: 3 strategies, when each fails
   - Stuck detection: 4 heuristics, real examples from your trajectories
   - File cache: why it's a 30% cost cut for almost no code
6. **The 4-provider matrix** — your table, with commentary: which one wins on quality? on cost? on speed?
7. **What I'd do differently for SWE-bench (next post)**
8. **Code is open**

Target 2200 words.

### Part B — Write (3 hours)
Draft in English directly. Use Claude to tighten phrasing once the structure is locked.

Mandatory inclusions:
- ≥ 4 code blocks (interface, loop, one stuck heuristic, one tool description)
- ≥ 1 screenshot (trajectory viewer)
- The 4-provider results table
- Total cost number for writing the entire blog (run a token-counter on your trajectories)

### Part C — Publish (1 hour)
- dev.to (English)
- 掘金 (Chinese)
- Twitter/X thread (5 tweets, the screenshot + 1 takeaway each)
- Submit to Hacker News with title like "I wrote a coding agent in 200 lines (here's what's hard)" — submit Tuesday 8am PT for best traction; if today isn't Tuesday, schedule it

### Part D — README update
Blog 3 entry → published, URLs added.

## Acceptance criteria
- [ ] Blog 3 published in 2 places
- [ ] Twitter thread posted (or scheduled)
- [ ] HN submission live (or scheduled for Tuesday)
- [ ] README reflects W3 essentially complete

## Commit message
`day20: publish blog 3 — coding agent loop in 200 lines`

## If you finish early
Replay your best Day-18 trajectory into a YouTube short (asciinema → svg-term → mp4 via `gif-for-cli` or `ttygif`). Pin to repo.

## If you fall behind
Drop sections 5b (stuck detection) and 5c (file cache) — keep just context management. A shorter blog with a great hook still wins.
