# Day 29 — Mock interviews + system design rehearsal

## Why this day matters
The first 3 interviews of any cycle are the most expensive — you'll lose them mostly to nerves and to questions you've never said the answer to *out loud*. Today we burn that cost in a rehearsal so the real interviews count.

## Reading (1)
- *Designing Data-Intensive Applications* — Chapter 8 (The Trouble with Distributed Systems) excerpt, ~30 min skim. Distributed reasoning vocabulary will come up in any agent-orchestration system-design question.

## Build tasks

### Part A — Question bank (1 hour)
`docs/job-search/interview-prep.md` — list 20 questions you must be able to answer in 60–90 seconds each. Suggested set:

**Project depth (10 questions about mini-harness)**
1. Walk me through your sandbox architecture in 2 minutes.
2. Why cgroups v2 instead of v1?
3. How does your seccomp profile decide allow vs deny?
4. What happens when context window fills up mid-task?
5. How do you detect a stuck agent? What do you do about it?
6. Why MCP and not a custom JSON-RPC?
7. Describe your trajectory format. Why JSONL?
8. Walk through one failure case from your SWE-bench run. Why did it fail? How would you fix it?
9. Why didn't you use LangChain?
10. If you had another 30 days, what would you build next?

**Concept understanding (5)**
11. What's the difference between a workflow and an agent (per Anthropic's taxonomy)?
12. Compare ReAct vs Reflection vs Plan-and-Execute.
13. Explain tool-use protocol from the model's POV — what does it actually see in its prompt?
14. What's the role of system prompt vs tool description? Where would you put each piece of info?
15. Cost vs quality tradeoffs across the 4 providers you tested.

**System design (5) — practice on a whiteboard**
16. Design a multi-agent system that fixes 1000 GitHub issues per day. (Capacity, queueing, sandbox sharing, eval, retries.)
17. Design a tool sandbox that supports network for some workloads, denies for others, scales to 10k concurrent sandboxes.
18. Design an MCP-server fleet for an IDE plugin (auth, multi-tenancy, observability).
19. Design an offline eval pipeline (regression suite, human review, A/B prompt testing).
20. Design the trajectory storage system for a fleet running 100k tasks/day.

### Part B — Self-recording rehearsal (3 hours)
- Open your phone's voice memo
- Pick 5 random questions from the bank
- Answer each, on tape, *without* notes
- Listen back. For each, write 3 specific improvements (e.g. "I said 'um' 7 times in 90 seconds", "I forgot to mention the cost number")
- Re-record the worst 2

### Part C — Live mock (2 hours)
Find one human (best: someone in the industry; second best: any technical friend) and run a 1-hour mock:
- 30 min project deep-dive (questions 1–10)
- 25 min system design (one of 16–20)
- 5 min Q&A (you ask them — practice your "tell me about the team" questions)

Take notes on what they pushed back on. Add to `interview-prep.md` as "questions I fumbled".

### Part D — Build the asset pack you'll send before interviews
`docs/job-search/asset-pack.md`:
- 1-paragraph project pitch (the version you'd put in a recruiter cold-DM)
- Repo link
- Top blog post link
- 60-second loom-style video walkthrough (re-use Day 26 demo)
- Résumé PDF link

## Acceptance criteria
- [ ] 20 questions documented with at least 3-bullet answer outlines each
- [ ] You completed at least 1 live mock interview
- [ ] Recordings of yourself answering ≥ 5 questions exist
- [ ] Asset pack ready to paste into outreach DMs

## Commit message
`docs: interview prep — question bank, system design exercises, asset pack`

## If you finish early
Schedule 2 more mocks for next week.

## If you fall behind
Skip the live mock — but do the self-recording. Hearing your own answers is the biggest single ROI step.
