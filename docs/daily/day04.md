# Day 04 — Read opencode source code (part 2: agent loop) + start blog 1

## Why this day matters
Yesterday you mapped the data. Today you map the *control flow* — how opencode actually decides what to do next. Then you start writing blog post #1, which is your single biggest recruiter-discovery asset.

## Reading (1)
- Continue with your local opencode clone. Today read only:
  - `packages/opencode/src/agent/` (or `src/runtime/` — whichever holds the main loop)
  - `packages/opencode/src/provider/` — at least the Anthropic and OpenAI providers
  - The single entry point that wires it all together (`cli/run.ts` or similar)

## Build tasks

### Part A — Architecture diagram
Create `docs/notes/opencode/architecture.excalidraw` (or `.png` exported from excalidraw). Required nodes:
- User input → CLI → Session → Agent loop → LLM provider
- Tool registry → Permission gate → Tool execution → Observation
- Trajectory persistence

Make it look like something you'd put on a slide. This will be reused in the blog and possibly in interviews.

### Part B — Start blog 1 draft
Create `docs/blog/01-opencode-from-systems-perspective.md`. **Draft only**, do not publish today.

Outline (write under each heading, 100–200 words):
1. **Why a systems engineer should read agent code** — your background, the gap you're closing
2. **Three abstractions that survived translation from OS kernels**
   - Session ≈ process; Tool ≈ syscall; Permission ≈ capability
   - Cite specific opencode source locations
3. **One thing opencode does well that I didn't expect**
4. **One thing I would design differently coming from a driver background**
5. **What this means for the harness I'm building** (link forward to mini-harness)

Word target: 1500–2000 words finished. Today aim for ~800 words of rough draft.

## Acceptance criteria
- [ ] One architecture diagram committed
- [ ] Blog draft has all 5 sections with at least bullet points; ≥ 800 words total
- [ ] Diagram is referenced from the blog draft

## Commit message
`docs: opencode architecture diagram + blog 1 draft`

## If you finish early
Begin reading aider's `coders/` package — comparison material for blog and for Day 5.

## If you fall behind
Skip the diagram, just describe the architecture in prose. Diagram can be redone in 30 min later.
