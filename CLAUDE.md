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
  critique), and `elenchus-plan` (plan mode — spec-first: composes over the
  `writing-plans` skill for plan-authoring craft, then **replaces its two solo steps**
  — the "fresh eyes" Self-Review becomes a **plan-check council round**
  (`COVERED / GAPS / DEFECTS` auditing the written plan against the spec), and the
  Scope Check becomes a **deep-tier split suggestion returned to the user for approval
  before any plan file is written**). Gather reuses the engine's fan-out + decorrelated
  seats + dedup + honesty, but has no premise and asks the user nothing between rounds;
  the chairman additionally re-verifies every URL before writing the corpus.
- **Post-execution stage (not a council front end):** `finishing-implementation-elenchus`
  runs *after* code is built. It is a **sequential verify→fix loop**, not the council
  engine: report-only `finishing-verifier` subagents (a no-Write sandbox) drive the running
  app via **Playwright MCP** and return a fixed schema (`PASSED / FAILED / NEEDS-HUMAN /
  MISSING` per acceptance-checklist item); the **chairman implements the fixes** one by one;
  repeat for N passes (default 3) + a free confirm pass. Verifiers observe the browser and
  never edit code; the chairman never verifies — the two halves stay separate. Full pipeline:
  `elenchus-build → brainstorming → elenchus-plan → execution → finishing-implementation-elenchus`.
- **Terminal-UI mockup stage (not a council front end):** `elenchus-tui` designs a
  **pure-ASCII** terminal mockup (one runnable stdlib script with named, navigable
  breakpoint-states + a `<breakpoint>.txt` snapshot each) and then **proves each state
  renders** by driving it in a real terminal. Like finishing it is **generate + verify with
  report-only seats**, not the council engine: one `tui-verifier` seat **per breakpoint**,
  each on its **own isolated tmux session** (`-L` private socket — never the default server),
  dispatched **in parallel**, returning `PASSED / FAILED / NEEDS-HUMAN / MISSING` + a one-line
  design note; the **chairman implements the fixes**. No MCP — tmux runs via `Bash`.

The tool never issues a verdict or green-lights a design — it surfaces contradictions, gaps,
and a study path; the user decides when they are ready. Preserve this: when seats disagree,
report **both** positions and the conditions under which each wins — never smooth into "they
basically agree."

There is no build/test/lint step — this repo is markdown skill/agent definitions, config,
and design docs.
This repo is the home for Elenchus architecture/research planning: it version-controls the
skill sources and the agents (`council-seat`, `finishing-verifier`, `tui-verifier`), and
holds the design docs and validation harness.

## Editing skills & agents — read before changing any SKILL.md or agent file

**Skills and agents follow different rules — do not assume one mirroring convention.**

- **Skills** (`skills/elenchus-build`, `skills/elenchus-study`, `skills/elenchus-gather`,
  `skills/elenchus-plan`, `skills/elenchus-council`, `skills/finishing-implementation-elenchus`,
  `skills/elenchus-tui`):
  the copy Claude Code actually loads is the **global install** (`~/.claude/skills/`).
  Each front end owns its `templates/` (round schemas); the engine owns
  `templates/{seat-base,tiers}.md`. `elenchus-tui` is standalone (no engine templates) and
  ships a `tui-ethos.md` supporting file beside its `SKILL.md`. The top-level `skills/`
  tree in this repo is a **version-controlled archive** — editing it does **not** change
  runtime behavior. Sync any change to the global install too, or the runtime won't see it.
  There is **no `.claude/skills/`**.
- **Agents** (`council-seat.md` for the council; `finishing-verifier.md` for the finishing
  skill; `tui-verifier.md` for the terminal-UI skill): kept as **two copies**. Top-level
  `agents/` is canonical (edit here); `.claude/agents/` is the **derived copy Claude Code
  loads at runtime**. After editing a canonical agent, **mirror it into `.claude/agents/`**
  or the runtime won't see it. Note `tui-verifier` has `Bash` (it needs tmux), so unlike the
  no-Write `council-seat`/`finishing-verifier` sandboxes its report-only guarantee is enforced
  by **hard rules + red-flags**, not structurally.

**Restart required.** Claude Code registers agents/skills at session start. After editing
`council-seat.md`, `finishing-verifier.md`, or `tui-verifier.md`, **start a fresh session**
before dispatching, or `subagent_type: <name>` errors with "agent type not found."

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

