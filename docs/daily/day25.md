# Day 25 — Multi-provider matrix run + comparative analysis

## Why this day matters
A single number ("28% on SWE-bench Lite with Claude") is a data point. A table of 4 providers with consistent setup is a story — and stories travel further on Twitter and recruiter mailboxes.

## Reading (1)
- Skip new reading — execution day.

## Build tasks

### Part A — Full matrix run (3 hours, mostly waiting)
```bash
python -m harness.runner.run_batch \
    --tasks harness/datasets/lite_15.json \
    --providers claude,deepseek,openai,qwen \
    --concurrency 4 \
    --max-steps 50 \
    --output runs/swebench/$(date +%Y%m%d)-matrix/
```
While running:
- Watch the cost meter every 15 min
- If projection > $200, kill the slowest-progressing provider (probably Qwen) and document why

### Part B — Aggregate analysis (2 hours)
`harness/analysis/aggregate.py` — script that ingests `runs/swebench/<run>/` and emits a markdown table:

| Provider | Model | Pass | Pass-rate | Total cost | $/passed | Median steps | Median wall time |
|---|---|---|---|---|---|---|---|
| anthropic | claude-sonnet-4-5 | 8/15 | 53% | $4.20 | $0.53 | 18 | 4m12s |
| deepseek | deepseek-chat | 5/15 | 33% | $0.60 | $0.12 | 24 | 5m08s |
| openai | gpt-4o | 6/15 | 40% | $3.10 | $0.52 | 21 | 4m45s |
| qwen | qwen-max | 4/15 | 27% | $1.80 | $0.45 | 28 | 6m20s |

Save to `docs/notes/day25-matrix.md`.

### Part C — Per-task heatmap (1 hour)
Same script outputs a per-task heatmap table:
|             | claude | deepseek | openai | qwen |
|---|---|---|---|---|
| django-13710 | ✅ | ✅ | ✅ | ❌ |
| sympy-21056  | ❌ | ❌ | ✅ | ❌ |
| ...

Insights to extract:
- How many tasks did *no* provider solve? (Probably impossible / harness bug.)
- How many did *all* solve? (Trivial — useful as smoke tests.)
- Where do providers diverge most? (Interesting failure modes.)

### Part D — Three findings for blog 4
Write three short paragraphs in `docs/notes/day25-findings.md`:
1. **Cost-efficiency winner** — likely DeepSeek; quote $/passed
2. **Reliability winner** — usually Claude; cite consistency across categories
3. **Surprise** — anything non-obvious from the heatmap

## Acceptance criteria
- [ ] Matrix run completed (or partially completed with documented reason if budget cut)
- [ ] Aggregate table committed
- [ ] Heatmap committed
- [ ] Three findings written

## Commit message
`harness: full 4-provider × 15-task matrix; aggregate + heatmap analysis`

## If you finish early
Run a 2nd Claude pass with `--max-steps 80` on the failing tasks only — does more thinking time help, or do failures repeat?

## If you fall behind
3 providers (drop Qwen). 10 tasks. Still produce table + heatmap.
