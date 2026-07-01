# Elenchus

A Claude Code skill set that makes Claude **argue with itself before it agrees with you** —
a Socratic council that stress-tests a build/architecture idea instead of handing you
sycophantic reassurance. A chairman (your main thread) dispatches anonymized seats across
model tiers (Opus / Sonnet / Haiku); they ask the biting questions your premise hasn't
answered, you answer them, and they stress-test your answers. The council flags
contradictions and gaps and points you at a study path — **you** decide when you're ready
to build.

See `docs/2026-06-02-elenchus-build-summary.md` for the v0.1 spec.

## Components

| Path in this repo | What it is |
|---|---|
| `skills/elenchus-council/` | The shared council engine (the loop, anonymization, dissent-preserving synthesis, the gate). |
| `skills/elenchus-build/` | The build/architecture front end over the engine. |
| `skills/elenchus-study/` | The research/study front end (resources-first inverted loop). |
| `skills/elenchus-gather/` | The harvest front end — builds a closed corpus of real, verified links/resources (fan-out → verify → dedup → coverage report). |
| `skills/visual-companion/` | Standalone browser companion — shows mockups/diagrams/side-by-side comparisons for *visual* questions while the user answers in the terminal (plain HTTP, no WebSockets). Dispatched by a front end (e.g. `elenchus-build` pairs it with `ui-ux-pro-max` for frontend-design questions). |
| `agents/council-seat.md` | One generic council seat, dispatched 3× pinned to different model tiers (Opus / Sonnet / Haiku). |

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
cp -r skills/elenchus-council skills/elenchus-build skills/elenchus-study skills/elenchus-gather skills/visual-companion ~/.claude/skills/
cp agents/council-seat.md ~/.claude/agents/
```

(For a per-project install, replace `~/.claude/` with `<your-project>/.claude/`.) The four
Elenchus skills depend on the `council-seat` agent, so always copy it alongside them.
`visual-companion` is optional (a display helper the front ends dispatch) and needs no agent.

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

## ui-ux-pro-max (recommended for frontend-design questions)

For *visual* frontend-design questions, `elenchus-build` hands the design thinking to the
**ui-ux-pro-max** skill (styles, palettes, font pairings, layout patterns) and renders the
result through `visual-companion`. It's a separate, third-party skill — install it to get
that path:

- Repo: <https://github.com/nextlevelbuilder/ui-ux-pro-max-skill>

Without it, Elenchus still runs fine; the chairman just designs without that extra
intelligence. Note the seats never generate designs — the **chairman** runs ui-ux-pro-max
**once** and pushes the single result to the browser, so this stays token-efficient.

## Usage

In a Claude Code session in this repo, describe the app/feature you want to build and ask to
have it stress-tested (e.g. *"review my architecture for X before I build"*). Answer the
questions the council surfaces, `/clear` or `/compact` when prompted, then re-invoke to
stress-test your answers. Durable state for each premise lives in `docs/elenchus/<slug>.md`
and survives a context clear.
