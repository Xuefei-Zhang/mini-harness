# Agent Harness 学习地图

> 覆盖完成 mini-harness 项目所需的全部编程语言、工具链、参考资料、和 tiny 项目。
> 按"学完这个才能做那个"的顺序排列。
>
> **前置知识自检** → 先看下面 §零，确认你能过关再往下学。

---

## 零、前置知识自检 + 容器化基础（开始前必须过）

> 你有 7 年系统软件经验，C/C++/Linux 不陌生。但 **容器化原语**（cgroups/seccomp/namespaces）你可能没直接接触过——它们是 Day 8-11 C++ sandbox 的前提。
>
> **总学习时间：~15-20 小时**，建议在 Day 1-7 的空闲时间完成，不要堆到 Day 8。

### 0.1 前置知识自检（每题 1 分钟）

| 你能回答吗？ | 不能 → 先看哪个链接 |
|---|---|
| `fork()` 和 `exec()` 的区别？一个子进程长什么样？ | [fork(2) man page](https://man7.org/linux/man-pages/man2/fork.2.html) |
| Linux 进程如何被信号杀死？`SIGKILL` vs `SIGTERM`？ | [signal(7)](https://man7.org/linux/man-pages/man7/signal.7.html) |
| 系统调用（syscall）是什么？`strace ls` 输出的是什么？ | [syscalls(2)](https://man7.org/linux/man-pages/man2/syscalls.2.html) + 终端跑 `strace ls` |
| C++ 里 `int main()` 如何调用 Linux 原语（`fork`, `execve`, `wait`）？ | 写一个 10 行 C++：`fork()` → 子进程 `execl("/bin/echo", ...)` → 父进程 `wait()` |
| `/proc/<pid>/` 目录是什么？`/proc/self/cgroup` 告诉你什么？ | `ls /proc/self/` + `cat /proc/self/cgroup` |
| `sudo` 是什么？为什么 sandbox 需要 root？ | 知道概念即可 |

**如果以上 6 题你能答对 ≥ 4 题，跳过 0.2，直接看 0.3。**

---

### 0.2 容器化速通（10-12 小时）

**核心认知**：Docker 容器 = process + namespaces + cgroups。没有魔法。

| 主题 | 学什么 | 怎么做 | 学多久 | 链接 |
|---|---|---|---|---|
| **Docker 基础操作** | `docker run`, `docker pull`, `docker ps`, `docker exec`, 镜像/容器/卷 | 终端实操：`docker run --rm alpine echo hello` | 1h | [Docker Getting Started](https://docs.docker.com/get-started/) |
| **Docker  internals** | 一个容器就是一个被 namespace 隔离 + cgroup 限制的进程 | `docker inspect` 看容器的 PID，然后 `ps -ef \| grep <pid>` 验证 | 1h | [How Docker Works](https://docs.docker.com/get-started/overview/) |
| **namespaces 入门** | 6 种 namespace（PID/MNT/NET/UTS/IPC/USER），`unshare` 命令 | 终端实操：`unshare --pid --mount-proc bash`，观察 `ps` 变化 | 2h | [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html) + [unshare(1)](https://man7.org/linux/man-pages/man1/unshare.1.html) |
| **cgroups v2 入门** | unified hierarchy, `memory.max`, `pids.max`, `cpu.max` | 终端实操：`mkdir /sys/fs/cgroup/mytest && echo 500M > /sys/fs/cgroup/mytest/memory.max` | 2h | [cgroups v2 design](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) |
| **seccomp 入门** | `SECCOMP_MODE_FILTER`, 系统调用白名单 vs 黑名单 | 用 `strace` 看一个程序发了哪些 syscall → 思考哪些该允许 | 2h | [seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html) |
| **chroot / pivot_root** | 切换进程的文件系统根目录 | 终端实操：`sudo chroot /var/empty`（空目录），观察什么都访问不了 | 1h | [chroot(1)](https://man7.org/linux/man-pages/man1/chroot.1.html), [pivot_root(2)](https://man7.org/linux/man-pages/man2/pivot_root.2.html) |
| **clone3** | 创建进程的现代 API（替代 `clone()`） | 读 man page，理解 `struct clone_args` | 1h | [clone3(2)](https://man7.org/linux/man-pages/man2/clone3.2.html) |

### 0.3 前置小实验（3-5 小时，必须在 Day 8 前完成）

在开始 Day 8（sandbox 设计）之前，完成这 3 个小实验：

**实验 1：用 `unshare` 手动隔离一个进程**（1h）
```bash
# 开一个 PID 隔离的 shell
unshare --pid --mount-proc bash
# 在里面跑 ps，观察 PID 1 是谁
ps aux
# exit 回到真实环境
```
✅ 通过标准：你能说出 "容器里的 PID 1 不是系统的 PID 1"

**实验 2：用 cgroups 限制内存**（1h）
```bash
# 创建 cgroup
sudo mkdir -p /sys/fs/cgroup/test_limit
echo 10M > /sys/fs/cgroup/test_limit/memory.max
echo $$ > /sys/fs/cgroup/test_limit/cgroup.procs
# 跑一个分配 20M 内存的程序，观察被 kill
python3 -c "x = 'a' * 20_000_000"
```
✅ 通过标准：程序被 OOM kill，`dmesg | tail` 能看到 cgroup 杀进程的记录

**实验 3：用 `strace` 看系统调用**（1h）
```bash
# 看 cat 命令发了哪些 syscall
strace cat /etc/hostname
# 关注：openat, read, write, close
```
✅ 通过标准：你能列出 `cat` 命令的 4 个核心 syscall，并说 "seccomp 就是过滤这些"

---

### 0.4 如果你只有 macOS（没有 Linux）

Day 8-11 的 C++ sandbox **需要 Linux**（cgroups/seccomp 是 Linux-only）。你需要：

| 方案 | 成本 | 推荐度 |
|---|---|---|
| **UTM/Lima Ubuntu VM（mac 本地）** | 免费 | ⭐⭐⭐ 免费，够用，速度慢一些 |
| **Hetzner CAX21 ARM 云** | ~€7/月 | ⭐⭐⭐⭐ 推荐，真 Linux，够跑整个项目 |
| **AWS/Aliyun 按量 Ubuntu 24.04** | 用完即删 | ⭐⭐⭐ 灵活，适合只用 W2 |

**Day 8 的 daily brief 要求你确认 Linux 环境可用。**

---

## 一、Python 现代异步栈（W1 需要）

### 必须掌握的
| 工具 | 学什么 | 学多久 | 链接 |
|---|---|---|---|
| **asyncio** | `async/await`, `gather`, `asyncio.timeout`, `asyncio.Queue` | 2-3h | [Real Python: Async IO](https://realpython.com/async-io-python/)（看到 Using a Queue 为止） |
| **httpx.AsyncClient** | 替换 `requests`，复用连接池，timeout 配置 | 1h | [httpx docs](https://www.python-httpx.org/) |
| **pydantic v2** | `BaseModel`, `Literal`, `Field`, 自定义 validator, JSON serialization | 2h | [Pydantic v2 docs](https://docs.pydantic.dev/) |
| **structlog** | 结构化日志，JSON renderer，每步 emit 一条可 grep 的日志 | 1h | [structlog quickstart](https://www.structlog.org/) |
| **typer** | CLI 参数解析，替代 argparse | 0.5h | [typer tutorial](https://typer.tiangolo.com/) |
| **uv** | 包管理 + 虚拟环境，`uv pip install`, `uv run` | 0.5h | [uv guide](https://docs.astral.sh/uv/) |

### 练手
- `experiments/day02_async_react.py`（计划 Day 2）— 把同步 ReAct 改 async，覆盖以上全部
- Tiny 项目：[https://github.com/encode/httpx](https://github.com/encode/httpx) — 看 examples 中的 `Client` 用法

---

## 二、C++ 系统编程（W2 需要）

### 必须掌握的
| 原语 | 学什么 | 学多久 | 链接 |
|---|---|---|---|
| **cgroups v2** | `pids.max`, `memory.max`, `cpu.max`；写 `/sys/fs/cgroup/...` | 3h | [cgroups v2 design](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) |
| **namespaces** | `CLONE_NEWPID`, `CLONE_NEWNS`, `CLONE_NEWNET`, `CLONE_NEWUTS` | 3h | [namespaces(7)](https://man7.org/linux/man-pages/man7/namespaces.7.html) |
| **clone3** | 替代 `clone()`，传递 `struct clone_args` | 1h | [clone3(2)](https://man7.org/linux/man-pages/man2/clone3.2.html) |
| **seccomp-bpf** | `SECCOMP_FILTER`, `seccomp_rule_add`, 系统调用白名单 | 4h | [seccomp(2)](https://man7.org/linux/man-pages/man2/seccomp.2.html) + [libseccomp guide](https://man7.org/linux/man-pages/man3/libseccomp.3.html) |
| **pivot_root** | 切换根文件系统，构建最小 rootfs | 2h | [pivot_root(2)](https://man7.org/linux/man-pages/man2/pivot_root.2.html) |
| **C++20** | `std::span`, `std::string_view`, `std::format`, 基础模块 | 2h | [cppreference C++20](https://en.cppreference.com/w/cpp/20) |

### 参考项目（读源码，不克隆）
- [runc (containerd)](https://github.com/containerd/runc) — 看 `libcontainer` 的 namespace 设置流程即可
- [bubblewrap](https://github.com/containers/bubblewrap) — 无特权 sandbox，看它怎么用 namespaces
- [nsjail](https://github.com/google/nsjail) — CTF sandbox，看配置结构

### Tiny 项目
- 计划 Day 9-11 的 C++ sandbox 本身就是最好的练习

---

## 三、LLM API & Tool Use（W2-W3 需要）

### 必须理解的协议
| 协议 | 学什么 | 学多久 | 链接 |
|---|---|---|---|
| **Anthropic tool-use** | `tool_use` / `tool_result` content blocks, stop_reason | 1h | [Anthropic tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) |
| **OpenAI function calling** | `function_call` → 内部类型的翻译 | 1h | [OpenAI function calling](https://platform.openai.com/docs/guides/function-calling) |
| **MCP 协议** | JSON-RPC over stdio, `initialize`/`tools/list`/`tools/call` lifecycle | 2h | [MCP spec](https://modelcontextprotocol.io/specification) |
| **Anthropic prompt caching** | `cache_control` breakpoints, hit rate 统计 | 0.5h | [Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) |

### 阅读
- Anthropic [Building effective agents](https://www.anthropic.com/research/building-effective-agents)（最重要的一篇）
- Anthropic [Long context tips](https://docs.anthropic.com/en/docs/build-with-claude/long-context-tips)

---

## 四、Agent 核心机制（贯穿 W1-W3）

### Paper 精读（按优先级）

**阅读策略**：先读 `docs/notes/paper_summaries.md` 中的中文总结（每篇 3-5 分钟），再决定是否需要看原文。
只有 Anthropic "Building Effective Agents" 建议全文阅读，其余看总结 + 关键章节即可。

| Paper | 读什么 | 学多久 | 链接 |
|---|---|---|---|
| **Anthropic: Building effective agents** (必读全文) | workflow vs agent, prompt chaining, routing, orchestrator-workers, evaluator-optimizer, reflection | 1h | [原文](https://www.anthropic.com/research/building-effective-agents) + [总结](docs/notes/paper_summaries.md) |
| **ReAct** | Thought-Action-Observation 循环为什么有效 | 看总结 5min | [总结](docs/notes/paper_summaries.md) \| [arxiv 2210.03629](https://arxiv.org/abs/2210.03629) |
| **Reflexion** | 失败后生成反思 → 下次避免 | 看总结 5min | [总结](docs/notes/paper_summaries.md) \| [arxiv 2303.11366](https://arxiv.org/abs/2303.11366) |
| **Chain of Thought** | abstract + intro | 看总结 3min | [总结](docs/notes/paper_summaries.md) \| [arxiv 2201.11903](https://arxiv.org/abs/2201.11903) |
| **SWE-agent** | ACI 设计，只看 method section | 看总结 5min | [总结](docs/notes/paper_summaries.md) \| [arxiv 2405.15793](https://arxiv.org/abs/2405.15793) |
| **Tree of Thoughts** | 树状搜索 vs 线性推理 | 看总结 3min | [总结](docs/notes/paper_summaries.md) \| [arxiv 2305.10601](https://arxiv.org/abs/2305.10601) |
| **SWE-bench** | 评估流水线、数据格式 | 看总结 5min | [总结](docs/notes/paper_summaries.md) \| [GitHub](https://github.com/SWE-bench/SWE-bench) |

### 源码精读（按优先级）
| 项目 | 读哪些文件 | 链接 |
|---|---|---|
| **opencode** | `src/tool/`, `src/session/`, `src/permission/`, `src/agent/` | [sst/opencode](https://github.com/sst/opencode) |
| **SWE-agent** | `sweagent/agent/agents.py`, `sweagent/environment/swe_env.py` | [princeton-nlp/SWE-agent](https://github.com/princeton-nlp/SWE-agent) |
| **aider** | `aider/repomap.py`, `aider/coders/editblock_coder.py` | [Aider-AI/aider](https://github.com/Aider-AI/aider) |

---

## 五、Evaluation & Harness（W4 需要）

| 工具 | 学什么 | 学多久 | 链接 |
|---|---|---|---|
| **SWE-bench** | 数据格式, evaluation pipeline, Docker 镜像 | 2h | [SWE-bench README](https://github.com/SWE-bench/SWE-bench) |
| **pytest** | `pytest`, `pytest-asyncio`, 基本 fixture | 1h | [pytest docs](https://docs.pytest.org/) |

### 阅读
- SWE-bench Lite dataset 结构：`problem_statement`, `patch`, `test_patch`
- 官方 Docker 镜像：`swebench/sweb.eval.x86_64.*`

---

## 六、KV Cache 原理（W3 需要）

| 资源 | 内容 | 学多久 | 链接 |
|---|---|---|---|
| **Karpathy LLM 课** | KV Cache 部分（约 30 分钟） | 0.5h | [YouTube](https://www.youtube.com/watch?v=kPRA0W1kEC8) |
| **The Illustrated Transformer** | Attention 机制基础 | 1h | [jalammar.github.io](https://jalammar.github.io/illustrated-transformer/) |

### PyTorch（仅 KV Cache demo 用）
| 概念 | 学什么 | 学多久 | 链接 |
|---|---|---|---|
| `nn.Module` | 定义 `TinyAttention` | 1h | [PyTorch 60-min tutorial](https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html) |
| `torch.matmul` | QKV 计算，softmax  | 0.5h | 同上 |

---

## 七、博客 & 技术写作

| 平台 | 用途 | 链接 |
|---|---|---|
| **掘金 (juejin.cn)** | 中文博客首发 | [juejin.cn](https://juejin.cn/) |
| **dev.to** | 英文博客首发 | [dev.to](https://dev.to/) |
| **Hacker News** | 英文博客推广 | [news.ycombinator.com](https://news.ycombinator.com/) |
| **r/LocalLLaMA** | 社区反馈 | [reddit.com/r/LocalLLaMA](https://www.reddit.com/r/LocalLLaMA/) |

### 技术写作参考
- [Blind 7 Java Tier System](https://medium.com/@zoujp2010/blind-7-java-tier-system-e2761fb15fb7) — 看结构，不看内容（如何组织技术博客）
- [Karpathy's blog posts](https://karpathy.github.io/) — 技术博客标杆（代码 + 可视化 + 叙事）

---

## 八、开发工具链

| 工具 | 用途 | 何时用 |
|---|---|---|
| **ruff** | Python lint + format | 每次提交前 |
| **mypy** | Python 类型检查 | 每次提交前 |
| **tokei** | 代码行数统计 | 每周复盘 |
| **excalidraw** | 手绘风架构图 | 写设计文档时 |
| **asciinema** | 终端录屏 | demo 录制 |
| **rich** | 终端美化输出 | trajectory viewer / 进度条 |
| **streamlit** | 快速 Web 可视化 | trajectory viewer |
| **SQLite + FTS5** | 轻量持久化存储 | memory 系统 |

---

## 九、按时间线的使用顺序

| 时间段 | 重点工具/语言 | 对应 Day |
|---|---|---|
| Day 1-2 | Python async, pydantic, httpx, structlog | 1-2 |
| Day 3-5 | LLM API (Anthropic/DeepSeek), prompt engineering | 3-5 |
| Day 6-7 | 读 opencode/aider/SWE-agent 源码 | 6-7 |
| Day 8-11 | C++20, cgroups v2, seccomp, namespaces | 8-11 |
| Day 12-13 | MCP 协议, JSON-RPC | 12-13 |
| Day 14 | Anthropic/OpenAI tool-use schema | 14 |
| Day 15-17 | 无新工具，复用已学 | 15-17 |
| Day 18-21 | Streamlit, SQLite | 18-21 |
| Day 22-27 | SWE-bench, Docker, pytest | 22-27 |
| Day 28-30 | 无新工具，简历 + 投递 | 28-30 |

---

## 十、拒绝列表（不学）

| 不学 | 原因 |
|---|---|
| LangChain / LangGraph | 顶尖公司不用，自己手写更显功力 |
| RAG / 向量数据库 / LangChain | 和 harness 岗几乎无关 |
| Docker（深度） | sandbox 用 cgroups 直接实现，Docker 只会 `docker pull/run` 即可 |
| React / 前端框架 | trajectory viewer 用 streamlit 够了 |
| Kubernetes / Helm | 不在 scope |
| CUDA / Triton | 那是推理岗，不是 harness 岗 |
