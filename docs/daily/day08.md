# Day 08 — Sandbox build skeleton + cgroups v2 primer

## Why this day matters
You've designed it; today you set up the build system and learn just enough cgroups v2 to write code tomorrow. **Do not try to write the sandbox today.** Setup + reading.

## Reading (1)
- The kernel docs are the only authoritative source — https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
  Read sections **1 (Introduction)**, **2.1–2.3 (Mounting, Organizing Processes, [Un]populated Notification)**, and **5.2 (Memory) + 5.3 (CPU)** controllers. Skip the rest.

  Test your understanding by running on your Linux box:
  ```bash
  mount | grep cgroup2          # confirm unified hierarchy
  cat /sys/fs/cgroup/cgroup.controllers
  mkdir /sys/fs/cgroup/test     # need root
  echo $$ > /sys/fs/cgroup/test/cgroup.procs
  cat /sys/fs/cgroup/test/cgroup.procs
  rmdir /sys/fs/cgroup/test
  ```

## Build tasks

### Part A — C++ build skeleton (1 hour)
```
sandbox/cpp/
  CMakeLists.txt
  src/
    main.cpp           # CLI entry
    runner.hpp         # public interface
    runner.cpp         # stub
    cgroup.hpp         # cgroups v2 helper
    cgroup.cpp         # stub
    process.hpp        # clone3 + namespace helper
    process.cpp        # stub
    seccomp.hpp        # syscall filter
    seccomp.cpp        # stub (next day's work)
    json.hpp           # vendored single-header (nlohmann/json) or your own minimal parser
  tests/
    test_cgroup.cpp    # gtest, stub
    CMakeLists.txt
```

`CMakeLists.txt` minimum:
- C++20, `-Wall -Wextra -Werror`
- Builds two targets: `mini-runc` (the binary) and `mini-runc-tests` (gtest)
- Use FetchContent for googletest + nlohmann/json (no system deps)

`main.cpp` reads one line of JSON from stdin, parses, prints `{"exit_code": 0, "stdout": "stub", ...}` (matches the contract from `docs/design/sandbox.md`). That's it — proves the round-trip.

### Part B — cgroup helper, real (3 hours)
Implement `cgroup.cpp`:
```cpp
class Cgroup {
 public:
  // Creates /sys/fs/cgroup/mini-runc-<pid>/<random>
  Cgroup();
  ~Cgroup();  // rmdir on destruct, kill any survivors first

  void set_memory_max(uint64_t bytes);  // writes memory.max
  void set_cpu_max(uint32_t period_us, uint32_t quota_us);  // writes cpu.max
  void set_pids_max(uint32_t n);        // writes pids.max  (anti-fork-bomb)
  void add_process(pid_t pid);          // writes cgroup.procs
  void freeze();                         // writes cgroup.freeze = 1
  std::string memory_peak();            // reads memory.peak
 private:
  std::filesystem::path path_;
};
```
Write a test: create cgroup, set memory.max=64M, fork a child that does `malloc(128M); memset()`, confirm OOM kill, confirm `memory.peak` is non-zero, confirm cgroup directory is cleaned up after destruct.

### Part C — Build & run on Linux
```bash
cd sandbox/cpp && cmake -B build && cmake --build build -j
./build/mini-runc <<< '{"cmd":["echo","hi"]}'
sudo ./build/mini-runc-tests
```
Cgroup tests need root or user-delegation. Document which in `sandbox/cpp/README.md`.

## Acceptance criteria
- [ ] `mini-runc` binary builds with zero warnings
- [ ] `Cgroup` class real implementation; one passing test that observes OOM kill
- [ ] Stub binary reads JSON in, emits JSON out

## Commit message
`sandbox: build skeleton + Cgroup v2 helper with OOM kill test`

## If you finish early
Implement `set_io_max()` for disk I/O throttling (writes io.max to per-cgroup interface).

## If you fall behind
Skip pids.max + cpu.max. Memory + add_process is the minimum viable cgroup wrapper.
