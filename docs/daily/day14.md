# Day 14 — Publish blog 2, polish, W2 retro

## Why this day matters
End-of-week: harvest the work into something the world (and recruiters) can see. This blog has the strongest signal-to-recruiter ratio of all four because the topic intersection (LLM agents × Linux internals × C++) is rare.

## Reading (1)
- No new reading. Use the time for a careful re-read of your own draft from Day 13. Distance helps you see it as a stranger.

## Build tasks

### Part A — Polish & publish blog 2 (4 hours)
- Take draft to ~2000 words, tighten every paragraph
- Have Claude proofread for English; you write the *first draft* in English (don't translate from Chinese — the structure changes)
- **Inline at least 3 code excerpts** with syntax highlighting (cgroup write, clone3 flags, seccomp rule)
- **Inline 1 architecture diagram + 1 cold-start latency chart** (matplotlib → png is fine)
- Publish to dev.to (English) **and** 掘金 (Chinese version, you can translate this one)
- Cross-post English to: r/cpp, r/LocalLLaMA, lobste.rs (link only), and Twitter/X if you have an account

### Part B — README polish (1 hour)
- Update roadmap progress bar to W2 done
- Add a "Sandbox" section with the architecture image, cold-start number, and a 4-line code example
- Update blog table with both URLs

### Part C — W2 retrospective (1 hour)
`docs/notes/week2-retro.md`:
- Total LOC produced (run `tokei sandbox/ tools/`)
- API spend so far (check provider dashboards)
- Where you went over time, where you went under
- Three open bugs / known issues to revisit later
- Update `docs/plan/PLAN.md` if W3 estimates need adjustment

### Part D — Sanity check the W3 entry point
Open `docs/daily/day15.md`. Make sure you have:
- 4 working API keys
- LLM API budget for ~100 calls/day
- The sandbox SDK importable from anywhere in the project

If anything's missing, fix it today, not Monday morning.

## Acceptance criteria
- [ ] Blog 2 published on dev.to AND 掘金
- [ ] README reflects W2 completion and links blog 2
- [ ] `week2-retro.md` committed
- [ ] At least 1 cross-post done

## Commit message
`day14: publish blog 2, README W2 polish, week2 retro`

## If you finish early
Add a `make demo` target that runs `experiments/day13_demo.py` so anyone cloning can see it work in one command.

## If you fall behind
Publish English-only, skip 掘金. Still polish README — recruiters will look there before any blog.
