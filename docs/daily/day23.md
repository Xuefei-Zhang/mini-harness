# Day 23 — Batch runner + parallelism + first full pass

## Why this day matters
Sequential runs of 15 tasks at ~5 minutes each = 75 minutes per provider. Sequential × 4 providers = 5 hours of staring at a terminal. A simple parallel runner cuts this to 30 minutes wall time and gives you a feedback loop short enough to iterate on prompts.

## Reading (1)
- Skip new reading. Today is execution-heavy.

## Build tasks

### Part A — Batch runner (3 hours)
`harness/runner/run_batch.py`:
```bash
python -m harness.runner.run_batch \
    --tasks harness/datasets/lite_15.json \
    --providers claude,deepseek \
    --concurrency 4 \
    --max-steps 50 \
    --output runs/swebench/batch-$(date +%s)/
```
Implementation:
- `asyncio.Semaphore(concurrency)` to cap parallel docker containers
- Each (task, provider) pair → one `run_one` invocation
- Real-time progress: rich `Progress` bar showing "task: pass/fail/running"
- After all tasks: write `summary.json` with overall pass-rate per provider
- Resilient: a single task crash should not fail the batch. Capture the exception and mark that task as `crashed` in summary.

### Part B — Cost guardrail (30 min)
Add `--budget-usd 50` flag. Track cumulative cost across all in-flight runs; abort new starts (let in-flight finish) when crossing 80% of budget. Print a clear message: "Budget guardrail: X/Y USD spent, no new tasks will start."

### Part C — First real run (3 hours)
Run the batch:
```bash
python -m harness.runner.run_batch \
    --tasks harness/datasets/lite_15.json \
    --providers claude \
    --concurrency 3 \
    --output runs/swebench/$(date +%Y%m%d)-claude-baseline/
```

While it runs, watch one trajectory live in the viewer. Take notes on failures.

After completion:
- Print summary: `X/15 passed (Y%)` — this is your **baseline number for blog 4**
- Total cost
- Median steps used
- Most common failure category (gut estimate from skimming a few trajectories)

Save a copy of `summary.json` and the per-task `result.json`s to `docs/notes/day23-baseline.md` (linked, not pasted).

## Acceptance criteria
- [ ] Batch runner completes 15 tasks for at least 1 provider without manual intervention
- [ ] Budget guardrail tested (run with `--budget-usd 1` to confirm it triggers)
- [ ] Baseline pass-rate recorded (any number is OK today; we're optimizing tomorrow)
- [ ] Total wall time ≤ 90 minutes for 15 tasks at concurrency 3 (otherwise raise concurrency Day 24)

## Commit message
`harness: parallel batch runner with cost guardrail; first 15-task baseline`

## If you finish early
Run a second provider (DeepSeek) in parallel with Claude. Save another summary.

## If you fall behind
Reduce to 10 tasks. A 10-task baseline is better than no baseline.
