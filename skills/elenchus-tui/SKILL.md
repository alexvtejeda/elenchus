---
name: elenchus-tui
description: >-
  Use when the user wants a terminal-UI (TUI) mockup designed and then proven to actually
  render — pure-ASCII, no framework — before building the real thing. Triggers: "mock up a
  terminal UI for X", "design a TUI / CLI dashboard I can show someone", "make an ASCII
  wireframe of this terminal app and make sure it renders", "prototype these terminal
  screens and verify the alignment". Generates one runnable stdlib script with named,
  navigable breakpoint-states + a `.txt` snapshot per state, then verifies each in an
  isolated tmux session. NOT the browser/web mockups of visual-companion, NOT stress-testing
  a build premise (elenchus-build), NOT verifying a finished web feature
  (finishing-implementation-elenchus).
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# elenchus-tui (design → parallel tmux-verify loop)

Announce at start: **"I'm using the elenchus-tui skill to design a pure-ASCII terminal
mockup and prove each state renders in an isolated tmux session."**

A standalone Elenchus skill for **terminal UIs**. It mirrors
`finishing-implementation-elenchus` in shape — **generate, then verify with report-only
seats** — but it is **not** an anonymized council (no premise, no gate, no dissent
synthesis). It designs a pure-ASCII mockup and then *proves it renders* by driving it in a
real terminal, one isolated tmux session per state, in parallel.

**Separation of concerns is the whole design** (the #1 thing the baseline got wrong — one
agent designed and graded its own work, produced a false result, and explained it away):

- **`tui-verifier` seats** (one per breakpoint) **only drive tmux → report.** Each opens its
  own private socket, captures the pane across time, measures width, and returns a fixed
  schema. They never edit the mockup.
- **The chairman (this thread)** designs the mockup, reads the reports, reconciles them, and
  **implements the fixes.** Design/repair and verification never live in the same agent.

Read **`tui-ethos.md`** (in this skill dir) before generating — it holds the 80-col grid law,
the width-1 glyph discipline, the flicker-free `paint()`, the too-small guard, and the shared
tmux verify-harness. The reference implementation is **`mockups/council_tui.py`** in this repo.

## The loop

```
a TUI to mock (app + the states/screens it needs)
  │
  ▼
[Gather breakpoints] name the states to show (offer a starter set). Each becomes a seat.
  │
  ▼
[Generate — TUI ethos] ONE runnable stdlib script: named, navigable states + a `--print
  │   <state>` path; pure-ASCII, 80-col, width-1 glyphs, synchronized paint, too-small guard.
  │   Emit `<breakpoint>.txt` per state. Kept under mockups/<slug>/.
  ▼
[Roster gate — EVERY dispatching round] confirm {breakpoint → tier} seat roster + the
  │   seat-call count with the user. One seat per breakpoint, each a unique private socket.
  ▼
[Verify — PARALLEL] dispatch one tui-verifier per breakpoint AT ONCE (own isolated socket
  │   each). Each: force 80×rows, status off, reach the state, capture twice (flicker),
  │   measure visible width, check keys + clean restore → PASSED/FAILED/NEEDS-HUMAN/MISSING
  │   + a one-line design note.
  ▼
[Merge + reconcile] every breakpoint appears; preserve dissenting design notes (don't smooth
  │   to "looks fine"); flag NEEDS-HUMAN honestly.
  ▼
[Fix — chairman only] edit the script for each FAILED/MISSING; re-emit its `.txt`.
  ▼
[Confirm round — PARALLEL, bounded] re-verify (roster re-confirmed). Loop fix→confirm up to
  │   N (default 2). Then stop.
  ▼
[Report] docs/elenchus/<slug>-tui.md (gitignored): per-breakpoint results across rounds, the
        fixes made, preserved design notes, what's still NEEDS-HUMAN. Aesthetic verdict = user's.
```

## Precondition check (before generating)

- **tmux must be available** (`which tmux`). If it isn't, say so — verification can't run, and
  the skill would only produce an unproven mockup. Offer to proceed generate-only (clearly
  labelled unverified) or stop.
- **This machine may have live tmux sessions** (`tmux ls`). Note it: seats must isolate onto
  private `-L` sockets and never touch the default server. This is why verification is done by
  the sandboxed `tui-verifier`, not ad-hoc.

## Gather the breakpoints

