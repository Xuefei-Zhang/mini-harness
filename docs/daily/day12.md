# Day 12 — Sandbox 集成测试 + 博客 2

## Why this day matters
Day 9-11 你写了 C++ sandbox。今天证明它能干活：写一个完整的 demo，并开写博客 2——这是四篇博客中工程师可信度最高的一篇，因为 LLM agents × Linux internals × C++ 的交集在国内很少有人做。

## Reading (1)
- E2B 源码（sandbox templates）— https://github.com/e2b-dev/E2B/tree/main/packages/python-sdk
  只看 sandbox template 部分，30 分钟。用于博客中的对比段落。

## Build tasks

### Part A — 集成 demo（3 小时）
`experiments/day12_sandbox_demo.py`：
1. 在 sandbox 内写一个小型 Flask 应用
2. 安装依赖（pip install）
3. 启动服务，验证 health check
4. 记录启动延迟、内存使用、吞吐量

写入 `docs/notes/day12-sandbox-bench.md`。

### Part B — 博客 2 草稿（4 小时）
`docs/blog/02-cpp-llm-sandbox.md`，目标 2000 字，今天先写 1200+：

1. **Hook**："每个 coding agent demo 都在跑不受信的代码。几乎没人解释怎么隔离的。这是我的 1500 行 C++ sandbox。"
2. **Threat model** — 200 字
3. **架构图** — 复用 sandbox.md
4. **四大原语** — 每段 200 字 + 代码片段：
   - cgroups v2（memory, CPU, pids）
   - namespaces + clone3
   - seccomp-bpf
   - pivot_root + minimal rootfs
5. **性能数据** — cold-start p50/p95
6. **与 E2B/Modal/Docker exec 对比表**
7. **代码开源** — 链接

## Acceptance criteria
- [ ] sandbox demo 跑通
- [ ] 博客 2 草稿 ≥ 1200 字，8 个章节都有骨架
- [ ] 对比表有你实测的数据

## Commit message
`day12: sandbox integration demo + blog 2 draft`

## If you finish early
- 录制 30 秒 asciinema demo

## If you fall behind
- 博客砍掉第 6-7 节，demo + 草稿是必须的
