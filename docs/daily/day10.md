# Day 10 — seccomp-bpf syscall filter + timeout/OOM handling

## Why this day matters
Namespaces stop a process from *seeing* the host. seccomp stops it from *asking the kernel* to do dangerous things. Together they cover ~95% of the realistic threat model. By end of today your sandbox can survive `:(){ :|:& };:` and 128 lines of malicious python.

## Reading (1)
- libseccomp documentation page — https://man7.org/linux/man-pages/man3/seccomp_init.3.html
  Read the man page once. Then look at one real-world filter for inspiration: nsjail's [config.proto](https://github.com/google/nsjail/blob/master/config.proto) syscall section (just skim what they allow/deny).

## Build tasks

### Part A — seccomp filter (3 hours)
Add libseccomp dep to CMake (`apt install libseccomp-dev` on the Linux box).

Implement `seccomp.cpp`:
```cpp
class SeccompFilter {
 public:
  enum class Profile { Strict, CodeRunner };
  explicit SeccompFilter(Profile);
  void apply();   // SECCOMP_FILTER_FLAG_TSYNC, applied just before execvp
};
```
- **Strict**: deny everything except a tiny allowlist (read/write/exit/exit_group/brk/mmap/mprotect/rt_sigaction/...). About 30 syscalls.
- **CodeRunner**: allow what a typical Python/Node interpreter needs. Start from strict and add: `clone`, `clone3`, `execve`, `openat`, `getdents64`, `fstat`, `lseek`, `pipe2`, `dup`, `dup2`, `wait4`, `prctl`, `getuid`, `getgid`, `getrandom`, `socket(AF_UNIX only)`...

  Critically **deny**: `socket(AF_INET/AF_INET6)`, `bpf`, `ptrace`, `kexec_load`, `mount`, `pivot_root`, `chroot`, `unshare`, `setns`, `keyctl`, `add_key`, `request_key`, `init_module`, `delete_module`, `reboot`, `swapon`, `swapoff`.

  Use `SCMP_ACT_ERRNO(EPERM)` for denied — better than KILL for debugging.

Wire into `process.cpp`: child calls `SeccompFilter(CodeRunner).apply()` immediately before `execvp`.

### Part B — Timeout + OOM machinery (2 hours)
In `runner.cpp`:
```cpp
struct Limits {
  uint64_t memory_mb;
  uint32_t cpu_seconds;
  uint32_t wall_seconds;
};

struct ExecResult {
  int exit_code;
  std::string stdout_data;
  std::string stderr_data;
  uint64_t duration_ms;
  uint64_t memory_peak_kb;
  std::string killed_by;  // "" | "memory" | "cpu" | "wall" | "signal"
};

ExecResult run(const SpawnConfig&, const Limits&);
```
- Wall timeout: parent sets `setitimer(ITIMER_REAL, ...)`, on alarm sends SIGKILL to whole cgroup via `cgroup.kill` (cgroup v2 feature).
- CPU timeout: `cgroup.set_cpu_max(period, quota)` (already done) + child does `setrlimit(RLIMIT_CPU, ...)` belt-and-braces.
- OOM: cgroup v2 emits a notification on `memory.events`; parent polls and reports `killed_by="memory"`.
- Always read `memory.peak` before destructing the cgroup.

### Part C — Update CLI contract
`main.cpp` now consumes the full JSON contract from `docs/design/sandbox.md`. Output JSON includes `killed_by` and `memory_peak_kb`.

## Acceptance criteria
- [ ] `mini-runc <<< '{"cmd":["python3","-c","import socket; socket.socket(socket.AF_INET).connect((\"1.1.1.1\",80))"]}'` exits non-zero with EPERM
- [ ] Fork bomb (`bash -c ":(){ :|:& };:"`) is contained — process count never exceeds pids.max, parent kills cleanly within wall_seconds
- [ ] 1GB malloc with memory_mb=128 → exit_code from SIGKILL, killed_by="memory"
- [ ] `sleep 100` with wall_seconds=2 → killed_by="wall", duration_ms ~2000

## Commit message
`sandbox: seccomp CodeRunner profile + cgroup-based timeout/OOM handling`

## If you finish early
Add a small benchmark: cold-start time of an empty `/bin/true` in the sandbox. Target ≤ 50ms on bare metal, ≤ 200ms in a VM. Save number to `docs/notes/sandbox-perf.md` — you'll cite it in blog 2.

## If you fall behind
Skip the Strict profile. CodeRunner alone is enough for the agent use case.