Ask what states/screens the TUI needs and give them **short kebab names** — these are the
navigable states, the `--print` targets, the `.txt` filenames, and one verifier seat each.
**Offer a starter set** inferred from the app (e.g. for a sync tool: `syncing / conflict /
done / empty / error`) and let the user trim/add. Fewer, meaningful states beat many thin ones.

## Generate the mockup (TUI ethos)

Write **one runnable stdlib script** to `mockups/<slug>/<slug>_tui.py` following `tui-ethos.md`:

- **Pure-ASCII, no framework.** stdlib only; readable and runnable by anyone.
- **80-col grid**, every framed line padded by **visible** width (strip ANSI; count wide/
  ambiguous glyphs correctly — never `len()`).
- **Width-1 glyph discipline:** own the terminal assumption explicitly (state it in the header)
  or offer an ASCII fallback — do not ship an ambiguous-width gamble as an end-note caveat.
- **Named, navigable states** (one key each) **and** a `--print <state>` path that emits one
  clean ANSI-stripped frame — used to generate each `<breakpoint>.txt` **and** as the width
  target.
- **Flicker-free `paint()`** (DEC-2026 synchronized output + absolute per-line positioning +
  `\x1b[K`), **alt-screen + clean restore**, and a **too-small guard**. Reuse the reference.
- **Emit `mockups/<slug>/<breakpoint>.txt`** for every state (run the `--print` path). These
  frozen snapshots are what the user judges — produce them, don't hand back only the script.

Ground any terminal/ANSI/tmux fact you're unsure of via Context7 before baking it in.

## Roster gate (before EVERY dispatching round)

Both the verify round and each confirm round are dispatching rounds — **confirm the roster
every time**, never just the first. Present and get an OK on:

- **Seats = one per breakpoint.** Each drives its own uniquely-named private socket
  (`tui_<breakpoint>_<run>`), so parallel seats and the user's sessions never collide.
- **Tier per breakpoint.** Default: distribute across `opus` / `sonnet` / `haiku` (assign the
  highest tier — `fable`, else `opus` — to the trickiest state). User may repin.
- **Seat-call count** this round (= number of breakpoints) and the round number.

## Verify — dispatch the seats IN PARALLEL

Unlike the browser finisher (one shared browser → sequential), each tmux seat has its **own
isolated socket**, so **dispatch them in parallel** (all `Agent` calls in one message). Each is
`subagent_type: tui-verifier`, pinned to its tier, and its prompt carries: the **script path**,
the **one breakpoint** to verify, **how to reach it** (the key and the `--print <state>` arg),
the **geometry** (80×rows, rows ≥ frame height), and the **unique socket name**. The agent
enforces the hard rules (private socket, never `kill-server`, force geometry + `status off`,
capture twice across time, measure visible width, keys + clean restore, report-only, the
schema).

## Merge + reconcile

