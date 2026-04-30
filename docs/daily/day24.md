# Day 24 — Failure analysis + targeted fixes

## Why this day matters
The gap between 30% pass-rate and 50% pass-rate is almost always 5 specific bugs in your harness or prompt — not a smarter model. Today you find them.

## Reading (1)
- Anthropic's *Raising the bar on SWE-bench Verified* — search "Anthropic SWE-bench engineering" on the Anthropic blog
  This documents what *they* learned tuning a coding agent against SWE-bench. Steal liberally.

## Build tasks

### Part A — Categorize failures (2 hours)
Open the trajectory of every failed task from yesterday's run. For each, write one line in `docs/notes/day24-failures.md`:
```
django__django-13710 | FAIL | reason: agent never read tests/, edited models.py guessing the schema
sympy__sympy-21056   | FAIL | reason: agent fixed the right file but added a print() that broke an unrelated test
flask__flask-2929    | CRASH| reason: docker container OOM during pytest, our memory limit too low
...
```
Group into categories: **prompt issue**, **tool issue**, **harness issue**, **model limitation**, **docker/infra issue**.

### Part B — Pick the top 3 categories. Fix them. (4 hours)

Likely candidates (you'll see your own list):

1. **"Agent doesn't run tests before declaring done"** → tighten system prompt: "Before calling finish, you MUST have run the failing tests and observed them passing. Reference the exact output."
2. **"Agent edits files it hasn't read"** → tool-layer guardrail: `write_file` rejects writes to files not in a per-session "read set". Returns: `"Refusing: read this file first to understand current contents."`
3. **"Agent gets stuck searching"** → add a `find_file` tool (just `find . -name PATTERN`) so it doesn't reinvent search via shell every time.
4. **"Long stack traces eat context"** → tool-layer truncation: stderr > 4000 chars gets a head/tail summary with `... (N lines elided) ...`.
5. **"Tests timeout"** → bump test container memory to 4GB, wall to 5 min.

Each fix in its own commit so you can revert if one regresses.

### Part C — Re-run (2 hours)
Same 15 tasks, same provider. Compare new pass-rate.

Update `docs/notes/day24-iteration.md`:
| Run | Pass | Cost | Median steps | Notes |
|---|---|---|---|---|
| baseline (Day 23) | x/15 | $? | ? | |
| iteration 1 (Day 24) | y/15 | $? | ? | added X, Y, Z |

Aim for absolute +2 tasks (e.g., 4/15 → 6/15) — realistic single-iteration delta.

## Acceptance criteria
- [ ] Failure categorization committed
- [ ] At least 3 targeted fixes shipped, each in its own commit
- [ ] Re-run completed; iteration table updated
- [ ] Pass-rate did not *regress* (most important — fixes should not break working tasks)

## Commit message format (one per fix)
- `agent: require test run before finish (system prompt)`
- `tools: write_file requires prior read (read-set guard)`
- `tools: add find_file (faster than shell find for the model)`
- `harness: truncate stderr > 4KB head/tail`

## If you finish early
Run a second provider on the iterated harness — does the fix help DeepSeek too, or only Claude?

## If you fall behind
Pick only the top 2 categories. Re-run is non-negotiable; without a re-run number, the fixes don't count.
