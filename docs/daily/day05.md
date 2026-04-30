# Day 05 — Read aider source code (repo map + edit format)

## Why this day matters
aider pioneered two things every modern coding agent borrows: the **repo map** (a token-budgeted view of a codebase) and **search-replace edit blocks** (the format Claude/GPT actually apply reliably). You will reimplement both, in simplified form, in W3. Today is reconnaissance.

## Reading (1)
- aider source — clone:
  ```bash
  git clone https://github.com/Aider-AI/aider ~/code/aider
  cd ~/code/aider
  ```
  Read **only**:
  - `aider/repomap.py` — the whole file
  - `aider/coders/editblock_coder.py` and `aider/coders/editblock_prompts.py`
  - `aider/coders/udiff_coder.py` (skim — for contrast)

  Bonus context: their docs page on [edit formats](https://aider.chat/docs/more/edit-formats.html), but only if you finish the source first.

## Build tasks
Produce `docs/notes/aider/` with two files:

1. **`repo-map.md`** — 300–500 words answering:
   - What is a "repo map" and why does it exist?
   - How does aider rank symbols (PageRank on the call graph)? At what granularity (file? function? class?)?
   - How does it stay within a token budget?
   - What's the cost-per-call (does it run on every turn, or cached)?
   - When would this approach **fail**? (e.g. dynamically-typed Python with heavy reflection)

2. **`edit-formats.md`** — 300–500 words answering:
   - Compare three formats: whole-file replace, search-replace block, unified diff. Which model is best at which?
   - What recovery strategy does aider use when an edit block doesn't match? (fuzzy match? retry? bail?)
   - What's the prompt structure that gets the model to emit clean blocks?
   - Quote the exact instruction text from `editblock_prompts.py`.

Each file: cite ≥ 3 source locations.

## Acceptance criteria
- [ ] Both notes committed
- [ ] You can answer in 60 seconds: "Why search-replace blocks instead of unified diffs?" with a concrete reason from the code

## Commit message
`docs: aider source notes — repo map and edit formats`

## If you finish early
Start `docs/notes/aider/git-integration.md` — how aider does auto-commits, dirty-tree handling, and undo. Useful for W3 sandbox-git interaction.

## If you fall behind
Skip the unified-diff coder. Repo map + search-replace blocks are the must-knows.
