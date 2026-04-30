# Day 18 — End-to-end coding agent demo (mini Flask repo)

## Why this day matters
Today the project crosses the threshold from "infrastructure" to "an agent that does real work". You assemble sandbox + tools + agent loop + trajectory recording into a single command that fixes a real bug. This is the screenshot you'll put in your résumé and at the top of blog 3.

## Reading (1)
- No new reading. Spend the budget on debugging.

## Build tasks

### Part A — Build the test repo (1 hour)
`experiments/day18_targets/flask_buggy/`:
- A 5-file Flask app: `app.py`, `models.py`, `auth.py`, `tests/test_app.py`, `requirements.txt`
- Intentional bugs (commit each in its own commit, so you can diff later):
  1. **Off-by-one** in pagination logic (`models.py`)
  2. **Missing parameter validation** that crashes on empty input (`app.py`)
  3. **Wrong status code** returned (200 instead of 401 on auth failure, `auth.py`)
- A complete pytest suite in `tests/` that *currently fails* on these bugs

### Part B — End-to-end runner (3 hours)
`experiments/day18_run.py`:
```bash
python experiments/day18_run.py \
    --provider claude \
    --task "Fix all failing tests in experiments/day18_targets/flask_buggy" \
    --workspace ./tmp/work-$(date +%s) \
    --max-steps 30
```
The script:
1. Copies the buggy repo to a fresh workspace
2. Configures the agent with tools pointed at that workspace, all `run_shell` going through the sandbox
3. Runs the agent
4. After completion: runs `pytest` in the workspace, captures pass count
5. Prints summary: pass-rate, steps used, total cost, latency, trajectory path

### Part C — Run the matrix
Run with all 4 providers, save 4 trajectories. For each, record:

| Provider | Pass-rate | Steps | Total cost | Wall time | Notes |
|---|---|---|---|---|---|
| claude-sonnet-4-5 | ?/3 | ? | $? | ?s | |
| gpt-4o | ?/3 | ? | $? | ?s | |
| deepseek-chat | ?/3 | ? | $? | ?s | |
| qwen-max | ?/3 | ? | $? | ?s | |

Drop into `docs/notes/day18-results.md`. **This table goes in your README.**

### Part D — Watch a failure
Pick the worst-performing provider. Open its trajectory in the viewer. Identify the failure mode in plain English (got stuck searching? misread the test output? edited the wrong file?). Write a 100-word post-mortem in `docs/notes/day18-failure-analysis.md`.

## Acceptance criteria
- [ ] At least 1 provider achieves 3/3 fixes
- [ ] All 4 providers produce a trajectory (even if 0/3)
- [ ] Results table committed and added to README
- [ ] Failure analysis written

## Commit message
`day18: end-to-end coding agent demo on Flask test repo, 4-provider matrix`

## If you finish early
Add a 4th bug that requires *adding* a new file (not just editing). Tests which providers handle file creation cleanly.

## If you fall behind
Skip Qwen and OpenAI; run only Claude + DeepSeek. The 2-row table is still credible.
