# Day 26 — Reproducibility, README rewrite, project polish

## Why this day matters
Tomorrow you publish blog 4. By the time anyone clones your repo, it must (a) build green from a fresh clone, (b) reproduce one SWE-bench task in one command, (c) tell its story in the first 30 seconds. Today is all about that.

## Reading (1)
- Read 3 well-presented agent repos for design inspiration:
  - https://github.com/princeton-nlp/SWE-agent (README structure)
  - https://github.com/sst/opencode (badges and demo gif)
  - https://github.com/Aider-AI/aider (prose tone)
  Spend ~30 min total. Steal layout, not text.

## Build tasks

### Part A — Reproducibility (3 hours)
- `make demo` — runs Day 18 Flask demo end-to-end (no SWE-bench needed). Should work on fresh clone in < 5 min.
- `make swebench-one` — runs ONE SWE-bench task end-to-end. Should work on a Linux box with docker, in < 10 min, < $0.20 cost.
- `make swebench-15` — runs the full 15-task matrix. Documented runtime + cost.
- `Makefile` is committed; each target prints what it'll do + estimated cost + asks `Continue? [y/N]` before incurring API spend.

Add `docs/REPRODUCING.md`: step-by-step, including the Linux/Docker requirement, how to get a Hetzner box if you don't have one, expected cost.

### Part B — README rewrite (2 hours)
Open today's README. Rewrite as if you are a recruiter who has 30 seconds:

Required structure (in this order):
1. **One-line tagline** — "A from-scratch coding agent harness scoring X% on SWE-bench Lite, built solo in 30 days."
2. **Headline number** — big, with how-to-reproduce link
3. **GIF or screenshot** — agent fixing a real bug, embedded
4. **Provider matrix table** — your Day 25 result
5. **What's inside** — 4 components with one-line descriptions, links into the codebase
6. **Quick start** — 5 commands max
7. **Blog series** — all 4 published, with URLs
8. **Author** — your name, GitHub, LinkedIn, "I'm looking for X roles"

The "Author" section is the call to action. It must say "I'm interviewing for Agent Infra / Harness / Coding Agent positions in 2026 H1. Reach me at <email>."

### Part C — Topics + social proof (1 hour)
- GitHub Topics on the repo: `llm-agent`, `swe-bench`, `mcp-server`, `sandbox`, `coding-agent`, `evaluation-harness`
- Pin the repo on your GitHub profile
- Set the repo's social-preview image (Settings → Social Preview) — a screenshot of the trajectory viewer with the headline number overlaid

## Acceptance criteria
- [ ] `make demo` works on the M4 (no Linux required for this one)
- [ ] `make swebench-one` works on the Linux box
- [ ] README rewritten following the recruiter-30s structure
- [ ] Repo topics + pinned + social preview set

## Commit message
`docs: README rewrite, Makefile demo targets, REPRODUCING guide`

## If you finish early
Set up GitHub Actions to run `make demo` (with mocked LLM provider) on every PR — proves the repo doesn't bit-rot.

## If you fall behind
Skip Actions. README rewrite + Makefile are the must-haves.
