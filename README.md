# Elenchus

[![Version](https://img.shields.io/github/v/release/alexvtejeda/elenchus?label=version)](https://github.com/alexvtejeda/elenchus/releases/latest)

![Elenchus — a chairman surrounded by three council seats](assets/elenchus-banner.png)

A Claude Code skill set that makes Claude **argue with itself before it agrees with you** —
a Socratic council that stress-tests a build/architecture idea instead of handing you
sycophantic reassurance. **Elenchus is a critique engine, not an end-to-end scaffolding
tool.** It's meant to *kickstart* a project, or to help you make a hard decision that will
change the direction of an existing one — the moment before you commit, when a bad premise
is cheapest to catch. It does not write your app; it interrogates your reasoning. A chairman
(your main thread) dispatches anonymized seats across model tiers (Opus / Sonnet / Haiku);
they ask the biting questions your premise hasn't answered, you answer them, and they
stress-test your answers. The council flags contradictions and gaps and points you at a
study path — **you** decide when you're ready to build.

> **Need end-to-end scaffolding?** That's not Elenchus's job. For actually *building* the
> thing, reach for a scaffolding framework like [superpowers](https://github.com/obra/superpowers)
> or GSD. Elenchus **bookends** that build instead of replacing it — it critiques and verifies
> at each seam where a wrong turn is expensive, and hands the scaffolding off in the middle:
> use **`elenchus-study`** first to benchmark those (and other) options, let the council
> **stress-test your premise**, then **`elenchus-plan`** to stress-test the resulting plan
> against its spec. Hand that plan to superpowers or GSD to scaffold and execute — then run
> **`finishing-implementation-elenchus`** to verify the built feature in the browser against
> its spec and fix what's missing. Elenchus interrogates and verifies; it doesn't scaffold.

See `docs/2026-06-02-elenchus-build-summary.md` for the v0.1 spec.

## Pipeline

Elenchus is a set of stages you drop into a build, not a single command. The council skills
share one engine; `elenchus-plan` verifies the plan, and the finishing pass is a separate
browser verify→fix loop after the code exists.

```
  elenchus-build / -study / -gather    →  stress-test the premise · research · harvest
            │
            ▼   (spec)
  elenchus-plan                         →  stress-test the plan against its spec
            │
            ▼   (approved plan)
  superpowers / GSD                     →  scaffold + execute   (not Elenchus)
            │
            ▼   (built feature)
  finishing-implementation-elenchus     →  verify in the browser, fix what's missing
```

## Components

| Path in this repo | What it is |
|---|---|
| `skills/elenchus-council/` | The shared council engine (the loop, anonymization, dissent-preserving synthesis, the gate). |
| `skills/elenchus-build/` | The build/architecture front end over the engine. |
| `skills/elenchus-study/` | The research/study front end (resources-first inverted loop). |
| `skills/elenchus-gather/` | The harvest front end — builds a closed corpus of real, verified links/resources (fan-out → verify → dedup → coverage report). |
| `skills/elenchus-plan/` | The plan/verification front end. Composes over the `writing-plans` skill for plan-authoring craft, then replaces its two solo steps — the fresh-eyes Self-Review becomes a **plan-check council round** (`COVERED / GAPS / DEFECTS` auditing the plan against the spec) and the Scope Check becomes a **deep-tier split suggestion returned to you for approval** before any plan file is written. |
| `skills/finishing-implementation-elenchus/` | The post-execution stage (not a council front end). A **sequential verify→fix loop**: report-only verifier subagents drive the running app via **Playwright MCP** and report `PASSED / FAILED / NEEDS-HUMAN / MISSING` per checklist item; the **chairman implements the fixes**. Verifiers observe; only the chairman edits. |
| `skills/visual-companion/` | Standalone browser companion — shows mockups/diagrams/side-by-side comparisons for *visual* questions while the user answers in the terminal (plain HTTP, no WebSockets). Dispatched by a front end (e.g. `elenchus-build` pairs it with `ui-ux-pro-max` for frontend-design questions). |
| `agents/council-seat.md` | One generic council seat, dispatched per tier (Opus / Sonnet / Haiku) by the four council front ends (`elenchus-build`, `-study`, `-gather`, `-plan`). |
| `agents/finishing-verifier.md` | The report-only browser-verification sandbox used by `finishing-implementation-elenchus` — Playwright `browser_*` + Context7 + read tools, **no Write/Edit, no recursion** (report-only by construction). |

## Install

**Cloning the repo is not enough.** Claude Code does not load skills from this repo's
top-level `skills/` directory — that tree is the version-controlled source. You must copy
the skills (and the agent) into a location Claude Code actually scans. Pick **one** scope:

- **Per-project** — usable only inside a given project:
  - skills → that project's `.claude/skills/`
  - agent  → that project's `.claude/agents/`
- **Global** — usable in every project:
  - skills → `~/.claude/skills/`
  - agent  → `~/.claude/agents/`

For example, to install globally from a clone of this repo:

```sh
cp -r skills/elenchus-council skills/elenchus-build skills/elenchus-study skills/elenchus-gather \
      skills/elenchus-plan skills/finishing-implementation-elenchus skills/visual-companion ~/.claude/skills/
cp agents/council-seat.md agents/finishing-verifier.md ~/.claude/agents/
```

(For a per-project install, replace `~/.claude/` with `<your-project>/.claude/`.) The four
council front ends (`elenchus-build`, `-study`, `-gather`, `-plan`) and the shared engine
depend on the `council-seat` agent; `finishing-implementation-elenchus` depends on the
`finishing-verifier` agent instead — copy whichever agents match the skills you install (or
both, to get everything). `visual-companion` is optional (a display helper the front ends
dispatch) and needs no agent. The finishing pass also needs the Playwright MCP server (see
[Playwright MCP](#playwright-mcp-for-the-finishing-pass) below).

> **Restart required.** Claude Code registers agents and skills at session start. After
> copying the files in (or after editing `council-seat.md`), **start a fresh Claude Code
> session** before convening the council, or `subagent_type: council-seat` will error with
> "agent type not found."

## Context7 MCP (recommended)

The seats use the [Context7](https://context7.com) MCP server to ground every framework/API
you mention against **current docs** — so the questions are accurate and the study path
points at real, up-to-date references. The repo ships a project-scoped `.mcp.json` already
wired to Context7; it works **without** a key (lower rate limits), but a free key is
recommended.

**The repo does NOT contain an API key, by design.** `.mcp.json` reads the key from the
`CONTEXT7_API_KEY` environment variable, so you supply your own:

1. Get a free API key at <https://context7.com/dashboard>.
2. Make it available to Claude Code via the environment variable, e.g. add to your shell
   profile (`~/.zshrc`, `~/.bashrc`):

   ```sh
   export CONTEXT7_API_KEY="your-key-here"
   ```

   Then restart the shell (and Claude Code) so it's picked up. Never commit your key.

3. (Optional) Confirm Claude Code sees the server: `claude mcp list` should show `context7`.

If `CONTEXT7_API_KEY` is unset, Context7 still runs keyless at lower rate limits, and the
seats fall back to web search for grounding.

## Playwright MCP (for the finishing pass)

`finishing-implementation-elenchus` drives your running app in a real browser, so its
verifier subagents need the [Playwright](https://github.com/microsoft/playwright-mcp) MCP
server. It's already wired in the repo's project-scoped `.mcp.json` (`npx @playwright/mcp@latest`,
the same project scope as Context7) and ships no secrets. First-run, one-time setup:

1. Approve the project-scoped `playwright` server (via `/mcp`, or restart `claude` and accept
   the project-server prompt). A project MCP server is *pending approval* until you do — check
   with `claude mcp list` (it should show `playwright ✔ Connected`, not `⏸ Pending approval`).
2. Install the browser binary once: `npx playwright install chromium`.
3. **Restart** Claude Code — MCP servers connect at session start.

Until `playwright` shows `✔ Connected`, verifier seats have no browser tools and every
checklist item comes back `NEEDS-HUMAN`. To reuse a logged-in session, add
`--storage-state <path>` to the server's args in `.mcp.json`. The other Elenchus skills don't
need Playwright — only the finishing pass does.

## ui-ux-pro-max (recommended for frontend-design questions)

For *visual* frontend-design questions, `elenchus-build` hands the design thinking to the
**ui-ux-pro-max** skill (styles, palettes, font pairings, layout patterns) and renders the
result through `visual-companion`. It's a separate, third-party skill — install it to get
that path:

- Repo: <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>

Without it, Elenchus still runs fine; the chairman just designs without that extra
intelligence. Note the seats never generate designs — the **chairman** runs ui-ux-pro-max
**once** and pushes the single result to the browser, so this stays token-efficient.

## Where `visual-companion` comes from

`visual-companion` is **not original to Elenchus** — it's adapted from the **brainstorming**
skill in Jesse Vincent's (obra's) `superpowers` repo. That skill is, quite literally, a
markdown file plus a `scripts/` directory, which is what we reshaped here:

- Skill source: <https://github.com/obra/superpowers/tree/main/skills/brainstorming>

We kept its shape (a `SKILL.md` + the browser-companion `scripts/`) and made one substantive
change: **we rewired the WebSocket feature so it only drives an automatic page refresh — it
no longer records an immediate selection.** The reason is that the click-to-select path was
unreliable, and you have to return to the terminal to finish the details anyway. So the
browser is display-only: it auto-refreshes to show the latest frame, and you always **answer
in the terminal**. How you arrange your windows (terminal + browser side by side, or on a
second screen) is entirely up to you.

## Usage

In a Claude Code session in this repo, describe the app/feature you want to build and ask to
have it stress-tested (e.g. *"review my architecture for X before I build"*). Answer the
questions the council surfaces, `/clear` or `/compact` when prompted, then re-invoke to
stress-test your answers. Durable state for each premise lives in `docs/elenchus/<slug>.md`
and survives a context clear.

### Checkpoint files & `.gitignore`

All the Elenchus skills — the four council front ends and the finishing pass — write their
session checkpoints and run reports under **`docs/elenchus/`** in your project. These are
private working scratch, not artifacts to commit — the skills will add a `docs/elenchus/`
line to your project's `.gitignore` automatically before writing the first checkpoint. If
you'd rather set it yourself (or want to be sure), add:

```gitignore
docs/elenchus/
```

Two outputs are real deliverables that live *outside* that ignored scratch: gather's
`docs/elenchus/<slug>-corpus.*` corpus (force-add it with `git add -f <path>` if you want it
tracked) and the plan files `elenchus-plan` writes to `docs/superpowers/plans/` (not ignored).
