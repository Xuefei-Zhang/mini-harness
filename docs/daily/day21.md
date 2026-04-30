# Day 21 — W3 retro + W4 SWE-bench prep

## Why this day matters
Sunday axe-sharpening before the hardest week. SWE-bench is operationally fiddly; an hour of prep today saves four hours of yak-shaving Monday.

## Reading (1)
- SWE-bench official README — https://github.com/SWE-bench/SWE-bench
  Read **only**: the Quickstart, "Datasets on Hugging Face" section, and the Evaluation section. Stop before the "Train your own" section.

  Then `git clone https://github.com/SWE-bench/SWE-bench ~/code/swe-bench` for tomorrow.

## Build tasks

### Part A — W3 retro (1 hour)
`docs/notes/week3-retro.md`:
- Total LOC across `agent/`, `harness/` (run `tokei`)
- Total API spend W3
- Cost per task on Day 18 (final, after Day 19 optimizations) — this is the number you need for SWE-bench budget math
- 3 things you'd do differently if starting W3 over
- Update PLAN if W4 needs adjustment

### Part B — SWE-bench Lite scoping (2 hours)
SWE-bench Lite has 300 tasks. You will run a **subset of 10–20** to keep cost and time bounded. Pick them today.

`harness/datasets/swebench_lite.py`:
- Load the dataset from HuggingFace (`datasets.load_dataset("princeton-nlp/SWE-bench_Lite")`)
- Filter helpers: `by_repo()`, `by_difficulty()`, `sample(n, seed)`
- Pick 15 tasks weighted toward easier-looking ones (small `patch_size`, recent issues)
- Save the chosen task IDs to `harness/datasets/lite_15.json` so runs are reproducible

### Part C — Docker readiness (2 hours)
SWE-bench's evaluator builds **per-task Docker images** containing the exact dependencies of each repo at that commit. They publish prebuilt images for the Lite split — verify on your Linux box:
```bash
docker pull swebench/sweb.eval.x86_64.django_1776_django-13710:latest
docker run --rm swebench/sweb.eval.x86_64.django_1776_django-13710:latest /bin/sh -c "cd /testbed && python -m pytest --collect-only" | head
```
For each of your 15 chosen tasks, confirm the prebuilt image pulls and runs `--collect-only` cleanly. If any fails, swap that task for another. Save the verified list back to `lite_15.json`.

Disk: prebuilt images are ~2GB each → 30GB for 15 tasks. Make sure your Linux box has it.

### Part D — Cost/time projection
With your Day-19 numbers and 15 tasks, project:
- Wall time per task × 15 = total run time
- Cost per task × 15 × 4 providers = total cost for full matrix

If the projection is > $500 or > 6 hours of wall time, reduce N or providers now. Document in `docs/notes/week4-budget.md`.

## Acceptance criteria
- [ ] `lite_15.json` committed with 15 verified task IDs
- [ ] Each image pulls and `--collect-only` succeeds
- [ ] Cost projection ≤ $300 (fits the original ¥3000 monthly budget)
- [ ] Linux box has ≥ 50GB free disk

## Commit message
`harness: SWE-bench Lite dataset loader + verified 15-task subset`

## If you finish early
Read 2–3 of your chosen tasks (`problem_statement` field) end-to-end. Get a feel for what the agent will actually face.

## If you fall behind
Pick only 10 tasks and one provider (Claude Sonnet). Better to have real numbers Friday than projections.
