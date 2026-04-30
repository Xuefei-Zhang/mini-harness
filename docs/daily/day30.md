# Day 30 — First applications + outreach + ongoing cadence setup

## Why this day matters
Today the work product becomes job offers — or rather, *interviews*. Apply to too few and you starve; apply to too many badly and you burn out and burn referrers. The plan today is **5–8 high-quality applications, every one tailored**, plus the cadence that runs after Day 30.

## Reading (1)
- *How to write a cold email that gets replies* — Patrick McKenzie, https://kalzumeus.com/2017/09/09/how-to-do-tech-job-offer-negotiation/
  Read only the section on initial outreach (~10 min). The rest is for offer-stage; bookmark for later.

## Build tasks

### Part A — Final list of 8 (1 hour)
From your 10 JDs, narrow to 8 you actually want. For each, write to `docs/job-search/applications.md`:

| # | Company | Role | Path (referral / direct / recruiter) | Contact | Status | Notes |
|---|---|---|---|---|---|---|

**Path priorities** (highest first):
1. Warm referral via someone you've worked with
2. 1st-degree LinkedIn connection at the company
3. Cold-DM the engineering manager or a senior IC on the team
4. Cold-DM their recruiter
5. Direct application via the careers portal (lowest yield, do it last)

For each company, identify the *specific person* to reach — not "HR". Use LinkedIn + GitHub stars on similar repos to find the actual EM/IC.

### Part B — 8 personalized messages (3 hours)
Each message: 4–6 sentences max. Template:

> Hi [name],
>
> [Specific reference to their work — paper they coauthored, blog post, GitHub commit, talk]. The reason I'm writing: I just shipped [mini-harness 1-line], scoring X% on SWE-bench Lite. I think the [Sandbox / Harness / Coding Agent] role at [company] is the closest match I've seen.
>
> Repo: github.com/Xuefei-Zhang/mini-harness
> Build log (4 posts): [most-read blog URL]
> Background: 7 yrs system software at Intel (driver / firmware / runtime), now full-time on agent infra.
>
> Open to a 15-min chat next week, on your schedule.
>
> — Xuefei

Save a copy of each sent message to `docs/job-search/applications.md` under the company row. Track every reply.

### Part C — Send (1 hour)
- Send all 8 today
- Schedule for Tuesday/Wednesday morning local time at the recipient's TZ (highest open rate)
- Use Boomerang or similar to schedule if today isn't Tuesday

### Part D — Ongoing cadence (1 hour)
`docs/job-search/cadence.md` — what you'll do every week from Day 31 onward:

**Mon**: Review pipeline. Update `applications.md`. Apply to 5 new companies.
**Tue**: Send follow-ups for week-old un-replied messages (one polite bump, then move on).
**Wed**: Technical practice — 1 LeetCode-style problem (yes, you'll get asked) + 1 system design from your bank.
**Thu**: Read 1 paper or 1 blog from the agent space. Tweet/post the best insight.
**Fri**: 1 ship-something day on mini-harness — small features that keep the repo alive (e.g., add a new tool, support a new model). New commit each week signals the project is not dead.
**Sat**: Mock interview if any scheduled. Otherwise rest.
**Sun**: Weekly retro. Update PLAN if needed. Plan the week.

Budget: aim for 5 new applications + 5 follow-ups + 2 actual interviews per week. Goal: 3 offers to negotiate from.

### Part E — One last commit
A clean `git log` from Day 1 to Day 30 is itself a signal — recruiters do clone the repo and read the history. Make sure your final commit is:

```
day30: ship — 4 blogs published, résumé v1, 8 applications sent
```

Tag it: `git tag v0.1.0 && git push --tags`. This becomes a milestone you can link to.

## Acceptance criteria
- [ ] 8 personalized applications sent (with the message saved in `applications.md`)
- [ ] Pipeline tracker created and populated
- [ ] Weekly cadence written and the next 4 weeks calendared
- [ ] Repo tagged `v0.1.0`

## Commit message
`day30: ship — 4 blogs published, résumé v1, 8 applications sent`

## If you finish early
Apply to 3 more (12 total). The marginal cost is low once your assets are ready.

## If you fall behind
Send 4 today, 4 tomorrow. Do *not* dilute the personalization to hit 8.

---

## After Day 30

The plan ends here, but the project doesn't. Keep:
- The repo alive with weekly small commits
- The blog warm with one post every 2–3 weeks (e.g., "Adding Firecracker support to my agent sandbox", "What I learned interviewing at 8 LLM companies")
- The cadence above

When you sign an offer: write a final post-mortem blog. It will help the next person — and your future self when you're hiring.

Good luck. The work was the easy part; the showing-up-every-day part is what most people skip.
