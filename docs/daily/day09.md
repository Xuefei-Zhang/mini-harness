# Day 09 — Linux namespaces + clone3 + minimal containerization

## Why this day matters
A container is just `clone3()` + namespaces + cgroups + a pivot_root. Today you stop using "container" as a magic word and write the 200 lines that *are* a container. This is the chapter of W2 you'll talk about most in interviews.

## Reading (1)
- `man 7 namespaces` — yes, the man page. https://man7.org/linux/man-pages/man7/namespaces.7.html
  Read the table of namespace types, then the **CLONE_NEW\*** flag descriptions. You need to know what each namespace isolates by name (mount, PID, network, IPC, UTS, user, cgroup, time).

  After: `man 2 clone3` (10 minutes, you only need the `clone_args` struct and the `flags` field).

## Build tasks

Implement `process.cpp`:

```cpp
struct SpawnConfig {
  std::vector<std::string> argv;
  std::filesystem::path rootfs;     // becomes new /  (via pivot_root)
  std::filesystem::path workdir;    // chdir after pivot_root
  std::vector<std::string> env;
  bool deny_network = true;
};

struct SpawnResult {
  pid_t pid;
  int   stdout_fd;  // pipe read end
  int   stderr_fd;
};

SpawnResult spawn_isolated(const SpawnConfig&);
```

Implementation must:
1. Use `clone3()` (not legacy `clone`) with these flags:
   `CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWNET | CLONE_NEWIPC | CLONE_NEWUTS | CLONE_NEWUSER | CLONE_NEWCGROUP`
2. In the child:
   - Set up uid/gid mappings (you'll be a "fake root" inside)
   - `mount("none", "/", NULL, MS_REC | MS_PRIVATE, NULL)` — stop mount events leaking out
   - Bind-mount rootfs over a temp dir, then `pivot_root` and `umount2(old_root, MNT_DETACH)`
   - Mount `/proc` fresh (PID namespace requires this)
   - `chdir(workdir)`
   - `execvp(argv[0], argv)` — at this point the child is in a hermetic world

3. In the parent: dup2 pipes for stdout/stderr capture, return immediately.

Wire it into `main.cpp`:
```bash
./build/mini-runc <<< '{
  "cmd": ["/bin/ls", "/"],
  "rootfs": "/tmp/alpine-rootfs"
}'
# expected: bin etc lib proc usr ...  (only the rootfs files, not your real /)
```

You'll need a small rootfs. Cheapest: untar Alpine minirootfs:
```bash
mkdir -p /tmp/alpine-rootfs && cd /tmp/alpine-rootfs
curl -sSL https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/alpine-minirootfs-3.20.0-x86_64.tar.gz | tar -xz
```
(Use the right arch for your VM.)

### Tests
Add `tests/test_process.cpp`:
- Spawn `/bin/sleep 1`; assert PID is 1 *inside* the namespace (read `/proc/self/status` from a wrapper script)
- Spawn process that does `mkdir /escape && touch /escape/x`; assert `/escape` does **not** exist on host
- Spawn process that does `ip addr`; assert it shows only `lo` (no host interfaces)

## Acceptance criteria
- [ ] `mini-runc` can run `/bin/ls /` in an Alpine rootfs and you see Alpine's `/` not the host's
- [ ] PID inside namespace is 1 (verifies PID ns)
- [ ] No host network interfaces visible inside (verifies NET ns)
- [ ] All 3 tests pass

## Commit message
`sandbox: clone3-based isolated process spawn (mount/pid/net ns + pivot_root)`

## If you finish early
Wire cgroup.add_process(child_pid) so cgroup limits apply to the spawned process. You'll do this for real Day 10 — but starting today saves time.

## If you fall behind
Drop CLONE_NEWUSER (skip uid mapping) — you'll then need real root to run, but everything else still works. Note this in the README as a v0 limitation.
