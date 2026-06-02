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

| Path | What it is |
|---|---|
| `.claude/skills/elenchus-council/SKILL.md` | The shared council engine (the loop, anonymization, dissent-preserving synthesis, the gate). |
| `.claude/skills/elenchus-build/SKILL.md` | The build/architecture front end over the engine. |
| `.claude/agents/council-seat.md` | One generic council seat, dispatched 3× pinned to different model tiers. |

## Install

These are project-scoped — cloning the repo and opening it in Claude Code is enough for the
skills and the `council-seat` agent to be discovered.

> **Restart required.** Claude Code registers agents and skills at session start. After
> cloning (or after editing `council-seat.md`), **start a fresh Claude Code session** before
> convening the council, or `subagent_type: council-seat` will error with "agent type not
> found."

To use them globally instead of per-project, copy the three paths above into your user
config (`~/.claude/skills/...` and `~/.claude/agents/...`).

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

## Usage

In a Claude Code session in this repo, describe the app/feature you want to build and ask to
have it stress-tested (e.g. *"review my architecture for X before I build"*). Answer the
questions the council surfaces, `/clear` or `/compact` when prompted, then re-invoke to
stress-test your answers. Durable state for each premise lives in `docs/elenchus/<slug>.md`
and survives a context clear.
