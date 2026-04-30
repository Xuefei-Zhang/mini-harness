# Day 22 — SWE-bench harness skeleton

## Why this day matters
Today you build the scaffolding to run one SWE-bench task end-to-end. Tomorrow you parallelize and tune. Friday you have publishable numbers.

## Reading (1)
- The official `run_evaluation.py` source — https://github.com/SWE-bench/SWE-bench/blob/main/swebench/harness/run_evaluation.py
  Read it once. You're not going to call it directly; you're going to **mimic the patch-application + test-run protocol** in your own runner. Pay attention to:
  - How they apply the model patch (`git apply` with retries)
  - How they run the test command (varies per repo; comes from the task's `test_directives`)
  - How they parse pass/fail (per-test, against `FAIL_TO_PASS` and `PASS_TO_PASS` lists in the task)

## Build tasks

### Part A — Task abstraction (1 hour)
`harness/datasets/task.py`:
```python
class SWEBenchTask(BaseModel):
    instance_id: str            # e.g. "django__django-13710"
    repo: str                   # "django/django"
    base_commit: str
    problem_statement: str      # the issue text — agent's main input
    hints_text: str | None
    test_patch: str             # patch that adds/modifies tests (do NOT show to agent)
    fail_to_pass: list[str]     # tests that must pass after fix
    pass_to_pass: list[str]     # tests that must continue to pass
    image_name: str             # prebuilt docker image
```

### Part B — Workspace setup per task (2 hours)
`harness/runner/workspace.py`:
```python
class Workspace:
    """Per-task ephemeral workspace, isolated from other tasks."""
    def __init__(self, task: SWEBenchTask):
        ...
    async def __aenter__(self): ...   # docker run -d, bind-mount a host dir, return path
    async def __aexit__(self, *exc): ...   # docker stop + rm, cleanup host dir
    async def apply_test_patch(self): ...  # git apply test_patch (so tests exist)
    async def run_tests(self, test_ids: list[str]) -> dict[str, Literal["PASS","FAIL","ERROR"]]: ...
    async def get_diff(self) -> str: ...   # git diff vs base_commit — this is the "model patch"
```

The workspace runs the **prebuilt SWE-bench image** as a long-lived container. Your Day-12 sandbox is *not* used here — SWE-bench needs the exact dep stack baked in their images, you can't rebuild that yourself.

(Note in `docs/notes/week4-decisions.md`: "SWE-bench evaluation uses the official prebuilt Docker images, not the home-grown C++ sandbox. The C++ sandbox is for the agent's `run_shell` tool when not running SWE-bench. Document this clearly in the README so reviewers understand the scope.")

### Part C — Single-task runner (2 hours)
`harness/runner/run_one.py`:
```bash
python -m harness.runner.run_one \
    --task django__django-13710 \
    --provider claude \
    --max-steps 50 \
    --output runs/swebench/
```
Sequence:
1. Open Workspace (start container, apply test patch — but `git stash` it before showing repo to agent, so the agent only sees the *original* code + the issue text)
2. Build agent with the workspace mounted; tools point inside
3. `await agent.run(task.problem_statement)`
4. After agent finishes: `git stash pop` (re-apply tests), `workspace.run_tests(fail_to_pass + pass_to_pass)`
5. Score: pass iff (all fail_to_pass now PASS) AND (all pass_to_pass still PASS)
6. Emit `runs/swebench/<instance_id>/result.json` with: pass/fail, per-test results, cost, steps, trajectory path, model_patch (the git diff)

### Part D — Smoke run
Pick the easiest of your 15 tasks. Run it with Claude. Whatever happens (pass, fail, crash) is fine — today is about plumbing, not score.

## Acceptance criteria
- [ ] One SWE-bench task runs end-to-end without exceptions
- [ ] `result.json` has the expected schema
- [ ] Agent never sees the test patch (verify by grepping its trajectory for the test code that's only in `test_patch`)
- [ ] Container is cleanly torn down (no leaked containers after a run; `docker ps -a` clean)

## Commit message
`harness: SWE-bench single-task runner with isolated docker workspaces`

## If you finish early
Add `--retry-on-error N` so transient docker failures don't waste a run.

## If you fall behind
Skip the agent integration today; just verify that you can apply patches and run tests programmatically. Wire the agent on Day 23.