**Every Elenchus skill writes under `docs/elenchus/`** (a single shared convention). These
files are private session scratch, so each skill **ensures `docs/elenchus/` is in the
caller project's `.gitignore`** (appending the line, creating the file if needed) before
writing its first checkpoint — the README documents this for users too. The exceptions are
real deliverables the user may commit: gather's `-corpus.*` file (`git add -f`), plan's plan
files under `docs/superpowers/plans/`, and `elenchus-tui`'s script + `<breakpoint>.txt`
snapshots under `mockups/<slug>/`.

`elenchus-build` writes a per-premise checkpoint to `docs/elenchus/<premise-slug>.md`
**during the round, before the user clears context** — so it survives `/clear` and `/compact`.
On re-invoke, the skill reads the checkpoint, and if it's open (`ready: false`) resumes from
the saved round. **Never** rely on SessionEnd hooks to persist state (their ~1.5s timeout can
drop the write).

`elenchus-study` writes **three** files per topic under `docs/elenchus/`:
`<topic-slug>.md` (session checkpoint) + `<topic-slug>-resources.md` (the Round-1 deduped
resource list) + `<topic-slug>-study-plan.md` (the approved phased roadmap). Same
resume-on-invoke + survive-`/clear` discipline as build mode.

`elenchus-gather` writes **two** files per corpus under `docs/elenchus/`:
`<corpus-slug>-gather.md` (session checkpoint + coverage report) + `<corpus-slug>-corpus.<yaml|json|md>`
(the deduped, verified entries in the format the downstream consumer reads). The corpus file
may be written during the round (it carries data, not a recommendation). Same
resume-on-invoke + survive-`/clear` discipline.

`elenchus-plan` writes a per-plan checkpoint to `docs/elenchus/<slug>-plan.md`
(session state: the split proposal + the user's plan-count decision, the plan paths,
and the plan-check `COVERED / GAPS / DEFECTS` + revisions). The **plan files** it
produces land under `docs/superpowers/plans/` and are **real deliverables — not
gitignored** (only the `docs/elenchus/` checkpoint is). Same resume-on-invoke +
survive-`/clear` discipline.

`finishing-implementation-elenchus` writes one run report to
`docs/elenchus/<slug>-finishing.md` (per-item PASSED/FAILED/NEEDS-HUMAN/MISSING across
passes, the fixes the chairman implemented, verifier disagreements, and what remains for
a human). It gitignores `docs/elenchus/` like the others. It has **no resume/checkpoint
loop** — a finishing run is one bounded pass-loop, not a multi-session convene.

`elenchus-tui` writes one run report to `docs/elenchus/<slug>-tui.md` (per-breakpoint
PASSED/FAILED/NEEDS-HUMAN/MISSING across rounds, the chairman's fixes, preserved per-tier
design notes, and what's still NEEDS-HUMAN) — gitignored like the others, and like finishing
it is a **bounded generate→verify→fix loop, no resume/checkpoint**. Its **kept deliverables**
— the runnable `<slug>_tui.py` + one `<breakpoint>.txt` per state — live under
`mockups/<slug>/` and are **not** gitignored (the user reviews and may commit them).

## MCP servers (Context7 + Playwright)

Seats ground frameworks/APIs against current docs via the **Context7 MCP** server, wired in
`.mcp.json`. It reads `CONTEXT7_API_KEY` from the environment (set it in your shell profile);
it runs keyless at lower rate limits and falls back to web search if unset. **Never commit
the key** — it lives in `.env`, which is gitignored. The repo ships no key by design.

The **Playwright MCP** server (`npx @playwright/mcp@latest`) is wired in the same
repo-root `.mcp.json` (project scope — Claude Code has no skill-directory MCP scope). Only
`finishing-implementation-elenchus`'s `finishing-verifier` seats use it, to drive the
running app. Ships no secrets; add `--storage-state <path>` to reuse a logged-in session.

`elenchus-tui` needs **no MCP** — its `tui-verifier` seats drive the terminal via `Bash`
(tmux) directly. (Context7 is available to them for grounding terminal/ANSI facts, the same
session-scoped wiring the other seats use, but the verify loop doesn't require it.)

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
