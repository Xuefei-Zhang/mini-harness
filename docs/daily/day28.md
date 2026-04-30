# Day 28 — Résumé rewrite + JD reverse-engineering

## Why this day matters
Your project does not get you the job — your project + a tightly-aligned résumé does. Today you study the actual JDs of your top 10 target companies, list the exact phrases they use, and rewrite your résumé to mirror that vocabulary while truthfully describing your work.

## Reading (1)
- Collect 10 JDs. Sources:
  - Moonshot, 智谱, MiniMax, 百川, 阶跃, 零一 — 官网 careers pages
  - 字节豆包 — 字节跳动 careers, search "Agent" / "Coze"
  - 阿里通义 — 阿里巴巴招聘, search "agent" / "智能体"
  - 腾讯混元 — 腾讯招聘 / Tencent Careers
  - DeepSeek — their LinkedIn or 招聘页
  - One foreign reach: Anthropic (claude-code team), Cognition, Cursor

  Save raw JD text to `docs/job-search/jds/<company>.md`.

## Build tasks

### Part A — JD analysis (2 hours)
For each JD, extract into `docs/job-search/jd-analysis.md`:

| Company | Role | Required skills (verbatim) | Nice-to-have | Their key phrases |
|---|---|---|---|---|

Then a roll-up table — across all 10 JDs, what phrases recur ≥ 3 times?  Likely candidates:
- "tool calling" / "MCP" / "function calling"
- "multi-agent" / "agent orchestration"
- "evaluation" / "benchmark" / "harness"
- "sandbox" / "code execution environment"
- "context engineering" / "context management"
- "trajectory" / "rollout"

These are the phrases your résumé must contain.

### Part B — Skill mapping (1 hour)
`docs/job-search/skill-map.md` — for each recurring JD requirement, list:
- Have it (with evidence: file/blog/commit URL)
- Have weakly (with mitigation: what specifically you'll mention to make it credible)
- Don't have (with workaround: adjacent skill, or honest gap to flag in interviews)

This becomes your interview cheat sheet.

### Part C — Résumé rewrite (3 hours)
`docs/job-search/resume.md` (markdown source; export to PDF later).

Structure:
1. **Header** — name, GitHub (`mini-harness` link), LinkedIn, email, phone, "Open to: Beijing / Shanghai / Hangzhou / Remote"
2. **Summary** — 3 lines, including the SWE-bench number
3. **mini-harness project** — *first*, before work history. 5 bullets:
   - "Built a 5000-LOC coding-agent harness from scratch in 30 days; achieved X% on SWE-bench Lite"
   - "C++ sandbox: cgroups v2 + seccomp + clone3 namespaces; <500ms cold start"
   - "MCP-protocol tool server consumable by Claude Desktop, opencode, Continue"
   - "Agent loop with 4-provider abstraction (Anthropic / OpenAI / DeepSeek / Qwen), context management, stuck detection"
   - Link: github.com/Xuefei-Zhang/mini-harness | 4 blog posts (link the most-read one)
4. **Work history** — Intel IPU, 7 years. Translate every bullet through an Agent-Infra lens:
   - "Multi-OS driver development (Win/Linux/FreeRTOS)" → emphasis on **portable runtime, IPC, perf-critical paths**
   - "Full stack from app to firmware" → "Comfortable across abstraction boundaries; useful for agent runtime work that spans Python harness, C++ sandbox, kernel APIs"
5. **Open source / writing** — link 4 blog posts with view counts if you have them
6. **Education** — brief

Constraints:
- 1 page if possible, 2 pages absolute max
- Every bullet starts with a verb
- Every bullet has a number where possible
- No "responsible for", no "passionate about"

### Part D — PDF + share
Export to PDF (pandoc + a LaTeX template, or just print-from-Markdown). Save as `Xuefei-Zhang-Resume-2026.pdf` to the repo (yes, commit it — it's part of the project narrative).

## Acceptance criteria
- [ ] 10 JDs collected
- [ ] JD analysis + skill map committed
- [ ] Résumé v1 written, ≤ 2 pages, contains ≥ 3 of the recurring JD phrases naturally
- [ ] PDF generated and committed

## Commit message
`docs: résumé v1, JD analysis across 10 target companies, skill map`

## If you finish early
Have one trusted friend (in industry) read the résumé. Apply edits.

## If you fall behind
Skip the PDF; markdown is fine. JD analysis + résumé are the must-haves.
