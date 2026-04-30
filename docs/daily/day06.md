# Day 06 — Read SWE-agent source + finalize blog 1

## Why this day matters
SWE-agent (Princeton) is the academic reference for coding agents on SWE-bench. Reading their **Agent-Computer Interface (ACI)** paper and code teaches you what action-space design looks like at the research-publication level — directly relevant to W4 when you score on SWE-bench yourself.

Also: today the blog ships. A draft that doesn't get published is wasted.

## Reading (1)
- SWE-agent — clone:
  ```bash
  git clone https://github.com/princeton-nlp/SWE-agent ~/code/swe-agent
  ```
  Read **only**:
  - `sweagent/agent/agents.py` — the main agent class
  - `sweagent/environment/swe_env.py` — the bash-based environment
  - `config/default.yaml` — the action space and prompt templates

  Skim their NeurIPS paper abstract + section 3 (ACI design) only if time permits — the code is the primary source.

## Build tasks

### Part A — ACI notes (1 hour)
`docs/notes/swe-agent/aci-design.md`, ~500 words:
- What does "Agent-Computer Interface" mean concretely?
- Compare SWE-agent's `edit` command vs aider's search-replace block vs raw shell `sed` — which fails how?
- What's their `find_file` / `goto` / `scroll_down` design? Why not just give the model `cat` and `grep`?
- One thing you'd steal for mini-harness; one thing you'd reject.

### Part B — Finalize and publish blog 1 (4–5 hours)
- Take yesterday's draft to ~1800 words
- Add the architecture diagram inline
- Add a closing "what's next in this series" pointing at blog 2 (sandbox)
- Have Claude proofread for tone (you write Chinese-flavored English; ask Claude to make it idiomatic without changing structure)
- Create English version → publish to **dev.to** under your real name
- Create Chinese version → publish to **掘金 (juejin.cn)**
- Cross-post English link to: r/LocalLLaMA, r/MachineLearning (Saturday gets best traffic), Hacker News (only if you have a US-friendly title)

### Part C — Wire blog into project
Update `README.md` blog series table: blog 1 status `published`, add both URLs.

## Acceptance criteria
- [ ] ACI notes committed
- [ ] Blog 1 published on dev.to (URL recorded)
- [ ] Blog 1 published on 掘金 (URL recorded)
- [ ] README updated with both URLs
- [ ] You posted the English version to ≥ 1 community

## Commit message
`day6: SWE-agent ACI notes + publish blog 1`

## If you finish early
Set up your personal blog on a custom domain (vercel + nextra, 30 min). Future blogs cross-post here too — owns your SEO long-term.

## If you fall behind
Cut the Chinese version — publish English-only on dev.to. Translate later. **Do not skip publishing.**
