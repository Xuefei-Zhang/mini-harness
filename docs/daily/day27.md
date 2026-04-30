# Day 27 — Blog 4 (write + publish), the capstone

## Why this day matters
This is the post recruiters and engineering leads will read. It's the most quotable, the most concrete (real numbers), and it ties together the previous three. Two hours' extra polish here is worth more than two days of additional code.

## Reading (1)
- Skim 2 widely-shared SWE-bench-related blog posts for tone:
  - Cognition's *Devin* technical post (any version)
  - Anthropic's *Raising the bar on SWE-bench Verified*
  Steal: how they describe failure modes; how they cite numbers; how they end the post.

## Build tasks

### Part A — Outline (30 min)
`docs/blog/04-swebench-30-days.md`. Outline:
1. **Hook**: "30 days ago I had never written an agent. Today my home-grown harness scores X% on SWE-bench Lite. Here's the build log."
2. **The pitch in one diagram** — your final architecture (sandbox + tool server + agent loop + harness)
3. **Headline numbers** — the matrix table, prominent
4. **What surprised me** (3 short anecdotes from your daily logs)
   - The cgroup gotcha that took 4 hours
   - The system-prompt tweak that doubled pass-rate
   - The provider that cost 1/10th of Claude and got 60% of the way
5. **What I deliberately didn't build** (and why) — no LangChain, no RAG, no fine-tuning. Frames you as someone who makes scope decisions.
6. **What I'd do next with another 30 days** — Firecracker microVMs, RL data collection, agent-vs-agent eval. Shows direction.
7. **Hiring** — short paragraph at the end (not the start). "I'm interviewing in 2026 H1 for Agent Infra / Harness / Coding Agent roles. Repo: …  CV: …  Email: …"

Target 2500 words.

### Part B — Write (4 hours)
- Draft in English, structure-locked from outline
- Code blocks: ≥ 5 (one per component)
- Charts: ≥ 2 (matrix table; cost-per-pass bar chart)
- A 30-second screen recording at the top is worth a thousand words — embed via dev.to's video support or a YouTube embed
- Final paragraph re-read out loud — it must sound like you, not Claude

### Part C — Publish (1 hour)
- dev.to (English)
- 掘金 (Chinese)
- Personal site if you set one up
- Twitter/X thread (10 tweets max)
- LinkedIn post — different tone, more "I learned, I shipped, I'm available"
- Hacker News submission, Tuesday 8am PT (schedule)
- r/LocalLLaMA, r/MachineLearning, lobste.rs
- 即刻 (Chinese tech community)

### Part D — Update everything else
- README blog table → all 4 published
- LinkedIn headline → "Coding agent infra; SWE-bench harness from scratch (X%)"
- GitHub profile README → top-pin mini-harness, link the blog 4 URL

## Acceptance criteria
- [ ] Blog 4 published on ≥ 3 surfaces (dev.to + 掘金 + LinkedIn)
- [ ] HN submission scheduled or live
- [ ] LinkedIn headline updated
- [ ] Project README final blog row filled in

## Commit message
`day27: publish blog 4 — SWE-bench harness in 30 days`

## If you finish early
Record a 5-minute walkthrough of the codebase for your YouTube. This is the artifact you send when a recruiter asks "tell me about your project".

## If you fall behind
Cut Chinese version to a stub link-out from the English post. English on dev.to + LinkedIn + HN is the minimum viable product.
