---
artifact: next-session-handoff
purpose: "Single entry point to resume Elenchus and design/build the elenchus-study front end."
read_first: true
supersedes: docs/2026-06-02-next-session-handoff.md
---

# Next session — design + build `elenchus-study`

**Status:** `elenchus-build` (v0.1) is **built and on `main`** — front end, reconciled engine,
council-seat agent, project-scoped Context7 `.mcp.json`, and a README. The engine is **no
longer stale**: it was reconciled to the refined spec (Socratic flow, no readiness verdict,
anonymized questions, checkpoint/resume, Context7). Next phase: the **v0.2 `elenchus-study`**
front end on the *same* engine.

This session is a **discussion-first** kickoff: `elenchus-study` was described in the original
design as "reportedly mostly done already," but no study front end exists in the repo. Decide
what it actually is before writing it.

## Read these, in order
1. `docs/2026-06-02-elenchus-build-summary.md` — the v0.1 spec / source of truth (note study is
   bundled with readiness as the **primary** use case there).
2. `.claude/skills/elenchus-build/SKILL.md` — **the template to mirror.** `elenchus-study` is the
   same shape: thin front end over the engine, supplying triggers / premise shaping / seat lens /
   seat tools / checkpoint / terminal.
3. `.claude/skills/elenchus-council/SKILL.md` — the (now-reconciled) engine. **Do not re-implement
   the loop in the front end.** Study reuses it; confirm it needs no further change for study mode.
4. `docs/2026-06-01-elenchus-build-design.md` §2, §3a — study scope + the v0.2/v1.1 roadmap and
   the "Reader3 wiring" verification gate.
5. `.claude/agents/council-seat.md` — the generic seat (R1 questions / R2 stress-test). Check
   whether study needs a different seat lens or can reuse this one.

## What `elenchus-study` must supply (front-end seam — mirror `elenchus-build`)
- **description / triggers:** study a source — "help me study this <link>", a paper, a chapter,
  docs. Third person, **no loop summary** (CSO trap). Must not overlap `elenchus-build`'s triggers.
- **premise shaping — the read-it-yourself-first protocol:** the user reads the material first and
  states their understanding; the council then quizzes *that* understanding Socratically (R1) and
  stress-tests the answers (R2). Define exactly how the source gets in (paste? link the seats
  WebFetch? Context7 for library docs?).
- **seat lens (study mode):** questions that probe comprehension of the material, not architecture
  risk. Decide: reuse `council-seat` as-is, or add a study-specific instruction block.
- **seat tools:** WebFetch (read the linked source) + Context7 MCP (current library/API docs).
- **terminal:** study → **Q&A / a study path**, not the brainstorming handoff. The user
  self-declares when they understand it; no readiness/comprehension verdict from the judge.
- **checkpoint:** `docs/elenchus/<slug>.md`, same frontmatter pattern (`artifact:
  elenchus-study-session`), write-during-round, scan-on-invoke resume.

## Open questions to resolve in discussion (before writing)
1. **What is "Reader3"?** The design treats it as study-side prep (verification gate 2) and says
   study is "mostly done" — but nothing for it is in the repo. Clarify: a separate reader agent? a
   protocol? Is there prior work elsewhere to import, or do we build from scratch?
2. **Does study reuse the engine loop unchanged,** or does "read-first then quiz" need an engine
   tweak? (Preference: keep the engine mode-agnostic; absorb differences in the front end.)
3. **Source ingestion:** for a paper/chapter, do seats WebFetch the link themselves, or does the
   user paste the text? How does this interact with the read-it-yourself-first discipline?
4. **Trigger boundary** between `elenchus-build` and `elenchus-study` so Claude routes correctly.

## Build approach
Mirror `elenchus-build`; follow the writing-skills discipline
(`docs/2026-06-01-elenchus-build-writing-skills-plan.md`): description = when-only, lean SKILL.md,
rationalization table + red-flags if discipline-bearing, test the trigger and the terminal.
**Restart Claude Code** after any `council-seat.md` change (agents register at session start).

## Kickoff line for the fresh session
"Read docs/2026-06-02-elenchus-study-handoff.md and let's design elenchus-study."