Combine the seat reports. **Every breakpoint must appear** — a dropped one is a reported gap,
not an omission. Keep the per-tier **design notes distinct**: if seats read the same state
differently, **report both** (that is signal about clarity), don't smooth into "looks fine."
**NEEDS-HUMAN** (no tmux, pane won't size) is surfaced, never quietly passed.

## Fix (chairman only) + confirm

- For each **FAILED**/**MISSING**, the chairman edits `<slug>_tui.py` (minimal, ethos-following)
  and **re-emits that breakpoint's `.txt`**. Seats never fix — they have `Bash` but are
  report-only by hard rule.
- Run a **confirm round** (roster re-confirmed, parallel) to prove the fixes and catch
  regressions. Loop fix→confirm up to **N (default 2)**; then stop and report what remains —
  don't grind forever.
- **No verdict.** The skill proves *rendering* (objective: renders, 80-col, no flicker, keys,
  clean restore) and hands over frozen `.txt` snapshots. Whether the design is *good* is the
  user's call — preserve the seats' design notes for them.

## Report + durable state

- **Gitignore `docs/elenchus/` first** (append the line; create `.gitignore` if absent), then
  write `docs/elenchus/<slug>-tui.md`: per-breakpoint PASSED/FAILED/NEEDS-HUMAN/MISSING across
  rounds, the chairman's fixes, preserved design notes, seat disagreements, and what's still
  NEEDS-HUMAN. This checkpoint is private scratch — gitignored.
- **The script + `<breakpoint>.txt` under `mockups/<slug>/` are KEPT deliverables** (not
  gitignored) — reviewable, and the user may commit them.

## Dispatch notes

- Verifier agent = `tui-verifier` (Bash + Read/Grep/Glob + Context7; **no Write/Edit, no
  recursion**). Report-only is enforced by **hard rules + red flags** (it needs `Bash` to run
  tmux, so it is not a no-Write sandbox like `finishing-verifier` — the softer guarantee is
  accepted so each seat drives its own pane).
- **Named-agent fallback + restart.** A freshly-installed `tui-verifier.md` isn't dispatchable
  until Claude Code restarts (agents register at session start). If
  `subagent_type: tui-verifier` errors "agent type not found," fall back to
  `subagent_type: general-purpose` with the tui-verifier hard rules + schema **inlined**, and
  tell the user to restart so the sandbox applies next run.
- **Graceful degradation.** If a tier can't be reached, run the seat on the fallback tier and
  **say so** in the report. Never silently collapse two breakpoints onto one seat.

## Common mistakes (from baseline testing)

- **One agent designing AND grading its own render.** The #1 baseline failure — a self-checking
  designer produced a false result and then explained it away. Verification is a separate,
  report-only seat; only the chairman fixes.
- **Shipping an ambiguous-width glyph gamble as a caveat.** Both baselines used `· ↑ ✓ █ ░ →`,
  passed their own width check (same assumed model), and footnoted "it may shift on a CJK
  terminal." Own the width-1 assumption in the design (or offer an ASCII fallback) — don't
  caveat it.
- **A single static width measure = "it renders."** Missing the flicker/scroll check across
  **time-separated** captures and the keystroke-reaches-the-right-state check. One frame isn't
  proof for a navigable UI.
- **No per-breakpoint `.txt`.** Handing back only the script leaves the user nothing frozen to
  judge. Emit one snapshot per state.
- **Using the default tmux server / bare `kill-server`.** With live sessions on the box this is
  catastrophic. Every seat uses a private `-L` socket and tears down only its own.
- **Reaching for a framework** (curses/rich/blessed) or **ui-ux-pro-max**. stdlib + the TUI
  ethos only.
- **Silently dropping a breakpoint** a seat didn't mention, or smoothing two different design
  notes into one — reconcile every state; preserve dissent.

## Rationalization table (excuse → reality)

| The excuse | The reality |
|---|---|
| "I designed it and my `--check` says 80 cols — it's verified." | The script grading itself is a closed loop. An independent seat capturing the real pane is the verification. |
| "These glyphs are width-1 on normal terminals, I'll just note the risk." | An end-note caveat is the baseline failure. Own the assumption in the design or offer an ASCII fallback. |
| "One capture shows 80 columns, done." | A navigable UI needs two time-separated captures (flicker) + keystroke checks. One frame isn't proof. |
| "The script runs, I don't need the `.txt` files." | The frozen per-state snapshot is what the user judges. Emit one per breakpoint. |
| "I'll just reuse the default tmux server, it's faster." | Live sessions live there; a stray `kill-server` destroys them. Private `-L` socket only. |
| "A seat can tweak the alignment while it's in there." | Seats are report-only (hard rule). Only the chairman edits. |
| "Seats mostly agree it looks fine, ship it." | A FAILED or a divergent design note is signal. Flag it; don't average. |

## Red flags — stop if you catch yourself

- About to have the same agent design the mockup **and** issue its render verdict.
- About to call a state verified from a width self-check **inside the script** (no real capture).
- About to accept a single static frame as proof for a navigable UI (no flicker/key check).
- About to ship ambiguous-width glyphs with a footnote instead of owning the assumption.
- About to run any tmux command **without** `-L <private-socket>`, or a bare `kill-server`.
- About to hand back the script with **no `<breakpoint>.txt`** snapshots.
- About to declare the design "good" — that's the user's call; you prove it *renders*.

## Install / sync

- Skill: `skills/elenchus-tui/` (archive) → sync to `~/.claude/skills/elenchus-tui/` (runtime
  copy Claude Code loads). Includes `SKILL.md` + `tui-ethos.md`.
- Agent: `agents/tui-verifier.md` (canonical) → mirror to `.claude/agents/`; **restart** before
  the first dispatch, or use the named-agent fallback.
- **No MCP required** — tmux runs via `Bash`. (Context7 is available for grounding terminal/ANSI
  facts, the same session-scoped wiring the other seats use; not required for the loop.)
