# Day 11 — Python SDK + escape-attempt test suite

## Why this day matters
The C++ binary is a power tool with sharp edges. The Python SDK is what your *agent loop* will use, and what reviewers will read first. Today you wrap it with a clean async Python API and write the test suite that proves the whole thing actually contains untrusted code.

## Reading (1)
- subprocess `asyncio.create_subprocess_exec` docs — https://docs.python.org/3.12/library/asyncio-subprocess.html
  Skim the API, then the "concurrent execution" example. That's all you need; you're not using fancy stream piping.

## Build tasks

### Part A — Python SDK (2 hours)
`sandbox/python/__init__.py`:
```python
class SandboxResult(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: int
    memory_peak_kb: int
    killed_by: Literal["", "memory", "cpu", "wall", "signal"]

class Sandbox:
    def __init__(self, runner_binary: Path = Path("./sandbox/cpp/build/mini-runc"),
                 default_rootfs: Path | None = None):
        ...

    async def run(
        self,
        cmd: list[str],
        *,
        rootfs: Path | None = None,
        memory_mb: int = 256,
        cpu_seconds: int = 5,
        wall_seconds: int = 10,
        network: Literal["deny", "allow"] = "deny",
        env: dict[str, str] | None = None,
        stdin_data: bytes | None = None,
    ) -> SandboxResult: ...
```
Implementation: build the JSON request, `await asyncio.create_subprocess_exec(self.runner_binary, ...)`, write JSON to stdin, read JSON from stdout, parse with pydantic.

Add `Sandbox.run_python(code: str, ...)` convenience wrapper.

### Part B — Escape-attempt test suite (3 hours)
`sandbox/tests/test_escape.py`. **Each test must run on CI** (so use a Linux runner). Mark as `@pytest.mark.skipif(not sys.platform.startswith("linux"))`.

Required tests — all must demonstrate **containment**, not host damage:

1. **`test_fork_bomb_contained`** — runs `:(){ :|:& };:`, asserts `killed_by` is `"wall"` or `"cpu"`, and host system load did not spike (check before/after `os.getloadavg()`)
2. **`test_oom_killed`** — Python that does `bytearray(2**30)`, memory_mb=128 → `killed_by="memory"`
3. **`test_wall_timeout`** — `sleep 100`, wall_seconds=2 → `killed_by="wall"`, duration ≤ 2500ms
4. **`test_no_network`** — Python `socket.create_connection(("1.1.1.1", 80))` → `exit_code != 0`, stderr mentions `Permission denied` or `EPERM`
5. **`test_no_host_filesystem`** — `cat /etc/shadow` → file not found (because rootfs doesn't have it)
6. **`test_no_escape_via_proc`** — `cat /proc/1/maps` works (it's the namespace's PID 1) but does *not* show host process memory; `ls /proc/host_pid` not visible
7. **`test_no_kernel_modules`** — `insmod` (or strace-equivalent) → blocked by seccomp
8. **`test_clean_exit_returns_value`** — sanity: `python -c "print('hello')"` → exit 0, stdout "hello\n"

### Part C — Cold-start benchmark
`sandbox/tests/bench_cold_start.py` — runs `/bin/true` 100 times, prints p50/p95 wall time. This number goes in blog 2.

## Acceptance criteria
- [ ] All 8 escape tests pass on the Linux box
- [ ] Cold-start p50 measured and recorded in `docs/notes/sandbox-perf.md`
- [ ] `from sandbox import Sandbox` works from anywhere in the project
- [ ] `pytest sandbox/tests/ -q` is green

## Commit message
`sandbox: Python SDK + escape-attempt test suite (8/8 passing)`

## If you finish early
Add `Sandbox.run_in_session(session_id, ...)` that reuses a long-lived sandbox process across calls — this is what your Day 17 trajectory recorder will need.

## If you fall behind
Drop tests 6–8. Tests 1–5 cover the dominant threat model and are all you need for blog 2.
