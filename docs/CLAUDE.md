# CLAUDE.md — docs/ directory instructions

> Guidelines for working with files in `docs/`.

## File map

| File | Purpose | Who reads |
|---|---|---|
| `plan/PLAN.md` | **SINGLE SOURCE OF TRUTH** — 30-day plan, JD mapping, status table | Everyone |
| `daily/dayNN.md` | Daily task brief: reading, build tasks, acceptance criteria | User + agent |
| `notes/dayNN.md` | Daily log: what was done, pitfalls, LOC count | User writes, agent reviews |
| `notes/paper_summaries.md` | Chinese summaries of all referenced papers | User reads before papers |
| `notes/pi-mono-learning-map.md` | Maps each Day → pi-mono files → interview Qs → handwork | User + agent |
| `AGENT_CONTEXT.md` | Project overview for AI agents | Agents |
| `interview_prep.md` | 76 interview questions + daily practice plan | User writes answers |
| `learning_map.md` | Languages, tools, papers, references, deny list | User |
| `design/` | Architecture diagrams (coming) | User + blog readers |
| `blog/` | Blog drafts (coming) | Blog readers |

## When updating daily briefs
- Each `docs/daily/dayNN.md` has: Reading → Build tasks → Acceptance criteria → Commit message
- Reading section should reference `paper_summaries.md` for papers, not require reading originals
- If the plan changes, update the brief AND `PLAN.md` §10 in the same commit

## When writing notes
- `docs/notes/dayNN.md`: ≤30 lines. Format: what was done, pitfalls, tomorrow's top 3, LOC/commit count
- Never write multi-page analysis docs — the user wants terse, actionable summaries
- Experiment tables: `| 任务 | 成功/失败 | 步数 | token | 观察 |`

## When updating PLAN.md
- §10 status table is the progress tracker — update when user confirms completion
- Daily tasks (Day 1-30) are in §7 — only edit if plan changes
- When plan changes, explain WHY in commit body

## Commit convention for docs
- `docs: <what changed>` — e.g. `docs: update 17 daily briefs to v3.0 alignment`
- `dayNN: <summary>` when the commit includes code + notes for that day
