# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What Elenchus Is

Elenchus is a Claude Code skill suite that makes Claude **argue with itself before agreeing
with you** — a Socratic council that stress-tests a build/architecture premise instead of
giving sycophantic reassurance. Architecture:

- **Chairman** = the main session thread. It owns all orchestration; seats cannot dispatch
  subagents (no recursion).
- **Seats** = `council-seat` subagents dispatched in parallel, each pinned to a model tier
  (Opus / Sonnet / Haiku). Round 1 asks biting questions; round 2 stress-tests the user's
  answers.
- **Engine** (`elenchus-council`) owns the loop, anonymization, dissent-preserving synthesis,
  and the gate. It is invoked by a front end, not triggered directly by ordinary feature
  requests.
- **Front ends** sit over the engine and supply mode specifics (triggers, premise/topic
  shaping, round templates, checkpoint, terminal): `elenchus-build` (build/architecture
  mode — premise-first), `elenchus-study` (research mode — resources-first inverted loop:
  gather → ground → challenge), and `elenchus-gather` (harvest mode — builds a closed
  corpus of verified links/resources: harvest → verify → dedup → coverage report, no
  critique). Gather reuses the engine's fan-out + decorrelated seats + dedup + honesty,
  but has no premise and asks the user nothing between rounds; the chairman additionally
  re-verifies every URL before writing the corpus.

The tool never issues a verdict or green-lights a design — it surfaces contradictions, gaps,
and a study path; the user decides when they are ready. Preserve this: when seats disagree,
report **both** positions and the conditions under which each wins — never smooth into "they
basically agree."

There is no build/test/lint step — this repo is markdown skill/agent definitions, config,
and design docs.
This repo is the home for Elenchus architecture/research planning: it version-controls the
skill sources and the `council-seat` agent, and holds the design docs and validation harness.

## Editing skills & agents — read before changing any SKILL.md or agent file

**Skills and agents follow different rules — do not assume one mirroring convention.**

- **Skills** (`skills/elenchus-build`, `skills/elenchus-study`, `skills/elenchus-gather`,
  `skills/elenchus-council`):
  the copy Claude Code actually loads is the **global install** (`~/.claude/skills/`).
  Each front end owns its `templates/` (round schemas); the engine owns
  `templates/{seat-base,tiers}.md`. The top-level `skills/`
  tree in this repo is a **version-controlled archive** — editing it does **not** change
  runtime behavior. Sync any change to the global install too, or the runtime won't see it.
  There is **no `.claude/skills/`**.
- **Agents** (`council-seat.md`): kept as **two copies**. Top-level `agents/` is canonical
  (edit here); `.claude/agents/` is the **derived copy Claude Code loads at runtime**. After
  editing the canonical file, **mirror it into `.claude/agents/`** or the runtime won't see it.

**Restart required.** Claude Code registers agents/skills at session start. After editing
`council-seat.md`, **start a fresh session** before convening, or
`subagent_type: council-seat` errors with "agent type not found."

**Seat prompts are composed from templates — the engine carries no round schemas.** The
`council-seat` agent is a **thin sandbox** (restricted tools, no recursion); its persona,
round task, and output schema arrive *inside the chairman's dispatch prompt*. That prompt is
composed of: `elenchus-council/templates/seat-base.md` (mode-agnostic persona) +
`elenchus-council/templates/tiers.md` (per-tier adapters) + the **front end's** round
template (`<front-end>/templates/round-N-*.md`, which owns the exact output schema) + the
premise. **Do not re-bake round schemas into the engine `SKILL.md`** — that breaks
mode-agnosticism. New modes add a front end with its own round templates; they reuse the
engine loop unchanged.

## Durable state (checkpoints)

`elenchus-build` writes a per-premise checkpoint to `docs/elenchus/<premise-slug>.md`
**during the round, before the user clears context** — so it survives `/clear` and `/compact`.
On re-invoke, the skill reads the checkpoint, and if it's open (`ready: false`) resumes from
the saved round. **Never** rely on SessionEnd hooks to persist state (their ~1.5s timeout can
drop the write).

`elenchus-study` writes **two** files per topic under `docs/elenchus-study/`:
`<topic-slug>.md` (session checkpoint) + `<topic-slug>-resources.md` (the Round-1 deduped
resource list). Same resume-on-invoke + survive-`/clear` discipline as build mode.

`elenchus-gather` writes **two** files per corpus under `docs/elenchus/`:
`<corpus-slug>-gather.md` (session checkpoint + coverage report) + `<corpus-slug>-corpus.<yaml|json|md>`
(the deduped, verified entries in the format the downstream consumer reads). The corpus file
may be written during the round (it carries data, not a recommendation). Same
resume-on-invoke + survive-`/clear` discipline.

## Context7 MCP

Seats ground frameworks/APIs against current docs via the Context7 MCP server, wired in
`.mcp.json`. It reads `CONTEXT7_API_KEY` from the environment (set it in your shell profile);
it runs keyless at lower rate limits and falls back to web search if unset. **Never commit
the key** — it lives in `.env`, which is gitignored. The repo ships no key by design.

## Conventions

- Skill/agent files: YAML frontmatter (`name`, `description`, `tools`/`allowed-tools`),
  kebab-case names.
- Git: no special branch/PR conventions — ordinary commits to `main` are fine. Commit only
  when asked.

## Source-of-truth docs

- `docs/2026-06-02-elenchus-build-summary.md` — v0.1 spec (read first).
- `docs/2026-06-01-elenchus-build-design.md` — build front-end design doc (companion to the spec).
- `docs/2026-06-02-next-session-handoff.md` — next-phase kickoff + engine reconciliation list.
- `docs/2026-06-01-elenchus-readiness-session.md` — design-decisions log.
- `docs/validation/harness.md` — repeatable validation harness (fixtures + spec-invariant
  rubric + run protocol); recorded runs live in `docs/validation/runs/`.
