# Day 07 — W1 retrospective + W2 sandbox interface design

## Why this day matters
Sunday is for sharpening the axe. You will lose more time in W2 to a bad sandbox interface than to any C++ syscall — design first, code second.

## Reading (1)
- MCP specification — https://modelcontextprotocol.io/specification/2025-06-18/basic
  Read only the **Lifecycle**, **Transports (stdio)**, and **Tools** sections. Total ~30 minutes. You will implement against this spec on Day 12.

## Build tasks

### Part A — W1 retrospective (1 hour)
Write `docs/notes/week1-retro.md`:
- 5 things that worked
- 3 things that wasted time
- What one habit would 2× next week's output?
- Update `docs/plan/PLAN.md` if anything in W2–W4 needs adjusting; commit the diff with a clear `plan: ...` message and a body explaining why.

### Part B — Sandbox design doc (4 hours)
`docs/design/sandbox.md`, ~1500 words. Required sections:

1. **Threat model** — what does the sandbox protect against?
   - Untrusted code from LLM execution (the main case)
   - Not: side-channel attacks, kernel zero-days, persistent malware
2. **Requirements**
   - Cold start ≤ 500ms (so a 50-step agent doesn't take 30s in overhead)
   - Memory limit, CPU limit, wall-clock limit
   - Filesystem: writable scratch dir, read-only system
   - Network: default deny, optional allowlist
   - Determinism: same input → same output (best effort)
3. **Survey of alternatives** (one paragraph each, with verdict)
   - Docker exec
   - Firecracker microVM
   - gVisor
   - nsjail / bubblewrap
   - WASM (wasmtime)
   - macOS sandbox-exec (for local dev)
4. **Decision: v0 = nsjail-style direct namespaces; v1 = Firecracker (deferred)**
   - Why: minimal deps, runs on Linux CI without Docker-in-Docker, teaches you the primitives directly
5. **Interface contract** — the C ABI between the C++ runner and the Python SDK:
   ```
   Input (stdin JSON):
     {
       "cmd": ["python", "-c", "print(1)"],
       "limits": {"memory_mb": 256, "cpu_seconds": 5, "wall_seconds": 10},
       "rootfs": "/path/to/overlay",
       "network": "deny"
     }
   Output (stdout JSON, single line):
     {
       "exit_code": 0,
       "stdout": "...",
       "stderr": "...",
       "duration_ms": 123,
       "killed_by": null  // or "memory" | "cpu" | "wall" | "signal"
     }
   ```
6. **Test plan** — 4 escape attempts the sandbox must defeat:
   - fork bomb
   - 10GB allocation
   - `curl https://example.com`
   - `cat /etc/shadow`

### Part C — Tooling check
- Confirm you have a Linux box for W2. mac M4 cannot run cgroups v2 / seccomp natively. Options (pick one and write into the design doc):
  1. UTM/Lima Ubuntu 24.04 VM on the M4 (free, slower)
  2. A cheap Linux server (Hetzner CAX21 ARM, ~€7/month)
  3. AWS/Aliyun Ubuntu 24.04 instance, on-demand for W2 only

## Acceptance criteria
- [ ] `week1-retro.md` committed
- [ ] `docs/design/sandbox.md` ≥ 1200 words, covers all 6 sections
- [ ] You have shell access to a Linux box, verified by running `cat /proc/self/cgroup` (must show cgroup v2 unified hierarchy: starts with `0::`)

## Commit message
`docs: week 1 retro + sandbox design v0`

## If you finish early
Bootstrap the C++ build: `sandbox/cpp/CMakeLists.txt` + an empty `main.cpp` that compiles. This buys you Day 9 morning.

## If you fall behind
Cut the survey of alternatives to bullet points. Threat model + interface contract are the parts that matter for W2.
